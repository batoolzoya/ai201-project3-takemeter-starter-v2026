# Capstone run log: after

Model: models/takemeter_e20

Sessions (one per trial): 4c280ac1, e854f974, b0e5d87c

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every post leaves a complete log record | 14 of 14 | 14/14 | 14/14 | 14/14 | MET |
| 2. Bad inputs rejected and logged | 2 of 2 | 2/2 | 2/2 | 2/2 | MET |
| 3. Real posts classified under 66 ms (incl. first) | 10 of 12 | 10/12 | 10/12 | 10/12 | MET |
| 4. Mean ms per classified post (cost) | < 110 ms | 61.4 ms | 61.8 ms | 63.5 ms | MET |
| 5. Real posts matching my label | >= 8 of 12 | 9/12 | 9/12 | 9/12 | MET |

Per-post timings (ms), in file order:

- Run 1: model load 148 ms; posts: 123, 51, 57, 55, 44, 48, 47, 46, 48, 56, 53, 108
- Run 2: model load 145 ms; posts: 121, 51, 56, 52, 44, 51, 50, 50, 47, 57, 56, 106
- Run 3: model load 147 ms; posts: 136, 54, 56, 54, 42, 49, 53, 46, 50, 59, 57, 106

Real output from Run 1 (records written by `demo.py::log_record`, via `demo.py::classify`, in `logs/predictions.jsonl`):

Criterion 1: all records from the run:
```
{"ts": "2026-11-22T00:46:26.212+00:00", "status": "ok", "label": "trip_report", "confidence": 0.7471, "expected": "trip_report", "duration_ms": 123.2, "input_tokens": 46, "truncated": false, "error": null, "input": "Just got back from Lisbon. Honestly the trams were a nightma"}
{"ts": "2026-11-22T00:46:26.265+00:00", "status": "ok", "label": "advice", "confidence": 0.8498, "expected": "advice", "duration_ms": 51.3, "input_tokens": 39, "truncated": false, "error": null, "input": "Spent 3 weeks in Vietnam last spring. If you go, skip Ha Lon"}
{"ts": "2026-11-22T00:46:26.324+00:00", "status": "ok", "label": "question", "confidence": 0.6685, "expected": "rant", "duration_ms": 56.7, "input_tokens": 48, "truncated": false, "error": null, "input": "Why does every airline now charge for seat selection?? I pai"}
{"ts": "2026-11-22T00:46:26.382+00:00", "status": "ok", "label": "question", "confidence": 0.6952, "expected": "question", "duration_ms": 55.2, "input_tokens": 44, "truncated": false, "error": null, "input": "I'm in Rome right now and it's my first time in Europe. Pick"}
{"ts": "2026-11-22T00:46:26.427+00:00", "status": "ok", "label": "question", "confidence": 0.8145, "expected": "advice", "duration_ms": 43.6, "input_tokens": 26, "truncated": false, "error": null, "input": "Have you tried booking directly with the hotel instead? I di"}
{"ts": "2026-11-22T00:46:26.477+00:00", "status": "ok", "label": "rant", "confidence": 0.5195, "expected": "rant", "duration_ms": 48.5, "input_tokens": 39, "truncated": false, "error": null, "input": "Hostels in Amsterdam are getting ridiculous. EUR 70 for a bu"}
{"ts": "2026-11-22T00:46:26.527+00:00", "status": "ok", "label": "trip_report", "confidence": 0.4899, "expected": "trip_report", "duration_ms": 47.4, "input_tokens": 37, "truncated": false, "error": null, "input": "Day 4 in Japan. Kyoto was beautiful but I underestimated how"}
{"ts": "2026-11-22T00:46:26.574+00:00", "status": "ok", "label": "advice", "confidence": 0.3342, "expected": "trip_report", "duration_ms": 45.5, "input_tokens": 34, "truncated": false, "error": null, "input": "Took the night train from Vienna to Venice. Would I do it ag"}
{"ts": "2026-11-22T00:46:26.625+00:00", "status": "ok", "label": "advice", "confidence": 0.9008, "expected": "advice", "duration_ms": 48.4, "input_tokens": 38, "truncated": false, "error": null, "input": "If you're flying into Lisbon, skip the taxi line and take th"}
{"ts": "2026-11-22T00:46:26.681+00:00", "status": "ok", "label": "rant", "confidence": 0.5988, "expected": "rant", "duration_ms": 55.7, "input_tokens": 51, "truncated": false, "error": null, "input": "Third time this year my checked bag didn't make the connecti"}
{"ts": "2026-11-22T00:46:26.736+00:00", "status": "ok", "label": "trip_report", "confidence": 0.6732, "expected": "trip_report", "duration_ms": 53.2, "input_tokens": 50, "truncated": false, "error": null, "input": "Just got back from 5 days in Hanoi. Spent most mornings walk"}
{"ts": "2026-11-22T00:46:26.847+00:00", "status": "ok", "label": "trip_report", "confidence": 0.6052, "expected": "trip_report", "duration_ms": 108.2, "input_tokens": 290, "truncated": true, "error": null, "input": "Two weeks in Peru, finally home and still processing it. We "}
{"ts": "2026-11-22T00:46:26.847+00:00", "status": "rejected", "label": null, "confidence": null, "expected": "rejected", "duration_ms": 0.01, "input_tokens": null, "truncated": null, "error": "empty or whitespace-only post", "input": ""}
{"ts": "2026-11-22T00:46:26.849+00:00", "status": "rejected", "label": null, "confidence": null, "expected": "rejected", "duration_ms": 0.01, "input_tokens": null, "truncated": null, "error": "empty or whitespace-only post", "input": "   \t  "}
```

