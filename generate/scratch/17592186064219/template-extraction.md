# Template extraction

Easy family: n/(1+b x²), u=s x, dx=du/s. Moderate family: n/(b+x²), factor b, u=x/s, dx=s du. Here s=√b, c=n/s, n,b>0. The domain is all real x and C is arbitrary real. Easy permits observed perfect squares and squarefree radicands 2,3,5,6; moderate sources use perfect squares. Source alternative asin values are assessed on their real branches; arcsec has its usual |argument|≥1 domain and cannot equal the global atan antiderivative.

Each original solution keeps its original fixed wording, differential relation, alignment, normalization stages and final notation. extract.py replaces only numerator and computed coefficient components, leaving the original denominator scale fixed. contract.json stores every complete source bank, prompt/solution template and parameter tuple.

The seven nonunit profiles vary n within 2..30 subject to source simplification constraints and five distinct option derivatives. Unit-numerator profiles and the n=s cancellation profile stay at the observed tuple. This deliberately narrower capability preserves omitted unit scalars and observed arithmetic layout; it is not evidence that wider sampling is impossible. Full finite limits are in capabilities.json.

Every recipe below includes +C. Each observed option is assigned in original order, not inferred from a pooled bank. The symbolic expressions are observed mathematical patterns; their psychological interpretations remain unspecified. No mistake labels or inferred feedback appear to learners.

## q-49540

Source entity 17592186064874; easy; n=6, b=9, s=√9; perfect square denominator; equation prompt; one radio `selection` field; no plots. Numerator policy: bounded variable numerator.

$\int \frac{@@N@@}{1+9{x}^{2}}\,\text{d}x=$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `n atan(sx)+C` | `$6\operatorname{arctan}⁡(3x)+C$` | no |
| 2 | `atan(sx)/s+C` | `$\frac{\operatorname{arctan}⁡(3x)}{3}+C$` | no |
| 3 | `c asin(sx)+C` | `$2\operatorname{arcsin}⁡(3x)+C$` | no |
| 4 | `c atan(sx)+C` | `$2\operatorname{arctan}⁡(3x)+C$` | yes |
| 5 | `asin(sx)/s+C` | `$\frac{\operatorname{arcsin}⁡(3x)}{3}+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-49548

Source entity 17592186064876; moderate; n=1, b=9, s=√9; perfect square denominator; equation prompt; one radio `selection` field; no plots. Numerator policy: fixed source tuple.

$\int \frac{1}{9+{x}^{2}}\,\text{d}x=$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `atan(x/b)/b+C` | `$\frac{1}{9}\operatorname{arctan}⁡(\frac{x}{9})+C$` | no |
| 2 | `atan(x/s)+C` | `$\operatorname{arctan}⁡(\frac{x}{3})+C$` | no |
| 3 | `c atan(x/s)+C` | `$\frac{1}{3}\operatorname{arctan}⁡(\frac{x}{3})+C$` | yes |
| 4 | `c atan(x/b)+C` | `$\frac{1}{3}\operatorname{arctan}⁡(\frac{x}{9})+C$` | no |
| 5 | `atan(x/b)+C` | `$\operatorname{arctan}⁡(\frac{x}{9})+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-114033

Source entity 17592186250166; easy; n=3, b=36, s=√36; perfect square denominator; calculate prompt; one radio `selection` field; no plots. Numerator policy: bounded variable numerator.

Calculate $\int \frac{@@N@@}{1+36{x}^{2}}\,\text{d}x.$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `atan(x/s)+C` | `$\operatorname{arctan}⁡(\frac{x}{6})+C$` | no |
| 2 | `(s/n) atan(sx)+C` | `$2\operatorname{arctan}⁡(6x)+C$` | no |
| 3 | `c atan(x)+C` | `$\frac{1}{2}\operatorname{arctan}⁡(x)+C$` | no |
| 4 | `c atan(x/s)+C` | `$\frac{1}{2}\operatorname{arctan}⁡(\frac{x}{6})+C$` | no |
| 5 | `c atan(sx)+C` | `$\frac{1}{2}\operatorname{arctan}⁡(6x)+C$` | yes |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-114035

