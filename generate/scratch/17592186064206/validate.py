"""Independent displayed calculus checks, exhaustive bounded banks, real radio grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('linear_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.Symbol('x',real=True)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def rational(text):
 text=text.strip().removeprefix('& =').strip()
 if not text:return sp.Integer(1)
 if text=='-':return sp.Integer(-1)
 text=re.sub(r'\\frac\{([0-9]+)\}\{([0-9]+)\}',r'(\1/\2)',text)
 return sp.sympify(text)
def polynomial(text):return sp.sympify(re.sub(r'(\d)x',r'\1*x',text),locals={'x':x})
def derivative(value):
 m=re.fullmatch(r'(.*?)\\operatorname\{ln\}⁡\|([^|]+)\|\+C',value);assert m,value
 c=rational(m[1]);d=polynomial(m[2]);return sp.cancel(c*sp.diff(d,x)/d)
def prompt_parameters(q):
 m=re.search(r'\\(?:d?frac)\{(\d+)\}\{([^}]+)\}',q[':question/problem']);assert m
 n=int(m[1]);p=sp.Poly(polynomial(m[2]),x);assert p.degree()==1
 return [n,int(p.coeff_monomial(x)),int(p.coeff_monomial(1))]
def fingerprint(q):return g.fingerprint(prompt_parameters(q))
def check(rec):
 meta=rec['generation'];q=rec['question'];p=prompt_parameters(q);assert p==meta['parameters']
 assert rec==g.generate('easy',meta['seed'],meta['template'],p)
 n,a,b=p;integrand=sp.cancel(n/(a*x+b));fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 bank=f[':answer-field/choices'];assert len(bank)==5
 ds=[derivative(z[':answer/value']) for z in bank]
 assert len(set(ds))==5,'equivalence modulo integration constants'
 correct=next(i for i,z in enumerate(bank) if z[':answer/id']==f[':answer-field/correct'][1]);assert correct==0 and ds[0]==integrand
 assert all(d!=integrand for d in ds[1:])
 # Extract the rendered substitution and verify its Jacobian and final answer.
 sol=q[':question/worked-solution'];u=re.search(r'First, let \$u=([^$]+)\.\$',sol);assert u and polynomial(u[1])==a*x+b
 du=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=([^\\]+)',sol);assert du and rational(du[1])==a
 if a!=1:assert r'\text{d}x='+g.tex(sp.Rational(1,a))+r'\text{d}u' in sol
 end=re.findall(r' & =(.*?)\\end\{aligned\}',sol,re.S)[-1].split(r' \\ ')[-1]
 assert derivative(end)==integrand
 logu=re.findall(r' & =([^&]*?)\\operatorname\{ln\}⁡\|u\|\+C',sol)[-1].split(r' \\ ')[-1]
 assert rational(logu)==sp.Rational(n,a)
 assert meta['mathematical_fingerprint']==g.fingerprint(p)
 assert '$$' not in [z[':answer/value'] for z in bank]
 return rec
def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==0 else 'rejected','purpose':'actual application radio ID grading'} for i,a in enumerate(f[':answer-field/choices'])]}
def main():
 source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};inputs=[];replay=[];review=[];all_records=[]
 for sid,t in g.PROFILES.items():
  r=check(g.generate('easy',0,sid,t['parameters']));q=r['question'];old=qs[sid];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'];assert q[':question/worked-solution']==old[':question/worked-solution']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  assert f[':answer-field/choices'][0][':answer/value']==of[':answer-field/correct'][':answer/value']
  replay.append({'source':sid,'profile':t['profile'],'matched_choices':5,'matched_distractors':4,'complete_bank_match':True,'prompt_exact':True,'solution_exact':True});inputs.append(native(sid,r))
  review.append('## '+sid+'\n\nOriginal\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(r)+'\n\nVariant\n\n'+g.markdown(check(g.generate('easy',42,sid))))
  ps=([n,1,b] for n in range(2,10) for b in range(1,13)) if t['profile']=='coefficient' else ([1,a,b] for a in range(-9,-1) for b in range(1,13)) if t['profile']=='negative-slope' else ([1,1,b] for b in range(-12,0)) if t['profile']=='negative-shift' else ([1,1,b] for b in range(2,13))
  for p in ps:
   r=check(g.generate('easy',0,sid,p));assert g.generate('easy',99,sid,p)['question']==r['question'];inputs.append(native(sid+' '+str(p),r));all_records.append(r)
 assert g.fingerprint([2,1,1])==g.fingerprint([4,2,2])
 # No supported declaration is inferred from the incomplete legacy bank.
 excluded=qs['q-49511'];assert ':question/worked-solution' not in excluded and ':question/difficulty' not in excluded and ':answer-field/correct' not in excluded[':question/answer-fields'][0]
 save('source-replay.json',{'passed':True,'complete_banks_matched':5,'complete_banks_total':5,'distractors_matched':20,'distractors_total':20,'profiles':replay,'excluded_incomplete_sources':['q-49511'],'exclusion_reason':'missing difficulty, correct designation and worked solution; retained unchanged'})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('previews.json',g.batch('easy',5,1902));(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'mathematical_checks':'independent rendered rational integrand and every choice derivative; distinct modulo constants; solution substitution/Jacobian/log coefficient/final answer','exhaustive_instances':len(all_records),'distinct_bounded_integrands':len({r['generation']['mathematical_fingerprint'] for r in all_records}),'source_fidelity':'5/5 complete banks; 20/20 distractors; exact prompt and worked solution; incomplete source excluded','native_grading':'all choices for every bounded parameter tuple','supported_levels':['easy'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'contract.json',HERE/'validate.py')}})
if __name__=='__main__':main()
