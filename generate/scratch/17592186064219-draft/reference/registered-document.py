"""Bounded classification, extraction, and contributor/commit notes for this KP."""
import importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
recipes={
'q-49540':['n atan(sx)','atan(sx)/s','c asin(sx)','c atan(sx)','asin(sx)/s'],
'q-114033':['atan(x/s)','(s/n) atan(sx)','c atan(x)','c atan(x/s)','c atan(sx)'],
'q-114035':['b atan(sx)','c atan(sx)','s atan(sx)','c atan(x)','c atan(x/b)'],
'q-114036':['c atan(x)','s atan(sx)','b atan(sx)','atan(x/s)','c atan(sx)'],
'q-114040':['c atan(sx)','(n/b) atan(sx)','s atan(sx)','c atan(bx)','n atan(sx)'],
'q-2504':['atan(sx)/s','s atan(sx)','atan(bx)/b','atan(sx)/b','atan(2sx)/(2s)'],
'q-2507':['atan(x)/b','atan(sx)/s','arcsec(bx)/b','asin(sx)/s','atan(bx)/b'],
'q-73713':['atan(sx)/c','asin(sx)/c','c atan(x)','c asin(sx)','c atan(sx)'],
'q-114039':['c atan(sx)','b atan(sx)','s atan(sx)','c atan(bx)','c atan(x)'],
'q-49548':['atan(x/b)/b','atan(x/s)','c atan(x/s)','c atan(x/b)','atan(x/b)'],
'q-114045':['c atan(sx)','atan(x/s)','atan(x/s)/s','c atan(x/s)','(n/b) atan(x/s)'],
'q-114046':['atan(x)/s','atan(sx)','atan(x/s)/s','atan(x/s)','s atan(x/s)'],
'q-49505':['c atan(x/s)','atan(x/s)','c atan(x)','atan(sx)','s atan(sx)'],
'q-49550':['c atan(x/s)','c asin(sx)','c asin(x/s)','c atan(sx)','atan(x/s)'],
'q-49551':['c asin(x/s)','c atan(cx)','asin(sx)/s','c atan(x/s)','atan(x/s)/s'],
'q-73714':['(s/n) atan(sx)','c atan(x/s)','atan(x/s)/n','c atan(sx)','(s/n) atan(x/s)']}
contract=json.loads((HERE/'contract.json').read_text())
for sid,t in contract['profiles'].items():t['recipes']=recipes[sid]
(HERE/'contract.json').write_text(json.dumps(contract,indent=2,ensure_ascii=False)+'\n')
source=json.loads((HERE/'source.json').read_text());basis=source['basis']
groups={'easy-equation-square-scaled':['q-49540','q-73713'],'easy-equation-square-unit-forward':['q-2504'],'easy-equation-square-unit-reversed-differential':['q-2507'],'easy-calculate-square-scaled':['q-114033'],'easy-calculate-radical-unit-thus':['q-114035'],'easy-calculate-radical-unit-so':['q-114036','q-114039'],'easy-calculate-radical-scaled':['q-114040'],'moderate-equation-unit':['q-49548','q-49505','q-49550'],'moderate-equation-scaled-unsimplified-factor':['q-49551'],'moderate-equation-scaled':['q-73714'],'moderate-calculate-scaled':['q-114045'],'moderate-calculate-cancelled':['q-114046']}
lines=['# Classification','',f'Captured all 16 practice members and canonical example at math basis {basis}; lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Query/Pull and original records are in reference/source.edn and source.json. No registered generator at this basis. The requested job .generated file was absent.','', '| Difficulty | Sources | Field layout | Markdown/value templates | Source bank profiles | Plots |','|---|---:|---|---:|---:|---|','| Easy | 9 | one radio field `selection`, five mathematical choices | 7 | 9 | none |','| Moderate | 7 | one radio field `selection`, five mathematical choices | 5 | 7 | none |','| Hard | 0 | unverified | 0 verified | 0 verified | unverified |','', 'Template counts retain changed solution sequences, differential direction, radical forms, prompt layouts, and omitted/cancelled coefficients; mere changed numbers are grouped. Full exact source-specific variants remain in contract.json. Choice recipes are never pooled across profiles.','']
for name,ids in groups.items():lines.append('- '+name+': '+', '.join(ids)+'; new plot rating none.')
lines.extend(['','No source errors, missing fields, or unresolved option mappings were found. Canonical e-471 illustrates factoring a denominator with two coefficients, but has no gradable fields and does not justify a new hard practice template. Hard is unsupported by this bounded package; it remains unfilled and new evidence reopens classification.'])
(HERE/'classification.md').write_text('\n'.join(lines)+'\n')
lines=['# Template extraction','', 'Easy family: n/(1+b x²), u=s x, dx=du/s. Moderate family: n/(b+x²), factor b, u=x/s, dx=s du. Here s=√b, c=n/s, n,b>0. The domain is all real x and C is arbitrary real. Easy permits observed perfect squares and squarefree radicands 2,3,5,6; moderate sources use perfect squares. Source alternative asin values are assessed on their real branches; arcsec has its usual |argument|≥1 domain and cannot equal the global atan antiderivative.','', 'Each original solution keeps its original fixed wording, differential relation, alignment, normalization stages and final notation. extract.py replaces only numerator and computed coefficient components, leaving the original denominator scale fixed. contract.json stores every complete source bank, prompt/solution template and parameter tuple.','', 'The seven nonunit profiles vary n within 2..30 subject to source simplification constraints and five distinct option derivatives. Unit-numerator profiles and the n=s cancellation profile stay at the observed tuple. This deliberately narrower capability preserves omitted unit scalars and observed arithmetic layout; it is not evidence that wider sampling is impossible. Full finite limits are in capabilities.json.','', 'Every recipe below includes +C. Each observed option is assigned in original order, not inferred from a pooled bank. The symbolic expressions are observed mathematical patterns; their psychological interpretations remain unspecified. No mistake labels or inferred feedback appear to learners.','']
for sid,t in contract['profiles'].items():
 n,b=t['parameters'];values,ci=g.bank(sid,[n,b]);assert values==t['source_choices']
 lines+=['## '+sid,'', f'Source entity {t["source_eid"]}; {t["difficulty"]}; n={n}, b={b}, s=√{b}; {t["number_form"]}; {t["layout"]} prompt; one radio `selection` field; no plots. Numerator policy: '+('fixed source tuple' if t['fixed_numerator'] else 'bounded variable numerator')+'.','',t['prompt'],'', '| Option | Recipe | Exact source value | Correct |','|---:|---|---|---|']
 for i,(recipe,value) in enumerate(zip(recipes[sid],values)):lines.append(f'| {i+1} | `{recipe}+C` | `${value}$` | '+('yes' if i==ci else 'no')+' |')
 lines+=['','Source replay checks all five mathematical values, exact rendered values, correct designation, original prompt and complete worked solution. See source-replay.json for the matched/total counts.','']
