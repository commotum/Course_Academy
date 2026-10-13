"""Regenerate descriptive evidence; no question payload is used as a generator."""
import importlib.util,json,sys
sys.dont_write_bytecode=True
from pathlib import Path
P=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('gen',P.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
route=json.load(open(P.parents[1]/'runs/current/lessons/17592186050929.json'))['record'][0]
steps={x[':db/id']:x for x in route[':activity/steps']};sid=route[':activity/first-step'][':db/id'];order=[]
while sid in steps:
 step=steps[sid];c=step[':step/content'];order.append(str(sid)+': '+c.get(':tutorial/title',c.get(':knowledge-point/title','')));sid=step.get(':step/next',{}).get(':db/id')
classification='''# Classification

Source: `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The complete immutable capture wrapper is copied to source.json. There are 14 practice questions: 2 easy, 6 moderate, 5 hard, 1 unrated. All 14 contain a single five-option `radio` field with key `selection` and whole mathematical primitives followed by `+C`. No blank fields, mixed fields, or plots occur. Plot rating: **none** for every template.

The canonical example is e-491, integral of x exp(7x); the key prerequisite is Integrating Exponential Functions Using Linear Substitution (topic 1112). The lesson's introduction uses x exp(2x), chooses u=x and v'=exp(2x), applies by parts once, and then integrates the remaining exponential. Later sibling KPs handle trigonometric expressions and definite integrals; this generator does neither. Lesson traversal follows first-step/next links:

'''+ '\n'.join('- '+x for x in order)+'''

Easy varies a positive coefficient and positive exponential slope, with two arithmetic divisions and one by-parts application. Moderate retains one application but uses a negative slope, a shifted exponent, or an integer exponential base with ln(base); these are observed peer demands, not a progression. Hard replaces ax with ax+b, preserving derivative a and one residual exponential integral, with signs and final affine simplification comparable to the observed hard sources. No repeated by parts, powers beyond a linear polynomial, transcendental new factors, or definite limits are added.

| Source | Original level | Template | Parameters | Bank profile | Plots |
|---|---|---|---|---|---|
'''
for sid,name,p in g.SOURCE_CASES:
 q=g.SOURCES[sid];level=q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1]
 classification+='| '+sid+' | '+level+' | '+name+' | `'+json.dumps(p,sort_keys=True)+'` | `observed:'+sid+'` | none |\n'
classification+='''
The 12 presentation/value layouts cover all source variants, including the supported legacy base layout. Thirteen rated questions have worked solutions and correct designations. q-2425 is unrated and has neither; it receives an explicitly authored moderate level because its base-2 calculation is exactly the base-3/base-5 moderate method. The original prompt's `\\intx` is repaired to `\\int x`. The independently differentiated answer is the option `(2^x/ln 2)(x-1/ln 2)+C`; this is an inferred supported designation, never a matched original ref.

The original lesson JSON and Markdown also omit the q-2425 correct designation. Its widget is five-option multiple choice with no blanks; the local evidence copy lesson-widget-q2425.json retains this corroboration. No source question is excluded.
'''
(P/'classification.md').write_text(classification)
extract='''# Template extraction

## 1. Describe each source specifically

The table in classification.md fixes every source's original number features, field and bank assignment. Specific descriptions and complete choice mappings follow below. The exact raw prompt/solution/choice evidence is source.json and originals are printed in review.md. Source function notation sometimes has invisible Unicode application characters; generated LaTeX normalizes those to standard ln. All source values are complete primitives, not coefficient blanks.

'''
for sid,name,p in g.SOURCE_CASES:
 q=g.SOURCES[sid];t=g.TEMPLATES[name];extract+='### '+sid+'\n\n'+q[':question/problem']+'\n\n'
 extract+='Parameters `'+json.dumps(p,sort_keys=True)+'`; template `'+name+'`; field `radio/selection`, five math options. Polynomial derivative is '+str(p['a'])+'; '+('exponential base '+str(p['r'])+' requires division by ln(base) twice.' if 'r' in p else 'exponential slope '+str(p['k'])+' and additive exponent shift '+str(p['h'])+'.')+' Final layout: '+t[3]+'. '+('An extra distributed by-parts row precedes the final integral.' if t[4] else 'No extra distributed row.')+' '+('An additional common-denominator simplification row precedes the final factor.' if t[5] else '')+'\n\n'
 extract+='| Source answer UUID | Exact source value | Complete parameterized value pattern | Designation | Interpretation |\n|---|---|---|---|---|\n'
 f=q[':question/answer-fields'][0];correct=f.get(':answer-field/correct',{}).get(':answer/id')
 for i,(answer,expr) in enumerate(zip(f[':answer-field/choices'],g.BANKS[sid])):
  pattern=' + '.join('('+str(e)+')' for e in g.BANK_PARTS[sid][i]) if sid in g.BANK_PARTS else str(expr)
  extract+='| `'+answer[':answer/id']+'` | $'+answer[':answer/value']+'$ | `'+pattern+' + C` | '+('correct' if answer[':answer/id']==correct else 'missing original ref' if correct is None else 'incorrect')+' | empirical expression replay; historical error intent unresolved |\n'
