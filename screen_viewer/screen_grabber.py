import mss
import mss.tools
import time

from pathlib import Path

gen_files_dir = Path(__file__).parent.parent / 'generated_files'
gen_files_dir.mkdir(parents=True, exist_ok=True)


def print_screen():
    screenshot_path = gen_files_dir / f"screenshot_{time.time_ns()}.png"

    with mss.MSS() as sct:
        screenshot = sct.grab(sct.monitors[1])  # Primary monitor
        mss.tools.to_png(
            screenshot.rgb,
            screenshot.size,
            output=str(screenshot_path)
        )

    return screenshot_path.resolve()
