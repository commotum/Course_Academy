"""Root complete real critical loci, all printed Jacobian stages and source banks."""
import sys,re,json,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent

def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'spatial-jacobian-readback.py','reader');u,v,w=p.u,p.v,p.w;vars=(u,v,w)
n=dict(records=0,choices=0,whole_banks=0,partial_rows=0,cofactor_minors=0,determinant_rows=0,zero_rows=0,conclusions=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,legacy_missing_refs=0)
def excluded(F):
 ans=[]
 for f in F:
  for pow in f.atoms(s.Pow):
   if pow.exp.is_number and (pow.exp<0 or pow.exp.q!=1) and pow.base.has(*vars):ans.append(pow.base)
 return ans

def zero_key(expr,exclusions):
 e=s.together(expr).as_numer_denom()[0].replace(s.exp,lambda _:s.Integer(1));e=s.factor(e)
 if e==0:return ('all',)
 if not e.free_symbols:return ('empty',)
 factors=s.factor_list(e,*vars)[1];pieces=[]
 for f,_ in factors:
  P=s.Poly(f,*vars);f=s.expand(f/P.LC())
  if any(not s.cancel(f/g).free_symbols for g in exclusions):continue
  involved=[z for z in vars if f.has(z)];H=s.hessian(f,involved)
  if P.total_degree()==2 and H.is_diagonal() and all(H[i,i]>0 for i in range(len(involved))):
   center={z:s.solve(s.diff(f,z),z)[0] for z in involved};minimum=s.simplify(f.subs(center))
   if minimum>0:continue
   if minimum==0:
    if any(s.simplify(g.subs(center))==0 for g in exclusions):continue
    pieces.append(('intersection',tuple(sorted(str(z-center[z]) for z in involved))));continue
  pieces.append(('factor',str(f)))
 return ('union',tuple(sorted(pieces,key=str))) if pieces else ('empty',)
def locus(text):
 axis=re.search(r'\$([uvw]{2})\s*-?\$(?:-|\s)*plane',text)
 if axis:return {'u':u,'v':v,'w':w}[next(c for c in 'uvw' if c not in axis[1])]
 bodies=re.findall(r'\$([^$]*)\$',text);eq=next(z.rstrip('.') for z in bodies if '=' in z)
 l,r=eq.split('=')
 if r'\pm' in r:r=r.replace(r'\pm','');return (p.scalar(l)-p.scalar(r))*(p.scalar(l)+p.scalar(r))
 return p.scalar(l)-p.scalar(r)

def check(rec):
 q=rec['question'];g=rec['generation'];F=p.components(q[':question/problem']);J=s.Matrix(F).jacobian(vars);det=J.det();ex=excluded(F);key=zero_key(det,ex);shown=p.partials(q[':question/worked-solution'],'xyz','uvw');assert all(p.same(a,b) for a,b in zip(shown,J));st=p.determinant_stages(q[':question/worked-solution'],J)
 for f in q[':question/answer-fields']:
  vals=[locus(a[':answer/value']) for a in f[':answer-field/choices']];keys=[zero_key(e,ex) for e in vals];assert len(keys)==5 and len(set(keys))==5 and sum(z==key for z in keys)==1
  if ':answer-field/correct' in f:assert next(a[':answer/id'] for a,z in zip(f[':answer-field/choices'],keys) if z==key)==f[':answer-field/correct'][1]
  else:assert g['evidence_only'] and g['template']=='q-161819';n['legacy_missing_refs']+=1
  n['choices']+=5;n['whole_banks']+=1
 sol=q[':question/worked-solution'];section=sol.split('So, we obtain',1)[1];blocks=p.displays(section);assert blocks
 for row in p.teaching_rows(blocks[0])[1:]:
  left,right=row.replace('&','').split('=');assert p.scalar(right)==0;assert zero_key(p.scalar(left),ex)==key;n['zero_rows']+=1
 tail=section[section.index('$$',section.index('$$')+2)+2:]
 equations=[z.rstrip('.') for z in re.findall(r'\$([^$]*)\$',tail) if '=' in z]
 assert equations
 if 'pair of intersecting planes' in tail:
  last=equations[-2:];combined=s.prod(locus('$'+z+'$') for z in last);assert zero_key(combined,ex)==key
 else:
  for eq in equations:assert zero_key(locus('$'+eq+'$'),ex)==key,(g['template'],eq,key)
 if 'i.e.' in tail and '-plane' in tail.split('i.e.')[-1]:assert zero_key(locus(tail.split('i.e.')[-1]),ex)==key
 n['records']+=1;n['partial_rows']+=9;n['cofactor_minors']+=st['cofactor_minors'];n['determinant_rows']+=st['determinant_rows'];n['conclusions']+=1
if __name__=='__main__':
 kp=17592186129270;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');source=json.load(open(D/'source.json'));assert source==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate('moderate',parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(rec);q=rec['question'];o=olds[c['source_id']]
  for k in (':question/problem',':question/worked-solution'):assert q[k]==o[k]
  assert len(q[':question/answer-fields'])==len(o[':question/answer-fields'])
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:
    val=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert val==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
   n['source_values']+=5
  n['source_prompts']+=1;n['source_solutions']+=1
 for item in json.load(open(D/'review.json')):check(item.get('record',item))
 for lv in ('easy','moderate','hard'):
  for seed in range(15):check(g.generate(lv,seed=650000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
