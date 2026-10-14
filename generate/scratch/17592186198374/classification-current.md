# Current classification

The source snapshot in `reference/initial/` is math basis 2287, lineage
`01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. It supersedes the difficulty and completeness
claims in the historical basis-1356 classification. All 12 current practice
questions are hard. All use five-value scalar radio fields; q-160433 has a
second captured legacy field without a correct reference and is excluded as a
whole from usable inventory. No source or learner record is repaired here.

| Sources | Backbone / template | Banks | Plot requirement |
|---|---|---:|---|
| q-160433 | squared linear numerator / linear denominator | 2 | moderate |
| q-160896 | shifted affine factor times squared shear | 1 | moderate |
| q-160901 | coordinate times sine of shear | 1 | moderate |
| q-160904, q-160895 | linear factor times exponential of independent linear form | 2 | moderate |
| q-160933 | affine form times exponential of its square | 1 | moderate |
| q-160935 | difference of squares times cosine of squared sum | 1 | moderate |
| q-160937 | linear numerator over coordinate denominator | 1 | moderate |
| q-160903 | factored difference of squares / squared difference | 1 | moderate |
| q-160938 | common-coordinate factor extracted from two-term polynomial | 1 | moderate |
| q-160906 | scaled coordinate times cosine of shear | 1 | moderate |
| q-160902 | factor a three-term quadratic into two mixed linear forms | 1 | moderate |

There are 11 Markdown/value backbones and 13 source field banks, with 65 choices
and 12 existing correct references. Each source uses the same five broad stages:
infer a map from the integrand (factor first when necessary), map four vertices
to a rectangle, compute the map determinant, take its reciprocal, separate and
evaluate two definite integrals. The distinct factoring and primitive operations
remain separate templates. `extraction-current.json` retains every source's
transform, bounds, exact integral, every field-owned choice and complete bank.

Easy remains an authored, validated canonical-example extension: the visible
polynomial/shear `(ax+by)y²`, four mapped vertices, constant Jacobian, and two
power primitives. The canonical question remains an example, never inventory.
Hard retains the validated sampler families, now including shifted polynomial
at its explicit current source rating. The sampler does not claim to cover the
new source families or q-160895's additional bank/transform domain.

Moderate is unsupported by this version. The previous moderate family was based
on unrated q-160896; its new hard rating is affirmative evidence against reusing
that provisional assignment. No different intermediate family is calibrated by
the present sources. This is a bounded package capability exception, reopenable
with new evidence, rather than a claim that moderate questions are impossible.
Its nominal five-question shortage remains explicit in `capabilities.json`.
