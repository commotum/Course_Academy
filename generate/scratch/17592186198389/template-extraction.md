# Template extraction

Database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Raw source.json is an unchanged copy of the captured wrapper.

## Stage 1: Specific observed descriptions

The complete per-question fields, coefficients, graph and bounds are in classification.md and raw source.json. Every field uses one radio `selection`, five whole polynomial expressions in u,v, with no learner distractor diagnoses. Bounds can include zero and negative endpoints. q-160887, q-161360, q-161359, q-161377 and q-161379 use quadratic products or powers; other fields are affine. Every graph is a homogeneous plane, so tangent normals are constant. Field subtraction signs, nested squares and implicit coordinate products are consequential. The source dot product can cancel whole coordinate terms.

All eight display stages are preserved: (1) general parametrized flux equality, (2) r=<u,v,g>, (3) rectangle D, (4) partial derivatives and both tangents, (5) determinant, three signed minors and cross product, (6) component substitution and optional collection, (7) vector dot, scalar products, optional distributed sum, final integrand, (8) surface integral, domain integral, repeated integral. Source q-161379 skips the expanded dot row; q-161360, q-161358, q-161359, q-161377 and q-161379 skip a redundant collected field row. All source inter-display prose is retained, including the common tangent/cross/substitution/dot/repeated-integral sentences. The source `8u-4v+-4u+2v+4u` spelling is normalized without changing its sum. q-161377 retains its nested graph squares in the distributed row, so the square cancellations remain visible rather than being prematurely expanded.

## Stage 2: Shared mathematical pattern

Given an explicit Cartesian graph and vector field on a rectangle, use the stated coordinate parametrization to derive tangents, their ordered cross product, substitute every field component, take the dot product, and fill its polynomial into an already displayed repeated integral. The field is a missing complete integrand, not the integral value. The template carries the eight source stages and one fixed solution independent of a chosen wrong option.

## Stage 3: Components and complete banks

The following maps account for every captured option and both q-161360 fields. Expressions are symbolic polynomial patterns with explicit Add/Mul/Pow component trees, not empirical ratios to the correct answer. The whole-field scale s is part of the printed F. Their source plane slopes are enforced; s covariance defines a limited structural expression extension. Sparse individual wrong expressions do not identify a learner's actual erroneous operation. Accordingly all unidentified patterns are evidence replay profiles, not learner defaults. The independently computed cross/dot integrand designates correctness. `bank-map.json` is the machine-readable one-to-one map. No options are dropped, reclassified as passed without value matching, or silently pooled.

### q-160887

Field 7ab05865-9935-59ef-90a4-5cba4fa4f3d9; original designation present.

- Original $uv+v$; UUID 1cea6d00-8d2b-5733-8616-9267687fd149; wrong; expression recipe `s*(u*v + v)`; operation tree `Add(Mul(Symbol('u', real=True), Symbol('v', real=True)), Symbol('v', real=True))`.

- Original $uv-v$; UUID 63293960-e3b1-529e-96e9-642aedf596e5; correct; expression recipe `s*(u*v - v)`; operation tree `Add(Mul(Symbol('u', real=True), Symbol('v', real=True)), Mul(Integer(-1), Symbol('v', real=True)))`.

- Original ${u}^{2}+uv+{v}^{2}$; UUID 84b21f44-ef97-5299-8654-bb5534b15960; wrong; expression recipe `s*(u**2 + u*v + v**2)`; operation tree `Add(Pow(Symbol('u', real=True), Integer(2)), Mul(Symbol('u', real=True), Symbol('v', real=True)), Pow(Symbol('v', real=True), Integer(2)))`.

- Original $2{u}^{2}v-uv+{v}^{2}$; UUID cb8fdbef-d72d-513a-8e44-4a96d82e4382; wrong; expression recipe `s*(2*u**2*v - u*v + v**2)`; operation tree `Add(Mul(Integer(2), Pow(Symbol('u', real=True), Integer(2)), Symbol('v', real=True)), Mul(Integer(-1), Symbol('u', real=True), Symbol('v', real=True)), Pow(Symbol('v', real=True), Integer(2)))`.

