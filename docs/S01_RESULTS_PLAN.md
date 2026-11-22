# S01 development-results plan (FYP-1)

Status: **APPROVED by the owner on 2026-11-23 (D34). Frozen.** Written 2026-11-23,
**before** any ground-truth label exists and before any pipeline output on S01 has
been compared with labels. The rules below are frozen. Any later change is logged
in `PROGRESS.md` with its reason, and results under both the old and the new rule
are reported.

## 1. What these results are, and are not

- **Development results on the data used for tuning** (D30). S01 is the only FYP-1
  dataset (D29): one session, one camera position, three volunteers, about 13 minutes
  of recording on 2026-11-20. The zones were drawn on S01 (D33), so the numbers are
  optimistic.
- They are **not** a held-out evaluation, not an accuracy estimate for other rooms,
  cameras or people, and not a pass of any SYS case. SYS-01–SYS-08 stay
  **PLANNED / NOT RUN**.
- The pipeline produces **observations** only: visible counts, tracks, zone
  membership. It makes no anomaly decision. Visible counts are not inferred
  occupancy, which stays `null`.
- There are **no pass/fail targets**. The owner has not set numeric targets, and none
  are invented afterwards. Results are descriptive.

## 2. Footage

| Used for results | Clips |
| --- | --- |
| Yes | SC01–SC08 of S01 (`cg_20261120_S01_SC0{1..8}_t1.MOV`), 202 labelled seconds in total |
| No (exploratory only, D32) | DOC01, DOC02 (camera moved; document handling EXPERIMENTAL) |

Known content deviations, from the protocol's § 8, are reported alongside the
results and not hidden:
- SC04 shows no brief exceedance;
- in SC08 the laptop is put on top of the PC tower (still partly visible there) and
  is not returned to the desk;
- SC02–SC04 do not end with an empty room.

## 3. Ground truth

**Labeller.** The owner, alone. There is no second labeller, so inter-annotator
agreement cannot be measured; this is stated as a limitation.

**Material.** One still per second, exported from the original files:
`~/contextguard-data/labelling/S01/<SCxx>/<SCxx>_tNNNs.jpg`. Second `t` is
decoded frame `round(t × reported_fps)`. That is exactly the frame the results are
read from (§ 5), so the labeller and the pipeline look at the same image. The
frame index is printed on each still and listed in `frame_index.json`. The labeller
may also watch the clip for context, but must not watch any annotated output
before all labels are finished.

**Sheet.** `~/contextguard-data/labels/S01_labels.csv` is pre-filled with every
`clip_file, time_s` row (202 rows). The columns are those of
`docs/dataset/ground_truth_template.csv`.

**Rules for each still:**

| Column | Value |
| --- | --- |
| `persons_visible` | Number of people you can see in the still, even partially (a head, a torso, or legs is enough; a hand alone is not). Count a person in the doorway even if only part of them shows. |
| `laptop_visible` | `1` if any part of the laptop can be seen, including while it is carried; otherwise `0`. |
| `backpack_visible` | `1` if any part of the backpack can be seen, including while it is carried; otherwise `0`. |
| `laptop_occluded` | `1` if the laptop is in the room but cannot be seen, e.g. hidden behind a person (SC06); otherwise `0`.* A laptop carried out of the room is `visible = 0, occluded = 0`. |
| `backpack_occluded` | As for the laptop. |
| `notes` | Anything unusual: a person only partly in frame, motion blur, unsure. Write `unsure` when you are not certain. |

\* *Correction 2026-11-23, after labelling and before any scoring:* this example
originally also said "or out of view on the PC tower (SC08)". That was a factual
error by Claude: the laptop on the PC tower is partly visible, so by the rule it is
`visible = 1`, as the owner labelled it. Only the example was wrong; the rule is
unchanged (logged in `PROGRESS.md`).

**Do not change the rules mid-way.** If a case is unclear, label your best judgement
and write `unsure` in `notes`. Unsure seconds are reported both included and
excluded.

**Second source of truth: visitors per clip.** The number of distinct visitors per
clip comes from the session log, written before any results: SC01 0, SC02 1,
SC03 2, SC04 2, SC05 1, SC06 1, SC07 1, SC08 1.

## 4. Pipeline settings (fixed in advance)

