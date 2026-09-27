# ContextGuard — MASTER_PLAN.md

> **Authoritative project specification for repository development**
>
> Source: *ContextGuard — Master FYP Project Handoff for Claude*.
> This repository version preserves the full project specification while adapting the AI-collaboration instructions for ChatGPT/Codex and other coding agents.

---

## Repository AI Operating Contract

This file is the **single source of truth for project scope and architectural intent** unless a newer, explicitly approved project decision is recorded in the repository.

Any AI coding agent working on ContextGuard must follow these rules:

1. **Read this entire file before making architectural or implementation changes.**
2. Inspect the current repository before writing code. Never assume a planned component already exists.
3. Keep **expected-vs-observed contextual reasoning** as the central research contribution.
4. Do not reduce ContextGuard to generic CCTV, generic theft detection, or generic object detection.
5. Keep **observation, inference, explanation, and human feedback separate** in code and data structures.
6. Never infer criminal intent. User-facing language must use cautious terms such as **potential anomaly**, **unexpected event**, or **requires review**.
7. Preserve the **structured event schema** as the stable contract between CV, temporal reasoning, anomaly reasoning, storage, dashboard, accessibility, and evaluation.
8. Build modular components with explicit interfaces. Avoid giant monolithic scripts.
9. Prefer the **simplest reliable, measurable implementation** over unnecessary model complexity.
10. Development must support **CPU-only execution for core development/testing**; GPU acceleration may be optional for later training/inference benchmarks.
11. Start with reproducible recorded-video processing before depending on live-camera behavior.
12. Use existing pretrained detection/tracking models where appropriate rather than training foundational perception models from scratch.
13. Freeze or version important schemas/configurations instead of silently changing them.
14. Add tests for event construction, context comparison, anomaly rules, API/data validation, and other deterministic logic.
15. Never invent experimental results, metrics, completed features, datasets, or model performance.
16. Keep training/validation/test data separated by session/actor/scene where possible to prevent leakage.
17. Track model versions, experiment configurations, thresholds, dataset revisions, and evaluation outputs.
18. Any learned temporal/anomaly component must be compared against simpler baselines.
19. Favor **false-positive reduction, explainability, evidence quality, and reproducibility**, not raw alert count.
20. Treat accessibility as a first-class system requirement, not a cosmetic UI feature.
21. Treat privacy, consent, retention, and access control as first-class design requirements.
22. Do not add face recognition unless a future approved project decision explicitly requires it.
23. Do not let an LLM invent sensor events or become the sole source of security decisions.
24. Human feedback must be stored separately from model predictions and used through controlled offline evaluation/retraining.
25. When debugging, trace the pipeline from **raw observation → track/state → structured event → context → temporal sequence → anomaly decision → evidence/explanation** before rewriting components.
26. Protect the MVP under scope pressure; postpone stretch features.
27. Documentation must describe the **implemented system**, clearly distinguishing implemented, experimental, planned, and deferred features.
28. For novelty or literature claims, verify against current research rather than making unsupported “first” claims.
29. Every alert must be traceable to structured evidence and relevant timestamps.
30. Update project progress/documentation whenever a milestone materially changes.

### Required development order

Unless evidence from implementation forces a justified change, development should proceed in this order:

`video playback → person detection/tracking → selected object detection/tracking → zones → interaction/object state → event logging → context engine → rule baseline → temporal reasoning → evidence extraction → dashboard/API → accessibility/TTS → optional audio/NLP → human feedback → learned improvement → ablation/evaluation`

### First runnable vertical slice

Before building the entire platform, the repository should support one deterministic end-to-end path:

`recorded video → detections → tracking → zones/object state → structured events → expected-context comparison → anomaly/normal decision → JSON/event storage → evidence window`

This vertical slice is the foundation for later ML, dashboard, accessibility, and multimodal additions.

---

## Status convention

Use these labels in repository documentation and issues:

- **IMPLEMENTED** — working code exists and has been run.
- **PARTIAL** — code exists but is incomplete, unstable, or unvalidated.
- **PLANNED** — specified but not implemented.
- **DEFERRED** — intentionally postponed.
- **EXPERIMENTAL** — prototype/research path not yet accepted into the core pipeline.

Never describe a **PLANNED** feature as implemented.

---

# Full Project Specification



| Item | Value |
| --- | --- |
| Project Type | Final Year Project (FYP) - Artificial Intelligence |
| Student | Washam Abbasi |
| Roll Number | 22P-9284 |
| Institution | FAST NUCES |
| Primary Domain | Computer Vision + Multimodal AI + Anomaly Detection + Assistive Technology |
| Product / System Name | ContextGuard |
| Target Environment | Controlled office / workplace workspace |
| Primary Users | Office administrators/security staff and visually impaired workspace users |
| Document Purpose | Provide Claude with a complete, consistent project specification for planning, research, coding, documentation and iteration |


# How This Document Should Be Used


This document is the authoritative working brief for the ContextGuard FYP concept finalized in the current project discussion. It is intended to be given to Claude or another AI collaborator as the main context before asking it to design architecture, perform literature review, plan implementation, generate code, write reports, design experiments, or review progress.

The project must be treated as an AI research-and-engineering FYP, not merely as a CCTV application. The central research and engineering idea is context-aware anomaly detection: the system represents what is expected to happen in a workspace, observes what actually happens through multimodal sensing, compares the two over time, and produces explainable, evidence-backed potential-anomaly alerts that remain subject to human verification.


Important: future work may refine implementation details, model choices, datasets, UI and evaluation methods. Such refinements must preserve the core problem definition and must not silently turn the project into a generic surveillance system.


# 0. Executive Project Definition


ContextGuard is a software-based intelligent workplace monitoring and accessibility system. It observes a controlled office environment using camera input and optional audio. It detects and tracks people, relevant office assets, locations, movements and interactions; converts observations into structured temporal events; maintains expected contextual information such as expected visitors, authorized tasks, expected objects and workspace rules; and identifies meaningful deviations between expected and observed activity.

When a potential anomaly is found, ContextGuard should not accuse a person of theft or infer criminal intent. Instead, it generates an evidence-backed alert explaining what was expected, what was observed, why the event was considered unusual, when it occurred, who/what was involved, and which short video segment should be reviewed.

The same event intelligence is exposed through an accessibility layer. A visually impaired user can receive important event notifications using text-to-speech and can query the event history with natural language, such as asking what happened while they were away. Human feedback is captured for alert correction and can later support controlled model improvement.


Core principle:


```text
EXPECTED CONTEXT
      +
MULTIMODAL OBSERVATIONS
      +
TEMPORAL EVENT REASONING
      ↓
COMPARE EXPECTED VS OBSERVED
      ↓
POTENTIAL ANOMALY
      ↓
EXPLANATION + RELEVANT EVIDENCE
      ↓
HUMAN VERIFICATION
      ↓
VALIDATED FEEDBACK FOR FUTURE IMPROVEMENT
```


# 1. Vision, Motivation and Problem


## 1.1 Motivation


Traditional CCTV systems are primarily recorders or rule-based alert systems. They can be useful for security but often create a large amount of footage that humans must monitor or search manually. A basic computer-vision system can detect a person, an object, an entry event or an object leaving an area, but an isolated visual event can be ambiguous. A person picking up a remote may be legitimately moving it or may be removing it without authorization.

