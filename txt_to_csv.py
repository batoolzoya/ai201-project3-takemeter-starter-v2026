"""
txt_to_csv.py - turn posts.txt into labels.csv

posts.txt looks like this - a [label] tag at the start, items separated by ---

    [question] Iceland in transit for 2 days. What should I do? ...
    ---
    [advice] Take the Flybus from KEF, it runs after every flight.
    ---
    [rant] Never flying this airline again. Six hours delayed and ...
    ---
    An item with no tag yet is fine - its label stays blank.

Usage (from the repo folder, venv active):
    python txt_to_csv.py

Writes labels.csv with columns text, label, note.
  - The first 20 tagged items get note "cold" (labelled by hand, no AI help).
  - Other tagged items get note "hand-labelled while collecting".
Safe to re-run: it rebuilds labels.csv from posts.txt every time,
so always edit posts.txt, never labels.csv.
"""

import csv
import re
import sys
from collections import Counter

LABELS = ["question", "advice", "trip_report", "rant"]   # must match the notebook
COLD = 20
IN, OUT = "posts.txt", "labels.csv"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    raw = open(IN, encoding="utf-8-sig").read()
except UnicodeDecodeError:
    raw = open(IN, encoding="cp1252").read()  # older Notepad "ANSI" save
except FileNotFoundError:
    sys.exit(f"Can't find {IN}. Run this from your repo folder.")

chunks = re.split(r"^\s*---\s*$", raw, flags=re.MULTILINE)
rows, seen, dupes, short, bad = [], set(), 0, 0, []
tagged = 0
for c in chunks:
    c = c.strip()
    if not c:
        continue
    label = ""
    m = re.match(r"^\[([^\]]*)\]\s*", c)
    if m:
        label = m.group(1).strip().lower().replace(" ", "_")
        c = c[m.end():]
    text = re.sub(r"\s+", " ", c).strip()   # one line per post
    if not text:
        continue
    if text.lower() in seen:
        dupes += 1
        continue
    seen.add(text.lower())
    if len(text) < 20:
        short += 1
    if label and label not in LABELS:
        bad.append((label, text[:60]))
    note = ""
    if label:
        tagged += 1
        note = "cold" if tagged <= COLD else "hand-labelled while collecting"
    rows.append({"text": text, "label": label, "note": note})

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["text", "label", "note"])
    w.writeheader()
    w.writerows(rows)

print(f"{len(rows)} items -> {OUT}  ({tagged} labelled, {len(rows) - tagged} not yet)")
counts = Counter(r["label"] for r in rows if r["label"])
for lab in LABELS:
    n = counts.get(lab, 0)
    pct = 100 * n / tagged if tagged else 0
    flag = "   <-- over the 70% cap" if pct > 70 else ""
    print(f"  {lab:<12} {n:>4}  ({pct:4.1f}%){flag}")
if bad:
    print("\n[FIX] Tags that aren't one of", LABELS)
    for lab, t in bad:
        print(f"  [{lab}]  {t}...")
if dupes:
    print(f"Skipped {dupes} duplicate(s) - you pasted the same item twice.")
if short:
    print(f"{short} item(s) are under 20 characters - check they pasted fully.")
