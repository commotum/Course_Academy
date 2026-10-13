"""Write source-backed classification/extraction and bounded capabilities."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
s=json.loads((P/'source.json').read_text());qs=s['record'][':knowledge-point/questions'];cases=json.loads((P/'source-cases.json').read_text())
def write(name,text):(P/name).write_text(text.strip()+'\n')
write('classification.md',f'''# General exponential functions with linear exponents

Captured math basis {s['basis']}, lineage {s['lineage']}. source.json and reference/initial preserve all 11 practice records and canonical e-460. No registered generator or job .generated file existed. Source plots: none; no new assets required.

| Difficulty/evidence | Field types | Structural families | Complete bank profiles | Source IDs |
|---|---|---|---|---|
| Easy rated | radio, one selection field with five choices | 2: integer-slope indefinite substitution; reciprocal-slope indefinite substitution with reversed differential statement | 3 | q-31412, q-31413; q-31417 |
| Moderate rated | radio; single exact blank field-1 | 3: definite radio substitution; negative-slope blank substitution with optional outer scale; positive unit-slope blank substitution omitting unnecessary coefficient pull | 1 radio bank; blanks have no distractor profile | q-30973; q-349625, q-349626, q-349631; q-349646, q-349648 |
| Unrated legacy | radio, five choices, correct designation and solution absent | 1: What is indefinite integral prompt; missing solution authored using canonical e-460 | 2 retained profiles | q-31405, q-31418 |
| Hard | none observed | 0 supported | 0 | none |

Changed numeric values within these groups do not create additional structural templates. Eleven source replay cases keep the source parameters, profiles and conditional solution shapes explicit. Legacy sources never count as available inventory. Their independent easy generation is an explicit classification extension, supported by the same linear substitution and full bank replay. Hard remains unsupported within this package; new source evidence reopens classification.

Original step sequences: integer easy: differential, substitute, pull reciprocal slope, integrate using log(base), back-substitute; reciprocal easy: same sequence with dx isolated on the left. Moderate: differential, limit table, substitute with coefficient, conditionally pull coefficient, evaluate primitive at transformed limits, expand base powers and simplify. The unit-slope moderate sources omit an unnecessary coefficient line. See review.md for originals/replays/variants side by side, and template-extraction.json for every source option.

All real bases are positive and unequal to 1; linear slopes are nonzero. Definite x limits are ordered even when transformed limits reverse. No source mathematical error was found. Two legacy records lack validated difficulty/correct designation/solution; they remain untouched and unavailable.
''')
write('template-extraction.md',r'''# Template extraction

Every source-specific prompt, solution, original parameter tuple, field type, choice value and recipe index is retained in template-extraction.json. source-cases.json maps every source to its complete bank. Recipes in bank() are mathematical expressions, not pooled labels. Psychological interpretations remain unresolved where the evidence only establishes a numerical expression.

Shared pattern: integrate a n^(kx+b), using u=kx+b and dx=du/k. The indefinite answer is a n^(kx+b)/(k ln n)+C. Definite answers evaluate that primitive at H and L; negative k reverses the transformed limits without changing the ordered x bounds. Fields preserve selection/radio with five owned choices, or field-1/blank with one canonical exact value. Answers are delimiter-free TeX; questions preserve the integral and field placeholder layout. No distractor feedback is added.

Write E=n^(kx+b), J=ln n, d=1/k, D=n^k-1. The complete observed profiles, in recipe order, are:

- q-31405: E/J; n^(kx/2+b)/k; E/k; E/(kJ); n^(kx/2+b)/J.
- q-31418 (k=-1, b<0): n^(-kx-b)/n; E/(kJ); -n^(-kx-b)/J; -n^(kx)/J; E/J.
- q-31412 (k=-1,b=0): E/(kJ); -E; n^x/J; E/J; -n^x/J.
- q-31413 (k>1,b=0): E/(kJ); E/k; E/J; -n^(kx-7)/(kJ); n^x/J. The observed altered constant -7 remains fixed; its error interpretation is unresolved.
- q-31417 (k=1/d,b=0,n!=d): n^x/(dJ); E/(dJ); dE/J; d n^x/ln d; E/ln d.
- q-30973 (k=6,n=3,L=0,H=1 originally): D/J; D/(2n); D/(kJ); D/(2J); (n^(k-1)-1)/(2J). The coefficient 2 is an observed fixed pattern; keep it rather than inventing an error explanation. Sampling is bounded to k in {4,6,8}, n in {2,...,6}, preserving these complete mathematical recipes.
- q-349625, q-349626, q-349631, q-349646, q-349648: one exact definite answer, no distractor recipes. Original tuples are (a,k,b,n,L,H)=(1,-2,7,3,1,2),(3,-1,5,2,1,3),(2,-1,1,4,0,1),(1,1,-1,5,0,2),(1,1,1,3,-1,1).

Observed easy tuples: q-31405 (1,6,-1,2); q-31418 (1,-1,-6,3); q-31412 (1,-1,0,5); q-31413 (1,5,0,4); q-31417 (1,1/3,0,6). Proposed bounds are separate: integer bases 2..6, positive integer outer coefficient 1..5 for blanks, bounded nonzero signed slopes, shifts -4..8 for blanks and bounded ordered integer limits -2<=L<H<=4. Easy profiles retain their specific signs, zero/nonzero shifts and unit/reciprocal slope constraints. Legacy positive shifts of either sign are an explicit extension. Blank positive slopes above 1 are an explicit extension requiring the conditional coefficient-pull line. No new difficulty is inferred from larger numbers.

Standardized TeX preserves the source substitution sentences, limit-table layout and worked method; differential direction and algebraic display formatting are normalized. Source-specific legacy solutions were missing and are newly authored from canonical e-460. Literal fidelity is reported separately from mathematical fidelity; source-bank replay requires all 35 choices across 11 banks, ignoring order while retaining correct designation where present. Exact numeric strings are never reused as unexplained source literals when parameterized recipes are known.

Sampling selects a complete profile first and rejects equivalent choices, extra correct answers, invalid domains and collapsed source features. Fingerprints use the simplified integrand and actual x bounds, ignoring seeds, UUIDs, profile choice, answer order and formatting. Existing mathematical tasks and the canonical example are excluded from new submissions. Hard is rejected. Bounded searches report explicit remaining shortages instead of duplicating content.
''')
write('plot-extraction.md','No plots, graphs, diagrams or plot references occur in the eleven practice sources or canonical e-460. Plot rating: none for every template. No generated assets or rendering needed.')
write('README.md','Scoped generator for KP 17592186096656. Run ../17592186096656.py using .venv/bin/python; validate.py checks printed calculus, all solution steps, complete source banks and native grading. replenish.py uses existing EDB integration with api.lock, basis guard, exact retained request and receipt/readback. Easy and moderate are supported; hard remains explicitly unsupported. Classification/extraction/review/validation and reference/replenishment retain evidence.')
caps=dict(knowledgePoint=17592186096656,source_basis=s['basis'],lineage=s['lineage'],supported_levels=['easy','moderate'],unsupported_levels=['hard'],unsupported_levels_filled=False,bounded_candidate_scan={'easy':1000,'moderate':1000},exceptions=[dict(level='hard',kind='unsupported',nominal_shortage=5,reason='No observed hard source family; numeric size changes cannot establish hard difficulty. Reopen on new source evidence.'),dict(kind='incomplete-source',sources=['q-31405','q-31418'],reason='Originals lack difficulty, correct designation and worked solution; retained and excluded. New easy variants use independent calculus verification and canonical substitution.'),dict(kind='narrow-profile',sources=['q-30973'],reason='Sparse radio evidence constrains limits 0..1, even slope 4/6/8, zero shift and unit outer coefficient; all recipes fully replayed.'),dict(kind='sampling-extension',sources=['q-31405','q-349646','q-349648'],reason='Signed legacy-positive shifts and positive nonunit blank slopes are explicit easy/moderate extensions of the same substitution method, with conditional solution steps.')])
(P/'capabilities.json').write_text(json.dumps(caps,indent=2)+'\n')
