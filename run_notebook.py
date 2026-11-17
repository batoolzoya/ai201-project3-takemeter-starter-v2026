"""
run_notebook.py - run takemeter.ipynb's own code from the terminal.

Why: the notebook needs Jupyter/VS Code to open. This script runs the SAME
code cells, in order, so no notebook editor is needed. Nothing in the
training code is changed - only the two FILL THIS IN lines are set.

Usage (repo folder, venv active):
    python run_notebook.py            # unit 5: sections 1-5 (stops at "Unit 6 starts here")
    python run_notebook.py --unit6    # unit 6: sections 1-7 (includes three seeds + matrix)
    python run_notebook.py --unit6 --after --epochs 10
                                      # unit 6 Milestone 5: RUN_LABEL="after", one setting changed

It also saves takemeter.ipynb with LABELS and NAME filled in, so the notebook
in your repo matches what was run.
"""

import json
import re
import sys
from pathlib import Path

LABELS = ["question", "advice", "trip_report", "rant"]   # must match labels.csv
NAME = "Zoya"
EMAIL = "github: batoolzoya"   # notebook only prints this; kept off your real email

# Windows consoles can't print the notebook's emoji without this.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

NB = Path("takemeter.ipynb")
if not NB.exists():
    sys.exit("takemeter.ipynb not found. Run this from your repo folder.")

nb = json.loads(NB.read_text(encoding="utf-8"))
unit6 = "--unit6" in sys.argv
after = "--after" in sys.argv
epochs = None
if "--epochs" in sys.argv:
    epochs = int(sys.argv[sys.argv.index("--epochs") + 1])


def src(cell):
    s = cell["source"]
    return "".join(s) if isinstance(s, list) else s


def fill_in(code):
    code = re.sub(r'^LABELS\s*=.*$', f"LABELS = {LABELS!r}", code, flags=re.M)
    if after:
        code = re.sub(r'^RUN_LABEL\s*=.*$', 'RUN_LABEL = "after"', code, flags=re.M)
    if epochs is not None:
        code = re.sub(r'^EPOCHS\s*=.*$', f"EPOCHS = {epochs}", code, flags=re.M)
    code = re.sub(r'^NAME\s*=.*$', f'NAME  = "{NAME}"', code, flags=re.M)
    code = re.sub(r'^EMAIL\s*=.*$', f'EMAIL = "{EMAIL}"', code, flags=re.M)
    return code


# 1. Save the filled-in notebook so the repo matches the run.
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        new = fill_in(src(cell))
        if new != src(cell):
            cell["source"] = new.splitlines(keepends=True)
NB.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

# Unit 6 re-runs sections 1-5 to define the functions it needs. Keep unit 5's
# committed results.json / test_split.csv exactly as they were.
saved = {}
if unit6:
    for f in ("results.json", "test_split.csv"):
        if Path(f).exists():
            saved[f] = Path(f).read_bytes()

# 2. Run the code cells in order, sharing one namespace like a notebook kernel.
namespace = {"__name__": "__main__"}
ran = 0
for cell in nb["cells"]:
    if cell["cell_type"] == "markdown" and "Unit 6 starts here" in src(cell) and not unit6:
        break
    if cell["cell_type"] != "code":
        continue
    code = src(cell)
    if not code.strip():
        continue
    ran += 1
    print(f"\n{'-' * 20} cell {ran} {'-' * 20}")
    exec(compile(code, f"<notebook cell {ran}>", "exec"), namespace)

    # Stop early if section 2's data check found problems, like the notebook asks.
    if namespace.get("problems"):
        sys.exit("\nStopped: fix the [FIX ME] lines above, then run again.")

for f, data in saved.items():
    Path(f).write_bytes(data)
if saved:
    print("(Kept your unit 5 results.json and test_split.csv unchanged.)")

print(f"\nDone - ran {ran} code cells.")
