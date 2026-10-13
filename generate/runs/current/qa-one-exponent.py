"""Root printed exponential equations, all rows and complete operation banks."""
import sys,re,json,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent

def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','reader');x=p.x
nchecks=dict(records=0,choices=0,whole_banks=0,exponential_rows=0,linear_rows=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,raw_fieldless=0,raw_unrated=0)
def read(z):
 z=re.sub(r'\\[A-Za-z]+|[ahkm]',lambda m:m[0] if m[0].startswith('\\') else 'x',z.strip().rstrip('.,').replace('&',''))
 return p.scalar(z)
def logs(a,b):return s.simplify(s.expand_log(s.log(a),force=True)-s.expand_log(s.log(b),force=True))
def eq(z):
 a,b=z.replace('&','').split('=');return read(a),read(b)
def root_of(a,b,exp=False):
 residual=logs(a,b) if exp else a-b;P=s.Poly(s.expand(residual),x);assert P.degree()==1;root=s.simplify(-P.coeff_monomial(1)/P.coeff_monomial(x));assert root.is_Rational and root!=0;return root

def check(rec):
 q=rec['question'];g=rec['generation'];raw=g['evidence_only'];parts=re.findall(r'\$([^$]+)\$',q[':question/problem']);math=next(z for z in parts if '=' in z and len(z)>3).rstrip('.');L,R0=eq(math);answer=root_of(L,R0,True)
 # Recover numeric bases/affine exponents from actual question, not metadata.
 leftbase,E=L.as_base_exp();rightbase,R=R0.as_base_exp();assert leftbase.is_Integer and rightbase.is_Integer and min(leftbase,rightbase)>1
 left=leftbase>rightbase;base=min(leftbase,rightbase);big=max(leftbase,rightbase);powers=[v for v in (2,3,4) if base**v==big];assert len(powers)==1;power=powers[0];hard=r'\frac{1}' in math;originalR=-R if hard else R
 a,c=s.expand(E).coeff(x),s.expand(E).subs(x,0);b,d=s.expand(originalR).coeff(x),s.expand(originalR).subs(x,0);A=power*a if left else a;C=power*c if left else c;B=b if left else power*b;D=d if left else power*d
 if hard:B,D=-B,-D
 assert answer==s.Rational(D-C,A-B)
 fields=q.get(':question/answer-fields',[])
 for f in fields:
  vs=[read(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vs)==5 and len(set(vs))==5;assert sum(z==answer for z in vs)==1
  if ':answer-field/correct' in f:assert next(z[':answer/id'] for z,v in zip(f[':answer-field/choices'],vs) if v==answer)==f[':answer-field/correct'][1]
  if not raw:
   if hard:
    forget=s.Rational(-D-C,A+B);omit=s.Rational(-d-c,a+b)
    expected=[answer,forget,omit,s.Rational(-d,power+a+b),1/answer] if left else [answer,forget,s.Rational(-D-C,A-B),omit,-answer]
   else:
    omit=s.Rational(d-c,a-b) if a!=b else s.Rational(-power*power*c,power*power*a-b) if left else power-c
    # Full double power scales all original affine components.
    second=s.Rational(d-c,power*a-b) if left else s.Rational(power*d-c,a-power*power*b)
    if not left and d!=0:assert 'multiply_slope_twice_keep_shift_once' in g['distractor_recipes']
    expected=[answer,omit,second,-answer,s.Rational(D-C,A+B)]
   assert set(vs)==set(expected),(g['template'],math,vs,expected)
  nchecks['choices']+=len(vs);nchecks['whole_banks']+=1
 sol=q.get(':question/worked-solution')
 if sol:
  align=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
  assert len(align)==(3 if hard else 2)
  for idx,body in enumerate(align):
   rows=body.split(r'\\')
   assert len(rows)==(3 if idx==0 else 1 if hard and idx==1 else 4 if hard else 2 if g['template']=='easy_right' else 3)
   for row in rows:
    l,r=eq(row);exponential=idx<(2 if hard else 1);assert root_of(l,r,exponential)==answer,(g['template'],row)
    nchecks['exponential_rows' if exponential else 'linear_rows']+=1
  if not raw:
   side=re.search(r'rewrite the (left|right)-hand side',sol)[1];assert side==('left' if left else 'right')
 nchecks['records']+=1
if __name__=='__main__':
 kp=17592186115200;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'g');source=json.load(open(D/'source.json'));assert source==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  level=c.get('level',c.get('assigned_level',c.get('difficulty')));rec=g.generate(level,parameters=c['parameters'],profile=c['bank_profile'],template=c['template']);check(rec);q=rec['question'];o=olds[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in o)
   if key in o and key!=':question/answer-fields':assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  for f,of in zip(q.get(':question/answer-fields',[]),o.get(':question/answer-fields',[])):
   assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:
    val=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert val==of[':answer-field/correct'][':answer/value'];nchecks['source_refs']+=1
   nchecks['source_values']+=5
  nchecks['source_prompts']+=1;nchecks['source_solutions']+=int(':question/worked-solution' in o);nchecks['raw_fieldless']+=int(':question/answer-fields' not in o);nchecks['raw_unrated']+=int(':question/difficulty' not in o)
 for item in json.load(open(D/'review.json')):check(item.get('record',item))
 for lv in ('easy','moderate','hard'):
  for seed in range(20):check(g.generate(lv,seed=57000+seed))
 # Exercise explicit authored two-shift bank, omitted from default sampler.
 for seed in range(8):check(g.generate('moderate',seed=94000+seed,template='moderate_two_shifts'))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(nchecks,indent=2)+'\n');print(nchecks)
