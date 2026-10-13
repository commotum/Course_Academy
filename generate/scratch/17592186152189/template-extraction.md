# Four-stage extraction

## 1. Describe every source specifically

The tables below record every source number form, response layout, correct designation presence and whole choice bank. Every curve has positive unequal integer semiaxes; shifted centers include both signs and zero x-shift. The full prompt and complete worked prose/math sequence are in source.json and review.md; masks in specs.json preserve their exact bytes. Source masks are specialized only by presentation layout, never by numerical answer lookup.

### q-78679

Parameters: `{'a': 4, 'b': 2, 'h': 2, 'k': 1}`; captured level: unrated; source database id 17592186152795.

Field `selection`, `:answer-field.type/radio`, correct ref absent.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x = 4\cos θ - 2, y = 2\sin θ - 1` | `['a', 'b', '-h', '-k', 'cos', 'sin']` |
| `x = 8\cos θ + 2, y = 4\sin θ + 1` | `['2*a', '2*b', 'h', 'k', 'cos', 'sin']` |
| `x = 2\cos θ + 2, y = 1\sin θ - 1` | `['a/2', 'b/2', 'h', '-k', 'cos', 'sin']` |
| `x = 4\cos θ + 2, y = 2\sin θ + 1` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |
| `x = 8\cos θ - 2, y = 4\sin θ - 1` | `['2*a', '2*b', '-h', '-k', 'cos', 'sin']` |

### q-78680

Parameters: `{'a': 2, 'b': 3, 'h': 3, 'k': -1}`; captured level: hard; source database id 17592186152796.

Field `selection`, `:answer-field.type/radio`, correct ref absent.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x = 4\cos θ + 3, y = 6\sin θ - 1` | `['2*a', '2*b', 'h', 'k', 'cos', 'sin']` |
| `x = 4\sin θ + 3, y = 6\cos θ - 1` | `['2*a', '2*b', 'h', 'k', 'sin', 'cos']` |
| `x = \cos θ - 3, y = \sin θ + 2` | `['1', '1', '-h', 'a', 'cos', 'sin']` |
| `x = 2\sin θ + 3, y = 3\cos θ - 1` | `['a', 'b', 'h', 'k', 'sin', 'cos']` |
| `x = 2\cos θ + 3, y = 3\sin θ - 1` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |

Field `selection`, `:answer-field.type/radio`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x=2\operatorname{sin}⁡\theta +3,\,y=3\operatorname{cos}⁡\theta -1` | `['a', 'b', 'h', 'k', 'sin', 'cos']` |
| `x=\operatorname{cos}⁡\theta -3,\,y=\operatorname{sin}⁡\theta +2` | `['1', '1', '-h', 'a', 'cos', 'sin']` |
| `x=2\operatorname{cos}⁡\theta +3,\,y=3\operatorname{sin}⁡\theta -1` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |
| `x=4\operatorname{cos}⁡\theta +3,\,y=6\operatorname{sin}⁡\theta -1` | `['2*a', '2*b', 'h', 'k', 'cos', 'sin']` |
| `x=4\operatorname{sin}⁡\theta +3,\,y=6\operatorname{cos}⁡\theta -1` | `['2*a', '2*b', 'h', 'k', 'sin', 'cos']` |

### q-106398

Parameters: `{'a': 5, 'b': 3, 'h': -2, 'k': -3}`; captured level: hard; source database id 17592186241164.

Field `selection`, `:answer-field.type/radio`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x=5\operatorname{cos}⁡\theta -2,\,y=3\operatorname{sin}⁡\theta -3` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |
| `x=10\operatorname{sin}⁡\theta -2,\,y=6\operatorname{cos}⁡\theta -3` | `['2*a', '2*b', 'h', 'k', 'sin', 'cos']` |
| `x=5\operatorname{cos}⁡\theta -3,\,y=3\operatorname{sin}⁡\theta -2` | `['a', 'b', 'k', 'h', 'cos', 'sin']` |
| `x=5\operatorname{sin}⁡\theta -2,\,y=3\operatorname{cos}⁡\theta -3` | `['a', 'b', 'h', 'k', 'sin', 'cos']` |
| `x=25\operatorname{cos}⁡\theta -3,\,y=9\operatorname{sin}⁡\theta -2` | `['a**2', 'b**2', 'k', 'h', 'cos', 'sin']` |