At the same time, visually impaired employees cannot directly inspect camera footage to understand what is happening in their workspace. An assistive system can help by converting relevant visual events into accessible descriptions and by maintaining a searchable event history.

The FYP addresses both limitations through contextual reasoning. Instead of asking only “What is visible?”, ContextGuard asks “What is visible, what was expected, what happened before and after, and does the observed activity deviate from the defined context?”


## 1.2 Problem Statement


Office environments contain many legitimate activities that can look unusual when viewed without context. Existing security analytics may detect object removal, unauthorized access or people entering a room, but these detections do not necessarily know whether the action was expected. Accessibility tools can describe visual scenes, but they are not specifically designed to reason about workplace expectations, tasks and security-related deviations.

There is therefore an opportunity to build a domain-specific system that combines computer vision, temporal reasoning, optional speech/NLP context, workplace expectations, explainable event evidence and human feedback in one workflow. The project aims to determine whether this additional context can improve detection reliability and usefulness compared with visual-only monitoring.


## 1.3 Primary Research Question


Can contextual and temporal multimodal information improve the accuracy, reliability and explainability of workplace anomaly detection compared with visual-only detection?


## 1.4 Secondary Research Questions

- How much does temporal reasoning reduce false positives compared with frame-level event detection?

- How useful is explicit expected-context information for distinguishing authorized actions from potential anomalies?

- Can spoken instructions be converted into structured expected tasks that meaningfully improve visual anomaly interpretation?

- Can evidence-based explanations help a human reviewer validate or reject alerts more efficiently?

- Can validated human feedback be used as a controlled pathway for future model improvement?

- Can the same event representation provide useful audio-based accessibility support for visually impaired users?


# 2. Final Scope


## 2.1 In Scope

- Controlled office/workspace environment.

- Camera-based person and selected asset detection and tracking.

- Predefined office zones such as desk area, entrance, cabinet area and exit.

- Tracking of selected monitored assets, such as keys, remote controls, laptop, phone, documents or other agreed demonstrator objects.

- Expected visitor definitions and participant-count expectations.

- Expected task definitions such as retrieving keys.

- Temporal event construction from frame-level detections.

- Detection of predefined anomalous or unexpected event classes.

- Relevant evidence clip extraction around a detected event.

- Explainable alert generation.

- Optional audio capture, speech-to-text and NLP extraction of task/context information.

- Accessible text-to-speech notifications and natural-language event queries.

- Human review and feedback labels.

- A custom controlled office activity/anomaly dataset.

- Quantitative comparison of visual-only and context-aware approaches.


## 2.2 Explicitly Out of Scope / Non-Goals

- Determining a person's criminal intent from video.

- Automatically declaring that someone is a thief or criminal.

- Autonomous disciplinary, legal or employment decisions.

- Universal recognition of every possible human behavior.

- Monitoring unrestricted public areas.

- Uncontrolled self-training directly from every user click.

- Guaranteeing perfect anomaly detection.

- Building a new foundation model from scratch.

- Making identity/face recognition a mandatory dependency.

- Collecting unnecessary biometric or private data.


# 3. Core Product Behavior


## 3.1 Expected Context


The system maintains an explicit representation of what is expected to happen. Example fields include:


| Context Field | Example | Why It Matters |
| --- | --- | --- |
| Expected person | Ahmed | Distinguishes scheduled/authorized visitors from unexpected people. |
| Expected visitor count | 1 | Detects count mismatches. |
| Expected time | 3:00 PM | Allows time-window validation. |
| Expected task | Meeting | Provides activity context. |
| Authorized task | Retrieve office keys | Distinguishes expected object movement. |
| Expected object(s) | Keys | Defines what may legitimately move. |
| Restricted zone | Storage cabinet | Provides location-based access rules. |
| Monitored asset | Office remote | Enables asset-state tracking. |
| Expected destination | Outside office with keys | Supports task-consistency checks. |


## 3.2 Observed Context


The perception pipeline produces structured observations:


```text
person_id = P02
object_id = O07
object_type = office_remote
zone = desk
action = pickup
timestamp = 15:04:18
confidence = 0.91
tracking_state = active
```


## 3.3 Expected-vs-Observed Reasoning


The anomaly engine should compare the current workspace state and event sequence against the defined expectation. This may use a hybrid of deterministic constraints/rules and learned models. Deterministic logic is useful for explainability; learned temporal models may improve generalization to less rigid patterns.

The system should retain the distinction between observation and inference. For example, “remote moved from desk zone to exit zone” is an observation derived from perception. “Potential unauthorized removal” is a contextual inference based on the expectation that no remote movement was authorized.


```text
EXPECTED:
- Visitor count = 1
- Visitor = Ahmed
- Task = retrieve keys
- Expected removed object = keys

OBSERVED:
- Visitor count = 2
- Second visitor not expected
- Keys removed
- Remote removed
- Remote leaves office

INFERENCE:
Potential anomaly: remote movement inconsistent with expected task.
```


# 4. Representative End-to-End Scenarios


## 4.1 Scenario A - Unexpected Additional Visitor


```text
Context:
Expected visitor: Ahmed
Expected count: 1
Scheduled time: 3:00 PM

Observed:
15:01 - Ahmed enters
15:01 - Person P02 enters
15:02 - Both remain in office

System result:
Potential anomaly: visitor-count mismatch.
Expected 1, observed 2.
Evidence: short clip covering entry sequence.
```


Accessibility output: “Alert. Two people entered your office at approximately 3:01 PM. One visitor was expected; the additional visitor was not expected.”


## 4.2 Scenario B - Scheduled Meeting with No Security Anomaly


```text
Expected:
Ahmed, 1 visitor, meeting, no asset movement.

Observed:
Ahmed enters.
Meeting occurs.
No monitored asset leaves.
Ahmed exits.

Result:
Normal meeting.
No anomaly alert.
Event remains in history for later queries.
```


## 4.3 Scenario C - Authorized Key Retrieval


```text
Spoken instruction:
“Ali, please go to my office and bring the keys.”

Extracted context:
Person = Ali
Task = retrieve
Expected object = keys
Expected location = office

Observed:
Ali enters.
Ali picks up keys.
Ali leaves with keys.

Result:
Expected action.
No anomaly.
```


## 4.4 Scenario D - Expected Keys + Unexpected Remote Removal


```text
Spoken instruction:
“Ali, please go to my office and bring the keys.”

Expected:
- Ali may enter office.
- Ali may retrieve keys.
- Remote should remain.

Observed:
- Ali enters office.
- Ali retrieves keys.
- Ali retrieves remote.
- Remote leaves monitored workspace.

Result:
Potential unauthorized asset removal.
Do NOT label Ali as a thief.
Generate explanation + evidence clip.
```


## 4.5 Scenario E - Object Moved but Returned


```text
Observed:
Person picks up remote.
Person uses it.
Person puts remote back on desk.

Result:
Context-dependent.
If the person's action is authorized or normal, label Normal/Authorized.
If not, it may still be logged as an interaction but should not automatically become a security anomaly.

Purpose:
Stress-test false-positive behavior.
```


## 4.6 Scenario F - Restricted Zone Entry


```text
Expected:
Visitor is limited to meeting area.

Observed:
Visitor enters restricted storage area.

Result:
Potential policy violation:
“Visitor entered a restricted workspace zone.”
Relevant clip should show entry and duration.
```


