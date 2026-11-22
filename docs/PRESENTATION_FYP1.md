# FYP-1 presentation guide (2026-11-24)

**Purpose:** what to show, in what order, which numbers to quote, how to word them
honestly, and how to answer likely questions. The FYP-1 target is the project
"about 30–40% working" (owner, 2026-11-21): the perception foundation running on the
team's own office footage, plus the full system design. All numbers here come from
[S01_RESULTS.md](S01_RESULTS.md); do not quote numbers that are not there.

## 1. The one-sentence story

> ContextGuard compares **what is expected** in a faculty office with **what is
> observed** on camera, to flag *potential* anomalies for a human to review. In
> FYP-1 we built and measured the observation half: a CPU pipeline that turns
> recorded office video into anonymous, structured, per-frame observations of people,
> laptops and backpacks in configured zones.

## 2. Suggested slide outline (about 12 slides)

| # | Slide | Content | Source |
| --- | --- | --- | --- |
| 1 | Title | ContextGuard: context-aware anomaly detection for a faculty office | — |
| 2 | Problem | Generic CCTV flags motion or objects, not context. The same event (a laptop leaving) is normal or not depending on permission and who is expected | MASTER_PLAN § 1–3 |
| 3 | Idea and contribution | Expected vs observed over time → explainable *potential-anomaly* alerts with evidence, for human review. Two target anomalies: excess simultaneous visitors; departure of a registered asset against its permission | CLAUDE.md, MASTER_PLAN |
| 4 | Scope: FYP-1 vs full system | Show the **workflow diagram**. Green/yellow = built (perception); grey = designed (reasoning, evidence, feedback) | [WORKFLOW.md](WORKFLOW.md) |
| 5 | Data | One staged, consented session (S01): 8 scenarios, 3 volunteers, iPhone 1080p, 30 fps. Protocol, consent, anonymous volunteer codes, no audio used, footage never in the public repo | RECORDING_PROTOCOL § 8, D24, D29, D31 |
| 6 | Pipeline | YOLO (COCO-pretrained, CPU) → class-wise ByteTrack (anonymous IDs) → polygon zones (doorway, desk area, foreground) → per-frame JSONL + annotated video + run manifest | [PIPELINE.md](PIPELINE.md) |
| 7 | **Demo** | Play 3–4 annotated clips (§ 3) | `~/contextguard-data/runs/S01_demo/yolo11s/` |
| 8 | How we measured | 202 seconds labelled by hand from exact frames **before** any comparison; rules frozen in advance (D34); all four models reported | [S01_RESULTS_PLAN.md](S01_RESULTS_PLAN.md) |
| 9 | Results | The four-model table (§ 4) | S01_RESULTS § 3 |
| 10 | Key insight | "Laptop gone from the desk" looks the same for hidden (SC06), carried out (SC05) and moved (SC08). Perception alone cannot decide; this motivates the temporal/context reasoning stage | S01_RESULTS § 4, WORKFLOW § 3 |
| 11 | Honest status and limitations | SYS-01–08 all PLANNED / NOT RUN; development results, not held-out; backpack weak; single session | [SYS_STATUS.md](SYS_STATUS.md), S01_RESULTS § 9 |
| 12 | Next: FYP-2 roadmap | Occupancy inference and durations; asset state with affirmative departure; session context and permissions; evidence clips and explanations; reviewer feedback; a held-out recording session | WORKFLOW § 1 |

## 3. Demo clips

Play the **annotated** videos made with the demo model **yolo11s** (D35). Never play
the original `.MOV` files: they contain audio, and the consent form says no audio is
used (D31). Use VLC; the annotated files are `mp4v` MP4.

The recommended clips and what to point at are filled in after the demo videos are
reviewed; see § 3a.

### 3a. Recommended clips

*(To be completed after the yolo11s demo videos are checked.)*

## 4. Numbers to quote (with the right wording)