### q-106399

Parameters: `{'a': 7, 'b': 4, 'h': -3, 'k': 2}`; captured level: hard; source database id 17592186241165.

Field `selection`, `:answer-field.type/radio`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x=7\operatorname{cos}⁡\theta +2,\,y=4\operatorname{sin}⁡\theta -3` | `['a', 'b', 'k', 'h', 'cos', 'sin']` |
| `x=4\operatorname{cos}⁡\theta -3,\,y=7\operatorname{sin}⁡\theta +2` | `['b', 'a', 'h', 'k', 'cos', 'sin']` |
| `x=7\operatorname{cos}⁡\theta -3,\,y=4\operatorname{sin}⁡\theta +2` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |
| `x=14\operatorname{sin}⁡\theta -3,\,y=8\operatorname{sin}⁡\theta +2` | `['2*a', '2*b', 'h', 'k', 'sin', 'sin']` |
| `x=7\operatorname{sin}⁡\theta +3,\,y=4\operatorname{cos}⁡\theta -2` | `['a', 'b', '-h', '-k', 'sin', 'cos']` |

### q-106704

Parameters: `{'a': 3, 'b': 8, 'h': 3, 'k': -2}`; captured level: moderate; source database id 17592186243930.

Field `selection`, `:answer-field.type/radio`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x=8\operatorname{cos}⁡\theta -3,\,y=3\operatorname{sin}⁡\theta +2` | `['b', 'a', '-h', '-k', 'cos', 'sin']` |
| `x=64\operatorname{cos}⁡\theta +3,\,y=9\operatorname{sin}⁡\theta -2` | `['b**2', 'a**2', 'h', 'k', 'cos', 'sin']` |
| `x=8\operatorname{cos}⁡\theta +3,\,y=3\operatorname{sin}⁡\theta -2` | `['b', 'a', 'h', 'k', 'cos', 'sin']` |
| `x=3\operatorname{cos}⁡\theta -3,\,y=8\operatorname{sin}⁡\theta +2` | `['a', 'b', '-h', '-k', 'cos', 'sin']` |
| `x=3\operatorname{cos}⁡\theta +3,\,y=8\operatorname{sin}⁡\theta -2` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |

### q-274862

Parameters: `{'a': 5, 'b': 3, 'h': 2, 'k': -1}`; captured level: hard; source database id 17592186292790.

Field `field-2`, `:answer-field.type/blank`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `3\operatorname{sin}\theta -1` | `['b', 'k', 'sin']` |

Field `field-1`, `:answer-field.type/blank`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `5\operatorname{cos}\theta +2` | `['a', 'h', 'cos']` |

### q-327171

Parameters: `{'a': 3, 'b': 8, 'h': 0, 'k': 5}`; captured level: hard; source database id 17592186302326.

Field `field-1`, `:answer-field.type/blank`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `3\operatorname{cos}\theta ` | `['a', 'h', 'cos']` |

Field `field-2`, `:answer-field.type/blank`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `8\operatorname{sin}\theta +5` | `['b', 'k', 'sin']` |

### q-327172

Parameters: `{'a': 4, 'b': 5, 'h': -2, 'k': 1}`; captured level: hard; source database id 17592186302327.

Field `field-1`, `:answer-field.type/blank`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `4\operatorname{cos}\theta -2` | `['a', 'h', 'cos']` |

Field `field-2`, `:answer-field.type/blank`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `5\operatorname{sin}\theta +1` | `['b', 'k', 'sin']` |

### q-79289

Parameters: `{'a': 8, 'b': 6, 'h': 4, 'k': 6}`; captured level: hard; source database id 17592186348193.

