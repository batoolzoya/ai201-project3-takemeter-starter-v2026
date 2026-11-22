"""
trial_report.py - turn the last three batch runs in logs/predictions.jsonl into
the capstone run log (five criteria x three trials).

Usage:
    python trial_report.py before   # last 3 batch runs of the 10-epoch model (models/takemeter)
    python trial_report.py after    # last 3 batch runs of the 20-epoch model (models/takemeter_e20)

Writes results/capstone_<label>.md and prints it. Every number comes from the
log records themselves (demo.py::log_record), grouped by the `session` field,
so each trial is one separate run of the script.
"""
import json
import statistics
import sys
from pathlib import Path

LOG = Path("logs/predictions.jsonl")
N_POSTS, N_BAD, N_REAL = 14, 2, 12
LABELS = {"question", "advice", "trip_report", "rant"}

# Targets from criteria.md (capstone section), committed before any trial results.
T1, T2, T3_COUNT, T3_MS, T4_MS, T5 = 14, 2, 10, 66, 110, 8

for _s in (sys.stdout,):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_records():
    out = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def model_of(r):
    # Records from before the --epochs option have no "model" field: that was the 10-epoch model.
    return r.get("model") or "models/takemeter"


def trials(records, model, n=3):
    sessions = []
    for r in records:
        if (r.get("event") == "predict" and r.get("mode") == "batch"
                and model_of(r).replace("\\", "/") == model and r["session"] not in sessions):
            sessions.append(r["session"])
    picked = sessions[-n:]
    return [(s, [r for r in records if r.get("session") == s]) for s in picked]


def measure(recs):
    preds = [r for r in recs if r.get("event") == "predict"]
    complete = [r for r in preds
                if r.get("status") in ("ok", "rejected", "error")
                and isinstance(r.get("duration_ms"), (int, float))
                and (r.get("label") or r.get("error"))]
    bad = [r for r in preds if r.get("expected") == "rejected"]
    bad_ok = [r for r in bad if r.get("status") == "rejected" and r.get("error")]
    real = [r for r in preds if r.get("expected") in LABELS]
    real_ok = [r for r in real if r.get("status") == "ok"]
    fast = [r for r in real_ok if r["duration_ms"] < T3_MS]
    mean_ms = statistics.mean(r["duration_ms"] for r in real_ok) if real_ok else float("nan")
    match = [r for r in real_ok if r["label"] == r["expected"]]
    load = [r for r in recs if r.get("event") == "load"]
    return {
        "c1": len(complete), "c2": len(bad_ok), "c3": len(fast), "c4": mean_ms, "c5": len(match),
        "preds": preds, "bad": bad, "real_ok": real_ok, "load_ms": load[0]["duration_ms"] if load else None,
    }


def verdict(values, ok):
    return "MET" if all(ok(v) for v in values) else "MISSED"


def short(r):
    keep = {k: r.get(k) for k in ("ts", "status", "label", "confidence", "expected",
                                  "duration_ms", "input_tokens", "truncated", "error")}
    keep["input"] = (r.get("input") or "")[:60]
    return json.dumps(keep, ensure_ascii=False)


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "before"
    # "before" = the 10-epoch model; "after" = the 20-epoch model from the improvement.
    model = "models/takemeter_e20" if label == "after" else "models/takemeter"
    if not LOG.exists():
        sys.exit("No logs/predictions.jsonl yet. Run demo.py --batch trial_posts.txt first.")
    runs = trials(load_records(), model)
    if len(runs) < 3:
        cmd = "python demo.py --epochs 20 --batch trial_posts.txt" if label == "after" \
            else "python demo.py --batch trial_posts.txt"
        sys.exit(f"Only {len(runs)} batch run(s) with {model} in the log. Run `{cmd}` "
                 f"until there are 3.")
    m = [measure(recs) for _, recs in runs]

    rows = [
        ("1. Every post leaves a complete log record", f"{T1} of {N_POSTS}",
         [f"{x['c1']}/{N_POSTS}" for x in m], verdict([x["c1"] for x in m], lambda v: v >= T1)),
        ("2. Bad inputs rejected and logged", f"{T2} of {N_BAD}",
         [f"{x['c2']}/{N_BAD}" for x in m], verdict([x["c2"] for x in m], lambda v: v >= T2)),
        (f"3. Real posts classified under {T3_MS} ms (incl. first)", f"{T3_COUNT} of {N_REAL}",
         [f"{x['c3']}/{N_REAL}" for x in m], verdict([x["c3"] for x in m], lambda v: v >= T3_COUNT)),
        ("4. Mean ms per classified post (cost)", f"< {T4_MS} ms",
         [f"{x['c4']:.1f} ms" for x in m], verdict([x["c4"] for x in m], lambda v: v < T4_MS)),
        ("5. Real posts matching my label", f">= {T5} of {N_REAL}",
         [f"{x['c5']}/{N_REAL}" for x in m], verdict([x["c5"] for x in m], lambda v: v >= T5)),
    ]

    out = [f"# Capstone run log: {label}", "",
           f"Model: {model}", "",
           "Sessions (one per trial): " + ", ".join(s for s, _ in runs), "",
           "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
           "|---|---|---|---|---|---|"]
    for name, target, vals, v in rows:
        out.append(f"| {name} | {target} | {' | '.join(vals)} | {v} |")

    out += ["", "Per-post timings (ms), in file order:", ""]
    for i, x in enumerate(m, 1):
        ts = ", ".join(f"{r['duration_ms']:.0f}" for r in x["real_ok"])
        out.append(f"- Run {i}: model load {x['load_ms']:.0f} ms; posts: {ts}")

    first = m[0]
    out += ["", "Real output from Run 1 (records written by `demo.py::log_record`, "
            "via `demo.py::classify`, in `logs/predictions.jsonl`):", ""]
    out.append("Criterion 1: all records from the run:")
    out.append("```")
    out += [short(r) for r in first["preds"]]
    out.append("```")
    out.append("")
    out.append("Criterion 2: the two bad inputs:")
    out.append("```")
    out += [short(r) for r in first["bad"]]
    out.append("```")
    out.append("")
    out.append("Criteria 3 and 4: the slowest and fastest classified posts:")
    srt = sorted(first["real_ok"], key=lambda r: r["duration_ms"])
    out.append("```")
    out += [short(r) for r in (srt[-2:] + srt[:1])]
    out.append("```")
    out.append("")
    out.append("Criterion 5: the posts that did NOT match my label:")
    out.append("```")
    out += [short(r) for r in first["real_ok"] if r["label"] != r["expected"]]
    out.append("```")

    text = "\n".join(out) + "\n"
    Path("results").mkdir(exist_ok=True)
    path = Path("results") / f"capstone_{label}.md"
    path.write_text(text, encoding="utf-8")
    print(text)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
