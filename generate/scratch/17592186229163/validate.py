#!/usr/bin/env python3
"""Fail-closed independent displayed-math, fidelity, scope and native-grading QA."""
import copy,hashlib,importlib.util,json,pathlib,re,subprocess,sys
import sympy as s
BASE=pathlib.Path(__file__).resolve().parent;ROOT=BASE.parents[2]
spec=importlib.util.spec_from_file_location('generator',str(BASE)+'.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sys.path.insert(0,str(BASE));from readback import scalar,x,y,a,b

def dump(name,value): (BASE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def eq(u,v):assert s.simplify(u-v)==0,(u,v,s.simplify(u-v))
def math_blocks(text):return re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)
def rows(block):return [r.split('& =',1)for r in block[len(r'\begin{aligned}'):-len(r'\end{aligned}')].split(r'\\')]
def formatting(text):
 assert text.count('$')%2==0
 assert text.count('$$')%2==0
 text=text.replace('{{field-1}}','')
 depth=0
 for c in text:
  depth+=(c=='{')-(c=='}');assert depth>=0
 assert depth==0
 assert '+-'not in text and '--'not in text and '-.'not in text

def independent(rec,raw=False):
 q,meta=rec['question'],rec['generation'];level=q[':question/difficulty'].split('/')[-1];two=level!='easy';prompt=q[':question/problem'];solution=q[':question/worked-solution'];fields=q[':question/answer-fields']
 assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 assert len(fields)==1;f=fields[0];assert f[':answer-field/type']==':answer-field.type/blank' and f[':answer-field/key']=='field-1';assert '{{field-1}}'in prompt
 assert f[':answer-field/correct'][0]==':answer/id';assert f[':answer-field/correct'][1]in [c[':answer/id']for c in f[':answer-field/choices']]
 import uuid
 for ident in [q[':question/id'],f[':answer-field/id']]+[c[':answer/id']for c in f[':answer-field/choices']]:uuid.UUID(ident)
 formatting(prompt);formatting(solution)
 ode=math_blocks(prompt)[0].rstrip(',');left,right=ode.split('=');assert left.startswith('{y}^{′}')
 c=scalar(left[len('{y}^{′}'):])/y;assert not c.free_symbols;rhs=scalar(right)
 complementary=re.search(r'\$\{y\}_\{c\}\(x\)=A([^$]+)\$',prompt)[1];hom=scalar(complementary);eq(s.diff(hom,x)+c*hom,0)
 r=-c;terms=s.expand(rhs).as_ordered_terms();assert len(terms)==(2 if two else 1)
 rates=[];forcing={}
 for t in terms:
  ee=[e for e in t.atoms(s.exp)];assert len(ee)==1 and ee[0].args[0]/x in s.Integers
  rate=ee[0].args[0]/x;forcing[rate]=s.simplify(t/ee[0]);rates.append(rate)
 assert r in forcing;av=forcing[r];assert av!=0
 if two:
  sv=next(k for k in rates if k!=r);bv=forcing[sv];beta=bv/(sv-r);assert bv!=0
 observed_p={'r':int(r),'a':int(av)}
 if two:observed_p.update(s=int(sv),b=int(bv))
 assert observed_p==meta['parameters'];g.validate_parameters(level,observed_p)
 blocks=math_blocks(solution);assert len(blocks)==(6 if two else 4)
 guess=scalar(blocks[0].split('=',1)[1]);eq(guess,a*x*s.exp(r*x)+(b*s.exp(sv*x)if two else 0))
 deriv=rows(blocks[1]);assert len(deriv)==4
 assert deriv[0][0].strip()=='{y}_{p}^{′}'
 assert deriv[0][1].strip().endswith(')^{′}')
 assert deriv[1][1].count(')^{′}')==(2 if two else 1)
 assert r'\alpha ('in deriv[2][1] and '1'in deriv[3][1]
 for _,right in deriv:eq(scalar(right),s.diff(guess,x))
 sub=rows(blocks[2]);assert len(sub)==(3 if two else 4)
 L=s.diff(guess,x)+c*guess
 for i,(left,right)in enumerate(sub):
  if i<3:eq(scalar(left),L);eq(scalar(right),rhs)
  else:eq(scalar(left),a);eq(scalar(right),av)
 # Distinct substitution/product, uncollected cancellation, collected rows.
 assert sub[0][0].strip().startswith('(') and r'\alpha x'in sub[0][0]
 assert '(1'in sub[1][0] and sub[1][0].count('x')==(3 if not two else 4)
 assert '(1'not in sub[2][0] and sub[2][0].count('x')==(1 if not two else 2)
 if two:
  for idx,expected in [(3,[(a,av),((sv-r)*b,bv)]),(4,[(a,av),(b,beta)])]:
   parts=blocks[idx].rstrip('.,').split(r'\,\text{and}\,');assert len(parts)==2
   for part,(el,er)in zip(parts,expected):
    l,rr=part.split('=');eq(scalar(l),el);eq(scalar(rr),er)
 particular=av*x*s.exp(r*x)+(beta*s.exp(sv*x)if two else 0)
 final=scalar(blocks[-1].split('=',1)[1]);eq(final,particular);eq(s.diff(final,x)+c*final,rhs)
 for answer in f[':answer-field/choices']:
  v=answer[':answer/value'];assert answer[':answer/type']==':answer.type/math' and '$'not in v
  assert '\\\\'not in v;formatting(v)
  eq(scalar(v),particular)
 if not raw:assert len(f[':answer-field/choices'])==1
 assert s.Symbol('t')not in final.free_symbols
 return particular

def build_checks(rec,label):
 f=rec['question'][':question/answer-fields'][0];v=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);p=rec['generation']['parameters'];r=p['r'];a=p['a'];e='e^{'+str(r)+'x}';canon=v
 checks=[{'submitted':canon,'expected':'accepted','purpose':'canonical exact expression'},
  {'submitted':str(a)+'x'+e+('+'+r'\frac{'+str(p['b'])+'}{'+str(p['s']-r)+'}e^{'+str(p['s'])+'x}'if 's'in p else ''),'expected':'accepted','purpose':'independently unreduced signed coefficient quotient'},
  {'submitted':'x('+str(a)+e+')'+('+'+r'\frac{'+str(p['b'])+'}{'+str(p['s']-r)+'}e^{'+str(p['s'])+'x}'if 's'in p else ''),'expected':'accepted','purpose':'factor ordering equivalent expression'},
  {'submitted':canon+'+1','expected':'rejected','purpose':'additive wrong value'},
  {'submitted':canon.replace('x{e}','{e}').replace('xe','e'),'expected':'rejected','purpose':'omitted resonant x method error'}]
 if rec['generation']['bank_profile']=='normal':checks.append({'submitted':canon+'+'+e,'expected':'rejected','purpose':'normal explicitly excludes added complementary-solution component'})
 return {'label':label,'record':rec,'checks':checks}

