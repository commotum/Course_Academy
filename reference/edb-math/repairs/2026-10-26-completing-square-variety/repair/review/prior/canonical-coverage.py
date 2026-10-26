import sys,json,subprocess,importlib.util
from pathlib import Path
from fractions import Fraction as F
W,E,R=map(Path,sys.argv[1:]);sys.path.insert(0,str(W));import generator as g
spec=importlib.util.spec_from_file_location('mf',R/'scripts/question_capture/math_format.py');mf=importlib.util.module_from_spec(spec);spec.loader.exec_module(mf)
records=[];checks=[]
for source,m,c,v in [('e-15021',7,0,'x'),('q-221418',15,0,'y'),('q-52277',5,3,'w')]:
 # w is a source-only variable. Ordinary variable renaming to x retains the partial input's method.
 rec=g.construct(m,c,'x' if v=='w' else v,'easy');mf.validate_generated_record(rec)
 expected=[F(m,2),abs(F(c)-F(m*m,4))];assert [z[':answer-field/choices'][0][':answer/value'] for z in rec['question'][':question/answer-fields']]==[g.tex(z) for z in expected]
 records.append(rec);checks.append({'label':source,'record':rec,'checks':[{'field_index':i,'submitted':str(x),'expected':'accepted','purpose':'Source input independently completed with exact fractions.'} for i,x in enumerate(expected)]+[{'field_index':1,'submitted':str(expected[1]+1),'expected':'rejected','purpose':'Wrong compensation.'}]})
(E/'canonical-partial-records.json').write_text(json.dumps(records,indent=2));(E/'canonical-grading-input.json').write_text(json.dumps(checks,indent=2));argv=[str(R/'generate/runs/current/check-engine'),str(E/'canonical-grading-input.json'),str(E/'canonical-grading-report.json')];r=subprocess.run(argv,capture_output=True,text=True);assert r.returncode==0,r.stderr
(E/'canonical-check.json').write_text(json.dumps({'source_ids':['e-15021','q-221418','q-52277'],'canonical_identity':'x²-7x=(x-7/2)²-49/4','partial_imports':'Instructional input coefficients retained; missing captured fields not fabricated or edited. The w input is verified under irrelevant renaming to x.','native_grader':{'argv':argv,'stdout':r.stdout,'returncode':r.returncode},'records_file':'canonical-partial-records.json'},indent=2));print(r.stdout)
