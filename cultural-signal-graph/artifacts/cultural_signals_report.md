# Cultural Signals Report

This report summarizes the strongest cultural signals in the refreshed artifact set after the latest phrase-quality tuning pass removed most of the earlier conversational and argument-shell residue.

## Top Stable Signals

These phrases now represent the top surviving stable signals after the latest tuning pass. The stable list is now largely topical and serviceable.

| Phrase | Salience | Frequency | Weeks Seen | Latest Weekly Count |
| --- | ---: | ---: | ---: | ---: |
| `nazi scum` | 15.50 | 47 | multi-week | 47 total mentions |
| `kids alright` | 9.81 | 4 | recurring high-salience phrase | 4 total mentions |
| `fuck ice` | 9.29 | 6 | multi-week | 6 total mentions |
| `trump` | 8.16 | 7 | multi-week | 7 total mentions |
| `texas` | 7.88 | 9 | multi-week | 9 total mentions |
| `democrats` | 7.13 | 8 | multi-week | 8 total mentions |

Read: the stable section is now substantially more thematic. It surfaces political hostility, immigration-related rhetoric, electoral conflict, and issue-specific identifiers much more clearly than earlier runs. Residual low-signal leakage is now mostly pushed below the main stable tier.

## Top Emerging Signals

These phrases spike in the latest observed week (`2026-03-09`) with little or no earlier presence.

| Phrase | Latest Week Count | Prior Total | Delta |
| --- | ---: | ---: | ---: |
| `splinter group neo nazi group called vanguard usa ...` | 10 | 0 | 10 |
| `httpswwwsplcenterorgresourceshatewatchmeetpatriotfront...` | 9 | 0 | 9 |
| `post locked direct comments thread instead ...` | 6 | 0 | 6 |
| `parents lied police reports raised nearly 30k funeral paid` | 5 | 0 | 5 |
| `woman s child drowned home intoxicated` | 5 | 0 | 5 |
| `second child s lost neglect s getting slap wrist` | 5 | 0 | 5 |

Read: emerging signals remain sharply event-driven. They cluster around extremist-organizing discourse, moderation spillover into related threads, and a repeated child-neglect narrative.

## Most Contested Signals

These phrases appear in comments whose verified reply depth exceeds 5.

| Phrase | Deep Comment Count | Max Verified Depth |
| --- | ---: | ---: |
| `ar15s collapsing stocks threaded barrels 30 round magazines common use` | 3 | 40 |
| `democrats` | 3 | 13 |
| `epstein files` | 3 | 13 |
| `arms supreme court protected 2a` | 2 | 40 |
| `legislation doesnt ban sale typical ar15` | 2 | 40 |
| `sale firearms protected constitution` | 2 | 36 |
| `trump` | 2 | 20 |
| `dont support gerrymandering` | 2 | 14 |

Read: the contested section is now much better. Most surviving phrases are issue-bearing, especially around firearms law, electoral conflict, and high-conflict national politics. The remaining residue is now minor and mostly confined to lower-ranked reply-style fragments.

## Top Co-Occurrence Clusters

The strongest co-occurrence clusters still come from concentrated thread-level narrative bundles.

| Phrase Pair / Cluster Example | Co-Occurrence Count |
| --- | ---: |
| `woman s child drowned home intoxicated` + `parents lied police reports raised nearly 30k funeral paid` | 5 |
| `woman s child drowned home intoxicated` + `second child s lost neglect s getting slap wrist` | 5 |
| `parents lied police reports raised nearly 30k funeral paid` + `second child s lost neglect s getting slap wrist` | 5 |
| `virginia judge blocks democrats referendum blow redistricting effort 4` + `house seats` | 4 |
| Patriot Front / Vanguard America descriptor cluster | 4 |
| `liberal` + multiple voter-ID / election-access claims | 4 |

Read: the co-occurrence output is currently the most interpretable part of the pipeline. It surfaces coherent narrative clusters around child neglect, redistricting and voter-ID conflict, and extremist political organization.

## Overall Read

- The latest phrase-quality pass made the stable leaderboard clearly serviceable.
- The contested list is now much closer to usable, with most of the earlier argument-shell residue removed.
- Emerging and co-occurrence outputs are already much more serviceable than the stable leaderboard for substantive regional analysis.
- Any future tuning can now be narrow and optional, focused only on low-volume reply-style residue such as `hope helps`, `going happen`, or `maybe run office` if those continue to surface.
