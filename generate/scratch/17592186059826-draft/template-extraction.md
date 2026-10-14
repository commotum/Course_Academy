# Four extraction stages

## 1. Specific source descriptions

q-102204 prints `The inequality $3 < x < 7$ can be expressed in interval notation as`. One radio key `selection`, five math intervals, a spaced comma and Unicode infinity. No rating, key or worked solution. Its unique derived correct interval is (3,7).

q-59294 prints `Which inequality corresponds to the interval $x ∈ (3, 4)$?`. One radio `selection`, four math double inequalities and a text `$x < 3$ or $x > 4$`. No rating, key or worked solution. Its unique derived answer is 3<x<4.

q-1256 prints `The inequality $-3<x<-1$ can be expressed in interval notation as`. Observed **easy**, one radio, all five math intervals with compact commas. Correct designation is (−3,−1). The full solution includes two notation bullets, prose naming both excluded negative endpoints, a displayed strict inequality, the open interval, and the more-formal membership with final period.

q-154704 uses the same compact prompt/solution backbone with −√2 and √2. Observed **easy**, one radio, correct designation (−√2,√2). The bank uses TeX `-\infty `, not Unicode infinity, for its omitted-lower-bound distractor. Its symmetric root endpoints require no root calculation. All four originals have no answer feedback, which remains absent in output.

`source.json` retains every original string and record. Decoded source bytes contain no adjacent backslashes or unexpected C0 controls; JSON-serialized doubled escapes are not raw TeX defects. Canonical e-10785 has exact extra spaces inside/around its colored `<` masks and a trailing space in endpoint-exclusion prose; these are retained in the parameterized canonical solution mask. No presentation or mathematical source repair is required.

## 2. Generalized stable backbone

Given ordered finite exact endpoints a<b and one variable v, convert a<v<b into (a,b), or v∈(a,b) into a<v<b. Both endpoints remain excluded, every endpoint reference changes together, and no calculation of endpoint values occurs. Supplied/requested roles, strict relations, finite bounded interval and radio response contract remain fixed because they are the assessed KP. Source option order and variable name are incidental. Endpoint signs/form/value may vary within explicitly documented catalogs without changing the method.

Separate masks preserve spaced versus compact prompt layouts and the membership prompt. Compact integer/root sources share their complete operative solution mask; different bank profiles do not become additional templates. The spaced original has no practice solution: normal output supplies the complete compact originals' three-stage source mask, explicitly authored completion rather than observed q-102204 solution fidelity. Membership likewise has no practice solution: normal output supplies the complete two-stage canonical e-10785 mask.

## 3. Complete original bank mapping

Every listed row belongs to `selection`. A `math` answer has delimiter-free value; the disjunction is `text` and retains its inline dollar delimiters. All complete banks are built from the listed operations together.

| Profile/source | Raw option | Complete parameterized value/operation | Designation evidence |
|---|---|---|---|
| spaced_ray / q-102204 | `(3, 7)` | `(a, b)` | key missing; independently derived correct |
| | `(- ∞, 7)` | `(- ∞, b)`; omit lower bound | key missing; derived wrong |
| | `[3, 7]` | `[a, b]`; include both endpoints | key missing; derived wrong |
| | `(3, 7]` | `(a, b]`; include right endpoint | key missing; derived wrong |
| | `[3, 7)` | `[a, b)`; include left endpoint | key missing; derived wrong |
| membership / q-59294 | `3 \le x < 4` | `a \le v < b` | key missing; derived wrong |
| | `3 < x < 4` | `a < v < b` | key missing; independently derived correct |
| | `3 < x \le 4` | `a < v \le b` | key missing; derived wrong |
| | `$x < 3$ or $x > 4$` | `$v < a$ or $v > b$`; outside disjunction | key missing; derived wrong |
| | `3 \le x \le 4` | `a \le v \le b` | key missing; derived wrong |
| compact_reflection / q-1256 | `[-3,-1]` | `[a,b]` | observed wrong |
| | `(-3,-1)` | `(a,b)` | observed correct |
| | `(1,3)` | `(-b,-a)`; reflect both endpoint signs/order | observed wrong |
| | `[-3,-1)` | `[a,b)` | observed wrong |
| | `(-3,-1]` | `(a,b]` | observed wrong |
| compact_ray / q-154704 | `(-\sqrt{2},\sqrt{2}]` | `(a,b]` | observed wrong |
| | `(-\infty ,\sqrt{2})` | `(-\infty ,b)` | observed wrong |
| | `[-\sqrt{2},\sqrt{2}]` | `[a,b]` | observed wrong |
| | `(-\sqrt{2},\sqrt{2})` | `(a,b)` | observed correct |
| | `[-\sqrt{2},\sqrt{2})` | `[a,b)` | observed wrong |

Bank operations directly reproduce full represented sets. The reflected option generalizes the complete original interval via x↦−x; it is not an arbitrary numerical fit. Interpretation labels describe displayed transformations rather than claiming recovered authoring code. Reflection is ineligible when a+b=0; this collision is rejected as a whole instance. Other banks have five distinct sets whenever finite a<b. The generator checks every pair, including wrong-wrong pairs, under the actual represented-set response criterion.

## 4. Reusable masks and slots

Slots are **complete** endpoint components a,b and variable v∈{x,y,t,z}. Sampling policies are in classification; aliases canonicalize exact rational spelling and never add task counts. Endpoint values affect prompt, all five answers, endpoint prose, every display row and final membership. Negative components render with a single leading minus; roots render with `\sqrt{n}` and exact fractions with `\frac{n}{d}`. No short global text replacement is used.

Fixed compact solution backbone: the exact source introductory sentence; parentheses/brackets bullets with intervening blank lines; `Our inequality contains only "less than" symbols. So, the endpoints $a$ and $b$ are *not* included. `; displayed `a\,\,<\,\,v\,\,<\,\,b`; therefore sentence; displayed `(a,b)`; more-formal sentence; displayed `v\in (a,b).`. These distinct inequality→interval→membership stage roles remain present at changed parameters. Full normal solutions for q-1256/q-154704 are byte-exact at anchors, and preserve the same full prose/masks under sampling.

Fixed membership solution backbone: the exact basis-2275 canonical bullets and endpoint-exclusion prose; colored membership row; therefore sentence; colored strict double-inequality row. Canonical whitespace and row structure are retained. No practice solution existed for q-59294, so its normal completion is separately authored from this canonical mask.

Public raw profiles `raw_spaced_ray`, `raw_membership`, `raw_compact_reflection`, `raw_compact_ray` reuse the same parameterized masks and recipes. Raw omission parity is checked per original. Raw complete sources keep observed easy/solution/key; raw incomplete sources omit absent attributes rather than invent them. All raw profiles carry author metadata `evidence_only=true`, `eligible_for_learning=false`. Normal profiles enrich only missing attributes and retain complete original solutions unchanged. Generated/field-owned UUIDs are regenerated from actual displayed content; source DB IDs and MA IDs remain provenance, not identities reused for changed practice.

Fidelity denominator: four prompts, four five-option banks (20 values,16 wrong options), two available correct refs (two missing), two available practice solutions (two missing), two available ratings (two missing), and one canonical solution. Missing values never count as recovered matches. Independent inventory is three exact records checked separately; it does not inflate any original denominator. No original prompts/options/solutions contain plots, so plot extraction/generation is unnecessary.
