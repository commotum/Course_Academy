# Current source classification and sampling scope

Database `math`, basis 2681, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The six frozen sources retain their prompts, solutions, banks and difficulty annotations. Two have since gained a calculator requirement; their existing facts will be preserved. Five additional source questions are captured in the adjacent exact EDB read and source-refresh.json.

| Difficulty | Current source count | Prompt/value templates | Fields | Plots |
|---|---:|---:|---|---|
| easy | 0 | 0 observed; 1 canonical-grounded authored family | radio whole tangent equation | none |
| moderate | 5 | 5 | 3 radio whole lines; 2 RHS blanks | none |
| hard | 5 | 5 | 3 radio coordinate pairs; 2 coordinate-blank pairs | none |
| unclassified | 1 | 1 | radio whole line with no correct reference or solution | none |

The existing generator remains version `parametric-tangent-1`: seven validated families, with authored complete choice banks. Its six observed bank profiles remain evidence only. Source replay fidelity is 23/23 values and 6/6 complete banks at the frozen basis. New structures below are classified and validated from displayed mathematics; no claim of generator replay fidelity is made for them. Their sampling is excluded from this replenishment. This does not make any difficulty unsupported: existing supported families cover all three levels.

## Newly captured templates

### q-350328 / 17592186527941: Fifth/cubic x and quadratic y; slope-intercept RHS blank

Observed coordinate functions: `x=2*t**5 - 4*t**3`, `y=t**2`; parameter `1`. Point `['-2', '1']`, slope `-1`, y-intercept `-1`. The exact prompt, domain, solution and full field-owned banks are retained in source-refresh.json.

Backbone: substitute the supplied parameter; differentiate both coordinate functions; take the ratio; evaluate the slope; form the point-slope line. RHS blanks rearrange to `y=...`; axis-intercept tasks additionally substitute the appropriate zero coordinate. These differences are separate templates, with no new sampler slots inferred from a single source.

Field `field-1` (:answer-field.type/blank), independent profile `q-350328:field-1`:

- `-x-1` — correct.

### q-122584 / 17592186527943: Square-root x and shifted cubic y; point-slope radio

Observed coordinate functions: `x=sqrt(t + 1)`, `y=t**3 + 4`; parameter `1`. Point `['sqrt(2)', '5']`, slope `6*sqrt(2)`, y-intercept `-7`. The exact prompt, domain, solution and full field-owned banks are retained in source-refresh.json.

Backbone: substitute the supplied parameter; differentiate both coordinate functions; take the ratio; evaluate the slope; form the point-slope line. RHS blanks rearrange to `y=...`; axis-intercept tasks additionally substitute the appropriate zero coordinate. These differences are separate templates, with no new sampler slots inferred from a single source.

Field `selection` (:answer-field.type/radio), independent profile `q-122584:selection`:

- `y-5=6(x-\sqrt{2})` — incorrect; observed expression retained, generalized recipe unresolved.
- `y-5=\sqrt{2}(x-\sqrt{2})` — incorrect; observed expression retained, generalized recipe unresolved.
- `y+5=2\sqrt{3}(x+2)` — incorrect; observed expression retained, generalized recipe unresolved.
- `y-5=6\sqrt{2}(x-\sqrt{2})` — correct.
- `y+\sqrt{2}=\frac{3\sqrt{2}}{4}(x+5)` — incorrect; observed expression retained, generalized recipe unresolved.

### q-75267 / 17592186527971: Quadratic x and seventh-power y; point-slope radio

Observed coordinate functions: `x=2*t**2 + 8*t`, `y=4*t**7`; parameter `1`. Point `['10', '4']`, slope `7/3`, y-intercept `-58/3`. The exact prompt, domain, solution and full field-owned banks are retained in source-refresh.json.

Backbone: substitute the supplied parameter; differentiate both coordinate functions; take the ratio; evaluate the slope; form the point-slope line. RHS blanks rearrange to `y=...`; axis-intercept tasks additionally substitute the appropriate zero coordinate. These differences are separate templates, with no new sampler slots inferred from a single source.

Field `selection` (:answer-field.type/radio), independent profile `q-75267:selection`:

- `y-4=\frac{7}{3}(x-10)` — correct.
- `y-2=7(x-10)` — incorrect; observed expression retained, generalized recipe unresolved.
- `y-4=\frac{14}{3}(x-3)` — incorrect; observed expression retained, generalized recipe unresolved.
- `y+2=\frac{7}{6}(x-10)` — incorrect; observed expression retained, generalized recipe unresolved.
- `y+4=\frac{3}{7}(x-10)` — incorrect; observed expression retained, generalized recipe unresolved.

### q-122700 / 17592186527989: Quadratic x and shifted square-root y; y-intercept radio

Observed coordinate functions: `x=t**2 + 3*t`, `y=sqrt(2)*sqrt(t) + 1`; parameter `2`. Point `['10', '3']`, slope `1/14`, y-intercept `16/7`. The exact prompt, domain, solution and full field-owned banks are retained in source-refresh.json.

Backbone: substitute the supplied parameter; differentiate both coordinate functions; take the ratio; evaluate the slope; form the point-slope line. RHS blanks rearrange to `y=...`; axis-intercept tasks additionally substitute the appropriate zero coordinate. These differences are separate templates, with no new sampler slots inferred from a single source.

Field `selection` (:answer-field.type/radio), independent profile `q-122700:selection`:

- `(0,\,\frac{16}{7})` — correct.
- `(0,\,\frac{16}{5})` — incorrect; observed expression retained, generalized recipe unresolved.
- `(0,\,-\frac{5}{7})` — incorrect; observed expression retained, generalized recipe unresolved.
- `(0,\,\frac{12}{7})` — incorrect; observed expression retained, generalized recipe unresolved.
- `(0,\,-\frac{2}{7})` — incorrect; observed expression retained, generalized recipe unresolved.

### q-350343 / 17592186527993: Rational quadratic x and cubic y; two y-intercept coordinate blanks

Observed coordinate functions: `x=t**2 + t/2 + 3/2`, `y=t**3 + 7*t**2 + 8*t`; parameter `-1`. Point `['2', '-2']`, slope `2`, y-intercept `-6`. The exact prompt, domain, solution and full field-owned banks are retained in source-refresh.json.

Backbone: substitute the supplied parameter; differentiate both coordinate functions; take the ratio; evaluate the slope; form the point-slope line. RHS blanks rearrange to `y=...`; axis-intercept tasks additionally substitute the appropriate zero coordinate. These differences are separate templates, with no new sampler slots inferred from a single source.

Field `field-1` (:answer-field.type/blank), independent profile `q-350343:field-1`:

- `0` — correct.

Field `field-2` (:answer-field.type/blank), independent profile `q-350343:field-2`:

- `-6` — correct.

## Eligibility and bounded exceptions

The unrated q-6862 is excluded from available inventory because its key, difficulty and solution are absent. No source repair is included. Coordinate blanks using “Do not round” are tested against canonical, equivalent and incorrect entries with the current grader; failures are excluded from our validated reserve even if the application lists them in its raw pool. Source facts and learner history remain unchanged.

This run fills by validated existing families only. Newly observed templates and opaque observed distractor generalizations remain outside sampling; their exact evidence is retained for future extension. No requested level is claimed filled unless at least five fresh distinct, mathematically checked and gradable tasks remain at the verified basis.
