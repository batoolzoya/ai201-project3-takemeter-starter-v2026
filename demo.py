"""
demo.py - TakeMeter, run and instrumented: classify r/travel posts and log every run.

Usage (repo folder, venv active):
    python demo.py                          # type posts one per line; empty line quits
    python demo.py --examples               # the 8 stress-test posts from notes.md
    python demo.py --batch trial_posts.txt  # a file of posts (one per line) -> summary
    python demo.py --log                    # show the last 10 log records
    python demo.py --epochs 20 --batch trial_posts.txt
                                            # capstone improvement: a model trained for 20 epochs

Every classification - answered, rejected or failed - appends one JSON record
to logs/predictions.jsonl (timestamp, input, output, duration and more). So
does loading the model. A run that errors still leaves a record.

First run trains the model (10 epochs, seed 42, the notebook's own code) and
saves it to models/takemeter/ (~270 MB, git-ignored). About 4 minutes on a
laptop CPU. Every run after that loads the saved model in a few seconds.

It does NOT change results.json, test_split.csv or the notebook.
"""

import json
import re
import statistics
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

LABELS = ["question", "advice", "trip_report", "rant"]
EPOCHS = 10          # the improved setting from unit 6 (was 3); --epochs N overrides
MAX_TOKENS = 128     # the model reads this many tokens; anything longer is cut off
MODEL_DIR = Path("models/takemeter")
LOG_PATH = Path("logs/predictions.jsonl")
SESSION = uuid.uuid4().hex[:8]   # ties together every record from one run of this script

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


# ── Logging ──────────────────────────────────────────────────────────────────

