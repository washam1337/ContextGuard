# S01 development results (FYP-1)

**Date:** 2026-11-23. **Status:** final for FYP-1 under the frozen plan
[`S01_RESULTS_PLAN.md`](S01_RESULTS_PLAN.md) (D34).

> **What these numbers are.** These are **development results on the same footage
> used for tuning** (D30): one session (S01), one camera position, three volunteers,
> eight short scripted clips, 202 labelled seconds, one labeller. The zones were
> drawn on this footage.
>
> They are **not** a held-out evaluation, **not** an accuracy estimate for other
> rooms, cameras or people, and **not** a pass of any SYS case. SYS-01–SYS-08 remain
> **PLANNED / NOT RUN**: the pipeline produces observations only (visible counts,
> tracks, zone membership) and makes no anomaly decision. Visible counts are not
> occupancy. Inferred occupancy stays `null`.

## 1. Summary

1. **People:** counted correctly in 196–199 of 202 labelled seconds (97.0–98.5%)
   by all four COCO-pretrained models, at the fixed threshold. The few errors fall at
   the same moments for every model: a person half-hidden at the door, two people
   overlapping, and one probable labelling miss (§ 6).
2. **Laptop:** detected in 156–161 of 184 visible seconds (84.8–87.5%). Almost every
   miss is in two situations, which all four models fail: the laptop **being carried**
   (held edge-on at the visitor's side, SC05) and the laptop **lying flat on top of the
   PC tower** (SC08). On the desk it is detected in nearly every second.
3. **Backpack:** the weak point. A dark backpack on a dark chair is detected by
   **yolo11s in 67 of 198 visible seconds (33.8%)**, and by the other three models in
   at most 2 seconds. No model produced a false backpack detection.
4. **Tracking:** one visitor normally keeps one anonymous track ID through the clip
   (SC02, SC05, SC06, SC08). Track IDs fragment when people overlap or stand behind
   the PC tower (SC04: 3 IDs for 2 visitors; SC07: 3–4 lasting IDs for 1 visitor).
5. **Zones:** arrivals and departures appear in the `doorway` zone at the right
   seconds. "Laptop leaves the desk area" looks **the same** for a hidden laptop (SC06)
   and a carried-out laptop (SC05). Frame-level perception cannot separate occlusion
   from departure. That is the job of the later temporal/context reasoning stage, and
   it is why the project never treats a missing detection as departure.
6. **Speed (CPU only, i5-1135G7):** nano models about 17 frames/s, small models
   about 7.5–8 frames/s, for the full pipeline on 1920×1080 video.
7. **Demo model: yolo11s** (owner decision D35, a recorded deviation). The frozen rule
   (§ 7 of the plan) selects **yolo26s**: all four models were within 2 points on
   person counting, yolo26s and yolo11s tied on laptop recall (87.5%), and yolo26s was
   faster (7.9 vs 7.47 fps). The rule does not consider the backpack, on which yolo11s
   is far better, so the owner chose yolo11s for the presentation (§ 5).

## 2. Setup

| Item | Value |
| --- | --- |
| Footage | S01 SC01–SC08 (`~/contextguard-data/raw/S01/`, read-only; SHA-256 in `review/S01_footage_check/S01_originals.sha256`) |
| Ground truth | `~/contextguard-data/labels/S01_labels.csv` (SHA-256 `bebfd587…77af`): 202 rows, one per second, owner-labelled from exact-frame stills. No row marked `unsure` |
| Label corrections | 9 seconds corrected **before any scoring**, after a rule-consistency check made from the stills only, without model output; owner-approved (see `PROGRESS.md`). The original sheet is kept as `S01_labels_owner_v1.csv` |
| Models | yolo26n, yolo26s, yolo11n, yolo11s (COCO-pretrained, Ultralytics 8.4.212, SHA-256 in [MODELS.md](MODELS.md)) |
| Settings (fixed in the plan) | imgsz 640, detector conf 0.10, count_conf 0.25, NMS IoU 0.7, class-wise ByteTrack (`configs/tracker/bytetrack.json`), zones `S01-office-v1` (D33), stride 1, 4 CPU threads |
| Code | Pipeline code unchanged between `720610a` and `dd4248e` (runs record one or the other). Scoring: `scripts/score_s01.py` (tested in `tests/test_score_s01.py`) |
| Outputs | `~/contextguard-data/runs/S01/<model>/<clip>/` (JSONL and manifests); results JSON `~/contextguard-data/results/S01_dev_results.json` (SHA-256 `eac81955…b86d`). None are committed |
| Matching | Label `(clip, t)` ↔ record at `source_frame_index = round(t × reported_fps)`, the same frame as the labelling still. Checked for all 202 rows; no missing predictions |

## 3. Results tables

### Overall (202 labelled seconds, pooled)

| Model | Person count exact | MAE | Over / under | Laptop recall | Laptop precision | Backpack recall | Backpack precision | Pipeline fps | Detector ms/frame (median of clip medians) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| yolo26n | 199/202 (98.5%) | 0.015 | 1 / 2 | 156/184 (84.8%) | 100.0% (0 FP) | 2/198 (1.0%) | 100.0% (0 FP) | 17.11 | 46.7 |
| yolo26s (selected by the rule) | 196/202 (97.0%) | 0.030 | 4 / 2 | 161/184 (87.5%) | 97.6% (4 FP) | 2/198 (1.0%) | 100.0% (0 FP) | 7.9 | 102.4 |
| yolo11n | 198/202 (98.0%) | 0.020 | 2 / 2 | 158/184 (85.9%) | 95.8% (7 FP) | 1/198 (0.5%) | 100.0% (0 FP) | 16.93 | 45.0 |
| **yolo11s** (demo, D35) | 196/202 (97.0%) | 0.030 | 5 / 1 | 161/184 (87.5%) | 99.4% (1 FP) | 67/198 (33.8%) | 100.0% (0 FP) | 7.47 | 107.0 |

"Exact" means the predicted visible-person count equals the labelled count in that
second. Recall is the share of labelled-visible seconds in which at least one box of
that class was counted (confidence ≥ 0.25). A presence "FP" is a second labelled not
visible in which a box of that class was counted; see § 6 for what these were.

### Person count: exact seconds per clip

| Clip | Seconds | yolo26n | yolo26s | yolo11n | yolo11s |
| --- | --- | --- | --- | --- | --- |
| SC01 empty room | 16 | 16 | 16 | 16 | 16 |
| SC02 one visitor | 21 | 20 | 20 | 20 | 21 |
| SC03 two visitors | 31 | 30 | 30 | 30 | 30 |
| SC04 second visitor | 34 | 33 | 33 | 33 | 33 |
| SC05 laptop carried out | 24 | 24 | 24 | 24 | 24 |
| SC06 laptop occluded | 26 | 26 | 26 | 26 | 26 |
| SC07 backpack carried out | 19 | 19 | 17 | 18 | 16 |
| SC08 laptop moved | 31 | 31 | 30 | 31 | 30 |

### Laptop: seconds detected / seconds visible (false-positive seconds)

| Clip | yolo26n | yolo26s | yolo11n | yolo11s |
| --- | --- | --- | --- | --- |
| SC01 | 16/16 (0) | 16/16 (0) | 16/16 (0) | 16/16 (0) |
| SC02 | 21/21 (0) | 21/21 (0) | 21/21 (0) | 21/21 (0) |
| SC03 | 21/22 (0) | 22/22 (3) | 21/22 (0) | 22/22 (0) |
| SC04 | 34/34 (0) | 34/34 (0) | 34/34 (0) | 34/34 (0) |
| SC05 | 12/22 (0) | 14/22 (0) | 12/22 (0) | 14/22 (0) |
| SC06 | 19/19 (0) | 19/19 (1) | 19/19 (7) | 19/19 (1) |
| SC07 | 19/19 (0) | 19/19 (0) | 19/19 (0) | 19/19 (0) |
| SC08 | 14/31 (0) | 16/31 (0) | 16/31 (0) | 16/31 (0) |

### Backpack: seconds detected / seconds visible

| Clip | yolo26n | yolo26s | yolo11n | yolo11s |
| --- | --- | --- | --- | --- |
| SC01 | 0/16 | 0/16 | 0/16 | 8/16 |
| SC02 | 0/21 | 0/21 | 0/21 | 4/21 |
| SC03 | 0/31 | 0/31 | 0/31 | 3/31 |
| SC04 | 0/34 | 0/34 | 0/34 | 20/34 |
| SC05 | 0/24 | 0/24 | 0/24 | 15/24 |
| SC06 | 0/26 | 0/26 | 0/26 | 8/26 |
| SC07 | 2/15 | 2/15 | 1/15 | 9/15 |
| SC08 | 0/31 | 0/31 | 0/31 | 0/31 |

In SC08 the backpack sits on the chair behind the desk, partly hidden; no model
detects it there.

### Person track IDs (IDs lasting ≥ 15 observed frames / all IDs) vs visitors

| Clip | Visitors (session log) | yolo26n | yolo26s | yolo11n | yolo11s |
| --- | --- | --- | --- | --- | --- |
| SC01 | 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| SC02 | 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| SC03 | 2 | 2 / 2 | 2 / 3 | 3 / 3 | 2 / 2 |
| SC04 | 2 | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 |
| SC05 | 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| SC06 | 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| SC07 | 1 | 3 / 5 | 3 / 4 | 4 / 5 | 3 / 6 |
| SC08 | 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |

Track IDs are anonymous and clip-scoped. More IDs than visitors means a visitor's
track was broken and restarted (fragmentation). Identity switches were not measured
(no per-frame identity labels).

### Object track IDs (additional; not a plan metric)

Added after scoring because the CG-005 exit criteria ask for object ID instability
to be recorded. Descriptive only: it uses every frame, and the ≥ 15-frame and all-IDs
counts as for people. There is **one** laptop and **one** backpack in every clip.

| Clip | Laptop IDs: yolo26n | yolo26s | yolo11n | yolo11s | Backpack IDs: yolo26n | yolo26s | yolo11n | yolo11s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SC01 | 1 / 1 | 1 / 1 | 2 / 2 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 | 1 / 1 |
| SC02 | 1 / 2 | 1 / 1 | 2 / 2 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 | 1 / 1 |
| SC03 | 2 / 3 | 2 / 2 | 4 / 5 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 | 1 / 1 |
| SC04 | 1 / 2 | 1 / 1 | 2 / 3 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 | 1 / 2 |
| SC05 | 1 / 3 | 3 / 4 | 1 / 4 | 3 / 5 | 0 / 0 | 0 / 0 | 0 / 0 | 2 / 2 |
| SC06 | 2 / 2 | 2 / 3 | 4 / 7 | 2 / 4 | 0 / 0 | 0 / 0 | 0 / 0 | 2 / 3 |
| SC07 | 2 / 2 | 2 / 3 | 3 / 3 | 1 / 1 | 1 / 2 | 2 / 3 | 1 / 1 | 2 / 2 |
| SC08 | 1 / 2 | 1 / 1 | 3 / 3 | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 1 |

Reading this table:
- The laptop keeps one ID while it stays on the desk. The ID breaks when it is
  hidden (SC06) or carried (SC05) and comes back under a new ID. So a **tracker ID is
  not a stable asset identity** (detector class ≠ tracker ID ≠ registered asset ID).
- yolo11n's extra laptop IDs include the PC-tower false detection (§ 6).
- For the backpack, yolo11s keeps **one** track through SC01–SC03, even though it is
  counted in only some seconds. ByteTrack's low-score stage keeps matching
  detections between 0.10 and 0.25. yolo26s produces many low-confidence backpack
  boxes but never starts a track (new tracks need ≥ 0.25), except in SC07 when the
  backpack is lifted.

### Occluded seconds (object in the room but labelled hidden)

| Model | Laptop occluded seconds | Counted anyway | Tracker kept a predicted box | Backpack occluded seconds | Counted anyway |
| --- | --- | --- | --- | --- | --- |
| yolo26n | 16 | 0 | 2 | 1 | 0 |
| yolo26s | 16 | 4 | 2 | 1 | 0 |
| yolo11n | 16 | 7 | 1 | 1 | 0 |
| yolo11s | 16 | 1 | 2 | 1 | 0 |

A tracker-predicted box is continuity information only and is never counted (count
policy v1). With the default track buffer (30 frames, about 1 s at 30 fps) it
survives only about 1 s of occlusion, so tracking alone cannot bridge the 6–9 s
occlusions in SC03 and SC06.

### Secondary: person-count exact rate at other count thresholds (same runs)

| Model | 0.15 | 0.25 (primary) | 0.40 |
| --- | --- | --- | --- |
| yolo26n | 97.5% | 98.5% | 99.0% |
| yolo26s | 97.0% | 97.0% | 97.5% |
| yolo11n | 96.5% | 98.0% | 98.5% |
| yolo11s | 96.5% | 97.0% | 97.0% |

Person counting is not sensitive to the threshold in this range. The primary
threshold stays 0.25 as planned; this table is not used to retune it.

### Person-count confusion, demo model yolo26s (rows: true; columns: predicted)

| True \ predicted | 0 | 1 | 2 | 3+ |
| --- | --- | --- | --- | --- |
| 0 | 46 | 2 | 0 | 0 |
| 1 | 1 | 118 | 2 | 0 |
| 2 | 0 | 1 | 32 | 0 |

## 4. Zones (descriptive, demo model yolo26s)

Each string has one character per labelled second (count of counted boxes whose
anchor is in the zone).

| Clip | What happens (session log) | What the zones show |
| --- | --- | --- |
| SC02 | V1 enters ~4 s, stands at the desk | `doorway` person at 3–6 s, then `foreground` from 7 s to the end |
| SC03 | V1 enters ~4 s, V2 ~16 s; both stay | `doorway` 4–6 s and 15 s; `foreground` 1 person from 8 s, 2 people from 16 s |
| SC04 | V1 enters ~6 s; V3 inside ~16–30 s | `doorway` 5–9 s and 15–18 s (two arrivals), 30–31 s (V3 leaving); `foreground` up to 2 people |
| SC05 | V1 takes the laptop ~12–14 s and carries it out | laptop in `desk_area` 0–13 s, then **absent from 14 s**; person back in `doorway` 20–22 s (leaving) |
| SC06 | V1 hides the laptop ~12–17 s | laptop in `desk_area` 0–11 s, **absent 12–17 s, back from 18 s** |
| SC07 | V2 takes the backpack ~10–12 s, leaves ~14–16 s | person in `desk_area` 7–12 s (standing behind the desk); `doorway` 3–4 s and 14–16 s |
| SC08 | V1 puts the laptop on the PC tower ~16–18 s | laptop in `desk_area` 0–15 s, then not detected (lying on the tower, edge-on) |

**The key observation for the next stage:** SC05 (carried out), SC06 (hidden) and
SC08 (moved to the tower) all show the same perception signal: "the laptop is no
longer detected in `desk_area`". Only context and time tell them apart:
- whether it comes back (SC06 after 6 s);
- whether a person holding it reaches the `doorway` and leaves (SC05);
- whether it stays in the room out of the detector's reach (SC08).

This is why ContextGuard keeps observation separate from inference and never
treats a missed detection as departure (domain invariant). It is the planned
reasoning stage, not something FYP-1 implements.

## 5. Choosing the demo model

- **The frozen rule** (plan § 7) applied as written: the best person exact-match is
  yolo26n at 98.5%. All four models are within 2 points (lowest 97.0%), so all tie.
  The highest laptop recall is yolo26s and yolo11s (87.5% each), so they tie again.
  The faster of those two is **yolo26s** (7.9 vs 7.47 fps). **Result: yolo26s.**
- **Trade-off the rule did not foresee:** the rule (written before any results) does
  not consider the backpack. On it, yolo11s detects 33.8% of visible seconds and
  every other model about 1%. yolo11s is otherwise equal to yolo26s on person
  counting (97.0%) and laptop recall (87.5%), slightly better on laptop precision
  (99.4% vs 97.6%), and 5% slower.
- **Decision (D35, owner, 2026-11-23): present yolo11s.** It is recorded as a
  deviation from the frozen rule, for these reasons:
  1. the backpack is one of the two registered asset classes, and the rule left it out;
  2. yolo11s ties with yolo26s on both of the rule's criteria;
  3. it is the only candidate that detects the backpack in a meaningful share of seconds;
  4. its laptop precision is higher;
  5. it is 5% slower, which does not matter for recorded video.

  Because the choice was made after seeing these results, it is a presentation choice
  and **not** evidence that yolo11s generalises better; that would need a held-out
  session. All four models' results above are unchanged.

## 6. Failure cases (described in words; no frames of people in this repository)

| Clip, second | Models | What happened |
| --- | --- | --- |
| SC02 t = 2 | yolo26n, yolo26s, yolo11n | Person half-visible at the door edge; detected at confidence **0.24**, just under the 0.25 counting threshold → counted 0 instead of 1 |
| SC03 t = 19 | all | Two people overlap: V2 walks close to the camera, motion-blurred, and hides V1 → 1 counted instead of 2. The tracker kept a predicted (uncounted) box for the hidden person |
| SC04 t = 5 | all | Counted 1 where the label says 0. The still shows a person **visible behind the door edge** (confidence 0.75), so this is very likely a **labelling miss**. The label was not changed after model output had been seen; the score stands as computed |
| SC07 t = 7, 9, 12, 16 | yolo26s (7, 9), yolo11n (9), yolo11s (7, 12, 16) | One visitor standing **behind the PC tower** (and at t = 16 at the door edge) gets **two overlapping person boxes**: one for the whole body and one for the upper body above the tower (e.g. 0.49 and 0.41) → counted 2 instead of 1. The same split causes the track fragmentation in SC07 |
| SC08 t = 3 | yolo26s, yolo11s | Counted 1 person (confidence 0.53 / 0.42, feet in `doorway`) where the label says 0: the visitor is appearing at the door, labelled from t = 4. Probably a label boundary case; not changed |
| SC05 t = 14–21 | all | Laptop **carried** edge-on at the visitor's side: not recognised as a laptop |
| SC08 t = 16–30 | all | Laptop **lying flat on top of the PC tower**, only its thin edge visible: not detected |
| SC03 t = 23, 27, 28; SC06 t = 11 | yolo26s (and others) | Laptop counted in seconds labelled hidden. In the stills **a strip of the lid is still visible** beside the person, so the detection is arguably correct and the label strict. Labels not changed |
| SC06 t = 11–17 | yolo11n | "Laptop" counted while the real laptop is hidden: the box is on the **cut-off PC tower at the bottom-left of the frame**, a different object. A genuine false detection |
| Backpack, all clips | all but yolo11s | Dark navy backpack on a dark blue chair: mostly detected below the 0.25 counting threshold. Of all backpack boxes (confidence ≥ 0.10): yolo26s 2,507, of which 2.5% reach 0.25; yolo11s 6,695, of which 31% reach 0.25; yolo26n 101 and yolo11n 99 boxes in total. Lowering a per-class threshold could raise recall, but that is tuning and would need a held-out session to validate |

## 7. Label quality

- Single labeller, 1 label per second, no inter-annotator agreement.
- 9 seconds were corrected before scoring, after a rule check made from the stills
  only (SC05 t14–19 and SC08 t16: carried laptop visible; SC07 t13: backpack hidden
  while carried; SC07 t16: person partly visible at the door).
- After scoring, three boundary cases were found that favour the model
  (SC04 t = 5, SC08 t = 3, and the laptop-lid strips in § 6). They are **reported,
  not corrected**, because any change after seeing model output would bias the
  results.

## 8. Speed

| Model | Pipeline frames/s (all 5,931 frames, 1920×1080) | Detector ms/frame |
| --- | --- | --- |
| yolo26n | 17.11 | 46.7 |
| yolo11n | 16.93 | 45.0 |
| yolo26s | 7.9 | 102.4 |
| yolo11s | 7.47 | 107.0 |

All runs are on a 4-core i5-1135G7 laptop CPU with no GPU, and include decoding,
detection, tracking, zones and JSONL writing (no video). The recordings are 30 fps,
so even the nano models run at a little over half real time; this is a
recorded-video system (FYP-1 scope). One run (yolo26s SC07) took 670 s of wall time
but only ~61 s inside the pipeline: the delay was before frame processing (the laptop
was busy or sleeping), and it does not affect the pipeline figures above.

## 9. Limitations

- **Development results only (D30):** the same footage was used to draw zones and
  will be used to present the demo; no held-out session exists (D29).
- **Small scale:** one room, one camera position at chest height, three volunteers
  (who appear in many clips), about 3.5 minutes of labelled video, one take per
  scenario.
- **Labels:** one labeller, 1 Hz, presence-level only (no boxes, no identities).
- **Models:** COCO-pretrained, not fine-tuned. Detector confidence is not a
  calibrated probability.
- **Scenario gaps:** SC04 does not show a brief exceedance, and SC08 does not show a
  return (protocol § 8), so neither is demonstrated.
- **No anomaly logic exists yet.** None of these numbers is a SYS result.

## 10. Reproduce

```bash
# runs (one per model and clip; outputs outside the repository)
python -B scripts/run_pipeline.py --input ~/contextguard-data/raw/S01/cg_20261120_S01_SC02_t1.MOV \
  --output ~/contextguard-data/runs/S01/yolo26s/SC02 --weights weights/yolo26s.pt \
  --zones configs/zones/S01_office_v1.json --threads 4 --no-video
# scoring (all models, all clips)
python -B scripts/score_s01.py --labels ~/contextguard-data/labels/S01_labels.csv \
  --runs ~/contextguard-data/runs/S01 --frame-index ~/contextguard-data/labelling/S01/frame_index.json \
  --output ~/contextguard-data/results/S01_dev_results.json
```
