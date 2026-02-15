import os
import tkinter as tk
import pygame
import math
import threading
from pathlib import Path
from PIL import Image, ImageTk

from speech_analyzer import extract_amplitude

root = tk.Tk()
root.overrideredirect(True)  # remove window frame
root.wm_attributes("-topmost", True)

# Set a temporary background color that won't appear in the PNG
transparent_color = "white"  # some color not in your image
root.config(bg=transparent_color)
root.wm_attributes("-transparentcolor", transparent_color)


def load_image(filename):
    path = Path(__file__).parent / "character_assets" / filename
    pil = Image.open(path)
    return ImageTk.PhotoImage(pil)


# Preload all images once
images = {
    "idle": load_image("mouse3.png"),
    "thinking": load_image("mouse_thinking.png"),
}


def change_image(name):
    new_image = images[name]
    label.config(image=new_image)
    label.image = new_image
    root.geometry(f"{new_image.width()}x{new_image.height()}+{x}+{y}")


image = images["idle"]
label = tk.Label(root, image=image, bg=transparent_color, borderwidth=0)
label.pack()

# Position bottom-right
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = screen_width - image.width()
y = screen_height - image.height()
root.geometry(f"{image.width()}x{image.height()}+{x}+{y}")


# Bounce variables
t = 0  # time counter
speech_amplitude = []
seconds_per_step = 0
bouncing = False


def bounce():
    global t

    if not bouncing:
        return

    # Stop if audio finished
    if not pygame.mixer.music.get_busy():
        stop_bounce()
        label.place(x=0, y=0)  # reset position
        return

    current_time = pygame.mixer.music.get_pos() / 1000.0
    index = int(current_time / seconds_per_step)

    if index >= len(speech_amplitude):
        stop_bounce()
        label.place(x=0, y=0)
        return

    dynamic_amplitude = speech_amplitude[index] * 40

    t += 0.4
    y_offset = int(dynamic_amplitude * math.sin(t)) + dynamic_amplitude

    label.place(x=0, y=y_offset)

    root.after(16, bounce)


pygame.mixer.init()


def play_speech(speech_file):
    pygame.mixer.music.load(speech_file)
    pygame.mixer.music.play()


def speak_and_bounce(speech_file):
    global speech_amplitude, seconds_per_step

    speech_amplitude, seconds_per_step = extract_amplitude(speech_file)

    play_speech(speech_file)
    start_bounce()
    check_music_end_and_cleanup(label, stop_bounce, speech_file)


def check_music_end_and_cleanup(label, bounce_stop_callback, audio_file="speech.wav"):
    """
    Checks if pygame music has finished. If so:
    - Stops bouncing via bounce_stop_callback()
    - Unloads the music
    - Deletes the speech file
    Should be repeatedly scheduled via root.after().

    Args:
        label: The Tkinter label for your character (used to reset position if needed)
        bounce_stop_callback: Function to stop the bounce
        audio_file: Path to the speech file to delete
    """
    # If music finished
    if not pygame.mixer.music.get_busy():
        # Stop the bounce
        bounce_stop_callback()
        # Reset character position
        label.place(x=0, y=0)
        # Unload music from mixer so file is released
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.unload()
        except pygame.error:
            pass  # ignore if already unloaded
        # Delete the speech file
        path = Path(audio_file)
        if path.exists():
            try:
                os.remove(path)
            except PermissionError:
                # Windows sometimes needs a short delay
                print(f"Failed to delete {audio_file}, retry later")
    # Re-schedule check
    root.after(100, lambda: check_music_end_and_cleanup(label, bounce_stop_callback, audio_file))


def start_bounce():
    global bouncing
    if not bouncing:
        bouncing = True
        bounce()


def stop_bounce():
    global bouncing
    bouncing = False


def desktop_pet_end():
    root.destroy()


def input_loop():
    while True:
        user_input = input("> ").lower()

        if user_input == "bounce":
            root.after(0, start_bounce)

        elif user_input == "stop":
            root.after(0, stop_bounce)

        elif user_input == "exit":
            root.after(0, desktop_pet_end)
            break


def window_gui():
    root.mainloop()


def window_end():
    root.after(0, desktop_pet_end)


if __name__ == "__main__":
    threading.Thread(target=input_loop, daemon=True).start()
    root.mainloop()
