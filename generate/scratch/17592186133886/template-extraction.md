# Template extraction

## Stage 1: specific original descriptions

All practice prompts ask a scalar boundary line integral over a pictured region. P,Q are linear in the differentiated coordinate, except constant P in q-126578. Region boundaries are positively oriented by the course convention: outer counterclockwise, holes clockwise. Pictures have no arrows. All original answer values are exact integers or integer multiples of π. Every supported widget is radio with five scalar math choices. q-126578 has one legacy duplicate field; authoritative captured lesson widget confirms only one question with five choices. Raw evidence retains both fields.

- **q-126515 / square_unrated**: {'a': -1, 'b': 1, 'W': 4, 'H': 4, 's': 2}; P=-y, Q=x, held partials -1,1; outer area 16, removed areas [4], remaining area 12, result 24. No difficulty, correct ref or worked solution exists in the source.
- **q-126578 / annulus_constant**: {'a': 1, 'b': 1, 'R': 2, 'r': 1}; P=1, Q=x, held partials 0,1; outer area 4*pi, removed areas [pi], remaining area 3*pi, result 3*pi. Observed level moderate; 7 aligned rows.
- **q-126853 / rectangle_square**: {'a': 2, 'b': 4, 'W': 6, 'H': 4, 's': 2}; P=2y, Q=4x, held partials 2,4; outer area 24, removed areas [4], remaining area 20, result 40. Observed level easy; 9 aligned rows.
- **q-126856 / annulus_negative**: {'a': 3, 'b': 2, 'R': 3, 'r': 1}; P=3y, Q=2x, held partials 3,2; outer area 9*pi, removed areas [pi], remaining area 8*pi, result -8*pi. Observed level moderate; 8 aligned rows.
- **q-126860 / square_square**: {'a': -5, 'b': 8, 'W': 8, 'H': 8, 's': 6}; P=-5y, Q=8x, held partials -5,8; outer area 64, removed areas [36], remaining area 28, result 364. Observed level easy; 9 aligned rows.
- **q-126894 / annulus_positive**: {'a': 6, 'b': 9, 'R': 3, 'r': 2}; P=6y, Q=9x, held partials 6,9; outer area 9*pi, removed areas [4*pi], remaining area 5*pi, result 15*pi. Observed level moderate; 7 aligned rows.
- **q-126891 / circle_semicircle**: {'a': 5, 'b': 11, 'R': 4, 'r': 2}; P=5y, Q=11x, held partials 5,11; outer area 16*pi, removed areas [2*pi], remaining area 14*pi, result 84*pi. Observed level moderate; 7 aligned rows.
- **q-126880 / diamond_square**: {'a': 8, 'b': 13, 'W': 6, 'H': 6, 's': 2}; P=8y, Q=13x, held partials 8,13; outer area 18, removed areas [4], remaining area 14, result 70. Observed level easy; 8 aligned rows.

## Stage 2: family generalization

Compute ∂Q/∂x−∂P/∂y while holding the other coordinate fixed. This is a constant k. Green's theorem gives k times the geometric area of the region: outer area minus the complete area of each hole. Retain each original integration-to-area and arithmetic chain. No polar-coordinate integration, nonconstant scalar curl, boundary parameterization, supplied circulations, or arbitrary extra function branch is introduced. Hard has exactly two unequal holes and keeps the same constant-curl operation.

## Stage 3: components and complete choice mapping

All historical banks below are fully mapped as explicit coefficient operations `v_i(p)=c_i·k(p)·Area(p)`, where `c_i=original_value/(original_k·original_area)`. For π banks the π cancels from c_i; for integer banks c_i is rational. This is an opaque proportional historical bank extension, **not recovered error intent**. It is evidence-only and ineligible for practice even when its correct choice is mathematically sound. No numerical interpolation polynomial or private literal replay path is used. The full bank is preserved together; it is never mixed with authored recipes. Raw anchor values retain their original Unicode/TeX spelling and trailing spaces.

### q-126515, observed_raw field 0

