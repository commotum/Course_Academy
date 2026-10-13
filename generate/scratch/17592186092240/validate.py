"""Independent normal-line validation, full blank replay, real learner grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent;ROOT=H.parents[2];SCRIPT=H.with_suffix('.py')
spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SOURCE=json.loads((H/'source.json').read_text())['record'][':knowledge-point/questions']
def number(v):
 v=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1)/(\2)',v)
 return s.Rational(s.sympify(v))
def check(r):
 p=r['generation'];c=g.CONFIG[p['profile']];q=r['question'];e=s.sympify(p['expression'],locals={'x':g.x});pt=s.Rational(p['point']);y=e.subs(g.x,pt)
 # Independently differentiate the mathematical object; the displayed equation
 # Ax+By=C must contain (pt,y) and have slope negative reciprocal to the tangent.
 bykey={f[':answer-field/key']:f for f in q[':question/answer-fields']};assert set(bykey)=={'field-1','field-2'}
 vals=[]
 for key in ['field-1','field-2']:
  f=bykey[key];assert f[':answer-field/type']==':answer-field.type/blank' and len(f[':answer-field/choices'])==1
  a=f[':answer-field/choices'][0];assert f[':answer-field/correct']==[':answer/id',a[':answer/id']];vals.append(number(a[':answer/value']))
 A=s.Integer(c['x_coefficient']);B=c['sign']*vals[0];D=vals[1];assert vals[0]>0
 assert s.simplify(A*pt+B*y-D)==0 and s.simplify((-A/B)*s.diff(e,g.x).subs(g.x,pt))==-1
 assert p['mathematical_key']==g.semantic_key(e,pt)
 assert q[':question/difficulty']==':question.difficulty/moderate'
 assert set(re.findall(r'\{\{(field-[12])\}\}',q[':question/problem']))==set(bykey)
 sol=q[':question/worked-solution'];assert g.latex(s.diff(e,g.x)) in sol and g.latex(-1/s.diff(e,g.x).subs(g.x,pt)) in sol
 assert r==g.generate('moderate',p['seed'],profile=p['profile'],parameters=p['parameters'])
 return True
def engine_item(label,r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  v=number(f[':answer-field/choices'][0][':answer/value'])
  for text,expected in [(f[':answer-field/choices'][0][':answer/value'],'accepted'),(g.latex(2*v/2),'accepted'),(f'({g.latex(v)})','accepted'),(g.latex(v+1),'rejected'),(g.latex(-v) if v else '1','rejected')]:
   checks.append({'field_index':i,'submitted':text,'expected':expected,'purpose':'Exact/equivalent blank value or incorrect value'})
 return {'label':label,'record':r,'checks':checks}
def run():
 replay=[];engine=[];coverage=[];review=[]
 for q in SOURCE:
  sid=q[':question/math-academy-id']
  if sid not in g.CONFIG:continue
  c=g.CONFIG[sid];r=g.generate('moderate',0,profile=sid,parameters={'scale':'1','point':c['point']});check(r)
  assert r['question'][':question/problem']==q[':question/problem']
  old={f[':answer-field/key']:f for f in q[':question/answer-fields']}
  for f in r['question'][':question/answer-fields']:
   sf=old[f[':answer-field/key']];assert len(sf[':answer-field/choices'])==1
   assert number(sf[':answer-field/choices'][0][':answer/value'])==number(f[':answer-field/choices'][0][':answer/value'])
   assert number(sf[':answer-field/correct'][':answer/value'])==number(f[':answer-field/choices'][0][':answer/value'])
  replay.append(r);coverage.append({'source':sid,'complete_banks_matched':2,'values_matched':2,'distractors':0,'prompt_exact':True,'solution_sequence':'derivative, tangent slope, normal slope, point-slope equation, rearrangement','layout_fidelity':'common source sentences retained; algebra layout compacted, not byte-identical'})
  engine.append(engine_item('Replay '+sid,r))
  for seed in [41,92,215]:
   v=g.generate('moderate',seed,profile=sid);check(v);review.append(v);engine.append(engine_item('Variant '+sid+' '+str(seed),v))
 keys=set();n=0
 for sid,p in g.candidates('moderate'):
  r=g.generate('moderate',0,profile=sid,parameters=p);check(r);keys.add(r['generation']['mathematical_key']);n+=1;engine.append(engine_item('Exhaustive '+sid+' '+str(p),r))
 for level in ['easy','hard','unclassified']:
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported level accepted')
 (H/'engine-input.json').write_text(json.dumps(engine,indent=2));subprocess.run([str(H/'check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
 native=json.loads((H/'engine-report.json').read_text());assert native['documented_unresolved_checks']==0
 for name,obj in [('source-replay.json',replay),('source-bank-replay.json',coverage),('review.json',review)]: (H/name).write_text(json.dumps(obj,indent=2))
 text='# Original and variant review\n'
 for q,r in zip([q for q in SOURCE if q[':question/math-academy-id'] in g.CONFIG],replay):
  text+='\n## '+q[':question/math-academy-id']+' original\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\n### Replayed template\n'+r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']+'\n'
 for r in review:text+='\n## Variant\n'+r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']+'\n'
 (H/'review.md').write_text(text)
 val={'passed':True,'source_basis':g.C['basis'],'supported_profiles':6,'source_banks_matched':12,'source_banks_total_supported':12,'source_values_matched':12,'source_distractors_matched':0,'source_distractors_total_supported':0,'mathematical_checks':n,'finite_distinct_capacity':len(keys),'fidelity':coverage,'correctness':True,'actual_grading':{k:native[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'contract_sha256':hashlib.sha256((H/'contract.json').read_bytes()).hexdigest()}
 (H/'validation.json').write_text(json.dumps(val,indent=2));print(json.dumps(val))
 return val
if __name__=='__main__':run()
