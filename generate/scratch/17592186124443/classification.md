# Classification (step 3)

Snapshot: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; source wrapper copied unchanged into `source.json`.

There are nine practice sources: four easy, four moderate, one unrated. All use one five-choice radio except polynomial q-35990 (duplicate legacy radio plus authoritative radio) and contextual q-168115 (two scalar blanks). Nine distinct prompt/solution families; no source family is silently pooled into another solution chain. Source IDs and actual source params are in `source-cases.json`.

| Family | Observed level | Assessment and source stages | Bank/profile |
|---|---|---|---|
| polynomial | easy | quadratic plus cross term and linear y; held-coordinate zero terms; two reduced components; point substitution; basis-vector output | original complete bank, including duplicate legacy field in raw replay |
| root | easy | x² times shifted square root; two formal partials; symbolic tuple; direct perfect-square substitution; collected tuple | raw historical scalar bank; separately authored method bank |
| log_cos | easy | ln(xy)+cos(y²); inner-product chain and zero y-only contribution for x; inner-power chain for y; reduced basis components | original complete operation bank |
| sin_log | easy | sin(xy)+x² ln y; chain on xy; held-coordinate power derivative and reciprocal; extra reciprocal reduction row | original complete operation bank |
| atan_product | moderate | a x atan y; held-coordinate components; symbolic tuple; substituted tuple; familiar angle and denominator evaluation; collected tuple | raw scalar bank, authored omitted-scale/swap/sign bank |
| radial_log | moderate | log(x²+y²); two formal chain partials; tuple; common factor; rational point substituted; denominator reduced; scalar multiplied; collected tuple | raw scalar bank, authored chain omission/factor/swap/sign bank |
| atan_ratio | moderate | atan(y/x); chain factors for both coordinates; common-denominator simplification and cancellation; reduced basis vector | original complete operation bank |
| components | moderate | referenced earlier supplied expansion partials; vector assembly without normalization; two component blanks | raw contextual evidence, authored standalone supplied-partial completion |
| quotient | unrated | linear numerator / linear denominator; source has prompt and radio only | original full quotient operation bank; normal moderate inference adds formal component solution |

No source practice prompt/option/solution contains a plot. Plot rating **none** for all templates; standalone TeX is not a plot. Lesson images outside this calculation KP do not alter this rating.

The authoritative local lesson capture `/home/jake/Developer/MA/DATA/Lessons/1934/Source/1934.json` shows q-35990 is a single five-choice widget. The duplicate EDB field is retained only in public raw replay; normal questions use its complete authoritative field. q-35988 lacks original correct reference, difficulty and solution. Raw replay preserves those omissions; correct gradient is independently derived, and the original bank's first expression is mathematically correct. Its missing designation is never counted matched.

q-168115 lacks the scalar fluid expansion expression and preceding part 2. Raw replay retains its referenced data and cannot certify missing context; normal practice explicitly supplies the two scalar partials, so no fluid-divergence computation is invented. q-127650 (actual ID in cases) supplies h but source solution names f. Raw evidence is retained; normal solution names h consistently. Neither decoded source text nor its JSON-serialized display provides evidence of doubled command escapes; decoded ord-92 pairs occur only for intentional aligned row separators.