| Original complete value | Coefficient operation c_i | Original designation |
|---|---|---|
| `24` | `1 · k · Area(D)` | designation absent for entire field |
| `36` | `3/2 · k · Area(D)` | designation absent for entire field |
| `16` | `2/3 · k · Area(D)` | designation absent for entire field |
| `12` | `1/2 · k · Area(D)` | designation absent for entire field |
| `8` | `1/3 · k · Area(D)` | designation absent for entire field |
### q-126578, observed_raw field 0

| Original complete value | Coefficient operation c_i | Original designation |
|---|---|---|
| `-2π` | `-2/3 · k · Area(D)` | designation absent for entire field |
| `6π` | `2 · k · Area(D)` | designation absent for entire field |
| `3π` | `1 · k · Area(D)` | designation absent for entire field |
| `4π` | `4/3 · k · Area(D)` | designation absent for entire field |
| `2π` | `2/3 · k · Area(D)` | designation absent for entire field |
### q-126578, observed_raw field 1

| Original complete value | Coefficient operation c_i | Original designation |
|---|---|---|
| `4\pi ` | `4/3 · k · Area(D)` | incorrect |
| `-2\pi ` | `-2/3 · k · Area(D)` | incorrect |
| `3\pi ` | `1 · k · Area(D)` | correct |
| `6\pi ` | `2 · k · Area(D)` | incorrect |
| `2\pi ` | `2/3 · k · Area(D)` | incorrect |
### q-126853, observed_raw field 0

| Original complete value | Coefficient operation c_i | Original designation |
|---|---|---|
| `20` | `1/2 · k · Area(D)` | incorrect |
| `60` | `3/2 · k · Area(D)` | incorrect |
| `10` | `1/4 · k · Area(D)` | incorrect |
| `40` | `1 · k · Area(D)` | correct |
| `30` | `3/4 · k · Area(D)` | incorrect |
### q-126856, observed_raw field 0

| Original complete value | Coefficient operation c_i | Original designation |
|---|---|---|
| `9\pi ` | `-9/8 · k · Area(D)` | incorrect |
| `-8\pi ` | `1 · k · Area(D)` | correct |
| `-12\pi ` | `3/2 · k · Area(D)` | incorrect |
| `10\pi ` | `-5/4 · k · Area(D)` | incorrect |
| `6\pi ` | `-3/4 · k · Area(D)` | incorrect |
### q-126860, observed_raw field 0

| Original complete value | Coefficient operation c_i | Original designation |
|---|---|---|
| `364` | `1 · k · Area(D)` | correct |
| `215` | `215/364 · k · Area(D)` | incorrect |
| `424` | `106/91 · k · Area(D)` | incorrect |
| `342` | `171/182 · k · Area(D)` | incorrect |
| `124` | `31/91 · k · Area(D)` | incorrect |
### q-126894, observed_raw field 0

| Original complete value | Coefficient operation c_i | Original designation |
|---|---|---|
| `12\pi ` | `4/5 · k · Area(D)` | incorrect |
| `14\pi ` | `14/15 · k · Area(D)` | incorrect |
| `15\pi ` | `1 · k · Area(D)` | correct |
| `16\pi ` | `16/15 · k · Area(D)` | incorrect |
| `18\pi ` | `6/5 · k · Area(D)` | incorrect |
### q-126891, observed_raw field 0

| Original complete value | Coefficient operation c_i | Original designation |
|---|---|---|
| `14\pi ` | `1/6 · k · Area(D)` | incorrect |
| `48\pi ` | `4/7 · k · Area(D)` | incorrect |
| `24\pi ` | `2/7 · k · Area(D)` | incorrect |
| `42\pi ` | `1/2 · k · Area(D)` | incorrect |
| `84\pi ` | `1 · k · Area(D)` | correct |
### q-126880, observed_raw field 0

| Original complete value | Coefficient operation c_i | Original designation |
|---|---|---|
| `18` | `9/35 · k · Area(D)` | incorrect |
| `32` | `16/35 · k · Area(D)` | incorrect |
| `45` | `9/14 · k · Area(D)` | incorrect |
| `70` | `1 · k · Area(D)` | correct |
| `90` | `9/7 · k · Area(D)` | incorrect |

