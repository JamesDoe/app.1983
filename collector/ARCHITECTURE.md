# ARCHITECTURE

## Purpose
This repository builds the Reddit-only collectors for a cultural-signal MVP.

## Core idea
Collect first. Analyze later.

## Components
- thread collector
- comment tree collector
- normalization layer
- JSONL writers
- checkpointing

## Modes
### Pulse
Recent activity:
- hot
- new

### Backfill
Historical accumulation:
- top(month)
- resumable collection

## Raw vs normalized
### Raw
Store original Reddit/PRAW payloads for recovery.

### Normalized
Store stable JSONL records shaped for downstream analysis.

## Key design rule
The collectors must preserve conversation topology:
- thread_id
- parent_id
- depth
- reply_count

## Output contracts
Document the thread and comment schemas exactly.