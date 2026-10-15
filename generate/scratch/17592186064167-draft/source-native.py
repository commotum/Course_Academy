"""Grade captured complete fields in actual rendered context; synthetic keys explicitly labeled."""
import sys;sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,subprocess,hashlib,copy
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('independent_math',D/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
items=[];qualified=[]
for case in json.loads((D/'source-cases.json').read_text()) + [{'source_id':'e-364 canonical context','record':json.loads((D/'source.json').read_text())['record'][':knowledge-point/canonical-example']}] + [{'source_id':'independently authored inventory '+str(i),'record':q['record']} for i,q in enumerate(json.loads((D/'independent-inventory.json').read_text())['questions'])]:
 sid=case['source_id'];q=v.plain(case['record']);v.check(q,True)
 if not q.get(':question/answer-fields'):
  qualified.append({'source_id':sid,'gap':'No captured field; no source-native grader probe fabricated.'});continue
 n=v.exponent(q[':question/problem']);synthetic=False
 for f in q[':question/answer-fields']:
  if ':answer-field/correct' not in f:
   correct=next(a for a in f[':answer-field/choices'] if v.family(v.expr(a[':answer/value']),v.x**(n+1)/v.sp.Integer(n+1)+v.C));f[':answer-field/correct']=[':answer/id',correct[':answer/id']];synthetic=True
  key=f[':answer-field/correct'][1]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'Captured full bank; '+('synthetic mathematically inferred missing key' if synthetic else 'captured original key')} for a in f[':answer-field/choices']]
 items.append({'label':sid+(' [synthetic fixture key; original key absent]' if synthetic else ''),'record':{'question':q,'knowledge_point':{'title':v.g.TITLE},'generation':{'template':'captured-source-or-inventory'}},'checks':checks})
(D/'source-native-input.json').write_text(json.dumps(items,indent=2)+'\n');(D/'source-native-gaps.json').write_text(json.dumps(qualified,indent=2)+'\n')
binary=ROOT/'generate/scratch/17592186059716-draft/check-engine';m=json.loads((D/'reference/grader-build.json').read_text());assert hashlib.sha256(binary.read_bytes()).hexdigest()==m['binary_sha256']
for name,sha in m['engine_sources'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha
subprocess.run([str(binary),str(D/'source-native-input.json'),str(D/'source-native-report.json')],check=True)
