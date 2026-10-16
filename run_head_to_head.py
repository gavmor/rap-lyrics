#!/usr/bin/env python3
"""
run_head_to_head.py - Head-to-head evaluation between Gemma 4 12B IT and Qwen 3.8 27B IQ3
using the rap-lyrics skill framework while preserving GPU headroom.
"""

import json
import time
import urllib.request
import subprocess
from pathlib import Path

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OUTPUT_DIR = Path("/home/user/Documents/rap-lyrics/head_to_head")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

skill_md = Path("/home/user/.agents/skills/rap-lyrics/SKILL.md").read_text()
techniques_md = Path("/home/user/.agents/skills/rap-lyrics/references/techniques.md").read_text()
styles_md = Path("/home/user/.agents/skills/rap-lyrics/references/styles.md").read_text()

system_prompt = f"""You are a master rap lyricist and flow architect equipped with the 'rap-lyrics' skill. Follow these core instructions and blueprints:

{skill_md}

References:
{techniques_md}
{styles_md}
"""

task_prompt = """Write an 8-bar rap verse in the style of Rakim about the discipline of the craft and navigating the city at midnight.
Requirements:
1. Adhere to the 16-dot grid: maintain a disciplined 10 to 13 syllables per bar.
2. Incorporate dense internal rhymes and multisyllabic compound rhymes.
3. Explicitly cross the bar line between Bar 5 and Bar 6 onto Beat 1 of Bar 6 (using full-vowel enjambment, never a weak reduced prefix).
4. Provide a brief technical breakdown identifying the rhyme families and barline crossing.
"""

models = [
    {
        "id": "hf.co/google/gemma-4-12B-it-qat-q4_0-gguf:Q4_0",
        "name": "Gemma-4-12B-IT",
        "options": {"num_ctx": 4096}
    },
    {
        "id": "Qwen3.8-27B-GSQ-RCO:iq3_s-mtp",
        "name": "Qwen-3.8-27B-MTP",
        "options": {"num_ctx": 4096, "num_gpu": 24}
    }
]

def query_model(model_cfg: dict) -> dict:
    model_id = model_cfg["id"]
    payload = {
        "model": model_id,
        "prompt": task_prompt,
        "system": system_prompt,
        "stream": False,
        "options": model_cfg["options"],
        "keep_alive": 0
    }
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=req_data, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode())
        dur = time.time() - t0
        return {
            "name": model_cfg["name"],
            "model_id": model_id,
            "response": data.get("response", ""),
            "total_duration": dur,
            "eval_count": data.get("eval_count", 0),
            "eval_duration": data.get("eval_duration", 0) / 1e9,
            "tok_per_sec": round(data.get("eval_count", 0) / (data.get("eval_duration", 1e-9) / 1e9), 2)
        }

def main():
    results = []
    for m in models:
        print(f"\n==========================================")
        print(f"Running model: {m['name']} ({m['id']})")
        print(f"==========================================")
        res = query_model(m)
        out_file = OUTPUT_DIR / f"{m['name']}_rakim_verse.md"
        out_file.write_text(res["response"])
        print(f"Tokens: {res['eval_count']} | Time: {res['total_duration']:.1f}s | Speed: {res['tok_per_sec']} tok/s")
        print(f"Output saved to {out_file}")
        
        # Analyze flow
        flow_proc = subprocess.run(
            ["python3", "/home/user/.agents/skills/rap-lyrics/scripts/analyze_flow.py", str(out_file), "--json"],
            capture_output=True, text=True
        )
        try:
            flow_metrics = json.loads(flow_proc.stdout)
        except Exception:
            flow_metrics = {"error": flow_proc.stdout}
        
        res["flow_metrics"] = flow_metrics
        results.append(res)
        
        # Force unload to ensure GPU headroom is restored immediately
        urllib.request.urlopen(urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps({"model": m["id"], "keep_alive": 0}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        ))

    summary_file = OUTPUT_DIR / "head_to_head_summary.json"
    summary_file.write_text(json.dumps(results, indent=2))
    print(f"\nHead-to-head completed! Results saved to {summary_file}")

if __name__ == "__main__":
    main()
