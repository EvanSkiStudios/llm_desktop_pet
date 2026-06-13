import math
import threading
import tkinter as tk

import pygame

from engines.speech_analyzer import extract_amplitude
from window_manager.pet_images import load_pet_image


# =========================================================
# IMAGE LOADING
# =========================================================
def load_images():
    return {
        "idle": load_pet_image("mouse3.png"),
        "thinking": load_pet_image("mouse_thinking.png"),
        "chibi_miku": load_pet_image("chibi_miku.png")
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
    # AUDIO
    # =========================================================
    def play_speech(self, file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

    def speak_and_bounce(self, file):
        self.speech_amplitude, self.seconds_per_step = extract_amplitude(file)
        self.play_speech(file)
        self.bouncing = True

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

