# Reciprocal-trigonometric tangent slopes: draft classification

This draft uses the exact refreshed math basis2275 wrapper, lineage
`01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is an unchanged byte copy.
The registered numeric script and its entire 97-path evidence/cache tree were
hashed before generator imports; `registered-baseline.json` includes paths,
kinds, modes, sizes, file SHA256s and manifest status. All Python entrypoints set
`sys.dont_write_bytecode=True`. The draft never imports the numeric generator,
and validation rechecks its full baseline after execution.

| MA source | Observed difficulty | Assessment | Stable method/stages | Plots |
|---|---|---|---|---|
| q1886 | moderate | radio, 5 | cosine−secant+reciprocal sum at sqrt(3); explicit reciprocal-power rewrite | none |
| q1905 | easy | radio, 5 | linear−scaled secant sum at pi/4; zero slope is valid | none |
| q104437 | moderate | fields absent | x*cot(x), product derivative then pi/4 evaluation | none |
| q340642 | moderate | blank | csc*cot product; factor csc; pi/2 evaluation | none |
| q104442 | easy | radio, 5 | sec/sqrt(3)+quadratic/pi; pi/3 evaluation | none |
| q1904 | easy | radio, 5 | negative quadratic+scaled csc; pi/6 evaluation | none |
| q340630 | easy | blank | exponential+secant; pi evaluation with zero tangent contribution | none |
| q340660 | moderate | blank | linear/secant quotient; factor and cancel one secant; zero evaluation | none |
| q70874 | easy | radio, 5 | ln+scaled csc sum; pi/3 evaluation | none |

There are nine MA practice families, five complete radio profiles, three
captured blanks, and one fieldless record. All nine prompts and worked solutions
are retained exactly in public parameterized evidence replay. The two non-MA
records (cosine coefficients12 and16 in q1886's family) are independently
authored inventory, not recovered original templates or observed difficulty
evidence. `independent-inventory.json` preserves their complete Pull records
and the immutable wrapper provenance separately.

The lesson route follows first-step/next, not collection order: Introduction →
Mnemonic Tricks → Cosecant → Cotangent → Secant → this Slope KP → Justifying
Reciprocal Derivatives. The introduction permits combinations of reciprocal
functions, and the three preceding KPs teach their first derivatives. This KP's
key prerequisites are unit-circle special-angle ratios and finding tangent
slopes by differentiation. The topic follows the quotient-rule topic and its
canonical e3648 explicitly differentiates a trig/trig quotient. The next topic
includes Chain Rule With Trigonometric Functions, so all trig arguments stay x;
there are no composed arguments, higher derivatives or tangent-line equations.

Hard is absent from practice evidence and is explicitly authored. It uses the
canonical -a*cot(x)/sin(x) quotient at pi/6, pi/4 or pi/3. Compared with moderate
linear/secant at0 and csc*cot atpi/2, both trig derivative contributions remain
nonzero and the denominator's special-angle square must be evaluated. Every
hard variant has exactly this quotient derivative, reciprocal identity reduction
and four-row familiar-angle evaluation; none adds another rule or progression.
The three angles carry the same derivative and arithmetic stages. Coefficients
1..24 change one scalar, with original coefficient2 included. Easy/moderate
bounds likewise vary only an existing coefficient (1..24; q1886 uses2..24 to
retain its nonunit cosine factor). Exponential, polynomial powers, term counts,
source angles and existing response roles remain fixed within each observed
family.

q104437's missing fields are preserved by raw evidence omission; normal output
adds an explicitly authored scalar-slope blank supported by the existing worked
solution and sibling blank layouts. No source correct designation is claimed
for it. q1905's historical wrong constants have opaque intent. Its entire
parameterized observed bank remains publicly available with explicit
`evidence_only=true`, `eligible_for_learning=false`; the authored default bank
uses actual derivative errors and allows correct0 and1. All other original
banks are preserved as complete profiles. No plots or source images occur in
these mathematical templates, so no plot generator is needed.
