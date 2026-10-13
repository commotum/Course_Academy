"""Retain source classification, complete recipe mapping and bounded policy."""
import importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((HERE/'source.json').read_text())[0][0];basis=json.loads((HERE/'basis.json').read_text())['basis']
families={'easy radio primitive':['q-103989','q-49903'],'easy radio log coefficient sum':['q-103991'],'moderate radio factored primitive':['q-103988'],'moderate radio expanded-denominator primitive':['q-49908'],'moderate radio constant-numerator coefficient sum':['q-49604'],'moderate radio linear-numerator coefficient sum':['q-49905'],'moderate two-blank log coefficients':['q-348896','q-348898','q-348933']}
text=f'''# Classification: {source[':knowledge-point/title']}

Captured database math, basis {basis}, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Complete scoped Pull is retained in source.edn, with every source identity, field, choice, key, difficulty, solution and canonical example; source.json is its JSON projection. Initial native inventory is inventory-initial.json. No registered generator or existing scratch package was present. No requested .generated artifact existed.

Twelve practice sources: three rated easy, eight rated moderate, one unrated. Easy uses one radio field and two Markdown/value templates, with three complete source bank profiles. Moderate uses radio or two blank math fields: five templates, four radio bank profiles, and three blank parameter sets with no distractor profiles. Hard has no source evidence and is unsupported by this bounded implementation. Absence alone does not establish mathematical impossibility.

The seven template families follow. All require no new plots (rating none); there are no plot references in prompts, options, solutions or canonical example.
'''
for family,ids in families.items():text+='\n- '+family+': '+', '.join(ids)+'. Plot rating none.\n'
text+='''
Two source exceptions are retained unchanged. q-49904 is unrated, has no correct answer/solution, and its five answers contain malformed determinant/log constructions. The original complete bank is retained; every comparison is unresolved and it is excluded from supported generation. q-128339 has two blank fields and a moderate label, but its prompt omits the definition of f(x); its solution rewrites a convergent improper integral as a difference of divergent improper integrals. Its original two answers are retained, but the mathematical prompt is underdefined, so it is excluded. Neither source is counted as a validated generated practice question.

The canonical e-506 factors a monic quadratic, computes partial fractions by substitution, and integrates to logarithms. It supports the method but is excluded from practice inventory. No source difficulty, prompt, field, answer or learner-history record is revised.
'''
(HERE/'classification.md').write_text(text)
parts=['# Template extraction\n\nAll source-specific components and raw bank values follow. Source values are observed evidence; proposed sampling k=2..9 is a narrower, explicit numerator/bank transport policy. k=1 is source replay. Changed numerators are variants, not new Markdown templates. Each radio source retains its complete bank profile; no recipes are pooled.\n']
mappings=[]
for t,q in g.sources().items():
 parts.append('## '+t+'\n\nSource entity '+str(q[':db/id'])+'; UUID '+q[':question/id']+'.\n\n'+q[':question/problem']+'\n')
 if t in g.DATA:
  level,kind,n,d1,d2,bank=g.DATA[t]
  parts.append(f'\nObserved pattern: {level}, {kind}; numerator {n}, ordered linear factors {d1} and {d2}. Parameters and signs are exactly those observed. The denominator has two distinct real poles. Required response is '+('two scalar coefficients in field-1 then field-2' if kind=='coefficients' else 'one scalar coefficient sum' if kind=='sum' else 'one complete antiderivative modulo an additive constant')+'.\n')
  parts.append('\nShared move: factor if needed, write N=A d2+B d1, eliminate A at d2=0 then B at d1=0, integrate A/d1+B/d2 with reciprocal slope factors, and report the authored response. For variants fixed factors retain their original signs/slopes, variable numerator is kN, and partial/log coefficients are multiplied by k. Prompt and solution structures are fixed within each family. Variant solution layout is simplified; original solution prose is retained exactly at k=1.\n')
 for i,f in enumerate(sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])):
  parts.append('\nField '+f[':answer-field/key']+' ('+f[':answer-field/type'][':db/ident']+').\n')
  for j,a in enumerate(f[':answer-field/choices']):
   correct=a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')
   if t not in g.DATA:recipe='Unresolved/unsupported; original retained without inference'
   elif kind=='logs':recipe=f'k*({bank[j][0]}) ln|{d1}| + k*({bank[j][1]}) ln|{d2}| + C; equality checked by differentiation on the real pole-free intervals'
   elif kind=='sum':recipe=f'k*({bank[j]}); complete observed scalar-bank transport'
   else:recipe=f'k*({bank[0][i]}); exact scalar coefficient fragment, no distractors'
   parts.append(f'\n- Choice {a[":answer/id"]}: `{a[":answer/value"]}`; correct marker {correct}; recipe {recipe}.\n')
   mappings.append({'source_question':t,'source_field':f[':answer-field/key'],'source_answer_id':a[':answer/id'],'original_value':a[':answer/value'],'correct':correct,'profile':t if t in g.DATA and kind!='coefficients' else None,'recipe':recipe,'replay_required':t in g.DATA})
 parts.append('\nOriginal worked solution:\n\n'+q.get(':question/worked-solution','[Absent; unresolved]')+'\n')