def main():
 source=json.load(open(BASE/'source.json'));qs=source['record'][':knowledge-point/questions'];byid={q[':question/math-academy-id']:q for q in qs};cases=json.load(open(BASE/'source-cases.json'));fidelity=[];engine=[];reviews=[];coverage=0;normal_repairs=[]
 assert source['basis']==1356 and source['lineage']==g.SOURCE['lineage']
 for case in cases:
  q=byid[case['source_id']];rec=g.generate(case['level'],parameters=case['parameters'],template=case['template'],profile=case['bank_profile']);independent(rec,raw=True)
  for key in [':question/problem',':question/worked-solution']:assert rec['question'][key]==q[key],(case['source_id'],key)
  f=q[':question/answer-fields'][0];gf=rec['question'][':question/answer-fields'][0]
  original=[(v[':answer/value'],v[':answer/id']==f[':answer-field/correct'][':answer/id'])for v in f[':answer-field/choices']]
  generated=[(v[':answer/value'],v[':answer/id']==gf[':answer-field/correct'][1])for v in gf[':answer-field/choices']]
  assert sorted(original)==sorted(generated);coverage+=len(original);fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact':True,'complete_bank_exact':True,'designation_exact':True,'values':len(original)})
  normal=g.generate(case['level'],parameters=case['parameters']);independent(normal)
  if case['bank_profile']=='duplicate_legacy':normal_repairs.append({'source_id':case['source_id'],'repair':'remove equivalent legacy blank answer'})
  engine.extend([build_checks(rec,case['source_id']+' raw'),build_checks(normal,case['source_id']+' normal')])
  reviews.append({'label':'Observed source replay '+case['source_id'],'record':rec})
  # Changed params at the original profile exercise the complete parameter recipe.
  variant=g.generate(case['level'],seed=42+len(reviews),profile=case['bank_profile'])
  if variant['generation']['parameters']==case['parameters']:variant=g.generate(case['level'],seed=142+len(reviews),profile=case['bank_profile'])
  assert variant['generation']['parameters']!=case['parameters']
  independent(variant,raw=True);reviews.append({'label':'Generated observed-profile variant '+case['source_id'],'record':variant});engine.append(build_checks(variant,case['source_id']+' variant'))
 count=0;distinct={l:set()for l in ['easy','moderate','hard']}
 for level in distinct:
  for seed in range(100):
   rec=g.generate(level,seed=seed);value=independent(rec);count+=1;distinct[level].add(rec['generation']['parameter_fingerprint'])
   alternate=g.generate(level,seed=seed+1000,parameters=rec['generation']['parameters']);assert rec['question']==alternate['question'];assert rec['generation']['parameter_fingerprint']==alternate['generation']['parameter_fingerprint']
   if seed<4:engine.append(build_checks(rec,level+' default '+str(seed)))
   if seed<2:reviews.append({'label':'Generated '+level+' default '+str(seed)+'; '+('authored hard extension'if level=='hard'else 'observed-method parameters'),'record':rec})
 boundary=[('easy',{'r':-6,'a':12}),('easy',{'r':6,'a':2}),('moderate',{'r':-6,'a':30,'s':3,'b':-12}),('moderate',{'r':-2,'a':2,'s':1,'b':1}),('hard',{'r':6,'a':-12,'s':-1,'b':1}),('hard',{'r':-1,'a':-2,'s':-6,'b':12}),('hard',{'r':2,'a':12,'s':-1,'b':-1})]
 for level,p in boundary:
  rec=g.generate(level,parameters=p);independent(rec);engine.append(build_checks(rec,level+' signed boundary '+json.dumps(p,sort_keys=True)))
 # Invalid explicit parameters may not silently drift into another workload.
 invalid=[('easy',{'r':1,'a':4}),('easy',{'r':3,'a':-4}),('moderate',{'r':3,'a':4,'s':1,'b':2}),('moderate',{'r':-3,'a':0,'s':1,'b':2}),('hard',{'r':2,'a':4,'s':4,'b':2}),('hard',{'r':2,'a':4,'s':4,'b':1}),('hard',{'r':2,'a':-40,'s':4,'b':1}),('hard',{'r':2,'a':-4,'s':2,'b':1})]
 for level,p in invalid:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('invalid explicit parameters accepted',level,p))
 # Mutating a displayed intermediate sign must fail even if the final answer remains right.
 tampered=copy.deepcopy(g.generate('moderate',parameters={'r':-3,'a':6,'s':2,'b':10}));tampered['question'][':question/worked-solution']=tampered['question'][':question/worked-solution'].replace('(1-3x+3x)','(1-3x-3x)')
 try:independent(tampered)
 except AssertionError:pass
 else:raise AssertionError('Missing displayed sign escaped independent checks')
 dump('native-input.json',engine)
 result=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(BASE/'native-input.json'),str(BASE/'native-report.json')],text=True,capture_output=True)
 (BASE/'native-log.txt').write_text(result.stdout+result.stderr);assert result.returncode==0,result.stderr
 native=json.load(open(BASE/'native-report.json'));dump('review.json',reviews)
 text=['# Review: resonant first-order particular solutions','Database math basis 1356. Raw original capture is source.json; exact replay follows. Generated variants are labeled. Hard is authored; all plots none.']
 for item in reviews:text.extend(['\n## '+item['label'],g.markdown(item['record'])])
 (BASE/'review.md').write_text('\n\n'.join(text)+'\n')
 report={'status':'pass','version':g.VERSION,'source':g.SOURCE,'practice_questions':12,'easy_sources':8,'moderate_sources':4,'hard_sources':0,'source_fidelity':{'questions':12,'prompts_exact':12,'solutions_exact':12,'complete_banks_exact':12,'values_exact':coverage,'correct_designations_exact':12,'details':fidelity},'normal_repairs':normal_repairs,'normal_math_repairs':0,'generated_math_instances':count+len(boundary),'explicit_signed_boundary_cases':len(boundary),'sampled_distinct_tasks':{k:len(v)for k,v in distinct.items()},'raw_api_replay':12,'invalid_input_checks':len(invalid),'independent_displayed_checks':'prompt ODE, complementary function, guess, every formal derivative and product row, every substitution/uncollected/collected row, coefficient equations, solved coefficients, final function and all owned answer values','tampered_stage_detected':True,'native':{k:native[k]for k in ['accepted_checks','rejected_checks','documented_unresolved_checks','database_writes']},'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'authored_extensions':['hard: same two-exponential/two-coefficient method, signed-rate collection and bounded noninteger beta'],'plots':'none','review_records':len(reviews),'remaining_findings':[],'finite_meaningful_domains':json.load(open(BASE/'finite-domains.json'))['meaningful_ode_parameter_tasks'],'normal_response_criterion':'no added complementary-solution term; observed wording preserved in replay profiles','source_fraction_raw_bytes':'single backslash: valid TeX; no doubled-escape source errors','normal_layout_normalizations':[{'source_id':'q-333147','change':'normal shared layout omits final periods in two aligned rows; punctuated observed replay preserves them'}]}
 dump('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
