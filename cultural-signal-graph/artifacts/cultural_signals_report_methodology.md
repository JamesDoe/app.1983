# Cultural Signals Report Methodology

This note documents a repeatable way to generate and tune the cultural signals summary from the current artifacts.

## Inputs

- `artifacts/top_signals.csv`
- `artifacts/contested_phrases.csv`
- `artifacts/phrase_cooccurrence.csv`
- `artifacts/temporal_phrase_counts.csv`
- Optionally `data/processed/phrases.parquet`, `data/processed/comment_phrase_edges.parquet`, `data/processed/reply_edges.parquet`, and `data/processed/comments.parquet` for deeper validation

## Exclusion Policy

The phrase extractor now excludes a curated list of low-signal conversational filler phrases before downstream analysis. This includes words such as:

- `yes`
- `lol`
- `right`
- `thank`
- `ok`
- `wow`
- `removed reddit`
- `wrong`
- `fuck`
- `lmao`
- `like`
- `correct`
- plus related low-signal variants like `yeah`, `yep`, `agree`, `agreed`, `sure`, `true`, `good`, `nope`, `look`, `know`, and `said`

This exclusion list is intentionally iterative, not final.

Rule:
- when a phrase repeatedly dominates stable, contested, or salience outputs without adding thematic value, add it to the exclusion list in `src/csg/extract/phrases.py`

Examples of phrases that still look like future exclusion candidates after the latest refresh:
- `hope helps`
- `going happen`
- `maybe run office`
- `party proud`
- `asking question`

## Section Logic

### Top Stable Signals

Pick phrases that:
- rank highly in `top_signals.csv`
- appear across multiple distinct weeks in `temporal_phrase_counts.csv`
- remain analytically meaningful after low-signal filtering

Use:
- `signal_salience`
- `phrase_frequency`
- count of distinct `week_start`
- latest weekly usage count

Do not blindly accept the raw top rows. Review them for conversational filler leakage and prefer phrases that are clearly topical, political, geographic, institutional, or event-specific.

Specific heuristic:
- if a phrase looks like a contraction fragment, reply-style shell, or argument wrapper rather than a topic label, add it to the exclusion process even if it is multiword

Current state:
- the pipeline is now in a usable state for analysis
- future exclusions should be narrow and justified by repeated appearance in top outputs, not broad cleanup passes

### Top Emerging Signals

Pick phrases that:
- appear in the latest `week_start`
- have low or zero prior total usage
- show the highest latest-week delta relative to all earlier weeks

Use:
- latest weekly count
- prior cumulative count
- `delta = latest_week_count - prior_total`

### Most Contested Signals

Use `contested_phrases.csv`.

Rank by:
- `deep_comment_count`
- then `max_verified_depth`

Again, inspect for rhetorical filler that may deserve future exclusion.

### Top Co-Occurrence Clusters

Use `phrase_cooccurrence.csv`.

Rank by:
- `cooccurrence_count`

Prefer summarizing 3-6 phrase pairs or pair-families that clearly reflect one narrative cluster.

## Interpretation Rules

- Distinguish between conversational markers and substantive topical phrases.
- Treat long repeated phrases as thread-local narratives unless they recur across multiple weeks.
- Use the stable/emerging contrast to separate ongoing regional discourse habits from short-lived event spikes.
- Co-occurrence clusters are often more interpretable than raw salience rankings.
- Keep the report concise; examples matter more than exhaustive lists.

## Maintenance Loop

After each refresh:

1. Regenerate phrase extraction and downstream artifacts.
2. Review `top_signals.csv`, `contested_phrases.csv`, and the stable-week summary for low-signal leakage.
3. Add newly identified filler phrases to the exclusion list in `src/csg/extract/phrases.py`.
4. Regenerate the artifacts and report.
5. Repeat until the top rows are predominantly thematic rather than rhetorical.
6. Once outputs are mostly serviceable, switch from broad exclusion passes to occasional targeted cleanup only.

## Caveats

- The current noun-phrase extraction can still surface generic rhetorical fragments.
- Co-occurrence clusters may reflect a single highly repetitive thread rather than a broad regional pattern.
- Emerging signals are sensitive to the latest weekly slice and may represent one bursty discussion.
- Any exclusion list introduces analyst judgment, so additions should be conservative and traceable.
