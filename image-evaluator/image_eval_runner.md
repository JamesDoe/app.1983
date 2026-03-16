# 1983 Image Evaluation Runner

This document defines how Codex (or another AI execution agent) should run the 1983 image evaluation pipeline.

This runner works together with:

- `codex_image_eval_spec.md`
- `1983_image_eval_prompt.md`

Those documents define the **evaluation logic**.

This document defines the **execution workflow**.

---

# Objective

Automatically evaluate a folder of environmental images and produce:

`1983_image_eval.json`

The JSON file should contain one evaluation object per image.

---

# Folder Structure

The runner expects the following structure:
project_root/
    images/
        1.jpg
        2.jpg
        3.jpg
        ...
    codex_image_eval_spec.md
    1983_image_eval_prompt.md
    image_eval_runner.md

All images inside `/images` should be evaluated.

---

# Step 1 — Scan Image Directory

The runner should:

1. Open `/images`
2. Identify all image files

Supported formats:

* .jpg
* .jpeg
* .png
* .webp


Sort files **alpha-numerically if possible**.

Example order:
1.jpg
2.jpg
3.jpg
...
20.jpg
untitled.jpg

---

# Step 2 — Initialize JSON Output

Create an empty structure:

```json
{
  "images": []
}
```

Each evaluated image will append an object to this array.

---

# Step 3 — Evaluate Each Image

For each image:
1. Load the image
2. Run Stage 1 environmental signal detection and record:
   `detected_signals`
   `detected_objects`
   `environment_behavior`
3. Apply the evaluation rubric defined in:
    codex_image_eval_spec.md
4. Follow evaluator behavior rules defined in:

`1983_image_eval_prompt.md`

---

# Step 4 — Generate Evaluation Object

For each image, produce an object in this format.

Important:
The final object written to `1983_image_eval.json` must include both:
- the Stage 1 detection fields
- the Stage 2/Stage 4 rubric fields

Do not discard Stage 1 output after scoring.

Example:

```json
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
  "signal_summary": ""
}
```

---

# Step 5 — Failure Pattern Detection

During evaluation, detect and record patterns such as:

* explained meaning
* advertisement framing
* predictable structure
* staged composition
* influencer-style imagery

If detected:
```json
"failure_patterns": ["explained meaning"]
```
Multiple patterns may appear in the list.

Example:

```json
"failure_patterns": [
  "explained meaning",
  "advertisement framing"
]
```

---

# Step 6 — Generate Signal Summary

Each image must include a short paragraph describing:
* Environmental signals present
* Whether the scene feels discovered or staged
* Evidence of implied life
* Contribution to regional storytelling

Tone must remain:
* analytical
* neutral
* observational
* Avoid marketing language.

Example:
"Graffiti-marked utility box on a brick sidewalk captures everyday municipal infrastructure and urban wear. The scene reads as a found environmental moment with strong traces of human activity."

---

# Step 6.5 — Consistency Check

Before finalizing scores, verify the following:

- Do not reduce `observational_quality` solely because the image is centered, legible, or somewhat symmetrical.
- If the environment clearly carries public residue, municipal use, transit logic, or civic life, `observational_quality` should not default to 0.
- Do not reduce `local_texture` solely because there is no famous landmark or explicit Hampton Roads text.
- Ordinary regional civic infrastructure, municipal wear, and coastal-urban residue may still justify `local_texture` = 1 or 2.

If a score of 0 is assigned to `observational_quality` or `local_texture`, provide a specific reason in the signal summary.

---

# Step 7 — Append to JSON

Append the completed object to:

```json
images[]
```

Example structure:
```json
{
  "images": [
    {...},
    {...}
  ]
}
```

---

# Step 8 — Write Output File

Save the final evaluation file to:

`1983_image_eval.json`

Example output:
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
      "scores": {...},
      "score_notes": {
          "observational_quality_note": "",
          "local_texture_note": ""
      },
      "failure_patterns": [],
      "url": "1.jpg",
      "residue_strength": "weak | moderate | strong",
      "signal_summary": "...",
      "total_score": 0,
      "tier": "greenlight | usable | reject",
      "signal_strength": "residue-driven | infrastructure-driven | circulation-driven | texture-driven | composition-driven | graphic-driven"
    },
    {
      "image_index": 2,
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
      "scores": {...},
      "score_notes": {
          "observational_quality_note": "",
          "local_texture_note": ""
      },
      "failure_patterns": [],
      "url": "2.jpg",
      "residue_strength": "weak | moderate | strong",
      "signal_summary": "...",
      "total_score": 0,
      "tier": "greenlight | usable | reject",
      "signal_strength": "residue-driven | infrastructure-driven | circulation-driven | texture-driven | composition-driven | graphic-driven"
    }
  ]
}
```

---

# Step 8.5 — Summary Similarity Check

After generating all signal summaries:

1. compare each summary against all others
2. flag summaries that are identical or near-identical
3. if two summaries are too similar, regenerate them with stronger image-specific anchors

A summary should be considered too similar if:
- it is identical
- it differs only by minor adjective changes
- it could plausibly describe the same scene without contradiction

When regenerating, require:
- more concrete object references
- stronger distinction in public residue or spatial behavior
- less reusable doctrine phrasing

---

# Step 9 — Optional Ranking

After evaluation, compute a total score:

`total_score = sum (all rubric categories)`

Suggested interpretation:

| Score | Meaning |
|---|---|
| 14–22 | Greenlight |
| 10–13 | Yellow |
| <10 | Reject |

---

# Step 10 — Sorting (Optional)

The runner may output images sorted by:

`total_score DESC`

This produces a ranked list of strongest environmental signals.

Example sorted output:
```json
{
  "images_ranked": [
    {...},
    {...},
    {...}
  ]
}
```

---

# Residue Preference

If two images have similar total scores (difference ≤ 2):

Prefer the image that contains:

- public_residue
- environmental_wear
- circulation_system

These signals indicate stronger implied life.

---

# Signal Multipliers

After calculating the base rubric score, apply signal multipliers.

Residue Multiplier
If residue_strength = strong → total_score +2

Infrastructure Multiplier
If municipal_infrastructure AND circulation_system = strong → total_score +1

Circulation Multiplier
If environment_behavior indicates active movement corridor → scroll_interruption +1

Graphic Penalty
If graphic_dominance = strong AND public_residue = weak → total_score −1

---

# Recommended Execution Loop

Pseudo-process:

scan /images

for image in images:

    load image

    evaluate rubric

    generate JSON object

    append to images[]

write 1983_image_eval.json

---

# Key Instruction

The evaluator should always prioritize:

truth > aesthetics

The best images will feel:

* quiet
* imperfect
* observational
* lived-in
* uninterested in impressing the viewer

These images build **environmental persuasion.**

---

# Final Output

The completed pipeline produces:

`images/ (source images)`
`1983_image_eval.json (evaluation results)`

Each image object in `1983_image_eval.json` must retain:
- `detected_signals`
- `detected_objects`
- `environment_behavior`
- all rubric scoring and summary fields

This file can then be used for:

* image ranking
* campaign selection
* training future evaluators
* dataset building
