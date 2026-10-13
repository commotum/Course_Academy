# Differentiating a trigonometric function using the chain rule

Captured math basis 1977, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All eleven practice sources and the canonical example were pulled together. source.json/source.edn retain every source field and original wording. No plots appear in prompts, banks or solutions. The canonical example e-732 is instructional evidence only.

Moderate: four templates, two blank and two five-option radio, with one bank profile each. Hard: five prompt/solution templates, two with usable fields (one blank and one five-option radio). q-31241 (quadratic sine slope), q-48508 (affine cosine tangent) and q-48636 (cubic cosine tangent) have no fields and are explicitly excluded. Unclassified: two radio derivative templates q-1943 and q-1946 without key, solution or rating; neither establishes an easy band. Easy remains unclassified/unsupported by this package. Every source is assigned to its own observed bank; none are pooled. Plot rating none for every template, including excluded templates.

q-1943 is cos(x²), with options x sin(2x), -x sin(x²), -2x sin(x²), x² sin(2x), x² cos(x²); differentiation supports -2x sin(x²), but no source key or difficulty is asserted. q-1946 is tan(2x+2), with options 2 csc²(2x+2), 2 cot(2x+2), 2 sec²(2x+2), 2 sec(2x+2), sec²(2x+2); differentiation supports 2 sec²(2x+2), with the same unresolved rating/key/solution limitation. The three fieldless hard sources have results 2 cos(1), y=1, y=1 respectively; the missing response structures are not inferred into generated questions.

q-310182 stores a delimited text answer `$-4\pi$`; its source bank is retained exactly as evidence. New blanks use delimiter-free mathematical values and preserve field key and fragment shape. q-310179 stores bare {sec} notation; generated answers use \sec. These are generated-content corrections only. Actual source grading rejects the equivalent -4*pi entry for q-310182 because its bank is lexical text; reference/source-grading-summary.json retains that failure and all other supported original grading results. This unchanged source is excluded from validated availability. Correctness, source-bank fidelity and actual grading are checked separately.


## q-1943 (unclassified)

Calculate $\frac{df}{dx}$ for $f(x) = \cos (x^{2})$.

Fields: :answer-field.type/radio. Unrated and missing key/solution; difficulty unresolved

## q-1946 (unclassified)

Find $f^{′}(x)$ for $f(x) = \tan (2x + 2)$.

Fields: :answer-field.type/radio. Unrated and missing key/solution; difficulty unresolved

## q-310182 (hard)

Find the slope $m$ of $y =\sin \left(\pi \left(x^{2} + 2x - 2\right)\right)$ at $x = 1.$

$m=$
{{field-1}}

Fields: :answer-field.type/blank. Template sin-pi-quadratic-slope-blank; bank q-310182.

## q-31241 (hard)

Find the slope of $y=\operatorname{sin}({x}^{2}+2x-1)$ at $x=0.$

Fields: . Missing fields; answer shape unresolved

## q-48508 (hard)

Find the equation of the tangent to the curve $y = \cos (5x-2 )$ at the point $\left(\dfrac 2 5,1\right).$

Fields: . Missing fields; answer shape unresolved

## q-48636 (hard)

Find the equation of the tangent to the curve $f(x) = \cos{\left(x^3\right)}$ at the point $\left(0,1\right).$

Fields: . Missing fields; answer shape unresolved

## q-310179 (moderate)

Given that $y=\operatorname{tan}⁡(3{x}^{4}-5)$, find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

Fields: :answer-field.type/blank. Template tan-polynomial-blank; bank q-310179.

## q-310180 (moderate)

Find the slope $m$ of the tangent to the curve $y=\operatorname{sin}⁡(3x)$ at $x=\frac{\pi }{6}.$

$m=$
{{field-1}}

Fields: :answer-field.type/blank. Template sin-special-slope-blank; bank q-310180.

## q-31153 (moderate)

Find the slope of the tangent to the curve $y=\operatorname{sin}⁡(3x+5)$ at the point where $x=2.$

Fields: :answer-field.type/radio. Template sin-affine-slope-radio; bank q-31153.

## q-31163 (moderate)

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y=\operatorname{cos}⁡(11-2x)-6{x}^{3}.$

Fields: :answer-field.type/radio. Template cos-plus-cubic-radio; bank q-31163.

## q-51026 (hard)

Find the equation of the tangent to the curve $y=2\operatorname{cos}⁡(x-1)$ at the point $(1+\pi ,-2).$

Fields: :answer-field.type/radio. Template cos-horizontal-tangent-radio; bank q-51026.