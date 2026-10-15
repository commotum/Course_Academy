# Templates and domain-size slots

Source-specific coordinates, choices, keys, Markdown and complete solution strings remain in `source.json`. `choice-recipes.json` maps every original answer identity/value to its field/profile and full mathematical recipe. The following are observed source instances, followed by the bounded same-method policy.

| Source | Supplied surface | Original domain | Required calculation |
|---|---|---|---|
| q-105920 | `(2u-v,3u+2,u+2v)` | `[0,1] × [-1,1]` | cross `(6,-5,3)`, norm `sqrt(70)`, rectangle area 2 |
| q-109710 | `(u+v,2-3u,1+u-v)` | `[0,2] × [-1,1]` | cross `(3,2,3)`, norm `sqrt(22)`, rectangle area 4 |
| q-109712 | `(u,v²,2v³/3)` | `[0,1] × [0,sqrt(3)]` | cross `(0,-2v²,2v)`, norm `2v sqrt(v²+1)`, integrate u then substitute `w=v²+1`, endpoints 1,4 |
| q-109761 | `(u²,uv,v²/2)` | `[0,1] × [1,2]` | cross `(v²,-2uv,2u²)`, norm `v²+2u²`, integrate u then v |
| q-105922 | `(-u+v,u-2v,3v)` | `u²+v² ≤ 4` | cross `(3,3,1)`, norm `sqrt(19)`, disk area `4pi` |
| q-109779 | `(u,v,u-v)` | `u²+v² ≤ 9` | cross `(-1,1,1)`, norm `sqrt(3)`, disk area `9pi` |
| q-110252 | `(u,v,1-2u+5v)` | `u²+v² ≤ 2` | cross `(2,-5,1)`, norm `sqrt(30)`, disk area `2pi` |
| q-110551 | `(u-v,u+2v,2u-v)` | `u²+v² ≤ 1` | cross `(-5,-1,3)`, norm `sqrt(35)`, disk area `pi` |

Each asks for a single exact scalar surface area in a five-choice radio field, `selection`. The ordered stages are surface-area formula; coordinate-to-vector conversion where supplied; formal partial operands; evaluated partials; determinant with signed minors; cross; norm reduction; explicit domain; integral or constant metric times domain area; final arithmetic. The substitution family also retains the nonnegative-v justification, factorization, inner integral separation, explicit w substitution, primitive, endpoint radicals and arithmetic. The quadratic family retains perfect-square norm reduction, inner primitive, evaluated inner integral, outer primitive and endpoint arithmetic. Normal variants reuse the source's prose and all preceding calculus stages, then parameterize the domain and every dependent area stage. Original source notation is reproduced byte-for-byte at its anchor. Changed parameter output retains the same stages; coefficient notation and the equivalent endpoint arithmetic can differ.

The domain slot is an integer `t` in **1..6**. Each profile is selected as a complete unit before sampling t. No other random slot exists. Surfaces stay fixed to isolate domain variation and retain the source derivative/cofactor workload; this is a deliberately narrow implementation policy, not a mathematical claim that coefficients cannot vary.

* Rectangular affine profiles: multiply the original upper u endpoint by t; keep u lower zero and v bounds -1,1. Area and every bank value scale by t.
* Separable cubic profile: upper u endpoint becomes t, with v domain unchanged. The inner integral is t; it is carried through the substitution integral, primitive and every endpoint row. Area and the complete bank scale by t. No change of substitution or branch is introduced.
* Homogeneous quadratic profile: domain becomes `[0,t] × [t,2t]`. Metric is homogeneous of degree two and parameter-domain area scales quadratically, so the surface area and complete bank scale by `t⁴`. Both integration limits, inner evaluation and outer primitive change together. The primitive is `t v³/3 + 2t³v/3`. The positive domain avoids sign and injectivity issues.
* Disk profiles: squared radius becomes original squared radius times t. The displayed radius becomes its positive square root, while metric stays constant. Area and complete bank scale by t. Some normal radii are irrational, as already observed in q-110252.

The target is always the whole supplied surface patch. There is no eligible cell, edge, component or other target-position slot for this response demand. The changed-domain test holds the entire supplied surface fixed at t=1 and t=2 and independently reads the new prompt, domain, solution and answer key. Coefficients, coordinate names, parameter names, choice ordering, field layout, response type, integral order and source profile are fixed. Changing these alone cannot increase capacity.

All fields use the existing field-owned answer model with delimiter-free math values. For every source answer a, the full transport recipe is `a * A(t)/A(1)`; this reproduces each complete original object at t=1. Its error interpretation is unresolved and the extension is explicitly authored. Distinctness and positive answer designation are independently checked at all six values for every profile, with all five options submitted through the actual learner grader. No mixed profile or inferred learner feedback is emitted.

Both supported levels have 24 mathematical tasks under this bound, including their four original tasks. Semantic inventory matching discards the t=1 copies; only a changed mathematical surface domain can yield a new task. The generator fails a request beyond capacity rather than duplicating by seed or option order. Easy remains unsupported with its nominal five-question reserve gap explicit.

Plot extraction/generation: no assets occur in any of the eight question/choice/solution records. The rating is none and the asset hash list is empty.
