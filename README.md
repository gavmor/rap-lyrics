# rap-lyrics

> Deconstructed hip-hop flow architecture, phonetic rhyme matrices, and prosodic scansion for AI agents and lyricists.

Based on the canonical musicological research in the Vox Earworm documentary *"Rapping, deconstructed: The best rhymers of all time"* (featuring Estelle Caswell and musicologist Martin Connor), alongside academic prior art from Adam Bradley (*Book of Rhymes*), Paul Edwards (*How to Rap*), Eric Malmi (*DopeLearning / DeepBeat*), and Hussein Hirjee & Daniel G. Brown (*ISMIR*).

---

## Features

- **8 Deconstructed Emcee Styles:** Concrete metric blueprints for Kurtis Blow, Rakim, The Notorious B.I.G., Mos Def (Yasiin Bey), André 3000, Eminem, Kendrick Lamar, and MF DOOM.
- **The 16-Dot Metric Grid:** Structural mapping across $4/4$ measures and 16th-note subdivisions with tempo-governed syllable budgeting (10–13 syllables/bar for relaxed boom-bap pockets).
- **Prosodic Scansion & Foot Metricality:** Conscious control over metrical feet (iambic swings, trochaic cascades, anapestic motives) and automatic detection of spondaic stress clashes (e.g. the *Iambic Reversal / Rhythm Rule* collision on *-teen* numbers).
- **Advanced Rhyme Architecture:** Formulas for multisyllabic compound matrices, full-vowel barline crossing onto Beat 1, interlocking daisy-chains, full-line holorimes, and phonetic vowel bending.
- **Deterministic MCP Server (`rap_tools_server.py`):** Offloads combinatorial phonetic calculations and scansion verification to CMUdict tools over the Model Context Protocol, eliminating tokenizer phonetic blindness.
- **Audible Verification via YuE2:** Validated against neural music synthesis models to ensure scansion and rhymes hold up when performed over drum loops.

---

## Master Emcee Style Profiles

| Emcee / Era | Signature Work | Core Flow Mechanics & Metric Architecture |
|---|---|---|
| **Kurtis Blow** | *"The Breaks"* (1980) | Strict AA BB couplets, end rhymes on beat 4, 1-to-1 sentence-to-bar match, single-syllable rhymes. |
| **Rakim** | *"Eric B. Is President"* (1986) | 16-dot grid, internal rhymes, multisyllabic compounds, full-vowel enjambment crossing onto Beat 1, metatheoretical lyricism. |
| **The Notorious B.I.G.** | *"Hypnotize"* (1997) | Daisy chaining (interlocking rhyme families connecting sentences), dynamic phrase length variation (staccato to legato), melodic groove motives. |
| **Mos Def (Yasiin Bey)** | *"Re:Definition"* (2002) | Metric saturation (filling nearly all 16 subdivisions), 4-syllable rhyme blocks sustained over 8–14 bars, clockwork pocket. |
| **André 3000** | *"Aquemini"* (1998) | Syncopated offbeat metric displacement (accents on offbeats `2-&`, `3-a` rather than beats 2 & 4), asymmetrical phrasing, jazz introspection. |
| **Eminem** | *"Business"*, *"Lose Yourself"* (2002) | Vowel bending & slant rhyme matrices (the "orange" principle), syllable-by-syllable phonetic deconstruction, visceral narrative urgency. |
| **Kendrick Lamar** | *"Rigamortus"* (2011) | 3-note anapestic motives (*short-short-long* cadence), motivic daisy-chaining, gear shifting into 4th gear (double-time acceleration). |
| **MF DOOM** | *"Madvillainy"* (2004) | Full-line holorimes (syllable-for-syllable matching), subversive punchlines that pivot to new rhyme families, eccentric supervillain logic. |

*See [`rap-lyrics/references/styles.md`](rap-lyrics/references/styles.md) for full blueprints.*

---

## Neurosymbolic MCP Server (`rap_tools_server.py`)

Transformer LLMs operate on Byte-Pair Encoding (BPE) tokens, which strip phonetic acoustics and syllable counts. This repository bundles a standalone **Model Context Protocol (MCP)** server backed by the CMU pronouncing dictionary (`pronouncing`) to provide ground-truth phonetic calculations:

