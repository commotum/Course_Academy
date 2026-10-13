"""Exhaustive independent calculus, source replay and actual radio grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.Symbol('x',real=True);K=sp.Symbol('K',positive=True)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def rational(t):
 t=t.strip().removeprefix("& =").strip()
 if not t:return sp.Integer(1)
 if t=='-':return sp.Integer(-1)
 t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1/\2)',t)
 return sp.sympify(t,locals={'K':K})
def polynomial(t):return sp.sympify(re.sub(r'(\d)x',r'\1*x',t),locals={'x':x})
def derivative(t):
 m=re.fullmatch(r'(.*?)\\operatorname\{ln\}⁡?(.*)',t);assert m,t
 c=rational(m[1]);rest=m[2];d=re.search(r'\|([^|]+)\|',rest);assert d,t
 d=polynomial(d[1]);sign=-1 if rest.startswith(r'(\frac{K}{|') else 1
 return sp.cancel(sign*c*sp.diff(d,x)/d)
def prompt_parameters(q):
 m=re.search(r'\\d?frac\{(\d+)\}\{([^}]+)\}',q[':question/problem']);assert m
 poly=sp.Poly(polynomial(m[2]),x);assert poly.degree()==1
 return [int(m[1]),int(poly.coeff_monomial(x)),int(poly.coeff_monomial(1))]
def fingerprint(q):return g.fingerprint(prompt_parameters(q))
def check(rec):
 meta=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1];p=prompt_parameters(q);assert p==meta['parameters']
 assert rec==g.generate(level,meta['seed'],meta['template'],p)
 n,a,b=p;target=sp.cancel(n/(a*x+b));f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];assert len(bank)==5
 ds=[derivative(z[':answer/value']) for z in bank];assert len(set(ds))==5,(p,ds)
 ci=next(i for i,z in enumerate(bank) if z[':answer/id']==f[':answer-field/correct'][1]);assert ds[ci]==target
 assert all(sp.cancel(d-target)!=0 for i,d in enumerate(ds) if i!=ci)
 # For the K-dependent wrong option, one accidental K value does not satisfy
 # the source's arbitrary-K identity. It cannot parameterize all antiderivatives.
 for d in ds:
  if K in d.free_symbols:assert sp.diff(d,K)!=0
 sol=q[':question/worked-solution'];assert '@@' not in sol and '@@' not in q[':question/problem']
 u=re.search(r'First, let \$u=([^$]+)\.\$',sol);assert u and polynomial(u[1])==a*x+b
 du=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=([^\\]+)',sol);assert du and rational(du[1])==a
 # Validate all rendered logarithmic antiderivative stages by their coefficients.
 logs=re.findall(r' & =(.*?)\\operatorname\{ln\}⁡?\|(?:u|[^|]+)\|\+C',sol,re.S)
 assert len(logs)>=2
 for z in logs:assert rational(z.split(r' \\ ')[-1].strip())==sp.Rational(n,a)
 last=sol.split('So, we finally conclude that')[-1];m=re.search(r'=(.*?)\.\s*\$\$',last,re.S);assert m
 assert derivative(m[1].strip())==target
 assert f'C={g.tex(sp.Rational(n,a))}'+r'\operatorname{ln}' in sol
 assert meta['mathematical_fingerprint']==g.fingerprint(p)
 return rec
def native(label,rec):
 f=rec['question'][':question/answer-fields'][0];ci=f[':answer-field/correct'][1]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==ci else 'rejected','purpose':'actual learner radio selection'} for z in f[':answer-field/choices']]}
def main():
 raw=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']};replays=[];inputs=[];allrs=[];review=[]
 for sid,t in g.PROFILES.items():
  r=check(g.generate(t['difficulty'],0,sid,t['parameters']));q=r['question'];old=qs[sid];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'],sid
  assert q[':question/worked-solution']==old[':question/worked-solution'],sid
  assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']),sid
  correct=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert correct==of[':answer-field/correct'][':answer/value']
  replays.append({'source':sid,'complete_bank_match':True,'choices_matched':5,'distractors_matched':4,'prompt_exact':True,'solution_exact':True})
  variant=check(g.generate(t['difficulty'],42,sid));review.append('## '+sid+'\n\nOriginal\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(r)+'\n\nVariant\n\n'+g.markdown(variant))
  for p in g.candidates(sid):
   z=check(g.generate(t['difficulty'],0,sid,p));assert g.generate(t['difficulty'],99,sid,p)['question']==z['question'];inputs.append(native(sid+' '+str(p),z));allrs.append(z)
 erroneous=qs['q-113533'][':question/answer-fields'][0];ds=[derivative(z[':answer/value']) for z in erroneous[':answer-field/choices']];assert ds.count(sp.cancel(1/(3*x+4)))==2
 save('source-replay.json',{'passed':True,'complete_banks_matched':6,'complete_banks_total':6,'distractors_matched':24,'distractors_total':24,'profiles':replays,'exclusions':{'q-113533':'two equivalent correct options, both derivatives 1/(3x+4); log(D/K) and log(KD) differ by arbitrary constant','q-49513':'unrated; missing correct and worked solution','q-49516':'unrated; missing correct and worked solution','q-49515':'rated moderate but no answer fields; ungradable'}})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('previews.json',g.batch('easy',5,1975)+g.batch('moderate',5,1975));(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 counts={level:len({r['generation']['mathematical_fingerprint'] for r in allrs if r['question'][':question/difficulty']==':question.difficulty/'+level}) for level in ('easy','moderate')}
 save('validation.json',{'passed':True,'exhaustive_instances':len(allrs),'distinct_bounded_integrands':counts,'mathematics':'independent rendered rational derivatives; all options distinct; complete substitution and final solution checks; arbitrary positive K','fidelity':'6/6 supported complete banks; 24/24 distractors; source errors and incomplete sources explicitly excluded','native_grading':'actual learning::grade_field checks all options for all bounded parameter tuples','supported_levels':['easy','moderate'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'contract.json',HERE/'validate.py')}})
if __name__=='__main__':main()
