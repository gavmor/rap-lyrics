---
name: rap-lyrics
description: Write, deconstruct, and analyze rap lyrics, hip-hop verses, bars, and flow schemes in the styles and techniques of master emcees. Use this skill whenever the user asks to write rap lyrics, hip-hop songs, verses, rhymes, or battle bars, or mentions flow architecture, meter, multisyllabic rhymes, crossing the bar line, daisy chaining, holorimes, rhythmic motives, slant rhymes/vowel bending, syncopated metric displacement, or emcees like Rakim, The Notorious B.I.G., Mos Def (Yasiin Bey), André 3000, Eminem, Kendrick Lamar, MF DOOM, or Kurtis Blow, even if they don't explicitly name a specific technique.
---

# Rap Lyrics & Flow Architecture

This skill provides an end-to-end framework for writing, analyzing, and structuring rap lyrics based on the musical and metric mechanics deconstructed in the Vox Earworm study *"Rapping, deconstructed: The best rhymers of all time"*.

Rather than writing generic rhyming couplets, this skill approaches rap as a rigorous musical discipline grounded in 4/4 meter, 16th-note subdivisions, syncopated metric placement, multisyllabic vowel matrices, and distinct emcee traditions.

---

## Core Workflow

Follow this 5-stage process whenever writing or analyzing rap lyrics:

```
1. Profile Selection ──► 2. Metric Setup ──► 3. Rhyme Architecture ──► 4. Verse Generation ──► 5. Deconstruction
   (Artist/Tradition)     (BPM & 16-Grid)     (Multis, Chains, Motives)   (Lyrics & Bar Marks)    (Technique Breakdown)
```

### Stage 1: Select or Identify the Style Profile
If the user specifies an artist or era, adopt that style profile. If no artist is specified, ask or select the profile best suited to their topic (or default to a sophisticated Modern Masterclass combining Rakim, Biggie, and Kendrick techniques).

| Style Profile | Hallmark Techniques | Signature Song Analyzed |
|---|---|---|
| **Kurtis Blow** | Strict AA BB couplets, end rhymes on beat 4, 1-to-1 sentence-to-bar match, single-syllable rhymes | *"The Breaks"* (1980) |
| **Rakim** | 16-dot grid, internal rhymes, multisyllabic compounds, crossing the bar line onto Beat 1, metatheoretical lyricism | *"Eric B. Is President"* (1986) |
| **The Notorious B.I.G.** | Daisy chaining (overlapping rhyme schemes), variable phrase lengths (staccato to legato), melodic groove motives | *"Hypnotize"* (1997) |
| **Mos Def (Yasiin Bey)** | Metric saturation (packing subdivisions), 4-syllable rhyme blocks sustained across 8–14 bars, clockwork precision | *"Re:Definition"* (2002) |
| **André 3000** | Syncopated offbeat metric displacement, shifting accents across subdivisions, conversational jazz phrasing | *"Aquemini"* (1998) |
| **Eminem** | Vowel bending & slant rhymes ("orange" matrix), syllable-by-syllable deconstruction, visceral narrative urgency | *"Business"*, *"Lose Yourself"* (2002) |
| **Kendrick Lamar** | Rhythmic motives (short-short-long), motivic daisy-chaining, gear shifting (accelerating into 4th gear) | *"Rigamortus"* (2011) |
| **MF DOOM** | Holorimes (whole lines rhyming syllable-for-syllable), subversive comic punchlines, oblique associative logic | *"Madvillainy"* (2004) |

*For deep structural profiles, read `references/styles.md`.*

---

### Stage 2: Establish the Metric Foundation (The 16-Grid)
Every bar is a measure of 4 beats in 4/4 time, subdivided into 16 sixteenth-notes:
`[1 - e - & - a] [2 - e - & - a] [3 - e - & - a] [4 - e - & - a]`

- **Determine Tempo & Pocket:**
  - *Boom-Bap / Golden Age:* 85–95 BPM (Rakim, Biggie, Mos Def, MF DOOM).
  - *Southern Swing / Jazz Pocket:* 75–85 BPM (André 3000).
  - *High-Velocity / Motivic:* 100–115 BPM (Kendrick Lamar, Eminem).
- **Target Bar Length:** Standard verses are 16 bars (or 8 bars for a compressed showcase). Group bars into 4-bar quads:
  - Bars 1–4: Motif & opening rhyme family.
  - Bars 5–8: Daisy chaining & barline crossing.
  - Bars 9–12: Metric acceleration or syncopated peak.
  - Bars 13–16: Resolution or punchline climax.

*For meter, counting, and tempo dynamics, read `references/meter_and_flow.md`.*

---

### Stage 3: Engineer the Rhyme & Flow Architecture
Apply the specific mechanics demanded by the style:

1. **Multisyllabic (Compound) Rhyming:** Match 2 to 5 consecutive syllables across words based on vowel assonance rather than dictionary consonants (e.g., *man-made a mix* / *band-aid to fix*).
2. **Crossing the Bar Line (Enjambment):** Do not end every sentence at the barline. Allow a phrase to end Bar 1 and land its resolving syllable squarely on **Beat 1 of Bar 2** (e.g., *"The rhyme can't be kept in- / [Bar 2, Beat 1] -side"*).
3. **Daisy Chaining:** Interlock vowel sounds. Before Rhyme Family A finishes, introduce Rhyme Family B. Conclude A, continue B, introduce C.
4. **The Holorime (DOOM Style):** Craft paired bars where every syllable in the setup line rhymes with the corresponding syllable in the punchline.
5. **Rhythmic Motives (Kendrick Style):** Establish a short rhythmic cell (such as *short-short-long*, e.g., two sixteenths + an eighth note) and repeat that rhythmic cadence across lines.
6. **Vowel Bending / Slant Rhymes (Eminem Style):** Manipulate pronunciation to force near-rhymes into sonic alignment across stressed beats (e.g., *orange / door hinge / storage / porridge*).
7. **Metric Displacement (André Style):** Shift rhyme placements away from beats 2 and 4 onto the offbeats (`2-&`, `3-a`).
8. **Prosodic Scansion & Natural Stress Invariant:** Ensure every word's natural spoken accent aligns with musical downbeats and syncopations. When crossing the bar line, never split on an unstressed reduced prefix (avoid *con- / -fined*); only split compound words with full vowel weight (*in- / -side*, *night- / -time*) or wrap complete phrases (*pen starts to / [Beat 1] WRITE*). In standard boom-bap (85–95 BPM), budget 10–13 syllables per bar to let the snare drum breathe; avoid 5-syllable polysyllables (*subdivisions*) that crowd the pocket.
9. **Jargon & Acronym Phonetic Expansion Invariant (The "Bee-mats" Rule):** Technical shorthand, gaming slang, and military acronyms (e.g. *Bmats*, *Rmats*, *RPG*, *FMC*) MUST be rendered in phonetic spelling (e.g. *Bee-mats*, *Are-mats*, *R-P-G*) to prevent neural vocoders from emitting mangled consonant clusters or spelling out letters awkwardly. Assign each term its exact metrical foot (e.g., *"Bee-mats"* is a trochee `1 0`: *“BEE-mats in the bed, DIE-sel in the tank”*).
10. **Metrical Foot Discipline & Clash Prevention:** Consciously govern whether lines are driven by an **iambic motor** ($\cup$ —, upbeat pickup) or a **trochaic motor** (— $\cup$, downbeat attack). Prevent spondaic stress clashes (`0 1 1`) by avoiding dictionary citation compounds (*six-TEEN*) immediately before stressed nouns (*DOTS*); use trochees or intervening unstressed words (*“all the dots”*, *“the entire grid”*).

*For full formulas and phonetic examples, read `references/techniques.md`.*
*For academic foundations, dual-meter poetics, and phonetic research (Bradley, Edwards, Hirjee & Brown, Malmi), read `references/prior_art_and_theory.md`.*

---

### Stage 4: Output Formats

Support both a single-verse showcase (8–16 bars) and full-length multi-section song architectures (~60–68 bars, 3:00–3:30 min):

#### Full Song Template (Radio / Album Structure)
```markdown
# [Track Title]
**Style Profile:** [Artist Name or Hybrid]
**Tempo:** [e.g., 90 BPM | 4/4 Time]
**Dominant Metrical Foot:** [e.g., Iambic swing with trochaic chorus symmetry]
**Phonetic Jargon Expansions:** [e.g., Bmats -> Bee-mats (trochee: 1 0)]

[Intro] (4 bars: setting the scene, radio atmosphere, rhythm establishing)
[Verse 1] (16 bars: core narrative, stockpile/conflict establishment, 16-dot grid, Beat 1 enjambment)
[Chorus] (8 bars: anthemic refrain, symmetrical hemistichs like "Bee-mats in the bed, diesel in the tank")
[Verse 2] (16 bars: escalating action, technical multisyllabic matrices and holorime showcases)
[Chorus] (8 bars: anthemic refrain)
[Verse 3 / Climax] (12-16 bars: river/combat gauntlet, tempo acceleration or gear shift)
[Outro] (4 bars: formal military/thematic signoff and musical fadeout)
```

---

## Bundled Helper Tools

When generating or validating verses, use the bundled scripts in `scripts/`:

### Flow & Syllable Analysis
Run `scripts/analyze_flow.py` on any lyrics file to verify syllable distribution, detect average syllables per bar, check rhythmic variance (standard deviation), and count rhyme density:
```bash
python scripts/analyze_flow.py path/to/lyrics.txt
# Or get JSON metrics:
python scripts/analyze_flow.py path/to/lyrics.txt --json
```

### Bar Sheet Grid Formatting
Run `scripts/format_bars.py` to format raw lyrics into standard 16-beat grid notation:
```bash
python scripts/format_bars.py path/to/lyrics.txt --bpm 92 --artist "Rakim"
```

### Deterministic Rhyme Matrix & Scansion MCP Server
Run or connect `scripts/rap_tools_server.py` (compatible with `traced-harness --server "rap_tools_server:server"`) to offload phonetic calculations and metric scansion to deterministic CMUdict tools:
- `calculate_rhyme_matrix(anchor_words)`: Computes verified phonetic vowel assonance, rhyming candidates, and multisyllabic options for anchor words.
- `find_multisyllabic_candidates(phrase)`: Deconstructs target phrases into stressed vowel sequences and generates matching multi-word compound rhymes.
- `check_scansion_and_flow(lines, target_bpm)`: Audits verses for syllable crowding (>13 syl at 90 BPM), weak prefix splits (`con-`), and metric alignment.