| Say | Number | Always add |
| --- | --- | --- |
| People counted exactly | **97.0–98.5%** of 202 labelled seconds (yolo11s: 97.0%) | "development results on our own tuning footage" |
| Laptop found when visible | **84.8–87.5%** (yolo11s: 87.5%) | "misses happen when it is carried edge-on or lying on the PC tower" |
| Backpack found when visible | yolo11s **33.8%**; others ≤ 1% | "the weak point: a dark bag on a dark chair" |
| Speed, CPU only | nano ~17 frames/s, small ~7.5–8 frames/s on a laptop i5 | "recorded video; not real time" |
| SYS cases | **0 of 8 run** | "the reasoning stage is designed, not built; by design we do not count a missing alert as a pass" |

**Never say:**
- "98% accuracy" without "development results on our tuning footage";
- "detects theft", "catches intruders" or "unauthorised person". Say "potential
  anomaly for human review"; the system never infers intent;
- "real-time";
- "the system knows the laptop was removed": it only observes that the laptop is no
  longer detected;
- "SYS-0x passed".

## 5. Why yolo11s (if asked)

- We fixed a selection rule in writing **before** seeing results: best person count,
  ties broken by laptop recall, then speed. All four models tied on persons, within
  2 points.
- The rule picked **yolo26s**. yolo11s tied with it on persons (97.0%) and laptop
  (87.5%).
- The rule had left out the **backpack**, which is one of our two registered asset
  types. Only yolo11s detects it meaningfully (33.8% vs ≤ 1%), and it keeps one
  backpack track through SC01–SC03.
- So we chose yolo11s, recorded as an **explicit, documented deviation** (D35). We
  still report all four models.
- Because we chose after seeing results, we do **not** claim yolo11s generalises
  better. That needs a held-out session.

## 6. Likely questions and short answers

| Question | Answer |
| --- | --- |
| Why not train your own model? | Too little data for training from scratch. Pretrained COCO models work for people and laptops; we fine-tune only against documented failures (the backpack is the candidate) |
| Is 98% good? | It is a development result on the same footage we tuned on (one session, three volunteers). We need a held-out session to estimate real performance |
| Why only one session? | Time; owner decision D29. It is stated as a limitation, and the results are labelled as development results |
| How do you avoid biased labels? | The rules and metrics were frozen before labelling (D34). Labels were made from exact-frame stills before seeing any output. Corrections were made only from stills, before scoring. Later doubtful cases were reported, not changed |
| How is privacy handled? | Signed consent, anonymous codes (V1–V3), no face recognition or identity, anonymous clip-scoped track IDs, footage and frames never in the public repository, audio not used |
| What is "occupancy = null"? | Visible people ≠ people in the room (someone may be hidden). We have not built occupancy inference, so we record it as unknown rather than copying the visible count |
| How will you tell occlusion from removal? | Not by the detector: by the planned asset-state and temporal reasoning, which needs affirmative evidence of departure (carried by a person who exits through the doorway, not reappearing). Never by a missed detection alone |
| Why ByteTrack per class? | ByteTrack matches by box overlap and ignores class, so a laptop box could take over a person's track; one tracker per class prevents that |
| Why CPU? | Project constraint (laptop, no GPU). The pipeline processes recorded video |
| What licence? | AGPL-3.0, matching Ultralytics (D25) |

## 7. Practical checklist

- Copy the chosen annotated clips (and VLC) to the presentation laptop, and test
  playback there beforehand.
- Open the GitHub repository (public) to show code, the docs and the passing tests.
  It contains no footage.
- Optional live run on a short clip:
  `python -B scripts/run_pipeline.py --input <clip> --output <new dir> --weights weights/yolo11s.pt --zones configs/zones/S01_office_v1.json`.
  SC01 (15 s) takes about a minute with yolo11s.
- Show one line of `observations.jsonl` and the `manifest.json` (settings, model
  SHA-256, warnings) to show the output is structured and traceable.
