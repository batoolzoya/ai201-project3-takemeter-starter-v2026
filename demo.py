"""
demo.py - live demo of TakeMeter: type a post, get a label + confidence.

Usage (repo folder, venv active):
    python demo.py              # type posts, one per line; empty line to quit
    python demo.py --examples   # run the 8 stress-test posts from notes.md

First run trains the model (the improved setup: 10 epochs, seed 42, same code
as the notebook) and saves it to models/takemeter/ (~270 MB, git-ignored).
That takes about 4 minutes on a laptop CPU. Every run after that loads the
saved model in a few seconds.

It does NOT change results.json, test_split.csv or the notebook.
"""

import json
import re
import sys
import time
from pathlib import Path

LABELS = ["question", "advice", "trip_report", "rant"]
EPOCHS = 10          # the improved setting from unit 6 (was 3)
MODEL_DIR = Path("models/takemeter")

# The 8 boundary posts from my Milestone 2 stress test, with the label I gave
# each one. None of them are in labels.csv, so the model has never seen them.
EXAMPLES = [
    ("Just got back from Lisbon. Honestly the trams were a nightmare, packed every single time and two of them broke down while we were on them. Food was great though and the views from Alfama made up for it.", "trip_report"),
    ("Spent 3 weeks in Vietnam last spring. If you go, skip Ha Long Bay day tours and do the overnight Lan Ha cruise instead, it's quieter and about the same price.", "advice"),
    ("Why does every airline now charge for seat selection?? I paid $400 for a ticket and they want another $45 so I can sit next to my own kid. Is there any airline left that doesn't do this?", "rant"),
    ("I'm in Rome right now and it's my first time in Europe. Pickpocketed on the metro this morning. Anyone know if the police station near Termini handles tourist reports in English?", "question"),
    ("Have you tried booking directly with the hotel instead? I did that in Porto last year and they upgraded me for free.", "advice"),
    ("Hostels in Amsterdam are getting ridiculous. EUR 70 for a bunk in a 12-bed dorm. I remember when it was EUR 25. Travel used to be for everyone.", "rant"),
    ("Day 4 in Japan. Kyoto was beautiful but I underestimated how much walking there is. Is it normal for feet to hurt this much? Thinking of skipping Nara tomorrow.", "trip_report"),
    ("Took the night train from Vienna to Venice. Would I do it again? Absolutely, but book a private compartment. The 6-berth couchette was miserable.", "trip_report"),
]

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def train_and_save():
    """Run the notebook's own cells up to (not including) section 5, then save."""
    nb = json.loads(Path("takemeter.ipynb").read_text(encoding="utf-8"))
    ns = {"__name__": "__main__"}
    print(f"No saved model yet - training once ({EPOCHS} epochs, seed 42). "
          f"About 4 minutes on CPU...\n")
    for cell in nb["cells"]:
        src = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
        if cell["cell_type"] == "markdown" and src.lstrip().startswith("## 5."):
            break
        if cell["cell_type"] != "code" or not src.strip():
            continue
        src = re.sub(r"^LABELS\s*=.*$", f"LABELS = {LABELS!r}", src, flags=re.M)
        src = re.sub(r"^EPOCHS\s*=.*$", f"EPOCHS = {EPOCHS}", src, flags=re.M)
        exec(compile(src, "<notebook>", "exec"), ns)
        if ns.get("problems"):
            sys.exit("Stopped: fix the [FIX ME] lines above, then run again.")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    ns["trainer"].save_model(str(MODEL_DIR))
    ns["tokenizer"].save_pretrained(str(MODEL_DIR))
    print(f"\nSaved the trained model to {MODEL_DIR}/\n")


def load():
    from transformers import pipeline
    return pipeline("text-classification", model=str(MODEL_DIR), tokenizer=str(MODEL_DIR),
                    top_k=None, truncation=True, max_length=128)


def classify(clf, text):
    start = time.perf_counter()
    scores = clf(text)
    ms = (time.perf_counter() - start) * 1000
    if scores and isinstance(scores[0], list):   # some versions nest one level
        scores = scores[0]
    scores = sorted(scores, key=lambda s: s["score"], reverse=True)
    return scores, ms


def show(scores, ms, expected=None):
    top = scores[0]
    line = f"  -> {top['label']}  ({top['score']:.0%} confident, {ms:.0f} ms)"
    if expected:
        line += "   " + ("matches my label" if top["label"] == expected
                         else f"MISS - I labelled it {expected}")
    print(line)
    print("     " + "  ".join(f"{s['label']} {s['score']:.0%}" for s in scores[1:]))


def main():
    if not (MODEL_DIR / "config.json").exists():
        train_and_save()
    print("Loading TakeMeter...")
    clf = load()

    if "--examples" in sys.argv:
        right = 0
        for i, (text, expected) in enumerate(EXAMPLES, 1):
            print(f"\n{i}. {text[:110]}{'...' if len(text) > 110 else ''}")
            scores, ms = classify(clf, text)
            show(scores, ms, expected)
            right += scores[0]["label"] == expected
        print(f"\n{right} of {len(EXAMPLES)} stress-test posts match my own labels.")
        return

    print("\nPaste or type an r/travel post and press Enter. Empty line to quit.")
    while True:
        try:
            text = input("\npost> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not text:
            break
        scores, ms = classify(clf, text)
        show(scores, ms)


if __name__ == "__main__":
    main()
