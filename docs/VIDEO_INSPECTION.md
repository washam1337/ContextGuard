# Recorded-video inspection

The CG-002 utility prepares a local recording for manual placement review. It
performs two sequential decode passes: one to count decoded frames and inspect
dimensions, then one to export first/middle/last samples. The entire recording is
never retained in memory. No audio is processed.

## Running the tool

After following the [setup instructions](../README.md#quick-start):

```bash
python scripts/inspect_video.py --input /path/to/pilot.mp4 --output outputs/pilot-review-001
```

The input must be a readable, nonempty local file. Use a finished recording that
will not change during inspection. The output directory must not exist; choose a
new name for every run. Existing files are not overwritten or automatically removed.

| Exit code | Meaning |
| --- | --- |
| `0` | Inspection and export completed; review all warnings |
| `1` | Input, decoding, or output failure |
| `2` | Invalid or missing CLI arguments |

A failed export can leave partial output. Keep it for diagnosis and use a new
directory for the next attempt.

## Report fields

`inspection.json` uses schema `contextguard.video_inspection.v1`.

| Field | Contents |
| --- | --- |
| `source` | Absolute input path and source file size in bytes |
| `decoder` | OpenCV runtime version and video backend |
| `reported` | Container/backend frame count, FPS, dimensions, and derived duration |
| `decoded` | Sequentially decoded frame count, dimension counts, and stop reason |
| `timing` | Frame-index convention and explicit timestamp limitations |
| `sample_selection` | Description of the representative-frame selection policy |
| `representative_frames` | JPEG paths, zero-based decoded indices, optional estimated seconds |
| `warnings` | Metadata problems, mismatches, and decode limitations |

Invalid numeric metadata becomes JSON `null` with a warning. Reported duration is
`reported_frame_count / reported_fps`; it is not independently measured. Optional
sample times use `decoded_frame_index / reported_fps` and assume constant frame rate.

## Interpreting results

OpenCV cannot reliably distinguish clean end-of-file from a failed read. A report
can describe only a readable prefix, and successful completion does not certify
that the whole source is uncorrupted. Precise timing, variable-frame-rate accuracy,
and complete corruption detection are not claimed.

Review exported frames for doorway coverage, laptop/backpack starting positions,
asset visibility, lighting, occlusion, and legible object size. Watch the source as
well: three samples cannot establish quality throughout the recording. The images
are placement-review artifacts, not anomaly evidence clips.

## Troubleshooting

| Message or symptom | Action |
| --- | --- |
| Output path already exists | Choose a new output directory |
| No such file / input is empty | Check the input path and recording size |
| Cannot open video / no frames decoded | Check recording integrity and codec support |
| Second decode pass ended early | Ensure the input is stable; inspect the source and retry into a new directory |
| Metadata/count mismatch | Review the source and decoded observations; do not assume metadata is correct |

## Existing development workstation

The original verified environment uses Python 3.10.21 at
`/home/w4shm1337/miniconda3/envs/fyp/bin/python`, with OpenCV already installed.
Contributors should use their own isolated environment; this path is local to the
original workstation. Do not modify Conda base to run the project.

```bash
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B -m unittest discover -s tests -v
```