Source entity 17592186250167; easy; n=1, b=5, s=√5; nonsquare radicand; calculate prompt; one radio `selection` field; no plots. Numerator policy: fixed source tuple.

Calculate $\int \frac{1}{1+5{x}^{2}}\,\text{d}x.$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `b atan(sx)+C` | `$5\operatorname{arctan}⁡(\sqrt{5}x)+C$` | no |
| 2 | `c atan(sx)+C` | `$\frac{\sqrt{5}}{5}\operatorname{arctan}⁡(\sqrt{5}x)+C$` | yes |
| 3 | `s atan(sx)+C` | `$\sqrt{5}\operatorname{arctan}⁡(\sqrt{5}x)+C$` | no |
| 4 | `c atan(x)+C` | `$\frac{\sqrt{5}}{5}\operatorname{arctan}⁡(x)+C$` | no |
| 5 | `c atan(x/b)+C` | `$\frac{\sqrt{5}}{5}\operatorname{arctan}⁡(\frac{x}{5})+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-114036

Source entity 17592186250168; easy; n=1, b=3, s=√3; nonsquare radicand; calculate prompt; one radio `selection` field; no plots. Numerator policy: fixed source tuple.

Calculate $\int \frac{1}{1+3{x}^{2}}\,\text{d}x.$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `c atan(x)+C` | `$\frac{\sqrt{3}}{3}\operatorname{arctan}⁡(x)+C$` | no |
| 2 | `s atan(sx)+C` | `$\sqrt{3}\operatorname{arctan}⁡(\sqrt{3}x)+C$` | no |
| 3 | `b atan(sx)+C` | `$3\operatorname{arctan}⁡(\sqrt{3}x)+C$` | no |
| 4 | `atan(x/s)+C` | `$\operatorname{arctan}⁡(\frac{\sqrt{3}x}{3})+C$` | no |
| 5 | `c atan(sx)+C` | `$\frac{\sqrt{3}}{3}\operatorname{arctan}⁡(\sqrt{3}x)+C$` | yes |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-114040

Source entity 17592186250169; easy; n=4, b=2, s=√2; nonsquare radicand; calculate prompt; one radio `selection` field; no plots. Numerator policy: bounded variable numerator.

Calculate $\int \frac{@@N@@}{1+2{x}^{2}}\,\text{d}x.$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `c atan(sx)+C` | `$2\sqrt{2}\operatorname{arctan}⁡(\sqrt{2}x)+C$` | yes |
| 2 | `(n/b) atan(sx)+C` | `$2\operatorname{arctan}⁡(\sqrt{2}x)+C$` | no |
| 3 | `s atan(sx)+C` | `$\sqrt{2}\operatorname{arctan}⁡(\sqrt{2}x)+C$` | no |
| 4 | `c atan(bx)+C` | `$2\sqrt{2}\operatorname{arctan}⁡(2x)+C$` | no |
| 5 | `n atan(sx)+C` | `$4\operatorname{arctan}⁡(\sqrt{2}x)+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-114045

Source entity 17592186250171; moderate; n=8, b=16, s=√16; perfect square denominator; calculate prompt; one radio `selection` field; no plots. Numerator policy: bounded variable numerator.

Calculate $\int \frac{@@N@@}{16+{x}^{2}}\,\text{d}x.$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `c atan(sx)+C` | `$2\operatorname{arctan}⁡(4x)+C$` | no |
| 2 | `atan(x/s)+C` | `$\operatorname{arctan}⁡(\frac{x}{4})+C$` | no |
| 3 | `atan(x/s)/s+C` | `$\frac{1}{4}\operatorname{arctan}⁡(\frac{x}{4})+C$` | no |
| 4 | `c atan(x/s)+C` | `$2\operatorname{arctan}⁡(\frac{x}{4})+C$` | yes |
| 5 | `(n/b) atan(x/s)+C` | `$\frac{1}{2}\operatorname{arctan}⁡(\frac{x}{4})+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-114046

Source entity 17592186250172; moderate; n=9, b=81, s=√81; perfect square denominator; calculate prompt; one radio `selection` field; no plots. Numerator policy: fixed source tuple.

Calculate $\int \frac{9}{81+{x}^{2}}\,\text{d}x.$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `atan(x)/s+C` | `$\frac{1}{9}\operatorname{arctan}⁡(x)+C$` | no |
| 2 | `atan(sx)+C` | `$\operatorname{arctan}⁡(9x)+C$` | no |
| 3 | `atan(x/s)/s+C` | `$\frac{1}{9}\operatorname{arctan}⁡(\frac{x}{9})+C$` | no |
| 4 | `atan(x/s)+C` | `$\operatorname{arctan}⁡(\frac{x}{9})+C$` | yes |
| 5 | `s atan(x/s)+C` | `$9\operatorname{arctan}⁡(\frac{x}{9})+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-2504

