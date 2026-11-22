# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

Overall accuracy on the held-out test set is at least 0.80 on all three seeds.

**Why this target:** My labels are based on the writer's purpose, which I expect to be clear in at least 8 out of 10 posts. The other 20% are edge cases like the ones in my notes, such as rants that ask questions or trip reports full of tips.

---

## 2.

Every label (question, advice, trip_report, rant) has an F1 of at least 0.7 on all three seeds, except rant, which needs at least 0.50.

**Why this target:** Close to my overall target for the three bigger labels. Rant is looser because it is my smallest label (about 12% of my data), so only a few rants land in each test split and its score will jump around.

---

## 3.

The trained model's accuracy is at least 20 points higher than the untrained baseline's accuracy on the same test posts.

**Why this target:** The trained model got to practice on my own labelled posts and my own choices. If it isn't at least 20 points better than a model that only read my definitions, the training didn't add much.

---

## 4.

My labels agree with the staff labels on at least 70% of the 30 staff posts.

**Why this target:** I expect the staff's written rules to be clear enough to arrive at consistent results at least 7/10 times.

---

## 5.

In labels.csv, no label is more than 50% of the rows and no label is less than 10%.

**Why this target:** Currently, my biggest (advice) label is at 41% and smallest (rant) at 12%. I do not wish for the disparity to grow as that would adversely impact the training by neglecting smaller labels.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone criteria (written before any capstone trial results)

1. In each trial, 14 of the 14 posts in trial_posts.txt leave a record in logs/predictions.jsonl with a status, a duration_ms, and either a label or an error.
   Why: This is plain code and if incorrect, the reason is a bug. So, we would like this to be perfect.

2. In each trial, 2 of the 2 bad inputs (empty post, whitespace-only post) are rejected with a message and logged with status "rejected", instead of being classified or crashing.
   Why: We want the system to be capable of clearly recognizing bad inputs rather than guess a label for nothing.

3. In each trial, 10 of the 12 real posts are classified in under 66 ms each (counting every post, including the first one after the model loads).
   Why: This is the target we achieved in the demo and expect to be minimum moving forward since we want an efficient system.

4. In each trial, the mean time per classified post (my cost per run, in CPU time) is under 110 ms.
   Why: My first run's mean was 107 ms so I kept a little wiggle room but want to stay close to it.

5. In each trial, at least 8 of the 12 real posts get the same label I gave them.
   Why: Rant is tricky as it is often short and can easily resemble any of the other labels. It is also my thinnest label. Additionally, the system seems to incline towards question as many posts/comments from other labels contain questions. We achieved 7/12 in the first run and expect higher than that for the trials. Also, a trained model should at least give higher than a 50% match, even with four categories.