parts.append('''
## Constraints, calculations and rendering

k must be an integer from 1 through 9; production candidates use 2 through 9. Positive scaling preserves the observed sign pattern and algebraic workload, and exact SymPy rational arithmetic retains fractions. No source pole, leading coefficient, coefficient sum, blank field order or answer count is silently changed. Hard and excluded source profiles raise/reject rather than inventing banks. Before rendering, compute residues at the two poles, divide each by its linear-factor slope to obtain log coefficients, then transport the selected whole source bank. Reject collisions modulo additive constants for primitives or exact scalar equality for other responses. Domain is real x excluding both poles, with separate integration constants allowed on each connected interval.

The exact original prompt, solution and bank strings are replayed at k=1. At k>1 LaTeX notation is normalized while field shape, absolute-value logs, constant C and solution sequence remain. The transport recipe is a documented sampling extension, not a claimed misconception explanation. Every mathematical source bank is replayed in full, and each variant's printed values are independently checked. Unresolved malformed answers remain excluded.

Distinctness uses the reduced printed rational integrand, so equivalent expression forms, seed, UUID, answer order, solution text and profile choice do not establish novelty. A finite generator has 24 easy and 56 moderate candidate integrands before subtracting the database's existing/presented/reserved pool. Exhaustion leaves a finite-limit shortage explicit.
''')
(HERE/'template-extraction.md').write_text('\n'.join(parts));(HERE/'choice-mapping.json').write_text(json.dumps(mappings,indent=2)+'\n')
(HERE/'plot-extraction.md').write_text('# Plot extraction\n\nNo plots are present in any source prompt, field bank, worked solution or canonical example. Plot rating none for all templates. Standalone LaTeX is mathematical text. No asset publication or plot generation is required.\n')
(HERE/'README.md').write_text('''# Partial-fraction generator

Run `../../../.venv/bin/python ../17592186068922.py --difficulty easy --count 5 --seed 1 --format json` from this package (or invoke the script from repository root). Easy and moderate only. The script also falls back to the project Python environment when launched by the application. Numerator scaling k=2..9 retains complete observed banks. `validate.py` exhausts every bounded variant and replays supported sources, including grading through the actual application. Source exceptions, hard shortage and finite capabilities remain in capabilities.json.

`replenish.py` holds the application's api.lock from inventory/basis recheck through native-spec preview, guarded commit, retained receipt and exact-basis readback. It resolves application/ca-engine, registers the stable generator UUID and repository-relative path, and adds only this KP's new content. Complete requests and verification remain in reference/replenishment. No source questions or learner history are rewritten.
''')
print('Wrote classification and complete mappings')
