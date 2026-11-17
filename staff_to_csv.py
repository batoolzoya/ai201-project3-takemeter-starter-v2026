"""
staff_to_csv.py - turn staff_todo.txt into my_staff_labels.csv

In staff_todo.txt, type a label inside the [ ] at the start of each line:
    [hot_take] sp_001 | Pulled the splits from...

The text in my_staff_labels.csv is copied EXACTLY from data/staff_posts.csv
(matched by id), so agreement.py can match every post.

Usage (repo folder, venv active):
    python staff_to_csv.py
"""
import csv
import re
import sys

ALLOWED = {"analysis", "hot_take", "reaction"}

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

posts = {r["id"]: r["text"] for r in csv.DictReader(open("data/staff_posts.csv", encoding="utf-8"))}
try:
    raw = open("staff_todo.txt", encoding="utf-8-sig").read()
except UnicodeDecodeError:
    raw = open("staff_todo.txt", encoding="cp1252").read()

mine, problems = {}, []
for m in re.finditer(r"^\[([^\]]*)\]\s*(sp_\d+)", raw, flags=re.M):
    label = m.group(1).strip().lower().replace(" ", "_").replace("-", "_")
    pid = m.group(2)
    if not label:
        problems.append(f"{pid}: no label yet")
    elif label not in ALLOWED:
        problems.append(f"{pid}: '{label}' is not one of {sorted(ALLOWED)}")
    else:
        mine[pid] = label

missing = [pid for pid in posts if pid not in mine and not any(p.startswith(pid) for p in problems)]
problems += [f"{pid}: line not found in staff_todo.txt" for pid in missing]

if problems:
    print("[FIX] Not written yet:")
    for p in problems:
        print("  " + p)
    sys.exit(1)

with open("my_staff_labels.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "text", "label"])
    for pid, text in posts.items():
        w.writerow([pid, text, mine[pid]])

counts = {l: sum(1 for v in mine.values() if v == l) for l in sorted(ALLOWED)}
print(f"Wrote my_staff_labels.csv: {len(mine)} posts  {counts}")
