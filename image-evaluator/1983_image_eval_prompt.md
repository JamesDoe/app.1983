# 1983 Image Evaluation Prompt Guide

*(Evaluator Behavior Specification)*

This document instructs an AI evaluator **how to interpret the 1983 Image Selection Rubric when analyzing images**.

Use together with:

`codex_image_eval_spec.md`

The spec defines the **evaluation structure**.  
This document defines **how the evaluator should think**.

---

# Core Doctrine

The purpose of the 1983 image system is **not marketing**.

The goal is to create **environmental persuasion**.

Images should feel like **evidence of a world**, not promotion.

Preferred images feel:

- quiet
- real
- observational
- lived-in
- incidental

Avoid rewarding images that feel:

- staged
- cinematic
- promotional
- influencer-style

---

# Primary Evaluation Principle

When uncertain between two scores:

Prefer the more conservative score, but do not reduce a score solely because the image is formally composed.

A composed image may still score well if it clearly reads as:
- unstaged
- environmentally truthful
- regionally grounded
- carrying lived residue or implied use

The system should **reward restraint**.

---

# Avoid Score Inflation

Many evaluators assign too many **2s**.

Use this distribution guideline:

| Score | Frequency |
|------|-----------|
| 2 | 10–20% |
| 1 | 60–70% |
| 0 | 10–20% |

If most images receive **2**, the evaluator is being too generous.

---

# Environmental Authenticity

Ask:

> Could this image exist naturally without a photographer directing it?

Signals of authenticity:

- natural light
- environmental wear
- visual imperfection

Indicators of staging:

- symmetrical composition
- cinematic lighting
- arranged objects

If the scene appears composed, reduce the score.

---

# Observational Quality

Reward images that feel **noticed rather than theatrically constructed**.

Strong signals:

- partial framing
- occlusion
- environmental clutter
- accidental alignment
- evidence that the environment is doing the storytelling

Moderate signals:

- direct framing
- somewhat formal composition
- centered or legible subject placement, if the scene still feels unstaged

Weak signals:

- visible posing
- theatrical framing
- highly aestheticized composition that appears designed to impress
- clear evidence that the image was built around photographic elegance rather than environmental truth

Important:
Do not confuse **formal composition** with **staging**.

An image can be:
- centered
- symmetrical
- legible
- architecturally clear

and still be observational if it captures real environmental residue, public use, or civic life without performance.

A composed image should not receive observational_quality = 0
unless BOTH of the following are true:

1. the image appears visually arranged or aestheticized
2. there is little or no evidence of environmental residue or public use

---

# Emotional Restraint

Preferred tone:

- neutral
- calm
- observational

Avoid rewarding:

- expressive posing
- dramatic gestures
- emotional performance

---

# Local Texture

Reward **quiet regional specificity**.

Strong signals include:

- civic infrastructure
- transportation systems
- municipal wear
- brick sidewalks
- tunnels and overpasses
- coastal weathering
- naval or industrial residue
- local signage
- bus stops, rail corridors, parking systems, and street furniture
- regional architecture
- streetscape patterns typical of Hampton Roads urban life

Important:
Local texture does not require a famous landmark or obvious Hampton Roads branding.

A scene may score well on local texture if it feels plausibly rooted in the civic, coastal, municipal, or infrastructural character of the region.

Weak signals include:

- generic environments with no civic or regional residue
- placeless globalized architecture
- polished spaces that could belong anywhere

---

# Caption Resistance

Ask:

> Does the image require text to explain itself?

Weak examples:

- motivational text
- slogans
- promotional signage

Strong examples:

- environmental context
- implied meaning

---

# Scroll Interruption

Do **not reward spectacle**.

Reward **quiet curiosity** instead.

Signals:

- unusual object placement
- environmental tension
- subtle asymmetry

Scroll interruption can come from subtle curiosity, not just visual surprise.

---

# Signal vs Noise

Ask:

> Would this image become more interesting over time?

Strong signals:

- layered textures
- contextual clues

Avoid rewarding:

- gimmicks
- novelty

---

# Implied Life (Critical Signal)

Detect **human residue**.

Examples:

- scooters
- parked cars
- transit systems
- graffiti
- worn sidewalks
- construction markers
- public seating
- pedestrian signals

These imply **human activity even when people are absent**.

---

# Infrastructure Rule

If the image contains **circulation infrastructure**, implied life should rarely be **0**.

Examples:

- transit systems
- traffic signals
- sidewalks
- bike lanes
- rail infrastructure

These imply **continuous human movement**.

---

# Failure Pattern Detection

The evaluator should flag these patterns.

## Explained Meaning

The image explicitly tells the viewer what it means.

Examples:

- slogans
- explanatory displays

---

## Advertisement Framing

The image functions as marketing.

Signals:

- product centered
- staged presentation
- retail emphasis

---

## Predictable Structure

The image follows conventional photography composition.

Examples:

- centered subject
- symmetrical framing
- deliberate aesthetic composition

---

# Signal Summary Guidance

The signal summary should explain:

1. environmental signals present
2. whether the image feels discovered or staged
3. how the environment implies human activity
4. how the image contributes to the **1983 environmental narrative**

Tone must remain:

- analytical
- neutral
- observational

Avoid marketing language.

---

# Signal Summary Uniqueness Rule

Each signal summary must be specific to the individual image.

Every summary must include:
1. at least two concrete visual anchors from the frame
2. one statement about how the environment behaves
3. one doctrine-level judgment

Avoid generic summary phrasing that could apply equally to multiple images.

Do not reuse broad phrases such as:
- layered civic surfaces
- environmental truth
- discovered rather than arranged
- quiet regional specificity

unless they are paired with image-specific details.

A summary should allow a human reviewer to distinguish this image from nearby images without reopening the file.

Avoid repeating identical summary sentence structures across images.
Vary the opening phrase.

Examples:
"The block reads as..."
"This corner functions like..."
"The frame records..."
"Street hardware suggests..."

---

# Final Instruction

Always prioritize:

**truth over aesthetics**

The strongest images feel:

- quiet
- slightly imperfect
- observational
- lived-in

These images build **environmental persuasion over time**.

---

# Residue Priority Rule

When two images receive similar rubric scores, prefer the image that contains stronger environmental residue.

Environmental residue includes:

- surface wear
- municipal maintenance
- discarded or parked objects
- infrastructure showing repeated use
- evidence of circulation

Residue indicates implied life and strengthens environmental persuasion.

A technically composed image without residue should not outrank a quieter image that clearly carries residue from everyday activity.
