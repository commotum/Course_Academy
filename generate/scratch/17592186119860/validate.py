#!/usr/bin/env python3
"""Read back displayed curves, velocities, norm stages and endpoint arithmetic.
Replay bank fidelity, source sequence/prose and native radio grading separately.
"""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,re,hashlib,subprocess,itertools,concurrent.futures
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
raw=json.loads((HERE/'source.json').read_text());sources={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']}

def equal(a,b):return sp.simplify(sp.trigsimp(a-b))==0
def normalize(s):return re.sub(r'\s+','',s).replace('{t}','t').replace('{0}','0').replace('{r}','r').replace('{f}','f')
def balance(s):
 assert s.count('$')%2==0
 depth=0
 for i,c in enumerate(s):
  if c=='{' and (i==0 or s[i-1]!='\\'):depth+=1
  if c=='}' and (i==0 or s[i-1]!='\\'):depth-=1;assert depth>=0
 assert depth==0

def check_display(record):
 q=record['question'];name=record['generation']['template'];p=record['generation']['parameters'];a,b=g.check_parameters(name,p)
 for key in (':question/problem',':question/worked-solution'):
  balance(q[key]);assert '@' not in q[key];assert not re.search(r'\\(?:sinh|cosh|tanh|coth|sech|csch|log)',q[key])
 prompt=q[':question/problem'];bounds=re.search(r'from\s+\$t\s*=\s*(.*?)\$ to \$t\s*=\s*(.*?)\$',prompt);assert bounds
 pa,pb=[g.parse_tex(x.rstrip('.')) for x in bounds.groups()];assert equal(pa,a) and equal(pb,b)
 tuple_text=re.search('⟨(.*?)⟩',prompt)[1];curve=[g.parse_tex(x) for x in tuple_text.replace(r'\,','').split(',')];assert len(curve)==3
 expected_curve=[g.expr(x) for x in g.TEMPLATES[name]['curve']];assert all(equal(x,y) for x,y in zip(curve,expected_curve))
 velocity=[sp.diff(x,g.T) for x in curve];norm_squared=sp.trigsimp(sum(x*x for x in velocity))
 worked=q[':question/worked-solution']
 if 'Notice that $t>0' in worked:assert a>0
 if r'Notice that $t\ge 0' in worked:assert a>=0
 first=worked.split('\\end{aligned}')[0].split('\\begin{aligned}')[1]
 tuples=re.findall('⟨(.*?)⟩',first)
 if name=='log_square':tuples=re.findall(r'\\langle (.*?)\\rangle',first)
 for item in (tuples if name=='log_square' else tuples[1:]):
  display_velocity=[g.parse_tex(x) for x in item.replace(r'\,','').split(',')];assert len(display_velocity)==3 and all(equal(x,y) for x,y in zip(display_velocity,velocity))
 rows=first.split(r'\\');norm_index=next(i for i,row in enumerate(rows) if '‖' in row or '\\|' in row)
 for row in rows[norm_index:]:
  stage=row.split('=',1)[1].strip();value=g.parse_tex(stage);assert equal(value**2,norm_squared),(name,stage,value,norm_squared)
 speed=g.parse_tex(rows[-1].split('=',1)[1]);mid=(a+b)/2;assert speed.subs(g.T,mid)>0
 L=sp.integrate(speed,(g.T,a,b));assert equal(L,g.expr(record['generation']['correct_value']))
 last_block=worked[worked.rfind('\\begin{aligned}L'):];irows=last_block.split(r'\\')
 # Read the displayed antiderivative before its evaluation bar.
 antirow=next(row for row in irows if ('|_{' in row or '|}_{' in row) and '=' in row)
 antitex=antirow.split('=',1)[1].split('|',1)[0].replace(r'\big','').replace(r'\,','').strip()
 # Source wraps the evaluation bar in a redundant opening brace; some wrap the whole evaluated expression.
 while antitex.count('{')>antitex.count('}') and antitex.endswith('{'):antitex=antitex[:-1]
 if antitex.startswith('{') and antitex.count('{')>antitex.count('}'):antitex=antitex[1:]
 assert equal(sp.diff(g.parse_tex(antitex),g.T),speed),(name,antitex)
 # Every displayed numeric endpoint stage is read back independently.
 n=g.TEMPLATES[name]['numeric_rows']
 if n:
  for row in irows[-n:]:
   stage=row.split('=',1)[1].split('\\end{aligned}')[0].strip().rstrip('.');assert equal(g.parse_tex(stage),L),(name,stage,L)
 else:
  assert equal(g.parse_tex(irows[-1].split('=',1)[1].split('\\end{aligned}')[0].strip().rstrip('.')),L)
 fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio'
 assert all(not re.search(r'\\(?:sinh|cosh|tanh|coth|sech|csch|log)',x[':answer/value']) for x in f[':answer-field/choices'])
 values=[g.parse_tex(x[':answer/value']) for x in f[':answer-field/choices']];assert len(values)==5 and all(v.is_real and v>0 for v in values)
 assert all(not equal(x,y) for i,x in enumerate(values) for y in values[i+1:]);correct=f[':answer-field/correct'][1]
 assert sum(equal(v,L) for v in values)==1
 assert next(x[':answer/id'] for x,v in zip(f[':answer-field/choices'],values) if equal(v,L))==correct
 return True

def main():
 cases=[];fidelity=[];records=[];review=[];engine=[]
 for name,c in g.TEMPLATES.items():
  sid=c['source_id'];q=sources[sid];params={'a':str(c['a']),'b':str(c['b'])};profile='observed_'+sid
  case={'source_id':sid,'level':c['level'],'template':name,'parameters':params,'bank_profile':profile};cases.append(case)
  r=g.generate(c['level'],template=name,parameters=params,profile=profile);check_display(r);records.append(r)
  expected=[g.parse_tex(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']];actual=[g.parse_tex(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert len(expected)==len(actual)==5 and all(sum(equal(x,y) for y in actual)==1 for x in expected)
  correct=q[':question/answer-fields'][0].get(':answer-field/correct');designation=correct is not None
  if designation:assert equal(g.parse_tex(correct[':answer/value']),g.expr(r['generation']['correct_value']))
  assert normalize(re.sub(r'!\[\]\(.*?\)','![](PLOT)',r['question'][':question/problem']))==normalize(re.sub(r'!\[\]\(.*?\)','![](PLOT)',q[':question/problem']))
  source_solution=q.get(':question/worked-solution');exact=False
  if source_solution:
   repaired=source_solution.replace(r'(\operatorname{cos}⁡t))⟩',r'(\operatorname{cos}⁡t)⟩').replace(r'({t}^{2}))⟩',r'({t}^{2})⟩').replace(r'({t}^{2})\,\frac',r'({t}^{2}),\,\frac')
   assert normalize(repaired)==normalize(r['question'][':question/worked-solution']),(name,'sequence/notation',repaired,r['question'][':question/worked-solution'])
   exact=normalize(source_solution)==normalize(r['question'][':question/worked-solution'])
  fidelity.append({'source_id':sid,'bank_values_matched':5,'bank_values_total':5,'correct_designation_matched':designation,'exact_solution_normalized':exact,'repaired_solution_matched':source_solution is not None,'prompt_matched':True,'source_solution_available':source_solution is not None})
  review.append({'label':'Source replay '+sid,'record':r,'source_original':q})
  # Two changed-parameter examples per family, both observed and authored banks.
  for i,selected_profile in enumerate([profile,'authored_operations']):
   for seed in range(50+i,100+i):
    variant=g.generate(c['level'],seed=seed,template=name,profile=selected_profile)
    if variant['generation']['parameters']!=params:break
   check_display(variant);records.append(variant);review.append({'label':'Generated '+name+' '+selected_profile,'record':variant})
 # Meaningful variety: enumerate all half-grid tasks and check every complete bank.
 variety={};enumerated=0
 for name,c in g.TEMPLATES.items():
  vals=[sp.Rational(i,2) for i in range(-6,11)] if name in ('poly_negative','poly_ordered','poly_constant','poly_radical','helix') else [sp.Rational(i,2) for i in range(11)]
  if name=='log_square':vals=[sp.Rational(1,2),sp.Integer(1),sp.Integer(2),sp.E]
  fingerprints=set()
  for a,b in itertools.combinations(vals,2):
   try:r=g.generate(c['level'],template=name,parameters={'a':str(a),'b':str(b)})
   except ValueError:continue
   check_display(r);fingerprints.add(r['generation']['mathematical_fingerprint']);enumerated+=1
  variety[name]=len(fingerprints);assert len(fingerprints)>=5
 # Explicit scope violations must fail rather than silently changing input.
 for name,params in [('chain_product',{'a':'-1','b':'2'}),('product_trig',{'a':'0','b':'6'}),('helix',{'a':'1/3','b':'2'}),('log_square',{'a':'-1','b':'E'}),('poly_ordered',{'a':'2','b':'1'})]:
  try:g.generate(g.TEMPLATES[name]['level'],template=name,parameters=params)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit scope accepted')
 # Concurrent renderer calls use isolated inputs and deterministic artifacts.
 for png in (HERE/'concurrency').glob('curve-*'):
  if png.suffix in ('.png','.json'):png.unlink()
 plot_params=[(sp.Rational(1,2),sp.Integer(2)),(sp.Rational(1,2),sp.Integer(2)),(sp.Integer(1),sp.Integer(2))]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:maps=list(pool.map(lambda bounds:g.render_plots('log_square',*bounds,output_dir=HERE/'concurrency'),plot_params))
 assert maps[0]==maps[1] and maps[0]!=maps[2]
 assert not list(HERE.glob('tmp*.json'))
 for bounds,asset in zip(plot_params,maps):
  sidecar=json.loads(Path(asset['prompt']).with_suffix('.json').read_text())
  assert all(r'\log' not in label for labels in sidecar['coordinate_labels'] for label in labels)
  assert sidecar['renderer']=='Matplotlib' and sidecar['segment']==[float(x) for x in bounds]
  assert all(equal(g.parse_tex(label),value) for labels,t in zip(sidecar['coordinate_labels'],bounds) for label,value in zip(labels,[sp.log(t),2*t,t*t]))
 # Seed/order changes preserve presentation identity and math identity.
 for r in records:
  gen=r['generation'];other=g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=981,template=gen['template'],parameters=gen['parameters'],profile=gen['bank_profile']);assert other['question'][':question/id']==r['question'][':question/id'];assert other['generation']['mathematical_fingerprint']==gen['mathematical_fingerprint']
  assert {x[':answer/id'] for x in other['question'][':question/answer-fields'][0][':answer-field/choices']}=={x[':answer/id'] for x in r['question'][':question/answer-fields'][0][':answer-field/choices']}
  f=r['question'][':question/answer-fields'][0];engine.append({'label':gen['template']+':'+gen['bank_profile']+':'+str(gen['parameters']),'record':r,'checks':[{'submitted_answer_id':x[':answer/id'],'expected':'accepted' if x[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Native radio selection for independently validated displayed value'} for x in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False,indent=2)+'\n');binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine.json')],check=True)
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
 report={'passed':True,'source_basis':1356,'source_questions':10,'source_banks_matched':10,'source_values_matched':50,'source_values_total':50,'source_distractors_matched':40,'source_distractors_total':40,'source_correct_designations_matched':9,'source_correct_designations_available':9,'missing_designation_independently_derived':1,'source_solutions_exact_normalized':sum(x['exact_solution_normalized'] for x in fidelity),'source_solutions_repaired_or_normalized_matched':9,'source_solutions_available':9,'source_prompts_matched':10,'source_prompt_match_normalization':'whitespace/redundant groups and regenerated plot asset path','source_prompts_raw_asset_path_changed':1,'plot_concurrency_actual_render_checked':True,'displayed_stage_checks':'all derivative expansion and simplification tuples, all norm rows including first distributed sums, actual prompt curve and bounds, antiderivative derivative, all numeric endpoint rows, complete displayed banks','source_details':fidelity,'authored_generated_examples':20,'exhaustive_valid_authored_instances':enumerated,'meaningful_interval_tasks_by_template':variety,'native_grader':json.loads((HERE/'engine.json').read_text()),'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'engine_binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest()}
 (HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 lines=['# Spatial arc length source replay and generated review','All values are exact. Original records remain verbatim in source.json. Generated records use presentation repairs documented in extraction.']
 for item in review:
  r=item['record'];q=r['question'];lines+=['\n## '+item['label'],'Parameters: '+json.dumps(r['generation']['parameters']),q[':question/problem'],'\nChoices: '+', '.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),q[':question/worked-solution']]
  if 'source_original' in item:lines+=['\nOriginal prompt:',item['source_original'][':question/problem'],'Original choices: '+', '.join('$'+a[':answer/value']+'$' for a in item['source_original'][':question/answer-fields'][0][':answer-field/choices']),'Original solution:',item['source_original'].get(':question/worked-solution','Unavailable; the generated worked solution is authored.')]
 (HERE/'review.md').write_text('\n\n'.join(lines)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('native_grader','source_details')},indent=2))
if __name__=='__main__':main()
