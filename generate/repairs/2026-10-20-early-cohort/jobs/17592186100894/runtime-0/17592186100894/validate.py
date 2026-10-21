"""Read displayed ODEs/ICs/banks independently and exercise real learner grader."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('gen894',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
pm=g.pm;X,Y=g.X,g.Y
# Extend the fail-closed expression parser with a derivative placeholder.
_original_atom=pm.Parser.atom
D=s.Symbol('D',real=True)
def atom(self):
 if self.peek()=='D':self.pop();return D
 return _original_atom(self)
pm.Parser.atom=atom

def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,default=str)+'\n')
def close(a,b):
 d=s.simplify(a-b)
 return d==0 or (d.has(s.sin,s.cos,s.cot) and s.trigsimp(d.rewrite(s.sin))==0)

def displayed(r):
 q=r['question'];m=re.search(r'\$\$?(.*?)\$\$?',q[':question/problem'],re.S);assert m
 ode=m[1].strip().split(',')[0].rstrip('.,')
 ode=ode.replace(r'\frac{\text{d}y}{\text{d}x}','D').replace('{y}^{′}','D')
 ode=re.sub(r'\\operatorname\{(sin|cos)\}[\u2061]?x',lambda m:'\\'+m[1]+'(x)',ode)
 lhs,rhs=pm.relation(ode);assert lhs is not None
 residual=lhs-rhs;assert s.diff(residual,D,2)==0
 F=s.cancel(-residual.subs(D,0)/s.diff(residual,D));assert not F.has(D)
 match=re.search(r'y\(([^()]*)\)\s*=([^$\n]+)',q[':question/problem']);assert match
 x0=pm.expression(match[1]);y0=pm.expression(match[2].rstrip(' .'))
 return F,x0,y0

def check_record(r):
 mid=r['generation']['template'];h=r['generation']['parameters']['h'];assert mid in g.MODELS and h in g.SHIFTS
 q=r['question'];assert q[':question/difficulty']==':question.difficulty/'+g.level(mid)
 F,x0,y0=displayed(r);rhs,base_x,base_y,base_solution=g.MODELS[mid]
 assert close(F,rhs.subs(X,X-h)),(mid,'rendered ODE',F)
 assert close(x0,s.sympify(base_x)+h) and close(y0,s.sympify(base_y)),(mid,'rendered initial condition')
 solution=base_solution.subs(X,X-h)
 assert close(s.diff(solution,X),F.subs(Y,solution)),(mid,'ODE residual')
 assert close(solution.subs(X,x0),y0),(mid,'initial residual')
 assert s.simplify(s.diff(pm.relation(q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])[1],X)) is not s.nan
 f=q[':question/answer-fields'][0];kind=f[':answer-field/type'];values=[pm.relation(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(values)==(5 if kind.endswith('/radio') else 1)
 if kind.endswith('/radio'):
  # Compare complete equation residuals after substituting the unique local
  # solution. An option with a free integration constant is not particular.
  correct=[]
  for lhs,val in values:
   assert lhs is not None
   res=s.simplify((lhs-val).subs(Y,solution));correct.append(res==0)
  assert sum(correct)==1,(mid,'correct count',correct)
 else:correct=[close(values[0][1],g.expected_fragment(mid,h))];assert correct[0]
 for i,a in enumerate(f[':answer-field/choices']):assert (a[':answer/id']==f[':answer-field/correct'][1])==correct[i]
 for i,a in enumerate(values):
  for b in values[:i]:assert not pm.equivalent(a,b),(mid,'equivalent choices')
 expected_prompt,expected_sol=g.question_text(mid,h)
 assert q[':question/problem']==expected_prompt and q[':question/worked-solution']==expected_sol
 # Independently read final equation from the solution, avoiding dependence on
 # source correct IDs or generation's answer values.
 tail=q[':question/worked-solution'].split('$$')[-2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace(r'\,','').rstrip('. \n')
 tail=tail.split(r'\\')[-1].strip();tail=tail.replace('&','').replace('y(x)','y').strip()
 if tail.startswith('='):tail='y'+tail
 parts=tail.split('=');assert len(parts)>=2
 vals=[pm.expression(z) for z in parts]
 assert all(close((vals[0]-val).subs(Y,solution),0) for val in vals[1:]),(mid,'rendered final solution',tail)
 return {'source':mid,'h':h,'ode':str(F),'x0':str(x0),'y0':str(y0),'ode_and_initial_condition_verified':True,'final_solution_verified':True}

def native_checks(r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every field-owned option'} for a in f[':answer-field/choices'])
  else:
   v=f[':answer-field/choices'][0][':answer/value'];mid=r['generation']['template'];h=r['generation']['parameters']['h'];value=g.expected_fragment(mid,h)
   for text,expected in [(v,'accepted'),(g.tex(value),'accepted'),(v+'+0','accepted'),(g.tex(value+1),'rejected'),('0','rejected')]:
    checks.append({'field_index':i,'submitted':text,'expected':expected,'purpose':'canonical/equivalent blank or independently wrong entry'})
 return checks

def main():
 records=[];audits=[];fidelity=[];ledger=[];review=[]
 for mid in g.MODELS:
  print('Validating',mid,flush=True)
  replay=g.generate(g.level(mid),template=mid,replay=True);src=g.QS[mid];sf=src[':question/answer-fields'][0];gf=replay['question'][':question/answer-fields'][0]
  matched=0
  for a in sf[':answer-field/choices']:
   matches=[b for b in gf[':answer-field/choices'] if pm.equivalent(pm.relation(a[':answer/value']),pm.relation(b[':answer/value']))];assert len(matches)==1,(mid,a)
   assert (a[':answer/id']==sf[':answer-field/correct'][':answer/id'])==(matches[0][':answer/id']==gf[':answer-field/correct'][1]);matched+=1
   ledger.append({'source':mid,'source_field':sf[':answer-field/id'],'source_answer':a[':answer/id'],'observed_value':a[':answer/value'],'profile':replay['generation']['bank_profile'],'recipe':'('+a[':answer/value']+')[x := x-h]','interpretation':'empirical expression, original error intent unresolved','exact_replay':True})
  fidelity.append({'source':mid,'matched_options':matched,'total_options':len(sf[':answer-field/choices']),'matched_distractors':matched-1,'complete_bank':True,'missing':[],'extra':[],'prompt_and_solution_repairs':g.REPAIRS.get(mid)})
  for h in g.SHIFTS:
   r=g.generate(g.level(mid),template=mid,parameters={'h':h});audits.append(check_record(r));records.append(r)
   assert r==g.generate(g.level(mid),template=mid,parameters={'h':h})
   r2=g.generate(g.level(mid),seed=44,template=mid,parameters={'h':h});assert r['question']==r2['question']
  review.append({'source':mid,'original':src,'variant':g.generate(g.level(mid),template=mid,parameters={'h':2})})
 # A changed abscissa with the ODE held constant is a genuinely changed initial
 # value problem: it must fail the joint rendered-data validator.
 bad=copy.deepcopy(g.generate('easy',template='q-355546',parameters={'h':2}));bad['question'][':question/problem']=bad['question'][':question/problem'].replace('y(3)=6','y(4)=6')
 try:check_record(bad)
 except AssertionError:stale_caught=True
 else:raise AssertionError('stale IC was accepted')
 save(HERE/'source-fidelity.json',fidelity);save(HERE/'choice-ledger.json',ledger);save(HERE/'slot-coverage.json',audits);save(HERE/'review.json',review)
 (HERE/'review.md').write_text('\n\n---\n\n'.join('Source '+z['source']+'\n\n'+z['original'][':question/problem']+'\n\n'+z['original'][':question/worked-solution']+'\n\nVariant\n\n'+g.markdown(z['variant']) for z in review))
 save(HERE/'native-input.json',[{'label':str(i),'record':r,'checks':native_checks(r)} for i,r in enumerate(records) if r['generation']['eligible_for_learning']])
 subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 native=json.loads((HERE/'native-report.json').read_text());assert native['documented_unresolved_checks']==0
 result={'status':'passed','source_basis':g.SOURCE['basis'],'source_lineage':g.SOURCE['lineage'],'source_questions':len(g.QS),'supported_source_banks':len(fidelity),'complete_banks_matched':len(fidelity),'matched_options':sum(f['matched_options'] for f in fidelity),'total_options':sum(f['total_options'] for f in fidelity),'mathematical_cases':len(audits),'supported_levels':list(g.SUPPORTED),'unsupported_levels':{'hard':'No hard source practice or canonical hard template in this captured KP. Bounded classification supports no hard form without a new instructional backbone; 0 generated, shortage 5 remains explicit. New evidence reopens classification.'},'excluded_source_questions':g.EXCLUDED,'ungradable_source_families':g.UNGRADABLE,'served_source_profiles':len(g.MODELS)-len(g.UNGRADABLE),'repairs':g.REPAIRS,'h_domain':g.SHIFTS,'changed_initial_condition_stale_key_caught':stale_caught,'seed_does_not_create_content':True,'native':{k:v for k,v in native.items() if k!='records'}}
 save(HERE/'validation.json',result)
 save(HERE/'validation-freeze.json',{'status':'passed','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'parse_math.py',HERE/'validate.py',HERE/'source.json',HERE/'validation.json',HERE/'check-engine',HERE/'native-build.json',ROOT/'engine/rust/learning.rs',ROOT/'engine/rust/symbolic.rs',ROOT/'scripts/question_capture/math_format.py']}})
 print(json.dumps({k:v for k,v in result.items() if k not in ('repairs','unsupported_levels','excluded_source_questions')}))
if __name__=='__main__':main()
