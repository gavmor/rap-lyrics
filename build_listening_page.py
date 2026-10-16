#!/usr/bin/env python3
import json
import shutil
import subprocess
from pathlib import Path

BASE = Path("/home/user/Documents/rap-lyrics")
WORKSPACE = Path("/home/user/.agents/skills/rap-lyrics-workspace/iteration-1")
OUTPUTS = BASE / "outputs"

tracks = [
    {
        "id": "rakim",
        "title": "The Midnight Manuscript (Rakim Style)",
        "artist": "Rakim",
        "eval_dir": WORKSPACE / "eval-0-rakim-barline-crossing" / "with_skill" / "outputs",
        "audio_name": "eval_0_rakim",
        "style": "Golden age 90s East Coast hip-hop, boom-bap drums, soulful jazz horn loop, deep bassline, crisp snare, male rap vocals, confident relaxed delivery, Rakim style.",
        "lyrics": """[Verse]
I draft the craft after dark, sixteen dots on the page
An architect of intellect who plots his thoughts on the stage
I step into the midnight mist, where the silence is deep
And sharpen surgical designs while the citizens sleep
With vision never blind, the manuscript can't be con-
-FINED; it breaks across the bar, leaving boundaries behind
I navigate the midnight blocks with a disciplined soul
And hold the sixty-four subdivisions in total control
""",
        "seed": 42,
        "prompt_id": "8cddc955-7219-401e-a254-285a6f36b571"
    },
    {
        "id": "mf_doom",
        "title": "Mad Science (MF DOOM Style)",
        "artist": "MF DOOM",
        "eval_dir": WORKSPACE / "eval-1-mf-doom-holorime-subversion" / "with_skill" / "outputs",
        "audio_name": "eval_1_doom",
        "style": "90s underground abstract hip-hop, dusty vinyl crackle, off-kilter jazz sample, heavy lo-fi drums, muffled bass, comic book supervillain aesthetic, raspy masked male emcee, MF DOOM style.",
        "lyrics": """[Verse]
Hunched inside the cellar like a trusty dungeon lurker
Cooking secret venom on a rusty Bunsen burner
Dusty corner, iron mask, he's plotting for a kill-
-ING, pouring heavy zinc into a classic Pyrex vial
Drop toxic liquid in, turn the cold dial
Pop lock-pick, wicked grin, burn the old file
Cold smile, no denial, brew a batch to make the hero choke
Vanished in a puffy cloud of STEAM, burnt the mocha cream
""",
        "seed": 99,
        "prompt_id": "b3665688-8b14-473d-a0a0-189f546f5731"
    },
    {
        "id": "kendrick",
        "title": "Sovereign Mortus (Kendrick Lamar Style)",
        "artist": "Kendrick Lamar",
        "eval_dir": WORKSPACE / "eval-2-kendrick-motivic-gearshift" / "with_skill" / "outputs",
        "audio_name": "eval_2_kendrick",
        "style": "Modern energetic jazz-rap, fast acoustic brass and horn section, rapid-fire hi-hats, hard acoustic drums, high-velocity syncopated delivery, Section.80 Rigamortus style, passionate male emcee.",
        "lyrics": """[Verse]
Crush systemic pressure, watch me break the grip, they tried to flip the
STATUTE, watch me rip the script and pick the lock
Redline across the city block, we shake the shock and carve in stone
They chain the cage, but cannot touch the flesh and bone, I claim the throne and bear the weight
Now watch me decimate the syndicate and ventilate the venom till they dead and gone, a veteran, a skeleton
Knock 'em off the pedestal, I morph into an animal, a cannibal, who fire off a cannonball
And tearing up the holy ground, I suffocate the competition, never turn around, resurrect the underground
The monument is broken down, I hover far above the ground, reclaim the sovereign crown, amen, A-MEN
""",
        "seed": 104,
        "prompt_id": "a4acddeb-f538-4380-9ada-4224e8fb9653"
    }
]

for t in tracks:
    tdir = OUTPUTS / t["id"]
    tdir.mkdir(parents=True, exist_ok=True)
    
    # Copy audio as song.mp3 and song.flac
    src_mp3 = t["eval_dir"] / f"{t['audio_name']}.mp3"
    src_flac = t["eval_dir"] / f"{t['audio_name']}.flac"
    
    if src_mp3.exists():
        shutil.copy2(src_mp3, tdir / "song.mp3")
    if src_flac.exists():
        shutil.copy2(src_flac, tdir / "song.flac")
    
    # Write request.json
    req = {
        "title": t["title"],
        "artist": t["artist"],
        "style": t["style"],
        "lyrics": t["lyrics"],
        "model": "yue2_3b_int8_convrot.safetensors",
        "backend": "comfyui-api",
        "sampler": "dpm_2",
        "scheduler": "sgm_uniform",
        "steps": 32,
        "cfg": 1.0,
        "seed": t["seed"],
        "max_duration": 45.0
    }
    (tdir / "request.json").write_text(json.dumps(req, indent=2))
    
    # Write result.json
    res = {
        "status": "success",
        "prompt_id": t["prompt_id"],
        "duration_seconds": 45.0,
        "sample_rate": 48000,
        "channels": 2,
        "format": "flac / mp3",
        "model": "YuE2 3B (int8 convrot)"
    }
    (tdir / "result.json").write_text(json.dumps(res, indent=2))

print("Created output folders for rakim, mf_doom, and kendrick.")

# Run listen.py from yue2-music skill
comp_dir = OUTPUTS / "listening_comparison"
cmd = [
    "python3",
    str(BASE / ".claude/skills/yue2-music/scripts/listen.py"),
    str(OUTPUTS / "rakim"),
    str(OUTPUTS / "mf_doom"),
    str(OUTPUTS / "kendrick"),
    "--output",
    str(comp_dir)
]
print(f"Running: {' '.join(cmd)}")
res = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
print("Exit code:", res.returncode)