- Original $u+v$; UUID e83e93b0-2e8f-5324-b1ed-23d683ac8523; wrong; expression recipe `s*(u + v)`; operation tree `Add(Symbol('u', real=True), Symbol('v', real=True))`.

### q-161360-legacy

Field 5503c223-e87a-5159-abb7-434053fd7b58; original designation ABSENT; separately inferred, never counted matched.

- Original $u^{2} + v^{2}$; UUID d9d8774c-14c0-5481-9a1f-1c3acd63867a; designation absent; expression recipe `s*(u**2 + v**2)`; operation tree `Add(Pow(Symbol('u', real=True), Integer(2)), Pow(Symbol('v', real=True), Integer(2)))`.

- Original $u^{2} - v^{2}$; UUID e5ce5f03-88a7-5102-bfd3-b0e4a75a4aed; designation absent; expression recipe `s*(u**2 - v**2)`; operation tree `Add(Pow(Symbol('u', real=True), Integer(2)), Mul(Integer(-1), Pow(Symbol('v', real=True), Integer(2))))`.

- Original $u^{2} + uv + v^{2}$; UUID 31b2be0c-93a0-5cd7-8143-0596b46129e1; designation absent; expression recipe `s*(u**2 + u*v + v**2)`; operation tree `Add(Pow(Symbol('u', real=True), Integer(2)), Mul(Symbol('u', real=True), Symbol('v', real=True)), Pow(Symbol('v', real=True), Integer(2)))`.

- Original $2uv$; UUID 6ce44ca0-320e-5c90-a723-d02a6010576d; designation absent; expression recipe `s*(2*u*v)`; operation tree `Mul(Integer(2), Symbol('u', real=True), Symbol('v', real=True))`.

- Original $2(u + v)^{2}$; UUID 7423bf6e-47f3-548e-afbe-feee4e861dd1; designation absent; expression recipe `s*(2*(u + v)**2)`; operation tree `Mul(Integer(2), Pow(Add(Symbol('u', real=True), Symbol('v', real=True)), Integer(2)))`.

### q-161360

Field 185487e5-090f-5815-93b2-dfc0c983e691; original designation present.

- Original ${u}^{2}+{v}^{2}$; UUID f754a120-8886-56d3-b535-398f13b91c9f; wrong; expression recipe `s*(u**2 + v**2)`; operation tree `Add(Pow(Symbol('u', real=True), Integer(2)), Pow(Symbol('v', real=True), Integer(2)))`.

- Original ${u}^{2}+uv+{v}^{2}$; UUID d28df103-ae23-5647-a506-1bc60c332868; wrong; expression recipe `s*(u**2 + u*v + v**2)`; operation tree `Add(Pow(Symbol('u', real=True), Integer(2)), Mul(Symbol('u', real=True), Symbol('v', real=True)), Pow(Symbol('v', real=True), Integer(2)))`.

- Original $2uv$; UUID e85142cb-e059-512c-8b7b-18eee7a8c253; correct; expression recipe `s*(2*u*v)`; operation tree `Mul(Integer(2), Symbol('u', real=True), Symbol('v', real=True))`.

- Original ${u}^{2}-{v}^{2}$; UUID e433762d-59a0-5efb-bef2-7687d8583f2a; wrong; expression recipe `s*(u**2 - v**2)`; operation tree `Add(Pow(Symbol('u', real=True), Integer(2)), Mul(Integer(-1), Pow(Symbol('v', real=True), Integer(2))))`.

- Original $2(u+v)^{2}$; UUID 3a53a3c7-e2f5-50e9-afd4-d3b986017cf4; wrong; expression recipe `s*(2*(u + v)**2)`; operation tree `Mul(Integer(2), Pow(Add(Symbol('u', real=True), Symbol('v', real=True)), Integer(2)))`.

### q-161358

Field 8692e3d1-c9bd-5cca-9274-6af9e13d6963; original designation present.

- Original $-7u+4v$; UUID 10279bac-75c2-5820-bf33-84359cbf720e; correct; expression recipe `s*(-7*u + 4*v)`; operation tree `Add(Mul(Integer(-1), Integer(7), Symbol('u', real=True)), Mul(Integer(4), Symbol('v', real=True)))`.

