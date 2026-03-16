# Environmental Signal Detector

This module performs **Stage 1 of the image evaluation pipeline**.

Its job is to detect **environmental signals** present in an image before applying the 1983 rubric.

The detector must **not judge image quality**.

It must only identify **what environmental systems are present**.

---

# Core Principle

Stage 1 answers:

> What signals exist in this image?

Stage 2 answers:

> Are these signals aligned with the 1983 doctrine?

Detection must remain **objective and descriptive**.

---

# Environmental Signal Categories

Each image may contain **multiple signals**.

Return `true` or `false` for each.

---

## Municipal Infrastructure

Presence of built civic systems.

Examples:

- traffic signals
- street lights
- parking meters
- public rail systems
- sidewalks
- crosswalks
- transit stations
- municipal barriers

---

## Circulation Systems

Evidence that people or vehicles regularly move through the space.

Examples:

- roads
- rail tracks
- sidewalks
- bike lanes
- transit platforms
- parking infrastructure

---

## Public Residue

Traces left by human activity.

Examples:

- graffiti
- worn surfaces
- discarded objects
- scooters
- bicycles
- maintenance marks
- surface wear

---

## Industrial or Working Environment

Evidence of labor or mechanical systems.

Examples:

- docks
- warehouses
- mechanical structures
- exposed utilities
- service corridors
- construction barriers

---

## Civic Architecture

Buildings connected to public life.

Examples:

- libraries
- schools
- government buildings
- courthouses
- public institutions

---

## Commercial Street Life

Urban retail or everyday commerce.

Examples:

- storefronts
- display windows
- restaurants
- signage
- sidewalk retail

---

## Transportation Infrastructure

Systems specifically designed for movement.

Examples:

- rail stations
- train tracks
- bus stops
- tunnels
- bridges
- ports

---

## Coastal Environment

Signals of the region’s coastal geography.

Examples:

- salt-weathered metal
- maritime infrastructure
- docks
- coastal wind patterns
- marine equipment

---

## Environmental Wear

Material aging caused by time and climate.

Examples:

- rust
- peeling paint
- worn pavement
- weathered signage

---

## Graphic Dominance

Strong visual graphics dominating the frame.

Examples:

- large text signage
- bold graphic panels
- advertisement boards
- promotional messages

This signal is not inherently negative but may affect doctrine scoring later.

---

# Detector Output Format

Example output:

```json
{
  "image": "12.jpg",

  "detected_signals": {
    "municipal_infrastructure": true,
    "circulation_system": true,
    "public_residue": true,
    "industrial_environment": false,
    "civic_architecture": false,
    "commercial_street_life": true,
    "transportation_infrastructure": true,
    "coastal_environment": false,
    "environmental_wear": true,
    "graphic_dominance": false
  },

  "detected_objects": [
    "traffic signal",
    "street sign",
    "downtown buildings"
  ],

  "environment_behavior": "urban circulation corridor"
}
```

---

# Important Rules
**Do not evaluate aesthetic quality**

This stage must **not assign rubric scores.**

**Do not determine tier**

This stage only detects signals.

**Avoid doctrine language**

Do not use phrases like:
* strong environmental truth
* discovered moment
* quiet persuasion

Those belong to **Stage 2.**

---

# Signal Detection Heuristics

Use the following logic:

**If infrastructure objects dominate** → municipal infrastructure = true

**If objects imply movement** → circulation system = true

**If lived-in experience, wear or residue exists** → public residue = true

**If signage dominates the frame** → graphic dominance = true