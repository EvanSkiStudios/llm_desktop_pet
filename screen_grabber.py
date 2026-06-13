import mss
import mss.tools

from pathlib import Path


def print_screen():
    screenshot_path = Path("screenshot.png")

    with mss.MSS() as sct:
        screenshot = sct.grab(sct.monitors[1])  # Primary monitor
        mss.tools.to_png(
            screenshot.rgb,
            screenshot.size,
            output="screenshot.png"
        )

    return screenshot_path.resolve()