# 5. Event Taxonomy


| Event Class | Definition | Example | Default Severity |
| --- | --- | --- | --- |
| Normal activity | Observed action fits expectation. | Scheduled visitor has a meeting. | Low |
| Expected object retrieval | Authorized task and expected object. | Retrieve keys. | Low |
| Unexpected visitor | Person enters without being expected. | Unscheduled visitor. | Medium |
| Visitor-count mismatch | Observed count exceeds expectation. | 2 visitors expected 1. | Medium |
| Restricted-area entry | Person enters a configured restricted zone. | Visitor enters storage. | Medium |
| Unexpected object interaction | Person interacts with monitored asset without matching context. | Visitor picks up remote. | Medium |
| Object removal | Monitored object changes state/location and exits a zone. | Remote removed. | High |
| Expected-task violation | Observed task outcome contains unexpected object/action. | Keys + remote taken. | High |
| Suspicious temporal sequence | Sequence of otherwise weak signals collectively deviates from context. | Desk interaction → object removal → exit. | High |
| False alarm / corrected event | Human review indicates alert was incorrect. | Object moved by authorized staff. | Feedback label |


# 6. System Architecture


```text
CONTEXTGUARD SYSTEM

      ┌────────────────── OFFICE ENVIRONMENT ──────────────────┐
      │                                                         │
      │   Camera(s)                      Microphone (optional)  │
      └───────────────┬─────────────────────────┬───────────────┘
                      │                         │
                      ▼                         ▼
             ┌─────────────────┐       ┌─────────────────┐
             │ CV PERCEPTION   │       │ AUDIO/NLP       │
             │ person/object   │       │ speech-to-text  │
             │ detection       │       │ instruction     │
             │ tracking        │       │ extraction      │
             │ zones           │       │ diarization*    │
             └────────┬────────┘       └────────┬────────┘
                      │                         │
                      └────────────┬────────────┘
                                   ▼
                        ┌────────────────────┐
                        │ EVENT REPRESENTATION│
                        │ who/what/where/when │
                        │ action/state        │
                        └──────────┬─────────┘
                                   │
                     ┌─────────────┴──────────────┐
                     ▼                            ▼
          ┌─────────────────────┐      ┌────────────────────┐
          │ EXPECTATION ENGINE  │      │ TEMPORAL ENGINE    │
          │ visitors            │      │ sequences           │
          │ tasks               │      │ before/during/after │
          │ assets              │      │ persistence         │
          │ permissions         │      │ state transitions   │
          └──────────┬──────────┘      └──────────┬─────────┘
                     └──────────────┬────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ ANOMALY REASONING    │
                         │ rules + learned      │
                         │ contextual scoring   │
                         └──────────┬───────────┘
                                    │
                              ┌─────┴─────┐
                              ▼           ▼
                           NORMAL     ANOMALY
                                          │
                                          ▼
                              ┌────────────────────┐
                              │ EVIDENCE GENERATOR │
                              │ explanation        │
                              │ timestamp          │
                              │ confidence         │
                              │ relevant clip     │
                              └─────────┬──────────┘
                                        │
                         ┌──────────────┴─────────────┐
                         ▼                            ▼
                 SECURITY DASHBOARD          ACCESSIBILITY LAYER
                 live events                 TTS alerts
                 timeline                    natural-language query
                 incident review             event summaries
                 feedback                    accessible controls
                         │                            │
                         └──────────────┬─────────────┘
                                        ▼
                               HUMAN FEEDBACK STORE
                                        │
                                        ▼
                            VALIDATED TRAINING DATA
                                        │
                                        ▼
                              PERIODIC MODEL UPDATE
```


* Speaker diarization is optional and should be included only if technically justified by time/resources.


# 7. Module-by-Module Technical Specification


## 7.1 Module A - Video Ingestion


Responsibilities: acquire camera frames, timestamp them, maintain a stable processing rate, optionally buffer recent frames for evidence extraction, and handle camera disconnect/reconnect conditions.

Requirements:
- Support one camera for the core prototype; multiple cameras are optional.
- Timestamp frames consistently.
- Keep a rolling evidence buffer so the system can save several seconds before and after an event.
- Avoid storing all footage indefinitely.
- Allow recorded video files to be replayed for deterministic testing.


## 7.2 Module B - Person Detection and Tracking


Use a modern object detector and tracker rather than training a person detector from scratch. Each visible person should receive a temporary tracking identity such as P01, P02, etc. The identity is a session-level tracking ID and does not inherently represent a real-world person's name.

Outputs:
person_id, bounding_box, confidence, timestamp, zone, track_state, optional appearance embedding if later justified.

Core requirement: stable track continuity should be good enough to connect entry, desk interaction and exit events.


## 7.3 Module C - Asset/Object Detection


The project should begin with a small controlled object vocabulary rather than attempting every possible office object. Candidate objects: keys, remote control, laptop, phone, documents, bag or a custom FYP asset.

Each monitored object should have a state:
- present at zone
- being interacted with
- moved
- carried
- outside zone
- returned

Object identification can be class-based in the demonstrator or use assigned visual markers/known object appearance where necessary for reliable tracking. This should be documented transparently.


## 7.4 Module D - Workspace Zones


The scene should be partitioned into logical zones. Example:
- entrance
- meeting area
- desk
- storage/restricted area
- exit boundary

Zone transitions allow statements such as “remote moved from desk to outside the office.” The first implementation can use manually defined polygon zones rather than complex scene segmentation.


## 7.5 Module E - Person-Object Interaction


```text
This module infers interactions between tracked people and monitored assets. Interaction should use spatial overlap/proximity, relative motion, and persistence over time. A single-frame overlap should not automatically imply pickup.

A robust interaction event may require:
approach → proximity → hand/object relationship or object movement → continued tracking → state change.

The exact method can be simplified for the FYP if the chosen camera angle makes hand-level reasoning unreliable. The system must state the limitation rather than overclaim precision.
```


## 7.6 Module F - Event Representation


All perception outputs should be converted to a common event schema so the anomaly engine does not depend on raw model-specific outputs.


```text
Event {
    event_id
    session_id
    timestamp_start
    timestamp_end
    event_type
    person_ids[]
    object_ids[]
    location
    source_modality[]
    confidence
    attributes{}
    evidence_start
    evidence_end
}
```


## 7.7 Module G - Expectation/Context Engine


Context may originate from a web dashboard, a simple configuration file/database, a scheduled calendar-like entry, or extracted speech. For the FYP, a controlled context-management screen is sufficient.

Example:


```text
Context {
    context_id
    valid_from
    valid_to
    expected_people[]
    expected_count
    expected_task
    allowed_zones[]
    expected_objects[]
    restricted_zones[]
    expected_outcomes[]
    notes
}
```


## 7.8 Module H - Speech-to-Text and NLP


```text
Audio is optional but valuable because it creates a genuine multimodal research component. Speech processing should extract only relevant contextual information rather than attempt broad “mind reading.”

Pipeline:
audio → speech-to-text → relevant statement detection → structured task extraction → context object.

Example:
“Please bring the office keys.”
becomes:
action=retrieve, object=keys, person=authorized_student (if known), location=office.

The system should handle uncertainty. If transcription or extraction confidence is low, it should not create a high-confidence authorization rule.
```


## 7.9 Module I - Temporal Reasoning


