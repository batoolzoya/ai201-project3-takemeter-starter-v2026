# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts posts and comments from **r/travel**, a large public subreddit where people plan trips, share trips and complain about travel. Each item gets exactly one of four labels based on the writer's **main purpose**: `question` (asking for help), `advice` (helping someone else), `trip_report` (describing their own trip) or `rant` (venting frustration). The model sees each item on its own text alone, without the thread it came from.

---

## Label Taxonomy

**General rule for every label:** label by the writer's main purpose, judged from the text alone, not by surface features. A question mark doesn't make a question, the word "rant" doesn't make a rant, and a sad tone doesn't make a rant.

### `question`

**Definition:** The writer's main purpose is to get information, help or opinions from others.

**Example 1:**
> Is booking two one-way flights instead of round trip asking for trouble? I'm looking at a US to Europe trip and somehow two separate one-way tickets are giving me more options than searching round trip...

**Example 2:**
> How to travel with pet - Connecting flights with different airlines. Does anyone know how I can ensure that my pet will be able to travel with me on my WHOLE trip?...

### `advice`

**Definition:** The writer's main purpose is to help with someone else's plans, decision or question: recommending, warning, correcting, or sharing an opinion or habit for them to weigh.

**Example 1:**
> BGY is not on Milan, it is in Bergamo which is a completly different town „far" away. if you want to save time BGY is no option...

**Example 2:**
> sorry your NYC trip got wrecked... Under the US DOT refund rule that's been in force since late 2024 if the airline cancels your flight and you don't accept the rebooking you're owed your money back in cash...

### `trip_report`

**Definition:** The writer's main purpose is to describe a trip or place they experienced themselves, even if tips slip in.

**Example 1:**
> A day in Verona. Yesterday I finally had the opportunity to visit Verona, which has been a dream of mine for years, safe to say it did not dissapoint!...

**Example 2:**
> Nice shots! I was also in South Korea for two weeks recently. Other than 3 days in Busan, I spent most of my time in Seoul. Hope to visit Jeju-do in the future.

### `rant`

**Definition:** The writer's main purpose is to vent frustration about a travel experience or situation, even if a question is included.

**Example 1:**
> Left Marseille at 3am Friday And now stuck In Miami at 3am. No flights tomorrow as they are all booked.

**Example 2:**
> Done with Frontier. Long story short: Arrived at the Atlanta airport 2 hours prior to flight... I'm now out $700... I'm done with Frontier forever.

### The hardest boundary

**Which two labels:** `trip_report` and `advice`

**The decision rule I used every time:** If the post's main purpose is to describe the writer's own trip, it is `trip_report`, even if it contains tips or a "next time I'd...". It is `advice` only if it is aimed at someone else's plans (answering a question, "you should", "I'd recommend").

**Tie-breakers for the other boundaries:**
- `rant` vs `question`: delete the question. If what's left is mainly complaining, it's a `rant`. If the complaining is background for a specific request, it's a `question`.
- `rant` vs `trip_report`: is the frustration the point of the post, or one part of a trip story?

**Stress test:** I asked an AI tool for 8 posts written to sit on these boundaries and labelled them myself using only the definitions above. All 8 fit one label. The closest call was a trip update that asks "is it normal for feet to hurt this much?", which I called `trip_report` because the question is a side note to the trip. The full list is in `notes.md`.

---

## The Dataset

**Where the posts came from:** r/travel (public), collected by copy-paste on 2026-11-15. I took posts in the order they appeared in /new, plus 1 to 3 top comments from each. Later I also searched r/travel for complaint posts, because `rant` started very thin (5 of my first 41). I first tried an automated collector, but Reddit returned HTTP 403, so I switched to copy-paste.

What I skipped: deleted/removed posts, mod posts, bots, and pure chit-chat that doesn't ask, advise, report or complain (for example short replies that only poke at the poster, like "... too much what?"). Known limitation: the model has never seen chit-chat, so it will force any chit-chat into one of the four labels.

**I collected 151 items, not 200**, because of time. That is above the 150 floor in the stop rule.