- Original $4u+7v$; UUID 397e53f3-63a0-518a-999e-8c3d8631bb27; wrong; expression recipe `s*(4*u + 7*v)`; operation tree `Add(Mul(Integer(4), Symbol('u', real=True)), Mul(Integer(7), Symbol('v', real=True)))`.

- Original $7u+8v$; UUID 897e0260-ef83-5fe5-9ee2-95ed9d4cd1a6; wrong; expression recipe `s*(7*u + 8*v)`; operation tree `Add(Mul(Integer(7), Symbol('u', real=True)), Mul(Integer(8), Symbol('v', real=True)))`.

- Original $8u-7v$; UUID bd3f2f9b-ef08-5972-b94d-02717ccd84df; wrong; expression recipe `s*(8*u - 7*v)`; operation tree `Add(Mul(Integer(8), Symbol('u', real=True)), Mul(Integer(-1), Integer(7), Symbol('v', real=True)))`.

- Original $-7u-8v$; UUID ee6d4a87-66ae-58b1-806a-631ade59590d; wrong; expression recipe `s*(-7*u - 8*v)`; operation tree `Add(Mul(Integer(-1), Integer(7), Symbol('u', real=True)), Mul(Integer(-1), Integer(8), Symbol('v', real=True)))`.

### q-161441

Field 7a3b6104-863d-512e-9bea-c3b626c9b6e0; original designation present.

- Original $-2u+7v$; UUID 10b5412c-a9ab-5d1e-8d26-9a4c8f27c8e6; correct; expression recipe `s*(-2*u + 7*v)`; operation tree `Add(Mul(Integer(-1), Integer(2), Symbol('u', real=True)), Mul(Integer(7), Symbol('v', real=True)))`.

- Original $4u+v$; UUID 16ffd34a-40d1-5df6-87ca-5595406b5509; wrong; expression recipe `s*(4*u + v)`; operation tree `Add(Mul(Integer(4), Symbol('u', real=True)), Symbol('v', real=True))`.

- Original $4v-u$; UUID 85617ab2-8072-5a8d-9456-259cf0bef230; wrong; expression recipe `s*(-u + 4*v)`; operation tree `Add(Mul(Integer(-1), Symbol('u', real=True)), Mul(Integer(4), Symbol('v', real=True)))`.

- Original $-2u+v$; UUID ce5a4f92-85cc-5237-ba98-a4e395360811; wrong; expression recipe `s*(-2*u + v)`; operation tree `Add(Mul(Integer(-1), Integer(2), Symbol('u', real=True)), Symbol('v', real=True))`.

- Original $2u+4v$; UUID fe69b9d6-2d90-53f7-90a8-f4819b62096e; wrong; expression recipe `s*(2*u + 4*v)`; operation tree `Add(Mul(Integer(2), Symbol('u', real=True)), Mul(Integer(4), Symbol('v', real=True)))`.

### q-161462

Field ca208624-88d6-5a85-8572-2dd062347b32; original designation present.

- Original $3u-3v$; UUID 002ddc9f-2c71-5478-8c1d-77a6a8c334bf; correct; expression recipe `s*(3*u - 3*v)`; operation tree `Add(Mul(Integer(3), Symbol('u', real=True)), Mul(Integer(-1), Integer(3), Symbol('v', real=True)))`.

- Original $2u+v$; UUID 023841e2-2821-56a0-955a-89084c15f8d2; wrong; expression recipe `s*(2*u + v)`; operation tree `Add(Mul(Integer(2), Symbol('u', real=True)), Symbol('v', real=True))`.

- Original $u+2v$; UUID 4d835b30-d2dd-53ba-9310-a5a2961e3b3e; wrong; expression recipe `s*(u + 2*v)`; operation tree `Add(Symbol('u', real=True), Mul(Integer(2), Symbol('v', real=True)))`.

- Original $2u-3v$; UUID b4df5cbd-8643-5942-bb9e-8d044eb77815; wrong; expression recipe `s*(2*u - 3*v)`; operation tree `Add(Mul(Integer(2), Symbol('u', real=True)), Mul(Integer(-1), Integer(3), Symbol('v', real=True)))`.

