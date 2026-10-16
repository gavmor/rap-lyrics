#!/usr/bin/env python3
"""
rap_tools_server.py - MCP Server for Rap Rhyme Matrix Calculation and Scansion Verification.
Instrumented for traced-harness and Agno agent integration.
"""

import json
import re
import sys
from pathlib import Path
from mcp.server.mcpserver import MCPServer
import pronouncing

server = MCPServer("rap-rhyme-matrix-tools")

# Common reduced prefixes with weak schwa stress
WEAK_PREFIXES = {"con", "com", "re", "de", "pre", "pro", "dis", "sub"}

def extract_word_phones(word: str) -> list[str]:
    clean = re.sub(r"[^a-zA-Z']", "", word).lower()
    if not clean:
        return []
    phones = pronouncing.phones_for_word(clean)
    return phones[0].split() if phones else []

def get_vowel_phonemes(phones: list[str]) -> list[str]:
    return [p for p in phones if any(c.isdigit() for c in p)]

def count_word_syllables(word: str) -> int:
    clean = re.sub(r"[^a-zA-Z']", "", word).lower()
    if not clean:
        return 0
    phones = pronouncing.phones_for_word(clean)
    if phones:
        return pronouncing.syllable_count(phones[0])
    # Fallback heuristic
    vowels = re.findall(r"[aeiouy]+", clean)
    return max(1, len(vowels))

@server.tool()
def calculate_rhyme_matrix(anchor_words: list[str]) -> str:
    """Calculate verified phonetic rhyme families, syllable counts, and vowel structures for anchor words.
    
    Args:
        anchor_words: List of words to build rhyme matrices for (e.g. ['page', 'deep', 'inside', 'soul']).
    
    Returns:
        JSON string containing the exact rhyme family, phonetic vowel assonance, and verified rhyming candidates.
    """
    matrix = {}
    for word in anchor_words:
        clean = re.sub(r"[^a-zA-Z']", "", word).lower()
        if not clean:
            continue
        phones = extract_word_phones(clean)
        vowels = get_vowel_phonemes(phones)
        rhyme_list = pronouncing.rhymes(clean)
        
        # Filter rhymes to common words and sort by length
        filtered_rhymes = [r for r in rhyme_list if len(r) >= 3 and not r.endswith("ide") or r in rhyme_list][:12]
        
        # Categorize rhymes by syllable count
        syl_buckets = {}
        for r in rhyme_list[:30]:
            r_phones = pronouncing.phones_for_word(r)
            if r_phones:
                syl = pronouncing.syllable_count(r_phones[0])
                syl_buckets.setdefault(f"{syl}_syllable", []).append(r)

        matrix[clean] = {
            "vowel_phonemes": vowels,
            "syllables": pronouncing.syllable_count(phones[0]) if phones else count_word_syllables(clean),
            "rhyme_part": pronouncing.rhyming_part(" ".join(phones)) if phones else "",
            "verified_rhymes": filtered_rhymes,
            "multisyllabic_rhyme_options": syl_buckets.get("2_syllable", [])[:6] + syl_buckets.get("3_syllable", [])[:4]
        }
    
    return json.dumps(matrix, indent=2)

@server.tool()
def find_multisyllabic_candidates(phrase: str) -> str:
    """Find multi-syllable compound rhyme candidates matching the vowel assonance of a target phrase.
    
    Args:
        phrase: The multi-word target phrase (e.g., 'dots on the page', 'Bunsen burner', 'break the grip').
    
    Returns:
        JSON analysis of the phrase's stressed vowel sequence and matching compound multi candidates.
    """
    words = [re.sub(r"[^a-zA-Z']", "", w).lower() for w in phrase.strip().split() if w]
    vowel_sequence = []
    total_syllables = 0
    
    for w in words:
        phones = extract_word_phones(w)
        if phones:
            vowels = get_vowel_phonemes(phones)
            vowel_sequence.extend(vowels)
            total_syllables += pronouncing.syllable_count(" ".join(phones))
        else:
            total_syllables += count_word_syllables(w)
    
    # Generate compound multi suggestions for the ending word
    end_word = words[-1] if words else ""
    end_rhymes = pronouncing.rhymes(end_word)[:15] if end_word else []
    
    compounds = []
    for r in end_rhymes:
        r_phones = extract_word_phones(r)
        r_syl = pronouncing.syllable_count(" ".join(r_phones)) if r_phones else 1
        if r_syl >= 2:
            compounds.append(r)
        else:
            # Pair with common rhyming adjectives or adverbs
            compounds.append(f"[modifier] {r}")

    result = {
        "phrase": phrase,
        "total_syllables": total_syllables,
        "vowel_phoneme_sequence": vowel_sequence,
        "multisyllabic_end_candidates": compounds[:10]
    }
    return json.dumps(result, indent=2)

