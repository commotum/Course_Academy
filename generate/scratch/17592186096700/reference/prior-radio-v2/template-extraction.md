# Four-stage template extraction

## 1. Describe each source before generalizing

q-19215: image above prose; five blue translated vectors a–e on an unlabeled 12×12 square grid. Statements exactly `b =-2e`, `c =-d`, `b = 2e`. One `selection` radio field. Complete text bank: I only; II and III only; I and III only; I and II only; III only. No difficulty, correct designation, or solution. Full raster: a=(4,2), b=(-4,-2), c=(2,5), d=(-2,-5), e=(2,1), in grid-square units. Thus I/II are true, III is false. Arrow tails/heads, not their displayed location, determine these displacements.

q-20404: same figure role/grid/style and prose; statements exactly `a =-c`, `c =-\frac{1}{2}a`, `b = d`. Complete bank: I only; II and III only; III only; II only; I and III only. Same field and missing attributes. Raster: a=(6,4), b=(-3,-5), c=(-3,-2), d=(3,5), e=(-4,0). Only II is true. I uses the wrong length (a is twice c), III ignores opposite arrow direction.

Canonical e-5183: prose first, diagram last; bold-vector notation. Three statements b=-c, e=2a, a=2e. The supplied fixed solution has three bullets: unequal b/c magnitudes; e/a same direction and magnitude ratio2; e larger than a; then only-II conclusion. The source is retained verbatim in review. Its shared explanatory structure and sentences anchor authored solutions; there is no practice worked-solution text to claim replicated. The canonical image's b magnitude2 and c magnitude3 independently support its first bullet.

## 2. Shared mathematical purpose

For each of three printed vector equalities, compare arrow direction and relative magnitude from a common equal-square grid. Select the unordered subset of true statements. Translation of a vector does not change it. A negative scalar reverses direction while positive scalar preserves direction. Exact equality requires both the direction and magnitude ratio. The response is a complete truth subset, never just a single matching vector.

## 3. Map every component and complete bank

Let u,v be nonzero nonparallel displacement families; k>0; s,t∈{-1,+1}.

| Mask | Computed vectors | Statement components |
|---|---|---|
| opposite_multiple | e=u, b=sk·u, c=v, d=t·v, unused a=k·u | b=-k·e; c=-d; b=k·e |
| reciprocal_multiple | a=k·u, c=s·u, b=v, d=t·v, unused e=(-4,0) | a=-c; c=-(1/k)·a; b=d |

Original parameters and all five tails are explicit in `source-cases.json`. Tips are derived from tails plus computed displacement; these are genuinely parameterized recipes. The complete original diagram is restored only if this whole geometry matches the measured original geometry. Otherwise raw profiles render the changed instance and retain missing difficulty/key/solution.

| Source / field | Choice text | Exact unordered subset | At original parameters |
|---|---|---|---|
| q-19215 / selection | I only | {I} | false: omits II |
| same | II and III only | {II,III} | false: omits I, adds III |
| same | I and III only | {I,III} | false: omits II, adds III |
| same | I and II only | {I,II} | independently correct |
| same | III only | {III} | false: omits I/II, adds III |
| q-20404 / selection | I only | {I} | false: omits II, adds I |
| same | II and III only | {II,III} | false: adds III |
| same | III only | {III} | false: omits II, adds III |
| same | II only | {II} | independently correct |
| same | I and III only | {I,III} | false: omits II, adds I/III |

These map the complete source answers one-to-one, without guessing the original author's psychological intent. The subset semantics are exact; omission/addition interpretations follow the actual truth set. The observed bank membership is a fixed categorical catalog, not an arbitrary fit to numbers. In normal completed profiles the same catalog applies to changed signs/geometry only when it contains exactly one correct subset. The entire instance is rejected otherwise. No first-valid recipe pool or option substitution exists.

Authored-selection-flips is a separately labeled complete profile: true subset T, T△{I}, T△{II}, T△{III}, T△{I,III}. Each wrong response is a real omission/addition of a displayed statement selection. Distinct flip masks guarantee five distinct subsets; all are checked against the actual printed criterion. This profile is chosen before parameter sampling. Learner-facing choices and worked solutions contain no invented distractor diagnosis.

## 4. Reusable masks, constraints, calculations

Fixed prompt: original image-first placement, original shared question sentence, three numbered `$…$` statements. Variable slots: complete left vector, complete multiplier, complete right vector; computed tips/labels; image reference. Source whitespace differs between the first two statements and the third and is retained. Radio layout, count5, text answer type and key `selection` are fixed. Original absent attributes remain absent in raw replay. Captured database IDs/math-academy IDs are provenance in `source.json`; local generated UUIDs own their fields/banks. No new external source identity is invented.

The generator first selects the whole family/profile, then samples its parameters; computes exact vectors; evaluates each complete printed equality; constructs the complete eligible bank; rejects missing/colliding valid responses; and renders one fixed solution. All arithmetic uses Rational values. Normal solution structure is three truth bullets and one subset conclusion, borrowing canonical wording for direction/magnitude arguments. False bullets vary only when the actual printed relation fails by direction versus magnitude. Every equation/conclusion is rebuilt from complete slots; no blind replacement across labels/prose occurs.

Scope constraints and level guards are documented in the script and classification. Integer-grid tails/tips, bounded nonzero displacements, distinct directions, and fixed common physical scale are preserved. Hard 3:2/2:3 ratios are exact and never achieved by enlarging an algebra problem. Mathematical-task fingerprints retain direction families, signed relations and ratio, but exclude unrelated pair length scaling, unused a/e, translation, answer bank and choice order. Presentation/content identity uses actual prompt, solution, complete displayed bank and difficulty. Raw original key absence prevents an inferred key being counted as fidelity.

No mathematical source error was found. The missing assessment attributes are explicit captured anomalies, not silently repaired evidence. Public raw bank fidelity:2 banks/10 choices. Original correct-designation denominator:0 available (2 missing). Original worked-solution denominator:0 available (2 missing). Completed inference/native grading is separate.