- Original $3v+u$; UUID f42daa7a-2c08-5500-aa68-d0405d0dc904; wrong; expression recipe `s*(u + 3*v)`; operation tree `Add(Symbol('u', real=True), Mul(Integer(3), Symbol('v', real=True)))`.

### q-161381

Field f789f76e-872e-5abd-b18f-ca246f894f3b; original designation present.

- Original $7uv-4v$; UUID 5477038f-1f6e-56c9-abc2-d2382dd8493b; wrong; expression recipe `s*(7*u*v - 4*v)`; operation tree `Add(Mul(Integer(7), Symbol('u', real=True), Symbol('v', real=True)), Mul(Integer(-1), Integer(4), Symbol('v', real=True)))`.

- Original $11u-24v$; UUID 938e31d9-0fe9-5c52-a191-c068034a6287; correct; expression recipe `s*(11*u - 24*v)`; operation tree `Add(Mul(Integer(11), Symbol('u', real=True)), Mul(Integer(-1), Integer(24), Symbol('v', real=True)))`.

- Original $11u+4v$; UUID 73e0a3dc-0594-5177-ad29-6281fad0f7ff; wrong; expression recipe `s*(11*u + 4*v)`; operation tree `Add(Mul(Integer(11), Symbol('u', real=True)), Mul(Integer(4), Symbol('v', real=True)))`.

- Original $u-v$; UUID 9cd2d79e-1a1c-53cf-b530-bcceff073bb9; wrong; expression recipe `s*(u - v)`; operation tree `Add(Symbol('u', real=True), Mul(Integer(-1), Symbol('v', real=True)))`.

- Original $24uv$; UUID 1188f498-8136-53fa-a7c5-2ca872f32cf0; wrong; expression recipe `s*(24*u*v)`; operation tree `Mul(Integer(24), Symbol('u', real=True), Symbol('v', real=True))`.

### q-161467

Field 1a967ea9-62a2-59e7-9156-ea0fff576b7d; original designation present.

- Original $8u$; UUID 0f202e15-0fbe-50af-9841-523a939ec510; wrong; expression recipe `s*(8*u)`; operation tree `Mul(Integer(8), Symbol('u', real=True))`.

- Original $u-2v$; UUID 176843b4-510b-5e14-95d1-94f7f1d2b76b; wrong; expression recipe `s*(u - 2*v)`; operation tree `Add(Symbol('u', real=True), Mul(Integer(-1), Integer(2), Symbol('v', real=True)))`.

- Original $8u-2v$; UUID 5fb6d1ec-f761-53b6-be0f-80e6cadaee49; correct; expression recipe `s*(8*u - 2*v)`; operation tree `Add(Mul(Integer(8), Symbol('u', real=True)), Mul(Integer(-1), Integer(2), Symbol('v', real=True)))`.

- Original $-4v$; UUID 73b04bf4-208b-5a5c-aac6-b4ba092785fe; wrong; expression recipe `s*(-4*v)`; operation tree `Mul(Integer(-1), Integer(4), Symbol('v', real=True))`.

- Original $2u+4v$; UUID eeb5f55b-ba54-5712-9575-db91590f82a9; wrong; expression recipe `s*(2*u + 4*v)`; operation tree `Add(Mul(Integer(2), Symbol('u', real=True)), Mul(Integer(4), Symbol('v', real=True)))`.

### q-161357

Field d15555d0-ef8f-523d-8686-3e2c75b76cda; original designation present.

- Original $-2u+v$; UUID 82fdd23c-cc42-585e-88f4-5b182b40e621; wrong; expression recipe `s*(-2*u + v)`; operation tree `Add(Mul(Integer(-1), Integer(2), Symbol('u', real=True)), Symbol('v', real=True))`.

- Original $3uv$; UUID 23aa505d-ac0a-5049-b866-d1c5cc38bc93; wrong; expression recipe `s*(3*u*v)`; operation tree `Mul(Integer(3), Symbol('u', real=True), Symbol('v', real=True))`.

