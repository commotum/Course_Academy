# Classification

Captured database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` retains the full wrapper and record. Six practice questions were inspected; the canonical example is curricular evidence, not a seventh practice question.

| Template | Source | Difficulty | Fields / bank | Plot requirement |
|---|---|---|---|---|
| asym_sign_zero | q-27638 | hard | selection radio; 5 text subsets | none: fixed graph in solution |
| asym_range_domain | q-27660 | absent | selection radio; 5 text subsets; correct absent | none: no original solution |
| domain_zero_range | q-103289 | hard | selection radio; 5 text subsets | none: fixed graph in solution |
| asym_point_identity | q-103295 | hard | selection radio; 5 text subsets | none: fixed graph in solution |
| two_identities_asym | q-28675 | hard | selection radio; 5 text subsets | none: fixed graph in solution |
| asym_identity_range | q-29608 | hard | selection radio; 5 text subsets | none: fixed graph in solution |

These are six distinct proposition/value templates and six observed complete banks. No practice source was discarded. `template-specs.json` lists every option and the full source prompt and solution. Textual choices denote entire subsets: their error operations omit true statements and/or include false statements. Their correctness follows the actual proposition truth vector; this is not a scalar distractor fit.

The raw unrated profile preserves absent difficulty, absent correct ref, and absent worked solution. The original MA lesson widget in `/home/jake/Developer/MA/DATA/Lessons/3558/Source/3558.json`, question 27660, confirms the five options and statement layout. It supplies no recoverable correct designation or solution. Normal completion derives **I only**: asymptotes are π/2+nπ; the proposed bounded range and excluded nπ domain are false. Its hard assignment and worked solution are explicitly authored, not recovered labels.

## Authored level scope

The lesson route is followed through `activity/first-step` and `step/next`: Introduction (zeros and asymptotes) → this KP canonical example (zeros/asymptotes/range) → periodicity tutorial → numerical periodicity sibling KP → oddness tutorial → numerical oddness sibling KP. The key prerequisite is Graphing Tangent and Cotangent (1493); Even and Odd Functions also precedes the owning topic. This generator never asks to evaluate a numerical tangent value, apply oddness to a supplied value, transform the tangent curve, or solve a trigonometric equation.

Easy is an authored three-claim classification of **zeros, asymptotes, range**, each a direct standard-graph property. Its 36 eligible catalog tuples each require those same three recognition decisions. Moderate is an authored three-claim classification of **domain, interval sign, least positive period**, requiring one global excluded set, one sign interval, and one repeated-distance judgement. Its 44 eligible tuples retain those same three decisions; no moderate instance can remove the sign or domain demand. At each level exactly one or two claims are true, preserving an unambiguous five-option subset response. Both levels are design claims grounded in the graph prerequisite and canonical example, not observed difficulty labels.

Hard defaults serve every observed source-shaped family plus a labeled extension of q-28675: **two periodic identities and one standard property**. The extension requires an arbitrary-integer coefficient judgement and subtraction of two familiar rational π shifts, followed by a direct property judgement. Coefficients are 1, 2, 3, 1/2; denominators are 2, 3, 4, 6; shift differences are π, 2π, π/2. Its 468 eligible tuples vary the truth vector, not merely the wording. Hard observed families retain their captured labels even where they contain direct facts. These observed demands are evidence, not a claim that every captured hard question is strictly more difficult than authored moderate. The missing-level authored catalogs are disjoint in actual displayed assessed information.

Meaningful variety is finite: 36 easy catalog tasks, 44 moderate catalog tasks, and 44 distinct normalized observed hard parameter tasks plus 468 authored hard tuples. Equivalent Unicode/TeX spellings do not add mathematical tasks. Actual counts and any fingerprint collisions appear in validation.json. Graph styles, seeds, option order, profile aliases and variable aliases do not inflate task counts. Finite catalogs are appropriate for this narrow property-recognition KP; there is no claim of infinite new skills.