```text
Temporal reasoning is central to the project. A useful anomaly is often a sequence rather than a single frame.

Example:
person enters → desk interaction → object disappears → object is carried → exit.

Implementation options:
- deterministic event-sequence rules for the first baseline;
- sliding windows over event embeddings;
- temporal classifier;
- sequence model if dataset size supports it.

The FYP does not require a highly complex temporal neural network if an event-based approach is more reliable and explainable.
```


## 7.10 Module J - Anomaly Reasoning


The anomaly engine should produce:
1. anomaly category;
2. severity/priority;
3. confidence;
4. explanation;
5. contributing observations;
6. evidence time window.

A possible hybrid scoring framework:


AnomalyScore =
    w_context * ContextMismatch
  + w_sequence * TemporalPatternScore
  + w_object   * AssetMovementScore
  + w_access   * AccessViolationScore
  + w_audio    * AudioContextMismatch

Final decision =
    score + rule constraints + minimum evidence requirements


The exact formula is a design choice to be experimentally validated. Do not present arbitrary weights as scientifically optimal until measured.


## 7.11 Module K - Evidence Extraction


```text
Every alert should reference the minimum useful evidence interval. The system should retain a configurable pre-event and post-event buffer, for example:
- pre-event: 5–10 seconds
- post-event: 5–15 seconds

Exact values should be determined experimentally. The evidence clip should be tied to the event record and should not require a reviewer to inspect the entire meeting.
```


## 7.12 Module L - Explainability


```text
The system should explain the alert using structured facts instead of fabricated reasoning. An explanation template can include:

Expected:
Observed:
Deviation:
Entities:
Time:
Location:
Evidence:

Example:
“Expected one visitor for a meeting. Two people entered at 15:01. The second person was not in the expected visitor list. A remote was subsequently removed from the desk at 15:05.”

Do not produce unsupported claims such as “the person intended to steal the remote.”
```


## 7.13 Module M - Dashboard


Suggested pages:
- Overview/live monitoring
- Current people and object state
- Expected context
- Event timeline
- Incidents/anomalies
- Evidence review
- Feedback labeling
- Asset registry
- Workspace zones
- Settings/privacy
- Dataset/evaluation mode for FYP experiments


## 7.14 Module N - Accessibility Layer


```text
The accessibility layer should not be treated as a cosmetic add-on. It uses the same structured event representation as the security interface.

Features:
- text-to-speech for high-priority events;
- concise alert messages;
- event-history queries;
- chronological “what happened while I was away?” summaries;
- configurable verbosity;
- accessible keyboard navigation and screen-reader-compatible controls.

Example:
User: “What happened in my office from 3 to 4 PM?”
System: “At 3:01, Ahmed entered with one additional person. At 3:05, a remote was removed from the desk. At 3:08, both people left.”
```


## 7.15 Module O - Human Feedback


A reviewer can label an event:
- Normal
- False alarm
- Authorized action
- Confirmed potential anomaly
- Other / needs review

Store the model prediction and final label separately. Feedback should create a validated data pool. Periodic retraining is preferred to uncontrolled online model updates.


## 7.16 Module P - Storage and Data Model


| Entity | Important Fields | Purpose |
| --- | --- | --- |
| User | user_id, role, accessibility_preferences | System account/permissions. |
| Workspace | workspace_id, zones, rules | Environment definition. |
| Asset | asset_id, type, zone, monitored | Track important objects. |
| ExpectedContext | time, people, count, task, objects, zones | What is expected. |
| Session | session_id, camera, start/end | Group observation runs. |
| Track | track_id, person/object, timestamps, zones | Tracking history. |
| Event | event_id, type, timestamps, entities, confidence | Structured observation. |
| Incident | incident_id, event_id, severity, explanation, clip_path | User-facing potential anomaly. |
| Feedback | feedback_id, incident_id, label, reviewer, note | Human correction. |
| ModelRun | model_version, metrics, timestamp | Experiment/version tracking. |


# 8. Proposed Technology Stack


| Layer | Preferred Technology | Alternatives / Notes |
| --- | --- | --- |
| Programming | Python | Primary language for AI/backend. |
| Computer Vision | OpenCV | Video I/O, zones, frame processing. |
| Object Detection | YOLO-family model | Choose specific version after benchmarking. |
| Tracking | ByteTrack or BoT-SORT | Select based on implementation stability. |
| Deep Learning | PyTorch | Use for model integration/training. |
| Speech-to-Text | Whisper-family model | Optional multimodal component. |
| NLP | Transformers / local LLM / rules | Use structured extraction, not unsupported claims. |
| Backend | FastAPI | REST/WebSocket services. |
| Frontend | React or Streamlit | React for richer UI; Streamlit for fastest prototype. |
| Database | SQLite initially; PostgreSQL if needed | SQLite is sufficient for a controlled FYP prototype. |
| Storage | Local file storage | Object/clip paths in DB; configurable retention. |
| Text-to-Speech | OS/cloud/local TTS | Prefer a practical low-latency option. |
| Version Control | Git/GitHub | Track code, experiments and documentation. |
| Deployment | Local workstation | Cloud deployment is not required for the FYP. |


# 9. Dataset Strategy


## 9.1 Why a Custom Dataset Is Needed


Public anomaly datasets can be useful for benchmarking concepts, but the core FYP is specific to office context: expected visitors, task-based object movement, desk interactions, restricted zones and context mismatches. Therefore, a controlled custom dataset is strongly recommended.

The dataset should include both positive anomaly cases and normal cases that superficially resemble anomalies. The latter are essential for measuring false positives.


## 9.2 Initial Scenario Matrix


| ID | Scenario | Expected | Observed | Label |
| --- | --- | --- | --- | --- |
| S01 | Normal meeting | 1 scheduled visitor | Meeting only | Normal |
| S02 | Unexpected visitor | No extra visitor | Extra visitor enters | Anomaly |
| S03 | Count mismatch | 1 visitor | 2 visitors | Anomaly |
| S04 | Key retrieval | Keys only | Keys removed | Normal |
| S05 | Key + remote | Keys only | Keys + remote removed | Anomaly |
| S06 | Remote use and return | Normal office use | Remote picked/returned | Normal/Authorized |
| S07 | Restricted area | Visitor stays in meeting zone | Visitor enters storage | Anomaly |
| S08 | Authorized asset movement | Staff may move laptop | Laptop moved by staff | Normal |
| S09 | Unexpected laptop departure | No asset departure | Laptop exits | Anomaly |
| S10 | Object interaction without removal | Object stays | Person interacts | Normal/Review |


## 9.3 Annotation Schema


video_id
session_id
scenario_id
timestamp_start
timestamp_end
event_type
person_id(s)
object_id(s)
source = video/audio/both
expected_state
observed_state
label = normal/anomaly/false_alarm/authorized
notes


## 9.4 Data Split


Use train/validation/test splits that avoid leakage from identical sessions. Where possible, separate scenes or actors between training and testing so performance does not simply reflect memorization of the recording setup.


## 9.5 Data Privacy


Use staged participants, explicit consent and controlled recordings. Avoid unnecessary biometric identification. For demonstrations, anonymous track IDs are enough. Raw recordings should have configurable retention and access controls.


# 10. Research and Experimental Plan


## 10.1 Baselines


