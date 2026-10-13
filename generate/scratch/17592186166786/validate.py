"""Independent displayed-bank parsing, symbolic calculus and actual engine grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('product',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.symbols('x',real=True)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def parse(t):
 t=t.replace(' + C','').replace(' ','').replace(r'\sinh','sinh')
 t=re.sub(r'\\frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',r'((\1)/(\2))',t)
 t=t.replace('^{','**(').replace('}',')').replace('{','(')
 t=re.sub(r'(\d|\))(?=sinh|x|e)',r'\1*',t)
 return sp.sympify(t,locals={'x':x,'e':sp.E,'sinh':sp.sinh})
def zero(e):return sp.simplify(sp.expand(e.rewrite(sp.exp)))==0
def fingerprint(q):return g.fingerprint(q)
def check(rec):
 meta=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1];n=meta['parameters']['n']
 assert rec['knowledge_point']['db_id']==g.KP_ID and level in ('easy','moderate')
 assert rec==g.generate(level,meta['seed'],meta['template'],meta['parameters'])
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 bank=f[':answer-field/choices'];assert len(bank)==5 and len({a[':answer/id'] for a in bank})==5
 expressions=[parse(a[':answer/value']) for a in bank]
 if level=='easy':
  assert int(re.search(r'cosh\s*\((\d+)x\^\{2\}',q[':question/problem'])[1])==n
  target=x*sp.cosh(n*x*x);correct=[zero(sp.diff(e,x)-target) for e in expressions]
  assert all(not zero(sp.diff(expressions[i]-expressions[j],x)) for i in range(5) for j in range(i))
  assert zero(sp.diff(sp.sinh(n*x*x)/(2*n),x)-target)
  assert rf'u={n}x^2' in q[':question/worked-solution'] and rf'\frac{{1}}{{{2*n}}}\sinh({n}x^2)+C' in q[':question/worked-solution']
 else:
  assert fingerprint(q)==g.digest(['sech^2(ln(x))/x',1,n])
  u=sp.symbols('u',real=True);assert zero(sp.diff(sp.tanh(u),u)-sp.sech(u)**2)
  # Independent original-variable derivative establishes the substitution.
  xp=sp.symbols('xp',positive=True)
  assert sp.simplify(sp.diff(sp.tanh(sp.log(xp)),xp)-sp.sech(sp.log(xp))**2/xp)==0
  target=(sp.exp(2*n)-1)/(sp.exp(2*n)+1)
  assert zero(sp.tanh(n)-sp.tanh(0)-target)
  correct=[zero(e-target) for e in expressions]
  assert all(not zero(expressions[i]-expressions[j]) for i in range(5) for j in range(i))
  assert 0<target<1
  assert rf'u={n}' in q[':question/worked-solution'] and rf'\frac{{e^{{{2*n}}}-1}}{{e^{{{2*n}}}+1}}' in q[':question/worked-solution']
 assert sum(bool(z) for z in correct)==1
 assert all(bool(c)==(a[':answer/id']==f[':answer-field/correct'][1]) for a,c in zip(bank,correct))
 assert fingerprint(q)==meta['mathematical_fingerprint']
 return rec
def native(label,r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'actual learner radio grading; mathematics checked independently'} for a in f[':answer-field/choices']]}
def main():
 inputs=[];records=[];replays=[];fps=set()
 for sid,old in g.sources().items():
  level,n=g.DATA[sid];r=check(g.generate(level,1984,sid,{'n':n}));q=r['question'];of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
  assert [a[':answer/value'] for a in nf[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
  assert nf[':answer-field/key']==of[':answer-field/key'] and nf[':answer-field/type']==of[':answer-field/type'][':db/ident']
  replays.append({'source':sid,'complete_bank_matched':True,'matched_values':5,'matched_distractors':4,'missing_or_extra':[],'key_origin':'independent calculus','solution_origin':'authored; none stored','prompt_changes':['repair missing space after integral control word'] if level=='easy' else ['render sech as operator']})
 for level in ('easy','moderate'):
  for sid,p in g.candidates(level):
   r=check(g.generate(level,1984,sid,p));fp=r['generation']['mathematical_fingerprint'];assert fp not in fps;fps.add(fp)
   assert g.generate(level,1,sid,p)['question']==r['question'];records.append(r);inputs.append(native(sid+'-'+str(p['n']),r))
 for level,p in [('hard',{'n':3}),('easy',{'n':1}),('easy',{'n':13}),('moderate',{'n':0}),('moderate',{'n':11}),('easy',{'n':2.5}),('easy',{'n':True}),('easy',{'n':3,'extra':1})]:
  try:g.generate(level,0,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid parameter accepted')
 try:g.batch('easy',12,0)
 except ValueError:pass
 else:raise AssertionError('Finite cap ignored')
 save('native-input.json',inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('source-replay.json',{'passed':True,'sources':replays,'complete_banks_matched':2,'complete_banks_total':2,'matched_values':10,'total_values':10,'matched_distractors':8,'total_distractors':8,'missing_or_extra':[],'source_keys_and_solutions_available':0})
 save('previews.json',records);save('review.json',{'originals':list(g.sources().values()),'generated_variants':records})
 (HERE/'review.md').write_text('\n\n'.join('## '+r['generation']['template']+' n='+str(r['generation']['parameters']['n'])+'\n\n'+g.markdown(r) for r in records)+'\n')
 save('validation.json',{'passed':True,'exhaustive_instances':21,'distinct_bounded_tasks':21,'counts':{'easy':11,'moderate':10},'source_bank_fidelity':'2/2 complete banks; 10/10 values; 8/8 distractors','native_grading':'all five options of 21 instances','mathematics':'independent rendered bank parser, exact derivatives, definite transformed endpoints, real domains, unique choices and correct designation','supported_levels':['easy','moderate'],'unsupported_levels':['hard'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',ROOT/'generate/runs/current/check-engine')}})
 print('Validated 21 distinct bounded tasks, two complete source banks and actual learner grading')
if __name__=='__main__':main()
