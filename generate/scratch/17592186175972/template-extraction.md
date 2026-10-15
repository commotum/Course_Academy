> Inventory decision, 2026-10-15: v2 certifies easy/moderate only. The hard normalization proposal below is retained as rejected draft analysis; it adds a solution stage and is not supported or generated. See capabilities.json and validation.json. All six captured sources are unchanged at the fresh pre-commit basis.

# Template extraction

## 1. Specific originals

All vectors are Cartesian triples in `(x,y,z)` basis order. Their actual shown function arguments, rather than nearby erroneous prose, establish independent parameters. No plot appears in prompt, solution or bank.

| Source | Actual vector / relation / requested role | Solution / captured defects |
|---|---|---|
| q103986 easy | f(x,z)=⟨x,missing,z⟩; y=4x²; second dependent coordinate | Standard tuple then substitute graph; x,z arbitrary real; conclude 4x². Duplicate radio fields: legacy lacks correct designation; supported field is keyed. |
| q103992 unrated | f(x,y)=⟨missing,y,9y²⟩; 9y²=z; first free coordinate | Prose erroneously says f(x,z). Missing correct ref, worked solution and rating. Actual parameters require x as free coordinate. |
| q164440 easy | f(x,z)=⟨x,6x²,missing⟩; y=6x²; third free coordinate | Standard tuple then graph, conclude z. Choice 6z is also a full covering parametrization unless coordinate-copy convention is required. |
| q164443 easy | f(y,z)=⟨missing,y,z⟩; x=3y²; first dependent coordinate | Standard tuple then graph, y,z real; conclude 3y². |
| q164441 easy | f(x,z)=⟨x,missing,z⟩; y=12x²; second dependent coordinate | Same graph stages; conclude 12x². |
| q164450 moderate | f(y,z)=⟨missing,y,z⟩; 8z²=x; first dependent coordinate | Same graph stages; y,z real; conclude 8z². Base parameter is second-listed. |

## 2. General pattern

A graph cylinder has exactly one relation `d=c*u²` with a free axis `v`. Its direct-coordinate parametrization inserts `c*u²` into the dependent slot and copies the two independently varying named coordinates. The learner fills either the dependent slot or the free slot, preserving that requested role. Covering the full surface requires both satisfying the relation and allowing every real base/free-coordinate pair, not just a pointwise relation.

The original free-axis teaching convention is made explicit in normal questions: “Use the named parameters directly as their corresponding Cartesian coordinates.” The source solution's formal tuple and domain sentence enact the same convention. Normal free-copy solutions additionally state the named free-axis coordinate explicitly before retaining all observed stages. This changes answer-form eligibility, not the geometric truth of `6z` as a covering parametrization. Every complete option is independently inserted in the actual printed vector. The source-geometric-audit records constraint, free coverage, complete-map eligibility and geometric aliases separately.

## 3. Component and complete-bank mapping

Let `u` be the actual quadratic base, `d` the dependent axis, `v` the free axis and `c=a/b`. Recipes are complete expressions, not source payload lookups. All raw profiles use b=1. The order below is recipe order; option order is incidental.

| Profile / field | Original choices | Parameterized complete bank |
|---|---|---|
| q103986 legacy | 2x, z², x², 4z², 4x² | (c/2)u, v², u², cv², cu²; missing correct key retained |
| q103986 supported | 4z², 4x², z², x², 2x | same full bank, original braced notation; cu² keyed |
| q103992 | y, x², sin y, x, y² | u, v², sin u, v, u²; no raw key |
| q164440 | z, z², 6z, x, 6x² | v, v², cv, u, cu²; v keyed |
| q164443 | 3y², z, 3z², y, 3y | cu², v, cv², u, cu; cu² keyed |
| q164441 | 12x, z, 12z, z², 12x² | cu, v, cv, v², cu²; cu² keyed |
| q164450 | y², 8z², y, 8z, 8y | v², cu², v, cu, cv; cu² keyed |
| Authored q103986 normal | original opaque half-linear member held in raw replay | cu, v², u², cv², cu²; one whole eligible method bank |
| Authored hard | no source bank | cu², au² (omit division), (1/c)u² (invert ratio), cu (omit square), cv² (wrong parameter) |

