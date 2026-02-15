import math
import threading
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk


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
