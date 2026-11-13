# Perception pipeline (FYP-1 combined CG-003/004/005)

Status: **PARTIAL.** The code is implemented and tested on synthetic software
fixtures (2026-11-13). It has **not yet been validated on office footage**: no
consented recordings exist yet. See D21–D23.

```text
recorded video → YOLO detector → class-wise ByteTrack → zones + visible counts
              → observations.jsonl + annotated video + manifest.json
```

The pipeline only **observes**. It does not infer interactions, asset departure,
permissions, occupancy or anomalies; those belong to later milestones.

## Running it

```bash
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B scripts/run_pipeline.py \
  --input ~/contextguard-data/raw/cg_20261116_S01_SC02_t1.mp4 \
  --output ~/contextguard-data/runs/S01_SC02_t1_yolo26n \
  --weights weights/yolo26n.pt \
  --zones configs/zones/<session-zone-config>.json \
  --threads 4
```

| Option | Default | Meaning |
| --- | --- | --- |
| `--weights` | required | YOLO weights (candidates in [MODELS.md](MODELS.md)) |
| `--zones` | none | Zone configuration (`contextguard.zones.v1`). Without it, zone fields are empty. |
| `--imgsz` | 640 | Detector input size |
| `--conf` | 0.10 | Detector threshold. Low on purpose, because ByteTrack uses low-score boxes to keep tracks alive. |
| `--count-conf` | 0.25 | Minimum confidence for a box to be **counted** |
| `--iou` | 0.7 | Detector non-maximum-suppression IoU |
| `--stride` | 1 | Process every Nth decoded frame |
| `--max-frames` | all | Stop after N processed frames |
| `--codec` | `mp4v` | Annotated video codec: `mp4v` (.mp4), `MJPG` (.avi), `VP80` (.webm) |
| `--no-video` | off | Skip the annotated video |

The output directory must not exist, and the source video is never modified. Exit
code 0 means success, 1 means an input/output/configuration failure, 2 means bad
arguments. A failed run still writes `manifest.json` with `status: "failed"`.

Candidate comparison (speed and raw detection rates, no accuracy):

```bash
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B scripts/benchmark_models.py \
  --input <tuning clip> --weights weights/yolo26n.pt weights/yolo26s.pt weights/yolo11n.pt weights/yolo11s.pt
```

## Outputs

| File | Contents |
| --- | --- |
| `observations.jsonl` | One `contextguard.observation.v1` record per processed frame, **including frames with nothing detected** |
| `annotated.mp4` | One annotated frame per record, in order. Record field `annotated_frame_index` = video frame number. |
| `manifest.json` | `contextguard.run_manifest.v1`: run ID; status; command; code commit (plus uncommitted-changes flag); source path, size and SHA-256; reported metadata; model, weights SHA-256, class map, thresholds; tracker config; zone config and SHA-256; contracts; software and hardware; summary (frames, detections per class, track IDs, runtime, inference ms); warnings |

Outputs belong outside the repository (e.g. `~/contextguard-data/runs/`); `outputs/`
and `runs/` are also git-ignored. Annotated videos of real people must never be committed.

## Observation record (`contextguard.observation.v1`)

| Field | Meaning |
| --- | --- |
| `run_id` | Links the record to `manifest.json` |
| `source_frame_index` | Zero-based decoded frame index in the source video |
| `processed_index` | Index among processed frames (differs from the source index when stride > 1) |
| `annotated_frame_index` | Frame number in the annotated video, or `null` without video |
| `frame_width`, `frame_height` | Decoded frame size in pixels |
| `timestamp.estimated_seconds` | `source_frame_index / reported_fps`, or `null` if the FPS is invalid. Assumes constant frame rate. |
| `timestamp.decoder_pos_msec` | What the OpenCV backend reports. Recorded for comparison, not validated. |
| `timestamp.validated` | Always `false`: no timestamps are validated presentation or wall-clock times |
| `objects[]` | See below |
| `counts` | Visible counts under `contextguard.count_policy.v1` |
| `inferred_occupancy` | Always `{"value": null, "available": false, …}`: not implemented, and never filled with visible counts |
| `warnings` | Per-frame warnings (normally empty) |

