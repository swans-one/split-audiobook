# Split Audio Book

Split an .m4b / m4a audiobook with chapter information into separate
.m4a files using ffmpeg.

# Installation

1. Ensure you have `ffmpeg` and `ffprobe` installed on you system.
1. Ensure you have `uv` installed
1. The clone this repo / copy the script `split-audiobook.py` to
   wherever you want it.

# Usage

Just point the script to an audiobook

```
uv run split-audiobook.py /path/to/audiobook.m4b
```

It will create a directory called `chapters` in the same directory as
the audiobook file and place the chapters there.

## Additional Options

- `-s` / `--output-suffix` :: Set the suffix of the output
  file. Defaults to the same suffix as the input file. Usefull if you
  want to rename `.m4b` to `.m4a` for example.
