"""Root reads actual determinant/root sets and source or whole method banks."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186105908;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_coplanar_readback',P/'triple-product-readback.py');g=module('root_coplanar_gen',D.with_suffix('.py'));t=p.p.t
C=dict(records=0,actual_vector_triples=0,choices=0,whole_method_banks=0,evidence_banks=0,solution_blocks=0,solution_equalities=0,solution_set_stages=0,prose_root_values=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_assessments=0,raw_bad_designations=0)
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def roots(expr):
 result=s.solveset(expr,t,domain=s.S.Reals);assert isinstance(result,s.FiniteSet) and len(result) in (1,2);return result
def option(text,d):
 spans=re.findall(r'\$(.*?)\$',text)
 if spans:parts=spans
 elif '=' in text:parts=text.split(',')
 else:parts=[text]
 values=[d['scalar'](v.split('=',1)[-1].strip().rstrip('.')) for v in parts];assert all(not z.free_symbols for z in values);return s.FiniteSet(*values)
def check(r):
 q=r['question'];meta=r['generation'];profile=meta['profile'];opaque=profile.startswith('source:');raw=profile.endswith(':raw');coordinatetext=''.join(re.findall(r'⟨(.*?)⟩',q[':question/problem']));letters=set(re.findall('[a-z]',re.sub(r'\\[A-Za-z]+','',coordinatetext)));assert len(letters)==1;var=next(iter(letters));d=p.given(q[':question/problem'],parameter=var);wanted=roots(d['triple']);assert meta['evidence_only']==opaque and meta['eligible_for_learning']==(not opaque);fields=q[':question/answer-fields'];corrects=[]
 for field in fields:
  values=[option(z[':answer/value'],d) for z in field[':answer-field/choices']];assert len(set(values))==len(values);C['choices']+=len(values)
  if ':answer-field/correct' in field:
   good=next(z for z in field[':answer-field/choices'] if z[':answer/id']==field[':answer-field/correct'][1]);correct=option(good[':answer/value'],d);corrects.append(correct)
   if field[':answer-field/type'].endswith('/radio'):
    if raw and meta['template']=='q-18266':assert correct==s.FiniteSet(3-meta['parameters']['shift']) and wanted!=correct;C['raw_bad_designations']+=1
    else:assert correct==wanted and values.count(wanted)==1
  else:assert raw and ':question/worked-solution' not in q and ':question/difficulty' not in q;C['raw_missing_assessments']+=1
 if corrects and fields[0][':answer-field/type'].endswith('/blank'):assert s.Union(*corrects)==wanted and sum(len(z) for z in corrects)==len(wanted)
 if ':question/worked-solution' in q:
  blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);assert len(blocks) in (2,3)
  prev=None
  for index,block in enumerate(blocks):
   for row in p.rows(block):
    if '=' not in row:continue
    parts=row.strip().rstrip('.,').split('=')
    if any(r'\pm' in z for z in parts):
     assert index==len(blocks)-1 and len(parts)==2;left=p.expression(parts[0],d);right=d['scalar'](parts[1].replace(r'\pm',''));assert s.Union(roots(left-right),roots(left+right))==wanted;C['solution_set_stages']+=1;continue
    vals=[]
    for n,z in enumerate(parts):
     if not z.strip():assert n==0 and prev is not None;value=prev
     else:value=p.expression(z,d)
     vals.append(value)
    if index<len(blocks)-1:assert all(s.expand(z-vals[0])==0 for z in vals[1:]);C['solution_equalities']+=len(vals)-1
    else:assert len(vals)==2 and roots(vals[0]-vals[1])==wanted;C['solution_set_stages']+=1
    prev=vals[-1]
   C['solution_blocks']+=1
  final=q[':question/worked-solution'].split('Therefore,')[-1]
  if 'Thus $' in final:final=final.split('Thus $')[-1];final='$'+final
  actual=[option(z,d) for z in re.findall(r'\$(.*?)\$',final) if re.match(var+r'\s*=',z)];assert actual and s.Union(*actual)==wanted;C['prose_root_values']+=len(actual)
 if opaque:C['evidence_banks']+=1
 else:
  matrix=s.Matrix([v.T for v in d['vectors']]);poly=s.Poly(d['triple'],t);A=poly.LC();B=poly.nth(0)
  if fields[0][':answer-field/type'].endswith('/radio'):
   vals=[option(z[':answer/value'],d) for z in fields[0][':answer-field/choices']]
   if poly.degree()==2:
    z=-B/A;root=s.sqrt(z);expected=[wanted,s.FiniteSet(root),s.FiniteSet(-root),s.FiniteSet(-z,z),s.FiniteSet(-s.sqrt(1/z),s.sqrt(1/z))]
   else:
    answer=-B/A;allplus=sum(matrix[0,j]*matrix.minor_submatrix(0,j).det() for j in range(3));wp=s.Poly(allplus,t);wrong=-wp.nth(0)/wp.nth(1);expected=[s.FiniteSet(z) for z in (answer,-answer,-B,-A/B,wrong)]
   assert set(vals)==set(expected)
  C['whole_method_banks']+=1;level=q[':question/difficulty'].split('/')[-1];nums=[z for z in matrix if not z.free_symbols];slots=[(i,j) for i in range(3) for j in range(3) if matrix[i,j].free_symbols];assert all(z.is_Integer and abs(z)<=8 for z in nums) and len({i for i,j in slots})==1
  if level=='easy':assert len(slots)==1 and max(abs(z) for z in nums)<=3 and nums.count(0)>=2 and poly.degree()==1
  elif level=='hard':assert len(slots)==1 and slots[0][0] in (1,2) and all(2<=abs(z)<=8 for z in nums) and any(z<0 for z in nums) and any(z>0 for z in nums) and poly.degree()==1
  elif poly.degree()==1:assert not(len(slots)==1 and max(abs(z) for z in nums)<=3 and nums.count(0)>=2)
 C['records']+=1;C['actual_vector_triples']+=1;return q
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate('moderate',template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_prompts']+=1;C['source_solutions']+=int(':question/worked-solution' in old)
 for of,f in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);C['source_values']+=len(of[':answer-field/choices']);C['source_banks']+=1
  if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
 check(g.generate('moderate',template=case['template'],parameters={'shift':2},profile=case['bank_profile'].replace(':raw',':normalized')))
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for kind in ('radio','blank'):
  for seed in range(8):check(g.generate(level,seed+5908,field_type=kind))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
