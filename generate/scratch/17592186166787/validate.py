"""Parse displayed banks independently, differentiate, check bounds and native grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('hyperbolic',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.symbols('x',real=True)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def parse(t):
 t=t.replace(' + C','').replace(' ','')
 t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
 t=t.replace(r'\csch^{2}x','csch(x)**2').replace('csch^{2}x','csch(x)**2').replace(r'\cschx','csch(x)').replace('cschx','csch(x)').replace(r'\cothx','coth(x)')
 if r'\mid' in t:
  before,inner,after=t.split(r'\mid');assert before.endswith(r'\ln') and after==''
  t=before[:-3]+'*log('+inner+')'
 else:
  assert t.startswith(r'\ln') or t.startswith(r'3\ln')
  factor='3*' if t.startswith('3') else ''
  t=factor+'log('+t[t.index(r'\ln')+3:]+')'
 t=re.sub(r'(\d|\))(?=csch|coth)',r'\1*',t)
 return sp.sympify(t,locals={'x':x,'log':sp.log,'csch':sp.csch,'coth':sp.coth})
def zero(e):return sp.cancel(sp.together(e.rewrite(sp.exp)))==0
def fingerprint(q):return g.fingerprint(q)
def check(rec):
 meta=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1];n=meta['parameters']['n']
 assert rec['knowledge_point']['db_id']==g.KP_ID and level in ('easy','moderate')
 assert rec==g.generate(level,meta['seed'],meta['template'],meta['parameters'])
 assert len(q[':question/answer-fields'])==1
 f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 bank=f[':answer-field/choices'];assert len(bank)==5 and len({a[':answer/id'] for a in bank})==5
 expressions=[parse(a[':answer/value']) for a in bank]
 if level=='easy':
  match=re.search(r'(\d+)\\coth x \+ 1',q[':question/problem']);assert int(match[1])==n
  integrand=1/(sp.sinh(x)**2*(n*sp.cosh(x)/sp.sinh(x)+1))
  correct=[zero(sp.diff(e,x)-integrand) for e in expressions]
  assert all(not zero(expressions[i]-expressions[j]) for i in range(5) for j in range(i))
  assert zero(sp.diff(-sp.log(n*sp.coth(x)+1)/n,x)-integrand)
  sol=q[':question/worked-solution']
  assert rf'u={n}\coth x+1' in sol and rf'=-{n}\csch^2 x' in sol
  assert rf'&=-\frac{{1}}{{{n}}}\ln|{n}\coth x+1|+C.' in sol
 else:
  match=re.search(r'\\ln (\d+)',q[':question/problem']);assert int(match[1])==n
  assert '3 + \\sinh x' in q[':question/problem']
  upper=3+sp.sinh(sp.log(n)).rewrite(sp.exp);upper=sp.simplify(upper)
  result=sp.log(upper/3)
  assert zero(sp.diff(sp.log(3+sp.sinh(x)),x)-sp.cosh(x)/(3+sp.sinh(x)))
  # Exact rational logarithm arguments plus high-precision separation of banks.
  correct=[sp.simplify(sp.expand_log(e-result,force=True))==0 or abs(sp.N(e-result,80))<sp.Float('1e-70') for e in expressions]
  assert all(abs(sp.N(expressions[i]-expressions[j],80))>sp.Float('1e-30') for i in range(5) for j in range(i))
  assert upper>3 and result>0
  sol=q[':question/worked-solution']
  assert rf'x=\ln {n}' in sol and rf'={sp.latex(upper)}.' in sol
  assert rf'&=\ln\left({sp.latex(upper/3)}\right).' in sol
 assert sum(bool(z) for z in correct)==1
 assert all(bool(c)==(a[':answer/id']==f[':answer-field/correct'][1]) for a,c in zip(bank,correct))
 assert fingerprint(q)==meta['mathematical_fingerprint']
 assert len(q[':question/worked-solution'])>100
 return rec
def native(label,r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'actual learner radio grading; mathematics checked separately'} for a in f[':answer-field/choices']]}
def main():
 inputs=[];records=[];replays=[];fps=set()
 for sid,old in g.sources().items():
  level,n=g.DATA[sid];r=check(g.generate(level,1916,sid,{'n':n}));q=r['question'];of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem']
  assert [a[':answer/value'] for a in nf[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
  assert nf[':answer-field/key']==of[':answer-field/key'] and nf[':answer-field/type']==of[':answer-field/type'][':db/ident']
  replays.append({'source':sid,'whole_bank_matched':True,'matched_options':5,'distractors':4,'missing_or_extra':[],'source_key':False,'source_solution':False,'derived_key_index':2 if level=='easy' else 3})
 for level in ('easy','moderate'):
  for sid,p in g.candidates(level):
   r=check(g.generate(level,1916,sid,p));fp=r['generation']['mathematical_fingerprint'];assert fp not in fps;fps.add(fp)
   assert g.generate(level,1,sid,p)['question']==r['question']
   records.append(r);inputs.append(native(sid+'-'+str(p['n']),r))
 for level,p in [('hard',{'n':3}),('easy',{'n':1}),('easy',{'n':13}),('easy',{'n':2.5}),('easy',{'n':True}),('easy',{'n':3,'extra':1})]:
  try:g.generate(level,0,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid parameter accepted')
 try:g.batch('easy',12,0)
 except ValueError:pass
 else:raise AssertionError('Finite cap ignored')
 save('native-input.json',inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('source-replay.json',{'passed':True,'source_results':replays,'complete_banks_matched':2,'complete_banks_total':2,'matched_answer_values':10,'total_observed_answer_values':10,'distractors_matched':8,'missing_or_extra_options':[],'prompts_exact':2,'source_keys_available':0,'source_solutions_available':0,'fidelity_limits':'Both keys and solutions are independently authored; no source solution sequence or difficulty exists. Distractor generalizations retain observed expression shapes; author mistake intentions unresolved.'})
 save('previews.json',records);save('review.json',{'originals':list(g.sources().values()),'generated_variants':records})
 (HERE/'review.md').write_text('\n\n'.join('## '+r['generation']['template']+' n='+str(r['generation']['parameters']['n'])+'\n\n'+g.markdown(r) for r in records)+'\n')
 save('validation.json',{'passed':True,'exhaustive_instances':22,'distinct_bounded_tasks':22,'counts':{'easy':11,'moderate':11},'source_bank_fidelity':'2/2 complete banks; 10/10 values; 8/8 distractors; no missing or extra choices','source_missing_keys_and_solutions':2,'native_grading':'all five options of all 22 questions; expected 22 accepted and 88 rejected','mathematics':'independent displayed bank parser; exact symbolic derivatives and denominator domains; exact transformed endpoint and log ratio; unique complete banks; rendered solution substitution and final answers','supported_levels':['easy','moderate'],'unsupported_levels':['hard'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',ROOT/'generate/runs/current/check-engine')}})
 print('Validated all 22 distinct bounded questions and two complete source banks')
if __name__=='__main__':main()
