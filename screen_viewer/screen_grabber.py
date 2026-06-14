from PIL import Image
import mss
import mss.tools
import time

from pathlib import Path

gen_files_dir = Path(__file__).parent.parent / 'generated_files'
gen_files_dir.mkdir(parents=True, exist_ok=True)

# set max image size
MAX_WIDTH = 672
MAX_HEIGHT = 448


def print_screen():
    screenshot_path = gen_files_dir / f"screenshot_{time.time_ns()}.png"

    with mss.MSS() as sct:
        screenshot = sct.grab(sct.monitors[1])

        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        img = img.resize((672, 448))  # or use .thumbnail((640, 360)) for aspect-safe scaling

        img.save(screenshot_path)

    return screenshot_path.resolve()
