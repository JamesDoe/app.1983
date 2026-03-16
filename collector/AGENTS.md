# AGENTS.md

## Goal
Build only the Reddit data collectors for the MVP.

## Scope
Implement:
- thread collector
- full comment-tree collector
- normalized JSONL writers
- raw payload archival
- checkpointing
- CLI entrypoints

Do not implement:
- concept extraction
- phrase extraction
- clustering
- graphs
- dashboards
- embeddings
- sentiment analysis
- databases beyond local files

## Repository expectations
- Use Python 3.11+
- Prefer simple, boring code
- Use type hints
- Keep modules small
- Add tests for normalization and recursive depth traversal
- Make output inspectable as JSONL
- Write raw payloads separately from normalized records

## Required normalized outputs

### Thread record
Fields:
- record_type
- source
- community
- thread_id
- native_id
- author_id
- created_at
- title
- text
- score
- num_comments
- upvote_ratio
- permalink

### Comment record
Fields:
- record_type
- source
- community
- thread_id
- content_id
- native_id
- author_id
- parent_id
- depth
- reply_count
- created_at
- text
- score
- permalink
- author_flair_text
- distinguished
- stickied

## Collector modes
- pulse
- backfill

## Success criteria
- Can collect threads from r/norfolk, r/VirginiaBeach, r/hamptonroads
- Can collect full comment trees with true depth
- Can rerun without duplicate normalized records
- Can write raw and normalized JSONL