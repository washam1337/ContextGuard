# Pretrained models and dependencies

Status: **candidates downloaded; no model selected yet** (D22). Selection is made by
a measured benchmark on the team's own consented footage, using the tuning takes
only, i.e. session S01 (see [dataset/RECORDING_PROTOCOL.md](dataset/RECORDING_PROTOCOL.md) § 6).
No accuracy on office footage has been measured yet.

## Software installed for the perception pipeline (2026-11-13, D23)

Installed into the `fyp` environment with pip. A dry run first confirmed that only
new packages would be added, and `pip check` was clean afterwards. Pinned in
`requirements.txt`.

| Package | Version | Licence (from package metadata) | Role |
| --- | --- | --- | --- |
| ultralytics | 8.4.212 | AGPL-3.0 | Detector and tracker framework (YOLO, ByteTrack/BoT-SORT) |
| torch | 2.14.1+cpu | Apache-2.0 (as declared) | CPU inference backend |
| torchvision | 0.29.2+cpu | BSD | Image ops used by Ultralytics |
| lap | 0.5.14 | BSD-2-Clause | Linear assignment for the tracker |
| ultralytics-thop | 2.2.5 | AGPL-3.0 | Ultralytics dependency |
| polars, networkx, fsspec, filelock, nvidia-ml-py | as pip resolved | various | Transitive dependencies |

Ultralytics telemetry is disabled (`sync: false` in `~/.config/Ultralytics/settings.json`).
GPU: none. All inference runs on the CPU.

**Licence note.** Ultralytics is AGPL-3.0, and the owner accepts this (D22). The
repository is licensed under AGPL-3.0 (D25, [LICENSE](../LICENSE)). The licence
text was copied from the Ultralytics 8.4.212 distribution (SHA-256 `0d96a4ff…abcb0`).

## Candidate weights

All are COCO-pretrained detection models, downloaded on 2026-11-13 into `weights/`
(git-ignored; never committed). Relevant classes in their COCO-80 class map:
`0 person`, `24 backpack`, `63 laptop`.

| File | Source | Size (bytes) | SHA-256 |
| --- | --- | --- | --- |
| `yolo26n.pt` | `github.com/ultralytics/assets/releases/download/v8.4.0/yolo26n.pt` | 5,544,453 | `9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef` |
| `yolo26s.pt` | `…/v8.4.0/yolo26s.pt` | 20,422,725 | `646f8bc3fe0a656803d95c294f7852321748cb29d13466a1af8862e2db384a1b` |
| `yolo11n.pt` | `…/v8.4.0/yolo11n.pt` | 5,613,764 | `0ebbc80d4a7680d14987a577cd21342b65ecfd94632bd9a8da63ae6417644ee1` |
| `yolo11s.pt` | `…/v8.4.0/yolo11s.pt` | 19,313,732 | `85a76fe86dd8afe384648546b56a7a78580c7cb7b404fc595f97969322d502d5` |

To verify a download: `sha256sum weights/*.pt`.

## Preliminary CPU smoke test (not a benchmark)

Ultralytics' bundled sample image `bus.jpg` (810×1080), `imgsz=640`, 4 threads,
i5-1135G7, median of 10 runs after 3 warm-up runs. Models were measured in the
order listed.

| Model | ms/frame | Persons found (image contains 4) |
| --- | --- | --- |
| yolo26n | 132 | 4 |
| yolo26s | 92 | 4 |
| yolo11n | 43 | 4 |
| yolo11s | 95 | 4 |

**These numbers are not reliable.** It is one image, not office footage. Run-order and
warm-up effects are likely; for example, a nano model measuring slower than its small
version is implausible. The real benchmark will use the team's footage, randomised
order and more frames, and will report throughput and per-class detection outcomes.

## Synthetic-clip benchmark (software check, not accuracy)

`scripts/benchmark_models.py` on a **synthetic software fixture**: Ultralytics'
bundled `zidane.jpg` (2 people) shifted across 90 frames at 1280×720, with one person
hidden for 8 frames. Settings: imgsz 640, conf 0.25, 4 threads, 10 warm-up frames
excluded, 80 frames measured, random model order (seed 7: 11s, 26s, 26n, 11n). Run
2026-11-13. The true mean over the measured frames is 1.900 people per frame.

| Model | Median ms/frame | p90 ms | ~Detection fps | People per frame |
| --- | --- | --- | --- | --- |
| yolo26n | 45.6 | 50.9 | 21.9 | 1.900 |
| yolo11n | 45.6 | 54.8 | 21.9 | 2.038 |
| yolo26s | 116.1 | 126.1 | 8.6 | 1.900 |
| yolo11s | 117.5 | 128.3 | 8.5 | 1.925 |

With order randomised and warm-up excluded, nano models run about 2.5× faster than
small ones; the one-image smoke test above was distorted by warm-up. The full
pipeline (detector, class-wise tracker, annotation and video writing) with yolo26n
processed the same 90 frames at 14.7 frames/s overall.

**This is a software check on one synthetic clip, not an accuracy result.** It
contains no office footage, no laptops and no backpacks. Model choice will be made
on the team's tuning takes.

## NMS and `--iou` (checked 2026-11-15, Ultralytics 8.4.212)

YOLO26 has an optional NMS-free (one-to-one) head, but in 8.4.212 a `.pt` model run
with the default `nms=None`, as this pipeline does, uses the **one-to-many head
followed by standard NMS** (`end2end` is `False` for both yolo26n and yolo11n). So
`--iou` applies equally to the YOLO26 and YOLO11 candidates, and the benchmark
compares them under the same post-processing. Measured on `bus.jpg`, conf 0.10: both
models give 6 boxes at iou 0.1 and 9 at iou 0.9. Passing `nms=False` would switch
YOLO26 to its NMS-free head (7 boxes in the same test); the pipeline does not do
this. If that mode is ever used, the manifest's `iou` value would no longer apply
to YOLO26 and must be recorded as such.

## Known limitations to evaluate

- Backpacks are a small, often-occluded COCO class; expect lower recall than for people.
- Closed or partly hidden laptops may be missed.
- A high, downward camera angle differs from most COCO training images.
- Detector confidence is not a calibrated probability.
- CPU processing is expected to be slower than real time; recorded video only.