Criterion 2: the two bad inputs:
```
{"ts": "2026-11-22T00:46:26.847+00:00", "status": "rejected", "label": null, "confidence": null, "expected": "rejected", "duration_ms": 0.01, "input_tokens": null, "truncated": null, "error": "empty or whitespace-only post", "input": ""}
{"ts": "2026-11-22T00:46:26.849+00:00", "status": "rejected", "label": null, "confidence": null, "expected": "rejected", "duration_ms": 0.01, "input_tokens": null, "truncated": null, "error": "empty or whitespace-only post", "input": "   \t  "}
```

Criteria 3 and 4: the slowest and fastest classified posts:
```
{"ts": "2026-11-22T00:46:26.847+00:00", "status": "ok", "label": "trip_report", "confidence": 0.6052, "expected": "trip_report", "duration_ms": 108.2, "input_tokens": 290, "truncated": true, "error": null, "input": "Two weeks in Peru, finally home and still processing it. We "}
{"ts": "2026-11-22T00:46:26.212+00:00", "status": "ok", "label": "trip_report", "confidence": 0.7471, "expected": "trip_report", "duration_ms": 123.2, "input_tokens": 46, "truncated": false, "error": null, "input": "Just got back from Lisbon. Honestly the trams were a nightma"}
{"ts": "2026-11-22T00:46:26.427+00:00", "status": "ok", "label": "question", "confidence": 0.8145, "expected": "advice", "duration_ms": 43.6, "input_tokens": 26, "truncated": false, "error": null, "input": "Have you tried booking directly with the hotel instead? I di"}
```

Criterion 5: the posts that did NOT match my label:
```
{"ts": "2026-11-22T00:46:26.324+00:00", "status": "ok", "label": "question", "confidence": 0.6685, "expected": "rant", "duration_ms": 56.7, "input_tokens": 48, "truncated": false, "error": null, "input": "Why does every airline now charge for seat selection?? I pai"}
{"ts": "2026-11-22T00:46:26.427+00:00", "status": "ok", "label": "question", "confidence": 0.8145, "expected": "advice", "duration_ms": 43.6, "input_tokens": 26, "truncated": false, "error": null, "input": "Have you tried booking directly with the hotel instead? I di"}
{"ts": "2026-11-22T00:46:26.574+00:00", "status": "ok", "label": "advice", "confidence": 0.3342, "expected": "trip_report", "duration_ms": 45.5, "input_tokens": 34, "truncated": false, "error": null, "input": "Took the night train from Vienna to Venice. Would I do it ag"}
```
