#!/usr/bin/env python3
"""
analyze_flow.py - Flow, Meter, and Rhyme Density Analyzer for Rap Lyrics.

Analyzes text for:
- Bar & line count
- Syllable counts per bar
- Rhyme scheme patterns and assonance families
- Multisyllabic rhyme candidates
- Rhythmic consistency & variance
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Common CMU-like vowel phoneme approximations for quick metric detection
VOWEL_PATTERNS = {
    "AY": [r"i[a-z]?e\b", r"\beye\b", r"igh", r"y\b", r"\blie\b", r"\btie\b"],
    "EE": [r"ee", r"ea\b", r"ie\b", r"[a-z]y\b", r"ey\b"],
    "OO": [r"oo", r"ue\b", r"ew\b", r"ou\b", r"u[a-z]?e\b"],
    "OH": [r"oa", r"ow\b", r"o[a-z]?e\b", r"\bgo\b", r"\bno\b", r"\bso\b"],
    "AW": [r"aw", r"au", r"all\b", r"ought\b"],
    "AH": [r"ar\b", r"ah\b", r"a[a-z]?e\b"],
    "IH": [r"i[bcdfghjklmnpqrstvwxyz]", r"in\b", r"it\b", r"is\b", r"ic\b"],
    "EH": [r"e[bcdfghjklmnpqrstvwxyz]", r"ed\b", r"et\b", r"en\b", r"ell\b"],
    "AE": [r"a[bcdfghjklmnpqrstvwxyz]", r"at\b", r"an\b", r"as\b", r"ack\b"],
    "UH": [r"u[bcdfghjklmnpqrstvwxyz]", r"un\b", r"up\b", r"us\b", r"um\b"],
}

def estimate_syllables(word: str) -> int:
    """Heuristic syllable counter for English words."""
    word = word.lower().strip()
    if not word:
        return 0
    # Clean non-alphanumeric except apostrophes
    word = re.sub(r"[^a-z']", "", word)
    if not word:
        return 0
    if len(word) <= 3:
        return 1

    # Exceptions
    word = word.rstrip("e")
    count = len(re.findall(r"[aeiouy]+", word))
    return max(1, count)

def analyze_verse(text: str) -> dict:
    raw_lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    
    # Filter out section headers like [Verse 1] or [Bar 1: ...]
    bars = []
    for line in raw_lines:
        clean_text = re.sub(r"^\[(?:Bar\s*\d+|Verse|Hook|Intro|Outro)[^\]]*\]:?", "", line).strip()
        if not clean_text:
            continue
        words = re.findall(r"[A-Za-z0-9'-]+", clean_text)
        syllables = sum(estimate_syllables(w) for w in words)
        last_word = words[-1].lower() if words else ""
        bars.append({
            "raw": line,
            "text": clean_text,
            "words": words,
            "word_count": len(words),
            "syllable_count": syllables,
            "last_word": last_word
        })

    if not bars:
        return {"error": "No lyrical lines detected"}

    syllable_counts = [b["syllable_count"] for b in bars]
    avg_syllables = sum(syllable_counts) / len(syllable_counts)
    variance = sum((s - avg_syllables) ** 2 for s in syllable_counts) / len(syllable_counts)
    stddev = variance ** 0.5

    # End-rhyme detection (last 2-3 characters phonetic approximation)
    endings = []
    for b in bars:
        w = b["last_word"]
        clean_w = re.sub(r"[^a-z]", "", w)
        endings.append(clean_w[-3:] if len(clean_w) >= 3 else clean_w)

    end_rhyme_matches = sum(1 for i in range(len(endings) - 1) if endings[i] == endings[i+1] or (i > 1 and endings[i] == endings[i-2]))

    return {
        "total_bars": len(bars),
        "total_words": sum(b["word_count"] for b in bars),
        "total_syllables": sum(syllable_counts),
        "avg_syllables_per_bar": round(avg_syllables, 2),
        "syllable_variance": round(variance, 2),
        "syllable_stddev": round(stddev, 2),
        "syllables_per_bar": syllable_counts,
        "end_rhyme_matches": end_rhyme_matches,
        "bars": bars
    }

def print_report(analysis: dict) -> None:
    if "error" in analysis:
        print("Error:", analysis["error"])
        return

    print("=" * 60)
    print("  RAP FLOW & METER ANALYSIS")
    print("=" * 60)
    print(f"  Total Bars:                {analysis['total_bars']}")
    print(f"  Total Syllables:           {analysis['total_syllables']}")
    print(f"  Avg Syllables / Bar:       {analysis['avg_syllables_per_bar']}")
    print(f"  Rhythmic StdDev:           {analysis['syllable_stddev']} (Lower = tighter metric lock; Higher = conversational/syncopated)")
    print("-" * 60)
    print("  BAR BREAKDOWN:")
    for i, bar in enumerate(analysis["bars"]):
        print(f"  [{i+1:02d}] ({bar['syllable_count']:2d} syl | {bar['word_count']:2d} words): {bar['text']}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Analyze flow, meter, and syllables in rap lyrics")
    parser.add_argument("file", nargs="?", help="Path to text/lyrics file (or reads stdin)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON analysis")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    analysis = analyze_verse(text)

    if args.json:
        print(json.dumps(analysis, indent=2))
    else:
        print_report(analysis)

if __name__ == "__main__":
    main()