Source entity 17592186290591; easy; n=1, b=16, s=√16; perfect square denominator; equation prompt; one radio `selection` field; no plots. Numerator policy: fixed source tuple.

$\int \frac{1}{1+16{x}^{2}}\,\text{d}x=$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `atan(sx)/s+C` | `$\frac{\operatorname{arctan}⁡(4x)}{4}+C$` | yes |
| 2 | `s atan(sx)+C` | `$4\operatorname{arctan}⁡(4x)+C$` | no |
| 3 | `atan(bx)/b+C` | `$\frac{\operatorname{arctan}⁡(16x)}{16}+C$` | no |
| 4 | `atan(sx)/b+C` | `$\frac{\operatorname{arctan}⁡(4x)}{16}+C$` | no |
| 5 | `atan(2sx)/(2s)+C` | `$\frac{\operatorname{arctan}⁡(8x)}{8}+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-2507

Source entity 17592186290600; easy; n=1, b=25, s=√25; perfect square denominator; equation prompt; one radio `selection` field; no plots. Numerator policy: fixed source tuple.

$\int \frac{1}{1+25{x}^{2}}\,\text{d}x=$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `atan(x)/b+C` | `$\frac{\operatorname{arctan}⁡(x)}{25}+C$` | no |
| 2 | `atan(sx)/s+C` | `$\frac{\operatorname{arctan}⁡(5x)}{5}+C$` | yes |
| 3 | `arcsec(bx)/b+C` | `$\frac{\text{arcsec}(25x)}{25}+C$` | no |
| 4 | `asin(sx)/s+C` | `$\frac{\operatorname{arcsin}⁡(5x)}{5}+C$` | no |
| 5 | `atan(bx)/b+C` | `$\frac{\operatorname{arctan}⁡(25x)}{25}+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-49505

Source entity 17592186332727; moderate; n=1, b=4, s=√4; perfect square denominator; equation prompt; one radio `selection` field; no plots. Numerator policy: fixed source tuple.

$\int \frac{1}{4+{x}^{2}}\,\text{d}x=$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `c atan(x/s)+C` | `$\frac{1}{2}\operatorname{arctan}⁡(\frac{x}{2})+C$` | yes |
| 2 | `atan(x/s)+C` | `$\operatorname{arctan}⁡(\frac{x}{2})+C$` | no |
| 3 | `c atan(x)+C` | `$\frac{1}{2}\operatorname{arctan}⁡x+C$` | no |
| 4 | `atan(sx)+C` | `$\operatorname{arctan}⁡(2x)+C$` | no |
| 5 | `s atan(sx)+C` | `$2\operatorname{arctan}⁡(2x)+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-49550

Source entity 17592186332738; moderate; n=1, b=25, s=√25; perfect square denominator; equation prompt; one radio `selection` field; no plots. Numerator policy: fixed source tuple.

$\int \frac{1}{25+{x}^{2}}\,\text{d}x=$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `c atan(x/s)+C` | `$\frac{1}{5}\operatorname{arctan}⁡(\frac{x}{5})+C$` | yes |
| 2 | `c asin(sx)+C` | `$\frac{1}{5}\operatorname{arcsin}⁡(5x)+C$` | no |
| 3 | `c asin(x/s)+C` | `$\frac{1}{5}\operatorname{arcsin}⁡(\frac{x}{5})+C$` | no |
| 4 | `c atan(sx)+C` | `$\frac{1}{5}\operatorname{arctan}⁡(5x)+C$` | no |
| 5 | `atan(x/s)+C` | `$\operatorname{arctan}⁡(\frac{x}{5})+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-49551

