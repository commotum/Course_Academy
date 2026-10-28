# Step 3 — classification

Frozen source: database math, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` retains the entire unchanged capture wrapper and record. No DB reads or writes were made. All eight practice questions were inspected; the canonical example is context, not counted as a practice original.

Seven questions have observed easy labels; one is unrated. Every source has a single radio field, `selection`, with five mathematical integrand fragments. Seven have a correct ref and a worked solution. The unrated q-161323 omits difficulty, worked solution and correct ref; public raw replay preserves these omissions individually, rather than replacing them with nulls or empty objects.

| Template | Source | Observed rating | Scalar function / surface | Solution structure | Plot rating |
|---|---|---|---|---|---|
| quadratic_xy | q-161106 | easy | 2xy / x²+y² | formal partials, substituted metric, integrand, repeated integral | none |
| plane_xz | q-161323 | absent | −3xz / √2x+√2y | absent; malformed AAAAAAA missing integrand | none |
| plane_xy_z2 | q-161319 | easy | xyz² / y−2x | formal partials, substituted metric, factored integrand, repeated integral | none |
| plane_xyz | q-161321 | easy | √2xyz / −√2x−√2y | formal partials, metric, substituted product, distributed product, repeated integral | none |
| quadratic_x2_z2 | q-161325 | easy | x²z² / −x²+2y² | formal partials, metric, substituted square, expanded repeated integrand | none |
| plane_x2yz | q-161314 | easy | x²yz / −x+y | formal partials, metric, substituted product, expanded repeated integrand | none |
| quadratic_x2y2z | q-161320 | easy | x²y²z / −x²−y² | formal partials, metric, substituted product, expanded repeated integrand | none |
| plane_y | q-161326 | easy | √2y / −√2x−y | formal partials, metric, constant metric product, repeated integral | none |

The eight masks and eight complete historical banks remain distinct. Each raw bank is evidence-only: variable-exponent/coefficient errors in several banks do not identify a defensible general method. q-161321, q-161325 and q-161314 also contain nonreal distractors over part of the given rectangle. Normal generation uses a separate complete bank from five actual differential-factor operations and covers all eight source-shaped families, including an explicitly authored completion of plane_xz. It does not silently promote raw malformed/opaque evidence.

Missing moderate/hard labels are authored, not recovered. Follow `:activity/first-step` 17592186106886 and `:step/next` to obtain Introduction → Express Surface Integrals as Repeated Integrals → Evaluating Surface Integrals → Evaluating Surface Integrals Using Polar Coordinates. The Introduction gives the general scalar formula on a Cartesian graph; prerequisites are Surface Integrals Over Parametric Surfaces and Areas of Surfaces. This places the boundary at constructing f(x,y,g)√(1+g_x²+g_y²); evaluation and polar domains belong to the next KPs.

Authored moderate has a nonzero coupled quadratic graph ax²+bxy+cy², two two-term partials, and one z-dependent monomial. Authored hard keeps that same graph and has two nonzero z-dependent terms, one linear and one squared. These are bounded extra substitution/product demands inside the general formula, not new integration skills. xz versus yz placements are unordered variations with identical workload inside each level. No level introduces a progression or numerical integration.