def log_record(**fields):
    """Append one JSON record to the log. Never raises: logging must not break a run."""
    record = {"ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
              "session": SESSION}
    record.update(fields)
    try:
        LOG_PATH.parent.mkdir(exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as exc:  # noqa: BLE001
        print(f"  [log] could not write log: {exc}", file=sys.stderr)
    return record


def read_log():
    if not LOG_PATH.exists():
        return []
    out = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def show_log(n=10):
    records = read_log()
    if not records:
        print(f"No records yet in {LOG_PATH}.")
        return
    print(f"Last {min(n, len(records))} of {len(records)} records in {LOG_PATH}:\n")
    for r in records[-n:]:
        if r.get("event") == "load":
            print(f"{r['ts']}  load      {r.get('duration_ms', 0):>7.0f} ms  model loaded")
            continue
        label = r.get("label") or "-"
        conf = f"{r['confidence']:.0%}" if r.get("confidence") is not None else "-"
        text = (r.get("input") or "").replace("\n", " ")[:45]
        print(f"{r['ts']}  {r.get('status', '?'):<8}  {r.get('duration_ms', 0):>7.0f} ms  "
              f"{label:<12} {conf:>4}  {text!r}")


# ── Model ────────────────────────────────────────────────────────────────────

def train_and_save():
    """Run the notebook's own cells up to (not including) section 5, then save."""
    nb = json.loads(Path("takemeter.ipynb").read_text(encoding="utf-8"))
    ns = {"__name__": "__main__"}
    print(f"No saved model yet - training once ({EPOCHS} epochs, seed 42). "
          f"About {max(4, round(EPOCHS * 0.4))} minutes on CPU...\n")
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
    start = time.perf_counter()
    clf = pipeline("text-classification", model=str(MODEL_DIR), tokenizer=str(MODEL_DIR),
                   top_k=None, truncation=True, max_length=MAX_TOKENS)
    ms = (time.perf_counter() - start) * 1000
    log_record(event="load", status="ok", duration_ms=round(ms, 1), model=str(MODEL_DIR))
    return clf


def classify(clf, text, mode, expected=None):
    """Classify one post and log it. Returns the log record."""
    start = time.perf_counter()
    base = {"event": "predict", "mode": mode, "model": str(MODEL_DIR), "input": text[:300],
            "input_chars": len(text), "expected": expected}

    if not text.strip():
        ms = (time.perf_counter() - start) * 1000
        return log_record(**base, status="rejected", error="empty or whitespace-only post",
                          label=None, confidence=None, duration_ms=round(ms, 2))
    try:
        n_tokens = len(clf.tokenizer(text)["input_ids"])
        scores = clf(text)
        if scores and isinstance(scores[0], list):   # some versions nest one level
            scores = scores[0]
        scores = sorted(scores, key=lambda s: s["score"], reverse=True)
        ms = (time.perf_counter() - start) * 1000
        return log_record(**base, status="ok", label=scores[0]["label"],
                          confidence=round(scores[0]["score"], 4),
                          scores={s["label"]: round(s["score"], 4) for s in scores},
                          input_tokens=n_tokens, truncated=n_tokens > MAX_TOKENS,
                          duration_ms=round(ms, 1), error=None)
    except Exception as exc:  # noqa: BLE001
        ms = (time.perf_counter() - start) * 1000
        return log_record(**base, status="error", error=f"{type(exc).__name__}: {exc}",
                          label=None, confidence=None, duration_ms=round(ms, 1))


def show(r):
    if r["status"] == "rejected":
        print(f"  -> rejected: {r['error']}  (logged)")
        return
    if r["status"] == "error":
        print(f"  -> ERROR: {r['error']}  (logged)")
        return
    line = f"  -> {r['label']}  ({r['confidence']:.0%} confident, {r['duration_ms']:.0f} ms)"
    if r.get("truncated"):
        line += f"  [long post: {r['input_tokens']} tokens, model read the first {MAX_TOKENS}]"
    if r.get("expected"):
        line += "   " + ("matches my label" if r["label"] == r["expected"]
                         else f"MISS - I labelled it {r['expected']}")
    print(line)
    others = [(k, v) for k, v in r["scores"].items() if k != r["label"]]
    print("     " + "  ".join(f"{k} {v:.0%}" for k, v in others))


# ── Batch mode ───────────────────────────────────────────────────────────────

def read_batch(path):
    """
    One post per line. Optional expected label before ' || '.
        advice || If you're flying into Lisbon, take the metro...
    <EMPTY> and <SPACES> stand for an empty post and a whitespace-only post.
    Lines starting with # are comments.
    """
    items = []
    for raw in Path(path).read_text(encoding="utf-8-sig").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        expected, text = None, raw
        if " || " in raw:
            expected, text = raw.split(" || ", 1)
            expected = expected.strip() or None
        text = text.strip()
        if text == "<EMPTY>":
            text = ""
        elif text == "<SPACES>":
            text = "   \t  "
        items.append((text, expected))
    return items


def run_batch(clf, path, load_ms):
    items = read_batch(path)
    before = len(read_log())
    wall = time.perf_counter()
    results = []
    for i, (text, expected) in enumerate(items, 1):
        preview = text[:90].replace("\n", " ") or "(empty)"
        print(f"\n{i}. {preview}{'...' if len(text) > 90 else ''}")
        r = classify(clf, text, "batch", expected)
        show(r)
        results.append(r)
    wall_s = time.perf_counter() - wall
    logged = len(read_log()) - before

    ok = [r for r in results if r["status"] == "ok"]
    rejected = [r for r in results if r["status"] == "rejected"]
    errors = [r for r in results if r["status"] == "error"]
    times = sorted(r["duration_ms"] for r in ok)
    graded = [r for r in ok if r.get("expected") in LABELS]
    right = sum(r["label"] == r["expected"] for r in graded)
    bad_expected = [r for r in results if r.get("expected") == "rejected"]
    bad_caught = sum(r["status"] == "rejected" for r in bad_expected)

    print("\n" + "=" * 60)
    print(f"Batch summary  (session {SESSION}, {path})")
    print("=" * 60)
    print(f"posts in file           {len(items)}")
    print(f"classified / rejected / errors   {len(ok)} / {len(rejected)} / {len(errors)}")
    print(f"log records written     {logged} of {len(items)}")
    if times:
        p95 = times[min(len(times) - 1, int(round(0.95 * (len(times) - 1))))]
        print(f"ms per post             mean {statistics.mean(times):.1f}  "
              f"median {statistics.median(times):.1f}  p95 {p95:.1f}  max {max(times):.1f}")
    print(f"model load              {load_ms:.0f} ms")
    print(f"whole batch (wall)      {wall_s:.2f} s")
    if graded:
        print(f"matches my labels       {right} of {len(graded)}")
    if bad_expected:
        print(f"bad inputs rejected     {bad_caught} of {len(bad_expected)}")
    long_posts = [r for r in ok if r.get("truncated")]
    if long_posts:
        print(f"long posts flagged      {len(long_posts)} (over {MAX_TOKENS} tokens)")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    global EPOCHS, MODEL_DIR
    if "--epochs" in sys.argv:
        EPOCHS = int(sys.argv[sys.argv.index("--epochs") + 1])
    if EPOCHS != 10:
        MODEL_DIR = Path(f"models/takemeter_e{EPOCHS}")   # keeps the 10-epoch model as it is

    if "--log" in sys.argv:
        n = 10
        if len(sys.argv) > sys.argv.index("--log") + 1:
            try:
                n = int(sys.argv[sys.argv.index("--log") + 1])
            except ValueError:
                pass
        show_log(n)
        return

    if not (MODEL_DIR / "config.json").exists():
        train_and_save()
    print("Loading TakeMeter...")
    try:
        clf = load()
    except Exception as exc:  # noqa: BLE001
        log_record(event="load", status="error", error=f"{type(exc).__name__}: {exc}")
        sys.exit(f"Could not load the model: {exc}  (logged)")
    load_ms = read_log()[-1].get("duration_ms", 0)

    if "--batch" in sys.argv:
        i = sys.argv.index("--batch")
        if i + 1 >= len(sys.argv):
            sys.exit("Usage: python demo.py --batch trial_posts.txt")
        run_batch(clf, sys.argv[i + 1], load_ms)
        return

    if "--examples" in sys.argv:
        right = 0
        for i, (text, expected) in enumerate(EXAMPLES, 1):
            print(f"\n{i}. {text[:110]}{'...' if len(text) > 110 else ''}")
            r = classify(clf, text, "examples", expected)
            show(r)
            right += r.get("label") == expected
        print(f"\n{right} of {len(EXAMPLES)} stress-test posts match my own labels.")
        return

    print("\nPaste or type an r/travel post and press Enter. Empty line to quit.")
    while True:
        try:
            text = input("\npost> ")
        except (EOFError, KeyboardInterrupt):
            break
        if not text.strip():
            break
        show(classify(clf, text, "interactive"))


if __name__ == "__main__":
    main()
