"""Root all actual common-denominator banks and complete repaired math stages."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186059643'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'rational-trig-readback.py','p');g=load(D.with_suffix('.py'),'g');known={17592186253599,17592186253600,17592186329718,17592186335821}
n=dict(records=0,choices=0,whole_banks=0,printed_equalities=0,raw_known_defective_solutions=0,source_prompts=0,source_solutions=0,source_values=0,source_designations=0)
def scalar(t):return p.scalar(t.strip().rstrip('.,='))
def check(r):
 q=r['question'];m=r['generation'];truth=scalar(q[':question/problem'].split('$')[1]);f=q[':question/answer-fields'][0];vs=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vs)==5 and all(not p.equal(a,b) for i,a in enumerate(vs) for b in vs[:i]);good=[i for i,v in enumerate(vs) if p.equal(v,truth)];assert len(good)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][good[0]][':answer/id']==f[':answer-field/correct'][1]
 assert m['eligible_for_learning']==(not m['evidence_only'])
 if m['profile']=='authored-operations':
  z=m['parameters'];a,b=s.Rational(z['a']),s.Rational(z['b']);F,G=(p.C,p.S) if z['dual'] else (p.S,p.C);tid=m['template']
  if tid=='one_denominator':expected=[a/G,a,a/F,a*(G*G-F*F)/G,a*G*G*F*F/G]
  elif tid=='crossed_fractions':expected=[a/(F*G),a/G,a/F,a*(F*F-G*G)/(F*G),a*F*F*G*G/(F*G)]
  elif tid=='squared_shift':expected=[a*(b+1)/(b+F*F),a*G*G/(b+F*F),a*(b+1)/(b+F),a*b/(b+F*F),a*(b+F*F)]
  else:expected=[(a*G+b)/(F*G),b/(F*G),(a*G-b)/(F*G),(a*G+b*(G*G-F*F))/(F*G),a*G/(F*G)]
  assert all(sum(p.equal(v,e) for v in vs)==1 for e in expected),'Complete method bank differs'
 sol=q.get(':question/worked-solution')
 if sol:
  if m['profile']=='raw-observed' and m['source_id'] in known:n['raw_known_defective_solutions']+=1
  else:
   blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert blocks
   for b in blocks:
    last=None
    for row in b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
     for term in row.replace('&','').split('='):
      if not term.strip():continue
      v=scalar(term);assert p.equal(v,truth),(m['template'],row,v,truth)
      if last is not None:assert p.equal(v,last);n['printed_equalities']+=1
      last=v
   for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',re.sub(r'\$\$.*?\$\$','',sol,flags=re.S),re.S):
    if '=' in inline:
     a,b=inline.split('=');assert p.equal(scalar(a),scalar(b));n['printed_equalities']+=1
 n['records']+=1;n['choices']+=5;n['whole_banks']+=1
if __name__=='__main__':
 assert json.load(open(D/'source.json'))==json.load(open(R/'sources/17592186059643.json'));old={q[':db/id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  r=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(r);q=r['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in of)==(':answer-field/correct' in f)
  if ':answer-field/correct' in of:
   ov=next(a[':answer/value'] for a in of[':answer-field/choices'] if a[':answer/id']==of[':answer-field/correct'][':answer/id']);gv=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert ov==gv;n['source_designations']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
  for dual in (False,True):check(g.generate(c['level'],template=c['template'],profile='repaired-observed',parameters={'argument':r'\alpha','dual':dual}))
 for tid,level in [('one_denominator','easy'),('crossed_fractions','moderate'),('squared_shift','moderate'),('linear_plus_quotient','hard')]:
  for seed in range(18):
   r=g.generate(level,template=tid,seed=26000+seed);check(r);z=g.generate(level,template=tid,seed=27000+seed,parameters=r['generation']['parameters']);assert r['question'][':question/id']==z['question'][':question/id']
 for r in json.load(open(D/'review.json')):check(r.get('record',r))
 for a in ('1/1000003','-10','13/4'):
  try:g.generate('easy',parameters={'a':a})
  except ValueError:pass
  else:raise AssertionError('Reduced number-form guard bypass')
 (R/'qa/17592186059643-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