- Original $11uv$; UUID e4493f5f-d9a0-53f7-a4c1-2310218fdc19; wrong; expression recipe `s*(11*u*v)`; operation tree `Mul(Integer(11), Symbol('u', real=True), Symbol('v', real=True))`.

- Original $u+v$; UUID 8e689bac-8fa3-596f-82fa-c4985e2215d2; wrong; expression recipe `s*(u + v)`; operation tree `Add(Symbol('u', real=True), Symbol('v', real=True))`.

- Original $5u-6v$; UUID 8b17b653-bdb9-591a-a066-41676556f6e8; correct; expression recipe `s*(5*u - 6*v)`; operation tree `Add(Mul(Integer(5), Symbol('u', real=True)), Mul(Integer(-1), Integer(6), Symbol('v', real=True)))`.

### q-161359

Field 396da9a4-de3b-5bd7-8b5e-dfc780e10bb9; original designation present.

- Original ${u}^{2}-uv+{v}^{2}$; UUID c8c22e69-9068-5d72-8593-ce78861036f9; correct; expression recipe `s*(u**2 - u*v + v**2)`; operation tree `Add(Pow(Symbol('u', real=True), Integer(2)), Mul(Integer(-1), Symbol('u', real=True), Symbol('v', real=True)), Pow(Symbol('v', real=True), Integer(2)))`.

- Original ${u}^{2}-{v}^{2}$; UUID 2f4db3f6-9c97-526b-8cb2-065c8f5de466; wrong; expression recipe `s*(u**2 - v**2)`; operation tree `Add(Pow(Symbol('u', real=True), Integer(2)), Mul(Integer(-1), Pow(Symbol('v', real=True), Integer(2))))`.

- Original $(u+v)^{2}$; UUID 7b2e8a80-65c9-5d70-9b0e-0e801e7e718d; wrong; expression recipe `s*((u + v)**2)`; operation tree `Pow(Add(Symbol('u', real=True), Symbol('v', real=True)), Integer(2))`.

- Original $(u-v)^{2}$; UUID 9f182d4d-0129-52ff-90b2-56e5acb487b3; wrong; expression recipe `s*((u - v)**2)`; operation tree `Pow(Add(Symbol('u', real=True), Mul(Integer(-1), Symbol('v', real=True))), Integer(2))`.

- Original ${u}^{2}+uv-{v}^{2}$; UUID c1e4fd3a-37bb-5bcd-85c6-185c9a1d61c2; wrong; expression recipe `s*(u**2 + u*v - v**2)`; operation tree `Add(Pow(Symbol('u', real=True), Integer(2)), Mul(Symbol('u', real=True), Symbol('v', real=True)), Mul(Integer(-1), Pow(Symbol('v', real=True), Integer(2))))`.

### q-161377

Field 2bbc92cc-19ad-54ee-9d42-9ce995a00f4a; original designation present.

- Original ${u}^{2}$; UUID 146aebe7-02b6-58b6-8dd1-374b1fcd30d0; correct; expression recipe `s*(u**2)`; operation tree `Pow(Symbol('u', real=True), Integer(2))`.

- Original $4uv$; UUID 3586c1bc-3061-5093-99ca-95e798991986; wrong; expression recipe `s*(4*u*v)`; operation tree `Mul(Integer(4), Symbol('u', real=True), Symbol('v', real=True))`.

- Original ${u}^{3}$; UUID 5a1a3ab5-07e2-55d2-b713-d20c37bdda9e; wrong; expression recipe `s*(u**3)`; operation tree `Pow(Symbol('u', real=True), Integer(3))`.

- Original $2uv$; UUID 6197b42b-5e97-5e6b-a1bb-2951dc50be38; wrong; expression recipe `s*(2*u*v)`; operation tree `Mul(Integer(2), Symbol('u', real=True), Symbol('v', real=True))`.

- Original $3v$; UUID cacced8e-053e-5057-89f0-678a72c14a18; wrong; expression recipe `s*(3*v)`; operation tree `Mul(Integer(3), Symbol('v', real=True))`.

### q-161379

