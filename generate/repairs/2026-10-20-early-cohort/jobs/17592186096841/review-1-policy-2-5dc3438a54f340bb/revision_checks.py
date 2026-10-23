from review import *
from collections import Counter
import copy

def function(r):
 return parse(re.search(r'f\(x\)\s*=\s*(.*?)\$',r['question'][':question/problem'])[1].rstrip('.,'))
def verify_solution(r):
 f=function(r);v=x; inner,n=f.args; sol=r['question'][':question/worked-solution']
 displayed_inner=parse(re.search(r'g=([^$]+)',sol)[1].strip())
 displayed_di=parse(re.search(r'\\frac\{\\text\{d\}g\}\{\\text\{d\}x\}=([^$]+)',sol)[1].strip().rstrip('.'))
 final=parse(sol.split('&=')[-1].split(r'\end')[0].rstrip('.'))
 return {'inner':s.expand(displayed_inner-inner)==0,'inner_derivative':s.expand(displayed_di-s.diff(inner,v))==0,'final':s.expand(final-s.diff(f,v))==0}

def main():
 pairs=[g.generate_moderate(99173,'quartic_radio',parameters=dict(a=3,b=1,n=5,second_power=k)) for k in [1,3]]
 assert s.expand(function(pairs[1])-(3*x**4+x**3)**5)==0
 assert s.expand(function(pairs[0])-(3*x**4+x)**5)==0
 assert pairs[0]['generation']['bank_design']==pairs[1]['generation']['bank_design']
 reordered=copy.deepcopy(pairs[1]);reordered['question'][':question/answer-fields'][0][':answer-field/choices'].reverse()
 pairs.append(reordered);save('counterfactual-records.json',pairs)
 samples=[g.generate_moderate(seed,'quartic_radio') for seed in range(617201,617225)]
 fresh=[g.generate(v[0],seed,template=name) for name,v in g.TEMPLATES.items() if name!='quartic_radio' for seed in range(617241,617244)]
 save('samples-independent.json',samples+fresh);save('samples-quartic.json',samples);save('samples-easy.json',[r for r in fresh if r['question'][':question/difficulty'].endswith('/easy')])
 batch=json.loads((E.parent/'samples.json').read_text());save('batch.json',batch)
 boundary=[]
 for k in [1,3]:
  for a,b,n in [(-12,12,2),(12,-12,6)]:
   for profile in ['authored_quartic','observed_48625']:
    boundary.append(g.generate_moderate(73219,'quartic_radio',parameters=dict(a=a,b=b,n=n,second_power=k),profile=profile))
 save('boundary-records.json',boundary)
 rejected=[]
 for k in [0,2,4,3.0,True]:
  try:g.generate_moderate(99173,'quartic_radio',parameters=dict(a=3,b=1,n=5,second_power=k)); ok=False
  except ValueError:ok=True
  rejected.append({'second_power':k,'rejected':ok})
 assert all(v['rejected'] for v in rejected)
 save('boundary-results.json',rejected)
 orig=json.loads((E.parent/'source/source.json').read_text());sq={q[':question/math-academy-id']:q for q in orig['material']['kp'][':knowledge-point/questions']}
 replay=[];sr=[]
 for sid,name,p,prof in list(g.SOURCE_CASES)+[('q-132770','quadratic_derivative',dict(a=1,b=3,n=2),None),('q-132994','quadratic_derivative',dict(a=1,b=1,n=3),None)]:
  r=g.generate(g.TEMPLATES[name][0],551,template=name,parameters=p,profile=prof);replay.append(r)
  original=sq[sid];of=original[':question/answer-fields'][0]
  before=[str(s.expand(parse(a[':answer/value']))) for a in of[':answer-field/choices']]
  if sid=='q-340690': before=[str(s.expand(parse(of[':answer-field/correct'][':answer/value'])))]
  after=[str(s.expand(parse(a[':answer/value']))) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  sr.append({'source_id':original[':question/id'],'source_ma':sid,'bank_equal':sorted(before)==sorted(after),'source_values':before,'generated_values':after,'note':'Incorrect extra blank alternative excluded' if sid=='q-340690' else ''})
 assert all(r['bank_equal'] for r in sr)
 sr.append({'source_id':'19bf8d06-cbcc-547b-b882-ac89cd39fd1a','canonical_function':str(function(pairs[1])),'function_matches':True,'solution_checks':verify_solution(pairs[1]),'note':'Canonical has no answer field; derivative now supported through quartic radio. Retained legacy explicit inputs default to degree one.'})
 save('source-replays.json',replay+[pairs[1]]);save('source-replay-results.json',sr)
 allrows=samples+fresh+batch+boundary+pairs+replay
 results=[check_record(r) for r in allrows]
 assert all(all(r[k] for k in ['key_correct','unique_correct','distinct']) for r in results)
 sols=[{'id':r['question'][':question/id'],**verify_solution(r)} for r in allrows if r['generation']['template']=='quartic_radio']
 assert all(all(r[k] for k in ['inner','inner_derivative','final']) for r in sols)
 save('math-results.json',results);save('solution-results.json',sols)
 native=[make_grading(r,'revision-'+str(i)) for i,r in enumerate(pairs+boundary+batch+replay)]
 # Radio identity is the actual contract. Every new option is checked against differentiation.
 # For irrelevant reorder, same UUID must still grade as accepted.
 native.append({'label':'irrelevant-reorder','record':pairs[2],'checks':[{'submitted_answer_id':correct(pairs[1]['question'])[':answer/id'],'expected':'accepted','purpose':'same mathematical answer after layout-only change'}]})
 save('grader-input.json',native)
 save('render-records.json',pairs+batch+[boundary[4]])
 save('coverage-results.json',{'quartic_degree_counts':dict(Counter(str(r['generation']['parameters']['second_power']) for r in samples)),'quartic_attempts':dict(Counter(r['generation']['sampling_attempts'] for r in samples)),'fresh_template_counts':dict(Counter(r['generation']['template'] for r in fresh)),'seeds':{'quartic':[617201,617224],'unchanged_regression':[617241,617243]},'canonical_seed':99173,'source_replays':len(sr),'math_records':len(results),'solution_checks':len(sols),'replay':all(r==g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],template=r['generation']['template']) for r in samples+fresh)})
 save('scope-results.json',{'change':'Second quartic term can be degree one or degree three; latter is canonical e-181. Same outer power, inner differentiation, multiplication, response type and moderate allocation. Easy generation unaffected.','unsupported_source_families':[],'source_gaps':read('source-analysis.json')['gaps']})
 save('runtime.json',{'python':platform.python_version(),'sympy':s.__version__,'mpmath':__import__('mpmath').__version__})
 print(json.dumps(read('coverage-results.json')))
 (E/'session-state.md').write_text('Source confirmed; targeted mathematical, solution, source-bank, boundary, and deterministic checks complete. Canonical degree change passes. Native grading, rendering, delivery, shortcut and package checks pending.\n')
if __name__=='__main__':main()
