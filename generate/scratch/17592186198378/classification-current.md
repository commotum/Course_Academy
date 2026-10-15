# Current classification

Current source capture: `reference/replenishment/initial/kp.json`, database `math`, basis 2693, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. All 12 practice questions have one `selection` radio field with five mathematical choices. No practice template requires plots. The original classification at basis 1356 remains preserved.

| Difficulty | Current practice sources | Templates | Bank profiles | Generation support |
|---|---:|---:|---:|---|
| easy | 6 | 6 | 6 whole observed banks | Five frozen families; later cubic surface family classified and checked separately |
| moderate | 6 | 6 | 6 whole observed banks | Four frozen families; two later coefficient families classified and checked separately |
| hard | 0 | 2 authored | authored method-error banks | Existing validated polar and exponential unhinted families |

Original nine source templates and their complete banks remain covered by `template-extraction.md`, `source-cases.json` and `validate.py`. Current records are compared with those immutable sources before preparation. New sources do not change those frozen templates:

- q-161253: F=(z,xz,yz), r=(u,u²,v), no hint. Derive tangents and cross product (2u,-1,0), substitute (v,uv,u²v), obtain uv, then identify a=1,b=0 in auv+bu²v and sum to 1. Bank {-1,1,2,0,-2}, key 1. Separate moderate template and bank; not replayed by frozen sampler.
- q-161385: F=(-2x,-2y,-z), r=(u³,v³,uv), supplied cross product (-3v³,-3u³,9u²v²). Substitute, multiply three components, combine 6u³v³+6u³v³-9u³v³=3u³v³. Easy missing-integrand template. Bank {3u³v³,6u³v³,u²v²(3u+2v),2u²v²(uv+1),3u²v²(u+v)}, first correct. Separate template, not replayed by frozen sampler.
- q-161305: F=(x,y,xz), r=(u,v²,uv), no hint. Derive tangents and cross (-2v²,-u,2v), substitute (u,v²,u²v), dot to 2u²v²-3uv², identify a=2,b=-3 and sum -1. Bank {-1,1,-2,0,2}, first correct. Separate moderate template, not replayed by frozen sampler.

All 15 added source options are independently parsed and checked for one correct value, unique distractors and correct designation. The two later moderate banks have underdetermined error intent; no unverified distractor recipe is inferred. Their original values remain evidence. No source is changed.

Hard support is an authored difficulty claim grounded in the canonical unhinted route and the existing polar/exponential examples, as described in `template-extraction.md`. It is not a claim of observed hard sources. New generation uses only the already validated frozen families. The additional three source families do not need generated variants to meet this replenishment target.
