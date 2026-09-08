# Find Winning Products 2.0 — Search History & Adaptive Learning

Persistent `SEARCH_HISTORY` (see
[discovery-engine.md §29](references/discovery-engine.md#29-never-run-the-same-search-blindly))
plus the adaptive-learning log
([§54](references/discovery-engine.md#54-adaptive-learning)). Read before every run; check
here before re-running an exact search. If a search dimension was recently exhausted with
zero new candidates, move to a different dimension instead of repeating it.

## SEARCH_HISTORY

One row per distinct search actually run. `endpoint` is one of
`pinterest-live | pinterest-historical | tiktok | meta`.

| Date | Endpoint | Keyword | Language | Country | Page/Scroll | Candidates | New candidates | Qualifying | Notes |
|---|---|---|---|---|---|---|---|---|---|

(none yet — this is the first run)

## Historical windows already searched

Per [§25](references/discovery-engine.md#25-historical-window-rotation): track which
`mindays`/`maxdays` windows (and the calendar period they approximate) have been swept, so
future runs rotate to new seasonal windows rather than re-checking the same one.

| Window (mindays–maxdays) | Approximate calendar period | Date searched | Survivors found |
|---|---|---|---|

(none yet)

## Adaptive learning log

One entry per run, per [§54](references/discovery-engine.md#54-adaptive-learning) and the
run report's LEARNING section ([§57](references/discovery-engine.md#57-final-run-report)).
Use this to decide where to spend more depth next run.

<!--
### 2026-09-08 (run 1)
- Best keyword family: <family> (<niche>) — <n> new qualifiers
- Worst keyword family: <family> — mostly duplicates/irrelevant
- Best language: <lang>
- Best market: <market>
- Best historical window: <window>
- Best niche: <niche>
- Carry-forward for next run: <what to search deeper, what to deprioritize>
-->

(none yet — this is the first run)