**How I labelled them:** By hand, while collecting. I typed a `[label]` tag in front of each item as I pasted it into `posts.txt`, and `txt_to_csv.py` turns that file into `labels.csv`. The first 20 labelled items are marked `cold` in the note column: labelled alone with no tools. **No AI pre-labelling was used.** Every label in the file is my own call. I labelled every item from its own text, as if I hadn't seen the thread, because that's all the model gets.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `question` | 42 | 27.8% |
| `advice` | 44 | 29.1% |
| `trip_report` | 34 | 22.5% |
| `rant` | 31 | 20.5% |
| **Total** | 151 | 100% |

**Three hard cases**

**1.**
> *The post:* "Switzerland - 10 days in a fairy tale..." A 10-day itinerary full of tips like "go early" and "Don't miss the short hike to the Riflesee lake".
>
> *Could have been:* `trip_report` or `advice`
>
> *I chose, because:* `trip_report`. The post is written to describe their own trip, and the tips are part of telling it. Under my hardest-boundary rule, tips slipping in doesn't make it advice.

**2.**
> *The post:* "Doctor ignoring me for rabies/typhoid vaccine. I've been calling my local doctors office for the past 2 months... Is this a thing? Why would my doctor blackball me like this?... it's just ridiculous that I have to."
>
> *Could have been:* `rant` or `question`
>
> *I chose, because:* `rant`. Deleting the questions leaves a post that is mainly complaining, and the writer has already decided what to do (find another doctor).

**3.**
> *The post:* "PSA and a Priceline Story: Always call and complain/question if something is not right!..." A long story about the writer's own booking problem and the free flights they got by complaining.
>
> *Could have been:* `advice`, `trip_report` or `rant`
>
> *I chose, because:* `advice`. Most of the text is the writer's own story, but it's told as a PSA, and the point is to tell other travellers what to do. Purpose wins over how much of the post is story.

More hard cases (the Korea trip with "If I could go back...", the "Kinda of ranting... how do people travel in their 20s?" question, the "Algerian Sahara" report full of prices and booking tips) are in `notes.md`.

---

## The Training Run

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, 128 tokens per post, seed 42. Trained on **CPU** (torch 2.15.0+cpu, Windows), and `results.json` records this too.

**Anything I changed from the defaults, and why:** No hyperparameters changed. I only set `LABELS` to my four labels. I ran the notebook's code from the terminal with `run_notebook.py` instead of in Jupyter/VS Code, because Jupyter isn't in `requirements.txt`. The script executes the notebook's own code cells in order, unchanged except for `LABELS` and my name, and saves the updated notebook.

**Split sizes:** train 105 / val 23 / test 23.

| Label | train | val | test |
|---|---|---|---|
| `question` | 30 | 6 | 6 |
| `advice` | 30 | 7 | 7 |
| `trip_report` | 24 | 5 | 5 |
| `rant` | 21 | 5 | 5 |

**Every label has fewer than 8 examples in the test split** (5 to 7 each), so per-label F1 will move a lot between seeds next unit. `results.json` and `test_split.csv` are committed. Reading the numbers is next unit's work.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I pasted the "2 Weeks in Korea" post and a reply, and asked whether they were `trip_report` or `advice`.
- *What came back:* The strongest case for each label, and three possible rules (by purpose / any tip wins / majority of the post), with what each would cost my label balance. It didn't pick one.
- *What I changed:* I chose the purpose rule, then noticed my other hard calls (rants with questions, questions that say "rant") all followed the same idea. So I made "label by main purpose, not surface features" the general rule for every label.

**Moment 2**

