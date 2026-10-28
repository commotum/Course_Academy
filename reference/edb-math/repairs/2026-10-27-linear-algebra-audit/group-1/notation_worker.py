import importlib.util,json,os,random,re,sys
from pathlib import Path
path=Path(sys.argv[1]);kp=int(sys.argv[2]);sys.path.insert(0,str(path.parent));spec=importlib.util.spec_from_file_location('notation_test_generator',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);original_case_ids=list(getattr(m,'CASES',{}));out=[]
for band in ['easy','moderate','hard']:
 if kp==17592186119857:
  rows=m.generate(band,2,27102026)
  for i,r in enumerate(rows):out.append({'case':'fresh-'+band+'-'+str(i),'record':r})
 else:
  for seed in [27102026,27102027]:
   for offset in range(20):
    try:r=m.generate(band,seed+offset);break
    except ValueError as e:
     if 'Degenerate'not in str(e):raise
   out.append({'case':'fresh-'+band+'-'+str(seed),'record':r})
if kp==17592186119805:
 for band in ['easy','moderate']:
  for sid in m.LEVELS[band]:
   out.append({'case':'source-'+sid,'record':m.generate(band,0,sid,dict(m.CASES[sid]))})
 # Explicit labels remain scalars even when matching a vector's base letter.
 sid=m.LEVELS['easy'][0]
 for label in ['a','b']:
  data=dict(m.CASES[sid]);data['letter']=label;out.append({'case':'explicit-scalar-'+label,'record':m.generate('easy',0,sid,data)})
elif kp==17592186119806:
 for sid in m.CASES:
  target=m.parse_problem(m.CASES[sid][':question/problem'])[-1];out.append({'case':'source-'+sid,'record':m.generate('easy',0,sid,{'scale':1,'target':target})})
elif kp==17592186119854:
 for sid in original_case_ids:
  if sid not in m.OPS:continue
  band=m.level(sid);A,b=m.parse(m.CASES[sid]);out.append({'case':'source-'+sid,'record':m.source_generate(band,0,sid,{'b':list(map(int,b))})})
else:
 H=Path(__file__).resolve().parent;D=json.loads((H/'proposed.json').read_text());ids={q for t,k,q in D['links']if k==kp}
 def vs(text):return[[m.F(c.strip())for c in body.split(r'\\')]for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
 for q in D['questions']:
  if q[':db/id']not in ids or not q.get(':question/answer-fields'):continue
  f=q[':question/answer-fields'][0];right=f.get(':answer-field/correct')
  if not right or not q.get(':question/math-academy-id'):continue
  band={17592186045485:'easy',17592186045486:'moderate',17592186045487:'hard'}.get(q.get(':question/difficulty',{}).get(':db/id'))
  if not band:continue
  replay={'source_id':q[':question/math-academy-id'],'bank':[vs(a[':answer/value'])for a in f[':answer-field/choices']],'correct':vs(right[':answer/value'])}
  out.append({'case':'source-'+q[':question/math-academy-id'],'record':m.build(vs(q[':question/problem']),band,random.Random(0),replay=replay)})
print(json.dumps(out,default=str))
