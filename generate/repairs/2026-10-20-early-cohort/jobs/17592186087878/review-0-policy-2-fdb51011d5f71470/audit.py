import sys,os,json,pathlib,importlib.util,re,collections,hashlib,platform
sys.dont_write_bytecode=True
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=pathlib.Path.cwd(); PKG=(ROOT/'../workspace').resolve();sys.path.insert(0,str(PKG))
import generator as g
x=s.Symbol('x',positive=True); C=s.Symbol('C',real=True)
def save(name,v): (ROOT/name).write_text(json.dumps(v,indent=2,ensure_ascii=False,default=str)+'\n')
def parse(t):
 t=t.replace('\\\\','\\').replace('⁡','').replace('−','-')
 t=re.sub(r'\\operatorname\{(sin|cos|ln)\}',r'\\\1 ',t)
 for a,b in [(r'\left',''),(r'\right',''),(r'\,',''),(r'\cdot','*'),(r'\text{d}','d')]:t=t.replace(a,b)
 def grp(i):
  assert t[i]=='{',(t,i)
  j=i+1;depth=1
  while depth:
   depth+=(t[j]=='{')-(t[j]=='}');j+=1
  return t[i+1:j-1],j
 while r'\frac' in t:
  i=t.rfind(r'\frac'); a,j=grp(i+5);b,k=grp(j);t=t[:i]+'(('+a+')/('+b+'))'+t[k:]
 t=t.replace('{','(').replace('}',')').replace('^','**')
 for f in ['sin','cos','ln']:
  # displayed trig arguments here are simple integer*x, optional parentheses
  t=re.sub(r'\\'+f+r'\s*(-?\d*\s*x)',lambda m:('log' if f=='ln' else f)+'('+m[1]+')',t)
 t=t.replace('\\ln','log').replace('\\sin','sin').replace('\\cos','cos')
 t=t.replace('e','E')
 return parse_expr(t,local_dict={'x':x,'C':C,'E':s.E,'sin':s.sin,'cos':s.cos,'log':s.log},transformations=standard_transformations+(implicit_multiplication_application,))
def equation(q):
 text=q[':question/problem'];t=re.search(r'\$\$?(.*?)\$\$?',text,re.S)[1]
 for d in [r'\frac{\text{d}y}{\text{d}x}',r'\frac{dy}{dx}']:t=t.replace(d,'DERIV')
 a,t=t.split('DERIV'); b,r=t.split('y',1);r=r.lstrip('= ')
 r=re.split(r',',r)[0].strip().rstrip('.').strip()
 a=parse(a) if a.strip() else s.Integer(1);b=(s.Integer(1) if b.strip()=='+' else -s.Integer(1) if b.strip()=='-' else parse(b)) if b.strip() else 0
 return s.simplify(b/a),s.simplify(parse(r)/a)
def mathcheck(rec):
 q=rec['question'];P,Q=equation(q);rows=[]
 for f in q[':question/answer-fields']:
  key=f[':answer-field/key'];hits=[]
  for ch in f[':answer-field/choices']:
   v=parse(ch[':answer/value']);res=s.simplify(s.diff(v,x)-P*v if key=='field-1' else s.diff(v,x)+P*v-Q)
   good=res==0 and (v!=0 if key=='field-1' else s.diff(v,C)!=0)
   if good:hits.append(ch[':answer/id'])
  stored=f[':answer-field/correct'][1];rows.append({'field':key,'mathematical_hits':hits,'stored':stored,'passed':stored in hits and len(hits)==(2 if rec['generation']['raw_ambiguous_bank'] and key=='field-2' else 1)})
 return {'id':q[':question/id'],'template':rec['generation']['template'],'P':str(P),'Q':str(Q),'fields':rows,'passed':all(v['passed'] for v in rows)}

def main():
 records=[]
 for t,spec in g.TEMPLATES.items():
  for seed in range(72041,72041+(12 if spec['level']=='easy' else 4)):
   records.append(g.generate(spec['level'],seed,template=t))
 save('independent-records.json',records)
 replay=[];replayresults=[];src=json.load(open('../source/source.json'))['material']['kp'][':knowledge-point/questions']
 for q in src:
  p=q[':question/math-academy-id'];t=g.PROFILES[p]['template'];spc=g.TEMPLATES[t];params=dict(spc['base'])
  if p=='q-339139':params={'n':4,'b':5}
  r=g.generate(spc['level'],91103,profile=p,parameters=params);replay.append(r)
  fs={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}; comparisons=[]
  for f in q[':question/answer-fields']:
   a=[parse(c[':answer/value']) for c in f[':answer-field/choices']];b=[parse(c[':answer/value']) for c in fs[f[':answer-field/key']][':answer-field/choices']]
   same=len(a)==len(b) and all(any(s.simplify(v-w)==0 for w in b) for v in a)
   comparisons.append({'field':f[':answer-field/key'],'source_count':len(a),'replay_count':len(b),'full_bank_equivalent':same})
  replayresults.append({'id':q[':question/id'],'source':p,'comparisons':comparisons,'passed':all(a['full_bank_equivalent'] for a in comparisons)})
 save('source-replays.json',replay);save('source-replay-results.json',replayresults)
 checks=[]
 for r in records+replay+json.load(open('../samples.json')):
  try:checks.append(mathcheck(r))
  except Exception as e:checks.append({'id':r['question'][':question/id'],'error':repr(e),'passed':False})
 save('math-results.json',checks)
 save('runtime.json',{'python':platform.python_version(),'packages':{'sympy':s.__version__}})
 print(json.dumps({'records':len(records),'replays':len(replay),'math_checks':len(checks),'math_failures':[c for c in checks if not c['passed']],'replay_failures':[c for c in replayresults if not c['passed']]},default=str))
if __name__=='__main__':main()
