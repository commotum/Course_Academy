# Current generator ages — November 11, 2026

EDB math basis: 14285. Count current knowledge-point → generator registrations,
not detached historical generator entities or saved drafts.

Current registrations: **997**, representing 997 distinct generator entities.
995 use packaged paths and two retain legacy scratch paths.

| Saved pipeline change | Current versions predating it | Current versions registered since |
| --- | ---: | ---: |
| Independent-practice overhaul, Oct 28 at 17:50:04 PDT (`674970d30e2`) | 711 | 286 |
| Phase policy 3/source-account overhaul, Nov 5 at 16:11:44 PST (`e0e0648ec7a`) | 876 | 121 |

Dates above are the saved Git revisions. Using the start of Oct 28 instead gives
634 before and 363 on/after that date.

Registration date measures the current generator version's first surviving
script assertion. Later reviews of the same version can occur without a new
registration. Age alone does not determine current instructional compliance.

`counts.json` contains all current KP IDs, generator IDs, script paths,
registration/binding dates, and the count cohorts. Read-only query capture is in
`/tmp/generator-age-audit-2026-11-11`. No generation or database changes occurred.

## Replacements of older generators

Retained knowledge-point → generator assertion history at the same EDB basis
shows that, among the 286 current versions first registered after the Oct 28
saved change, **181 replaced a generator for a KP that already had one before
that change**, while **105 were first registrations** for their KPs.

Among the 121 current versions since the Nov 5 phase change, 48 replaced
pre-existing generators and 73 were first registrations. These are overlapping
cutoff analyses, not additive groups.

A replacement identifies a new registered version; it does not itself distinguish
pedagogical repair from repackaging. Reviews of unchanged versions are additional
work not counted as replacements. Per-KP records are in
`oct28-replacement-history.json` and `nov5-replacement-history.json`.
