# Templates and complete bank recipes

The source-specific tables below preserve every original option with its exact pattern recipe. Recipes are complete observed banks, never pooled. See contract.json for literal prompt and ordered full solution templates and reference/registered-template-extraction.md for the original extraction. Psychology of mistakes is not inferred.

Source-scale substitution replaces only explicitly assigned b and √b numeric roles while protecting every exponent 2. Numerator/coefficient tokens come from one n,b instance. Unit-numerator profiles keep n=1 because omitted unit factors are part of those solution layouts; cancellation q-114046 keeps n=√b. Integral-valued source coefficient templates keep that relation. This preserves omitted factors and arithmetic layout rather than imposing arbitrary original denominators.

Square scales sample √b=2..12; nonsquare easy radicands sample {2,3,5,6,7,10,11,13}. Scaled numerator templates vary n within the declared candidate policy (unit profiles fixed n, cancelled profile tied n, integer-coefficient profiles n=m√b, m=2..7, other profiles n=2..16). Original tuples are explicitly included. Complete profile first, then parameters: any wrong/correct or wrong/wrong equivalent derivative rejects the whole instance modulo C. No first-valid pooled distractor selection occurs. H samples n=1..17,a=2..9,s=2..12 and uses one explicitly authored five-option bank.

## q-49540 — easy

Observed n,b=[6, 9]; perfect square denominator; equation; no plots.

$\int \frac{6}{1+9{x}^{2}}\,\text{d}x=$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`n atan(sx)`|`6\operatorname{arctan}⁡(3x)+C`|False|
|2|`atan(sx)/s`|`\frac{\operatorname{arctan}⁡(3x)}{3}+C`|False|
|3|`c asin(sx)`|`2\operatorname{arcsin}⁡(3x)+C`|False|
|4|`c atan(sx)`|`2\operatorname{arctan}⁡(3x)+C`|True|
|5|`asin(sx)/s`|`\frac{\operatorname{arcsin}⁡(3x)}{3}+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-49548 — moderate

Observed n,b=[1, 9]; perfect square denominator; equation; no plots.

$\int \frac{1}{9+{x}^{2}}\,\text{d}x=$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`atan(x/b)/b`|`\frac{1}{9}\operatorname{arctan}⁡(\frac{x}{9})+C`|False|
|2|`atan(x/s)`|`\operatorname{arctan}⁡(\frac{x}{3})+C`|False|
|3|`c atan(x/s)`|`\frac{1}{3}\operatorname{arctan}⁡(\frac{x}{3})+C`|True|
|4|`c atan(x/b)`|`\frac{1}{3}\operatorname{arctan}⁡(\frac{x}{9})+C`|False|
|5|`atan(x/b)`|`\operatorname{arctan}⁡(\frac{x}{9})+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-114033 — easy

Observed n,b=[3, 36]; perfect square denominator; calculate; no plots.

Calculate $\int \frac{3}{1+36{x}^{2}}\,\text{d}x.$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`atan(x/s)`|`\operatorname{arctan}⁡(\frac{x}{6})+C`|False|
|2|`(s/n) atan(sx)`|`2\operatorname{arctan}⁡(6x)+C`|False|
|3|`c atan(x)`|`\frac{1}{2}\operatorname{arctan}⁡(x)+C`|False|
|4|`c atan(x/s)`|`\frac{1}{2}\operatorname{arctan}⁡(\frac{x}{6})+C`|False|
|5|`c atan(sx)`|`\frac{1}{2}\operatorname{arctan}⁡(6x)+C`|True|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-114035 — easy

Observed n,b=[1, 5]; nonsquare radicand; calculate; no plots.

