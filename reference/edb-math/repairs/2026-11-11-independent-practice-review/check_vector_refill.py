import copy,importlib.util,json,sys,tempfile,re
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy');b=R/'reference/edb-math/repairs/2026-11-11-vector-independent-practice';sys.path.insert(0,str(b/'package'))
s=importlib.util.spec_from_file_location('review_vector_refill',b/'package/check_refill.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
checks=[]
for band in ['easy','moderate','hard']:
 path=b/'verification'/band/'records.json'
 if not path.exists():path=b/'verification'/band/'raw.json'
 if not path.exists():
  choices=[p for p in (b/'verification'/band).glob('*.json') if p.name not in ['delivery.json']];raise Exception(str(choices))
 records=json.loads(path.read_text()); reps={}
 for rec in records:
  kind=c.enum(rec['question'][':question/answer-fields'][0][':answer-field/type']);reps.setdefault(kind,rec)
 for kind,record in reps.items():
  for name,expected in [('clean','accepted'),('residual-direction-hint','rejected'),('solution-image-before-answer','rejected'),('wrong-visible-component','rejected'),('wrong-key','rejected')]:
   rec=copy.deepcopy(record);q=rec['question']
   if name=='residual-direction-hint':q[':question/problem']=q[':question/problem'].replace('\n\n',' The remaining path points in the opposite direction.\n\n',1)
   if name=='solution-image-before-answer':q[':question/problem']=q[':question/problem'].replace(rec['generation']['plot_assets']['prompt'],rec['generation']['plot_assets']['solution'])
   if name=='wrong-visible-component':q[':question/problem']=q[':question/problem'].replace(r'\mathbf{b}$',r'\mathbf{b}+\mathbf{b}$')
   if name=='wrong-key':
    f=q[':question/answer-fields'][0];target=c.answer_id(f[':answer-field/correct']);v=next(a for a in f[':answer-field/choices'] if a[':answer/id']==target);v[':answer/value']=str(-c.parse(v[':answer/value']))
   try:
    with tempfile.TemporaryDirectory() as tmp:c.check(rec,Path(tmp))
    observed='accepted'
   except (AssertionError,ValueError,KeyError):observed='rejected'
   assert expected==observed,(band,kind,name,observed)
   checks.append({'band':band,'field':kind,'control':name,'expected':expected,'observed':observed})
report={'status':'passed','controls':checks};out=R/'reference/edb-math/repairs/2026-11-11-independent-practice-review/vector-refill-controls.json';out.write_text(json.dumps(report,indent=2)+'\n');print({'status':'passed','controls':len(checks)})
