# Capstone run log: after

Sessions (one per trial): c4b8b636, 4c280ac1, e854f974

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every post leaves a complete log record | 14 of 14 | 14/14 | 14/14 | 14/14 | MET |
| 2. Bad inputs rejected and logged | 2 of 2 | 2/2 | 2/2 | 2/2 | MET |
| 3. Real posts classified under 66 ms (incl. first) | 10 of 12 | 10/12 | 10/12 | 10/12 | MET |
| 4. Mean ms per classified post (cost) | < 110 ms | 63.2 ms | 61.4 ms | 61.8 ms | MET |
| 5. Real posts matching my label | >= 8 of 12 | 7/12 | 9/12 | 9/12 | MISSED |

Per-post timings (ms), in file order:

- Run 1: model load 142 ms; posts: 147, 56, 58, 55, 41, 48, 48, 46, 50, 52, 52, 104
- Run 2: model load 148 ms; posts: 123, 51, 57, 55, 44, 48, 47, 46, 48, 56, 53, 108
- Run 3: model load 145 ms; posts: 121, 51, 56, 52, 44, 51, 50, 50, 47, 57, 56, 106

Real output from Run 1 (records written by `demo.py::log_record`, via `demo.py::classify`, in `logs/predictions.jsonl`):

Criterion 1: all records from the run:
```
{"ts": "2026-11-22T00:21:14.487+00:00", "status": "ok", "label": "trip_report", "confidence": 0.3984, "expected": "trip_report", "duration_ms": 146.9, "input_tokens": 46, "truncated": false, "error": null, "input": "Just got back from Lisbon. Honestly the trams were a nightma"}
{"ts": "2026-11-22T00:21:14.545+00:00", "status": "ok", "label": "advice", "confidence": 0.4345, "expected": "advice", "duration_ms": 56.4, "input_tokens": 39, "truncated": false, "error": null, "input": "Spent 3 weeks in Vietnam last spring. If you go, skip Ha Lon"}
{"ts": "2026-11-22T00:21:14.604+00:00", "status": "ok", "label": "question", "confidence": 0.3644, "expected": "rant", "duration_ms": 57.6, "input_tokens": 48, "truncated": false, "error": null, "input": "Why does every airline now charge for seat selection?? I pai"}
{"ts": "2026-11-22T00:21:14.661+00:00", "status": "ok", "label": "question", "confidence": 0.4008, "expected": "question", "duration_ms": 55.0, "input_tokens": 44, "truncated": false, "error": null, "input": "I'm in Rome right now and it's my first time in Europe. Pick"}
{"ts": "2026-11-22T00:21:14.703+00:00", "status": "ok", "label": "question", "confidence": 0.3658, "expected": "advice", "duration_ms": 41.0, "input_tokens": 26, "truncated": false, "error": null, "input": "Have you tried booking directly with the hotel instead? I di"}
{"ts": "2026-11-22T00:21:14.753+00:00", "status": "ok", "label": "question", "confidence": 0.2924, "expected": "rant", "duration_ms": 48.3, "input_tokens": 39, "truncated": false, "error": null, "input": "Hostels in Amsterdam are getting ridiculous. EUR 70 for a bu"}
{"ts": "2026-11-22T00:21:14.805+00:00", "status": "ok", "label": "trip_report", "confidence": 0.3384, "expected": "trip_report", "duration_ms": 48.4, "input_tokens": 37, "truncated": false, "error": null, "input": "Day 4 in Japan. Kyoto was beautiful but I underestimated how"}
{"ts": "2026-11-22T00:21:14.850+00:00", "status": "ok", "label": "question", "confidence": 0.2715, "expected": "trip_report", "duration_ms": 46.5, "input_tokens": 34, "truncated": false, "error": null, "input": "Took the night train from Vienna to Venice. Would I do it ag"}
{"ts": "2026-11-22T00:21:14.904+00:00", "status": "ok", "label": "advice", "confidence": 0.5231, "expected": "advice", "duration_ms": 50.2, "input_tokens": 38, "truncated": false, "error": null, "input": "If you're flying into Lisbon, skip the taxi line and take th"}
{"ts": "2026-11-22T00:21:14.958+00:00", "status": "ok", "label": "question", "confidence": 0.3363, "expected": "rant", "duration_ms": 51.6, "input_tokens": 51, "truncated": false, "error": null, "input": "Third time this year my checked bag didn't make the connecti"}
{"ts": "2026-11-22T00:21:15.012+00:00", "status": "ok", "label": "trip_report", "confidence": 0.4001, "expected": "trip_report", "duration_ms": 52.1, "input_tokens": 50, "truncated": false, "error": null, "input": "Just got back from 5 days in Hanoi. Spent most mornings walk"}
{"ts": "2026-11-22T00:21:15.115+00:00", "status": "ok", "label": "trip_report", "confidence": 0.4082, "expected": "trip_report", "duration_ms": 104.1, "input_tokens": 290, "truncated": true, "error": null, "input": "Two weeks in Peru, finally home and still processing it. We "}
{"ts": "2026-11-22T00:21:15.115+00:00", "status": "rejected", "label": null, "confidence": null, "expected": "rejected", "duration_ms": 0.0, "input_tokens": null, "truncated": null, "error": "empty or whitespace-only post", "input": ""}
{"ts": "2026-11-22T00:21:15.121+00:00", "status": "rejected", "label": null, "confidence": null, "expected": "rejected", "duration_ms": 0.0, "input_tokens": null, "truncated": null, "error": "empty or whitespace-only post", "input": "   \t  "}
```

