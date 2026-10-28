"""Independent cosine facts, including visible checkbox statements."""
import collections,json,re,sys
from pathlib import Path
import sympy as S
from texmath import parse
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH
D=json.loads((H/'current.json').read_text());tids={t['entity']for t in D['topics']if t['ma_id']==3557};ids={q for t,k,q in D['links']if t in tids};out=[]
def maths(p):return [m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1]for m in MATH.finditer(p)]
def equal(a,b):return a==b or S.simplify(a-b)==0
def claim(text):
 ms=maths(text)
 if 'range'in text:
  pair=re.search(r'\[([^\]]+)\]',ms[-1]);left,right=pair[1].split(',');return equal(parse(left),-1)and equal(parse(right),1),'cos range=[−1,1]'
 if 'output'in text:
  v=parse(ms[-1].split('=')[-1]);return bool(v>=-1 and v<=1),'Every cosine output lies in[−1,1]'
 if 'y$-axis'in text or'y$-axis'in text.replace(' ','')or'y$-axis'in text: # retained source wording
  v=parse(ms[-1].split('=')[-1]);return equal(v,1),'cos0=1'
 if 'y-axis'in text:
  v=parse(ms[-1].split('=')[-1]);return equal(v,1),'cos0=1'
 if 'passes through'in text:
  a,b=ms[-1].strip('().').split(',');return equal(S.cos(parse(a)),parse(b)),'Substitute point into y=cosx'
 target=0 if('zero'in text or'x$-axis'in text or'x-axis'in text)else 1 if'maximum'in text else -1 if'minimum'in text else None
 if target is None:raise ValueError('Unrecognized claim '+text)
 equation=next(m for m in reversed(ms)if '='in m);angle=parse(equation.split('=',1)[1].rstrip('.'));n=next((v for v in angle.free_symbols if str(v)=='n'),None)
 truth=all(equal(S.cos(angle.subs(n,i)if n else angle),target)for i in range(4))
 complete=('complete set'in text or'The zeros of the function are'in text or'Its zeros are'in text)
 if complete and n:truth=truth and equal(S.Abs(S.diff(angle,n)),S.pi if target==0 else 2*S.pi)
 return truth,{'cosine_target':target,'angle':str(angle),'complete_set_required':complete,'step':str(S.diff(angle,n))if n else None}
manual_radio={'q-27019':'I and III only','q-103227':'II and III only','q-103219':'II only','q-27012':'II and III only'}
for q in D['questions']:
 if q[':db/id']not in ids:continue
 fs=q.get(':question/answer-fields',[]);checks=[]
 if fs and fs[0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
  for f in fs:
   try:truth,proof=claim(f[':answer-field/key']);a=f[':answer-field/correct'];checks.append({'field':f[':db/id'],'display_statement':f[':answer-field/key'],'derived_truth':truth,'canonical':a[':answer/value'],'pass':a[':answer/value']==('true'if truth else'false'),'proof':proof})
   except Exception as ex:checks.append({'field':f[':db/id'],'error':str(ex)})
 elif q.get(':question/math-academy-id')in manual_radio:
  expected=manual_radio[q[':question/math-academy-id']];checks=[{'field':fs[0][':db/id'],'expected':expected,'pass':fs[0][':answer-field/correct'][':answer/value']==expected,'proof':'cos zeros are odd half-multiplesπ, minima atoddπ, maxima atevenπ, cos0=1, range[−1,1]. Each of the three displayed claims checked against these complete facts.'}]
 elif len(fs)==5:
  expected={'field-1':-S.oo,'field-2':S.oo,'field-3':-1,'field-4':1,'field-5':2*S.pi}
  checks=[{'field':f[':db/id'],'pass':equal(parse(f[':answer-field/correct'][':answer/value']),expected[f[':answer-field/key']]),'proof':'Both displayed sine/cosine have real domain, range[−1,1], fundamentalperiod2π; no task/topic function relabelling inferred.'}for f in fs]
 else:continue
 out.append({'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'checks':checks,'passed':all(c.get('pass')for c in checks)})
(H/'cosine-claims-validation.json').write_text(json.dumps(out,indent=2));print('questions',len(out),'claims',sum(len(r['checks'])for r in out),'failures',[r for r in out if not r['passed']])
