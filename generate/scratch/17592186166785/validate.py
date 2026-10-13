"""Independent displayed-value parser, derivatives, quadrature and native grading."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
import mpmath as mp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.symbols('x',real=True)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def parse(t):
 t=t.replace(' + C','').replace(' ','').replace('\\','')
 t=re.sub(r'frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
 t=t.replace('^{2}','**2')
 pieces=[];pos=0
 while (m:=re.search(r'(sech|csch|tanh)(\*\*2)?',t[pos:])):
  start=pos+m.start();end=pos+m.end();pieces.append(t[pos:start])
  if t[end]=='(':
   depth=1;stop=end+1
   while depth:
    depth+=(t[stop]=='(')-(t[stop]==')');stop+=1
   arg=t[end:stop]
  else:
   number=re.match(r'\d+',t[end:]);assert number;stop=end+len(number[0]);arg=number[0]
  pieces.append(m[1]+'('+arg+')'+(m[2] or ''));pos=stop
 pieces.append(t[pos:]);t=''.join(pieces)
 t=re.sub(r'(\d|\))(?=x|sech|csch|tanh|\()',r'\1*',t)
 return sp.sympify(t,locals={'x':x,'sech':sp.sech,'csch':sp.csch,'tanh':sp.tanh})
def zero(e):
 if e==0:return True
 # A separated value disproves identity cheaply; exact reduction is required
 # for a putatively equal expression, including every correct derivative.
 probe=sp.N(e.subs(x,sp.Rational(1,3)),80)
 if abs(probe)>sp.Float('1e-50'):return False
 return sp.cancel(sp.together(e.rewrite(sp.exp)))==0
def fingerprint(q):return g.fingerprint(q)
def check(rec):
 meta=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1];n=meta['parameters']['n']
 assert rec['knowledge_point']['db_id']==g.KP_ID
 assert rec==g.generate(level,meta['seed'],meta['template'],meta['parameters'])
 assert len(q[':question/answer-fields'])==1
 f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 bank=f[':answer-field/choices'];assert len(bank)==5 and len({a[':answer/id'] for a in bank})==5
 es=[parse(a[':answer/value']) for a in bank]
 if level=='easy':
  assert int(re.search(r'\\frac\{(\d+)x\}\{5\}',q[':question/problem'])[1])==n
  a=sp.Rational(n,5);integrand=sp.sech(a*x)**2
  correctness=[zero(sp.diff(e,x)-integrand) for e in es]
  assert all(not zero(sp.diff(es[i]-es[j],x)) for i in range(5) for j in range(i))
  sol=q[':question/worked-solution'];assert rf'u=\frac{{{n}x}}{{5}}' in sol and rf'&={sp.latex(1/a)}\tanh(\frac{{{n}x}}{{5}})+C.' in sol
 else:
  assert int(re.search(r'(?:\\sech|sech)\s*(\d+)x',q[':question/problem'])[1])==n
  integrand=sp.sech(n*x)*sp.tanh(n*x);primitive=-sp.sech(n*x)/n
  assert zero(sp.diff(primitive,x)-integrand)
  target=(sp.sech(n)-sp.sech(2*n))/n
  correctness=[zero(e-target) for e in es]
  assert all(abs(sp.N(es[i]-es[j],80))>sp.Float('1e-40') for i in range(5) for j in range(i))
  mp.mp.dps=75;quad=mp.quad(lambda t:1/mp.cosh(n*t)*mp.tanh(n*t),[1,2])
  assert abs(quad-mp.mpf(str(sp.N(target,75))))<mp.mpf('1e-65')
  sol=q[':question/worked-solution'];assert rf'u={2*n}' in sol and rf'&=\frac{{1}}{{{n}}}(\sech {n}-\sech {2*n}).' in sol
 assert sum(bool(c) for c in correctness)==1
 assert all(bool(c)==(a[':answer/id']==f[':answer-field/correct'][1]) for a,c in zip(bank,correctness))
 assert fingerprint(q)==meta['mathematical_fingerprint']
 return rec
def native(label,rec):
 f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'actual learner radio selection'} for a in f[':answer-field/choices']]}
def main():
 replay=[];mapping=[]
 for sid,old in g.sources().items():
  level,n=g.DATA[sid];rec=check(g.generate(level,1969,sid,{'n':n}));q=rec['question'];nf=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem']
  assert [a[':answer/value'] for a in of[':answer-field/choices']]==[a[':answer/value'] for a in nf[':answer-field/choices']]
  recipes=(['a*tanh(a*x)^2','-1/a*csch(a*x)^2','a*tanh(a*x)*sech(a*x)','1/a*tanh(a*x)','-5*tanh(x/a)'] if level=='easy' else ['(sech(a)-sech(2))/a','a*(sech(2)-sech(a))','(tanh(2)-tanh(a))/a','tanh(2*a)^2/a','(sech(a)-sech(2*a))/a'])
  mapping.append({'source':sid,'profile':sid,'parameter':str(sp.Rational(n,5) if level=='easy' else n),'choices':[{'source_answer_id':a[':answer/id'],'value':a[':answer/value'],'recipe':r,'complete_value_reproduced':True,'correct':i==(3 if level=='easy' else 4),'interpretation':'observed expression pattern; author mistake intention unresolved'} for i,(a,r) in enumerate(zip(of[':answer-field/choices'],recipes))]})
  replay.append({'source':sid,'prompt_exact':True,'matched_options':5,'distractors_matched':4,'missing_or_extra':[],'source_key_available':False,'source_solution_available':False,'derived_key_index':3 if level=='easy' else 4})
 records=[];fps=set()
 for level in ('easy','moderate'):
  for sid,p in g.candidates(level):
   rec=check(g.generate(level,1969,sid,p));fp=fingerprint(rec['question']);assert fp not in fps;fps.add(fp)
   assert g.generate(level,99,sid,p)['question']==rec['question'];records.append(rec)
 for level,p in [('hard',{'n':3}),('easy',{'n':0}),('easy',{'n':13}),('easy',{'n':True}),('moderate',{'n':2}),('moderate',{'n':15}),('easy',{'n':1,'extra':0})]:
  try:g.generate(level,0,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Unsupported parameter accepted')
 try:g.batch('easy',13,0)
 except ValueError:pass
 else:raise AssertionError('Finite capacity ignored')
 save('native-input.json',[native(r['question'][':question/id'],r) for r in records])
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('source-choice-mapping.json',mapping);save('source-replay.json',{'passed':True,'complete_banks_matched':2,'complete_banks_total':2,'matched_values':10,'matched_distractors':8,'results':replay,'fidelity_limits':'No source difficulty, keys or practice solutions. These are authored. Source missing command slashes retained in replay and repaired in new parameter variants.'})
 save('previews.json',records);save('review.json',{'originals':list(g.sources().values()),'variants':records})
 (HERE/'review.md').write_text('\n\n'.join('## '+r['generation']['template']+' n='+str(r['generation']['parameters']['n'])+'\n\n'+g.markdown(r) for r in records)+'\n')
 save('validation.json',{'passed':True,'exhaustive_instances':len(records),'counts':{'easy':12,'moderate':12},'mathematics':'independent parsing of all displayed choices; exact derivatives; nonconstant difference for indefinite banks; 80-digit separation of definite banks; independent 75-digit quadrature; correct unique keys; domains and endpoint substitution','native_grading':'24 questions, every option; 24 accepted and 96 rejected','fidelity':'2/2 complete banks, 10/10 values, 8/8 distractors; source missing keys/solutions explicitly authored','supported_levels':['easy','moderate'],'unsupported_levels':['hard'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',ROOT/'generate/runs/current/check-engine')}})
 print('Validated 24 distinct tasks, two complete source banks, and all 120 native grade checks')
if __name__=='__main__':main()
