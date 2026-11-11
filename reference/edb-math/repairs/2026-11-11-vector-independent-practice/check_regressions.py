"""Retain counterexamples to the refill contract without writing database state."""
import copy,json,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'package'))
import check_refill
r=json.loads((H/'verification/easy/records.json').read_text())[0];mutations=[]
x=copy.deepcopy(r);x['question'][':question/problem']=x['question'][':question/problem'].replace(x['generation']['plot_assets']['prompt'],x['generation']['plot_assets']['solution']);mutations.append(('solution-image-before-answer',x))
x=copy.deepcopy(r);x['question'][':question/problem']+=' The path is drawn.';mutations.append(('auxiliary-path-prose',x))
x=copy.deepcopy(r);k=int(x['generation']['parameters']['k']);x['question'][':question/problem']=x['question'][':question/problem'].replace('+'+str(k)+r'\mathbf{b}','+'+str(k+1)+r'\mathbf{b}');mutations.append(('visible-known-coefficient',x))
x=copy.deepcopy(r);f=x['question'][':question/answer-fields'][0];key=check_refill.answer_id(f[':answer-field/correct']);next(a for a in f[':answer-field/choices'] if a[':answer/id']==key)[':answer/value']='37';mutations.append(('wrong-key',x))
results=[]
with tempfile.TemporaryDirectory(prefix='vector-regression-') as t:
 check_refill.check(r,Path(t))
 for name,x in mutations:
  assert x!=r,name
  try:check_refill.check(x,Path(t))
  except AssertionError as error:results.append(dict(name=name,rejected=True,reason=str(error)))
  else:raise AssertionError('mutation passed: '+name)
(H/'refill-regressions.json').write_text(json.dumps(dict(passed=True,mutations=results),indent=2)+'\n');print(json.dumps(results))
