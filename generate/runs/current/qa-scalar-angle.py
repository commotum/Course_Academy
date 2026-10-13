"""Root independent magnitude/angle banks and every printed projection stage."""
import sys,re,json,hashlib,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'spatial-jacobian-readback.py','scalar')
n=dict(records=0,choices=0,formal_rows=0,substituted_rows=0,product_inputs=0,final_rows=0,complete_method_banks=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
def angle(raw):
 raw=raw.strip().rstrip('.,')
 if '∘' in raw or r'\circ' in raw or '°' in raw:return s.Rational(int(re.search(r'\d+',raw)[0]),180)*s.pi
 return p.scalar(raw)
def check(rec):
 q=rec['question'];meta=rec['generation'];text=q[':question/problem'];M=p.scalar(re.search(r'\|=(.*?)\$ and',text)[1]);theta=angle(re.search(r'(?:\\theta|θ)\s*=\s*(.*?)\$',text)[1]);names=re.search(r'vectors \$(\w)\$ and \$(\w)\$',text).groups();A,B=names;correct=s.simplify(M*s.cos(theta));f=q[':question/answer-fields'][0];values=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']];blank=f[':answer-field/type'].endswith('/blank');assert len(values)==(1 if blank else 5)
 if blank:assert '{{'+f[':answer-field/key']+'}}' in text
 assert all(not p.same(a,b) for i,a in enumerate(values) for b in values[:i]);hits=[i for i,a in enumerate(values) if p.same(a,correct)];assert len(hits)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][hits[0]][':answer/id']==f[':answer-field/correct'][1]
 else:assert meta['evidence_only'] and not meta['eligible_for_learning']
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];assert r'{\text{comp}}_{'+B+r'}\,'+A in sol;rows=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[0].split(r'\\');assert len(rows)==4
  rhs=[z.split('=',1)[1].replace('&','').strip().rstrip('.') for z in rows]
  assert rhs[0]==r'|\,'+A+r'\,|\operatorname{cos}⁡\theta';n['formal_rows']+=1
  mag,at=rhs[1].split(r'\operatorname{cos}⁡(',1) if r'\operatorname{cos}⁡(' in rhs[1] else rhs[1].split(r'cos\,(',1);assert at.endswith(')') and p.same(p.scalar(mag),M) and p.same(angle(at[:-1]),theta);n['substituted_rows']+=1
  m,c=rhs[2].split(r'\cdot ');assert p.same(p.scalar(m),M) and p.same(p.scalar(c),s.cos(theta));n['product_inputs']+=2
  assert p.same(p.scalar(rhs[3]),correct);n['final_rows']+=1
 if meta['eligible_for_learning'] and not blank:
  profile=meta['profile'];co=s.cos(theta)
  if profile=='trig_signed':want=[correct,M*s.sin(theta),-correct,M,co]
  elif profile=='trig_denominator':want=[correct,-correct,2*correct,co,M/2]
  else:assert profile=='right_angle' and co==0;want=[0,M,-M,M/2,-M/2]
  assert all(sum(p.same(a,b) for b in want)==1 for a in values);n['complete_method_banks']+=1
 n['records']+=1;n['choices']+=len(values)
if __name__=='__main__':
 kp=17592186105916;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(rec);q=rec['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=len(f[':answer-field/choices']);n['source_solutions']+=int(':question/worked-solution' in o)
 for item in json.load(open(D/'review.json')):check(item.get('record',item))
 for level in ('easy','moderate','hard'):
  for seed in range(18):check(g.generate(level,seed=81000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
