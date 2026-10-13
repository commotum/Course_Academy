# Four extraction stages

## 1. Specific source descriptions

Complete original evidence is source.json; source-cases.json maps every original to its public parameterized recipe. The detailed component inventory below preserves all prompt/solution strings, complete ordered banks, correct presence and actual source difficulty. q-7809 is F=[3,5,2,7], 1×4. q-125543 is Y=[sqrt(2)], 1×1; q-7813 K=[0], 1×1. q-319329 S is the column [2,−sqrt(7),0,4], 4×1. q-319338 E is [2/3,−sqrt(3),5,0,−4], 5×1. q-7810 G=[5,−9,2] is 3×1 in bmatrix; q-7812 J=[3] is a literal singleton bracket.

## 2. Shared mathematical pattern

Read the rectangular array. Count horizontal rows, then vertical columns, and give the ordered pair. Entries can be negative, zero, rational or radical without altering dimensions. A singleton has both counts one. No scalar calculations are performed. The four source masks preserve their punctuation, placeholders, layouts and two-sentence count/conclusion sequence when present.

## 3. Components and complete banks

Let (r,c) denote the displayed dimensions and n=max(r,c), v the integer singleton entry. Each complete bank is selected before entries/shapes are sampled. No first-valid choice pool is used.

| Profile | Complete ordered bank | Interpretation |
|---|---|---|
| row_observed | (0,n),(n,0),(n,1),(1,n),(n−1,2n−1) | historical affine replay; final error intent unresolved |
| singleton_root_observed | (2,0),(0,2),(1,2),(1,0),(1,1) | historical fixed singleton count bank |
| singleton_zero_observed | (0,1),(0,0),(1,0),(1,1),(2,1) | historical fixed singleton count bank |
| legacy_column_observed | (1,n),(n,1),(1,1),(n,n),(n+2,n−1) | historical affine replay; final intent unresolved |
| legacy_singleton_observed | (v,v),(0,1),(1,1),(1,0),(0,0) | historical entry-as-count plus count errors |
| blank_observed | field-2=c, field-1=r | independent scalar blanks |
| blank_plural_observed | field-2=c, field-1=r | same values; historical “columns” grammar |

Historical legacy choices retain source `\cdot` spelling; other radios retain `\times`. These are ordered dimension labels. Correct refs point into owned banks when present originally; source absences remain absent. See source-components.json for the full one-to-one original answer mapping.

## 4. Reusable masks and extensions

Name is a complete uppercase-letter slot; each scalar entry is a complete bounded TeX slot; rows/columns are determined solely by the rectangular array separators. Preserve `aligned_radio`, `double_blank`, `legacy_column`, `legacy_singleton` prompt masks and blank collection order. Normal prose uses the source “has … row(s) and … column(s). So/Therefore, its dimensions are …” sequence, correct grammar and actual changed name/counts. Public evidence profiles preserve original prose exactly where present and apply raw attribute-presence masks where absent. No literal source payload or answer lookup table is returned.

Authored normal radio bank for n>1: (r,c), reversed (c,r), (n,n), count the long axis one too low, count it one too high. These are direct count/order errors. Singleton normal bank: (1,1),(0,1),(1,0),(0,0),(2,2), from missing/both-missing or double-counted axes. Each whole bank must have exactly five unequal ordered pairs and exactly one true pair; reject a collision as a whole. Double blanks retain exact scalar shapes and have no distractors. Native radio grading selects identities, so independent ordered-pair checks are necessary and included.

Normal defaults sample all eligible source-shaped masks. Legacy singleton is eligible only at easy; the remaining three masks serve all levels. Authored level bounds and long-layout entry guards are explicit as well as sampled. Content identity hashes version, actual prompt, actual solution, full displayed bank, actual difficulty/omissions, and field shape, ignoring choice order. Mathematical fingerprint hashes only ordered dimensions. Changing seed at fixed parameters/profile/template leaves identity unchanged.