extract+='''
In patterns x is the integration variable; a,b are polynomial coefficient/constant; k,h are exponential slope/shift; r is the integer base. `exp(k*x+h)` and `r**x` are computed from those prompt parameters. Each observed profile contains all five patterns together. Separate structured pieces preserve displayed sums even when algebraic collection is possible. The mappings are explicit empirical generalizations of whole expressions, not claims to have recovered source authoring code. Some coefficients in an empirical bank remain numerically anchored to its observed pattern. They are restricted to explicit replay/profile requests and never promoted to default distractor intent.

## 2. Generalized mathematical pattern

Integrate `(ax+b) exp(kx+h)` or `x r^x` by taking u to be the linear polynomial and v' the exponential. Compute u'=a and v=exp(kx+h)/k (or r^x/ln r), form uv minus the residual exponential integral, integrate it once, and append C. Source levels differ in the signed/logarithmic divisions and affine simplification they require; no new integration technique is introduced.

## 3. Components and banks

Each table above maps every original answer UUID and exact value to its whole expression recipe. Prompt template controls equals/Calculate/Calculate the integral, exponential type, linear-factor parentheses, and integral notation. The worked solution uses the source's shared sentences, states the by-parts identity, fixes u/u'/v'/v, substitutes their values, displays the remaining exponential integral, then a primitive and optional factored simplification. e_negative_distributed retains its extra distributed row and the original "We, substitute" sentence. hard_negative_factor retains the extra simplification row. Base layouts retain both the expanded primitive and final outer factor. No chosen error changes the fixed worked solution.

All 14 five-option source profiles are complete. The normal authored profile is `authored:parts_errors`, selected before any parameters are constructed. Its complete bank comprises correct uv-a*z/rate^2, reversed residual-integral sign uv+a*z/rate^2, omitted residual integral uv, reversed uv sign -uv-a*z/rate^2, and replacing u' with u in the residual integral uv-u*z/rate^2. This last operation is an explicit algebraic method error; no distractor feedback is shown. If any complete-bank member is equivalent, invalid, or correct unexpectedly, the whole instance is rejected. There is no first-valid pool or unrelated random perturbation.

## 4. Reusable template and constraints

The public API supports all 12 layouts, radio field requests, deterministic sampling, and exact source parameters/profiles. Explicit invalid inputs raise rather than silently changing values. Easy: a=1..8,k=1..8,b=h=0. Moderate negative: a=1..8,k=-1..-8,b=h=0; shifted moderate: positive k=1..8 and nonzero h=-8..8,b=0; base moderate: a=1,b=0,r=2..9. Hard: a=1..8, nonzero b=-8..8, the same k bounds and observed template sign/shift constraints; the unit-slope shift layout keeps a=k=1. Sampling remains unordered within each difficulty. Authored domains include the source coefficients and enough meaningful sign/coefficient/shift combinations for repeated practice, with the same single by-parts workload.

A source bank is eligible only for its assigned layout. Empirical profiles may have unknown error interpretation, but correct values and complete displayed bank equality are validated mathematically at every source parameter and at varied parameters. Their default alternatives are separately labeled authored banks. Values are compared modulo an additive integration constant because the assessed whole objects are indefinite primitives with explicit +C. Full derivatives, not isolated terms, are compared. Literal prose and semantic integration stages are checked separately from mathematical bank fidelity; LaTeX whitespace, standard ln notation, fraction placement, and equivalent grouping are normalized, so this is mathematical/structural fidelity rather than byte-for-byte source LaTeX.

q-2425 has no solution or correct designation in either source capture; its default supported solution follows the rated base-log layout. Prompt-spacing repair and derived designation are separated from original designation matches. All raw omissions remain in source.json. No empirical source errors in available correct primitives or worked stages were found. Source final choices retain +C; no arbitrary learner-facing error diagnoses are added.

Content identity hashes generator version, visible prompt, fixed worked solution, complete displayed bank, field type and key; it is independent of seed/choice order for fixed inputs. The mathematical fingerprint hashes the simplified visible integrand, independent of layout, bank, and presentation. UUIDs are field owned. JSON is local review data, never transaction EDN.

Plots: none. Steps 5 and 7 need no plot extractor/renderer. No image model, SVG, or plot dependency is used.
'''
(P/'template-extraction.md').write_text(extract)
v=json.load(open('/home/jake/Developer/MA/DATA/Lessons/317/Source/317.json'))
def locate(v):
 if isinstance(v,dict):
  if v.get('question_id')=='2425':return v
  for x in v.values():
   found=locate(x)
   if found:return found
 elif isinstance(v,list):
  for x in v:
   found=locate(x)
   if found:return found
widget=locate(v)
(P/'lesson-widget-q2425.json').write_text(json.dumps({'provenance':'/home/jake/Developer/MA/DATA/Lessons/317/Source/317.json','record':widget},indent=2,ensure_ascii=False)+'\n')
(P/'README.md').write_text('''# Exponential integration by parts generator

Generator: ../17592186064245.py. Local evidence only; no database writes.

```sh
.venv/bin/python generate/scratch/17592186064245/validate.py
.venv/bin/python generate/scratch/17592186064245.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186064245.py --difficulty moderate --profile observed:q-2425 --format json
```

The validator parses visible integrands, u/u'/v'/v, every residual integration stage, and whole displayed options; compares all 14 complete source banks; tests deterministic content/semantic identities, invalid explicit inputs, all layouts, and profile peers; then sends every correct/wrong radio selection to the real native grader. No blanks occur. Review originals and generated difficulty-labeled peers in review.md/review.json. The source q-2425's missing designation/solution/difficulty remain explicit; moderate level and derived answer/solution are authored repairs. Empirical profiles have unresolved historical error interpretations and are not default banks.
''')