Field `selection`, `:answer-field.type/radio`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x=8\operatorname{cos}⁡\theta +4,\,y=6\operatorname{sin}⁡\theta +6` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |
| `x=8\operatorname{cos}⁡\theta +6,\,y=6\operatorname{sin}⁡\theta +4` | `['a', 'b', 'k', 'h', 'cos', 'sin']` |
| `x=6\operatorname{cos}⁡\theta +6,\,y=8\operatorname{sin}⁡\theta +4` | `['b', 'a', 'k', 'h', 'cos', 'sin']` |
| `x=16\operatorname{sin}⁡\theta +4,\,y=12\operatorname{cos}⁡\theta +6` | `['2*a', '2*b', 'h', 'k', 'sin', 'cos']` |
| `x=8\operatorname{sin}⁡\theta +4,\,y=6\operatorname{cos}⁡\theta +6` | `['a', 'b', 'h', 'k', 'sin', 'cos']` |

### q-79290

Parameters: `{'a': 6, 'b': 4, 'h': -2, 'k': 5}`; captured level: hard; source database id 17592186348194.

Field `selection`, `:answer-field.type/radio`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x=6\operatorname{cos}⁡\theta -2,\,y=4\operatorname{sin}⁡\theta +5` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |
| `x=4\operatorname{cos}⁡\theta +5,\,y=6\operatorname{sin}⁡\theta -2` | `['b', 'a', 'k', 'h', 'cos', 'sin']` |
| `x=12\operatorname{sin}⁡\theta -2,\,y=8\operatorname{cos}⁡\theta +5` | `['2*a', '2*b', 'h', 'k', 'sin', 'cos']` |
| `x=12\operatorname{cos}⁡\theta -2,\,y=8\operatorname{sin}⁡\theta +5` | `['2*a', '2*b', 'h', 'k', 'cos', 'sin']` |
| `x=6\operatorname{sin}⁡\theta -2,\,y=4\operatorname{cos}⁡\theta +5` | `['a', 'b', 'h', 'k', 'sin', 'cos']` |

### q-106706

Parameters: `{'a': 6, 'b': 4, 'h': -3, 'k': 2}`; captured level: moderate; source database id 17592186399531.

Field `selection`, `:answer-field.type/radio`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x=36\operatorname{cos}⁡\theta -2,\,y=16\operatorname{sin}⁡\theta +3` | `['a**2', 'b**2', '-k', '-h', 'cos', 'sin']` |
| `x=6\operatorname{cos}⁡\theta +3,\,y=4\operatorname{sin}⁡\theta -2` | `['a', 'b', '-h', '-k', 'cos', 'sin']` |
| `x=12\operatorname{cos}⁡\theta +2,\,y=8\operatorname{sin}⁡\theta -3` | `['2*a', '2*b', 'k', 'h', 'cos', 'sin']` |
| `x=12\operatorname{cos}⁡\theta -3,\,y=8\operatorname{sin}⁡\theta +2` | `['2*a', '2*b', 'h', 'k', 'cos', 'sin']` |
| `x=6\operatorname{cos}⁡\theta -3,\,y=4\operatorname{sin}⁡\theta +2` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |

### q-79285

Parameters: `{'a': 5, 'b': 3, 'h': -3, 'k': 2}`; captured level: moderate; source database id 17592186403988.

Field `selection`, `:answer-field.type/radio`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x=5\operatorname{cos}⁡\theta -3,\,y=3\operatorname{sin}⁡\theta +2` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |
| `x=5\operatorname{cos}⁡\theta +3,\,y=3\operatorname{sin}⁡\theta -2` | `['a', 'b', '-h', '-k', 'cos', 'sin']` |
| `x=10\operatorname{cos}⁡\theta +2,\,y=6\operatorname{sin}⁡\theta -3` | `['2*a', '2*b', 'k', 'h', 'cos', 'sin']` |
| `x=10\operatorname{cos}⁡\theta -3,\,y=6\operatorname{sin}⁡\theta +2` | `['2*a', '2*b', 'h', 'k', 'cos', 'sin']` |
| `x=25\operatorname{cos}⁡\theta -2,\,y=9\operatorname{sin}⁡\theta +3` | `['a**2', 'b**2', '-k', '-h', 'cos', 'sin']` |

