#!/usr/bin/env python3
"""
Restore lessons.json to the full 1239-lesson knowledge base.

Strategy:
1. Get the 1232-lesson version from git history (commit 82c65ac)
2. Add the 7 missing lessons from missing_lessons.json
3. Replace the patterns section with the updated one from patterns.json
4. Write the restored lessons.json

Expected result: 1239 lessons
"""
import json
import subprocess
import hashlib
import sys

BASE_COMMIT = "82c65ac"

print(f"Step 1: Getting 1232-lesson base from commit {BASE_COMMIT}...")
result = subprocess.run(
    ["git", "show", f"{BASE_COMMIT}:lessons.json"],
    capture_output=True, text=True, check=True
)
base_data = json.loads(result.stdout)
print(f"  Base version: {len(base_data['lessons'])} lessons")

print("Step 2: Loading 7 missing lessons...")
with open("missing_lessons.json") as f:
    missing = json.load(f)
print(f"  Missing lessons: {len(missing)}")

print("Step 3: Merging...")
base_data["lessons"].update(missing)
print(f"  Total lessons: {len(base_data['lessons'])}")

print("Step 4: Replacing patterns section...")
with open("patterns.json") as f:
    base_data["patterns"] = json.load(f)
print(f"  Patterns updated, last_updated: {base_data['patterns'].get('last_updated')}")

print("Step 5: Writing lessons.json...")
with open("lessons.json", "w") as f:
    json.dump(base_data, f, indent=2)
    f.write("\n")

print("Step 6: Verifying...")
with open("lessons.json") as f:
    verify = json.load(f)
count = len(verify["lessons"])
print(f"  Lesson count: {count}")

if count != 1239:
    print(f"ERROR: Expected 1239 lessons, got {count}")
    sys.exit(1)

with open("lessons.json", "rb") as f:
    content = f.read()
sha256 = hashlib.sha256(content).hexdigest()
print(f"  SHA256: {sha256}")
print("  SUCCESS: lessons.json restored with 1239 lessons!")
