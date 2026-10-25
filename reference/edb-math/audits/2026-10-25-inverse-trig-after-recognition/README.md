# Inverse-trig generator review after restoring recognition

Read-only review at EDB basis T7089 of topic 17592186048189 and all four
registered generators. Verified all 96 active generated questions against the
previously checked complete-calculation pool and verified the four immutable
package implementations. Each KP has 8 easy, 8 moderate and 8 hard questions.
No active prompt supplies u or the primitive. Worked solutions supply those steps
after answering. No database changes were made in this review.

The supplied-substitution defect affected this topic and was included in the
last repair. The present questions assess complete calculation. Remaining
pedagogical weaknesses prevent an unconditional approval of the generators.

- Inverse sine and tangent have a reasonable core progression: direct standard
  form, normalization of the denominator constant, then two coefficients to
  normalize. Hard calibration is inconsistent after cancellation. Question
  17592186682785 is labelled hard but 4/(16x²+4) reduces to 1/(1+4x²).
  Cancellation is valid and should remain eligible under a suitable band.
  These two KPs have no imported hard anchors; their hard bands are authored.
- Inverse secant now distinguishes integer differential matching, fractional
  adjustment and absolute-value normalization. That progression is defensible.
  The easy banks still include the weak bare-linear-function distractor in
  seven of eight questions.
- Definite integration remains too narrow. All sixteen easy/moderate questions
  start at zero; all eight hard questions have symmetric bounds. The positive
  normalized endpoint is always 1/2 for sine or 1 for tangent. Imported hard
  q-19394 (17592186064544) instead asks for the integral from 0 to 1 of
  2/sqrt(2-x²), testing familiar small-radical normalization and a pi/4 endpoint.
  Imported q-114078 (17592186250185) similarly uses 1/sqrt(8-x²) from 0 to 2.
- Definite easy question 17592186691202 has answer 2pi/9 and distractors
  0, -2pi/9, 2pi/9+1 and 2pi/9+2. The additive offsets are generic filler.
  Imported easy q-114074 (17592186250184) uses pi/3, pi/6, pi/12, 3pi and
  pi/2, offering more comparable wrong answers. New banks should derive errors
  from omitted differential factors, incorrect normalization and bound handling.

The underlying remaining construction issues are rigid parameter patterns for
bands and generic distractor fallbacks. Correctness and removing supplied-u
prompts do not establish adequate decision variety or reliable difficulty.
Prioritize the definite generator, replace weak distractors, and assess actual
work after simplification before assigning hard labels. Preserve small numbers
and legitimate cancellations; do not manufacture difficulty through arithmetic.

Machine-readable findings: `audit.json`. Historical mathematical/engine checks:
`reference/edb-math/repairs/2026-10-25-restore-substitution-recognition/`.
