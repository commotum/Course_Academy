# Four extraction stages

## 1. Specific sources

`source.json` retains every captured field, UUID, answer value, prose sentence,
and missing attribute. `templates.json` freezes complete mathematical component
masks rather than importing live capture utilities. `source-cases.json` gives
all eight original parameters and their public evidence profile. No template
uses an original-parameter literal-payload shortcut: every replay runs the same
coefficient/factor recipes used for changed parameters.

q1889 has f=csc(x)+2tan(x)−cos(x), five complete derivative expressions and no
rating/key/solution. The local authoritative 1686 widget confirms all five
values (its order differs from EDB); `authoritative-widget-q1889.json` preserves
that complete widget. Differentiation uniquely identifies the first EDB value.
q31283 has f=x²−6csc(x), an easy radio, and the ordered formal-derivative,
substituted-derivatives, collected-result chain. q104316 has f=e^x csc(x), a
moderate product-rule chain ending in factored e^x csc(x)(1−cot(x)), no fields.
q313722 is a moderate blank for h=4x csc(x), product-rule formal operand,
substituted two products, then distributed result. q105299 is moderate f=2^x
csc(x), with formal, substituted and factored rows plus five radio choices.
q340582 is a moderate blank h=ln(x)csc(x), with formal, two substituted products,
and distributed reciprocal/log result. q105298 is hard f=ln(x)−5csc(x), first
three derivative rows, then explicit pi/2 substitution, 1 and 0 trig values,
and collection; five scalar radio values. q313723 is a hard blank g=csc(x)−2x³
+cos(x), three derivative rows and four evaluation rows at pi/4. Its first
formal operand erroneously begins −csc(x), while its prompt, all later rows,
and answer consistently use +csc(x).

## 2. Shared patterns and boundaries

Easy sums apply the memorized cosecant derivative and established elementary
rules term by term. Moderate products apply one product rule, keeping each
factor's argument x. Hard sums add one familiar-angle substitution to the same
first derivative calculation. All outputs keep one worked solution independent
of learner choice. Function names, number of terms, powers, independent
variable, derivative order, operation order and answer fragment are fixed
roles. No change introduces chain rules, higher derivatives or tangent lines.

## 3. Complete component and bank mapping

Let C=csc(x)cot(x), S=sec²(x), N=sin(x), L=ln(b), B=b^x. The original profile
order below is EDB order; runtime shuffles complete banks after owning IDs are
fixed. Each entry is the whole mathematical answer, not an independently
compared side or fragment. The observed error operation is stated only when
supported; opaque intent is explicitly retained as a formula interpretation.

| Family | Parameter | Complete bank / correct index (zero based) |
|---|---|---|
| q1889 | c=2 | cS−C+N; cS−C−N; cS+C+N; cS−csc²(x)+N; cS+csc²(x)+N. Authored key index 0. Sign and cot/csc derivative-confusion operations. |
| q31283 | c=6 | x+cC; 2x²−cC; −2+cC; 2+cC; 2x+cC. Correct 4. First omits power factor, second retains quadratic and wrong csc sign; constant ±2 power-rule errors have historically opaque intent but are preserved literally as formula recipes. |
| q104316 | c=1 | No captured bank. Authored blank c e^x csc(x)(1−cot(x)); the original factored solution provides exact support. |
| q313722 | c=4 | Blank c csc(x)−cx csc(x)cot(x). |
| q105299 | b=2 | B csc(x)(L+cot(x)); csc(x)(BL−cot(x)); B csc(x)(L−cot(x)); csc(x)(BL+cot(x)); BL csc(x)cot(x). Correct 2. Full sign, omitted B factor on second product, and multiplied derivative patterns. |
| q340582 | c=1 | Blank c csc(x)/x−c ln(x)csc(x)cot(x). |
| q105298 | c=5, angle pi/2 | 2c; 2/pi+c; 2/pi−c; 2c/pi; 2/pi. Correct 4. Error intentions of 2c and 2c/pi are opaque; preserve as observed formula profile, do not promote an invented diagnosis. c=1 rejected because 2c/pi duplicates correct. |
| q313723 | c=2, angle pi/4 | Blank −3sqrt(2)/2−(3c/16)pi². |

The authored q105298 familiar-angle bank is chosen before parameters: correct
1/a+c csc(a)cot(a); opposite cosecant sign; omit cosecant derivative; omit log
derivative; confuse cosecant derivative with −csc². All five are evaluated
complete scalar values and must be pairwise unequal. The angle pi/2 is excluded
from this authored bank because the opposite-sign/omitted-term errors collide;
the separate exact source profile supports pi/2. No pooled-first-four logic or
single-option replacement is used.

## 4. Reusable masks and dependencies

`templates.json` preserves original masks and prose; c is the coefficient of a
whole existing term/factor and b the entire exponential base. c=1 is rendered
without a scalar where the source has an implicit coefficient; explicit source
coefficients retain their source style. No replacement targets a variable
letter or command argument. q313723's c, 3c and 3c/16 slots synchronously change
the supplied polynomial, derivative, evaluated polynomial contribution, and
final answer while preserving all original rows. q105299's b changes both
exponential bases and every ln(b), including every wrong option. q104316's
c changes the complete exp(x) factor in the prompt and both product-rule terms.
q340582's c changes the complete log factor, its reciprocal derivative, and
both final terms. The fixed solutions retain source prose and operative stages;
q1889's missing solution follows the same three-row sum-rule structure and
q104316 gains an authored source-shaped blank placeholder.

Hard authored evaluation retains formal derivative, substituted derivatives,
collected derivative; then actual substitution, individually evaluated trig
factors, final exact scalar. The full finite domain is explicit in
`parameters_domain`, enforced identically on explicit inputs and samplers, with
bool rejected. Seeds control family/parameter choice and order only. IDs depend
on actual prompt, fixed solution, difficulty, full unordered bank and format;
mathematical keys exclude banks/profiles and order. In the pi/2 historical bank,
c does not change the actual derivative value and these variants count as one
assessed task in finite batches. Every generated blank has its exact placeholder.

Domains are real connected pole-free intervals (k*pi,(k+1)*pi), with the log
families intersected with x>0. The tan sum additionally avoids cos(x)=0. All
explicit hard angles lie inside (0,pi) and are nonpoles. No plots are required,
as all captures are symbolic expressions without mathematical assets.

Presentation normalization is separate: legacy csc⁡/cot⁡/ln⁡/sin⁡/cos⁡ become
proper TeX commands and redundant nested aligned wrappers are flattened. Raw
profile strings remain byte-exact. q313723's mathematical repair changes only
the first formal operand's erroneous minus sign, so all normal equalities
represent the actual displayed prompt. q1889 key, easy level and worked solution
and q104316 blank/key are authored completions, not observed fidelity matches.
