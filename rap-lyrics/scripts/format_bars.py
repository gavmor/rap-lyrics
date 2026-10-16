#!/usr/bin/env python3
"""
format_bars.py - Format lyrics into 16-beat grid Bar Sheets.

Usage:
    python format_bars.py <lyrics_file> [--bpm BPM] [--artist ARTIST]
"""

import argparse
import re
import sys
from pathlib import Path

def format_lyrics(text: str, bpm: int = 90, artist: str = "") -> str:
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    formatted = []
    
    header = f"=== BAR SHEET NOTATION (Tempo: ~{bpm} BPM"
    if artist:
        header += f" | Style: {artist}"
    header += ") ==="
    formatted.append(header)
    formatted.append("Grid: [Beat 1 . . . | Beat 2 . . . | Beat 3 . . . | Beat 4 . . .]\n")

    bar_num = 1
    for line in lines:
        if line.startswith("[") and ("Verse" in line or "Hook" in line or "Intro" in line or "Outro" in line):
            formatted.append(f"\n{line}")
            continue

        clean = re.sub(r"^\[Bar\s*\d+[^\]]*\]:?", "", line).strip()
        formatted.append(f"[Bar {bar_num:02d} | 1 . 2 . 3 . 4 .] {clean}")
        bar_num += 1

    return "\n".join(formatted)

def main():
    parser = argparse.ArgumentParser(description="Format rap lyrics into bar sheets")
    parser.add_argument("file", nargs="?", help="Input lyrics file")
    parser.add_argument("--bpm", type=int, default=90, help="Tempo in BPM")
    parser.add_argument("--artist", type=str, default="", help="Artist/Style name")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    print(format_lyrics(text, bpm=args.bpm, artist=args.artist))

if __name__ == "__main__":
    main()
