"""Root parses displayed arrays and ordered dimensions; full bank/prose checks."""
import importlib.util,json,re,itertools,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent

def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_matrix_scalar',R/'ode-scalar-parser.py')
def arrays(text):
 out={}
 pattern=r'([A-Z])\s*=\s*(?:\\begin\{(bmatrix)\}([\s\S]*?)\\end\{bmatrix\}|\[\\begin\{(aligned)\}([\s\S]*?)\\end\{aligned\}\]|\[([^\[\]]+)\])'
 for m in re.finditer(pattern,text):
  body=m[3] or m[5] or m[6];rows=[row.strip().split('&') for row in body.split(chr(92)*2)]
  assert len(set(map(len,rows)))==1
  for row in rows:
   for cell in row:assert p.scalar(cell.strip()).is_real
  out[m[1]]=(len(rows),len(rows[0]))
 assert out,text;return out

def pair(raw):
 m=re.fullmatch(r'(\d+)\s*\\(?:times|cdot)\s*(\d+)\.?',raw.strip().replace('$',''));assert m,raw;return int(m[1]),int(m[2])
for K in (17592186087713,):
 D=R.parents[2]/f'generate/scratch/{K}';g=module('root_matrix_'+str(K),D.with_suffix('.py'));C=dict(instances=0,displayed_values=0,source_questions=0,source_banks=0,source_values=0,source_existing_refs=0,source_missing_refs=0,source_exact_prompts=0,source_exact_solutions=0,solution_dimension_checks=0)
 tasks=set()
 def check(r):
  q=r['question'];prompt=q[':question/problem'];worked=q[':question/worked-solution'];ds=arrays(prompt);multi=K==17592186087713
  if multi:
   target=pair(re.search(r'is a \$([^$]+)\$ matrix',prompt)[1]);correct={name for name,d in ds.items() if d==target};assert len(correct) in (1,2) and len(ds)==3
   shapes=tuple(sorted(ds.values()));tasks.add((target,shapes))
  else:
   assert len(ds)==1;target=next(iter(ds.values()));tasks.add(target)
   if K==17592186087694:assert 1 in target and max(target)<=5
   else:assert all(2<=n<=6 for n in target)
  for f in q[':question/answer-fields']:
   choices=f[':answer-field/choices'];vals=[]
   for a in choices:
    text=a[':answer/value']
    if multi and f[':answer-field/type'].endswith('/checkbox'):
     assert f[':answer-field/key'] in ds
     assert text in ('false','true');value=text;good=(text=='true')==(f[':answer-field/key'] in correct)
    elif multi:
     names=set(re.findall(r'\$([A-Z])\$',text));assert names and names<=ds.keys() and text==' and '.join('$'+n+'$' for n in re.findall(r'\$([A-Z])\$',text))+' only';value=tuple(sorted(names));good=names==correct
    elif f[':answer-field/type'].endswith('/radio'):value=pair(text);good=value==target
    else:
     value=int(text);idx=0 if f[':answer-field/key']=='field-1' else 1;good=value==target[idx];assert '{{'+f[':answer-field/key']+'}}' in prompt
    vals.append(value);assert good==(a[':answer/id']==f[':answer-field/correct'][1]),(K,text,target)
   assert len(set(vals))==len(vals);C['displayed_values']+=len(vals)
  stated=re.findall(r'The matrix \$([A-Z])\$ has \$(\d+)\$ rows?\s+and \$(\d+)\$ columns?',worked)
  assert len(stated)==len(ds),(stated,worked)
  for name,rows,cols in stated:
   raw_label_exception=K==17592186087693 and r['generation']['source_analysis']['solution_label_anomaly_preserved']
   if raw_label_exception:assert name=='R' and 'P' in ds;name='P'
   assert ds[name]==(int(rows),int(cols));C['solution_dimension_checks']+=1
  printed=re.findall(r'dimensions are\s+\$([^$]+)\$',worked);assert len(printed)==len(ds)
  assert [pair(z) for z in printed]==[(int(a),int(b)) for _,a,b in stated]
  if multi:
   conclusions=re.search(r'Therefore, only (.*?) (?:is a|are) \$([^$]+)\$',worked);assert set(re.findall(r'\$([A-Z])\$',conclusions[1]))==correct and pair(conclusions[2])==target
   marks=re.findall(r'\$([A-Z])\$ has[^\n]+?\$\\,(✓|\\times )\$',worked);assert len(marks)==3
   for name,mark in marks:assert (name in correct)==(mark=='✓')
  C['instances']+=1;return q
 sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
 for case in json.loads((D/'source-cases.json').read_text()):
  old=sources[case['source_id']];q=check(g.generate(case['level'],field_type='radio',template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile'))));C['source_questions']+=1
  assert q[':question/problem']==old[':question/problem'];C['source_exact_prompts']+=1
  if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'];C['source_exact_solutions']+=1
  fresh={f[':answer-field/key']:f for f in q[':question/answer-fields']}
  for of in old.get(':question/answer-fields',[]):
   nf=fresh[of[':answer-field/key']];assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in nf[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(of[':answer-field/choices'])
   if of.get(':answer-field/correct'):
    correct_value=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert correct_value==of[':answer-field/correct'][':answer/value'];C['source_existing_refs']+=1
   else:C['source_missing_refs']+=1
 review=json.loads((D/'review.json').read_text())
 if isinstance(review,dict):review=[z for values in review.values() for z in values]
 for item in review:
  rec=item.get('record',item.get('generated',item))
  if 'question' in rec:check(rec)
 for rec in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(rec)
 def params(shapes):
  matrices=[[['-\\sqrt{3}' if K!=17592186087713 else '\\sqrt{3}' for _ in range(c)] for _ in range(r)] for r,c in shapes]
  return {'entries':matrices[0],'name':'W'} if K!=17592186087713 else {'target':list(shapes[0]),'labels':['W','X','Y'],'matrices':matrices}
 if K!=17592186087713:
  domain=[(r,c) for r in range(2,7) for c in range(2,7)] if K==17592186087693 else [(1,1)]+[(1,n) for n in range(2,6)]+[(n,1) for n in range(2,6)]
  for level in ('easy','moderate','hard'):
   for shape in domain:
    for template in (('display-radio','display-dual-blank') if K==17592186087693 else ('aligned_radio','double_blank')):check(g.generate(level,template=template,parameters=params([shape])))
  C['finite_union_tasks']=len(domain)
 else:
  catalogs={}
  for level in ('easy','moderate','hard'):
   catalog=set()
   for target in itertools.product(range(1,5),repeat=2):
    if level=='easy':
     r,c=target
     if max(target)>3 or r==c:continue
     families=[(target,(c,r),(r,r)),(target,(c,r),(c,c))]
    else:
     if level=='hard' and min(target)<3:continue
     foils=[v for v in itertools.product(range(1,5),repeat=2) if v!=target and (level!='hard' or min(v)>=2 and sum(abs(a-b) for a,b in zip(v,target))==1)]
     families=[(target,*z) for z in itertools.combinations(foils,2)]+[(target,target,z) for z in foils]
    for shapes in families:
     multiple=shapes[1]==target;template='peer_multiple' if multiple else 'peer_single';rec=g.generate(level,template=template,parameters=params(shapes));check(rec);catalog.add((target,tuple(sorted(shapes))))
   catalogs[level]=len(catalog)
  assert catalogs=={'easy':12,'moderate':1920,'hard':25},catalogs;C['finite_level_tasks']=catalogs
 C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(K,C)
