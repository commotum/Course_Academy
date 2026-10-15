"""Exhaustive finite-domain checks and actual learner grading; no database writes."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def independent(r):
 p=r['generation']['parameters'];a,b=p['a'],p['b'];q=r['question']
 # Read the rendered linear polynomial independently of generator differentiation.
 latex=q[':question/problem'].split('$f(x,y)=')[1].split('$')[0]
 # Every allowed integer polynomial is parsed by term coefficients, including unit coefficients.
 terms=re.findall(r'([+-]?\s*\d*)\s*([xy])',latex)
 assert len(terms)==2,(latex,terms)
 coeff={v:int(c.replace(' ','')+'1') if c.replace(' ','') in ('','+','-') else int(c.replace(' ','')) for c,v in terms}
 assert coeff=={'x':a,'y':b}
 assert s.diff(a*g.x+b*g.y,g.x)==a and s.diff(a*g.x+b*g.y,g.y)==b
 expected=[[(a*px,a) for px,py in g.POINTS],[(a,b)]*3,[(a,0)]*3,[(a*px,b) for px,py in g.POINTS],[(0,b)]*3]
 assert r['generation']['vectors']==expected
 assert len({tuple(v) for v in expected})==5
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 assert len(f[':answer-field/choices'])==5 and f[':answer-field/key']=='selection'
 assert f[':answer-field/correct']==[':answer/id',f[':answer-field/choices'][1][':answer/id']]
 for i,ans in enumerate(f[':answer-field/choices']):
  path=ROOT/ans[':answer/value'];d=json.loads(path.with_suffix('.json').read_text())
  assert d['points']==[list(z) for z in g.POINTS] and d['vectors']==[list(z) for z in expected[i]]
  assert path.read_bytes().startswith(b'\x89PNG')
  for (px,py),(u,v) in zip(g.POINTS,expected[i]):assert -9<px+u<9 and -9<py+v<9
 sol=q[':question/worked-solution'];assert f'f_x(x,y)=\\frac{{\\partial}}{{\\partial x}}({s.latex(a*g.x+b*g.y)})={a}' in sol
 assert f'f_y(x,y)=\\frac{{\\partial}}{{\\partial y}}({s.latex(a*g.x+b*g.y)})={b}' in sol
 for px,py in g.POINTS:assert f'\\nabla f({px},{py})&=({a})\\,i+({b})\\,j' in sol
 assert f[':answer-field/choices'][1][':answer/value'] in sol
 assert q[':question/difficulty']==':question.difficulty/easy'
 for text in (sol,q[':question/problem']):assert text.count('$')%2==0 and text.count('{')==text.count('}')
 return r['generation']['mathematical_signature']
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete field-owned image bank'} for a in f[':answer-field/choices']]
def main():
 records=[]
 for a in g.COEFFICIENTS:
  for b in g.COEFFICIENTS:
   if a==b:continue
   r=g.generate(parameters={'a':a,'b':b});independent(r);assert r==g.generate(parameters={'a':a,'b':b});records.append(r)
 assert len({independent(r) for r in records})==30
 replay=g.generate(parameters={'a':-1,'b':2});sf=g.SOURCE[':question/answer-fields'][0]
 # Concrete source image endpoint measurements, visually read on its unit grid.
 source_vectors=[[(2,-1),(-2,-1),(-2,-1)],[(-1,2)]*3,[(-1,0)]*3,[(2,2),(-2,2),(-2,2)],[(0,2)]*3]
 assert replay['generation']['vectors']==source_vectors
 assert sf[':answer-field/correct'][':answer/id']==sf[':answer-field/choices'][1][':answer/id']
 mapping=[{'source_answer_id':ans[':answer/id'],'asset':ans[':answer/value'],'points':g.POINTS,'vectors_at_original_parameters':source_vectors[i],'recipe':['(a*x,a)','(a,b)','(a,0)','(a*x,b)','(0,b)'][i],'correct':i==1,'complete_mathematical_value_replay':True} for i,ans in enumerate(sf[':answer-field/choices'])]
 (HERE/'reference/source-bank-mapping.json').write_text(json.dumps(mapping,indent=2))
 # All captured fields are graded without changing duplicate source fields.
 fixtures=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]
 excluded=[];source_checks=0
 for q in g.KP[':knowledge-point/questions']:
  if len(q[':question/answer-fields'])!=1 or any(':answer-field/correct' not in f for f in q[':question/answer-fields']):excluded.append(q[':question/math-academy-id']);continue
  qq=copy.deepcopy(q)
  for f in qq[':question/answer-fields']:
   f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
   for ans in f[':answer-field/choices']:ans[':answer/type']=ans[':answer/type'][':db/ident']
  r={'question':qq,'knowledge_point':{'title':g.KP[':knowledge-point/title']},'generation':{'template':'source-image-bank'}}
  fixtures.append({'label':q[':question/math-academy-id'],'record':r,'checks':checks(r)});source_checks+=1
 (HERE/'reference/native-input.json').write_text(json.dumps(fixtures,indent=2))
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'reference/native-input.json'),str(HERE/'reference/native-report.json')],check=True)
 # Mutation checks establish the validator can catch stale keys and solution coefficients.
 for mutate in ('key','solution','plot'):
  r=copy.deepcopy(records[0])
  if mutate=='key':r['question'][':question/answer-fields'][0][':answer-field/correct'][1]=r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']
  elif mutate=='solution':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('f_x','g_x')
  else:r['generation']['vectors'][1][0]=(99,99)
  try:independent(r)
  except AssertionError:pass
  else:raise AssertionError('Mutation escaped: '+mutate)
 report={'status':'pass','generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'finite_domain':30,'distinct_tasks':30,'source_replay':{'supported_template':'linear','profile':'q-122699-observed','distractors_matched':4,'distractors_total':4,'complete_banks_matched':1,'complete_banks_total':1,'original_prompt_and_solution_layout':'same ordered instructional stages; typesetting normalized','plot_fidelity':'exact original anchor points and vector components; matplotlib grid expanded for full domain'},'source_grading_valid_banks':source_checks,'excluded_malformed_source':excluded,'coefficient_slot_coverage':{'a':list(g.COEFFICIENTS),'b':list(g.COEFFICIENTS)},'targets':'three fixed source points; this linear family does not select a variable target','changed_coefficients_fixed_points':True,'mutation_checks':['key','solution','plot'],'native_report':'reference/native-report.json','unsupported_levels':['moderate','hard'],'unvalidated_source_families':'captured, classified and excluded from generator support; no claim of bank fidelity for those families'}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':main()
