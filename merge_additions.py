#!/usr/bin/env python3
"""
Merges daily additions files into lessons.json.
Run from repo root: python3 merge_additions.py
"""
import json
import glob
import os

LESSONS_FILE = "lessons.json"
ADDITIONS_GLOB = "daily_additions/*.json"

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {path}")

def main():
    if not os.path.exists(LESSONS_FILE):
        print(f"ERROR: {LESSONS_FILE} not found. Run from repo root.")
        return

    base = load_json(LESSONS_FILE)
    additions_files = sorted(glob.glob(ADDITIONS_GLOB))

    if not additions_files:
        print("No additions files found in daily_additions/")
        return

    total_added = 0
    for additions_path in additions_files:
        date_tag = os.path.basename(additions_path).replace(".json", "")
        print(f"Processing {additions_path} ...")
        additions = load_json(additions_path)
        new_lessons = additions.get("new_lessons", {})
        added = 0
        for uid, lesson in new_lessons.items():
            if uid not in base["lessons"]:
                base["lessons"][uid] = lesson
                added += 1
        print(f"  Added {added} new lessons from {date_tag}")
        total_added += added

        patterns_update = additions.get("patterns_update", {})
        if patterns_update:
            p = base.get("patterns", {})
            key_map = {
                "most_effective_hook_patterns": "new_hook_patterns_today",
                "most_effective_formats": "new_formats_today",
                "most_effective_tones": "new_tones_today",
                "most_effective_triggers": "new_triggers_today",
                "cross_niche_insights": "cross_niche_insights_today"
            }
            for key, new_key in key_map.items():
                new_items = patterns_update.get(new_key, [])
                existing = p.get(key, [])
                for item in new_items:
                    if item not in existing:
                        existing.append(item)
                p[key] = existing
            p["last_updated"] = patterns_update.get("last_updated", p.get("last_updated", ""))
            base["patterns"] = p

    print(f"\nTotal lessons added: {total_added}")
    print(f"Total lessons in base: {len(base['lessons'])}")
    save_json(LESSONS_FILE, base)

if __name__ == "__main__":
    main()
