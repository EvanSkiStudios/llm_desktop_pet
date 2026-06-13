from pathlib import Path
from PIL import Image, ImageTk


def load_pet_image(filename):
    path = Path(__file__).parent.parent / "character_assets" / filename
    pil = Image.open(path)

    # Define new dimensions as a tuple (width, height)
    new_size = (int(round(pil.width * 0.25)), int(round(pil.height * 0.25)))

    # Resize the image using the high-quality LANCZOS resampling filter
    resized_image = pil.resize(new_size, Image.Resampling.LANCZOS)

    return ImageTk.PhotoImage(resized_image)