| System | Inputs | Purpose |
| --- | --- | --- |
| Baseline A | Visual frame/object events only | Measure conventional visual-only behavior. |
| Baseline B | Visual + temporal events | Measure value of sequence reasoning. |
| Model C | Visual + temporal + context | Primary ContextGuard reasoning configuration. |
| Model D | Visual + temporal + context + human feedback | Measure improvement after validated feedback. |


## 10.2 Metrics

- Precision: how many predicted anomaly events are actually anomalies.

- Recall: how many true anomaly events are detected.

- F1-score: balance of precision and recall.

- False-positive rate: critical for practical usability.

- Event localization accuracy: whether the system points to the correct temporal segment.

- Alert latency: time from event occurrence to alert generation.

- Explanation correctness: whether the generated explanation accurately reflects the structured evidence.

- Feedback correction rate: how often reviewers reject or correct alerts.

- Accessibility task success: whether a user can correctly answer event questions using the audio interface.


## 10.3 Ablation Study


A key research result should be an ablation study showing the incremental value of each information source. Report results for visual-only, visual+temporal, visual+context, and visual+temporal+context; audio can be compared separately if the multimodal component is implemented.


## 10.4 Expected Hypothesis


The working hypothesis is that adding temporal and context information will reduce false positives and improve event-level precision compared with visual-only detection, especially in situations where the same object movement can be either authorized or anomalous depending on the expected task.

This is a hypothesis to test, not a guaranteed result.


## 10.5 Error Analysis


For every important failure mode, categorize why it happened:
- missed detection;
- tracking identity switch;
- object occlusion;
- poor camera angle;
- incorrect zone assignment;
- speech transcription error;
- context configuration error;
- temporal reasoning failure;
- false anomaly due to ordinary activity.

Use this analysis in the final FYP report.


# 11. Explainability and Evidence Requirements


Every anomaly alert should be traceable to structured observations. The system should store contributing events so a reviewer can understand how the alert was formed.

Minimum incident record:


Incident:
ID
Category
Severity
Confidence
Timestamp
Expected context summary
Observed event summary
Mismatch explanation
People involved
Objects involved
Location/zone
Evidence clip
Underlying event IDs
Reviewer feedback
Model version


This design also makes the system easier to debug and scientifically evaluate.


# 12. Accessibility Requirements


| Requirement | Target Behavior |
| --- | --- |
| Audio alerts | Read important anomalies and critical state changes. |
| Concise language | Avoid overwhelming the user with every low-level detection. |
| Event history query | Answer time-bounded questions about workspace events. |
| Chronological summary | Summarize what happened while the user was away. |
| Priority levels | Differentiate informational, warning and high-priority events. |
| Repeat/recap | Allow the user to repeat the last alert. |
| Keyboard/screen-reader access | All critical dashboard actions must remain operable without a mouse where practical. |
| Uncertainty wording | Say “potential anomaly” or “detected” when certainty is limited. |


# 13. Privacy, Safety and Ethics


This project processes potentially sensitive workplace video and, optionally, audio. Privacy should therefore be a first-class design constraint.

Principles:
1. Data minimization - collect only what is required for the FYP.
2. Controlled consent - use staged participants and explicit permission.
3. Human verification - alerts support a person; they do not make disciplinary or legal decisions.
4. No intent inference - do not claim that visual evidence proves criminal intent.
5. Role-based access - only authorized users should access recordings/incidents.
6. Configurable retention - raw media should not be retained forever.
7. Auditability - keep model version and evidence references for incidents.
8. Anonymous IDs by default - real identity is not necessary for the core prototype.
9. Secure development - avoid hard-coded credentials and unsecured public camera endpoints.
10. Transparent limitations - clearly state what the prototype can and cannot infer.


# 14. Security of the System Itself

- Protect camera endpoints and credentials.

- Avoid exposing live camera streams without authentication.

- Sanitize file paths and user inputs.

- Use role-based permissions for evidence clips.

- Log incident review and feedback actions.

- Store model versions alongside predictions.

- Avoid arbitrary code execution through configurable rules.

- Back up only the data required for experiments.


# 15. Software Architecture and Repository Plan


```text
contextguard/
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── services/
│   ├── ui/
│   └── utils/
├── cv/
│   ├── detection/
│   ├── tracking/
│   ├── zones/
│   ├── interactions/
│   └── event_builder/
├── audio/
│   ├── asr/
│   ├── nlp/
│   └── context_extraction/
├── anomaly/
│   ├── rules/
│   ├── temporal/
│   ├── scoring/
│   └── explainability/
├── accessibility/
│   ├── tts/
│   └── query/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── annotations/
│   └── splits/
├── experiments/
│   ├── configs/
│   ├── runs/
│   └── reports/
├── tests/
├── docs/
├── scripts/
├── requirements.txt
└── README.md
```


This is a suggested structure, not a mandatory one. It exists to keep perception, reasoning, UI and experiments separated and maintainable.


# 16. API / Backend Concept


## 16.1 Suggested Endpoints


| Endpoint | Method | Purpose |
| --- | --- | --- |
| /contexts | GET/POST | Create and retrieve expected workspace contexts. |
| /assets | GET/POST/PATCH | Manage monitored assets. |
| /zones | GET/POST/PATCH | Manage workspace zones. |
| /sessions/start | POST | Start live or recorded analysis. |
| /sessions/stop | POST | Stop an analysis session. |
| /events | GET | Retrieve structured events. |
| /incidents | GET | Retrieve potential anomalies. |
| /incidents/{id} | GET | View incident details. |
| /incidents/{id}/feedback | POST | Submit reviewer classification. |
| /evidence/{id} | GET | Retrieve evidence clip/metadata. |
| /query | POST | Natural-language event query. |
| /status | GET | System health and model status. |


# 17. Example Natural-Language Queries

- Who entered my office today?

- Did anyone enter while I was away?

- How many people came to my meeting?

- Did anyone remove anything from my desk?

- What happened between 3 PM and 4 PM?

- Was anyone in the restricted area?

- What happened after Ali entered?

- Why was I given the last security alert?

- Which alerts were later marked as false alarms?


# 18. Dashboard / UX Concept


## 18.1 Overview


```text
OFFICE STATUS
People currently present: 2
Expected visitors: 1
Monitored assets present: 5
Open incidents: 1

RECENT EVENTS
15:01  Ahmed entered              NORMAL
15:01  Additional person entered  WARNING
15:05  Remote removed             HIGH
15:08  Visitors exited            NORMAL

[Review Incident] [View Timeline] [Ask Assistant]
```


## 18.2 Incident Review


```text
INCIDENT #104

Type: Potential unauthorized asset removal
Severity: High
Confidence: 0.89

Expected:
Keys may be retrieved.

Observed:
Keys removed + remote removed.

Why flagged:
Remote movement was not part of the configured task.

Evidence:
15:04:45 - 15:05:20

[Play Clip]
[Normal]
[Authorized]
[False Alarm]
[Potential Anomaly]
```


# 19. Human-in-the-Loop Learning Design


```text
Human feedback is a research feature, but it must be implemented carefully. A feedback button is not equivalent to an autonomous learning system. The safe FYP design is:

Detection → Review → Label → Validation → Feedback Dataset → Offline evaluation/retraining → New model version.

Every model version should be tracked. After retraining, compare the new model against a frozen test set. Do not claim improvement solely because training accuracy increased.
```


