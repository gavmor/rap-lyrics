#!/usr/bin/env python3
"""
test_small_models.py - Test rap-lyrics skill on small Ollama models.
Evaluates qwen2.5:0.5b and llama3.2:1b both with and without the skill.
"""

import json
import time
import urllib.request
from pathlib import Path

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OUTPUT_DIR = Path("/home/user/Documents/rap-lyrics/small_models_eval")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load skill context
skill_md = Path("/home/user/.agents/skills/rap-lyrics/SKILL.md").read_text()
techniques_md = Path("/home/user/.agents/skills/rap-lyrics/references/techniques.md").read_text()
styles_md = Path("/home/user/.agents/skills/rap-lyrics/references/styles.md").read_text()

skill_context = f"""You are equipped with the 'rap-lyrics' skill. Follow these instructions and blueprints carefully:

---
{skill_md}
---

Reference Techniques:
{techniques_md}

Reference Styles:
{styles_md}
---
"""

test_tasks = [
    {
        "id": "rakim_barline",
        "name": "Rakim (Internal Rhymes, Multis, Barline Crossing)",
        "prompt": "Write an 8-bar rap verse in the style of Rakim about the discipline of the craft and navigating the city at midnight. Make sure to use his signature 16-dot grid approach, internal rhymes, multisyllabic rhymes, and explicitly cross the bar line onto Beat 1 of the next bar. Include a breakdown of the techniques."
    },
    {
        "id": "doom_holorime",
        "name": "MF DOOM (Holorime & Expectation Subversion)",
        "prompt": "Write an 8-bar rap verse in the style of MF DOOM with an eccentric supervillain comic-book persona cooking up a secret formula in a dimly lit lab. Feature at least one holorime (where a setup bar rhymes every syllable with the punchline bar), dense multisyllabic rhymes, and a deliberate subversion of a rhyming expectation. Provide a technical breakdown."
    }
]

models = [
    "qwen2.5:0.5b",
    "llama3.2:1b"
]

def query_ollama(model: str, prompt: str, system: str = "") -> dict:
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 1024
        }
    }
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=req_data, headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())
            dur = time.time() - t0
            return {
                "response": data.get("response", ""),
                "total_duration": dur,
                "eval_count": data.get("eval_count", 0),
                "eval_duration": data.get("eval_duration", 0) / 1e9
            }
    except Exception as e:
        return {"error": str(e), "total_duration": time.time() - t0}

def main():
    results = {}
    for model in models:
        clean_model = model.replace(":", "_").replace("/", "_")
        results[model] = {}
        print(f"\n=======================================================")
        print(f"Testing model: {model}")
        print(f"=======================================================")
        
        for task in test_tasks:
            t_id = task["id"]
            results[model][t_id] = {}
            print(f"\n--- Task: {task['name']} ---")
            
            # 1. Baseline (Without Skill)
            print(f"  Running Baseline (without skill)...")
            res_wout = query_ollama(model, task["prompt"], system="")
            out_path_wout = OUTPUT_DIR / f"{clean_model}_{t_id}_without_skill.md"
            out_path_wout.write_text(res_wout.get("response", ""))
            results[model][t_id]["without_skill"] = {
                "chars": len(res_wout.get("response", "")),
                "duration": res_wout.get("total_duration", 0),
                "tokens": res_wout.get("eval_count", 0)
            }
            print(f"    Done in {res_wout.get('total_duration', 0):.1f}s ({res_wout.get('eval_count', 0)} tokens)")
            
            # 2. With Skill
            print(f"  Running With Skill...")
            res_with = query_ollama(model, task["prompt"], system=skill_context)
            out_path_with = OUTPUT_DIR / f"{clean_model}_{t_id}_with_skill.md"
            out_path_with.write_text(res_with.get("response", ""))
            results[model][t_id]["with_skill"] = {
                "chars": len(res_with.get("response", "")),
                "duration": res_with.get("total_duration", 0),
                "tokens": res_with.get("eval_count", 0)
            }
            print(f"    Done in {res_with.get('total_duration', 0):.1f}s ({res_with.get('eval_count', 0)} tokens)")

    summary_file = OUTPUT_DIR / "summary.json"
    summary_file.write_text(json.dumps(results, indent=2))
    print(f"\nAll tests completed! Results saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
