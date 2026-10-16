# Meter, Flow, and Bar Sheet Notation Guide

This guide explains how to structure, annotate, and evaluate rap verses using standard musical metric notation.

---

## 1. The Standard 16-Bar Verse Structure

Most rap verses consist of **16 bars** (measures), often split into:
- **Bars 1–4 (Opening Quad):** Establishes the rhythmic motive, tone, and opening rhyme family.
- **Bars 5–8 (Development):** Expands the rhyme scheme, introduces daisy-chaining, or crosses the bar line.
- **Bars 9–12 (Climax / Gear Shift):** Metric acceleration, dense multisyllables, or syncopated displacement.
- **Bars 13–16 (Resolution / Punchline Outro):** Deceleration or punchline closure leading into the hook.

(An 8-bar verse follows the same trajectory in compressed form: Bars 1–2 Establish, 3–4 Develop, 5–6 Peak, 7–8 Resolve).

---

## 2. The Bar Sheet Format

When presenting deconstructed lyrics, use this standard annotation format:

```text
[Bar 1 | 1 . 2 . 3 . 4 .] Syllables matching the beat...
[Bar 2 | 1 . 2 . 3 . 4 .] Syllables continuing or crossing...
```

### Subdivision Markers
To indicate exact 16th-note placements:
```text
Beat:  1   e   &   a   2   e   &   a   3   e   &   a   4   e   &   a
Word:  The rhy-me      can't   be      kept            in-
```
Then for the bar-line cross:
```text
Beat:  1   e   &   a   2   e   &   a   3   e   &   a   4   e   &   a
Word:  -SIDE,  it      creeps  in      your            room
```

---

## 3. Syllable & Rhyme Highlighting Conventions

Use phonetic brackets or uppercase highlights to identify rhyme families:

- **[A]**: Primary vowel family (e.g., Long-I `/aɪ/` - *inside / ride / stride*)
- **[B]**: Secondary vowel family (e.g., Short-I `/ɪ/` - *mix / fix / tricks*)
- **[C]**: Tertiary vowel family (e.g., Long-O `/oʊ/` - *flow / slow / glow*)

For multisyllabic rhymes:
> [Bar 1] (man-made a mix) [A-B-C-D]  
> [Bar 2] (band-aid to fix) [A-B-C-D]

---

## 4. Tempo (BPM) & Flow Dynamics

- **Boom Bap / Golden Age (85–95 BPM):** Natural pocket for 16th-note cadences, Rakim, Biggie, Mos Def, and MF DOOM.
- **Southern / OutKast Bounce (75–85 BPM):** Spacious pocket allowing André 3000's syncopated offbeat triplets and laid-back enjambment.
- **Fast / Chopper / Motivic (100–115 BPM):** Kendrick Lamar ("Rigamortus") or Eminem ("Business") driving double-time subdivision bursts and high-velocity motives.

---

## 5. Prosodic Scansion, Lexical Stress & Pocket Budgeting

Proper rap scansion requires that the **natural lexical stress** of conversational English coincides precisely with the **musical downbeats and syncopations** of the measure.

### Syllable Budgeting by Style & Tempo
- **Laid-Back / Jazz Pocket (85–95 BPM - Rakim, Biggie):**
  - **Target:** **10 to 13 syllables per bar**.
  - **Breath & Space:** Leaving deliberate rests on subdivisions (e.g. on Beat 2 or Beat 4) allows the snare drum to hit cleanly and gives the voice a measured, authoritative presence.
  - **Avoid Overcrowding:** Jamming 15–18 syllables into a 90 BPM bar without explicit double-time cadence forces the speaker/vocal model to scramble, slur, and misplace metric accents.
  - **Word Choice:** Avoid clunky, 5-syllable polysyllabic academic words (such as *sub-di-vi-sions*, *in-di-vis-i-bil-i-ty*). Prefer sharp, punchy 1-to-3-syllable words (*grid*, *dots*, *bars*, *ink*, *blueprint*, *cadence*) that fit squarely into 16th-note pockets.

### Lexical Stress Alignment
Every English word has an inherent accent pattern (e.g., *MA-nu-script*, *DIS-ci-pline*, *in-TEL-lect*, *con-TROL*).
- **Rule:** Place syllables with primary lexical stress on musical accents (Beat 1, Beat 2, Beat 3, Beat 4, or accented syncopated offbeats).
- **Violation Example:** Attempting to force *sub-di-vi-sions in to-tal con-trol* into a 2-beat space compresses 8 syllables, flattening the primary stress on *-vi-* and turning the delivery into an unlistenable mumble.

---

## 6. Metrical Feet in Hip-Hop: Iambs, Trochees, Anapests & Dactyls

A high-level emcee (and a properly guided generation model) does not merely count syllables; they consciously govern the **metrical foot** of the line.

### 1. The Four Primary Rap Metrical Feet

| Metrical Foot | Stress Rhythm | Cadence Feel | Emcee Signatures | Concrete Example |
|---|---|---|---|---|
| **Iamb** | $\cup$ — (`0 1`, *da-DUM*) | Upbeat pick-up, resolves heavy on downbeat; calm, regal, measured | **Rakim**, **The Notorious B.I.G.** | *“I DRAFT the CRAFT in the DARK on the PAGE”* |
| **Trochee** | — $\cup$ (`1 0`, *DUM-da*) | Hard downbeat impact, falling offbeat; forward-tumbling, aggressive | **Eminem**, **MF DOOM** | *“HUNCHED in the CEL-lar like a DUN-geon LURK-er”* |
| **Anapest** | $\cup$ $\cup$ — (`0 0 1`, *da-da-DUM*) | Double pickup, explosive punchline resolution; rolling, athletic | **Kendrick Lamar** (*Rigamortus*) | *“break the GRIP”*, *“rip the SCRIPT”*, *“hit the LOCK”* |
| **Dactyl** | — $\cup$ $\cup$ (`1 0 0`, *DUM-da-da*) | Waltz/triplet burst, cascading multisyllabics | **André 3000**, **Eminem** | *“CAN-ni-bal”*, *“AN-i-mal”*, *“PED-es-tal”* |

---

### 2. The Foot Inversion & Stress Clash Trap (The "Sixteen" Problem)

A frequent cause of unnatural delivery in rap lyrics (especially when performed by neural vocal synthesizers like YuE2) is an **accidental foot clash**:

1. **The Iambic Reversal / Rhythm Rule Collision:**
   - Words like *sixteen*, *fourteen*, *unknown*, *bamboo* carry dictionary citation stress on the second syllable (`0 1` — *six-TEEN*).
   - When placed immediately before an accented monosyllable (*dots*, *bars*, *men*), human speech automatically reverses the stress to avoid collision: `SIX-teen dots` (`1 0 1`).
   - **Machine Vocoder Blindspot:** Neural vocoders (trained on raw dictionary citations) read `0 1` followed by `1`, resulting in a jarring stress clash: `six-TEEN DOTS` (`0 1 1`).
2. **Foot Consistency Rule:**
   - If you establish an **iambic** groove (starting on unaccented syllables like *“I walk...”, “And keep...”*), maintain iambic transitions (`0 1 0 1`).
   - If you establish a **trochaic** groove (starting with heavy stressed impacts like *“Hunched in...”, “Cooking...”*), maintain trochaic endings.
   - Never crash an iamb directly into an accented monosyllable without a weak intervening syllable.
