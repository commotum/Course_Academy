"""Parent prompt-first cross-product and complete real-root-bank validation."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=P.parents[2]/f'generate/scratch/{K}';unknown=K==17592186059737
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
g=module('root_cross'+str(K),D.with_suffix('.py'));v=module('root_cross_scalar',P/'vector-math-parser.py');p=module('root_cross_stages',P/'triangle-readback.py')
C=dict(records=0,choices=0,fields=0,determinants=0,solution_sides=0,root_equations=0,source_values=0,source_banks=0,source_keys=0,source_missing_keys=0,source_raw_prompts=0,source_raw_solutions=0)
def scalar(z):
 z=re.sub(r'\\sqrt\[(\d+)\]\{([^{}]+)\}',lambda m:'('+m[2]+')^{\\frac{1}{'+m[1]+'}}',z)
 return v.scalar(z.replace('±',r'\pm'))
def roots(z):
 z=z.replace('±',r'\pm').replace(r'\,','').replace(' ','').replace('x=','')
 if r'\pm' in z:a=scalar(z.replace(r'\pm',''));return s.FiniteSet(-a,a)
 return s.FiniteSet(*[scalar(a) for a in z.split(',') if a])
def norm_(z):return z.replace('±',r'\pm')
def check(r):
 q=r['question'];prompt=q[':question/problem'];pairs=re.findall(r'\$([aubv])\s*=\s*([^$]+)\$',prompt)[:2];assert len(pairs)==2,(prompt,pairs)
 names=[a for a,b in pairs];u,w=[v.vector(b.strip().rstrip('.,')) for a,b in pairs];cross=u.cross(w);N=s.expand(cross.dot(cross));data=dict(kind='vectors',vals={a:p.basis(b) for a,b in zip(names,(u,w))},arrows={},scalars={})
 if unknown:
  R=scalar(re.search(r'\|\s*=\s*([^$]+)',prompt)[1]);assert R>0;expected=s.solveset(N-R**2,v.x,domain=s.S.Reals);assert isinstance(expected,s.FiniteSet) and expected
  for root in expected:assert s.simplify(s.sqrt(N.subs(v.x,root))-R)==0
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==(3 if unknown else 1)
 # Preserve determinant internals before splitting the actual teaching rows.
 for bi,block in enumerate(blocks):
  arrays=[]
  def save(m):arrays.append(m[0]);return 'MATRIX'+str(len(arrays)-1)
  pattern=r'\|\\begin\{aligned\}((?:(?!\\begin\{).)*?)\\end\{aligned\}\|'
  block=re.sub(pattern,save,block,flags=re.S);C['determinants']+=len(arrays)
  if bi==0:
   assert len(arrays)==4
   rows=re.search(pattern,arrays[0],re.S)[1].split(r'\\');assert [z.strip() for z in rows[0].split('&')]==list('ijk')
   assert s.Matrix([scalar(z) for z in rows[1].split('&')])==u and s.Matrix([scalar(z) for z in rows[2].split('&')])==w
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','');previous=None
  for row in block.split(r'\\'):
   row=re.sub(r'MATRIX(\d+)',lambda m:arrays[int(m[1])],row).strip().rstrip('.')
   if '=' not in row:continue
   if unknown and bi==2:
    # Each solving row must have precisely the same complete real root set.
    row=re.sub(r'\|[^|]+\|',lambda m:s.latex(s.sqrt(N)),row).replace('±',r'\pm').replace(r'\,','');parts=row.split('=',1);assert len(parts)==2,row
    lhs,rhs=parts
    if ',' in rhs or r'\pm' in rhs:
     actual=s.EmptySet
     for component in rhs.split(','):
      lhs1,rhs1=component.split('=',1) if '=' in component else (lhs,component)
      for root in roots(rhs1):actual=actual.union(s.solveset(scalar(lhs1)-root,v.x,domain=s.S.Reals))
    else:actual=s.solveset(scalar(lhs)-scalar(rhs),v.x,domain=s.S.Reals)
    assert actual==expected,('False complete root equation',row,actual,expected);C['root_equations']+=1;continue
   vals=[]
   for index,side in enumerate(row.split('=')):
    if not side.strip():assert index==0 and previous is not None;value=previous
    else:value=p.expression(side,data)
    vals.append(value)
   assert all(s.simplify(z.replace(lambda a:a.is_Pow and a.exp==s.Rational(1,2),lambda a:s.sqrt(s.factor(a.base)))-vals[0].replace(lambda a:a.is_Pow and a.exp==s.Rational(1,2),lambda a:s.sqrt(s.factor(a.base))))==0 for z in vals),('False printed cross stage',row,vals)
   previous=vals[-1];C['solution_sides']+=len(vals)-1
  if bi==0:assert s.simplify(previous-p.basis(cross))==0
  if unknown and bi==1:assert s.simplify(previous**2-N)==0
 for f in q[':question/answer-fields']:
  opts=f[':answer-field/choices'];ref=f[':answer-field/correct'][1];kind=f[':answer-field/type'].split('/')[-1];values=[]
  for z in opts:
   value=roots(z[':answer/value']) if unknown and kind=='radio' else scalar(z[':answer/value']) if kind=='blank' else v.vector(z[':answer/value'])
   if unknown:target=expected if kind=='radio' else sorted(expected,key=float)[int(f[':answer-field/key'].split('-')[-1])-1]
   elif kind=='radio':target=cross
   else:
    idx=int(f[':answer-field/key'].split('-')[-1])-1;before=prompt.split('{{'+f[':answer-field/key']+'}}')[0];sign=-1 if idx>0 and re.search(r'\\,-\\,\$\s*$',before) else 1;target=cross[idx]*sign
   good=value==target if isinstance(value,(s.FiniteSet,s.MatrixBase)) else s.simplify(value-target)==0
   assert (z[':answer/id']==ref)==good,(prompt,z,target);assert value not in values;values.append(value);C['choices']+=1
  if kind=='radio' and not r['generation'].get('template','').startswith('q-'):
   if unknown:
    root=max(expected);operations=[expected,s.FiniteSet(root),s.FiniteSet(-root),s.FiniteSet(-root**2,root**2),s.FiniteSet(-s.sqrt(root),s.sqrt(root))]
   else:operations=[cross,-cross,s.Matrix([cross[0],-cross[1],cross[2]]),s.Matrix([u[1]*w[2]+u[2]*w[1],-(u[0]*w[2]+u[2]*w[0]),u[0]*w[1]+u[1]*w[0]]),s.Matrix([cross[1],cross[2],cross[0]])]
   assert all(any(obj==target for target in operations) for obj in values) and len(operations)==len(values)
   C['method_banks']=C.get('method_banks',0)+1
  C['fields']+=1
 C['records']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 level=case.get('level',case.get('difficulty'));profile=case['bank_profile'];r=g.generate(level,template=case['template'],parameters=case['parameters'],profile=profile);q=check(r);old=sources[case['source_math_academy_id']]
 ofs=old[':question/answer-fields'];ofs=[ofs[0]] if case.get('legacy_evidence_only') else [f for f in ofs if unknown or f.get(':answer-field/correct') or case['template']=='q-1408']
 for of,f in zip(ofs,q[':question/answer-fields']):
  assert sorted(norm_(z[':answer/value']) for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in f[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(of[':answer-field/choices'])
  if of.get(':answer-field/correct'):assert norm_(of[':answer-field/correct'][':answer/value'])==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
  else:C['source_missing_keys']+=1
 if not unknown:
  raw=g.generate(level,template=case['template'],parameters=case['parameters'],profile=profile+':raw')['question'];assert raw[':question/problem']==old[':question/problem'];C['source_raw_prompts']+=1
  if old.get(':question/worked-solution'):assert raw[':question/worked-solution']==old[':question/worked-solution'];C['source_raw_solutions']+=1
 else:
  raw=g.generate(level,template=case['template'],parameters=case['parameters'],profile=profile+':raw');rq=raw['question'];assert rq[':question/problem']==old[':question/problem'];C['source_raw_prompts']+=1
  assert rq.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_raw_solutions']+=int(':question/worked-solution' in old)
  assert raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning']
  for of,rf in zip(old[':question/answer-fields'],rq[':question/answer-fields']):assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in rf[':answer-field/choices'])
  if case['template']=='q-19783':assert ':question/difficulty' not in rq and ':answer-field/correct' not in rq[':question/answer-fields'][0]
for item in json.loads((D/'review.json').read_text()):
 r=item.get('record',item)
 if not r['generation'].get('evidence_only'):check(r)
for item in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(item)
for level in ('easy','moderate','hard'):
 for seed in range(35):
  if unknown:check(g.generate(level,seed+88))
  else:
   for template in ('tuple_radio','basis_radio','tuple_blank','basis_blank'):check(g.generate(level,seed+88,template=template))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
