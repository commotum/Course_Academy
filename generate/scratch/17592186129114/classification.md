# Classification: identifying matrices in row echelon form

Live math basis 2350; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All 14 practice sources captured together in source.json.

Easy: two prompt templates (select echelon / select **not** echelon), 13 complete source profiles. Each has three checkbox fields A/B/C, each with field-owned text false/true. One Boolean-bank profile per field; no invented distractors. The same definitions, three ordered matrix inspections, and final subset conclusion are retained. Numbered definitions and witness wording remain source layout profiles. Plot rating: none; ordinary matrices are LaTeX, not plots.

Unclassified: q-42369 is a single selection radio with five subset choices, no correct answer, no worked solution, and no difficulty. It cannot support replay or gradable generation; preserve it without modification.

Moderate and hard: no source-backed templates or validated workload distinction. These are bounded package exceptions; they are not a proof that future authoring is impossible. New source evidence reopens classification. Reserves remain explicitly unfilled.

| Source | DB ID | Polarity | Matrix sizes | Leading columns (0-based; null = zero row) | Selected fields |
|---|---:|---|---|---|---|
|q-42024|17592186129773|in|[(3, 4), (3, 4), (3, 6)]|[[0, None, 2], [1, 2, None], [0, 2, 4]]|['B', 'C']|
|q-129214|17592186262985|in|[(5, 4), (4, 4), (3, 4)]|[[0, 1, 2, 3, None], [1, 2, 3, None], [1, 2, 3]]|['A', 'B', 'C']|
|q-129220|17592186262990|not|[(3, 5), (4, 3), (3, 3)]|[[None, 1, 3], [0, 1, 2, None], [0, 1, 2]]|['A']|
|q-129225|17592186262993|not|[(3, 4), (5, 4), (4, 5)]|[[1, 3, 3], [0, 1, None, 2, 3], [1, 3, 4, 4]]|['A', 'B', 'C']|
|q-72489|17592186339126|not|[(3, 4), (3, 5), (5, 3)]|[[0, 2, 3], [0, None, 2], [None, 2, 1, 0, None]]|['B', 'C']|
|q-72498|17592186339127|in|[(4, 3), (3, 4), (3, 4)]|[[0, 1, 1, 2], [1, 2, 3], [0, None, 1]]|['B']|
|q-129213|17592186400408|in|[(4, 4), (3, 4), (4, 4)]|[[0, 1, 2, None], [1, 2, 3], [0, None, 1, 3]]|['A', 'B']|
|q-129217|17592186400415|in|[(4, 5), (3, 3), (4, 4)]|[[0, 2, 4, 4], [0, 2, None], [1, 2, 3, None]]|['B', 'C']|
|q-129222|17592186400422|not|[(4, 3), (5, 3), (3, 3)]|[[0, 1, 2, 2], [0, 1, 2, 2, None], [0, 2, None]]|['A', 'B']|
|q-42366|17592186402796|in|[(4, 4), (5, 4), (4, 4)]|[[0, 1, None, 3], [3, 2, 1, 0, None], [0, 1, 3, None]]|['C']|
|q-72491|17592186403578|not|[(5, 4), (3, 5), (4, 4)]|[[0, 2, 3, 2, None], [0, 2, 4], [0, 1, 1, 2]]|['A', 'C']|
|q-72492|17592186403585|not|[(3, 3), (4, 4), (3, 3)]|[[0, 1, None], [0, 1, 3, None], [1, 1, 2]]|['C']|
|q-42005|17592186413824|in|[(4, 4), (5, 4), (4, 4)]|[[0, 1, 1, 2], [0, 0, 1, 2, None], [0, 1, 2, 3]]|['C']|
