import importlib.util,json,hashlib
from pathlib import Path
here=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',here.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
lesson=json.load(open('generate/runs/current/lessons/17592186050372.json'))
act=lesson['record'][0];steps={s[':db/id']:s for s in act[':activity/steps']};route=[];cur=act[':activity/first-step'][':db/id']
while cur:
 s=steps[cur];c=s[':step/content'];route.append({'step':cur,'content':c[':db/id'],'title':c.get(':knowledge-point/title',c.get(':tutorial/title'))});cur=s.get(':step/next',{}).get(':db/id')
(here/'lesson-route.json').write_text(json.dumps({'database':lesson['database'],'basis':lesson['basis'],'lineage':lesson['lineage'],'ordered_route':route},indent=2)+'\n')
md=['# Classification','Snapshot: math basis1356; lineage '+g.SOURCE['lineage']+'. Nine practice questions: five easy, two moderate, two unrated. Canonical e-10008 is context, not counted as practice.',
'Six mathematical/layout families: spaced whole-expression radio; compact whole-expression radio; supplied binomial plus remainder blanks; supplied binomial minus magnitude blanks; p/q radio; p/q blank. The nine source-mask identifiers preserve punctuation/notation variants without treating changed numbers as new skills. Six observed complete five-choice radio banks, three two-field blank layouts. Plot rating **none** throughout.',
'Unrated q-140221 receives an explicitly authored easy routing label for whole-expression rewriting; q-250390 receives moderate for coefficient identification. Public raw replay omits their difficulty, worked solution and every missing correct/choices attribute individually. Completed profiles author mathematical grading and the canonical four-stage solution, but remain evidence-only when paired with opaque original banks.',
'| Source | Captured level | Fields | Shape | a | c | q=c−a² |', '|---|---|---|---|---:|---:|---:|']
for sid,cfg in g.CONFIG.items():
 level,v,a,c,kind,shape=cfg;src=g.QUESTIONS[sid]
 md.append(f'| {sid} | {level if ":question/difficulty" in src else "unrated (authored "+level+")"} | {kind}, '+str(len(src[':question/answer-fields']))+f' fields | {shape} | {a} | {c} | {c-a*a} |')
md+=['## Curriculum bounds','The ordered route is recorded in lesson-route.json from first-step/next edges. Isolated perfect-square rewriting precedes this KP. The immediately preceding tutorial demonstrates adding and subtracting the square inside x²+10x+15. Negative linear terms belong to sibling17592186068876. Odd terms and quadratic equation solving are succeeding topics. This generator keeps a monic polynomial with positive even linear coefficient and positive constant.',
'Observed easy reaches a=11 (22y+131), requiring square121. Moderate changes the response to named coefficients p,q. Hard is an authored arithmetic extension of the same p/q response with a=12..15 and 1≤|q|≤25; all four stages remain identical. Its distinction is larger familiar square evaluation, with no new algebra. Easy/moderate retain a=1..11, c≤140, c>0, 1≤|q|≤25. Explicit calls enforce these bounds too. Radio a=1 causes the chosen complete method bank to collide and is rejected as a whole; blank layouts remain eligible. Plus/minus supplied fragments retain their required remainder signs.',
'Variable aliases, bank profiles and radio-versus-blank p/q layouts do not inflate the mathematical task count. Expression, plus-fragment and minus-fragment demands differ because their supplied notation/required fragments differ. Counts enumerate valid normal domains in validation.json.']
(here/'classification.md').write_text('\n\n'.join(md)+'\n')
md=['# Template extraction','## 1. Specific source descriptions','All originals are monic expressions with positive even linear coefficients and positive integer constants. The source record and source-cases.json preserve every prompt, field key, complete bank and solution omission. The following records give the exact displayed polynomial and requested response before generalization.']
for sid,cfg in g.CONFIG.items():
 src=g.QUESTIONS[sid];md+=['### '+sid,src[':question/problem'],'Field order/shape: '+', '.join(f[':answer-field/key']+' '+g.enum(f[':answer-field/type']) for f in src[':question/answer-fields']),src.get(':question/worked-solution','Worked solution absent; completion is authored, not recovered.')]