Calculate $\int \frac{1}{1+5{x}^{2}}\,\text{d}x.$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`b atan(sx)`|`5\operatorname{arctan}⁡(\sqrt{5}x)+C`|False|
|2|`c atan(sx)`|`\frac{\sqrt{5}}{5}\operatorname{arctan}⁡(\sqrt{5}x)+C`|True|
|3|`s atan(sx)`|`\sqrt{5}\operatorname{arctan}⁡(\sqrt{5}x)+C`|False|
|4|`c atan(x)`|`\frac{\sqrt{5}}{5}\operatorname{arctan}⁡(x)+C`|False|
|5|`c atan(x/b)`|`\frac{\sqrt{5}}{5}\operatorname{arctan}⁡(\frac{x}{5})+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-114036 — easy

Observed n,b=[1, 3]; nonsquare radicand; calculate; no plots.

Calculate $\int \frac{1}{1+3{x}^{2}}\,\text{d}x.$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`c atan(x)`|`\frac{\sqrt{3}}{3}\operatorname{arctan}⁡(x)+C`|False|
|2|`s atan(sx)`|`\sqrt{3}\operatorname{arctan}⁡(\sqrt{3}x)+C`|False|
|3|`b atan(sx)`|`3\operatorname{arctan}⁡(\sqrt{3}x)+C`|False|
|4|`atan(x/s)`|`\operatorname{arctan}⁡(\frac{\sqrt{3}x}{3})+C`|False|
|5|`c atan(sx)`|`\frac{\sqrt{3}}{3}\operatorname{arctan}⁡(\sqrt{3}x)+C`|True|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-114040 — easy

Observed n,b=[4, 2]; nonsquare radicand; calculate; no plots.

Calculate $\int \frac{4}{1+2{x}^{2}}\,\text{d}x.$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`c atan(sx)`|`2\sqrt{2}\operatorname{arctan}⁡(\sqrt{2}x)+C`|True|
|2|`(n/b) atan(sx)`|`2\operatorname{arctan}⁡(\sqrt{2}x)+C`|False|
|3|`s atan(sx)`|`\sqrt{2}\operatorname{arctan}⁡(\sqrt{2}x)+C`|False|
|4|`c atan(bx)`|`2\sqrt{2}\operatorname{arctan}⁡(2x)+C`|False|
|5|`n atan(sx)`|`4\operatorname{arctan}⁡(\sqrt{2}x)+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-114045 — moderate

Observed n,b=[8, 16]; perfect square denominator; calculate; no plots.

Calculate $\int \frac{8}{16+{x}^{2}}\,\text{d}x.$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`c atan(sx)`|`2\operatorname{arctan}⁡(4x)+C`|False|
|2|`atan(x/s)`|`\operatorname{arctan}⁡(\frac{x}{4})+C`|False|
|3|`atan(x/s)/s`|`\frac{1}{4}\operatorname{arctan}⁡(\frac{x}{4})+C`|False|
|4|`c atan(x/s)`|`2\operatorname{arctan}⁡(\frac{x}{4})+C`|True|
|5|`(n/b) atan(x/s)`|`\frac{1}{2}\operatorname{arctan}⁡(\frac{x}{4})+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-114046 — moderate

Observed n,b=[9, 81]; perfect square denominator; calculate; no plots.

Calculate $\int \frac{9}{81+{x}^{2}}\,\text{d}x.$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`atan(x)/s`|`\frac{1}{9}\operatorname{arctan}⁡(x)+C`|False|
|2|`atan(sx)`|`\operatorname{arctan}⁡(9x)+C`|False|
|3|`atan(x/s)/s`|`\frac{1}{9}\operatorname{arctan}⁡(\frac{x}{9})+C`|False|
|4|`atan(x/s)`|`\operatorname{arctan}⁡(\frac{x}{9})+C`|True|
|5|`s atan(x/s)`|`9\operatorname{arctan}⁡(\frac{x}{9})+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-2504 — easy

Observed n,b=[1, 16]; perfect square denominator; equation; no plots.

$\int \frac{1}{1+16{x}^{2}}\,\text{d}x=$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`atan(sx)/s`|`\frac{\operatorname{arctan}⁡(4x)}{4}+C`|True|
|2|`s atan(sx)`|`4\operatorname{arctan}⁡(4x)+C`|False|
|3|`atan(bx)/b`|`\frac{\operatorname{arctan}⁡(16x)}{16}+C`|False|
|4|`atan(sx)/b`|`\frac{\operatorname{arctan}⁡(4x)}{16}+C`|False|
|5|`atan(2sx)/(2s)`|`\frac{\operatorname{arctan}⁡(8x)}{8}+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-2507 — easy

Observed n,b=[1, 25]; perfect square denominator; equation; no plots.

$\int \frac{1}{1+25{x}^{2}}\,\text{d}x=$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`atan(x)/b`|`\frac{\operatorname{arctan}⁡(x)}{25}+C`|False|
|2|`atan(sx)/s`|`\frac{\operatorname{arctan}⁡(5x)}{5}+C`|True|
|3|`arcsec(bx)/b`|`\frac{\text{arcsec}(25x)}{25}+C`|False|
|4|`asin(sx)/s`|`\frac{\operatorname{arcsin}⁡(5x)}{5}+C`|False|
|5|`atan(bx)/b`|`\frac{\operatorname{arctan}⁡(25x)}{25}+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-49505 — moderate

Observed n,b=[1, 4]; perfect square denominator; equation; no plots.

