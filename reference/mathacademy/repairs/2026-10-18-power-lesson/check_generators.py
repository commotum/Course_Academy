"""Check all registered lesson generators for malformed equation chains."""
import importlib.util,json,re,subprocess
from pathlib import Path
from scripts.generator_packages import materialize_package
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('current_formatter',ROOT/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
if __name__=='__main__':
 checks=[];findings=[];samples=[]
 for kp in json.loads((HERE/'topic.json').read_text())[0][0][':topic/knowledge-points']:
  ref=kp[':knowledge-point/question-generator'][':question-generator/script'];destination=HERE/'generator-runs'/str(kp[':db/id'])
  if not destination.exists():script=materialize_package(ref,Path('/media/jake/SSD/EDB/math'),destination)
  else:script=destination/'generator.py'
  if kp[':db/id']==17592186064303 and (HERE/'generator-repair/generator.py').exists():script=HERE/'generator-repair/generator.py'
  bands={17592186064301:['easy'],17592186064302:['easy','moderate'],17592186064303:['easy','moderate','hard'],17592186064304:['moderate','hard']}[kp[':db/id']]
  for band in bands:
   r=subprocess.run([str(ROOT/'.venv/bin/python'),'-B',str(script),'--difficulty',band,'--count','20','--seed','181038'],capture_output=True,text=True,timeout=60)
   assert r.returncode==0,r.stderr
   records=json.loads(r.stdout);samples.append(records[0]);count=0
   def audit(value,attr=None):
    nonlocal_placeholder=None
    if isinstance(value,dict):
     for k,v in value.items():audit(v,k)
    elif isinstance(value,list):
     for v in value:audit(v,attr)
    elif isinstance(value,str) and attr in (':question/problem',':question/worked-solution',':answer/value',':answer/feedback'):
     try:
      (fmt.validate_tex if attr==':answer/value' else fmt.validate_prose)(value)
      assert not re.search(r'&\s*=\s*\\\\',value),'Dangling equals before row break'
      assert r'\eqalign' not in value,'Legacy eqalign'
      assert fmt.scalable_fraction_parentheses(value)==value,'Unscaled fraction parentheses'
     except (ValueError,AssertionError) as ex:findings.append({'kp':kp[':db/id'],'difficulty':band,'attribute':attr,'error':str(ex),'text':value})
   for record in records:audit(record['question'])
   checks.append({'kp':kp[':db/id'],'difficulty':band,'records':len(records),'script':ref})
 result={'passed':not findings,'generators_checked':4,'checks':checks,'findings':findings};(HERE/'generator-audit.json').write_text(json.dumps(result,indent=2)+'\n');(HERE/'generator-render-input.json').write_text(json.dumps(samples,indent=2)+'\n');print(json.dumps({'passed':not findings,'records':sum(c['records'] for c in checks),'findings':len(findings)}));assert not findings,findings[:2]
