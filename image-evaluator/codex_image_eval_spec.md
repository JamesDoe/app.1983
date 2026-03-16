# 1983 Image Evaluation Specification (Codex Reference)

## Purpose

This document defines how an automated evaluator should analyze images in a folder and produce a structured JSON file aligned with the **1983 Image Selection Rubric**.

The goal is to evaluate environmental photographs according to the brand doctrine of **quiet realism, environmental persuasion, and implied life**.

The evaluator should:

- Read all images in a specified folder
- Evaluate each image according to rubric categories
- Output a structured JSON file describing scores and observations

---

# Folder Input

Codex should expect a directory structure like:

images/
    1.jpg
    2.jpg
    3.jpg
    untitled
    ...


Each file should be evaluated independently.

The filename should be preserved in the JSON output as:

```json
"url": "1.jpg"
```

---

# Evaluation Rubric

Each image should be scored from **0–2**.

| Score | Meaning |
|------|--------|
| 0 | Reject |
| 1 | Acceptable |
| 2 | Ideal |

---

# 1. Environmental Authenticity

**Question:**  
Does the image feel like a real moment in a real place?

Strong signals:

- imperfect lighting
- natural wear
- authentic shadows
- environmental asymmetry

Red flags:

- studio lighting
- staged composition
- overly polished environment

---

# 2. Product Subordination

If clothing appears, it should feel incidental.

The garment should appear as:

> something someone happened to be wearing

Not a hero product shot.

---

# 3. Observational Quality

Does the frame feel **noticed rather than theatrically constructed**?

Strong signals:

- partial framing
- imperfect alignment
- environmental storytelling
- accidental composition
- public residue or real-world use doing the narrative work

Moderate signals:

- clear or direct composition that still feels unstaged
- centered framing where the environment remains primary

Avoid:

- fashion-shoot framing
- deliberate posing
- theatrical composition built to impress
- visual arrangements that foreground photographic polish over environmental truth

Note:
Formal clarity alone is not a reason to reduce the score.

---

# 4. Emotional Restraint

The image should **not attempt to evoke strong emotion**.

Desired tone:

- calm
- quiet
- observational

Avoid:

- dramatic expressions
- emotional staging

---

# 5. Local Texture

Does the image contain cues of **Hampton Roads or a comparable regional civic environment** without announcing it?

Examples of strong local texture:

- tunnels
- naval infrastructure
- worn sidewalks
- coastal environments
- working districts
- municipal barriers
- transit systems
- brick streetscapes
- civic signage
- parking systems
- public maintenance objects
- infrastructure shaped by water, weather, or everyday urban use

Important:
Local texture may be conveyed through ordinary civic residue and municipal systems, not only landmarks or explicit place names.

Avoid:

- tourist landmarks used as postcard shorthand
- generic polished environments
- imagery with no plausible regional character

---

# 6. Visual Humility

Does the image resist spectacle?

Preferred characteristics:

- quiet composition
- environmental modesty
- ordinary settings

Avoid:

- dramatic cinematic framing
- visual theatrics

---

# 7. Temporal Continuity

The image should feel **timeless**.

Avoid:

- trendy aesthetics
- influencer posing
- obvious content creation

---

# 8. Caption Resistance

The image should **not require a caption to function**.

Strong images:

- create interpretive tension
- communicate visually

Weak images:

- require text explanation
- explicitly state their meaning

---

# 9. Scroll Interruption

Would the image cause a subtle pause while scrolling?

Not through spectacle — but through **quiet curiosity**.

---

# 10. Signal vs Noise

Does the image hold attention across **repeated viewing**?

Strong signals:

- layered environmental detail
- textures revealed over time

Weak signals:

- novelty-based imagery
- gimmicks

---

# 11. Implied Life

**Question:**  
Does the image suggest ongoing human activity beyond the frame?

Strong signals:

- scooters
- parked vehicles
- transit infrastructure
- graffiti
- pedestrian systems
- maintenance equipment
- environmental wear

| Score | Meaning |
|------|--------|
| 0 | static environment |
| 1 | possible human activity |
| 2 | strong evidence of human activity |

---

# Output JSON Schema

Codex should output JSON structured as:
```json
{
  "images": [
    {
      "image_index": 1,
      "detected_signals": {
        "municipal_infrastructure": false,
        "circulation_system": false,
        "public_residue": false,
        "industrial_environment": false,
        "civic_architecture": false,
        "commercial_street_life": false,
        "transportation_infrastructure": false,
        "coastal_environment": false,
        "environmental_wear": false,
        "graphic_dominance": false
      },
      "detected_objects": [],
      "environment_behavior": "",
      "scores": {
        "environmental_authenticity": 0,
        "product_subordination": 0,
        "observational_quality": 0,
        "emotional_restraint": 0,
        "local_texture": 0,
        "visual_humility": 0,
        "temporal_continuity": 0,
        "caption_resistance": 0,
        "scroll_interruption": 0,
        "signal_vs_noise": 0,
        "implied_life": 0
      },
      "failure_patterns": [],
      "url": "1.jpg",
      "residue_strength": "weak | moderate | strong",
      "signal_summary": "",
      "total_score": 0,
      "tier": "greenlight | usable | reject",
      "signal_strength": "residue-driven | infrastructure-driven | circulation-driven | texture-driven | composition-driven | graphic-driven"
    }
  ]
}
```

The final JSON object for each image must include both:
- Stage 1 detection output: `detected_signals`, `detected_objects`, `environment_behavior`
- Stage 2 scoring output: `scores`, `score_notes` when used, `failure_patterns`, `signal_summary`, `total_score`, `tier`, `signal_strength`

Stage 1 detections are not intermediate-only fields. They must be preserved in `1983_image_eval.json`.

# Failure Patterns

The evaluator should flag patterns such as:
+ explained meaning
+ over-broad audience
+ predictable structure
+ staged composition
+ advertisement framing

These should appear in:

```json
"failure_patterns": []
```

---

# Implementation Guidance

Codex should:
1. Scan a folder of images
2. Evaluate each image using the rubric
3. Generate a JSON entry for each file
4. Write results to:

`1983_image_eval.json`

---

# Selection Thresholds

| Score | Meaning |
|---|---|
| 14–22 | Greenlight |
| 10–13 | Yellow |
| <10 | Reject |

If two images score similarly:

**Choose the one that feels less impressive.**

Impressive images signal **marketing.**
Quiet images signal **truth.**

For the 1983 brand doctrine: **truth beats spectacle.**

---

# Signal Summary

Provide a short paragraph explaining:

- 2–3 concrete visual details actually present in the image
- whether the image feels discovered, documentary, or staged
- what kind of implied life or public residue is present
- how it contributes to the 1983 environmental storytelling system

Requirement:
The summary must be specific enough that it would not fit another image in the same folder without obvious mismatch.

Avoid generic summary language that could describe many frames equally well.

---

## Overused Summary Language

Avoid relying on repeated phrases such as:
- environmental truth
- layered civic surfaces
- visible public residue
- quiet regional specificity
- discovered rather than arranged
- strong implied circulation

Use fresh wording tied to the actual frame.
