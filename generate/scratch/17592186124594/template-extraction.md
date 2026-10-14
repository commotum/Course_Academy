# Template extraction

## 1. Specific originals

See classification for every exact Cartesian expression/target/name. All require a symbolic derivative expression, without an equation left-hand side, a numerical point, or a rounding instruction. Original source radio layout is a fixed `selection` field with five math answers. q-37196 has neither a difficulty, a correct ref, nor a worked solution. All other six have four worked display blocks: generic two-term chain rule, Cartesian partials, substituted polar partials, then ordered substitution/collection. Final block row counts are respectively 3, unavailable, 3, 3, 2, 2, 3. The easy formulas use polynomials of degree 2/3 and natural logs of linear/radial expressions; exact integer/rational coefficients, sin/cos(theta), and double angles. r>0 is the polar domain; ln(x+y) additionally requires r(cos(theta)+sin(theta))>0.

## 2. General pattern

For Cartesian-given F(x,y), calculate F_x and F_y. Substitute x=r cos(theta), y=r sin(theta), then form F_r=F_x cos(theta)+F_y sin(theta) or F_theta=-r F_x sin(theta)+r F_y cos(theta). Simplify only after the explicit substitution and original collection stages. Easy templates introduce a positive linear scale a. All observed full option expressions are correspondingly scaled: source expression-pattern preservation, not a fitted polynomial or recovered psychological error recipe. Because several original mistakes are underdetermined, default generation uses separately labeled authored operation banks. Observed/legacy banks remain complete replay profiles, never mixed into a pooled default.

## 3. Component and complete-bank map

The table below accounts for every raw captured option, including the duplicate legacy bank. Each displayed value is the full source expression; the parameterized recipe is a times that full expression. No option is dropped or silently interpreted as an operation. At a=1 all values match independently parsed mathematics. Current correct refs and absent refs are distinguished. Raw answer UUIDs remain in source.json; review output owns new field-specific UUIDs.

### q-37192 / legacy

Prompt: Given that $f(x,y)=2xy+{y}^{2},$ find $\frac{∂f}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

| Captured answer | Complete parameterized recipe | Source designation | Intent |
|---|---|---|---|
| $2r^{2}\cos (2θ) + r^{2}\sin (2θ)$ | $a\left(2r^{2}\cos (2\theta) + r^{2}\sin (2\theta)\right)$ | no correct ref in capture | expression pattern; intended wrong operation unresolved |
| $3r^{2}\cos (2θ)$ | $a\left(3r^{2}\cos (2\theta)\right)$ | no correct ref in capture | expression pattern; intended wrong operation unresolved |
| $2r\sin (2θ) + 2r\sin^{2} θ$ | $a\left(2r\sin (2\theta) + 2r\sin^{2} \theta\right)$ | no correct ref in capture | expression pattern; intended wrong operation unresolved |
| $2r\cos (2θ) + r\sin (2θ)$ | $a\left(2r\cos (2\theta) + r\sin (2\theta)\right)$ | no correct ref in capture | expression pattern; intended wrong operation unresolved |
| $r^{2}\cos θ + r^{2}\sin θ$ | $a\left(r^{2}\cos \theta + r^{2}\sin \theta\right)$ | no correct ref in capture | expression pattern; intended wrong operation unresolved |

### q-37192 / observed

Prompt: Given that $f(x,y)=2xy+{y}^{2},$ find $\frac{∂f}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