| Feedback Label | Meaning |
| --- | --- |
| Normal | The event was normal workplace activity. |
| False Alarm | The alert logic/detection was incorrect. |
| Authorized | The event was unusual but explicitly allowed. |
| Potential Anomaly | The reviewer agrees that further action/review is warranted. |
| Needs Review | Insufficient evidence for a confident label. |


# 20. Model Development Strategy


## 20.1 Do Not Start With a Giant End-to-End Model


The recommended development order is modular. First make perception reliable, then construct events, then add contextual rules, then add temporal learning, then add optional audio/NLP and accessibility. This makes the system testable and prevents the FYP from becoming an un-debuggable monolith.


## 20.2 Suggested Development Sequence

1. Video input and reproducible playback.

1. Person detection and tracking.

1. Selected object detection/tracking.

1. Zone assignment.

1. Basic interaction/object state changes.

1. Structured event logging.

1. Context management.

1. Simple rule-based anomaly baseline.

1. Temporal sequence reasoning.

1. Evidence extraction.

1. Dashboard.

1. Accessibility/TTS.

1. Speech/NLP context extraction.

1. Human feedback.

1. Controlled model improvement.

1. Ablation study and final evaluation.


# 21. FYP Milestone Plan


| Phase | Work | Exit Criteria |
| --- | --- | --- |
| 1 | Requirements + literature review | Final problem definition, event taxonomy, research questions, architecture draft. |
| 2 | Data/scenario design | Scenario matrix, annotation format, consent plan, initial recordings. |
| 3 | CV prototype | Person/object detection, tracking and zones working on staged data. |
| 4 | Event engine | Structured event logs and asset state changes. |
| 5 | Context engine | Expected visitors, expected tasks and rules configurable. |
| 6 | Baseline anomaly detection | Visual-only baseline with metrics. |
| 7 | Temporal reasoning | Sequence-level anomaly detection and comparison. |
| 8 | Evidence + dashboard | Incident review and clip generation. |
| 9 | Audio/NLP | At least one task/context scenario extracted from speech. |
| 10 | Accessibility | TTS alerts and event-history queries. |
| 11 | Human feedback | Feedback storage and validated labels. |
| 12 | Evaluation | Baselines, ablations, metrics, error analysis. |
| 13 | Finalization | Documentation, demo, presentation and reproducible setup. |


# 22. Risk Register


| Risk | Impact | Mitigation |
| --- | --- | --- |
| Object detection unreliable | High | Reduce object vocabulary, improve camera angle, add markers/custom training. |
| Tracking ID switches | High | Use stable camera, tracker tuning, event persistence requirements. |
| Occlusion | High | Controlled layout, zone-based rules, multiple views only if necessary. |
| Too many false alerts | High | Context + temporal constraints; tune thresholds using validation data. |
| Audio transcription errors | Medium | Treat speech as optional context with confidence; allow manual context entry. |
| Dataset too small | High | Create diverse staged scenarios and emphasize controlled evaluation. |
| Scope explosion | High | Freeze event taxonomy early and prioritize core scenarios. |
| Privacy concerns | High | Consent, anonymized IDs, local processing where possible, retention control. |
| Hardware limitations | Medium | Use lightweight models, recorded-video mode, batch evaluation. |
| Integration complexity | High | Modular services and structured event schema. |
| Novelty claim too broad | High | Position novelty around integration/context framework and validate through literature review. |


# 23. What Counts as a Successful FYP?


The FYP is successful if a controlled office demonstration can reliably show the following chain:

1. Define an expected context.
2. Observe a staged activity.
3. Detect and track relevant people/objects.
4. Build an event sequence.
5. Compare observed behavior with expected behavior.
6. Flag a potential anomaly when a meaningful mismatch occurs.
7. Produce a concise explanation and evidence clip.
8. Let a human approve/reject/correct the event.
9. Store that feedback.
10. Communicate important events through an accessible audio interface.
11. Quantitatively demonstrate whether context/temporal reasoning improves over a visual-only baseline.

The project does not need to solve unrestricted real-world surveillance to be a strong FYP. A carefully controlled, quantitatively evaluated prototype with a clear research question is preferable to an overly broad system that works unreliably.


# 24. Novelty Positioning - What to Claim and What Not to Claim


## 24.1 Do Not Claim

- The project is the first theft-detection AI.

- The project is the first AI vision assistant for blind people.

- No existing system can detect object removal.

- The project can know a person's true intent.

- The project replaces professional security staff.


## 24.2 Stronger, Defensible Contribution

- A domain-specific framework for expected-vs-observed workplace reasoning.

- Integration of computer vision events with temporal context and optional speech-derived task context.

- Evidence-backed anomaly alerts that explain the mismatch rather than making unsupported accusations.

- A shared event memory that supports both security review and accessibility queries.

- A human-in-the-loop feedback pathway tied to model evaluation/improvement.

- A custom controlled dataset focused on context-rich workplace anomalies.


The novelty statement must ultimately be supported by an up-to-date literature review before the final thesis is written. Similar components and related multimodal anomaly-detection research are expected to exist; the thesis should claim the specific system integration and evaluated approach, not an unsupported absolute “first.”


# 25. Literature Review Strategy


The literature review should be organized around gaps rather than a random list of papers. Search and compare work in:
- video anomaly detection;
- action recognition and temporal event detection;
- object tracking and object removal detection;
- workplace/security video analytics;
- multimodal video-language reasoning;
- speech-to-text for context extraction;
- assistive vision for blind/low-vision users;
- human-in-the-loop and active learning;
- explainable AI for surveillance/video analytics;
- privacy-preserving or responsible video analytics.

For every relevant paper, record:
problem, dataset, modalities, model, context use, temporal reasoning, explainability, feedback, metrics, limitations, and how ContextGuard differs or builds on it.


Claude should browse the web for current literature when performing this section because research status may change and novelty claims must be current.


# 26. Documentation Requirements

- README with setup, architecture and run instructions.

- System requirements and supported hardware.

- Dataset creation/annotation guide.

- Configuration guide for zones, assets and contexts.

- API documentation.

- Model cards / version notes for third-party models where appropriate.

- Experiment logs and reproducibility instructions.

- Evaluation report with baselines and ablations.

- Known limitations and ethical considerations.

- FYP thesis chapters aligned with actual implementation, not planned-only features.


# 27. Definition of Important Terms


| Term | Meaning in This Project |
| --- | --- |
| Context | Information describing what is expected or relevant for an activity. |
| Expectation | A configured statement about people, tasks, objects, timing, zones or outcomes. |
| Observation | A fact derived from sensor/model output, such as a person entering a zone. |
| Event | A structured time-bounded observation or interpreted action. |
| Anomaly | A detected deviation from expected context or configured normal behavior. |
| Potential anomaly | An anomaly requiring human verification; avoids claiming intent. |
| Evidence | A short relevant media segment and underlying structured events supporting an alert. |
| Temporal reasoning | Interpretation based on event sequence and time relationships. |
| Multimodal | Combination of more than one information modality, such as video and audio. |
| Human-in-the-loop | A design where human feedback is explicitly used in review or future model development. |
| Accessibility layer | Interface that communicates system information to a visually impaired user. |
| Asset | A monitored office object such as a remote, keys or laptop. |


# 28. Example Data Flow


