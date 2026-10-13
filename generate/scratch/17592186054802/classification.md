# Identifying a Line Given a Graph

Captured source basis: 2036. Database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The job's basis 1994 is stale. Native inventory at basis 2037 reports two available hard questions and a shortage of three. No generator or supplied `.generated` file existed.

All four practice questions and the canonical example are retained in `source.json` and the exact EDB read in `reference/source.edn`. No source or learner facts are edited.

| Band | Fields | Templates | Profiles | Plot requirement | Source |
|---|---|---:|---:|---|---|
| Hard | One radio `selection`, five text subset labels | 2 | 2 | Moderate: prompt graph plus solution graph with A/B | q-71837, q-54293 |
| Unrated | Three text-valued checkbox fields I/II/III | 2 | 2 | Moderate: prompt graph only | q-54285, q-59732 |
| Easy | No source-rated template | 0 | 0 | Unresolved outside bounded package | None |
| Moderate | No source-rated template | 0 | 0 | Unresolved outside bounded package | None |

The hard templates share a question stem but have different equation structures, truth subsets, substitution sequences, and complete choice banks. They remain separate. Unrated checkbox layouts differ from radio selection and are not assigned a difficulty by this package. Their mathematics and Boolean banks are independently verified but they do not contribute to rated inventory.

The canonical example e-1702, line `y=2x-1`, shows I/III true and II false with points (0,-1), (2,3). It supplies context, not practice inventory. All graph bytes were inspected: q-71837 has intercepts (0,6), (2,0); q-54293 has (0,2), (4,0); q-54285 passes through (0,2), (4,4); q-59732 has (0,4), (4,0).

Source q-54293's Equation I substitution writes `-1(0)` for an equation with slope -2. The residual is unchanged at x=0, but the coefficient is inconsistent. Generated solutions correct it to `-2(0)` and record this correction. The source remains intact.

The supported band is hard, based on both source difficulty facts. Easy and moderate are bounded capability exceptions: this implementation has no rated templates or validated extension for those bands. This does not establish mathematical impossibility; new evidence reopens classification. Each exception retains the nominal five-question shortage.
