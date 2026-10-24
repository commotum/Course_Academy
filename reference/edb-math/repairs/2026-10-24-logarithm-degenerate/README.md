# Nontrivial calculator practice and fair rounding grading

Committed the question/generator repair to `math` at **T6302**. The learner
service was restarted with the tested grading change. Read-only checks through
its actual preview endpoint passed at **T6303**.

Question **17592186576201** asked for log base 17 of 17 to three decimal places.
The generator deliberately sampled a below/equal/above taxonomy, so its equal
region always supplied the identity log_a(a)=1. That region eliminated the
calculator change-of-base operation being assessed. The grader separately
treated any rounding instruction as an exact representation requirement, so
it rejected `1` against `1.000` despite their identical numerical values.

The sampler now excludes equal inputs, argument 1, base 10, and integer inputs
that are powers of a common integer base. Both below-base and above-base cases
remain. Explicit standalone construction rejects the same shortcuts. Original
source replay is retained. Capacity is calculated from the eligible finite
pools instead of the old unfiltered bound.

The complete bank contains eleven imported and five generated questions. Only
17592186576201 has the demonstrated shortcut; it is retired from future practice.
The other four generated questions and all imported questions remain unchanged.
A new immutable generator successor was registered with CAS; its original
package remains intact. The exact transaction changes only retirement and
generator registration facts, with `:agent/codex` attribution. It preserves
question identities, answers, bank membership, saved attempts, and learner facts.

For ordinary rounding instructions, the native grader now accepts plain decimal
numerals with the same exact value, including omitted or additional trailing
zeros. It does not round a submitted wrong value again: `0.8501` still differs
from `0.850`. Fractions, expressions, and scientific notation do not substitute
for the requested decimal numeral. Explicit significant-figure instructions,
instructions to retain trailing zeros, exact decimal-format instructions, and
reduced-fraction requirements retain their form checks.

Author and reviewer prompts now explicitly challenge parameter regions that
remove the assessed method and require trailing-zero grading probes. This
clarifies the existing shortcut and grading review requirements.

Validation completed:

- All **191 engine tests** and **10 native comparison tests** passed.
- An independent integer-power check covered all **840 bounded parameter pairs**.
- **150 deterministic samples** covered every response profile and below/above
  region, both requested precisions, and every radio answer rank. Answers were
  checked against an independent numerical calculation and banks checked for
  collisions. All **12 source replays** succeeded.
- The actual native learner grader passed **24 accepted** and **12 rejected**
  checks on new generated blanks.
- Three representative questions rendered in the unmodified learner UI; the
  blank example was visually inspected.
- A published, relocated copy produced 25 valid records before registration.
- Native preview and the committed receipt matched the exact expected datoms.
- The running app's read-only preview accepted `1`, `1.0`, and `1.000` for the
  reported question and rejected `1.001`, `0.999`, and `1/1`.

Past recorded task outcomes and scores were not recalculated. The grading
correction applies to subsequent submissions and read-only answer checks.

See [verification.json](verification.json),
[live-grading-verification.json](live-grading-verification.json),
[generator-verification.json](generator-verification.json), and
[dispositions.json](dispositions.json). The exact transaction, intent, preview,
receipt, and tests are retained here for review and recovery.