```text
1. Camera receives frame.
2. Detector finds P01 and O03.
3. Tracker associates detections with persistent IDs.
4. Zone module assigns P01 = desk zone, O03 = desk zone.
5. Interaction module detects P01 interacting with O03.
6. Object state changes: O03 present → carried.
7. Event engine creates:
      PERSON_OBJECT_INTERACTION
      OBJECT_MOVED
8. Context engine says O03 is not part of expected task.
9. Temporal engine sees:
      enter → approach desk → pickup → carry → exit
10. Anomaly engine raises:
      POTENTIAL_UNAUTHORIZED_ASSET_REMOVAL
11. Evidence generator selects relevant 15–30 second window.
12. Dashboard shows incident.
13. TTS says concise alert.
14. Reviewer labels Authorized/False Alarm/Potential Anomaly.
15. Feedback is stored for analysis/retraining.
```


# 29. Example Pseudocode for Core Reasoning


```text
def process_observation(observation):
    update_tracks(observation)
    update_object_states(observation)

    events = build_events(observation)

    context = get_active_context(observation.timestamp)

    sequence = update_temporal_window(events)

    anomaly = anomaly_engine.evaluate(
        events=events,
        sequence=sequence,
        expected_context=context
    )

    if anomaly.triggered:
        evidence = evidence_buffer.extract(
            start=anomaly.start_time,
            end=anomaly.end_time
        )

        incident = create_incident(
            anomaly=anomaly,
            evidence=evidence
        )

        notify_dashboard(incident)
        accessibility.notify(incident)

    save_events(events)
```


This pseudocode is intentionally high-level. Claude should refine implementation only after the data model and module interfaces are agreed upon.


# 30. Evaluation Protocol - Detailed


## 30.1 Test Set Construction


The final test set should contain normal events, obvious anomalies, and hard negatives that resemble anomalies but are authorized. Example: an authorized staff member moving the same remote that an unauthorized visitor would move. This tests whether context, rather than object movement alone, changes the decision.


## 30.2 Per-Scenario Reporting

- Number of instances.

- Detected/not detected.

- Correct class.

- Event localization correctness.

- Alert confidence.

- Whether evidence contained the key action.

- Whether explanation matched the recorded facts.


## 30.3 Statistical/Scientific Discipline


Do not cherry-pick successful examples. Report all defined scenarios in the test protocol, include failure cases, and keep evaluation data separate from tuning data. If the dataset is small, clearly identify the limitations and use cross-validation or repeated runs where appropriate rather than inventing statistically strong conclusions from a few clips.


# 31. Minimum Viable Product vs Stretch Features


| Priority | Feature |
| --- | --- |
| MVP | Single-camera video analysis |
| MVP | Person detection/tracking |
| MVP | 3–5 monitored objects |
| MVP | 4–6 workspace zones |
| MVP | Expected visitor + count context |
| MVP | Expected task/object context |
| MVP | Event timeline |
| MVP | Rule/temporal anomaly engine |
| MVP | Evidence clips |
| MVP | Dashboard |
| MVP | Human feedback labels |
| MVP | Text-to-speech alert |
| Strong | Speech-to-text context extraction |
| Strong | Natural-language event query |
| Strong | Temporal learned model |
| Stretch | Multiple cameras |
| Stretch | Advanced speaker diarization |
| Stretch | Real-time model adaptation |
| Stretch | Mobile application |
| Stretch | Calendar integration |


# 32. Recommended FYP Development Philosophy

- Build the simplest reliable pipeline before adding sophisticated models.

- Prefer measurable improvements over more features.

- Freeze the core event taxonomy early.

- Keep observation separate from inference.

- Keep identity anonymous unless identity is truly required.

- Use structured events as the central interface between modules.

- Every AI prediction should be reproducible from stored inputs and model version.

- Every anomaly should have a human-readable reason.

- Every major design decision should have an evaluation plan.

- Avoid claims stronger than the evidence.


# 33. Instructions to Claude - How Claude Should Work on This Project


The following instructions are intended to be copied together with this document when beginning a new Claude project/chat. They define how Claude should behave as the project research, architecture and implementation assistant.


You are assisting with a Final Year Project called ContextGuard.

Project core:
ContextGuard is a context-aware multimodal workplace anomaly-detection and accessibility system. It compares expected workspace context with observed activity from camera and optional audio, uses temporal reasoning, generates explainable evidence-based potential-anomaly alerts, and exposes the same event memory through an accessibility interface for visually impaired users.

Your responsibilities:
1. Keep the project aligned with the finalized scope in this document.
2. Treat expected-vs-observed contextual reasoning as the central concept.
3. Do not reduce the project to generic CCTV or simple theft detection.
4. Do not claim that the system knows criminal intent.
5. Do not silently expand the scope into universal behavior recognition.
6. Recommend the simplest technically reliable architecture that can be evaluated.
7. When suggesting an ML model, explain why it is appropriate for the dataset, hardware and FYP timeline.
8. Distinguish existing techniques from the project-specific contribution.
9. For current literature or novelty claims, browse up-to-date sources.
10. Keep observation, inference, explanation and user feedback as separate concepts.
11. When writing code, keep modules testable and interfaces explicit.
12. Do not write a giant monolithic script when a modular design is possible.
13. Track model versions and experiment configurations.
14. Build reproducible evaluation pipelines.
15. Favor false-positive reduction and explainability, not only raw detection count.
16. Treat accessibility as a first-class system requirement.
17. Treat privacy and consent as design requirements.
18. When evidence is uncertain, use cautious language such as “potential anomaly”.
19. Never invent experimental results.
20. Never present a feature as completed if it is only planned.
21. When the project faces scope pressure, protect the MVP and postpone stretch features.
22. When proposing novelty, explicitly compare against existing research and avoid unsupported “first” claims.
23. When generating documentation, align it with the actual implemented system.
24. When debugging, ask what module produced the faulty event and trace the structured event pipeline before rewriting the whole system.
25. Preserve the event schema as the stable contract between perception, reasoning, storage, dashboard and accessibility layers.


# 34. Suggested First Tasks for Claude


1. Convert this document into a formal software requirements specification (SRS).


2. Perform a current literature review focused on workplace video anomaly detection, multimodal context, assistive vision, temporal reasoning and human-in-the-loop learning.


3. Produce a novelty/gap matrix comparing ContextGuard with existing academic and commercial systems.


4. Design the final system architecture and event/data schemas.


5. Design the custom office dataset and annotation protocol.


6. Define the MVP implementation backlog and Git repository structure.


7. Select candidate detection/tracking models based on FYP hardware constraints.


8. Design the baseline, context-aware model and ablation experiments.


9. Design the database schema and backend APIs.


10. Design the dashboard and accessibility UX.


11. Create a phased implementation plan beginning with video playback, tracking and event extraction.


# 35. Supervisor Discussion Points

- Confirm whether camera and optional audio recording are acceptable for the FYP demonstration.

- Confirm expected duration/team size and available hardware.

- Confirm whether a custom dataset can be collected using staged participants.

- Agree on the final event taxonomy before large-scale implementation.

- Agree on whether speech/NLP is mandatory or a strong optional module after the visual pipeline works.

- Agree on evaluation standards and minimum acceptable metrics.

- Agree on privacy/consent and data retention rules.

- Agree on how much of the accessibility component is required for the final grading scope.


# 36. Final One-Paragraph Project Summary