### q-79286

Parameters: `{'a': 4, 'b': 6, 'h': -4, 'k': -4}`; captured level: moderate; source database id 17592186403995.

Field `selection`, `:answer-field.type/radio`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x=4\operatorname{cos}⁡\theta -4,\,y=6\operatorname{sin}⁡\theta -4` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |
| `x=36\operatorname{cos}⁡\theta -4,\,y=16\operatorname{sin}⁡\theta -4` | `['b**2', 'a**2', 'h', 'k', 'cos', 'sin']` |
| `x=4\operatorname{cos}⁡\theta +4,\,y=6\operatorname{sin}⁡\theta +4` | `['a', 'b', '-h', '-k', 'cos', 'sin']` |
| `x=6\operatorname{cos}⁡\theta +4,\,y=4\operatorname{sin}⁡\theta +4` | `['b', 'a', '-h', '-k', 'cos', 'sin']` |
| `x=6\operatorname{cos}⁡\theta -4,\,y=4\operatorname{sin}⁡\theta -4` | `['b', 'a', 'h', 'k', 'cos', 'sin']` |

### q-79287

Parameters: `{'a': 3, 'b': 5, 'h': 3, 'k': 2}`; captured level: moderate; source database id 17592186404002.

Field `selection`, `:answer-field.type/radio`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x=9\operatorname{cos}⁡\theta -2,\,y=25\operatorname{sin}⁡\theta +3` | `['a**2', 'b**2', '-k', 'h', 'cos', 'sin']` |
| `x=3\operatorname{cos}⁡\theta +3,\,y=5\operatorname{sin}⁡\theta +2` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |
| `x=5\operatorname{cos}⁡\theta -3,\,y=3\operatorname{sin}⁡\theta -2` | `['b', 'a', '-h', '-k', 'cos', 'sin']` |
| `x=5\operatorname{cos}⁡\theta +3,\,y=3\operatorname{sin}⁡\theta +2` | `['b', 'a', 'h', 'k', 'cos', 'sin']` |
| `x=3\operatorname{cos}⁡\theta +2,\,y=5\operatorname{sin}⁡\theta -3` | `['a', 'b', 'k', '-h', 'cos', 'sin']` |

### q-79292

Parameters: `{'a': 1, 'b': 2, 'h': 3, 'k': 1}`; captured level: hard; source database id 17592186404009.

Field `selection`, `:answer-field.type/radio`, correct ref present.

| Exact displayed source value | Parameterized complete operation |
|---|---|
| `x=\operatorname{cos}⁡\theta +3,\,y=2\operatorname{sin}⁡\theta +1` | `['a', 'b', 'h', 'k', 'cos', 'sin']` |
| `x=2\operatorname{cos}⁡\theta +3,\,y=4\operatorname{sin}⁡\theta +1` | `['2*a', '2*b', 'h', 'k', 'cos', 'sin']` |
| `x=\operatorname{sin}⁡\theta +3,\,y=2\operatorname{cos}⁡\theta +1` | `['a', 'b', 'h', 'k', 'sin', 'cos']` |
| `x=\operatorname{cos}⁡\theta +1,\,y=2\operatorname{sin}⁡\theta +3` | `['a', 'b', 'k', 'h', 'cos', 'sin']` |
| `x=2\operatorname{sin}⁡\theta +1,\,y=4\operatorname{cos}⁡\theta +3` | `['2*a', '2*b', 'k', 'h', 'sin', 'cos']` |

## 2. Generalize the mathematical pattern

Given or graph-read center (h,k) and positive horizontal/vertical semiaxes a,b, translate x=a cosθ,y=b sinθ by (h,k). The graph-only sources request the locus. Hard sources explicitly require rightmost-start CCW traversal on θ∈[0,2π). Sine/cosine interchange has the same ellipse locus but starts at its top and goes clockwise, so it is a valid hard distractor. Blank fields require only the separate x and y expressions, never equations with an equals sign.