## Stage 4: reusable masks and domains

The generator renders each family's own aligned sequence from computed complete mathematical components. A source-derived shared-prose mask supplies the theorem, extension sentence, P,Q definitions, formal held-coordinate operators, and concluding transition. Arithmetic rows are generated independently from parameters, not returned as literal source payloads. The raw unrated family omits its difficulty, worked solution, and correct ref exactly. Raw duplicate-field presence remains unchanged. The two erroneous initial LHSs are intentionally confined to raw replay; normal rows use the actual prompt integrand.

Normal chains at original and changed parameters preserve the initial formal theorem row, substituted curl, constant-integrand reduction, factor extraction where present, Area(D), source geometry formula, separately evaluated area components where source shows them, collected area where source shows it, and final scalar. Constant-P cancellation when k=1 and negative coefficient −1 omit redundant coefficient multiplication just as the source does; changed k retains the operative stages with a visible coefficient. The annulus-positive and semicircle sources combine their evaluated outer-minus-hole area directly, so normal chains retain that omission. Two-hole hard extensions show each hole's separately evaluated area before collection.

Bounds applied identically to explicit calls and samplers: nonzero signed integer a,b with absolute magnitude ≤13; nonzero curl. Moderate nested radii 1≤r<R≤7. Easy even outer dimensions 4..16 and square-hole side 2..14 strictly inside; square outer sides must agree; diamond is a symmetric diamond with equal diagonal lengths and 2s<W. Hard circle radii R in 5..10, r,t in 1..3, r≠t, max(r,t)<R/2, disjoint holes. Hard rectangle uses even sides ≤16 with two unequal even square sides ≤6, strict vertical and horizontal containment, and disjoint holes. The negative-annulus normal family requires negative curl; the positive-annulus and semicircle normal families require positive curl. Geometry bounds are practice policies, not recovered source code. Difficulty never changes the number of holes within a family.

Complete authored default banks, selected before parameters:

- Linear single-hole: kA; −kA (reverse orientation); kO (ignore hole); k(O+H) (add hole); Q_x A (omit P_y).
- Constant-P annulus: kA; −kA; kO; kH (integrate only hole); k(O+H).
- Upper-semicircle hole: kA; −kA; kO; k(O−2H) (remove full circle); k(O+H).
- Two-hole hard: kA; −kA; k(O−H₁); k(O−H₂); k(O+H₁+H₂).

Here O is outer area, H or H₁,H₂ the exact removed area(s), A=O−ΣH and k=Q_x−P_y. Every bank is operation-derived; equivalence of any choices rejects the whole sampled instance. Explicit invalid parameters raise an error and are never silently resampled. Default sampling serves all source-shaped families and both authored hard families. Profiles, cosmetic spelling and shuffled order do not inflate the mathematical fingerprint; displayed prompt, worked solution, level and complete bank determine presentation identity.

## Source anomalies and repair denominators

1. q-126515 has no rating, correct designation or solution. The authoritative lesson widget confirms a five-choice question, but contains no key. Geometry and derivatives independently give 24; this is an authored completion in normal output, not a matched historical designation. Raw absence remains exact.
2. q-126578 has a duplicate legacy field without a correct ref. The lesson widget records one supported five-choice bank. Raw preserves both; normal uses one supported field. Seven present keys can be matched; two absent keys cannot.
3. q-126894 and q-126891 copied the initial LHS `∮ dx+x dy` from another question; their P,Q and final answers correspond to their actual prompts. Raw preserves these two errors; normal fixes only the LHS. All seven final answers are independently correct, while only five complete present source solutions have correct initial LHSs.
4. No source geometry or bank correctness anomaly was found after all original boundaries and 45 scalar choices were inspected. Historical wrong-option intent remains unresolved. Raw replays are evidence-only.

No wrong-choice diagnosis is added to learner content. Native radio ID tests are separate from mathematical choice-value verification. The engine cannot load a raw field with no correct ref; native source fixtures project only existing supported fields and clearly label that projection, never fabricate a recovered key.