Criterion 2: the two bad inputs:
```
{"ts": "2026-11-22T00:21:15.115+00:00", "status": "rejected", "label": null, "confidence": null, "expected": "rejected", "duration_ms": 0.0, "input_tokens": null, "truncated": null, "error": "empty or whitespace-only post", "input": ""}
{"ts": "2026-11-22T00:21:15.121+00:00", "status": "rejected", "label": null, "confidence": null, "expected": "rejected", "duration_ms": 0.0, "input_tokens": null, "truncated": null, "error": "empty or whitespace-only post", "input": "   \t  "}
```

Criteria 3 and 4: the slowest and fastest classified posts:
```
{"ts": "2026-11-22T00:21:15.115+00:00", "status": "ok", "label": "trip_report", "confidence": 0.4082, "expected": "trip_report", "duration_ms": 104.1, "input_tokens": 290, "truncated": true, "error": null, "input": "Two weeks in Peru, finally home and still processing it. We "}
{"ts": "2026-11-22T00:21:14.487+00:00", "status": "ok", "label": "trip_report", "confidence": 0.3984, "expected": "trip_report", "duration_ms": 146.9, "input_tokens": 46, "truncated": false, "error": null, "input": "Just got back from Lisbon. Honestly the trams were a nightma"}
{"ts": "2026-11-22T00:21:14.703+00:00", "status": "ok", "label": "question", "confidence": 0.3658, "expected": "advice", "duration_ms": 41.0, "input_tokens": 26, "truncated": false, "error": null, "input": "Have you tried booking directly with the hotel instead? I di"}
```

Criterion 5: the posts that did NOT match my label:
```
{"ts": "2026-11-22T00:21:14.604+00:00", "status": "ok", "label": "question", "confidence": 0.3644, "expected": "rant", "duration_ms": 57.6, "input_tokens": 48, "truncated": false, "error": null, "input": "Why does every airline now charge for seat selection?? I pai"}
{"ts": "2026-11-22T00:21:14.703+00:00", "status": "ok", "label": "question", "confidence": 0.3658, "expected": "advice", "duration_ms": 41.0, "input_tokens": 26, "truncated": false, "error": null, "input": "Have you tried booking directly with the hotel instead? I di"}
{"ts": "2026-11-22T00:21:14.753+00:00", "status": "ok", "label": "question", "confidence": 0.2924, "expected": "rant", "duration_ms": 48.3, "input_tokens": 39, "truncated": false, "error": null, "input": "Hostels in Amsterdam are getting ridiculous. EUR 70 for a bu"}
{"ts": "2026-11-22T00:21:14.850+00:00", "status": "ok", "label": "question", "confidence": 0.2715, "expected": "trip_report", "duration_ms": 46.5, "input_tokens": 34, "truncated": false, "error": null, "input": "Took the night train from Vienna to Venice. Would I do it ag"}
{"ts": "2026-11-22T00:21:14.958+00:00", "status": "ok", "label": "question", "confidence": 0.3363, "expected": "rant", "duration_ms": 51.6, "input_tokens": 51, "truncated": false, "error": null, "input": "Third time this year my checked bag didn't make the connecti"}
```