| Captured answer | Complete parameterized recipe | Source designation | Intent |
|---|---|---|---|
| ${r}^{2}\operatorname{cos}⁡\theta +{r}^{2}\operatorname{sin}⁡\theta $ | $a\left({r}^{2}\cos\theta +{r}^{2}\sin\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $2r\operatorname{cos}⁡(2\theta )+r\operatorname{sin}⁡(2\theta )$ | $a\left(2r\cos(2\theta )+r\sin(2\theta )\right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $2r\operatorname{sin}⁡(2\theta )+2r{sin}^{2}⁡\theta $ | $a\left(2r\sin(2\theta )+2r\sin^{2}\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $3{r}^{2}\operatorname{cos}⁡(2\theta )$ | $a\left(3{r}^{2}\cos(2\theta )\right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $2{r}^{2}\operatorname{cos}⁡(2\theta )+{r}^{2}\operatorname{sin}⁡(2\theta )$ | $a\left(2{r}^{2}\cos(2\theta )+{r}^{2}\sin(2\theta )\right)$ | correct ref present | expression pattern; intended wrong operation unresolved |

### q-37196 / observed

Prompt: Given that $g(x, y) = \ln (x + y)$, find $\frac{∂g}{∂r}$, where $(x, y)$ are Cartesian coordinates and $(r, θ)$ are the corresponding plane polar coordinates.

| Captured answer | Complete parameterized recipe | Source designation | Intent |
|---|---|---|---|
| $\frac{1}{r}$ | $a\left(\frac{1}{r}\right)$ | no correct ref in capture | expression pattern; intended wrong operation unresolved |
| $r$ | $a\left(r\right)$ | no correct ref in capture | expression pattern; intended wrong operation unresolved |
| $\frac{\cos θ - \sin θ}{\cos θ + \sin θ}$ | $a\left(\frac{\cos \theta - \sin \theta}{\cos \theta + \sin \theta}\right)$ | no correct ref in capture | expression pattern; intended wrong operation unresolved |
| $\frac{1}{r\cos θ + r\sin θ}$ | $a\left(\frac{1}{r\cos \theta + r\sin \theta}\right)$ | no correct ref in capture | expression pattern; intended wrong operation unresolved |
| $r^{2}\sin θ$ | $a\left(r^{2}\sin \theta\right)$ | no correct ref in capture | expression pattern; intended wrong operation unresolved |

### q-94999 / observed

Prompt: Given that $h(x,y)={x}^{2}y,$ find $\frac{∂h}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

| Captured answer | Complete parameterized recipe | Source designation | Intent |
|---|---|---|---|
| $2{r}^{3}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta $ | $a\left(2{r}^{3}\cos\theta \sin^{2}\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $3{r}^{2}\operatorname{cos}⁡\theta $ | $a\left(3{r}^{2}\cos\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| ${r}^{2}{cos}^{2}⁡\theta $ | $a\left({r}^{2}\cos^{2}\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $3{r}^{2}{cos}^{2}⁡\theta \operatorname{sin}⁡\theta $ | $a\left(3{r}^{2}\cos^{2}\theta \sin\theta \right)$ | correct ref present | expression pattern; intended wrong operation unresolved |
| $2{r}^{2}{sin}^{2}⁡\theta $ | $a\left(2{r}^{2}\sin^{2}\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |

### q-95109 / observed

Prompt: Given that $w(x,y)=\operatorname{ln}⁡({x}^{2}+{y}^{2}),$ find $\frac{∂w}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

| Captured answer | Complete parameterized recipe | Source designation | Intent |
|---|---|---|---|
| $2{cos}^{2}⁡\theta -1$ | $a\left(2\cos^{2}\theta -1\right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $\frac{r}{2}$ | $a\left(\frac{r}{2}\right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $2r$ | $a\left(2r\right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $\frac{2}{r}$ | $a\left(\frac{2}{r}\right)$ | correct ref present | expression pattern; intended wrong operation unresolved |
| ${r}^{2}\operatorname{cos}⁡\theta $ | $a\left({r}^{2}\cos\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |

### q-95112 / observed

Prompt: Given that $f(x,y)={x}^{2},$ find $\frac{∂f}{∂r},$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

| Captured answer | Complete parameterized recipe | Source designation | Intent |
|---|---|---|---|
| $2r{cos}^{2}⁡\theta $ | $a\left(2r\cos^{2}\theta \right)$ | correct ref present | expression pattern; intended wrong operation unresolved |
| $2r{sin}^{2}⁡\theta $ | $a\left(2r\sin^{2}\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $2r\operatorname{cos}⁡(2\theta )$ | $a\left(2r\cos(2\theta )\right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $r{cos}^{2}⁡\theta $ | $a\left(r\cos^{2}\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $r\operatorname{cos}⁡(2\theta )$ | $a\left(r\cos(2\theta )\right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |

### q-95113 / observed

Prompt: Given that $g(x,y)={y}^{2},$ find $\frac{∂g}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

| Captured answer | Complete parameterized recipe | Source designation | Intent |
|---|---|---|---|
| $r{cos}^{2}⁡\theta $ | $a\left(r\cos^{2}\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| ${r}^{2}(1-{sin}^{2}⁡\theta )$ | $a\left({r}^{2}(1-\sin^{2}\theta )\right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $r\operatorname{sin}⁡(2\theta )$ | $a\left(r\sin(2\theta )\right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| ${r}^{2}{sin}^{2}⁡\theta $ | $a\left({r}^{2}\sin^{2}\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| ${r}^{2}\operatorname{sin}⁡(2\theta )$ | $a\left({r}^{2}\sin(2\theta )\right)$ | correct ref present | expression pattern; intended wrong operation unresolved |

### q-95116 / observed

Prompt: Given that $w(x,y)=\frac{{x}^{2}}{2}+\frac{{y}^{2}}{2},$ find $\frac{∂w}{∂\theta },$ where $(x,y)$ are Cartesian coordinates and $(r,\theta )$ are the corresponding plane polar coordinates.

| Captured answer | Complete parameterized recipe | Source designation | Intent |
|---|---|---|---|
| $1-{r}^{2}\operatorname{sin}⁡(2\theta )$ | $a\left(1-{r}^{2}\sin(2\theta )\right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| ${r}^{2}\operatorname{sin}⁡(2\theta )$ | $a\left({r}^{2}\sin(2\theta )\right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $0$ | $a\left(0\right)$ | correct ref present | expression pattern; intended wrong operation unresolved |
| $r{sin}^{2}⁡\theta $ | $a\left(r\sin^{2}\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |
| $r{cos}^{2}⁡\theta $ | $a\left(r\cos^{2}\theta \right)$ | wrong under existing correct ref | expression pattern; intended wrong operation unresolved |

## 4. Reusable masks, domains, calculations and repairs

Fixed components: original prompt sentences, function-of-two-Cartesian-variables form, full source worked prose, four display blocks, and original final-stage sequence/row count. Variable complete components: Cartesian function RHS, its two partial RHSs, their polar substitution RHSs, every ordered final-stage RHS, target derivative/function labels, and each full bank expression. Formula insertion uses a complete RHS slot; it never blindly replaces x or y throughout text. `easy_components` contains explicit arithmetic stage masks; `calculation` supplies independent exact derivatives for bank correctness. A nonunit coefficient is inserted into every additive contribution, including both numerator terms of rational partials. Trig commands have explicit lexical separators, so implicit xy and sequential theta/r products are parsed and printed correctly. Named-function replacement touches only actual function labels, never variables or TeX command text.

All source solution prose paragraphs and every final mathematical stage replay in sequence. Generated math uses conventional \sin/\cos/\ln rather than imported invisible application glyphs; brace/spacing conventions and punctuation inside displays are normalized. This is not byte-exact worked-solution reproduction: validation reports that denominator honestly, separately from complete mathematical-stage/prose fidelity. Raw source strings are unchanged in source.json. There is one fixed solution, independent of answer selection.

The source-format anomalies and minimal repairs are:

| Source | Raw evidence | Generated treatment | Fidelity denominator |
|---|---|---|---|
| q-37192 | Two fields both key selection; legacy lacks ref. Original MA JSON/screenshot shows one five-option widget. | One field; preserve both full banks as current/legacy replay profiles. Existing current correct ref selects 2r²cos(2theta)+r²sin(2theta). | 10/10 values, 2/2 banks; only one captured designation can match. |
| q-37196 | One five-choice widget, no correct marker/ref/difficulty/solution. | Independent derivative of ln(r(cos(theta)+sin(theta))) is 1/r; add mathematically derived ref, author easy assignment and common-method solution. | 5/5 values; 0 original designation available, never claimed matched; no original solution fidelity. |
| q-94999 | Generic radial chain formula labels its second partial as g, although function is h. | g→h only in that label. | Source teaching-label repair, not raw exact match. |
| q-95113 | Polar partial block labels the zero first partial as g_y. | First derivative label y→x. | Source teaching-label repair. |
| q-95116 | Polar partial block labels first partial as w_y. | First derivative label y→x. | Source teaching-label repair. |

Original MA authoritative widget evidence is saved in original-widgets.json; inspected screenshots are `/home/jake/Developer/MA/DATA/Lessons/1942/Source/Sections/03-question-37192.png` and `04-question-37196.png`. Both screenshots have exactly one radio widget with five options. Neither screenshot supplies the missing q-37196 designation. No source mathematical choice needs a value correction or exclusion.

Every complete observed/default/authored bank is rejected as a whole on equivalent values or a missing/ambiguous correct answer. Default authored easy operations include omitted coordinate derivatives/contributions, incorrect derivative target, lost power/Jacobian factors, reciprocal factors and sign errors; these are author metadata, with no invented distractor diagnosis in the learner solution. Moderate/hard defaults use correct, negated correct, one dropped radial factor, x-only contribution and y-only contribution, with eligibility enforced by whole-bank checks. Source profiles retain all five patterns rather than taking the first valid distractors.

No plots occur in these practices; steps 5/7 require no asset generator. No blank fields exist, so blank equivalence and the native “round” wording limitation do not apply. Native radio grading checks all five owned answer IDs, while independent exact mathematics checks every displayed option and row.

## Basis-2370 additional source evidence

The five newly captured families are recorded, without expanding the frozen
sampler. Every bank below is a complete source expression-pattern profile at
its original parameters; no inferred psychological recipe is claimed and no
sampling bounds are assigned. The `*` marks the independently verified correct
value. The unchanged raw strings, source UUIDs, field UUIDs and answer UUIDs are
in `reference/replenishment/initial-snapshot.edn`. Comparison normalizes doubled
TeX command escaping and imported trig glyphs only. This is a comparison view,
not a transaction to repair source content.

- q-95108, p=2x+y², theta: r² sin²(theta)−2r cos(theta);
  r² sin(2theta); *r² sin(2theta)−2r sin(theta); −2r² cos(theta);
  −2r² sin(2theta)+r sin(theta). Solution: generic rule, partials (2,2y),
  polar partials (2,2r sin(theta)), substitution, distribution, double-angle
  collection. Preserve the 3-row final sequence. The prose n/p error is flagged.
- q-165280, f=2y−xy, theta: 2r sin(theta)−r cos(theta);
  cos(theta)−r² sin(2theta); *2r cos(theta)−r² cos(2theta);
  r(sin(theta)+cos(2theta)); r²(cos(theta)+sin(2theta)). Solution: rule,
  partials (−y,2−x), polar partials, substitution, distribution, square
  grouping, double-angle conversion, final reorder: 5 final rows.
- q-95115, h=x²−y², r: r² cos(2theta); *2r cos(2theta);
  2r cos²(theta); 2r sin(2theta); 2r sin²(theta). Solution: rule, partials
  (2x,−2y), polar partials, substitution, difference-of-squares collection,
  double angle: 3 final rows. Subtraction of the negative y contribution is
  valid; the validator now permits this sign while checking every equality.
- q-165281, f=x²+y, theta: *r cos(theta)−r² sin(2theta);
  r²(cos(theta)−sin(theta)); the raw malformed `r(sin(2theta)+r cos(theta)`;
  r sin(theta)+r² sin(2theta); r cos(theta)+r sin(2theta). The third expression
  lacks its closing outer parenthesis, so this bank is excluded rather than
  guessed or claimed as a successful complete-bank replay. Solution: rule,
  partials (2x,1), polar partials, substitution, double-angle collection,
  final reorder: 3 final rows.
- q-95111, q=xy, theta: r² cos(2theta)−sin(2theta); *r² cos(2theta);
  −2r cos(theta); r² sin(2theta); r² sin(2theta)+cos²(theta).
  Solution: rule, partials (y,x), polar partials, substitution, distribution,
  square grouping, double-angle conversion: 4 final rows.

All supported frozen source banks were replayed again: 40/40 values, 8/8
complete banks and all 6 previously available reference designations. The
basis-1356 missing references remain described as derived, even though current
q-37196 is complete. Current original bank correctness is reported independently;
excluded new families do not inflate the frozen generator's fidelity denominator.
