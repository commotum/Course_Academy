"""Independent final-result checks of existing worked solutions in the named topics."""
from pathlib import Path
import ast,json,re
P=Path(__file__).resolve().parent
scope={};exec(compile((P/'priority_math.py').read_text().split('report=[];')[0],str(P/'priority_math.py'),'exec'),{'__file__':str(P/'priority_math.py')},scope)
# Functions need the same globals for the closed parser and SymPy.
ns={'__file__':str(P/'priority_math.py')};exec(compile((P/'priority_math.py').read_text().split('report=[];')[0],str(P/'priority_math.py'),'exec'),ns)
matrices,scalar,same=ns['matrices'],ns['scalar'],ns['same'];records={}
for topic in [862,146,232]:
 for kp in json.loads((P/(str(topic)+'-priority-after.json')).read_text())[':topic/knowledge-points']:
  for q in [kp[':knowledge-point/canonical-example']]+kp[':knowledge-point/questions']:records[q[':db/id']]=q
checks=[];review=[]
for r in json.loads((P/'after-priority-math-report.json').read_text()):
 q=records[r['entity']];sol=q.get(':question/worked-solution','');expected=r['expected'];kind=''
 try:
  assert sol.strip(),'No solution'
  if isinstance(expected,list):
   ending=sol.rsplit('Therefore,',1)[-1];chosen=set(re.findall(r'\$([A-Z])\$',ending));assert chosen==set(expected),(chosen,expected);kind='classification conclusion'
  elif isinstance(expected,str) and expected.startswith(r'\begin{bmatrix}'):
   target=matrices(expected)[0]['matrix'];actual=matrices(sol);assert actual and same(actual[-1]['matrix'],target),(actual[-1]['matrix'] if actual else None,target);kind='computed final matrix'
  elif isinstance(expected,str) and expected.startswith('('):
   a,b=ast.literal_eval(expected);norm=re.sub(r'[\s{}]','',sol);assert re.search(str(a)+r'\\(?:times|cdot)'+str(b),norm),(expected,sol);kind='ordered transpose dimensions'
  elif isinstance(expected,str) and re.fullmatch(r'[+\-\d/]+',expected):
   blocks=re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',sol);flat=[b for b in blocks if r'\begin{' not in b];found=[]
   for block in flat:
    for row in block.split(r'\\'):
     if re.match(r'\s*k\s*&?\s*=',row):found.append(scalar(row.split('=',1)[1]))
   assert found and found[-1]==scalar(expected),(found,expected);kind='computed final scalar'
  else:
   # Small text classifications were inspected directly below; do not claim a generic English proof checker.
   review.append(dict(entity=r['entity'],expected=expected,solution=sol));continue
  checks.append(dict(entity=r['entity'],kind=kind,passed=True))
 except Exception as ex:review.append(dict(entity=r['entity'],expected=expected,error=repr(ex),solution=sol))
(P/'named-solution-results.json').write_text(json.dumps(dict(checked=checks,manualReview=review,scope='Final results and selection conclusions; intermediate algebra is not exhaustively re-proved'),indent=2));print('Checked',len(checks),'final results; review',len(review))
for x in review:print(x['entity'],x['expected'],x.get('error','text classification'))