- *What I asked for:* Help drafting one-sentence definitions from my purpose rule and the calls I had already made, then 8 posts written to sit on my label boundaries.
- *What came back:* Draft definitions, two tie-breaker tests, and the 8 test posts.
- *What I changed:* I labelled the 8 posts myself using only the definitions. All 8 fit one label, so I kept the definitions. My closest call (#7) is written up in `notes.md`.

Other AI help: a Reddit collector script (blocked by Reddit with HTTP 403, so I switched to copy-paste), the `txt_to_csv.py` converter that reads my `[label]` tags, and `run_notebook.py`, which runs the notebook's cells from the terminal.

**Moment 3 (unit 6)**

- *What I asked for:* Help reading my first three-seed results, where my trained model lost to the untrained baseline on every label.
- *What came back:* It pointed out that my training loss (1.35) was almost exactly what a random guesser scores for 4 labels (about 1.39), and that the matrix showed the model calling 21 of 23 posts `question`. So the model had barely trained, rather than mixing up two of my labels.
- *What I changed:* I picked "epochs 3 to 10" as my one improvement because of that diagnosis, after checking my agreement report (97%) to rule out my labelling. I made the verdict calls and the staff-set adjudication myself. AI also wrote the helper scripts for this unit (`staff_to_csv.py`, and the `--unit6 --after --epochs` options in `run_notebook.py`).

**Pre-labelling disclosure:** None. All 151 labels were typed by me while collecting. The first 20 are marked `cold`.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

Both models on the same 23 held-out posts (`test_split.csv`, seed 42). The baseline is `facebook/bart-large-mnli` doing zero-shot classification with my four definitions from `label_definitions.txt` as the only input.

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.565 | 0.348 | -0.217 |
| Macro F1 | 0.561 | 0.222 | -0.339 |
| F1 — `advice` | 0.526 | 0.444 | -0.082 |
| F1 — `question` | 0.800 | 0.444 | -0.356 |
| F1 — `rant` | 0.250 | 0.000 | -0.250 |
| F1 — `trip_report` | 0.667 | 0.000 | -0.667 |

**What I predicted before I looked:**
I expected the trained model to do best on `question`, then `rant`, then `trip_report`, then `advice`.

**What the gap actually means:**
The untrained baseline beat my trained model on every label. My fine-tuning, as run with the default settings, added nothing. It made things worse. `question` really was the trained model's best label, as I predicted, but only because it called almost everything `question` (see the matrix below). My prediction was wrong about `rant`: the trained model never got a single rant right. The baseline is also slower (a few seconds per post on CPU, against well under a second for the trained model), but that speed is no use while it's this inaccurate.

---

## Run Log — Before

Trained on CPU (torch 2.15.0+cpu, Windows), 3 epochs, learning rate 2e-5, batch 16, 151 labelled posts (105 train / 23 val / 23 test per seed).

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.80 | 0.348 | 0.435 | 0.609 | MISSED |
| 2. Per-label F1 | question, advice, trip_report ≥ 0.70; rant ≥ 0.50 | q 0.444, a 0.444, t 0.000, r 0.000 | q 0.444, a 0.667, t 0.000, r 0.000 | q 0.615, a 0.737, t 0.667, r 0.000 | MISSED |
| 3. Beats baseline accuracy by ≥ 20 points | ≥ +0.20 | -0.217 (0.348 vs 0.565) | not run | not run | MISSED |
| 4. Agreement with staff labels | ≥ 70% | 97% (29/30), one number, not per seed | | | MET |
| 5. Label balance in labels.csv | none > 50%, none < 10% | max 29.1% (`advice`), min 20.5% (`rant`), same file for every seed | | | MET |

The notebook's spread table:

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.348 | 0.435 | 0.609 | 0.261 |
| Macro F1 | 0.222 | 0.278 | 0.505 | 0.283 |
| F1 — `question` | 0.444 | 0.444 | 0.615 | 0.171 |
| F1 — `advice` | 0.444 | 0.667 | 0.737 | 0.292 |
| F1 — `trip_report` | 0.000 | 0.000 | 0.667 | 0.667 |
| F1 — `rant` | 0.000 | 0.000 | 0.000 | 0.000 |

Accuracy moved 26 points across the three seeds, more than the 10-point line the notebook uses for a stable measure.

### Confusion matrix

Seed 42, 23 test posts:

| true \ predicted | question | advice | trip_report | rant |
|---|---|---|---|---|
| **question** | 6 | 0 | 0 | 0 |
| **advice** | 5 | 2 | 0 | 0 |
| **trip_report** | 5 | 0 | 0 | 0 |
| **rant** | 5 | 0 | 0 | 0 |

**My biggest off-diagonal number, and what it means:**
5 real `advice` posts were called `question`, and 0 went the other way. But `trip_report` and `rant` also lost all 5 of their posts to `question`. So this isn't one boundary the model mixed up: it called 21 of 23 posts `question` and only ever predicted one other label (`advice`, twice). It never learned to tell my labels apart at all.

---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.80 on all three seeds | MISSED | All three seeds were below 0.80 (best was 0.609). |
| 2 | Per-label F1 | ≥ 0.70 (rant ≥ 0.50) on all three seeds | MISSED | No label reached its target on all three seeds. `rant` was 0.000 every time. |
| 3 | Beats baseline by ≥ 20 points | on all three seeds | MISSED | The baseline was only scored on seed 42's test posts, and there the trained model was 21.7 points *below* it. The target has to hold on every seed, so one clear miss decides it. |
| 4 | Agreement with staff | ≥ 70% | MET | 29 of 30 = 97%. |
| 5 | Label balance | none > 50%, none < 10% | MET | Largest label 29.1%, smallest 20.5%. |

**Diagnoses**

**Criteria 1, 2 and 3: the model didn't train enough to learn anything.**
- *Cause:* 3 epochs over 105 training posts is only 21 small training steps, and the model barely moved.
- *Evidence 1, the loss:* training loss went from 1.37 to 1.33 on seed 42 (final average 1.347). A model that's purely guessing among 4 labels scores about 1.39 (ln 4), so it finished almost exactly where a random guesser starts.
- *Evidence 2, the matrix:* it called 21 of 23 posts `question`, including every `rant` and every `trip_report`. Rants and trip reports look nothing like questions, so this is a model that collapsed to one answer, not one that confused two similar labels.
- *Evidence 3, the agreement report:* it says this is a model problem, not a labelling problem. When I applied someone else's written, purpose-style rules to 30 posts, I matched them on 29 (97%), and my one miss was a rule I applied loosely once, not a pattern. That's indirect evidence (it's a different taxonomy), but it suggests I can apply a written rule consistently. Inconsistent labels would also show up as confusion between specific pairs, like `trip_report` and `advice`, not as everything going to one label.
- *What this rules out:* it isn't class imbalance. My labels are 20–29% each, so no label dominates the data.

**On top of that: the test splits are too small for a stable measure.**
- Each test split has only 5–7 posts per label, so one post moves a label's F1 a lot. Accuracy swung 26 points across seeds (0.348 to 0.609), and `trip_report` went from 0.000 to 0.667 depending only on which posts landed in the test set.
- This comes from collecting 151 posts instead of 200. It explains the spread, but not the collapse: even the best seed called most things `question`.

---

## Agreement Report

**Agreement rate:** 29 / 30 = 97%

I labelled the 30 posts under `data/staff_taxonomy.md`, not my own taxonomy, and committed my labels (`my_staff_labels.csv`) before I saw the staff file.

**Disagreements**

**1.**
> *The post:* "Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people." (sp_010)
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. The claim is built on the fact: three runners, same session, 5 miles, within 10 seconds. Take the numbers away and there's no argument left. That is Rule 1's test, "does the fact carry the argument?" I had read the small, private sample as "no real support", but the definition asks whether a fact carries the argument, not whether the sample is big. I labelled three similar posts (sp_002, sp_005, sp_007, each one runner's own measurements) as `analysis`, so I applied the rule one way three times and the other way once.
>
> *Which pile:* (a), the rule covered it and I applied it loosely.

**What the pattern in my disagreements tells me:**
With only one disagreement, there isn't much of a pattern. It's a single slip on Rule 1, not a boundary I keep getting wrong. For my own project, this is the main evidence that my 151 labels are probably consistent, so my model's misses are more likely about training than about my labelling.

---

## The Improvement

**What I changed:** Epochs from 3 to 10. Nothing else changed: same 151 labels, same learning rate (2e-5), batch size 16, same three seeds and therefore the same splits. Run with `python run_notebook.py --unit6 --after --epochs 10`, which sets `RUN_LABEL = "after"` and `EPOCHS = 10` in the notebook.

**Which diagnosis pointed at it:** The diagnosis for criteria 1–3. The training loss stayed at chance level (1.35 against 1.39 for random guessing) after only 21 training steps, and the model collapsed to calling almost everything `question`. That points at too little training, not at my labels (97% agreement) or at imbalance (every label is 20–29%). 10 epochs gives it about 70 steps.

### Run Log — After

Same three seeds and splits, 10 epochs instead of 3. Nothing else changed. CPU, torch 2.15.0+cpu.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.80 | 0.696 | 0.609 | 0.696 | MISSED |
| 2. Per-label F1 | question, advice, trip_report ≥ 0.70; rant ≥ 0.50 | q 0.615, a 0.750, t 0.909, r 0.333 | q 0.526, a 0.833, t 0.667, r 0.333 | q 0.667, a 0.714, t 0.800, r 0.571 | MISSED |
| 3. Beats baseline accuracy by ≥ 20 points | ≥ +0.20 | +0.131 (0.696 vs 0.565) | not run | not run | MISSED |
| 4. Agreement with staff labels | ≥ 70% | 97% (29/30), unchanged | | | MET |
| 5. Label balance in labels.csv | none > 50%, none < 10% | unchanged (29.1% / 20.5%) | | | MET |

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.696 | 0.609 | 0.696 | 0.087 |
| Macro F1 | 0.652 | 0.590 | 0.688 | 0.098 |
| F1 — `question` | 0.615 | 0.526 | 0.667 | 0.140 |
| F1 — `advice` | 0.750 | 0.833 | 0.714 | 0.119 |
| F1 — `trip_report` | 0.909 | 0.667 | 0.800 | 0.242 |
| F1 — `rant` | 0.333 | 0.333 | 0.571 | 0.238 |

Confusion matrix after, seed 42:

| true \ predicted | question | advice | trip_report | rant |
|---|---|---|---|---|
| **question** | 4 | 2 | 0 | 0 |
| **advice** | 1 | 6 | 0 | 0 |
| **trip_report** | 0 | 0 | 5 | 0 |
| **rant** | 2 | 1 | 1 | 1 |

Before and after, side by side (accuracy):

| Seed | Before (3 epochs) | After (10 epochs) | Change |
|---|---|---|---|
| 42 | 0.348 | 0.696 | +0.348 |
| 7 | 0.435 | 0.609 | +0.174 |
| 2024 | 0.609 | 0.696 | +0.087 |
| Spread | 0.261 | 0.087 | 17 points more stable |

**Did it help, and how do I know:**
Yes. Accuracy went up on all three seeds, macro F1 went up on all three, and the spread between seeds dropped from 26 points to 9. The model stopped collapsing to `question`: on seed 42 it now gets all 5 `trip_report` posts right (it got 0 before), and `rant` is above 0 on every seed. The training loss confirms the diagnosis. With 10 epochs it fell to 0.86 by the end, well below the ~1.39 of a random guesser, where before it stayed at 1.35. The validation loss was still falling at epoch 10 (1.02), so this doesn't look like overfitting yet. The trained model now beats the baseline on seed 42 (0.696 vs 0.565). No criterion changed from MISSED to MET, though: the improvement was real but not big enough to reach my targets.

---

## What's Still Broken

**Criterion 1, overall accuracy ≥ 0.80 (best 0.696).**
What I'd do: collect up to 200+ posts, especially more rants, and try more epochs as a separate, measured change, since validation loss was still going down at epoch 10. Why I stopped: the brief allows one change, and I ran out of time.

**Criterion 2, per-label F1 (`rant` 0.33–0.57, `question` 0.53–0.67).**
`rant` is still the weakest label. In the after-matrix its 5 posts went to four different labels (1 right, 2 `question`, 1 `advice`, 1 `trip_report`). `rant` has the fewest training examples (21 per split), and it's the label my own rules define *against* surface features ("a rant can contain a question", "frustration can be part of a trip story"). What I'd do: add about 30 more rants, the brief's "add examples to your thinnest label" fix. Why I stopped: one change only.

**Criterion 3, beat the baseline by ≥ 20 points (+13 on seed 42).**
It now beats the baseline, but by 13 points, not 20. The baseline was also only run on seed 42's test split. What I'd do: run `baseline.py` on the seed 7 and seed 2024 test splits so the comparison covers all three seeds. Why I stopped: time.

**The gap between what I meant my labels to capture and what the model learned:**
I meant my labels to capture the writer's *purpose*, so that a rant with a question in it is still a rant and a trip story full of tips is still a trip report. The matrix suggests the model learned closer to surface form instead: it separates `trip_report` (long first-person stories) and `advice` well, but rants get scattered to `question`, `advice` and `trip_report`, which are exactly the labels whose surface features (a question mark, a recommendation, a story) my purpose rule says to ignore.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

---

## Capstone

**What This Extends**

TakeMeter, my unit 5–6 classifier that sorts r/travel posts into `question`, `advice`, `trip_report` or `rant` by the writer's main purpose (DistilBERT fine-tuned on 151 posts I labelled). Before the capstone it only ran inside a training notebook, plus a small `demo.py` I wrote for Demo Day that classified posts in the terminal but recorded nothing. What's new: every classification now writes a structured log record, bad input is rejected and logged instead of crashing or being skipped, a batch mode runs a file of posts with a timing summary, and I measured what one run costs.

**The Shape**

**Shape A: deploy and instrument.** The extension is the operational layer around the classifier I already have: one documented start command (`python demo.py --batch trial_posts.txt`), a structured log (`logs/predictions.jsonl`) with a record for every load, prediction, rejection and error, and a measured cost per post in seconds of CPU.

Out of scope, on purpose:
- **No changes to the model.** No new labels, no new training data, no retraining beyond the 10-epoch setup from unit 6. The model is what it was.
- **No hosting.** The model is ~270 MB and the free host has 512 MB of memory, so it runs locally (Path B).
- **No new interface.** It stays a command-line tool. No web page and no API endpoint.

**Running It**

Path B, local with logs. The start command, the environment it needs (Python 3.11–3.13, pinned packages, the ~268 MB base model and the ~268 MB trained model) and how to read the log back are in [RUNNING.md](RUNNING.md), section 3 of the Quick start.

**Instrumentation**

Every time `demo.py` loads the model or classifies a post, `demo.py::log_record` appends one JSON record to `logs/predictions.jsonl`. Rejected and failed runs are logged too: a bad input gets `status: "rejected"` with the reason, and any exception during classification gets `status: "error"` with the error type and message. Each record holds:

| Field | What it is |
|---|---|
| `ts` | UTC timestamp, to the millisecond |
| `session` | One id per run of the script, so each trial can be told apart |
| `event` | `load` (model loaded) or `predict` (one post) |
| `mode` | `batch`, `examples` or `interactive` |
| `model` | Which saved model answered (`models/takemeter` = 10 epochs) |
| `input`, `input_chars` | The post (first 300 characters) and its full length |
| `input_tokens`, `truncated` | How many tokens it is, and whether it went over the 128 the model reads |
| `status` | `ok`, `rejected` or `error` |
| `label`, `confidence`, `scores` | The prediction, its probability, and all four label probabilities |
| `expected` | My own label for the post (batch mode), so matches can be counted later |
| `duration_ms` | How long that one classification took, end to end |
| `error` | Why it was rejected or failed (`null` when it worked) |

Fifteen records from my first instrumented run (`python demo.py --log 16`), including the model load and the two rejected inputs:

```
2026-11-21T23:50:47.381+00:00  load          312 ms  model loaded
2026-11-21T23:50:48.002+00:00  ok            605 ms  trip_report   40%  'Just got back from Lisbon. Honestly the trams'
2026-11-21T23:50:48.064+00:00  ok             60 ms  advice        43%  'Spent 3 weeks in Vietnam last spring. If you '
2026-11-21T23:50:48.131+00:00  ok             65 ms  question      36%  'Why does every airline now charge for seat se'
2026-11-21T23:50:48.193+00:00  ok             60 ms  question      40%  "I'm in Rome right now and it's my first time "
2026-11-21T23:50:48.239+00:00  ok             46 ms  question      37%  'Have you tried booking directly with the hote'
2026-11-21T23:50:48.296+00:00  ok             54 ms  question      29%  'Hostels in Amsterdam are getting ridiculous. '
2026-11-21T23:50:48.341+00:00  ok             52 ms  trip_report   34%  'Day 4 in Japan. Kyoto was beautiful but I und'
2026-11-21T23:50:48.402+00:00  ok             51 ms  question      27%  'Took the night train from Vienna to Venice. W'
2026-11-21T23:50:48.459+00:00  ok             54 ms  advice        52%  "If you're flying into Lisbon, skip the taxi l"
2026-11-21T23:50:48.521+00:00  ok             62 ms  question      34%  "Third time this year my checked bag didn't ma"
2026-11-21T23:50:48.585+00:00  ok             60 ms  trip_report   40%  'Just got back from 5 days in Hanoi. Spent mos'
2026-11-21T23:50:48.698+00:00  ok            113 ms  trip_report   41%  'Two weeks in Peru, finally home and still pro'
2026-11-21T23:50:48.700+00:00  rejected        0 ms  -               -  ''
2026-11-21T23:50:48.702+00:00  rejected        0 ms  -               -  '   \t  '
```

The full JSON for a run, one record per line, is under the run log below. The whole log is committed in `logs/predictions.jsonl`. I tested the failure path with an empty post and a whitespace-only post: both were rejected and logged. No run raised an error, so there's no `status: "error"` record yet.

**What It Costs**

TakeMeter makes no API calls, so the cost is **compute time on my laptop CPU** (Windows, CPU only, torch 2.15.0+cpu).

- **Measured cost per run (one post classified): 62.6 ms of CPU time.** That's the mean `duration_ms` over all 36 classifications in my three trials (12 real posts × 3 runs: 63.1, 61.6 and 63.2 ms per trial), read from the log records, not estimated.
- **Plus a one-time model load per session: about 146 ms** (142–149 ms in the three trials; 312 ms the first time the files were read from disk).
- **API spend: $0. Tokens: none billed.** The model runs locally.

**For a hundred people a day**, if each person classifies 10 posts in one session:
100 sessions × 146 ms = 14.6 s of loading, plus 100 × 10 posts × 62.6 ms = 62.6 s of classifying, so **about 77 seconds of CPU per day**, and still $0 in API cost. On a hosted server the real cost would be keeping ~270 MB of model in memory all day, not the seconds of compute.

**Run Log and Verdicts**

The target has to hold in all three trials. Run with `python demo.py --batch trial_posts.txt` three times, with nothing changed in between, then `python trial_report.py before` (it reads the three sessions back from the log). The full output, with every record from Run 1, is in `results/capstone_before.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every post leaves a complete log record | 14 of 14 | 14/14 | 14/14 | 14/14 | MET |
| 2. Bad inputs rejected and logged | 2 of 2 | 2/2 | 2/2 | 2/2 | MET |
| 3. Real posts classified under 66 ms (incl. first) | 10 of 12 | 10/12 | 10/12 | 10/12 | MET |
| 4. Mean ms per classified post (cost) | < 110 ms | 63.1 ms | 61.6 ms | 63.2 ms | MET |
| 5. Real posts matching my label | ≥ 8 of 12 | 7/12 | 7/12 | 7/12 | MISSED |

Per-post timings (ms), in file order:
- Run 1: model load 146 ms; posts: 140, 52, 54, 51, 43, 52, 49, 47, 51, 57, 57, 104
- Run 2: model load 149 ms; posts: 139, 50, 54, 51, 40, 48, 47, 45, 48, 56, 56, 105
- Run 3: model load 142 ms; posts: 147, 56, 58, 55, 41, 48, 48, 46, 50, 52, 52, 104

Real output for each criterion, from Run 1 (`logs/predictions.jsonl`, written by `demo.py::log_record` via `demo.py::classify`):

Criterion 2, the two bad inputs:
```
{"ts": "2026-11-22T00:20:28.775+00:00", "status": "rejected", "label": null, "confidence": null, "expected": "rejected", "duration_ms": 0.01, "input_tokens": null, "truncated": null, "error": "empty or whitespace-only post", "input": ""}
{"ts": "2026-11-22T00:20:28.775+00:00", "status": "rejected", "label": null, "confidence": null, "expected": "rejected", "duration_ms": 0.01, "input_tokens": null, "truncated": null, "error": "empty or whitespace-only post", "input": "   \t  "}
```

Criteria 3 and 4, the two slow posts and the fastest:
```
{"ts": "2026-11-22T00:20:28.135+00:00", "status": "ok", "label": "trip_report", "confidence": 0.3984, "expected": "trip_report", "duration_ms": 140.3, "input_tokens": 46, "truncated": false, "error": null, "input": "Just got back from Lisbon. Honestly the trams were a nightma"}
{"ts": "2026-11-22T00:20:28.773+00:00", "status": "ok", "label": "trip_report", "confidence": 0.4082, "expected": "trip_report", "duration_ms": 104.1, "input_tokens": 290, "truncated": true, "error": null, "input": "Two weeks in Peru, finally home and still processing it. We "}
{"ts": "2026-11-22T00:20:28.344+00:00", "status": "ok", "label": "question", "confidence": 0.3658, "expected": "advice", "duration_ms": 43.4, "input_tokens": 26, "truncated": false, "error": null, "input": "Have you tried booking directly with the hotel instead? I di"}
```

Criterion 5, the five posts that didn't match my label:
```
{"ts": "2026-11-22T00:20:28.245+00:00", "status": "ok", "label": "question", "confidence": 0.3644, "expected": "rant", "duration_ms": 54.1, "input_tokens": 48, "truncated": false, "error": null, "input": "Why does every airline now charge for seat selection?? I pai"}
{"ts": "2026-11-22T00:20:28.344+00:00", "status": "ok", "label": "question", "confidence": 0.3658, "expected": "advice", "duration_ms": 43.4, "input_tokens": 26, "truncated": false, "error": null, "input": "Have you tried booking directly with the hotel instead? I di"}
{"ts": "2026-11-22T00:20:28.398+00:00", "status": "ok", "label": "question", "confidence": 0.2924, "expected": "rant", "duration_ms": 51.6, "input_tokens": 39, "truncated": false, "error": null, "input": "Hostels in Amsterdam are getting ridiculous. EUR 70 for a bu"}
{"ts": "2026-11-22T00:20:28.497+00:00", "status": "ok", "label": "question", "confidence": 0.2715, "expected": "trip_report", "duration_ms": 46.7, "input_tokens": 34, "truncated": false, "error": null, "input": "Took the night train from Vienna to Venice. Would I do it ag"}
{"ts": "2026-11-22T00:20:28.608+00:00", "status": "ok", "label": "question", "confidence": 0.3363, "expected": "rant", "duration_ms": 56.8, "input_tokens": 51, "truncated": false, "error": null, "input": "Third time this year my checked bag didn't make the connecti"}
```

Verdicts and diagnoses:

- **1, MET.** All 14 records were complete in every run, including the two rejections.
- **2, MET.** Both bad inputs were rejected with a message and logged in every run, without reaching the model (0.01 ms).
- **3, MET, but only just.** Exactly 10 of 12 every time, and the same two posts were slow in all three runs. **The first post after loading (139–147 ms):** this is a warm-up cost in the model stage. The first call through the model is slower than the rest, even though the Lisbon post is a normal 46 tokens. **The long Peru post (104–105 ms):** it is 290 tokens, so the model reads the full 128-token window instead of the usual ~40–50 tokens, and the model's work grows with the number of tokens it reads. One more slow post would turn this into a miss.
- **4, MET.** 62–63 ms mean per post, well under 110.
- **5, MISSED (7/12 in every run).** **Stage:** the classifier itself, the fine-tuned DistilBERT whose highest-scoring label `demo.py::classify` returns. **Mechanism:** all 5 misses were predicted `question`, and with low confidence (27–37%). Across all 12 posts the top confidence was only 27–52%, close to the flat 25% of a pure guess. So the model hasn't separated the four labels well, and when the scores are close, `question` comes out on top, especially when the post contains a question mark or a question (4 of the 5 misses do: "??", "Have you tried…?", "Would I do it again?", "Why do we even pay…?"). All three rants in the trial set went to `question`, the same pattern as my unit 6 confusion matrix. The result was identical in all three runs because prediction has no randomness, so this is a property of the trained model, not bad luck in one run. The underlying cause is that the model is still undertrained: in unit 6 its validation loss was still falling at epoch 10 (1.02), and training loss had only reached 0.86.

**The Improvement**

**What I changed:** I trained the model for **20 epochs instead of 10**, with nothing else changed: same 151 labels, same seed (42), same learning rate and batch size, same trial file, same code path. It's run as `python demo.py --epochs 20 --batch trial_posts.txt`, which trains once into `models/takemeter_e20/` and leaves the 10-epoch model untouched.

**Why:** the diagnosis for criterion 5 names the model stage. Its confidences are nearly flat (27–52%), and unit 6 showed it was still improving when training stopped at 10 epochs. More training is the one change aimed at that mechanism. It doesn't change the model's size, so it shouldn't change the timing criteria (3 and 4). This crosses one of my out-of-scope lines ("no retraining beyond the 10-epoch setup"). I'm doing it on purpose, because the diagnosis pointed at the model and not at the operational layer.
