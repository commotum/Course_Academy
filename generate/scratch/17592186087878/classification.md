# Classification at math basis 1356

Capture lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The untouched capture wrapper is `source.json`. Eight practice questions: two easy, two moderate, one hard, and three unrated. Every source has two select fields, one integrating-factor fragment and one general-solution RHS fragment. No initial conditions appear in this KP. No plots or graphical assets occur; plot rating **none** for every template.

| Template | Source | Captured level | Generated level | Assessed calculation |
|---|---|---|---|---|
| exp_forcing | q-335402 | easy | easy | Constant P, exponential forcing, one exponential antiderivative |
| exp_cancel | q-339138 | easy | easy | Exponential factor cancels forcing exponential, integrate x |
| exp_cancel_legacy | q-335392 | unrated | easy (authored assignment) | Same cancellation, integrate x² |
| power_exp | q-335412 | moderate | moderate | P=n/x, logarithmic IF, forcing denominator cancels |
| power_constant | q-339140 | moderate | moderate | P=n/x, integrate b xⁿ, divide by xⁿ |
| power_constant_legacy | q-334915 | unrated | moderate (authored assignment) | Same reciprocal-coefficient method, original inline layout/bank |
| power_sin | q-335409 | hard | hard | P=n/x, multiply to x sin(rx), one integration by parts |
| normalize_linear | q-335069 | unrated | hard (authored assignment) | Divide nonunit derivative coefficient; one exponential IBP |
| power_cos | canonical e-21742 | not a practice source | hard (authored peer) | Same reciprocal-coefficient method and one cosine IBP |

These are eight observed Markdown/value/layout templates and one authored same-method peer. Each observed template has its complete original bank profile. `q-335409-repaired` preserves the five-choice solution field while replacing its duplicate correct choice. Nine separately labeled authored default profiles use complete operation-based banks.

Lesson route is traversed from activity `17592186087942` first-step `17592186088817` through step/next: Introduction → Integrating Factor Method → transforming KP `17592186087877` → this solving KP `17592186087878` → initial-value KP `17592186087879` → derivation tutorial. Collection order was not used. Prerequisites are direct integration and introductory integration by parts. Initial-value conditions, substitution into another ODE type, mixtures and other applications belong elsewhere and are not added.

Unrated assignments are design claims. q-335392 repeats the rated easy exponential cancellation with another direct power antiderivative. q-334915 repeats the rated moderate n/x constant-forcing calculation. q-335069 needs division into standard form plus the same single IBP prerequisite seen in hard and the canonical example; its authored hard explanation shows every operation. Hard sine/cosine peers are alternatives of equal demand, not a progression.

## Raw anomalies and supported repairs

The three unrated sources lack difficulty, both correct references, and worked solutions in EDB. The owning `/home/jake/Developer/MA/DATA/Lessons/877/Source/877.json` confirms two select-list widgets and their four-option banks for those originals; it contains no worked solutions/correct designations. We independently derive:

- q-334915: I=x², x² y=x³+C, y=x+C/x².
- q-335069: divide by 2; I=e^(x/2), ∫(3/2)x e^(x/2) dx=3(x−2)e^(x/2); y=3(x−2)+C e^(−x/2).
- q-335392: I=e^(−2x), I Q=x²; y=e^(2x)(x³/3+C).

These six supplied correct refs do **not** count as matched source designations. Their explanations are authored, not source-exact worked solutions.

q-335409 field-2 contains both `04a488da-8074-50a9-ba1d-c7e0f32bf719` and `b92c0b6e-441f-5b77-9aa7-a8dc52625f53` with the same correct function; U+2061 is the only mathematical-notation difference. Raw bank extraction preserves all five values. Explicit original-profile generation with fixed parameters returns marked evidence-only raw replay; normal defaults use the repaired/authored profile, replacing the duplicate with the same particular solution plus C/x instead of C/x². Choice count and the designated correct value remain unchanged. Exact raw bank extraction, safe normal bank reproduction and stored correct designations have separate denominators.

Several captured answer values double-escape TeX command backslashes. Raw strings remain untouched in `source.json`; generated strings use one command backslash. This is notation normalization, not an algebraic repair. The five captured full worked solutions and all eight prompts reproduce byte-for-byte at original parameters.