$\int \frac{1}{4+{x}^{2}}\,\text{d}x=$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`c atan(x/s)`|`\frac{1}{2}\operatorname{arctan}⁡(\frac{x}{2})+C`|True|
|2|`atan(x/s)`|`\operatorname{arctan}⁡(\frac{x}{2})+C`|False|
|3|`c atan(x)`|`\frac{1}{2}\operatorname{arctan}⁡x+C`|False|
|4|`atan(sx)`|`\operatorname{arctan}⁡(2x)+C`|False|
|5|`s atan(sx)`|`2\operatorname{arctan}⁡(2x)+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-49550 — moderate

Observed n,b=[1, 25]; perfect square denominator; equation; no plots.

$\int \frac{1}{25+{x}^{2}}\,\text{d}x=$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`c atan(x/s)`|`\frac{1}{5}\operatorname{arctan}⁡(\frac{x}{5})+C`|True|
|2|`c asin(sx)`|`\frac{1}{5}\operatorname{arcsin}⁡(5x)+C`|False|
|3|`c asin(x/s)`|`\frac{1}{5}\operatorname{arcsin}⁡(\frac{x}{5})+C`|False|
|4|`c atan(sx)`|`\frac{1}{5}\operatorname{arctan}⁡(5x)+C`|False|
|5|`atan(x/s)`|`\operatorname{arctan}⁡(\frac{x}{5})+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-49551 — moderate

Observed n,b=[2, 64]; perfect square denominator; equation; no plots.

$\int \frac{2}{64+{x}^{2}}\,\text{d}x=$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`c asin(x/s)`|`\frac{\operatorname{arcsin}⁡(\frac{x}{8})}{4}+C`|False|
|2|`c atan(cx)`|`\frac{\operatorname{arctan}⁡(\frac{x}{4})}{4}+C`|False|
|3|`asin(sx)/s`|`\frac{\operatorname{arcsin}⁡(8x)}{8}+C`|False|
|4|`c atan(x/s)`|`\frac{\operatorname{arctan}⁡(\frac{x}{8})}{4}+C`|True|
|5|`atan(x/s)/s`|`\frac{\operatorname{arctan}⁡(\frac{x}{8})}{8}+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-73714 — moderate

Observed n,b=[3, 36]; perfect square denominator; equation; no plots.

$\int \frac{3}{36+{x}^{2}}\,\text{d}x=$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`(s/n) atan(sx)`|`2\operatorname{arctan}⁡(6x)+C`|False|
|2|`c atan(x/s)`|`\frac{1}{2}\operatorname{arctan}⁡(\frac{x}{6})+C`|True|
|3|`atan(x/s)/n`|`\frac{1}{3}\operatorname{arctan}⁡(\frac{x}{6})+C`|False|
|4|`c atan(sx)`|`\frac{1}{2}\operatorname{arctan}⁡(6x)+C`|False|
|5|`(s/n) atan(x/s)`|`2\operatorname{arctan}⁡(\frac{x}{6})+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-73713 — easy

Observed n,b=[10, 4]; perfect square denominator; equation; no plots.

$\int \frac{10}{1+4{x}^{2}}\,\text{d}x=$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`atan(sx)/c`|`\frac{\operatorname{arctan}⁡(2x)}{5}+C`|False|
|2|`asin(sx)/c`|`\frac{\operatorname{arcsin}⁡(2x)}{5}+C`|False|
|3|`c atan(x)`|`5\operatorname{arctan}⁡x+C`|False|
|4|`c asin(sx)`|`5\operatorname{arcsin}⁡(2x)+C`|False|
|5|`c atan(sx)`|`5\operatorname{arctan}⁡(2x)+C`|True|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

## q-114039 — easy

Observed n,b=[1, 6]; nonsquare radicand; calculate; no plots.

Calculate $\int \frac{1}{1+6{x}^{2}}\,\text{d}x.$

|Option|Recipe (+C)|Exact captured value|Key|
|---|---|---|---|
|1|`c atan(sx)`|`\frac{\sqrt{6}}{6}\operatorname{arctan}⁡(\sqrt{6}x)+C`|True|
|2|`b atan(sx)`|`6\operatorname{arctan}⁡(\sqrt{6}x)+C`|False|
|3|`s atan(sx)`|`\sqrt{6}\operatorname{arctan}⁡(\sqrt{6}x)+C`|False|
|4|`c atan(bx)`|`\frac{\sqrt{6}}{6}\operatorname{arctan}⁡(6x)+C`|False|
|5|`c atan(x)`|`\frac{\sqrt{6}}{6}\operatorname{arctan}⁡(x)+C`|False|

Ordered solution stages remain literally preserved by this profile, including forward/reversed differential, quotient-final notation, radical rationalization, and raw/simplified factoring stages. Original and changed-parameter full banks appear in review.md.

