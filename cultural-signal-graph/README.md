# cultural-signal-graph

CLI-driven MVP for ingesting discussion data, extracting phrases, building lightweight graphs, and running basic analyses.

Developer handoff documentation is available in `dev-docs.html`.

## Requirements

- Python 3.11+

## Setup

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .[dev]
python -m spacy download en_core_web_sm
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .[dev]
python -m spacy download en_core_web_sm
```

Because this project uses a `src/` layout, install it in editable mode before running module commands like `python -m csg.cli.ingest`.

## Project Layout

```text
src/csg/
  cli/          # pipeline commands
  io/           # input loaders
  extract/      # normalization and phrase extraction
  graph/        # graph construction
  analysis/     # basic statistics
```

## Pipeline Overview

Run the current pipeline in this order:

```bash
pip install -e .[dev]
python -m csg.cli.ingest
python -m csg.cli.extract_phrases
python -m csg.cli.build_graph
python -m csg.cli.analyze
```

This produces:

- `data/processed/comments.parquet`
- `data/processed/threads.parquet`
- `data/processed/phrases.parquet`
- `data/processed/comment_phrase_edges.parquet`
- `data/processed/reply_edges.parquet`
- `data/processed/thread_metrics.parquet`
- `artifacts/phrase_frequency.csv`
- `artifacts/phrase_cooccurrence.csv`
- `artifacts/contested_phrases.csv`
- `artifacts/temporal_phrase_counts.csv`
- `artifacts/top_signals.csv`
- `artifacts/errors.jsonl`

## Ingestion

The ingestion pipeline validates raw JSONL, normalizes `created_at` to UTC datetimes, skips malformed rows, logs invalid inputs to `artifacts/errors.jsonl`, and writes parquet outputs.

```bash
pip install -e .[dev]
python -m csg.cli.ingest
```

Installed entrypoint form:

```bash
pip install -e .[dev]
csg-ingest --comments data/raw/comments.jsonl --threads data/raw/threads.jsonl
```

Outputs:

- `data/processed/comments.parquet`
- `data/processed/threads.parquet`
- `artifacts/errors.jsonl`

## Phrase Extraction

Phrase extraction reads `data/processed/comments.parquet`, uses spaCy to extract noun-phrase candidates, normalizes phrases, preserves local abbreviations such as `hrbt`, `vb`, `odu`, `norfolk`, and `ghent`, and writes:

- `data/processed/phrases.parquet`
- `data/processed/comment_phrase_edges.parquet`

```bash
python -m csg.cli.extract_phrases
```

## Reply Graph

Reply graph reconstruction reads `data/processed/comments.parquet`, reconstructs comment-to-comment reply edges from Reddit `parent_id` values, computes verified reply depth and thread-level depth statistics, and writes:

- `data/processed/reply_edges.parquet`
- `data/processed/thread_metrics.parquet`

```bash
python -m csg.cli.build_graph
```

## Analysis

The analysis stage reads the processed parquet artifacts and produces phrase frequency, phrase co-occurrence, contested phrase signals from deep reply chains, weekly temporal counts, and a salience ranking.

Outputs:

- `artifacts/phrase_frequency.csv`
- `artifacts/phrase_cooccurrence.csv`
- `artifacts/contested_phrases.csv`
- `artifacts/temporal_phrase_counts.csv`
- `artifacts/top_signals.csv`

```bash
python -m csg.cli.analyze
```