ContextGuard is a context-aware multimodal AI system for controlled workplace environments. It observes people, monitored assets and workspace activity through computer vision and optional audio, converts observations into structured temporal events, and compares them with expected context such as scheduled visitors, authorized tasks, permitted zones and expected object movements. Rather than attempting to infer criminal intent, the system detects potential deviations from expectations and produces explainable alerts containing the reason for flagging, relevant entities, timestamp and short evidence clip. The same event memory supports an accessibility layer for visually impaired users through text-to-speech notifications and natural-language queries about what happened in their workspace. Human reviewers can label alerts as normal, authorized, false alarms or potential anomalies; validated feedback becomes a controlled source of data for future model evaluation and improvement. The FYP's research contribution is evaluated by comparing visual-only, temporal and context-aware approaches and measuring whether contextual multimodal reasoning improves anomaly-detection accuracy, false-positive rate, evidence quality and accessibility usefulness.


# 37. Final One-Sentence Pitch


ContextGuard learns what is expected to happen in a workspace, observes what actually happens, detects meaningful deviations across video and optional audio, explains those deviations with evidence, and communicates important events accessibly to the user.


# 38. Current Project Status at Handoff


| Item | Status |
| --- | --- |
| Overall concept | Finalized concept direction |
| Problem definition | Defined |
| Expected-vs-observed principle | Core design principle |
| Event taxonomy | Initial taxonomy defined; supervisor/literature review may refine it |
| AI architecture | Conceptually defined; model selection remains an implementation task |
| Dataset | Not yet collected; scenario/annotation plan defined |
| Backend/frontend | Not yet implemented |
| Accessibility | Requirements defined; implementation pending |
| Audio/NLP | Optional but recommended strong component; implementation pending |
| Human feedback | Design defined; implementation pending |
| Research evaluation | Experimental framework defined; actual results pending |
| Novelty claim | Positioned conservatively; requires current literature verification before thesis claim |


# 39. Important Boundary Conditions for Future Work

- Do not turn the system into an unrestricted employee-surveillance product.

- Do not add face recognition simply because it is technically possible.

- Do not claim a person intended to steal based only on a video sequence.

- Do not let a language model invent events that are not present in structured observations.

- Do not let the LLM be the sole source of security decisions.

- Do not hide false positives; they are part of the research evaluation.

- Do not evaluate only on staged positive examples; include normal and hard-negative cases.

- Do not train and test on overlapping clips from the same exact recording without controlling leakage.

- Do not present model confidence as absolute probability unless calibration is actually performed.

- Do not sacrifice reproducibility for a flashy demo.


# 40. Final Direction


The project should be developed as a research-backed, modular AI system with a narrow and demonstrable office domain. The key differentiator is the use of context to interpret activity: an action becomes potentially anomalous because it conflicts with a defined expectation, especially when the temporal sequence and optional spoken context reinforce the mismatch.

The final demonstration should feel like an intelligent workplace assistant rather than an ordinary CCTV dashboard. A strong demo is one where the system is told what should happen, observes a staged scenario, recognizes the deviation, extracts the short evidence clip, explains the mismatch, allows a human to correct the decision, and communicates the same event through the accessible interface.


End of master handoff document.


---

# Repository Implementation Notes for Codex / ChatGPT

When this file is placed at the repository root as `MASTER_PLAN.md`, use it together with the actual repository state.

For the first repository audit, the coding agent should:

1. Print the repository tree while excluding large virtual-environment/cache/data directories.
2. Identify the active Python interpreter and dependency state.
3. Classify every relevant module as IMPLEMENTED, PARTIAL, PLANNED, DEFERRED, or EXPERIMENTAL.
4. Map existing code to the modules defined in this specification.
5. Run existing tests or smoke scripts without destructive changes.
6. Identify broken imports, dependency conflicts, hard-coded paths, model-download assumptions, and GPU-only assumptions.
7. Recommend the smallest next vertical slice that produces an end-to-end measurable result.
8. Do **not** refactor working code until the audit explains why a change is needed.

## Suggested repository control files

As implementation begins, maintain:

- `MASTER_PLAN.md` — this authoritative specification.
- `README.md` — setup and user-facing run instructions.
- `docs/ARCHITECTURE.md` — implemented architecture and interfaces.
- `docs/PROGRESS.md` — milestone/status log.
- `docs/DATASET.md` — collection, consent, annotation, split, and version notes.
- `docs/EVALUATION.md` — baselines, metrics, ablations, test protocol, and results.
- `configs/` — versioned zones, model settings, thresholds, contexts, and experiment configurations.
- `tests/` — deterministic tests for schemas, rules, events, APIs, and pipeline behavior.

## Non-negotiable research invariant

The core experimental comparison must remain capable of testing whether:

**visual-only < visual + temporal < visual + temporal + expected context**

in useful event-level behavior, particularly false-positive reduction and explanation quality.

A sophisticated demo that cannot support this comparison does not satisfy the intended research design.

---

*End of repository master plan.*

---

## Scope amendment CG-002 — 2026-09-27

Authority: accepted working decisions supplied by the user/coordinator for CG-002.
These decisions explicitly supersede conflicting scope, MVP, scenario, scheduling,
and workflow statements above for the current build. The original specification
is retained unchanged for traceability. This is not supervisor approval: the
refinement, particularly audio/accessibility deferral, still needs to be
communicated to the supervisor.

- Domain: one university faculty office, initially represented by a staged room.
- Capture: one fixed camera, recorded video first, CPU-compatible local development.
- First prototype sessions exclude the office occupant; all entering people are
  visitors. Use anonymous session track IDs, not inferred real identities.
- Initial assets: one laptop and one backpack at registered starting positions.
  This replaces the initial 3–5-object MVP and keys/remote examples as build scope.
- Core anomalies: excess simultaneous visitor occupancy (not cumulative arrivals)
  and observed asset departure inconsistent with explicitly configured session
  permission. Missing permission must not silently imply authorization.
- Occlusion, lost tracking, or missing object detections alone must never establish
  asset departure. Preserve an unknown/unobserved state distinct from departure;
  departure requires affirmative evidence to be defined and tested in a later task.
- Audio and accessibility workflows are DEFERRED from the current build, including
  speech-derived context, TTS, and accessibility event-query workflows. Original
  requirements remain historical/future scope, not current acceptance criteria.
- Use pretrained models first. Fine-tuning requires documented observed failures.
  Learned temporal modelling remains optional/proposed; deterministic temporal
  reasoning remains planned for the baseline.
- Team/resources: two students and 2–3 available volunteers. Consent and controlled
  collection remain required; availability is not evidence of consent or recordings.
- Schedule: presentation on 2026-10-14; working-system target by the end of 2026.
- Dependencies are selected per implementation milestone, not by installing the
  full proposed technology stack.

Expected-versus-observed reasoning, separation of observation/inference/feedback,
cautious anomaly wording, evidence traceability, and comparative evaluation remain
unchanged. Improvements from context/temporal reasoning are hypotheses to measure.

CG-002 is bounded to recorded-video inspection: metadata, decoded frame counts,
timing limitations, warnings, and representative review frames. No application
functionality existed at task entry. Detection, tracking, zones, asset state,
structured events, context comparison, anomaly decisions, event storage, and
evidence windows remain PLANNED; an inspection report is not an event log or an
anomaly evidence window. See docs/PROGRESS.md for verified implementation status.
