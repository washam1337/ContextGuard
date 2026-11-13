# Staged office recording protocol (FYP-1)

Status: **DRAFT, PLANNED**. No recordings exist yet. This protocol governs the
team-recorded, consented, staged footage used for the 2026-11-24 FYP-1
presentation (D20, D21). Synthetic test fixtures are not part of this dataset.

## 1. Before recording

- Every volunteer reads and signs the [consent form](CONSENT_FORM_TEMPLATE.md)
  **before** any camera is switched on. Keep signed forms on paper or in private
  storage, never in this repository.
- Give each volunteer an anonymous code (`V1`, `V2`, `V3`, …). Use codes, never
  names, in file names, logs and labels.
- The office occupant is **not** in the footage (all people are visitors, D02).
- Remove or cover anything private in view: screens, documents, notice boards,
  name plates.

## 2. Camera set-up (keep identical for every take)

| Setting | Value |
| --- | --- |
| Device | One phone or webcam. Write the model in the session log. |
| Mounting | Fixed: tripod or stable shelf, high in a corner, angled down |
| Field of view | Must include the **doorway** and the **desk**, with the laptop and backpack at their registered starting positions |
| Orientation | Landscape |
| Resolution / rate | 1920×1080 or 1280×720, 30 fps (constant frame rate if the app allows it) |
| Format | MP4 (H.264) |
| Focus / exposure | Locked (tap-and-hold on phones). No zoom. No filters, HDR or stabilisation. |
| Lighting | Even room light; avoid strong backlight from windows |
| Audio | Not needed; mute or ignore (audio is DEFERRED) |

Do **not** move the camera between takes. If it moves, start a new session ID.

Before the main session, record one 30–60 s **test clip** and run the inspector
(section 5) to check placement.

## 3. Shot list

Each clip is 30–90 s. Start and end each clip with **3 s of the room as it is**.
Record **2–3 takes** of each scenario with different volunteers.

| Code | Scenario | Script | What it tests |
| --- | --- | --- | --- |
| SC01 | Empty room | 30 s, nobody, laptop and backpack in place | No false detections |
| SC02 | One visitor | V enters, sits ~20 s, leaves | Person detection and tracking |
| SC03 | Two visitors at once | V1 enters; V2 enters; both stay ≥20 s; both leave | Simultaneous count (relates to SYS-02) |
| SC04 | Brief second visitor | V1 inside; V2 enters, leaves within ~3 s | Brief exceedance (relates to SYS-07) |
| SC05 | Laptop carried out | V walks to desk, picks up laptop, leaves with it | Carried object (relates to SYS-03/04) |
| SC06 | Laptop occluded | V stands between camera and laptop ~5 s, moves away | Occlusion is not departure (relates to SYS-05) |
| SC07 | Backpack carried out | V picks up backpack, leaves with it | Second asset |
| SC08 | Laptop moved and returned | V moves laptop across desk, puts it back | Moved, not removed |

The relations to SYS cases are for planning only. SYS-01–08 stay PLANNED / NOT RUN
until the later reasoning stage exists.

## 4. Files, naming and storage

- Store footage **outside this repository**, e.g. `~/contextguard-data/raw/`. It
  must never be committed; this repository is public.
- Name each file `cg_<YYYYMMDD>_<session>_<scenario>_t<take>.mp4`,
  e.g. `cg_20261116_S01_SC03_t2.mp4`. A session (`S01`, `S02`…) is one continuous
  camera set-up.
- **Never edit, trim or re-encode the originals.** Processing writes to new folders.
- Fill in the session log below for every session.

## 5. Placement check (CG-002 inspector)

```bash
/home/w4shm1337/miniconda3/envs/fyp/bin/python -B scripts/inspect_video.py \
  --input ~/contextguard-data/raw/cg_20261116_S01_SC02_t1.mp4 \
  --output ~/contextguard-data/inspection/cg_20261116_S01_SC02_t1
```

Check the three exported frames: are the doorway, laptop and backpack visible and
large enough? Also watch the clip, because three frames cannot show everything.

## 6. Tuning versus evaluation split

Decide the split **before** looking at model results:

- **Tuning set:** take 1 of every scenario. Used to choose the model size, thresholds and zones.
- **Evaluation set:** takes 2–3. Used once for the reported results, and never for tuning.

Report the split, and every evaluation clip, including the failures.

## 7. Session log (copy for each session)

```text
Session ID:            S01
Date / time:
Location:              staged office room (no private details)
Camera device / app:
Resolution / fps:
Camera position notes: (photo of the set-up stored privately)
Laptop position:       (desk, left/right…)
Backpack position:
Lighting:
Volunteers present:    V1, V2, …   (consent forms signed: yes/no)
Clips recorded:        file name | scenario | take | notes
Problems:
```