### Available Tools:
1. **`calculate_rhyme_matrix(anchor_words: list[str]) -> str`**:
   - Calculates exact ARPAbet vowel phonemes (e.g. `page` $\to$ `['EY1']`, `inside` $\to$ `['IH2', 'AY1']`).
   - Surfaces verified single-syllable, 2-syllable, and 3-syllable compound rhyming candidates.
2. **`find_multisyllabic_candidates(phrase: str) -> str`**:
   - Deconstructs multi-word phrases (e.g. *"dots on the page"*, *"Bunsen burner"*) into stressed vowel sequences and generates matching compound rhymes.
3. **`check_scansion_and_flow(lines: list[str], target_bpm: int = 90) -> str`**:
   - Counts exact syllables per bar via CMUdict.
   - Detects overcrowded bars (>13 syllables at 90 BPM) and 5-syllable polysyllables (*subdivisions*).
   - Detects improper enjambment splitting on reduced unstressed prefixes (*con-*, *re-*, *de-*, *sub-*).
   - Detects spondaic stress clashes and *Iambic Reversal* collisions (e.g. *six-TEEN DOTS*).

### Using with `traced-harness`:
```bash
# In-process execution with OpenTelemetry tracing:
traced-harness --server "rap_tools_server:server" \
  --skill /path/to/rap-lyrics/SKILL.md \
  "Use calculate_rhyme_matrix to find rhymes for 'page' and 'inside', then check_scansion_and_flow on your draft."
```

---

## Quick Start & Agent Skill Installation

### Install as an Agent Skill
The portable package is bundled at `rap-lyrics.skill`:
```bash
# Unpack into your agent skills directory:
cp rap-lyrics.skill ~/.agents/skills/
# Or copy the directory directly:
cp -r rap-lyrics/ ~/.agents/skills/rap-lyrics
```

### Flow & Syllable CLI Analyzer
Analyze any verse from the terminal:
```bash
python3 rap-lyrics/scripts/analyze_flow.py path/to/verse.txt
```

### Bar Sheet Grid Formatter
Format lyrics into the standard 16-beat grid notation:
```bash
python3 rap-lyrics/scripts/format_bars.py path/to/verse.txt --bpm 90 --artist "Rakim"
```

---

## Theoretical Foundations

This repository bridges music theory, linguistic prosody, and NLP:

1. **Dual-Meter Theory (Adam Bradley):** Rap operates on the intersection between linguistic speech stress and the rigid $4/4$ musical grid. Tension and release between these two meters produce flow.
2. **Phonetic Slant-Rhyme Hierarchy (Hussein Hirjee & Daniel G. Brown):** Constrained dissimilarity over phonemes—consonant voicing pairs (`/p/` $\leftrightarrow$ `/b/`, `/t/` $\leftrightarrow$ `/d/`, `/k/` $\leftrightarrow$ `/g/`) and vowel tongue-height tolerances.
3. **Rhyme Density Metric (Eric Malmi et al., KDD 2016):** Measuring the longest common vowel subsequences across temporal proximity.
4. **Metrical Feet & The Rhythm Rule:** Balancing iambic ($\cup$ —), trochaic (— $\cup$), and anapestic ($\cup$ $\cup$ —) meters to avoid stress clash collisions in human and neural vocoder performances.

*Read [`rap-lyrics/references/prior_art_and_theory.md`](rap-lyrics/references/prior_art_and_theory.md) for full citations and formal models.*

---

## Audio Artifacts

Pre-rendered 48kHz audio demonstrations generated via YuE2 (3B int8) are available under `audio/`:
- **`audio/rakim_midnight_manuscript_v2.flac`**: Corrected scansion and full-vowel enjambment (`remain in- / -SIDE`).
- **`audio/mf_doom_mad_science_v2.flac`**: Balanced 10-syllable holorime and tight on-beat boom-bap rhythm.
- **`audio/kendrick_sovereign_mortus_v2.flac`**: 3-note short-short-long motivic cadence locked to marching snare.
- **`audio/qwen38_rakim_midnight.flac`**: Lyrical verse generated by Qwen 3.8 27B via `traced-harness`.

Playlists are available in `rap_lyrics_playlist_v2.xspf` and `rap_lyrics_playlist_v2.m3u`.

---

## License

Apache-2.0
