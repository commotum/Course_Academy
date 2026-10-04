# Historical activity capture and timing

Captured all **219 task URLs** in `reference/progress.csv` on October 4, 2026.
The capture read completed history pages only. It did not start activities,
submit answers, import content into EDB, or change learner records.

The original CSV SHA-256 is
`5ec6ef5fcd34c77493ed76775410c41fdafd85df77a500a4e3e1f7e1f4d255b0`.

Each `<task-id>.json` retains question order, IDs, difficulty, displayed outcome,
elapsed time, answer timestamp, KP title/source link, and question/activity HTML.
Large page HTML was exported in pieces to avoid the browser export's per-string
limit. `manifest.json` records the requested tasks and capture status.

`observations.json` adds numeric durations, question prompts, worked solutions,
and canonical KP example references. Canonical examples generally come from the
existing MA lesson archive; they do not establish which version of an example
the learner read historically. Topic 281's archived “Leibnitz” spelling is
matched to the history's “Leibniz.” Example 22727 in topic 7011 was missing from
the archive and was captured from its current reference page; its separate
source record preserves that provenance.

All **1,638 questions** have prompts, worked solutions, difficulty labels,
outcomes, displayed durations, and matched canonical examples. Linked image URLs
are retained; this capture does not bundle every image. Source HTML retains
response evidence, but derived canonical answer keys are not asserted here.

Reproduce the extraction and summaries with:

```sh
/home/jake/Developer/MA/.venv/bin/python reference/mathacademy/progress-history-2026-10-04/derive.py
```

## Timing results

The pooled ratio is `sum(question seconds) / (60 * sum(base XP))` over the same
set of activities. Earned XP is not used. Eight diagnostics lack base XP and are
excluded from the ratio, but their question evidence is retained.

| Type | Activities | Base minutes | Question minutes | Pooled ratio |
|---|---:|---:|---:|---:|
| Lesson | 135 | 1,443 | 2,259.87 | 1.57× |
| Review | 53 | 227 | 665.07 | 2.93× |
| Assessment | 13 | 177 | 146.37 | 0.83× |
| Multistep | 10 | 101 | 268.55 | 2.66× |
| All with base XP | 211 | 1,948 | 3,339.85 | 1.71× |
| Reviews and assessments | 66 | 404 | 811.43 | 2.01× |

These are recorded **question-time** ratios. They exclude tutorial/example
reading and may include pauses. Quiz time limits constrain observed durations.
They describe this history rather than establishing one common speed factor
for every activity type. No duration is inferred from completion timestamps.

## Instructional overhead for a later approximation

The existing fitted lesson-base formula contains the contribution
`0.07513004637186382 * R + 0.034422123109798704 * E` minutes, where `R` is tutorial
and canonical-example prose words divided by 100 and `E` is the number of equals
signs in canonical-example solutions. This can be reused as an instructional
overhead proxy without difficulty ratings. The terms were fitted jointly to
total lesson XP; they are not independently measured reading times. The
seven-XP floor applies to the whole lesson estimate, not to reading overhead.

No revised base-XP or question-band timing formula was fitted during this capture.