## 3. Components and banks

Each six-tuple in the tables means `(x coefficient, y coefficient, x shift, y shift, x trig, y trig)`. Three-tuples denote `(coefficient, shift, trig)` for a fragment blank. Slots are complete coordinate/radius/function components. Formal generic equations remain fixed; source-specific center and a,b sentences and the entire concluding parametrization vary together. The A coordinate is computed as (h+a,k). Images vary from the same parameter values. Options are derived from the original complete bank: radius doubling/halving/squaring, swapping a/b, shifting/sign swapping h/k, swapping sine/cosine, or using both sines. No post-parameter first-valid distractor pool exists.

The q-78680 wrong unit-circle option uses unit coefficients, center −h and y-shift a. It reproduces the historical expression pattern but its intended mistake is unresolved: moving the radius a into a center coordinate is not promoted to a normal default. The remaining compound historical banks similarly document algebraic operations without claiming original author intent. All raw observed profiles are evidence-only; the public API builds these parameterized recipe banks and rejects ambiguous changed instances.

Normal complete authored locus bank: correct, double both radii, swap radii, negate center, square the swapped radii. Normal orientation bank: correct, swap sine/cosine, double radii plus swap sine/cosine, swap radii, negate center. Each operation arises from the two coefficient/function/shift components in the displayed method. Distinct a,b and non-origin center guard the full banks. The bank/profile is chosen before sampling. No unrelated additive perturbation is used as a normal distractor.

## 4. Reusable template and constraints

The source masks consist of fixed full prose, fixed formal x/y template and domain, and variable CENTER, START, A, B, FINAL and PLOT slots. Every answer formatter has source-extracted prefix/function spelling/spacing/unit-coefficient convention. Each source field's exact correct-ref presence and every question attribute's presence are retained. The normal solution has the complete shared formal rule, optional traversal sentence, actual center/radii substitution sentence, and final full parametrization. Source replay has precisely the original two math blocks and exact shared prose, including source blank whitespace and field collection order.

Sampling domain: 56 ordered unequal a,b pairs from 1..8 and 168 non-origin (h,k) pairs from −6..6, giving **9,408 substantive mathematical tasks per information/criterion family**. Coefficients and shifts all affect the locus. Normal hard radio/blank layouts and their aliases share one mathematical task fingerprint; source/bank notation is excluded from it. Easy versus moderate information, and hard's starting/traversal criterion, are substantive fingerprint components. Presentation identity hashes version, actual prompt, fixed solution, full displayed bank and difficulty; seed/shuffle changes cannot change it.

Observed source profiles preserve raw fields but are ineligible for normal learner generation. Missing levels are authored claims: easy removes the graph-reading demand while retaining general-center translation. Moderate reads center/radii; hard checks start/direction. All three retain the same parameter ceiling. Explicit invalid parameters and any whole-bank ambiguity are rejected. General-center scope forbids origin, equal-radius circles and rotated/partial ellipses.

## Independent verification and limitations

Validator parses the actual rendered prompt, all displayed choices, formal rule, substituted center/radii prose, final equations, and blank fragments. It checks full source prose and math-block sequence equality, attribute presence, mathematical eligibility by locus plus start/tangent direction, formatting, identities, domain bounds, fresh concurrent renderer writes, source raster extents and generated raster extents. Original snapshots, measured transforms and generated PNG hashes are retained. Raw legacy ungraded fields cannot count as native grading passes. Native fixtures select only captured designated fields and state that selection explicitly.

Canonical and nontrivially factored translation expressions are accepted by the native engine. Trigonometric phase-shift equivalent blank expressions are independently exact but the engine returns “symbolic equivalence is not established by the supported rules”: **14 unresolved native checks**, separately counted; they are never reported as accepted. No engine change is made. No source mathematical error or prompt repair was needed.
