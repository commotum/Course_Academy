"""Independent visible-bank parsing, exact calculus, replay and application grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def expr(t):
 # Closed grammar for these bounded visible answers, independent of objects().
 def frac(m):return '('+m[1]+'/'+m[2]+')'
 t=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',frac,t)
 t=re.sub(r'e\^\{(\d+)\}',r'exp(\1)',t)
 t=t.replace(r'\cosh','cosh').replace(r'\sinh','sinh')
 t=re.sub(r'(\d)x',r'\1*x',t)
 t=re.sub(r'(?<=[\d)])(?=(?:cosh|sinh))','*',t)
 assert re.fullmatch(r'[0-9xC+\-*/().\sacoeshinp]+',t),t
 return s.sympify(t,locals={'x':g.X,'C':g.C,'cosh':s.cosh,'sinh':s.sinh,'exp':s.exp})
def independent(r):
 q,md=r['question'],r['generation'];m,p=md['template'],md['parameters'];level=q[':question/difficulty'].split('/')[-1]
 assert r==g.generate(level,md['seed'],m,p,md['bank_profile'])
 if m=='q-95532':
  z=p['a']*g.X+p['b'];integrand=s.sinh(z);expected=s.cosh(z)/p['a']+g.C
 else:
  integrand=s.cosh((2*g.X-1)/p['n']);expected=s.integrate(integrand,(g.X,s.Rational(1,2),1))
 f=q[':question/answer-fields'][0];vals=[expr(a[':answer/value']) for a in f[':answer-field/choices']];ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
 assert s.simplify(vals[ci]-expected)==0
 if m=='q-95532':assert s.simplify(s.diff(vals[ci],g.X)-integrand)==0
 for i,a in enumerate(vals):
  for b in vals[i+1:]:
   if m=='q-95532':assert s.simplify(s.diff(a-b,g.X))!=0
   else:assert abs((a-b).evalf(60))>s.Float('1e-30')
 if m=='q-95532':assert sum(s.simplify(s.diff(v,g.X)-integrand)==0 for v in vals)==1
 assert q[':question/worked-solution'].split(' = ')[-1].strip().removesuffix('$$').strip()==f[':answer-field/choices'][ci][':answer/value']
 for text in (q[':question/problem'],q[':question/worked-solution']):assert text.count('$')%2==0 and text.count('{')==text.count('}')
 assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
 assert md['parameter_fingerprint']==g.fingerprint(q)
def fingerprint(q):return g.fingerprint(q)
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Complete bank through actual radio grader'} for a in f[':answer-field/choices']]
def main():
 source=json.loads((HERE/'source.json').read_text());cases=[];replays=[]
 for old in source['record'][':knowledge-point/questions']:
  m=old[':question/math-academy-id'];r=g.generate(g.LEVELS[m],template=m,parameters=g.DEFAULTS[m]);independent(r)
  assert r['question'][':question/problem']==old[':question/problem']
  oldv=sorted(a[':answer/value'] for a in old[':question/answer-fields'][0][':answer-field/choices']);newv=sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']);assert oldv==newv
  cases.append({'source':m,'matched_values':5,'total_values':5,'complete_bank':True,'prompt_exact':True,'source_correct_designation':'absent; inferred and calculus verified','source_solution':'absent; authored and verified','missing':[],'extra':[]});replays.append(r)
 records=[r for l in g.SUPPORTED_LEVELS for r in g.batch(l,100,1972)]
 for r in records:independent(r)
 assert len({fingerprint(r['question']) for r in records})==len(records)
 assert g.batch('easy',5,1)==g.batch('easy',5,1)
 for m in g.DEFAULTS:
  try:g.generate(g.LEVELS[m],template=m,parameters={'a':2,'b':0} if m=='q-95532' else {'n':2})
  except ValueError:pass
  else:raise AssertionError('Boundary rejection failed')
 save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(replays+records)])
 binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 report=json.loads((HERE/'engine-report.json').read_text());assert report['documented_unresolved_checks']==0
 save('source-cases.json',cases);save('review.json',{'replays':replays,'variants':records});(HERE/'review.md').write_text('\n\n---\n\n'.join(['## Source replay '+r['generation']['template']+'\n\n'+g.markdown(r) for r in replays]+['## '+l+' variants\n\n'+'\n\n---\n\n'.join(g.markdown(r) for r in records if r['question'][':question/difficulty'].endswith('/'+l)) for l in g.SUPPORTED_LEVELS]))
 save('validation.json',{'status':'pass','source_basis':source['basis'],'complete_source_banks':2,'matched_values':10,'total_values':10,'missing_options':[],'extra_options':[],'validated_distinct_domain':len(records),'fidelity':'Exact source prompts and all bank values. Source ratings, correct refs and solutions absent; generated values add verified authored facts, without modifying originals.','native_grading':{k:report[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',binary]}})
 print('Passed: complete source banks, all 38 variants, real grading, deterministic replay.')
if __name__=='__main__':main()