Each object:

| Field | Meaning |
| --- | --- |
| `class_id`, `class_name` | COCO class: `0 person`, `24 backpack`, `63 laptop` |
| `box_source` | `observed` (the detector saw it in this frame) or `predicted` (tracker estimate for a lost track) |
| `bbox_observed` | Detector box, `[x1, y1, x2, y2]` float pixels, origin top-left. `null` for predictions. |
| `bbox_track` | Tracker's Kalman-filtered box (a prediction when `lost`). `null` for untracked detections. |
| `confidence` | Detector confidence. **Not a calibrated probability.** `null` for predictions. |
| `track_id` | Anonymous, run-scoped ID such as `person:0003`. Not an identity and not a registered asset ID. |
| `track_state` | `tracked` (detection matched to a track), `untracked` (detection with no track, e.g. low confidence), `lost` (track not seen this frame; predicted) |
| `zones` | IDs of every zone containing the box's membership anchor (zones may overlap) |

### Counting policy `contextguard.count_policy.v1`

- Counted: objects with `box_source == "observed"` and `confidence >= count_conf`,
  whatever their track state.
- **Never counted:** lost-track predictions.
- A counted box adds 1 to every zone that contains its anchor point.
- `visible_persons` is *what the camera sees now*. It is **not** room occupancy and
  **not** cumulative arrivals.

### Tracking

- One Ultralytics ByteTrack tracker per class (`configs/tracker/bytetrack.json`,
  Ultralytics 8.4.212 defaults), so a track can never change class.
- `track_buffer` is counted in **processed** frames: with stride N, a lost track
  survives `track_buffer × N` source frames.
- Brief occlusion appears as `lost`/`predicted` and then re-found under the same
  ID. Disappearance is never treated as departure.

## Zones (`contextguard.zones.v1`)

- Polygons are drawn on a frame from the real camera position, **one config per
  camera set-up**. `configs/zones/TEMPLATE_staged_office.json` is a placeholder
  marked `draft`, and every run that uses it carries a warning.
- Membership anchor: `bottom_center` (feet) for people, `center` for objects.
  Boundaries are inclusive; zones may overlap.
- Polygons are scaled from `reference_width`/`height` to the video size, with a
  warning if the aspect ratio differs.
- Kinds: `entry`, `asset_area`, `restricted`, `general`. Being in a `restricted`
  zone is an observation, **not** a violation.

## Verified so far (2026-11-13; synthetic only)

- 31 unit/integration tests pass:
  - CG-002 ×10;
  - zones ×8;
  - observation schema and counting ×5;
  - class-wise ByteTrack with the real Ultralytics tracker ×3;
  - pipeline with a scripted fake detector ×4;
  - real YOLO26n smoke test ×1 (skipped in CI, where weights are absent).
- End-to-end run with YOLO26n on a 90-frame synthetic clip (two people sliding,
  one hidden for 8 frames):
  - 172/172 expected person detections;
  - 2 track IDs;
  - the hidden person shown as `lost/predicted` and re-found under the same ID;
  - 90 records ↔ 90 annotated frames;
  - 14.7 frames/s overall on the CPU.

## Network and telemetry

Importing `contextguard` sets `YOLO_OFFLINE=1` before Ultralytics loads. This
stops Ultralytics' update checks, automatic package installs and usage events,
and prevents weight downloads. Weights must already be in `weights/`. Telemetry is
also disabled in Ultralytics' settings (`sync: false`).

## Limitations and open items

- No office footage, laptops or backpacks have been tested yet.
- Model choice, thresholds and zones are to be fixed on **tuning takes only**.
- H.264 output is unavailable without an external FFmpeg. `mp4v` plays in VLC and
  most desktop players; check playback on the presentation laptop.
- Processing is slower than real time on large models (small models ~8–9 fps
  detection on this CPU). Recorded video only.
- The accuracy evaluation (matching rules, metrics, sample) is not yet written; it
  must be fixed before evaluation takes are scored.
