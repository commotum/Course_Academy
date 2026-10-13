"""Root standard-circle extraction, full center/radius choices and teaching rows."""
import sys,re,json,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent

def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','reader');x,y=p.x,p.y
n=dict(records=0,choices=0,whole_banks=0,generic_rows=0,comparison_rows=0,prose_assignments=0,conclusions=0,radical_reduction_sides=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
def scalar(raw):
 raw=raw.strip().rstrip('.,?');raw=re.sub(r'\\[A-Za-z]+|[abr]',lambda m:m[0] if m[0].startswith('\\') else {'a':'u','b':'v','r':'t'}[m[0]],raw)
 return p.scalar(raw)
def same(a,b):return s.simplify(a-b)==0
def equation(raw):
 l,r=raw.replace('&','').split('=');return s.expand(scalar(l)-scalar(r))
def triple(text):
 m=re.fullmatch(r'The center is \$\((.*),(.*)\)\$ and (?:the )?radius is \$(.*)\$',text);assert m,text;return tuple(scalar(z) for z in m.groups())
def check(rec):
 q=rec['question'];g=rec['generation'];expr=re.findall(r'\$([^$]+)\$',q[':question/problem'])[0];F=equation(expr);P=s.Poly(F,x,y);assert P.total_degree()==2 and P.coeff_monomial(x*x)==P.coeff_monomial(y*y)!=0 and P.coeff_monomial(x*y)==0;K=P.coeff_monomial(x*x);a=-P.coeff_monomial(x)/(2*K);b=-P.coeff_monomial(y)/(2*K);S=a*a+b*b-P.coeff_monomial(1)/K;assert S>0;r=s.sqrt(S);expected=(a,b,r)
 f=q[':question/answer-fields'][0];vs=[triple(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vs)==5 and len(set(vs))==5;correct=[i for i,z in enumerate(vs) if all(same(v,w) for v,w in zip(z,expected))];assert len(correct)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][correct[0]][':answer/id']==f[':answer-field/correct'][1]
 else:assert g['evidence_only']
 if g['bank_profile'] in ('authored','authored_axis'):
  want=[(a,b,r),(-a,-b,r),(-a,b,r),(a,-b,r),(a,b,S)] if g['bank_profile']=='authored' else [(a,b,r),(-a,-b,r),(a,b,S),(-a,-b,S),(0,0,r)]
  assert set(vs)==set(want)
 sol=q.get(':question/worked-solution')
 if sol:
  displays=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(displays)==(3 if q[':question/difficulty'].endswith('/hard') else 2)
  gener=(x-p.u)**2+(y-p.v)**2-p.t**2;assert equation(displays[0])==s.expand(gener);n['generic_rows']+=1
  rows=displays[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==3 and equation(rows[0])==s.expand(gener)
  for row in rows[1:]:assert same(equation(row),F/K)
  substitutions={p.u:a,p.v:b,p.t:r};assert same(equation(rows[0]).subs(substitutions),F/K)
  assert '(x-' in rows[-1] and '(y-' in rows[-1]
  assignments=re.search(r'We see that \$a=(.*?),\$ \$b=(.*?),\$ and \$r=(.*?)\.\$',sol);assert assignments and all(same(scalar(z),v) for z,v in zip(assignments.groups(),expected))
  final=re.search(r'Therefore, the circle is centered at \$\((.*),(.*)\)\$ and its radius is \$(.*?)\.\$',sol);assert final and all(same(scalar(z),v) for z,v in zip(final.groups(),expected))
  if len(displays)==3:
   parts=displays[2].split('=');assert parts[0]=='r' and len(parts)==4
   for part in parts[1:]:assert same(scalar(part),r)
   assert r'\cdot' in parts[2] and r'\sqrt' in parts[2];n['radical_reduction_sides']+=3
  n['generic_rows']+=1;n['comparison_rows']+=2;n['prose_assignments']+=3;n['conclusions']+=1
 n['records']+=1;n['choices']+=5;n['whole_banks']+=1
if __name__=='__main__':
 kp=17592186087656;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');source=json.load(open(D/'source.json'));assert source==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(rec);q=rec['question'];o=olds[c['source_id']]
  for k in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (k in q)==(k in o)
   if k in o:assert q[k]==(o[k][':db/ident'] if k.endswith('difficulty') else o[k])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   val=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert val==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for item in json.load(open(D/'review.json')):check(item.get('record',item))
 for lv in ('easy','moderate','hard'):
  for seed in range(15):check(g.generate(lv,seed=880000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