md+=['## 2. Shared mathematical pattern','Rewrite v²+2av+c as (v+a)²+(c−a²), or identify a and c−a² as p,q. Operative stages: decompose linear coefficient into2·a; add and subtract a² inside the expression; factor only the first three terms; collect −a²+c. Supplied minus blanks request the positive magnitude −q, not the signed remainder. No equation is solved.',
'## 3. Component maps and complete observed profiles','All source choices below use a=half the printed linear coefficient and q=c−a². A pair (r,s) means the complete polynomial (v+r)²+s, or the complete assignment p=r,q=s. Scaling a and offsetting q are faithful expression patterns; they do **not** recover the source author’s error intent. Arbitrary source scalar offsets remain explicitly opaque and evidence-only. No default uses these offsets.']
for sid,recipes in g.BANKS.items():
 src=g.QUESTIONS[sid];f=src[':question/answer-fields'][0]
 md+=['### raw:'+sid,'| Exact original option | Parameterized complete components (r,s) | Captured designation |','|---|---|---|']
 for ans,(scale,off) in zip(f[':answer-field/choices'],recipes):
  designation='correct' if ans[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id') else ('incorrect' if ':answer-field/correct' in f else 'designation absent')
  md.append('| `'+ans[':answer/value']+'` | ('+str(scale)+'·a, q'+('+' if off>=0 else '')+str(off)+') | '+designation+' |')
md+=['For blank field-1/field-2, plus/minus completion expects (v+a,q) or (v+a,−q); p/q expects (a,q). q-250390 has no choices/correct refs; field order is field-2 then field-1 in raw replay and the placeholders confirm each role independently.',
'## 4. Reusable masks, constraints and calculations','Source prompt/solution masks replace complete original polynomial strings, half-coefficient components, their squared bases, retained constants, collected signed remainders, and p/q conclusions. Variable tokens are changed only inside math and after implicit ASLOT·v components have been explicitly marked. Fixed prose and four displayed stages are retained exactly. Each mask replays through the normal generate API; no branch returns a literal question record or precomputed answer bank.',
'Normal five-choice method profile is chosen before parameters: (a,c−a²), (a,c), (a,c−a), (a,c+a²), (2a,c−(2a)²). These respectively assess the correct square correction, omitted correction, subtracting the half coefficient instead of its square, adding instead of subtracting, and using the full linear coefficient as binomial shift. Whole complete polynomials/assignments must remain unequal; any collision rejects the entire instance. Source profiles preserve their complete five-option banks, never pooled subsets.',
'Raw replay keeps attribute omissions. Completed profiles supply mathematically inferred answers p=7,q=−18 and (y+6)²−21, with the same canonical solution prose. Missing captured correct designations are excluded from matched-designation denominators. No captured mathematical error or duplicated equivalent bank was found. The original MA widget at /home/jake/Developer/MA/DATA/Lessons/450/Source/450.json independently confirms the unrated q-140221 five-choice bank and q-250390 two ordered entry slots. Its SHA256 is recorded in provenance.json.',
'TeX byte inspection confirms ordinary single backslashes before cdot in decoded source strings. No double-slash repair was applied. Source grouped closing-parenthesis notation and subscript underbrace marker are preserved; all generated math has balanced braces/delimiters and no unintended C0 controls. No plots or plot assets occur; steps5/7 require no renderer.']
(here/'template-extraction.md').write_text('\n\n'.join(md)+'\n')
p=Path('/home/jake/Developer/MA/DATA/Lessons/450/Source/450.json')
(here/'provenance.json').write_text(json.dumps({'capture':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'authoritative_widget':str(p),'widget_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'decoded_solution_double_backslashes':{sid:q.get(':question/worked-solution','').count('\\\\') for sid,q in g.QUESTIONS.items()}},indent=2)+'\n')
(here/'README.md').write_text('''# Completing the square on a quadratic expression

Run `.venv/bin/python generate/scratch/17592186068875/validate.py`.
Preview `.venv/bin/python generate/scratch/17592186068875.py --difficulty all --count 2 --format markdown`.

Basis1356, nine sources, all three levels. Normal generation samples every eligible observed layout with a complete method-derived bank. `--profile raw:<source-id>` preserves original banks and missing attributes; `completed:<source-id>` adds explicitly authored missing grading/solutions. Both historical-bank modes are evidence-only. `--field-type radio|blank` filters eligible families. Explicit source parameters are in source-cases.json. No database writes or registrations.

Scope: positive even linear coefficient, monic expression, completing square by adding and subtracting the half coefficient squared. Hard is authored familiar-square arithmetic (half coefficient12–15), preserving the p/q response and four-stage canonical method. No equation solving, odd terms or negative linear-term prompts.

Validation independently reads printed polynomial, decomposition, square addition/subtraction, factoring, collection, conclusion and fragments; checks complete source banks, presence parity, identity, finite variety and formatting; then exercises real native grading with equivalent and wrong blank entries and every radio option. See validation.json for separate denominators.
''')
