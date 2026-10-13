# Classification

Snapshot: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Context captures: `generate/runs/current/topics/17592186048185.json` and `generate/runs/current/lessons/17592186048185.json`. All 10 practice questions are included; the canonical example is separate evidence. No unrated or malformed fields occur. All answer fields are five-option `radio`, key `selection`, with scalar exact math values. No source question, option or solution requires a plot.

| Level | Practice questions | Structural recipes | Complete observed banks | Plot rating |
|---|---:|---:|---:|---|
| easy | 0 | 0 observed; 1 authored | 0 | none |
| moderate | 5 | 5 | 5 | none |
| hard | 5 | 5 | 5 | none |

A structural recipe includes its polynomial surface/field and solution sequence. These are not ten new skills: all assess the same scalar flux evaluation. Four moderate recipes supply the fundamental vector product; q-162593 is an observed unhinted moderate recipe. Hard recipes include tangent derivatives and cross-product determinants. Affine and curved surfaces, one-variable and two-variable integrands, and separated versus iterated evaluation sequences are retained. Numerical changes are variants, never additional templates.

| Source | Level | Surface structure | Field structure | Solution route | Profile |
| q-160845 | hard | `u-1 ; 2*v ; 2-3*u-2*v` | `3*x+y+z ; y/2-2 ; -3*x-z` | derive normal; separable_v final calculation | observed:q-160845 |
| q-160886 | moderate | `2*u-1 ; u*v ; 3*v` | `2*x ; x*z/3-2*y ; 2*z` | supplied normal; terms final calculation | observed:q-160886 |
| q-161260 | moderate | `u-v ; 2 ; v**2` | `y+z ; x+z ; 1` | supplied normal; terms final calculation | observed:q-161260 |
| q-161262 | moderate | `3*u*v**2 ; u-v ; 2` | `x**2 ; x+y ; z` | supplied normal; terms final calculation | observed:q-161262 |
| q-161263 | hard | `u**2 ; v ; u*v` | `3 ; z ; y` | derive normal; none final calculation | observed:q-161263 |
| q-161273 | hard | `u-v ; v-u ; -2*u*v` | `x ; 0 ; y` | derive normal; terms final calculation | observed:q-161273 |
| q-161278 | hard | `u+v ; v-u ; -v` | `-x-z ; x-y ; -z` | derive normal; terms final calculation | observed:q-161278 |
| q-161283 | hard | `u*v**2 ; -1 ; 1-2*u` | `z ; 2 ; -3*x*y` | derive normal; separable_uv final calculation | observed:q-161283 |
| q-161258 | moderate | `3*u*v ; u ; -v` | `3*x ; -y**2 ; 2` | supplied normal; terms final calculation | observed:q-161258 |
| q-162593 | moderate | `-v ; -u ; u**2` | `3*z ; -2*x ; -y` | derive normal; none final calculation | observed:q-162593 |

## Lesson scope and authored easy level

The lesson route is reconstructed from `activity/first-step` and `step/next`: step 17592186199281 (Introduction) → 17592186199280 (Expressing Flux Through a Surface as a Double Integral, KP17592186198378) → 17592186199283 (this KP). Pull collection order would put the examples in the wrong order. The tutorial derives cancellation of the normalized surface normal and surface-area Jacobian. The prerequisite operations visible in that derivation and canonical example are partial derivatives, vector cross and dot products, coordinate substitution, and polynomial rectangular double integrals. The capture does not supply a separate prerequisite-title edge list; no unseen prerequisite list is claimed.

Canonical e-12358 uses affine geometry `r=(1+2u+v,u+v,u-v)` and cyclic field `F=(z,x,y)`, producing `5u+6v+3`. The authored easy template uses that same geometry and field, supplies `r_u cross r_v=(-2,3,1)` as the observed hinted moderate questions do, and asks for the **evaluated scalar flux**, so it remains distinct from the sibling KP's integrand-only response. Easy demands substitution, one short dot product and two linear antiderivatives. The small rational rectangle varies independently at the same demand; there is no difficulty progression or new surface method. Easy is a design claim, not an observed source label.

Moderate and hard retain source labels and geometry/field structures. Source bound values and signed features are all accepted. Authored sampling uses short integer rectangular domains. Nonnegative v is retained for q-161260/q-161263; nonnegative u,v for q-161273/q-161283; q-161262 retains u_max=0 and v_min=0. These restrictions avoid creating extra folded geometry through sampling. No triangles, nonrectangular domains, orientation decisions, divergence theorem, Cartesian conversion, numerical integration, trig fields or other KP branches are added.

## Parent variety extension

Normal sampling uses translated integer rectangles: u lower bound −3..2 and v lower bound −2..2, independently chosen widths1..4. This offers480 affine easy domains rather than54, with the same two linear antiderivatives and short exact arithmetic. Families already restricted to nonnegative parameters keep lower bounds0..2; q-161262 retains u_max=v_min=0 with widths1..4. Geometry, field, orientation, question demand and every source replay remain the same. These are authored sampling bounds, not new observed templates or a within-level progression.
