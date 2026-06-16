import math
import os
import threading
import tkinter as tk
import ctypes

import warnings

# supress pygame warning
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*"
)

import pygame

from window_manager.speech_analyzer import extract_amplitude
from window_manager.pet_images import load_pet_image

pygame.init()
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)


# =========================================================
# IMAGE LOADING
# =========================================================
def load_images():
    return {
        "idle": load_pet_image("mouse3.png"),
        "thinking": load_pet_image("mouse_thinking.png"),
        "chibi_miku": load_pet_image("chibi_miku.png"),
        "isabel": load_pet_image('isabel.png')
    }


# =========================================================
# WINDOW CLASS
# =========================================================

class DesktopPet:
    def __init__(self):
        # ---------------- WINDOW ----------------
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)

        self.transparent_color = "white"
        self.root.config(bg=self.transparent_color)
        self.root.wm_attributes("-transparentcolor", self.transparent_color)

        # ---------------- STATE ----------------
        self.window_hidden = False

        self.window_x = 0
        self.window_y = 0

        self.bouncing = False
        self.t = 0

        self.speech_amplitude = []
        self.seconds_per_step = 0

        self.is_speaking = False

        # ---------------- PYGAME ----------------
        pygame.mixer.init()

        # ---------------- IMAGES ----------------
        self.images = load_images()
        self.current_image = self.images["idle"]

        # ---------------- LABEL ----------------
        self.label = tk.Label(
            self.root,
            image=self.current_image,
            bg=self.transparent_color,
            borderwidth=0
        )
        self.label.place(x=0, y=0)
        self.label.image = self.current_image

        # ---------------- INITIAL POSITION ----------------
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.buffer = 30

        self.window_x = self.screen_width - (self.current_image.width() + self.buffer)
        self.window_y = self.screen_height - (self.current_image.height() + self.buffer)

        self.update_geometry()

        # ---------------- LOOP ----------------
        self.root.after(16, self.update)

    # =========================================================
    # WINDOW GEOMETRY
    # =========================================================
    def update_geometry(self):
        img = self.label.image
        self.root.geometry(
            f"{img.width()}x{img.height()}+{self.window_x}+{self.window_y}"
        )

    # =========================================================
    # IMAGE CONTROL
    # =========================================================
    def change_image(self, name):
        self.current_image = self.images[name]
        self.label.config(image=self.current_image)
        self.label.image = self.current_image
        self.update_geometry()

    # =========================================================
    # WINDOW CONTROL
    # =========================================================
    def hide(self):
        if self.window_hidden:
            return
        self.window_hidden = True
        self.root.withdraw()

    def show(self):
        if not self.window_hidden:
            return

        self.window_hidden = False
        self.root.deiconify()

        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", self.transparent_color)

        self.update_geometry()

    def toggle(self):
        if self.window_hidden:
            self.show()
        else:
            self.hide()

    # =========================================================
    # PREVENT MOUSE BLOCKING
    # =========================================================

    def set_clickthrough(self, enabled: bool):
        hwnd = self.root.winfo_id()

        ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)

        if enabled:
            ctypes.windll.user32.SetWindowLongW(
                hwnd,
                -20,
                ex_style | 0x20  # WS_EX_TRANSPARENT
            )
        else:
            ctypes.windll.user32.SetWindowLongW(
                hwnd,
                -20,
                ex_style & ~0x20
            )

    def is_mouse_over(self):
        mx = self.root.winfo_pointerx()
        my = self.root.winfo_pointery()

        x1 = self.window_x
        y1 = self.window_y

        img = self.label.image
        x2 = x1 + img.width()
        y2 = y1 + img.height()

        return x1 <= mx <= x2 and y1 <= my <= y2

    # =========================================================
    # AUDIO
    # =========================================================
    def play_speech(self, file):
        self.is_speaking = True

        pygame.mixer.music.load(file)

        pygame.mixer.music.set_volume(0.5)  # 50% volume (0.0 to 1.0)

        pygame.mixer.music.play()

        def wait_and_cleanup():
            if pygame.mixer.music.get_busy():
                self.root.after(50, wait_and_cleanup)
                return

            pygame.mixer.music.stop()

            try:
                pygame.mixer.music.unload()
            except Exception:
                pass

            try:
                os.remove(file)
            except Exception:
                pass

            self.is_speaking = False

        wait_and_cleanup()

    def speak_and_bounce(self, file):
        self.speech_amplitude, self.seconds_per_step = extract_amplitude(file)
        self.bouncing = True
        self.play_speech(file)

    # =========================================================
    # BOUNCE LOGIC
    # =========================================================
    def update_bounce(self):
        if not self.bouncing:
            return

        if not pygame.mixer.music.get_busy():
            self.stop_bounce()
            self.reset_position()
            return

        current_time = pygame.mixer.music.get_pos() / 1000.0
        index = int(current_time / self.seconds_per_step)

        if index >= len(self.speech_amplitude):
            self.stop_bounce()
            self.reset_position()
            return

        amplitude = self.speech_amplitude[index] * 40

        self.t += 0.4
        bounce_offset = int(amplitude * math.sin(self.t)) + amplitude

        self.label.place(x=0, y=bounce_offset)

    def reset_position(self):
        self.label.place(x=0, y=0)

    def start_bounce(self):
        self.bouncing = True

    def stop_bounce(self):
        self.bouncing = False

    # =========================================================
    # MAIN UPDATE LOOP
    # =========================================================
    def update(self):
        if self.is_mouse_over():
            self.set_clickthrough(True)
            self.hide()
        else:
            self.set_clickthrough(False)
            self.show()

        self.update_bounce()
        self.root.after(16, self.update)

    # =========================================================
    # EXIT
    # =========================================================
    def destroy(self):
        self.root.destroy()

    # =========================================================
    # RUN
    # =========================================================
    def run(self):
        self.root.mainloop()


# =========================================================
# OPTIONAL INPUT THREAD (CLI CONTROL)
# =========================================================
def input_loop(pet: DesktopPet):
    while True:
        cmd = input("> ").strip().lower()

        if cmd == "bounce":
            pet.start_bounce()

        elif cmd == "stop":
            pet.stop_bounce()
            pet.reset_position()

        elif cmd == "hide":
            pet.hide()

        elif cmd == "show":
            pet.show()

        elif cmd == "exit":
            pet.destroy()
            break


if __name__ == "__main__":
    pet = DesktopPet()

    threading.Thread(
        target=input_loop,
        args=(pet,),
        daemon=True
    ).start()

    pet.run()

