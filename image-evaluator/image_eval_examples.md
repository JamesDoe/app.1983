# 1983 Image Evaluation Examples

This document provides **reference examples** for the 1983 image evaluator.

These examples help the evaluator understand the difference between:

- quiet environmental signal
- empty realism
- marketing imagery

This document should be used alongside:

- codex_image_eval_spec.md
- 1983_image_eval_prompt.md
- image_eval_runner.md

---

# Core Principle

The goal of the 1983 system is **environmental persuasion**, not advertising.

Images should feel like:

> evidence of a lived world

not

> content produced for a brand.

---

# Example Category A  
# Strong Environmental Signal

## Example: Urban Residue

**Scene**

- rental scooter leaning against city fencing  
- graffiti on nearby infrastructure  
- worn sidewalk  
- no people visible  

**Evaluation**

Environmental Authenticity: 2  
Observational Quality: 2  
Implied Life: 2  

**Reason**

The scooter functions as **human residue**.  
It implies someone was recently present.

The scene feels discovered rather than staged.

---

# Example Category B  
# Strong Implied Life

## Example: Transit Infrastructure

**Scene**

- light rail station platform  
- rails extending into distance  
- pedestrian signage  
- downtown buildings  

**Evaluation**

Environmental Authenticity: 2  
Observational Quality: 2  
Implied Life: 2  

**Reason**

Transit infrastructure implies **continuous human circulation**, even if people are absent.

---

# Example Category C  
# Moderate Signal

## Example: Ordinary Streetscape

**Scene**

- sidewalk
- traffic lights
- parked cars
- neutral architecture

**Evaluation**

Environmental Authenticity: 2  
Observational Quality: 1  
Implied Life: 1  

**Reason**

The environment is real, but the frame does not capture a specific moment of environmental tension.

---

# Example Category D  
# Empty Realism

## Example: Static Architecture

**Scene**

- large building facade
- empty plaza
- symmetrical framing

**Evaluation**

Environmental Authenticity: 1  
Observational Quality: 0  
Implied Life: 0  

**Reason**

The environment is real but **contains no evidence of human activity**.

This is architectural documentation, not environmental storytelling.

---

# Example Category E  
# Explained Meaning

## Example: Promotional Signage

**Scene**

- storefront window
- motivational phrase
- graphic typography dominating frame

**Evaluation**

Caption Resistance: 0  
Signal vs Noise: 0  

Failure Pattern:

explained meaning

**Reason**

The image tells the viewer what it means instead of allowing the environment to imply meaning.

---

# Example Category F  
# Advertisement Framing

## Example: Product-Focused Image

**Scene**

- clothing centered
- clean background
- model posing

**Evaluation**

Product Subordination: 0  

Failure Pattern:

advertisement framing

**Reason**

The product becomes the subject of the image.

This violates the environmental persuasion doctrine.

---

# Example Category G  
# Quiet but Strong

## Example: Civic Maintenance

**Scene**

- traffic barrel on brick sidewalk
- uneven shadows
- street landscaping
- subtle wear

**Evaluation**

Environmental Authenticity: 2  
Visual Humility: 2  
Implied Life: 2  

**Reason**

Maintenance objects imply **ongoing civic activity**.

These objects function as subtle evidence of daily life.

---

# Example Category H  
# Weak Scroll Interruption

## Example: Generic City Scene

**Scene**

- street intersection
- no unusual objects
- balanced framing

**Evaluation**

Scroll Interruption: 0  
Signal vs Noise: 1  

**Reason**

The environment is real but lacks tension or curiosity.

---

# Example Category I
# Formal but Still Observational

## Example: Transit Corridor with Clear Symmetry

**Scene**

- light rail platform or street corridor
- strong lines receding into distance
- relatively centered framing
- public infrastructure dominates
- no posing or theatrical action

**Evaluation**

Observational Quality: 1 or 2  
Implied Life: 2  

**Reason**

The image may be formally composed, but it still feels observational because the environment is primary and the frame captures real public infrastructure rather than staged intention.

Centered composition alone does not make an image non-observational.

---

# Example Category J
# Quiet Regional Texture

## Example: Municipal Streetscape with Coastal-Civic Wear

**Scene**

- brick sidewalk
- traffic hardware
- utility markings
- weathered surfaces
- low-key civic architecture
- no famous landmark visible

**Evaluation**

Local Texture: 1 or 2  

**Reason**

The image does not need an iconic regional landmark to carry local texture. Ordinary municipal systems, coastal wear, and public infrastructure can quietly signal place.

---

# Evaluator Calibration

Across a typical dataset:

| Score | Expected Frequency |
|------|--------------------|
| 2 | 10–20% |
| 1 | 60–70% |
| 0 | 10–20% |

If most images receive **2**, the evaluator is being too generous.

---

# Final Instruction

The evaluator should always prioritize:

truth > aesthetics

The strongest images will feel:

- quiet
- imperfect
- observational
- lived-in

These images build **environmental persuasion over time**.