Field dce1231b-682c-5119-8b60-1e600b81511c; original designation present.

- Original $-uv$; UUID 0b89c0b5-bd8b-5088-a053-0db9bc0fd31f; wrong; expression recipe `s*(-u*v)`; operation tree `Mul(Integer(-1), Symbol('u', real=True), Symbol('v', real=True))`.

- Original $5uv$; UUID 57bc1e11-c92f-5bf5-b1cd-bdfca274f1c3; correct; expression recipe `s*(5*u*v)`; operation tree `Mul(Integer(5), Symbol('u', real=True), Symbol('v', real=True))`.

- Original $3u{v}^{2}$; UUID 62a07ee3-0b12-5f4d-81e0-7183964e0136; wrong; expression recipe `s*(3*u*v**2)`; operation tree `Mul(Integer(3), Symbol('u', real=True), Pow(Symbol('v', real=True), Integer(2)))`.

- Original $uv+v$; UUID 876d48e1-3fb3-5bc6-88d3-a7e99ab5d29a; wrong; expression recipe `s*(u*v + v)`; operation tree `Add(Mul(Symbol('u', real=True), Symbol('v', real=True)), Symbol('v', real=True))`.

- Original $uv-v$; UUID b65ee624-a7db-5060-ba14-007644627aeb; wrong; expression recipe `s*(u*v - v)`; operation tree `Add(Mul(Symbol('u', real=True), Symbol('v', real=True)), Mul(Integer(-1), Symbol('v', real=True)))`.

### q-161471

Field de6e4169-2fd0-5a0b-b7fe-172964aca58f; original designation present.

- Original $8u-23v$; UUID 556660a7-ba40-5142-a23c-96cdb3bb38b3; wrong; expression recipe `s*(8*u - 23*v)`; operation tree `Add(Mul(Integer(8), Symbol('u', real=True)), Mul(Integer(-1), Integer(23), Symbol('v', real=True)))`.

- Original $12u-v$; UUID 86aaa33f-073f-5b9c-b6ed-02e42f1370d2; wrong; expression recipe `s*(12*u - v)`; operation tree `Add(Mul(Integer(12), Symbol('u', real=True)), Mul(Integer(-1), Symbol('v', real=True)))`.

- Original $8u+14v$; UUID 8fa80cac-9ed0-54f2-a0fb-a71697486081; wrong; expression recipe `s*(8*u + 14*v)`; operation tree `Add(Mul(Integer(8), Symbol('u', real=True)), Mul(Integer(14), Symbol('v', real=True)))`.

- Original $5u-17v$; UUID 9d9623af-3bba-5a0d-9c01-61a215703653; correct; expression recipe `s*(5*u - 17*v)`; operation tree `Add(Mul(Integer(5), Symbol('u', real=True)), Mul(Integer(-1), Integer(17), Symbol('v', real=True)))`.

- Original $u-6v$; UUID b721d1da-8cb3-5423-bdff-f515271a77db; wrong; expression recipe `s*(u - 6*v)`; operation tree `Add(Symbol('u', real=True), Mul(Integer(-1), Integer(6), Symbol('v', real=True)))`.

The authored default complete bank uses A=P(r)*N_x, B=Q(r)*N_y, C=R(r)*N_z and I=A+B+C. Its five expressions are I (correct), -I (reverse ordered cross), -A+B+C (reverse first normal component), A-B+C (reverse second normal component), A+B (omit third dot contribution). The entire selected bank is rejected if any two values are equivalent or a required wrong value equals I. All three levels share this complete operation bank. No first-valid-option selection occurs.

## Stage 4: Reusable template, constraints and calculations

Fixed components are the complete source prose between math blocks, eight display positions, radio shape and mathematical stage ordering. Variable slots are whole field expressions, graph, ordered rectangle endpoints, parametrization, partials/tangents, determinant/minors/cross, unsimplified substituted component expressions, collected field if present, each dot contribution, distributed polynomial, simplified integrand and complete choices. They are calculated from the same exact SymPy instance. Optional rows are controlled by the observed source family, not the answer choice. Authored levels use all substitution and dot rows. Rendering uses whole-expression slots rather than replacing short mathematical tokens through prose or basis labels; substitution inserts the entire graph only at the coordinate symbol z in each already isolated field component.

