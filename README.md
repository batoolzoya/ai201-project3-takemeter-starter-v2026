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

**Pre-labelling disclosure:** None. All 151 labels were typed by me while collecting. The first 20 are marked `cold`.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



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
