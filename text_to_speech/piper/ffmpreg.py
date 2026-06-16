import subprocess
import json

from pathlib import Path

in_gain = 0.5
out_gain = 0.7
delay_1 = 15
delay_2 = 25
delay_3 = 35
delay_1_gain = 0.4
delay_2_gain = 0.3
delay_3_gain = 0.2

aecho_str = (
    f"aecho={in_gain}:{out_gain}:"
    f"{delay_1}|{delay_2}|{delay_3}:"
    f"{delay_1_gain}|{delay_2_gain}|{delay_3_gain}"
)

pitch = 1.03


def ffmpeg_reverb(filename):
    filename = Path(filename)

    output_file = filename.with_stem(
        f"{filename.stem}_reverb"
    )

    sr = get_sample_rate(filename)
    afilter = (
        f"{aecho_str},"
        f"asetrate={sr * pitch},"
        f"aresample={sr}"
    )

    subprocess.run([
        "ffmpeg",
        "-v", "error",
        "-y",
        "-i", str(filename),
        "-af", afilter,
        str(output_file)
    ], check=True)

    return output_file


def get_sample_rate(path):
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate",
        "-of", "json",
        str(path)
    ], capture_output=True, text=True, check=True)

    return int(json.loads(result.stdout)["streams"][0]["sample_rate"])

