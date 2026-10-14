"""Check actual independent variables before any symbolic proxy normalization."""
import re,json,importlib.util,copy
from pathlib import Path
D=Path(__file__).resolve().parent

def check(record):
 q=record['question'];p=q[':question/problem']
 m=re.search(r'\\text\{d\}\s*(\\theta|[xyθ])',p)or re.search(r'd([xyθ])',p)
 assert m,'missing displayed differential'
 var=m[1].replace('θ',r'\theta')
 strings=[q.get(':question/worked-solution',''),*[a[':answer/value']for f in q.get(':question/answer-fields',[])for a in f[':answer-field/choices']]]
 count=0
 for t in strings:
  t=re.sub(r'\\operatorname\{(sin|cos|tan)\}',r'\1',t).replace('⁡','')
  for a in re.findall(r'(?:sin|cos|tan)(?:\}\^\{2\}|\^\{2\})?\s*(?:[({]\s*)?(\\theta|[xyθ])',t):
   assert a.replace('θ',r'\theta')==var,(var,a,t);count+=1
  for a in re.findall(r'\\text\{d\}\s*(\\theta|[xyθ])',t):assert a.replace('θ',r'\theta')==var
 return count

def main():
 z=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
 rs=json.load(open(D/'review.json'))
 for c in json.load(open(D/'source-cases.json')):
  for p in [c['parameters'],{k:[8,7][i]for i,k in enumerate(c['parameters'])}]:rs.append(g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=p))
 n=sum(check(r)for r in rs)
 r=g.generate('easy',template='cos',parameters={'a':-5});bad=copy.deepcopy(r);f=bad['question'][':question/answer-fields'][0]
 for a in f[':answer-field/choices']:a[':answer/value']=a[':answer/value'].replace(' x',' y')
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('stale variable mutation escaped')
 (D/'variable-readback.json').write_text(json.dumps({'status':'passed','records':len(rs),'actual_trig_arguments':n,'stale_variable_mutation':'rejected','before_proxy_normalization':True},indent=2))
 print('Variable readback:',len(rs),'records,',n,'actual arguments; stale-variable mutation rejected.')
if __name__=='__main__':main()
