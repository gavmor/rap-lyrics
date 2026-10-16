#!/usr/bin/env python3
"""
generate_qwen38_track.py - Generate YuE2 audio track from Qwen 3.8 Rakim verse.
"""

import json
import time
import urllib.request
import urllib.parse
import subprocess
from pathlib import Path

COMFY_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = Path("/home/user/Documents/rap-lyrics/audio/qwen38")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

style_prompt = "Classic 90s East Coast boom-bap, steady 90 BPM drum beat, punchy kick and snare on 2 and 4, smooth upright bassline, subtle jazz horn sample, clear authoritative male hip-hop vocals, relaxed flow locked to the beat, Rakim style."

lyrics = """[Verse]
Midnight on the streets, the streetlights hum a minor key
Concrete underfoot, I’m a ghost with the poetry
Sodium glow, cold breath, the city keeps its secrets
Every alley is a page, I write the nights in letters
No clock, no crowd, just the rhythm in my footsteps
Moonlight on the pavement, thoughts that never stop us
Walk through the silence, let the silence do the talking
Midnight understands the words before I’m speaking
"""

prompt_dict = {
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
            "style": style_prompt,
            "lyrics": lyrics,
            "abc": "",
            "seed": 88,
            "mode": "full",
            "max_duration": 45.0,
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
            "seed": 88,
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
            "filename_prefix": "audio/yue2/qwen38_rakim",
            "format": "flac"
        }
    }
}

def main():
    print("Queueing prompt to ComfyUI...")
    data = json.dumps({"prompt": prompt_dict, "client_id": "qwen38_render"}).encode("utf-8")
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        prompt_id = res["prompt_id"]
        print(f"Queued with prompt ID: {prompt_id}")

    # Poll for completion
    start = time.time()
    while time.time() - start < 300:
        time.sleep(3.0)
        try:
            req = urllib.request.Request(f"{COMFY_URL}/history/{prompt_id}")
            with urllib.request.urlopen(req) as resp:
                h_data = json.loads(resp.read().decode())
                if prompt_id in h_data:
                    print(f"Prompt {prompt_id} completed!")
                    outputs = h_data[prompt_id].get("outputs", {})
                    save_node = outputs.get("14", {})
                    audios = save_node.get("audio", [])
                    if audios:
                        audio_info = audios[0]
                        filename = audio_info["filename"]
                        subfolder = audio_info.get("subfolder", "")
                        params = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": "output"})
                        flac_path = OUTPUT_DIR / "qwen38_rakim_midnight.flac"
                        mp3_path = OUTPUT_DIR / "qwen38_rakim_midnight.mp3"
                        
                        print(f"Downloading audio -> {flac_path}")
                        urllib.request.urlretrieve(f"{COMFY_URL}/view?{params}", str(flac_path))
                        print(f"Saved FLAC: {flac_path} ({flac_path.stat().st_size} bytes)")
                        
                        cmd = ["ffmpeg", "-y", "-i", str(flac_path), "-b:a", "192k", str(mp3_path)]
                        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                        print(f"Converted to MP3: {mp3_path} ({mp3_path.stat().st_size} bytes)")
                        return
        except Exception as e:
            print(f"Polling error: {e}")

    print("Error: timed out waiting for audio")

if __name__ == "__main__":
    main()
