# Template extraction

Every source is described separately in source-cases.json (observed exact parameters, field type, template and profile), source.json (unaltered evidence), and template-extraction.json (every source answer ID/value mapped one-to-one to its recipe index). Original and generated renderings appear side by side in review.md. The calculus domain is real x, nonzero slope, and ordered finite real limits.

Indefinite pattern: integrate a exp(kx+b); set u=kx+b, dx=du/k, take the constant outside, integrate exp(u), substitute back and add C. Preserve each source's radio field key selection and five options. Product pattern first combines equal linear exponents before the same substitution. Definite pattern also transforms both limits and evaluates a/k times the exponential difference. Blanks retain field-1, one delimiter-free exact answer, and no invented feedback/distractors.

Recipe order follows original banks:

- legacy q-13733: kE, -E, E, -(a/k)E, (a/k)E where E=exp(kx); a>0,k<0.
- fraction-shift q-113833: exp(x+b)/k, -E/k, E/k, kE, E. a=1, 0<k<1; shift b includes negative, zero and positive values.
- scaled q-13732: (k/a)E, aE, (a/k)E, kE, (a/k)exp(ax). Positive unequal a,k, k!=1.
- unit-definite q-30923: exp(-1), e-1, e, H, 1/H; a=k=1/H, L=0,H>1, fixed transformed limits 0 and 1. Different H gives different integrands/bounds, despite identical answer.
- positive-log q-13775: a/k, (a/k)(n^k+1), (a/k)(n^k-1), (a/k)n^k, n^k-1; log base n>1, L=0.
- negative-log q-13786: a*(20/9), a*(20/81), a*(2/27), a*(16/9), a*(8/81); fixed k=-4,n=3,b=0. These explicit observed ratios replay every value; their pedagogical error interpretation is unresolved. Only outer a varies; no claim of inferred slope/base recipes.
- negative-coefficient-log q-30922: a*(5/16), a*(15/32), a*(3/16), a*(15/16), a*(5/8); fixed k=-2,n=4,b=0, negative a. Observed ratios, unresolved error interpretation; only outer a varies.
- product q-51160: kE, E/k, -exp(x^2)/k, E, exp(kx/2)/k; two factors exp(kz/2), a=1,b=0,k>0. Original z is preserved for presentation and alpha-normalized for duplicate detection.
- All four blank profiles: exact a/k*(exp(kH+b)-exp(kL+b)), one canonical bank value.

All source choices are complete mathematical expressions including the integration constant when indefinite. No mixed banks. Any equivalent pair or multiple correct choice causes resampling. The inferred legacy correct designation is recorded separately from observed designations. Source parameter values are replayed before sampling.

Proposed bounds are explicit extensions: signed outer magnitudes 2..20 and slope magnitudes 2..10 retaining observed signs; reciprocal slopes 1/d for d=2..10; shifts -5..5 (fraction template) or -4..4 in other sampled non-log templates; logarithmic-limit families keep zero shift; logarithm bases 2..6; product slopes even 2..12. Numeric bounds remain the source bounds (0,2) or (-1,0). Sparse negative-log banks fix slope/base. Unit-limit template varies H=2..10. Boundary validation additionally tests magnitudes 1 and 20 and admissible signs. No unsupported hard extension.

Rendered TeX is standardized, so literal-string fidelity is reported separately from complete mathematical bank/prompt fidelity. Definite solution row counts are preserved by source: 5,9,10,8,9,8,6,7 respectively; product has its preliminary combination and five integration rows. Source differential-variable mistakes are corrected with the evidence in classification.md. The legacy missing solution is newly authored. Shared instructional sentences and substitution sequence are preserved. No original records are edited.