(HERE/'template-extraction.md').write_text('\n'.join(lines)+'\n')
(HERE/'README.md').write_text('''# Inverse-tangent substitution generator

Script: `generate/scratch/17592186064219.py`. The stable generator identity is derived from the existing knowledge-point UUID; an already registered identity takes precedence on replenishment.

`validate.py` exhaustively checks the bounded family with SymPy and the actual application grader. It verifies exact source-bank replay, complete source wording, deterministic identity independent of seed, option distinctness, printed integrands, substitution coefficients and final derivatives. `review.md` places every original next to its replay and variant. No plots or new assets are required.

`replenish.py` reuses the configured database integration and application contributor. It acquires `.local/learning/requests/math/api.lock`, rechecks current basis, distinct unseen/unreserved stock, identities and source evidence, and holds the lock through preview, guarded submission, exact receipt readback and inventory recheck. Only this KP's generator registration and fresh validated questions can be added. Original source records, canonical content and all learner facts are preserved. Durable requests are retained and recovered under their original keys before new intent. Evidence lives in reference/replenishment.

Sampling is deliberately bounded: observed denominator scale, restricted nonunit numerator variation, fixed unit/cancellation profiles. Unsupported hard and exhausted finite stock remain explicit. Seed, source profile, identity, and choice order are never counted as distinct tasks.
''')
print('Documented classification, templates and all 80 original options')