Historical q103986 `(c/2)u` reproduces the observed 2x and remains an explicit observed expression mask. Its authorial intent is underidentified; no derivative error is asserted. It remains available only in evidence-only raw replay. The q103986 normal default selects the complete authored bank replacing this one member with `cu` (omit the square); this bank is labeled authored, not recovered. q103992's sine option is an observed distractor only, not a newly authored surface operation. No feedback was captured and none is invented. All complete banks are selected before parameters; collisions reject the whole question. Coefficients c=1 and zero are excluded from normal/source-mask sampling so no dropped-scale bank collision arises.

Wrong-versus-wrong comparison uses complete inserted maps, and independently reports geometric equivalence of full-cover maps. q164440's z and 6z are different functions but the same cylinder image. Under the explicit direct-coordinate convention only z is eligible. z² and x² do not cover the entire free real axis; x-only or sin(y)-only options couple the free axis to the base. Pointwise satisfaction alone is insufficient. For dependent banks the wrong coordinate changes the graph relation, including linear versus quadratic base and use of the other parameter.

## 4. Backbone, slots and replay

Fixed: one nonzero quadratic monomial, one dependent coordinate, one unrestricted free axis, Cartesian tuple basis `(x,y,z)`, source radio response shape, five-option complete profile, graph-copy solution stages. Observed solution sequence: common opening → formal f(args)=⟨x,y,z⟩ → completed graph tuple → actual argument domain sentence → target ordinal and component conclusion. Inline q103992 has no observed solution; its normal solution is explicitly authored from this shared family.

Variable: base/dependent axes are any distinct pair from x,y,z; free axis is the remaining one. Requested target may be any eligible axis preserving its selected dependent/free role. Function f/g/h and argument order are independent slots, changed everywhere. Equation orientation is conditional; moderate retains quadratic-first and free-first arguments. Easy source profiles permit both argument orders on explicit calls. Normal q103992 repairs prose using its actually displayed f(x,y), never f(x,z).

Easy/moderate coefficient a is an integer 2..12 and b=1, reflecting source integer forms including 12. Hard is a distinct authored family: a=2..12, b=2..5, coprime, noninteger a/b; normalize once and use the same graph tuple. This guard applies both to sampling and explicit calls. Hard normalization adds one justified stage and no new relation operator or mathematical surface class; its grade remains uncertain. All six ordered role-axis permutations are eligible. There is no ellipse, two-variable quadratic, paraboloid, cone, rotation, translation, square-root branch or restricted-axis variation.

Public raw replay profiles use suffix `_raw`, e.g. `generate('easy', profile='q-103992_raw', parameters=...)`. They preserve full exact source prompt/answer spellings, every present solution sentence, omissions and duplicate fields. Raw source attribute presence is checked separately from mathematical correctness; absent correct refs never count as matched designations. The complete immutable wrapper remains in source.json. Normal output removes q103986 legacy field and uses its separately labeled complete authored bank, adds matching keyed placeholders, infers the q103992 mathematically verified x key and authors its missing solution/easy metadata, and clarifies the free-axis convention.

Mathematical fingerprints omit names, banks, option ordering, argument ordering, equation orientation and incidental free-task coefficients/base-dependence. Free-copy tasks count only the three eligible target coordinate positions. Dependent tasks count ordered actual base/dependent axes and reduced coefficient; hard normalization is a distinct reasoning workload. Full content identity includes actual displayed prompt, fixed solution, difficulty and complete bank with attribute presence, but excludes seed/order/profile aliases. Meaningful capacity is finite and exhaustively enumerated in validation.json. Easy and moderate copy-dependent tasks overlap and are counted once in global capacity; level labels are not extra mathematical tasks.
