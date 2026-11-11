import copy,importlib.util,json,sys
from pathlib import Path
b=Path('/home/jake/Developer/Course_Academy/reference/edb-math/repairs/2026-11-11-normal-independent-practice/package');sys.path.insert(0,str(b))
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=mod('review_normal_g',b/'generator.py');c=mod('review_normal_c',b/'check_refill.py');tests=[]
for band in ['easy','moderate','hard']:
 q=g.generate_batch(band,1,71)[0]['question']
 for name,mutation,expected in [('clean',lambda q:None,'accepted'),('reverse-field-array',lambda q:q[':question/answer-fields'].reverse(),'accepted'),('supplied-derivative',lambda q:q.update({':question/problem':q[':question/problem'].replace('\n\n'," You are given $f'(x)=2x$.\n\n",1)}),'rejected'),('supplied-normal-rule',lambda q:q.update({':question/problem':q[':question/problem'].replace('\n\n',' The normal slope is the negative reciprocal of the tangent slope.\n\n',1)}),'rejected'),('changed-endpoint',lambda q:q.update({':question/problem':q[':question/problem'].replace('values of $a$ and $b$','values of $a+b$')}),'rejected'),('wrong-field-key',lambda q:q[':question/answer-fields'][0].update({':answer-field/key':'unknown'}),'rejected')]:
  r=copy.deepcopy(q);mutation(r)
  try:controls=c.check(r);observed='accepted'
  except (AssertionError,ValueError,KeyError):observed='rejected';controls=[]
  assert observed==expected,(band,name,observed)
  if name=='reverse-field-array':
   for i,f in enumerate(r[':question/answer-fields']): assert all(x['field_index']==i for x in controls[2*i:2*i+2])
  tests.append({'band':band,'control':name,'expected':expected,'observed':observed})
report={'status':'passed','tests':tests};Path('/home/jake/Developer/Course_Academy/reference/edb-math/repairs/2026-11-11-independent-practice-review/normal-refill-controls.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'passed','controls':len(tests)}))
