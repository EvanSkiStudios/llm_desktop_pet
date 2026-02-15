import math
import threading
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.overrideredirect(True)  # remove window frame
root.wm_attributes("-topmost", True)

# Set a temporary background color that won't appear in the PNG
transparent_color = "green"  # some color not in your image
root.config(bg=transparent_color)
root.wm_attributes("-transparentcolor", transparent_color)

# Load transparent PNG
image_path = Path(__file__).parent / "character_assets" / "mouse3.png"
pil_image = Image.open(image_path)
image = ImageTk.PhotoImage(pil_image)

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
amplitude = 20  # pixels to move up/down
frequency = 0.5  # speed of bounce
bouncing = False


def bounce():
    global t

    if not bouncing:
        return

    t += frequency
    y = int(amplitude * math.sin(t)) + amplitude  # sine wave movement
    label.place(x=0, y=y)
    root.after(10, bounce)


def pet_start_bounce():
    global bouncing
    if not bouncing:
        bouncing = True
        bounce()


def pet_stop_bounce():
    global bouncing
    bouncing = False


def desktop_pet_end():
    root.destroy()


def input_loop():
    while True:
        user_input = input("> ").lower()

        if user_input == "bounce":
            root.after(0, pet_start_bounce)

        elif user_input == "stop":
            root.after(0, pet_stop_bounce)

        elif user_input == "exit":
            root.after(0, desktop_pet_end)
            break


def pet_window_gui():
    root.mainloop()


def pet_window_end():
    root.after(0, desktop_pet_end)


if __name__ == "__main__":
    threading.Thread(target=input_loop, daemon=True).start()
    root.mainloop()