| Setting | Value | Why |
| --- | --- | --- |
| Models | **All four** candidates: yolo26n, yolo26s, yolo11n, yolo11s (SHA-256 in `MODELS.md`) | Reporting all four avoids picking a model on the results and hiding the others |
| Input size | `imgsz 640` | Ultralytics default; not tuned |
| Detector confidence | `conf 0.10` | Pipeline default; feeds ByteTrack's low-score stage |
| Count confidence | `count_conf 0.25` | Pipeline default (count policy v1) |
| NMS IoU | `0.7` | Pipeline default |
| Tracker | `configs/tracker/bytetrack.json`, one tracker per class | Pipeline default |
| Zones | `configs/zones/S01_office_v1.json` (D33) | Approved by the owner |
| Frames | Every frame (`stride 1`), CPU, 4 threads | |
| Code | The committed pipeline at the commit recorded in each run manifest | |

Each run writes `observations.jsonl` and `manifest.json` (settings, model SHA-256,
source SHA-256, warnings) under `~/contextguard-data/runs/S01/<model>/<clip>/`,
outside the repository.

**Secondary analysis, labelled as such.** Person counting is also recomputed from the
same JSONL at `count_conf` 0.15 and 0.40, to show sensitivity. It does not replace
the primary result at 0.25.

## 5. Matching rule

For each labelled row `(clip, t)`, the prediction is the observation record with
`source_frame_index == round(t × reported_fps)` of that clip. There is no time window
and no smoothing. If a record is missing, the row is reported as "no prediction",
never silently dropped.

## 6. Metrics

All are reported **per clip and overall, for each model.**

1. **Visible-person count.** Predicted `counts.visible_persons` vs `persons_visible`:
   - exact-match rate (share of seconds where the counts are equal);
   - mean absolute error;
   - number of over-count and under-count seconds;
   - confusion table of true 0/1/2 vs predicted 0/1/2/3+.
2. **Laptop presence.** Predicted present = `visible_by_class.laptop ≥ 1`, vs
   `laptop_visible`:
   - TP, FN, FP, TN;
   - recall = TP / (TP + FN), precision = TP / (TP + FP); "not defined" when the
     denominator is 0.
3. **Backpack presence.** The same, with `backpack`.
4. **Occluded seconds.** For rows with `*_occluded = 1`:
   - how often a box was still counted (it should not be, because the object is not
     visible);
   - how often the tracker kept a `lost`/predicted box for it. That box is
     continuity information only and is never counted.
5. **Track fragmentation (people).** Per clip, the number of distinct person track
   IDs with at least 15 observed frames (0.5 s), compared with the visitors per clip
   (§ 3). The total ID count is also reported. Identity switches are **not**
   measured: that needs per-frame identity labels, which do not exist.
6. **Zones (descriptive, no metric).** Per clip, the seconds with at least one person
   in `doorway`, `desk_area` and `foreground`, and the seconds with a laptop or
   backpack in `desk_area`. These are compared in words with the storyline in the
   session log, e.g. "SC05: the laptop leaves `desk_area` at about 12–14 s".
7. **Speed.** Wall-clock frames/s of the full pipeline per model on the project
   laptop (i5-1135G7, CPU only).

**Unsure labels.** Every metric is computed with all rows, and again without rows
marked `unsure`.

## 7. Choosing the demo model

Rule, fixed now: the demo model is the one with the highest **overall person
exact-match rate** (metric 1). Ties within 2 percentage points are broken by higher
laptop recall, then by speed. Results for all four models are reported whichever is
chosen. Annotated videos for the presentation are made with the demo model.

## 8. Reporting

- A results document in `docs/` with every table above: all clips, all models,
  including failures. It contains no frames of people; it is a public repository.
- Failure cases are described in words with clip and second, e.g. "SC06 t = 14 s:
  person not detected while partly out of frame".
- Limitations stated with the results:
  - one session, three volunteers, a single labeller;
  - tuned on the same data (zones drawn on S01);
  - 1 Hz labels;
  - the chest-height camera;
  - COCO-pretrained models, with no fine-tuning;
  - detector confidence is not a calibrated probability.
- Ground-truth labels and run outputs stay in `~/contextguard-data/` and are not
  committed. Only aggregate numbers go in the repository.
