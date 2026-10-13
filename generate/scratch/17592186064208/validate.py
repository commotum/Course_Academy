"""Parse printed prompts, answers and solution rows independently; real radio grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('combined_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.Symbol('x',real=True)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def rational(t):
 t=t.strip()
 if not t or t=='+':return sp.Integer(1)
 if t=='-':return sp.Integer(-1)
 t=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1/\2)',t);return sp.sympify(t)
def polynomial(t):return sp.sympify(re.sub(r'(\d)x',r'\1*x',t),locals={'x':x})
def prompt(q):
 ds=re.findall(r'\\(?:d?frac)\{1\}\{([^}]+)\}',q[':question/problem']);assert len(ds)==2
 return list(map(polynomial,ds))
def fingerprint(q):return g.digest(str(sp.cancel(sum(1/d for d in prompt(q)))))
def derivative(value):
 m=re.fullmatch(r'(.*?)\\operatorname\{ln\}⁡\(K\|(.*?)\|\)',value);assert m,value
 c=rational(m[1]);inner=m[2]
 m=re.fullmatch(r'\\frac\{([^}]+)\}\{([^}]+)\}',inner)
 if m:z=polynomial(m[1])/polynomial(m[2])
 else:
  m=re.fullmatch(r'\((.*?)\)\((.*?)\)',inner);assert m,inner
  z=polynomial(m[1])*polynomial(m[2])
 return sp.cancel(c*sp.diff(z,x)/z)
def check(rec):
 meta=rec['generation'];q=rec['question'];assert rec==g.generate('hard',meta['seed'],meta['template'],meta['parameters'])
 ds=prompt(q);integrand=sp.cancel(sum(1/d for d in ds));assert all(sp.Poly(d,x).degree()==1 for d in ds)
 assert sp.solve(ds[0],x)!=sp.solve(ds[1],x)
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 bank=f[':answer-field/choices'];assert len(bank)==5 and len({a[':answer/id'] for a in bank})==5
 vals=[derivative(a[':answer/value']) for a in bank];assert len(set(vals))==5,'Equivalent distractors'
 right=[a[':answer/id'] for a,z in zip(bank,vals) if z==integrand];assert right==[f[':answer-field/correct'][1]]
 # Verify the rendered solution's split integral, separate log coefficients,
 # combined log, replacement C=(1/a)ln K, and final antiderivative.
 sol=q[':question/worked-solution'];rows=sol.split(r' \\ ');assert len(rows)==4
 assert re.findall(r'\\frac\{1\}\{([^}]+)\}',rows[0])==[strpart for strpart in re.findall(r'\\frac\{1\}\{([^}]+)\}',q[':question/problem'])]*2
 split=rows[1].split('& =')[1];matches=re.findall(r'(.*?)\\operatorname\{ln\}⁡\|([^|]+)\|',split);assert len(matches)==2
 coefs=[rational(z[0]) for z in matches];args=[polynomial(z[1]) for z in matches];assert args==ds
 assert all(c==1/sp.diff(d,x) for c,d in zip(coefs,ds))
 final=rows[3].split('& =')[1].split(r'\end{aligned}')[0];assert derivative(final)==integrand
 mid=rows[2].split('& =')[1];mid=mid.replace('\\text{\u00a0}','').replace(' ','')
 c=rational(re.match(r'(.*?)\\operatorname',mid)[1]);assert c==coefs[0]
 combined=re.search(r'\|(.*?)\|',mid)[1];reconstructed=str(c)+r'\operatorname{ln}⁡(K|'+combined+'|)'
 assert derivative(reconstructed)==integrand
 constant=mid.split('|')[-1];cm=re.search(r'\+(.*?)\\operatorname\{ln\}⁡K',constant);assert cm and rational(cm[1])==c
 assert meta['mathematical_fingerprint']==fingerprint(q)
 return rec
def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual application radio grading'} for a in f[':answer-field/choices']]}
def main():
 qs={q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']};inputs=[];replay=[];fps=set();n=0;review=[]
 for sid,t in g.PROFILES.items():
  r=check(g.generate('hard',0,sid,t['parameters']));q=r['question'];old=qs[sid];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  replay.append({'source':sid,'profile':sid,'matched_choices':5,'matched_distractors':4,'complete_bank_match':True,'prompt_exact':True,'solution_exact':True})
  variant=check(g.generate('hard',42,sid));review.append('## '+sid+'\n\nOriginal\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(r)+'\n\nVariant\n\n'+g.markdown(variant))
  for p in g.candidates(sid):
   r=check(g.generate('hard',0,sid,p));assert g.generate('hard',99,sid,p)['question']==r['question'];inputs.append(native(sid+' '+str(p),r));fps.add(r['generation']['mathematical_fingerprint']);n+=1
 excluded=qs['q-49521'];assert ':question/worked-solution' not in excluded and ':question/difficulty' not in excluded and ':answer-field/correct' not in excluded[':question/answer-fields'][0]
 save('source-replay.json',{'passed':True,'complete_banks_matched':9,'complete_banks_total':9,'distractors_matched':36,'distractors_total':36,'profiles':replay,'excluded_incomplete_sources':['q-49521'],'exclusion_reason':'missing difficulty, correct designation and solution; preserved unchanged'})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('previews.json',g.batch('hard',5,1908));(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'mathematical_checks':'independent printed integrand, option derivatives distinct modulo constants, poles, every worked solution row and K>0 constant substitution','exhaustive_instances':n,'distinct_bounded_integrands':len(fps),'source_fidelity':'9/9 complete banks; 36/36 distractors; exact prompt, solution and choice notation','native_grading':'all choices for every bounded parameter tuple','supported_levels':['hard'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'contract.json',HERE/'validate.py')}})
 print('Validated',n,'instances,',len(fps),'distinct integrands')
if __name__=='__main__':main()