Observed recipe bounds: original plane slopes are required for source profiles, |s|<=3 for explicitly supplied parameters, positive s=1..3 in the evidence sampler. Normal defaults vary signed slopes, signed field multiplier and domain while using the method-derived bank. All explicit API parameters must match the exact expected key set, satisfy integer and signed magnitude constraints, and pass complete bank validity; invalid explicit inputs raise rather than resample. Only sampled invalid complete instances are retried.

Displayed mathematical tasks are fingerprinted by expanded printed F, graph and ordered orientation; uncomputed rectangle endpoints only enter presentation identity, independent of bank, seed and family spelling. Presentation identity includes version, complete prompt, fixed solution, level and sorted full bank. Each field owns UUID answer identities. Source cases replay through the ordinary API with original parameters/profile; no literal question-payload branch exists.

## Source repairs and interpretation limits

q-161360 has two captured `selection` fields. The authoritative original widget in /home/jake/Developer/MA/DATA/Lessons/4143/Source/4143.json (question 161360) and inspected 04-question-161360.png has one five-option selection. Both captured banks match the same five values. The legacy field 5503c223-e87a-5159-abb7-434053fd7b58 lacks a correct ref; independently -u²-v²+(u+v)²=2uv. Normal output uses one field. Both banks are replayed separately. That missing designation is never counted matched.

q-161471's last surface-integral LHS incorrectly prints <z-y,2y-z,xy>, while its prompt, substitution and correct dot integrand use <x+z,2z,y+z>. This sole LHS field is repaired from the actual prompt; raw evidence remains unchanged. Eleven solutions have no mathematical repair, one has this repair. All 12 source prose/row sequences match. All prompt/solution mathematical typography is normalized (SymPy powers/spacing, balanced domain braces and parenthesized final integrands), so no verbatim full-solution equality is claimed.

Error intent for several original polynomial choices remains underdetermined. Exact expression-pattern replay plus covariance is not evidence of an original authoring algorithm. The authored default operation bank is separately identified in metadata and evidence.




## Supported operation enumeration and residual patterns

Before retaining an opaque expression, enumerate all normal-component sign/omission combinations, omitted normals/isolated field components, doubled components, source distributed-term omission/sign reversal, multiplying the full dot by u/v, false z substitution by 0/u/v, and wrong graph-square cross coefficients combined with omitted other dot components. Exact whole-polynomial matches identify supported operation candidates. All matches are listed; ambiguity is not misrepresented as recovered intent. Selected source-bank choices are computed by these actual operations where supported. Covariant symbolic expression patterns remain only for residual underidentified shapes. Among the 60 distinct family-bank choices, 28 have supported candidates (12 correct and 16 wrong), 32 retain residual patterns, and 10 have multiple candidate matches. The duplicate legacy bank adds five mapped values, including four wrong values, without adding a new pattern.

### q-160887

- $uv + v$: selected `dot_component_weights_-1,-1,1`; all candidates `dot_component_weights_-1,-1,1`, `omit_normal_sum_field_components`, `reverse_distributed_term_1:v`.

- $uv - v$: selected `correct_cross_dot`; all candidates `correct_cross_dot`, `replace_graph_coordinate_z_by_0`, `replace_graph_coordinate_z_by_u`, `replace_graph_coordinate_z_by_v`.

- $u^{2} + uv + v^{2}$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $2 u^{2} v - uv + v^{2}$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $u + v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

### q-161360

- $u^{2} + v^{2}$: selected `dot_component_weights_-1,-1,0`; all candidates `dot_component_weights_-1,-1,0`, `graph_square_cross_factor_0_use_component_2_omit_others`.

- $u^{2} + uv + v^{2}$: selected `graph_square_cross_factor_1_use_component_2_omit_others`; all candidates `graph_square_cross_factor_1_use_component_2_omit_others`.

- $2 uv$: selected `correct_cross_dot`; all candidates `correct_cross_dot`.