Source entity 17592186332739; moderate; n=2, b=64, s=√64; perfect square denominator; equation prompt; one radio `selection` field; no plots. Numerator policy: bounded variable numerator.

$\int \frac{@@N@@}{64+{x}^{2}}\,\text{d}x=$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `c asin(x/s)+C` | `$\frac{\operatorname{arcsin}⁡(\frac{x}{8})}{4}+C$` | no |
| 2 | `c atan(cx)+C` | `$\frac{\operatorname{arctan}⁡(\frac{x}{4})}{4}+C$` | no |
| 3 | `asin(sx)/s+C` | `$\frac{\operatorname{arcsin}⁡(8x)}{8}+C$` | no |
| 4 | `c atan(x/s)+C` | `$\frac{\operatorname{arctan}⁡(\frac{x}{8})}{4}+C$` | yes |
| 5 | `atan(x/s)/s+C` | `$\frac{\operatorname{arctan}⁡(\frac{x}{8})}{8}+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-73714

Source entity 17592186342065; moderate; n=3, b=36, s=√36; perfect square denominator; equation prompt; one radio `selection` field; no plots. Numerator policy: bounded variable numerator.

$\int \frac{@@N@@}{36+{x}^{2}}\,\text{d}x=$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `(s/n) atan(sx)+C` | `$2\operatorname{arctan}⁡(6x)+C$` | no |
| 2 | `c atan(x/s)+C` | `$\frac{1}{2}\operatorname{arctan}⁡(\frac{x}{6})+C$` | yes |
| 3 | `atan(x/s)/n+C` | `$\frac{1}{3}\operatorname{arctan}⁡(\frac{x}{6})+C$` | no |
| 4 | `c atan(sx)+C` | `$\frac{1}{2}\operatorname{arctan}⁡(6x)+C$` | no |
| 5 | `(s/n) atan(x/s)+C` | `$2\operatorname{arctan}⁡(\frac{x}{6})+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-73713

Source entity 17592186368716; easy; n=10, b=4, s=√4; perfect square denominator; equation prompt; one radio `selection` field; no plots. Numerator policy: bounded variable numerator.

$\int \frac{@@N@@}{1+4{x}^{2}}\,\text{d}x=$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `atan(sx)/c+C` | `$\frac{\operatorname{arctan}⁡(2x)}{5}+C$` | no |
| 2 | `asin(sx)/c+C` | `$\frac{\operatorname{arcsin}⁡(2x)}{5}+C$` | no |
| 3 | `c atan(x)+C` | `$5\operatorname{arctan}⁡x+C$` | no |
| 4 | `c asin(sx)+C` | `$5\operatorname{arcsin}⁡(2x)+C$` | no |
| 5 | `c atan(sx)+C` | `$5\operatorname{arctan}⁡(2x)+C$` | yes |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

## q-114039

Source entity 17592186428006; easy; n=1, b=6, s=√6; nonsquare radicand; calculate prompt; one radio `selection` field; no plots. Numerator policy: fixed source tuple.

Calculate $\int \frac{1}{1+6{x}^{2}}\,\text{d}x.$

| Option | Recipe | Exact source value | Correct |
|---:|---|---|---|
| 1 | `c atan(sx)+C` | `$\frac{\sqrt{6}}{6}\operatorname{arctan}⁡(\sqrt{6}x)+C$` | yes |
| 2 | `b atan(sx)+C` | `$6\operatorname{arctan}⁡(\sqrt{6}x)+C$` | no |
| 3 | `s atan(sx)+C` | `$\sqrt{6}\operatorname{arctan}⁡(\sqrt{6}x)+C$` | no |
| 4 | `c atan(bx)+C` | `$\frac{\sqrt{6}}{6}\operatorname{arctan}⁡(6x)+C$` | no |
| 5 | `c atan(x)+C` | `$\frac{\sqrt{6}}{6}\operatorname{arctan}⁡(x)+C$` | no |

Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.

