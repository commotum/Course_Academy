# Classification — Calculating Flux Across Rectangles

Database math, basis 2281, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. All ten practice questions have one radio field named selection, five mathematical choices, one key, and a full worked solution. Canonical e-9565 is evidence only. No generator existed and no .generated handoff existed at initial read.

| Source | Observed band | Component functions P; Q | Rectangle [a,b] × [c,d] | Plot need | Profile |
|---|---|---|---|---|---|
| q-126820 | hard | `2*x**2*y + exp(y)`; `2*x*y**2 + exp(x)` | (-1, 2, 0, 1) | none (fixed asset) | q-126820 |
| q-126821 | moderate | `-x**2 + cos(pi*y)`; `2*y + sin(pi*x)` | (0, 1, 0, 1) | none (fixed asset) | q-126821 |
| q-127303 | moderate | `2*x + sin(y)`; `x**5 - 3*y` | (-1, 1, -1, 1) | none (fixed asset) | q-127303 |
| q-127308 | moderate | `-3*x**3 + cos(y)`; `-4*x*y**3 + x*exp(x)` | (-1, 1, 0, 1) | none (fixed asset) | q-127308 |
| q-127322 | hard | `x + y**(1/3)`; `-3*x**2*y**2 + sin(x)` | (0, 2, 0, 1) | none (fixed asset) | q-127322 |
| q-127324 | hard | `-x**2*y + sin(2*y)`; `2*x*y + cos(2*x)` | (0, 1, -1, 0) | none (fixed asset) | q-127324 |
| q-127305 | moderate | `-4*x*y + exp(y)`; `2*x*y + cos(x)` | (-1, 1, -1, 0) | none (fixed asset) | q-127305 |
| q-127337 | hard | `-x + y**7`; `x*y**2 + exp(3*x)` | (-1, 0, -1, 1) | none (fixed asset) | q-127337 |
| q-127326 | hard | `-4*x*y + y*exp(y)`; `-4*x*y**3 + sin(pi*x)` | (0, 1, -1, 1) | none (fixed asset) | q-127326 |
| q-127307 | moderate | `8*x*y**3 + y**2`; `2*y**2 + exp(x)` | (-1, 0, 0, 1) | none (fixed asset) | q-127307 |

Each row remains a separate source template, retaining its prompt format (inequality square/rectangle or vertices) and derivative/integration structure. Moderate has five templates; hard has five, of which q-127322 is replay only. Every template has one complete observed bank. There are no blank or mixed fields.

Easy is unobserved and unsupported in this bounded package. Constant divergence is already rated moderate in the sources, so relabeling it easy would not establish a distinct supported workload. This does not prove that an easy design is mathematically impossible. New sources or a separately justified design reopen classification.

Source exceptions: q-127322 uses cuberoot(y) at y=0 while its stated Green theorem assumes C1 on an open neighborhood of D. The flux value agrees with direct edge integration but the displayed sufficient hypothesis fails; retain source unchanged and exclude new practice from this family. Source choice values use valid single-backslash TeX; JSON/EDN serialization escapes are not content errors. Generated choices use canonical SymPy TeX.

Plots inspected at source resolution/contact sheet: light-blue rectangle interior, thin orange boundary, black x/y axes with arrows, endpoint ticks and numeric labels. No vector arrows or field-dependent plot content. Rectangle positions and bounds agree with the ten source prompts. Fixed geometry permits exact asset reuse. Plot rating is none for this scaling policy; changing bounds would require a renderer and is deliberately outside this package.