@server.tool()
def check_scansion_and_flow(lines: list[str], target_bpm: int = 90) -> str:
    """Audit rap lyrics for syllable crowding, natural scansion, barline crossing legality, and end-rhyme consistency.
    
    Args:
        lines: List of lyrical lines (bars) to evaluate.
        target_bpm: Target tempo in BPM (defaults to 90 BPM for boom-bap).
    
    Returns:
        JSON report with per-bar syllable counts, warnings for overcrowding or bad enjambment, and rhythm score.
    """
    bar_reports = []
    warnings = []
    total_syllables = 0
    
    max_recommended = 13 if target_bpm <= 95 else 16
    min_recommended = 8
    
    for idx, raw_line in enumerate(lines):
        line = re.sub(r"^\[(?:Bar\s*\d+|Verse|Hook)[^\]]*\]:?", "", raw_line).strip()
        if not line:
            continue
        
        words = [re.sub(r"[^a-zA-Z'-]", "", w) for w in line.split() if w]
        syl_count = sum(count_word_syllables(w) for w in words)
        total_syllables += syl_count
        
        bar_num = idx + 1
        bar_warn = []
        
        # Check overcrowding
        if syl_count > max_recommended:
            bar_warn.append(
                f"Overcrowded bar ({syl_count} syl > {max_recommended} max for {target_bpm} BPM). "
                f"Risk of rushing the pocket or stumbling over the snare."
            )
            warnings.append(f"Bar {bar_num}: Overcrowded with {syl_count} syllables.")
            
            # Check for 5-syllable polysyllables
            for w in words:
                wsyl = count_word_syllables(w)
                if wsyl >= 5:
                    bar_warn.append(f"Contains 5-syllable polysyllabic word '{w}' ({wsyl} syl). Replace with punchy 1-3 syllable words.")
                    warnings.append(f"Bar {bar_num}: Avoid clunky 5-syllable word '{w}'.")
        
        elif syl_count < min_recommended:
            bar_warn.append(f"Thin bar ({syl_count} syl < {min_recommended} min). Ensure deliberate rhythmic pauses fill the space.")
        
        # Check barline enjambment on line ends
        last_word = words[-1].lower() if words else ""
        if last_word.endswith("-"):
            prefix_part = last_word.rstrip("-")
            if prefix_part in WEAK_PREFIXES:
                bar_warn.append(
                    f"Improper scansion enjambment: '{last_word}' splits on a weak reduced prefix. "
                    f"Do not split across unstressed schwa prefixes like 'con-', 're-', 'sub-'. Split on full-vowel words (e.g. 'in-', 'night-')."
                )
                warnings.append(f"Bar {bar_num}: Split on weak reduced prefix '{last_word}'.")

        # Check for foot clash / spondaic collisions (e.g. '01 1' like 'sixteen dots' or '111')
        stresses_list = []
        for w in words:
            clean_w = re.sub(r"[^a-zA-Z']", "", w).lower()
            p = pronouncing.phones_for_word(clean_w) if clean_w else []
            if p:
                stresses_list.append(pronouncing.stresses(p[0]))
        flat_stress = "".join(stresses_list)
        if "0111" in flat_stress or "111" in flat_stress or ("sixteen" in line.lower() and re.search(r"sixteen\s+[a-z]+", line.lower())):
            if "sixteen" in line.lower():
                bar_warn.append("Potential Iambic Reversal clash on 'sixteen': citation stress is '0 1', creating collision with following noun. Replace with 'entire grid' or 'all the dots'.")
                warnings.append(f"Bar {bar_num}: Iambic Reversal clash on 'sixteen'.")
            elif "111" in flat_stress:
                bar_warn.append(f"Spondaic stress clash detected ({flat_stress}). Three consecutive stressed syllables force an awkward collision.")
                warnings.append(f"Bar {bar_num}: Spondaic stress clash.")
        
        bar_reports.append({
            "bar": bar_num,
            "text": line,
            "syllable_count": syl_count,
            "word_count": len(words),
            "warnings": bar_warn
        })
    
    avg_syl = round(total_syllables / len(bar_reports), 2) if bar_reports else 0
    scansion_valid = len(warnings) == 0
    
    return json.dumps({
        "status": "PASS" if scansion_valid else "WARNINGS_FOUND",
        "total_bars": len(bar_reports),
        "total_syllables": total_syllables,
        "avg_syllables_per_bar": avg_syl,
        "target_bpm": target_bpm,
        "warnings_summary": warnings,
        "bar_details": bar_reports
    }, indent=2)

if __name__ == "__main__":
    # When run directly, start stdio server
    server.run()
