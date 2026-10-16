# Theoretical Foundations & Prior Art in Computational Hip-Hop

This document synthesizes the foundational academic literature, musicological research, and computational linguistics frameworks underpinning the `rap-lyrics` skill.

---

## 1. Key Academic Literature & Canon

### A. Adam Bradley — *Book of Rhymes: The Poetics of Hip Hop* (Basic Books, 2009 / 2017)
* **Core Contribution:** The definitive literary and formal poetic treatise on rap music.
* **The Dual-Meter Theory:** Bradley posits that rap operates simultaneously on two distinct meters:
  1. **The Poetic Meter:** The natural linguistic rhythm of English speech stresses (accentual-syllabic rhythm).
  2. **The Musical Meter:** The rigid $4/4$ framework of the musical beat (typically divided into 16 sixteenth-note subdivisions).
* **Flow as Metric Tension:** Authentic flow is created by the dynamic tension between these two meters. When an emcee strictly adheres to the downbeats, the flow is predictable (early old-school); when an emcee delays, anticipates, or enjambs across the barline (Rakim, André 3000), they create syncopated polyrhythms over the musical grid.
* **Rhyme Taxonomy:** Formalizes the taxonomy of rap rhyming:
  - *End Rhymes* vs. *Internal Rhymes*
  - *Multisyllabic (Compound) Rhymes*
  - *Mosaic Rhymes* (rhyming one multi-syllable word with multiple single-syllable words)
  - *Slant / Assonance Rhymes* (vowel-matching across consonants)
  - *Apocopated Rhymes* (rhyming the accented syllable of one word with a multi-syllable word)

---

### B. Paul Edwards — *How to Rap: The Art and Science of the Hip-Hop MC* (Chicago Review Press, 2009 / 2013)
* **Core Contribution:** An empirical manual of flow architecture compiled from in-depth interviews with over 100 veteran emcees (including Rakim, Kool G Rap, Big Daddy Kane, Chuck D, and Pharoahe Monch).
* **Key Flow Mechanics:**
  - **Diagramming Flow:** Emcees mentally or visually chart syllables across 16 subdivisions per measure, leaving rests on downbeats (beats 2 and 4) to let the snare drum breathe.
  - **The 16-Bar Stanza:** Standardizing the structural progression of verses into four 4-bar quads (Establishment $\to$ Expansion $\to$ Climax $\to$ Closure).
  - **The Craft of Multis:** Edwards documents how multisyllabic rhyming emerged in the late 1980s (championed by Kool G Rap and Rakim) as the universal benchmark of technical emceeing.

---

### C. Hussein Hirjee & Daniel G. Brown — *Automatic Detection of Internal and Imperfect Rhymes in Rap Lyrics* (ISMIR 2009, 2010)
* **Core Contribution:** Pioneered the application of bioinformatics sequence alignment (Needleman-Wunsch / Smith-Waterman) to phonetic transcripts (CMUdict) to detect internal and slant rhymes in hip-hop.
* **Articulatory Phonetic Distance:** Hirjee & Brown demonstrated that rap rhymes are governed by constrained phonetic dissimilarity:
  - **Consonant Voicing Pairs:** Consonants sharing place of articulation but differing only in voicing form natural slant codas:
    - `/p/` $\leftrightarrow$ `/b/`, `/t/` $\leftrightarrow$ `/d/`, `/k/` $\leftrightarrow$ `/g/`, `/s/` $\leftrightarrow$ `/z/`, `/f/` $\leftrightarrow$ `/v/` (e.g., *ricochet* / *trigger say*).
  - **Manner-Sharing Consonants:** Nasals (`/m/` $\leftrightarrow$ `/n/`, e.g., *frame* / *rain*) and liquids (`/r/` $\leftrightarrow$ `/l/`).
  - **Vowel Distance (The "Orange" Principle):** Vowels sharing tongue height or backness can be bent into assonance by manipulating performance stress.

---

### D. Eric Malmi et al. — *DopeLearning: A Computational Approach to Rap Lyrics Generation* (ACM KDD 2016)
* **Core Contribution:** First large-scale neural ranking engine for rap generation (**DeepBeat**), trained on over 500,000 lines from 104 artists.
* **The RhymeDensity Metric:** Formulated the mathematical measurement of multisyllabic rhyme density:
  $$\text{RhymeDensity} = \frac{1}{|W|} \sum_{w \in W} \text{LCVS}(w)$$
  where $\text{LCVS}(w)$ represents the Longest Common Vowel Subsequence matching in the temporal proximity of word $w$.
* **Empirical Emcee Rankings:** Validated that technical emcees (Inspectah Deck: 1.187, Rakim: 1.180, Biggie: 1.059, Eminem: 1.047) achieve statistically superior rhyme density compared to standard pop lyrics ($<0.80$).

---

### E. Martin Connor — *Rap Analysis* (2014–Present)
* **Core Contribution:** The musicologist featured in the Vox Earworm documentary.
* **The 16-Dot Coordinate System:** Transcribed complex rap cadences onto sheet music and 16th-note subdivision graphs. Demonstrated that Rakim's lyrical revolution came from applying jazz phrasing (John Coltrane) and metric enjambment (landing accented rhyme syllables on Beat 1 of the following measure) to the rigid 4/4 rap pocket.

---

### F. Marjan Ghazvininejad et al. — *Hafez: an Interactive Poetry Generation System* (EMNLP 2016)
* **Core Contribution:** Established the foundational neurosymbolic architecture:
  - A neural language model generates semantic narrative and topical coherence.
  - An external, deterministic phonetic/metric transducer (Finite-State Acceptor over CMUdict) enforces rhythm, scansion, and rhyming matrices.
* **Application to LLMs:** Solves the "tokenizer phonetic blindness" problem by decoupling acoustic/metric computation from autoregressive token prediction.

---

## 2. Architectural Mapping in the `rap-lyrics` Skill

| Academic Theoretical Principle | Source Literature | Implementation in `rap-lyrics` |
|---|---|---|
| **Dual-Meter Tension & Resolution** | Bradley (2009) | `references/meter_and_flow.md` (16-Grid Subdivision Mapping) |
| **Phonetic Slant & Assonance Rules** | Hirjee & Brown (2009) | `references/techniques.md` (The "Orange" Principle & Vowel Bending) |
| **16-Bar Quad Architecture** | Edwards (2009), Connor (2014) | `references/styles.md` (Blueprints for Rakim, Biggie, Mos Def) |
| **Multisyllabic Compound Matrices** | Malmi et al. (2016) | `scripts/rap_tools_server.py` (`calculate_rhyme_matrix`) |
| **Quantitative Flow & Density Audit** | Malmi et al. (2016) | `scripts/analyze_flow.py` (Syllable variance & rhyme density) |
| **Neurosymbolic Tool Offloading** | Ghazvininejad et al. (2016) | `scripts/rap_tools_server.py` (`check_scansion_and_flow`) |
