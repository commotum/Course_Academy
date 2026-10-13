"""Root derives the scalar from printed formal vectors and reads every step."""
import sys,re,json,importlib.util,hashlib,math
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','scalar');x,y,L=p.x,p.y,p.z
n=dict(records=0,choices=0,formal_distribution=0,coefficient_quotients=0,whole_vector_factoring=0,conclusions=0,whole_banks=0,source_prompts=0,source_values=0,source_absences=0)
def scalar(t):
 t=t.replace('λ','z');t=re.sub(r'\\[A-Za-z]+|[ab]',lambda m:m[0] if m[0].startswith('\\') else 'x' if m[0]=='a' else 'y',t);return p.scalar(t)
def same(a,b):return s.simplify(a-b)==0
def check(rec):
 rec=rec.get('record',rec);q=rec['question'];g=rec['generation'];prompt=q[':question/problem'];assert '(non-zero)' in prompt
 parts=re.findall(r'\$(.*?)\$',prompt);assert len(parts)==3 and parts[-1]=='λ';eqs=[scalar(t) for t in parts[:2]];assert sum(e.has(L) for e in eqs)==1
 unknown=next(e for e in eqs if e.has(L));target=next(e for e in eqs if not e.has(L));base=s.expand(unknown).coeff(L);assert same(unknown,L*base)
 u,v=s.expand(base).coeff(x),s.expand(base).coeff(y);tu,tv=s.expand(target).coeff(x),s.expand(target).coeff(y);assert u and v and tu and tv and same(base,u*x+v*y) and same(target,tu*x+tv*y);K=tu/u;assert K!=0 and tv/v==K
 f=q[':question/answer-fields'][0];vs=[]
 for a in f[':answer-field/choices']:
  if a[':answer/type'].endswith('/text'):assert a[':answer/value']=='No such $λ$';vs.append(None)
  else:vs.append(scalar(a[':answer/value']))
 assert len(vs)==5 and len(set(vs))==5 and vs.count(K)==1
 if ':answer-field/correct' in f:assert vs[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])]==K
 else:assert g['evidence_only'] and ':question/difficulty' not in q and ':question/worked-solution' not in q
 if g['eligible_for_learning']:
  assert set(vs)=={K,-K,1/K,-1/K,None};n['whole_banks']+=1;level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert all(c.q==1 for c in [u,v,K]) and 1<=abs(u)<=4 and 1<=abs(v)<=6 and 2<=abs(K)<=8 and max(abs(tu),abs(tv))<=48
  elif level=='moderate':assert abs(u.p)==1 and u.q in (2,4,5) and v.q==K.q==tu.q==1 and 1<=abs(v)<=6 and 2<=abs(K)<=6 and max(abs(tu),abs(tv))<=36
  else:assert level=='hard' and u.q==v.q==1 and 2<=K.q<=5 and 2<=abs(K.p)<=9 and (u/K.q).q==(v/K.q).q==1 and 1<=abs(u/K.q)<=4 and 1<=abs(v/K.q)<=6 and max(abs(tu),abs(tv))<=54
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==4
  terms=[scalar(t) for t in blocks[0].strip().rstrip('.').split('=')];assert len(terms)==2 and same(terms[0],L*base) and same(terms[1],L*(u*x+v*y));n['formal_distribution']+=1
  rows=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\');assert len(rows)==2
  for row,num,den in zip(rows,[tu,tv],[u,v]):
   parts=row.replace('&','').split('=');assert len(parts)==3 and scalar(parts[0])==L and scalar(parts[1])==K and scalar(parts[2])==K
   # Exact printed quotient components must appear, not just matching CAS result.
   assert parts[1].strip()==r'\frac{'+s.latex(num).replace('- ','-')+'}{'+s.latex(den).replace('- ','-')+'}';n['coefficient_quotients']+=1
  terms=[scalar(t) for t in blocks[2].strip().rstrip('.').split('=')];assert len(terms)==2 and same(terms[0],target) and same(terms[1],K*base);n['whole_vector_factoring']+=1
  assert [scalar(t) for t in blocks[3].strip().split('=')]==[L,K];assert ('directions are the same' in sol)==(K>0) and ('directions are opposite' in sol)==(K<0);n['conclusions']+=1
 n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186096648;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c.get('level',c.get('difficulty',c.get('authored_level'))),template=c['template'],profile=c.get('bank_profile',c.get('profile')),parameters=c['parameters']);check(rec);q=rec['question'];o=old[c['source_id']];assert q[':question/problem']==o[':question/problem'];assert all((k in q)==(k in o) for k in [':question/difficulty',':question/worked-solution',':question/answer-fields'])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in of[':answer-field/choices']);assert ':answer-field/correct' not in f and ':answer-field/correct' not in of;n['source_prompts']+=1;n['source_values']+=5;n['source_absences']+=1
 for rec in json.load(open(D/'review.json'))+json.load(open(R/'qa'/f'{kp}-sampled.json')):check(rec)
 counts={}
 for level in ['easy','moderate','hard']:
  # Independently enumerate normalized arithmetic tasks from source workload bounds.
  us=[s.Rational(sign,d) for d in [2,4,5] for sign in [-1,1]] if level=='moderate' else [s.Integer(u) for u in range(-20,21) if u];keys=set()
  for u in us:
   for v in range(-30,31):
    if not v:continue
    ks=[s.Rational(a,d) for d in range(2,6) for a in range(-9,10) if a and math.gcd(abs(a),d)==1] if level=='hard' else list(map(s.Integer,range(-8,9)))
    for k in ks:
     if not k or k in [-1,1]:continue
     if level=='easy':ok=u.q==1 and 1<=abs(u)<=4 and 1<=abs(v)<=6 and 2<=abs(k)<=8 and max(abs(k*u),abs(k*v))<=48
     elif level=='moderate':ok=1<=abs(v)<=6 and 2<=abs(k)<=6 and (k*u).q==1 and max(abs(k*u),abs(k*v))<=36
     else:ok=2<=abs(k.p)<=9 and (u/k.q).q==(s.Rational(v,k.q)).q==1 and 1<=abs(u/k.q)<=4 and 1<=abs(s.Rational(v,k.q))<=6 and max(abs(k*u),abs(k*v))<=54
     if ok:keys.add((str(k),str(s.Rational(v)/u)))
  counts[level]=len(keys)
 n['independently_enumerated_tasks']=counts;assert counts=={'easy':448,'moderate':108,'hard':1280}
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
