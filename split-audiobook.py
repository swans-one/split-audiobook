# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "click",
# ]
# ///


"""
Split a .m4b audiobook file into separate chapters.

Usage: `uv run split-audiobook.py SomeAudiobook.m4b`
"""

import click
import json
import math
import pathlib
import subprocess


def make_chap_num_formatter(max_chapters):
    width = math.ceil(math.log(max_chapters + 1, 10))

    def format_chap_num(i):
        return f"{i}".rjust(width, "0")

    return format_chap_num


def process_chapter(infile, outdir, chapter, i, fmt_chap):
    title = chapter.get("tags", {}).get("title", f"Chapter {i}")
    safe_title = title
    start = chapter["start_time"]
    end = chapter["end_time"]
    duration = "{:.6f}".format(float(end) - float(start))
    outfile = outdir / f"{fmt_chap(i)} - {title}{infile.suffix}"

    cmd = [
        "ffmpeg",
        "-ss", start,
        "-i", str(infile),
        "-t", duration,
        "-map", "0:a",
        "-map", "0:v?",
        "-map_chapters", "-1",
        "-codec", "copy",
        "-y",
        str(outfile)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Exited with non zero return code: {result.returncode}")
        print()
        print(result.stderr)
        return None

    print(f"Wrote: {outfile}")
    return outfile


@click.command()
@click.argument('filepath')
def main(filepath) -> None:
    infile = pathlib.Path(filepath).resolve()
    if not infile.is_file():
        raise ValueError("Provided path is not a file")

    outdir = infile.parent / "chapters"

    print("Splitting out audiobook chapters")
    print("From: ", infile)
    print("To: ", outdir)

    ffprobe_result = subprocess.run(
        [
            "ffprobe", "-i", infile,
            "-print_format", "json",
            "-show_chapters", "-show_format"
        ],
        capture_output=True,
        text=True,
    )
    ffprobe = json.loads(ffprobe_result.stdout)
    chapters = ffprobe.get("chapters")
    fmt_chap_num = make_chap_num_formatter(len(chapters))

    if chapters is None or len(chapters) == 0:
        raise ValueError("No chapters found in file")

    outdir.mkdir(exist_ok=True)

    print(f"Processing {len(chapters)} chapters")
    for i, chapter in enumerate(chapters, 1):
        out = process_chapter(infile, outdir, chapter, i, fmt_chap_num)
        if out is None:
            return

if __name__ == "__main__":
    main()
