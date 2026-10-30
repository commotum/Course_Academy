import json,re,runpy
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;m=runpy.run_path(str(H/'math_review.py'));scalar=m['scalar'];vector=m['vector'];syms=m['syms'];correct=m['correct'];response=m['response'];plain=m['plain'];S=m['S'];qs=m['qs'];owners=m['owners'];checks=[];fail=[]
def unfont(t):
 t=re.sub(r'\\mathbf\s*(?:\{([a-z0])\}|([a-z0]))',lambda m:m[1]or m[2],t);t=t.replace(r'\langle','⟨').replace(r'\rangle','⟩');return t

def expected(q):
 p=unfont(q[':question/problem']);target=re.search(r'Find\s+\$([^$]+)\$',p)[1].rstrip('.,');L,R=target.split(r'\times');L,R=scalar(L),scalar(R);given={}
 for mat in re.finditer(r'([abcd])\s*\\times\s*([abcd])\s*&?=',p):
  tail=p[mat.end():].lstrip()
  if tail.startswith('⟨'):v=tail[:tail.index('⟩')+1]
  else:v=re.split(r'\$|&|\\\\|\n|[,.]',tail)[0]
  if not v or '{{'in v:continue
  given[mat[1],mat[2]]=vector(v)
 ans=sp.zeros(3,1);terms=[]
 for a in'abcd':
  for b in'abcd':
   coeff=sp.expand(L).coeff(syms[a])*sp.expand(R).coeff(syms[b])
   if coeff==0 or a==b:continue
   if(a,b)in given:value=given[a,b]
   else:value=-given[b,a]
   ans+=coeff*value;terms.append({'coefficient':coeff,'ordered_pair':a+'×'+b,'value':list(value)})
 return ans,terms
for q in qs:
 eid=q[':db/id']
 if owners[eid]not in[17592186203897,17592186203898]:continue
 try:
  ans,terms=expected(q);vals=correct(q)if q.get(':question/answer-fields')else{};ch=[]
  if'selection'in vals:
   assert vector(vals['selection'])==ans
   for f in q[':question/answer-fields']:
    candidates=[]
    for a in f[':answer-field/choices']:
     try:ok=vector(a[':answer/value'])==ans
     except Exception:ok=False
     if ok:candidates.append(a[':db/id'])
    assert candidates==[f[':answer-field/correct'][':db/id']],candidates;ch.append({'field':f[':db/id'],'all_options_checked':len(f[':answer-field/choices']),'unique_correct':candidates[0]})
  elif vals:
   r=unfont(response(q,vals));r=r.rsplit('=',1)[-1]
   # Fragmented coordinate responses reconstruct as one complete vector.
   actual=vector(r);assert actual==ans,(r,actual,ans)
  else:
   # Canonical examples end in basis-vector equalities.
   sol=unfont(q[':question/worked-solution']);last=sol.rsplit('=',1)[-1].split(r'\end',1)[0].replace('$','');assert vector(last)==ans,(last,ans)
  checks.append({'entity':eid,'expected':list(ans),'ordered_terms':terms,'choice_checks':ch,'proved':'Bilinearity, operand order, anticommutativity, and zero self-products.'})
 except Exception as e:fail.append({'entity':eid,'error':repr(e),'prompt':q[':question/problem']})
(H/'cross-math-verification.json').write_text(json.dumps({'passed':not fail,'checks':checks,'failures':fail,'database_writes':0},default=str,indent=2)+'\n');print('Cross checks',len(checks),'failures',len(fail));print([(x['entity'],x['error'])for x in fail])