- $u^{2} - v^{2}$: selected `dot_component_weights_-1,1,0`; all candidates `dot_component_weights_-1,1,0`, `omit_normal_first_minus_second`.

- $2 \left(u + v\right)^{2}$: selected `double_field_component_2_omit_others`; all candidates `double_field_component_2_omit_others`.

### q-161358

- $- 7 u + 4 v$: selected `correct_cross_dot`; all candidates `correct_cross_dot`.

- $4 u + 7 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $7 u + 8 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $8 u - 7 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $- 7 u - 8 v$: selected `reverse_distributed_term_0:v`; all candidates `reverse_distributed_term_0:v`.

### q-161441

- $- 2 u + 7 v$: selected `correct_cross_dot`; all candidates `correct_cross_dot`.

- $4 u + v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $- u + 4 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $- 2 u + v$: selected `omit_distributed_term_1:v`; all candidates `omit_distributed_term_1:v`.

- $2 u + 4 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

### q-161462

- $3 u - 3 v$: selected `correct_cross_dot`; all candidates `correct_cross_dot`.

- $2 u + v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $u + 2 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $2 u - 3 v$: selected `dot_component_weights_0,1,0`; all candidates `dot_component_weights_0,1,0`, `replace_graph_coordinate_z_by_v`.

- $u + 3 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

### q-161381

- $7 uv - 4 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $11 u - 24 v$: selected `correct_cross_dot`; all candidates `correct_cross_dot`.

- $11 u + 4 v$: selected `omit_distributed_term_1:v`; all candidates `omit_distributed_term_1:v`.

- $u - v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $24 uv$: residual symbolic pattern; no supported candidate in the enumerated operation set.

### q-161467

- $8 u$: selected `double_field_component_2_omit_others`; all candidates `double_field_component_2_omit_others`.

- $u - 2 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $8 u - 2 v$: selected `correct_cross_dot`; all candidates `correct_cross_dot`, `dot_component_weights_0,-1,1`.

- $- 4 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $2 u + 4 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

### q-161357

- $- 2 u + v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $3 uv$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $11 uv$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $u + v$: selected `omit_normal_use_field_component_0`; all candidates `omit_normal_use_field_component_0`.

- $5 u - 6 v$: selected `correct_cross_dot`; all candidates `correct_cross_dot`.

### q-161359

- $u^{2} - uv + v^{2}$: selected `correct_cross_dot`; all candidates `correct_cross_dot`.

- $u^{2} - v^{2}$: selected `dot_component_weights_-1,1,0`; all candidates `dot_component_weights_-1,1,0`.

- $\left(u + v\right)^{2}$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $\left(u - v\right)^{2}$: selected `dot_component_weights_1,1,0`; all candidates `dot_component_weights_1,1,0`, `omit_distributed_term_2:u*v`.

- $u^{2} + uv - v^{2}$: selected `dot_component_weights_-1,1,1`; all candidates `dot_component_weights_-1,1,1`, `omit_normal_sum_field_components`.

### q-161377

- $u^{2}$: selected `correct_cross_dot`; all candidates `correct_cross_dot`, `omit_normal_sum_field_components`, `replace_graph_coordinate_z_by_0`, `replace_graph_coordinate_z_by_u`, `replace_graph_coordinate_z_by_v`.

- $4 uv$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $u^{3}$: selected `multiply_dot_by_u`; all candidates `multiply_dot_by_u`.

- $2 uv$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $3 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

### q-161379

- $- uv$: selected `dot_component_weights_0,0,-1`; all candidates `dot_component_weights_0,0,-1`.

- $5 uv$: selected `correct_cross_dot`; all candidates `correct_cross_dot`, `replace_graph_coordinate_z_by_0`, `replace_graph_coordinate_z_by_u`, `replace_graph_coordinate_z_by_v`.

- $3 uv^{2}$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $uv + v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $uv - v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

### q-161471

- $8 u - 23 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $12 u - v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $8 u + 14 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.

- $5 u - 17 v$: selected `correct_cross_dot`; all candidates `correct_cross_dot`.

- $u - 6 v$: residual symbolic pattern; no supported candidate in the enumerated operation set.
