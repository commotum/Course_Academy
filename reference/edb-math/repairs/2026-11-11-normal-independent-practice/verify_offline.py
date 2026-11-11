import sys,json,subprocess,tempfile,shutil,copy,hashlib,importlib.util
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generator_publish import Publisher,prepare_records,normalized_question
from scripts.generator_refill import validate_survivors
from scripts.generator_refill_plan import validate_refill_plan
from scripts.generator_evidence import batch_sha256
P=H/'package';manifest=json.loads((P/'package.json').read_text());p=Publisher.from_environment(source=':agent/codex')
source=json.loads((H/'source/source.json').read_text());inventory=json.loads((H/'inventory/inventory.json').read_text())
plan=validate_refill_plan(P,manifest,[dict(id=i) for i in ['supplied-assessed-work','awkward-coefficient-dot']],H/'review')
sys.path.insert(0,str(P));import generator as g;import check_refill as check
summary=[];reps=[]
with tempfile.TemporaryDirectory(prefix='normal-repair-relocation-',dir='/tmp') as tmp:
 relocated=Path(tmp)
 for name in manifest['files']:shutil.copy2(P/name,relocated/name)
 for band in g.LEVELS:
  records=g.generate_batch(band,30,20261111);verification=H/'verification';verification.mkdir(exist_ok=True)
  (verification/(band+'.json')).write_text(json.dumps(records,indent=2)+'\n')
  repeat=json.loads(subprocess.check_output([sys.executable,str(relocated/'generator.py'),'--difficulty',band,'--count','30','--seed','20261111'],cwd=relocated,timeout=120))
  assert records==repeat
  # Independently derive endpoint from the function, point, and perpendicularity.
  import sympy as s
  for r in records:
   d=r['generation'];params=d['parameters'];a,b,c,t=map(s.Rational,[params[k] for k in ('a','b','c','point')]);x=s.Symbol('x',real=True)
   expr={'quadratic':a*x*x+b*x+c,'cubic':a*x**3+b*x+c,'sextic':a*x**6/8-b*x**3/4+c,'root-reciprocal':a/s.sqrt(x)+b/x+c,'reciprocal-powers':a/x+b/x**2+c,'cube-linear':a*x**s.Rational(1,3)+b*x+c}[d['template']]
   h=expr.subs(x,t);m=s.diff(expr,x).subs(x,t);normal=-1/m;intercept=h-normal*t
   expected=[m,t+m*h] if band=='moderate' else [normal,intercept]
   q=r['question'];stem=rf'Find the equation of the normal line to the curve $y={s.latex(s.expand(expr))}$ at $\left({s.latex(t)},{s.latex(h)}\right)$.'
   assert q[':question/problem'].startswith(stem)
   for f,value in zip(q[':question/answer-fields'],expected):
    correct=next(v for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1]);assert s.Rational(check.rational(correct[':answer/value']))==s.simplify(value)
  accepted,dups=prepare_records(records,17592186092240,g.KP['id'],inventory['fingerprints'],p.config.math_root,P)
  assert accepted
  out=H/'delivery'/band;out.mkdir(parents=True,exist_ok=True)
  (out/'accepted.json').write_text(json.dumps(accepted,indent=2)+'\n')
  result=validate_survivors(accepted,inventory,out,root=P,manifest=manifest,band=band,python=sys.executable,repo_root=ROOT,environment=p.client.environment,expected_plan=plan)
  assert result['status']=='passed'
  seen=set()
  for r in accepted:
   family=r['generation']['template']
   if family not in seen:reps.append(r);seen.add(family)
  summary.append(dict(band=band,sampled=len(records),surviving=len(accepted),duplicates=dups,relocated_identical=True,independent_mathematics=True,batch_sha256=batch_sha256(records),result=str(out/'result.json')))
# Actual repaired stored questions, with all original owned fields and keys.
qs=json.loads((H/'proposed-siblings.json').read_text());ledger=json.loads((H/'case-ledger.json').read_text());changed={r['entity'] for r in ledger if r['changed']}
fixed=[dict(knowledge_point=g.KP,question=normalized_question(q)) for q in qs if q[':db/id'] in changed]
for r in fixed:
 for f in r['question'][':question/answer-fields']:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct']]
(H/'verification/stored-repaired.json').write_text(json.dumps(fixed,indent=2)+'\n')
(H/'verification/render-representatives.json').write_text(json.dumps(reps+fixed,indent=2)+'\n')
cases=[]
for r in fixed:
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);v=check.rational(correct[':answer/value'])
  checks += [dict(field_index=i,submitted=f'({v.numerator})/({v.denominator})',expected='accepted',control='equivalent',purpose='Exact original key in ordinary fraction notation'),dict(field_index=i,submitted=str(v+1),expected='rejected',control='wrong',purpose='Different coefficient changes the uniquely specified normal equation')]
 cases.append(dict(label=r['question'][':question/id'],record=r,checks=checks))
(H/'verification/stored-native-input.json').write_text(json.dumps(cases,indent=2)+'\n')
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'verification/stored-native-input.json'),str(H/'verification/stored-native-report.json')],check=True)
(H/'preflight-verification.json').write_text(json.dumps(dict(passed=True,database_writes=0,checks=summary,stored_repaired=len(fixed),refill_plan=plan),indent=2)+'\n')
print(json.dumps(summary,indent=2))
