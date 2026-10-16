#!/usr/bin/env python3
"""
generate_small_models_audio.py - Generate audible tracks from local small models' lyrics using YuE2.
"""

import json
import time
import urllib.request
import urllib.parse
import subprocess
from pathlib import Path

COMFY_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = Path("/home/user/Documents/rap-lyrics/audio/small_models")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

tracks = [
    {
        "id": "llama1b_rakim_barline_sea",
        "title": "Llama-3.2-1B: 'Crossing the Barline (Where Street Meets the Sea)'",
        "model_author": "Llama 3.2 1B",
        "style": "Classic 90s East Coast boom-bap, steady 90 BPM drum beat, punchy kick and snare on 2 and 4, smooth upright bassline, subtle jazz horn sample, clear authoritative male hip-hop vocals, relaxed flow locked to the beat, Rakim style.",
        "lyrics": """[Verse]
I'm walking down midnight streets, where the city's alive
The neon lights reflect, on my black and grey ride
I'm the king of the night, with my thoughts on my mind
The darkness surrounds me, but I'm feeling so divine
I'm crossing the barline, where the street meets the sea
My rhymes are like waves, crashing on the concrete spree
I'm the master of the flow, like a phantom in the night
My verse is a journey, through the city's twisted delight
""",
        "seed": 42,
        "max_duration": 45.0
    },
    {
        "id": "llama1b_doom_emperor_holorime",
        "title": "Llama-3.2-1B: 'Emperor of Holorime'",
        "model_author": "Llama 3.2 1B",
        "style": "Underground boom-bap hip-hop, 88 BPM, heavy head-nod drums, steady crisp snare on beats 2 and 4, warm dusty jazz piano loop, deep sub bass, raspy masked male emcee, calm conversational flow, rhyming locked tightly on the beat, MF DOOM style.",
        "lyrics": """[Verse]
I'm the Emperor of Holorime, the sultan of despair
My throne is made of shattered dreams, my kingdom's a mess in the air
Expectation's my accomplice, it's my best friend and foe
We're colliding in a kaleidoscope of woe
I'm painting masterpieces with broken glass and tears
My art's a commentary on the futility of fears
I'm a conductor of chaos, orchestrating the fall
Expectation's the melody, I'm the maestro of despair's call
""",
        "seed": 99,
        "max_duration": 45.0
    },
    {
        "id": "qwen2b_rakim_king_streets",
        "title": "Qwen-3-VL-2B: 'Rakim, King of the Streets'",
        "model_author": "Qwen 3 VL 2B",
        "style": "Classic 90s East Coast boom-bap, steady 90 BPM drum beat, punchy kick and snare on 2 and 4, smooth upright bassline, subtle jazz horn sample, clear authoritative male hip-hop vocals, relaxed flow locked to the beat, Rakim style.",
        "lyrics": """[Verse]
Midnight streets of the city, where lights are bright
Rap culture is rising, but it's hard to keep up
Midnight streets, the best streets to be
Rakim, king of the streets
This is the rhythm, we go on
Rakim in the streets, he's a king
Midnight streets of the city, where lights are bright
Rap culture is rising, and it's hard to keep up
""",
        "seed": 104,
        "max_duration": 45.0
    }
]

def build_prompt(style: str, lyrics: str, seed: int, prefix: str, max_duration: float = 45.0) -> dict:
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "yue2_3b_int8_convrot.safetensors"
            }
        },
        "2": {
            "class_type": "YuE2GenerateMusic",
            "inputs": {
                "clip": ["1", 1],
                "style": style,
                "lyrics": lyrics,
                "abc": "",
                "seed": seed,
                "mode": "full",
                "max_duration": max_duration,
                "temperature": 1.0,
                "top_p": 0.95,
                "top_k": 100,
                "repetition_penalty": 1.2
            }
        },
        "10": {
            "class_type": "ConditioningZeroOut",
            "inputs": {
                "conditioning": ["2", 0]
            }
        },
        "11": {
            "class_type": "EmptyYuE2LatentAudio",
            "inputs": {
                "seconds": ["2", 1],
                "batch_size": 1
            }
        },
        "12": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["10", 0],
                "latent_image": ["11", 0],
                "seed": seed,
                "control_after_generate": "fixed",
                "steps": 32,
                "cfg": 1.0,
                "sampler_name": "dpm_2",
                "scheduler": "sgm_uniform",
                "denoise": 1.0
            }
        },
        "13": {
            "class_type": "VAEDecodeAudio",
            "inputs": {
                "samples": ["12", 0],
                "vae": ["1", 2]
            }
        },
        "14": {
            "class_type": "SaveAudioAdvanced",
            "inputs": {
                "audio": ["13", 0],
                "filename_prefix": f"audio/yue2/{prefix}",
                "format": "flac"
            }
        }
    }

def queue_prompt(prompt_dict: dict) -> str:
    data = json.dumps({"prompt": prompt_dict, "client_id": "yue2_small_models"}).encode("utf-8")
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        return res["prompt_id"]

def wait_for_completion(prompt_id: str, timeout: float = 300.0) -> dict:
    start = time.time()
    print(f"Waiting for prompt {prompt_id}...")
    while time.time() - start < timeout:
        time.sleep(3.0)
        try:
            req = urllib.request.Request(f"{COMFY_URL}/history/{prompt_id}")
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                if prompt_id in data:
                    print(f"Prompt {prompt_id} completed!")
                    return data[prompt_id]
        except Exception as e:
            print(f"Polling error: {e}")
    raise TimeoutError(f"Prompt {prompt_id} timed out after {timeout}s")

def download_audio(audio_info: dict, dest_path: Path):
    filename = audio_info["filename"]
    subfolder = audio_info.get("subfolder", "")
    params = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": "output"})
    url = f"{COMFY_URL}/view?{params}"
    print(f"Downloading {url} -> {dest_path}")
    urllib.request.urlretrieve(url, str(dest_path))

def main():
    generated_files = []
    for item in tracks:
        print(f"\n==========================================")
        print(f"Generating Audio: {item['title']}")
        print(f"==========================================")
        prompt_dict = build_prompt(
            style=item["style"],
            lyrics=item["lyrics"],
            seed=item["seed"],
            prefix=item["id"],
            max_duration=item["max_duration"]
        )
        prompt_id = queue_prompt(prompt_dict)
        print(f"Queued with prompt ID: {prompt_id}")
        
        history = wait_for_completion(prompt_id)
        outputs = history.get("outputs", {})
        save_node_out = outputs.get("14", {})
        audios = save_node_out.get("audio", [])
        if not audios:
            print(f"Error: no audio output found in {outputs}")
            continue
        
        audio_info = audios[0]
        flac_path = OUTPUT_DIR / f"{item['id']}.flac"
        mp3_path = OUTPUT_DIR / f"{item['id']}.mp3"
        
        download_audio(audio_info, flac_path)
        print(f"Saved FLAC: {flac_path} ({flac_path.stat().st_size} bytes)")
        
        # Convert to MP3
        cmd = ["ffmpeg", "-y", "-i", str(flac_path), "-b:a", "192k", str(mp3_path)]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"Converted to MP3: {mp3_path} ({mp3_path.stat().st_size} bytes)")
        
        generated_files.append({
            "id": item["id"],
            "title": item["title"],
            "model_author": item["model_author"],
            "flac": str(flac_path),
            "mp3": str(mp3_path),
            "lyrics": item["lyrics"]
        })

    # Save manifest
    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(generated_files, indent=2))
    print(f"\nManifest saved to {manifest_path}")

if __name__ == "__main__":
    main()
