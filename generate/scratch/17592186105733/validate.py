#!/usr/bin/env python3
"""Fail-fast independent QA of actual printed stages, fidelity and native grading."""
import hashlib,importlib.util,itertools,json,re,subprocess,uuid,sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('triangle',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)
i,j,k=sp.symbols('i j k')
def group(s,at):
 assert s[at]=='{';depth=1;end=at+1
 while depth:depth+=(s[end]=='{')-(s[end]=='}');end+=1
 return s[at+1:end-1],end
def math(s):
 s=s.strip().rstrip('.')
 while r'\frac' in s:
  at=s.index(r'\frac');num,end=group(s,at+5);den,end=group(s,end)
  s=s[:at]+'('+str(math(num)/math(den))+')'+s[end:]
 while r'\sqrt' in s:
  at=s.index(r'\sqrt');rad,end=group(s,at+5)
  s=s[:at]+'('+str(sp.sqrt(math(rad)))+')'+s[end:]
 s=s.replace(r'\cdot','*').replace('^','**').replace('{','(').replace('}',')')
 s=re.sub(r'([ijk])',lambda m:{'i':'x','j':'y','k':'z'}[m[1]],s)
 s=re.sub(r'(?<=\d)([xyz])',r'*\1',s)
 return sp.simplify(parse_expr(s,local_dict={'x':i,'y':j,'z':k,'sqrt':sp.sqrt},transformations=TRANS))
def equal(a,b):assert sp.simplify(a-b)==(sp.zeros(*a.shape) if isinstance(a,sp.MatrixBase) else 0),(a,b)
def vec(s):
 if '⟨' in s:return sp.Matrix([math(x) for x in s.strip().rstrip('.').strip('⟨⟩').split(',')])
 expr=math(s);return sp.Matrix([expr.coeff(x) for x in (i,j,k)])
def balanced(s):
 depth=0
 for x in s:
  depth+=(x=='{')-(x=='}');assert depth>=0,s
 assert depth==0,s
 assert s.count('$')%2==0,s
 assert not re.search(r'(?<!\\)[+-]{2}',s),s

def inspect(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'};assert r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];balanced(prompt);balanced(sol)
 points=re.findall(r'([A-Z])\(([^()]*)\)',prompt);assert len(points)==3
 labels=''.join(x[0] for x in points);a,b,c=[sp.Matrix([math(v) for v in x[1].split(',')]) for x in points]
 u=b-a;v=c-a;w=u.cross(v);n=w.dot(w);area=sp.sqrt(n)/2;assert area>0
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==4
 # All 8 vector construction rows: symbolic difference, ordered position vectors,
 # basis-vector reduction and coordinate tuple, each independently verified.
 expressions=re.findall(r' & =(.*?)(?= \\\\ |\\end\{aligned\})',blocks[0]);assert len(expressions)==8
 for idx,(end,e) in enumerate(((b,u),(c,v))):
  off=idx*4;assert expressions[off]==labels[idx+1].lower()+'-'+labels[0].lower()
  position_expr=expressions[off+1];assert ')-' in position_expr
  left,right=position_expr.split(')-',1);equal(vec(left+')'),end);equal(vec(right),a)
  equal(vec(position_expr),e);equal(vec(expressions[off+2]),e);equal(vec(expressions[off+3]),e)
 parts=re.split(r' \\\\  & =',blocks[1]);assert len(parts)==5
 # Read each printed determinant's row components, never generation metadata.
 mats=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',parts[0],re.S);assert len(mats)==1
 rows=mats[0].split(' \\\\ ');assert rows[0]=='i & j & k'
 assert sp.Matrix([[math(z) for z in row.split(' & ')] for row in rows[1:]])==sp.Matrix([list(u),list(v)])
 minors=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',parts[1],re.S);assert len(minors)==3
 printed=[]
 for m in minors:printed.append(sp.Matrix([[math(z) for z in row.split(' & ')] for row in m.split(' \\\\ ')]))
 assert printed==[sp.Matrix([[u[1],u[2]],[v[1],v[2]]]),sp.Matrix([[u[0],u[2]],[v[0],v[2]]]),sp.Matrix([[u[0],u[1]],[v[0],v[1]]])]
 equal(sp.Matrix([printed[0].det(),-printed[1].det(),printed[2].det()]),w)
 equal(vec(parts[2]),w);equal(vec(parts[3]),w);equal(vec(parts[4].split(r'\end{aligned}')[0]),w)
 products=re.findall(r'(\(-?\d+\)|\d+)\\cdot (\(-?\d+\)|\d+)',parts[2]);assert len(products)==6
 intended=[(u[1],v[2]),(u[2],v[1]),(u[0],v[2]),(u[2],v[0]),(u[0],v[1]),(u[1],v[0])]
 for pair,wanted in zip(products,intended):assert tuple(map(math,pair)) in (wanted,wanted[::-1])
 norms=re.split(r' \\\\  & =',blocks[2]);assert len(norms)>=3
 squares=re.findall(r'(\(-?\d+\)|\{\d+\})\^\{2\}',norms[1]);assert len(squares)==3
 for x,y in zip(squares,w):equal(math(x)**2,y*y)
 for row in norms[1:]:equal(math(row.split(r'\end{aligned}')[0]),sp.sqrt(n))
 chain=blocks[3].rstrip('.').split('=');assert chain[1]==r'\frac{1}{2}A'
 for value in chain[2:]:equal(math(value),area)
 f=q[':question/answer-fields'][0];kind=f[':answer-field/type'].split('/')[-1]
 assert f[':answer-field/key']==('field-1' if kind=='blank' else 'selection')
 if kind=='blank':assert '{{field-1}}' in prompt
 bank=f[':answer-field/choices'];assert len(bank)==(1 if kind=='blank' else 5)
 actual=[math(x[':answer/value']) for x in bank];assert all(v>0 for v in actual)
 if not r['generation']['raw_bank_anomaly']:assert len(set(actual))==len(actual)
 correct=f[':answer-field/correct'][1];assert correct in [x[':answer/id'] for x in bank]
 for x,value in zip(bank,actual):balanced(x[':answer/value']);uuid.UUID(x[':answer/id']);assert (x[':answer/id']==correct)==(sp.simplify(value-area)==0)
 uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id'])
 return n

def checks(r,label):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  cases=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned radio ID'} for a in f[':answer-field/choices']]
 else:
  points=re.findall(r'([A-Z])\(([^()]*)\)',r['question'][':question/problem']);a,b,c=[sp.Matrix([math(z) for z in x[1].split(',')]) for x in points];w=(b-a).cross(c-a);n=w.dot(w);value=f[':answer-field/choices'][0][':answer/value']
  cases=[{'submitted':value,'expected':'accepted','purpose':'canonical exact fragment'}, {'submitted':f'sqrt({n})/2','expected':'accepted','purpose':'independent unreduced cross-norm'}, {'submitted':f'sqrt({4*n})/4','expected':'accepted','purpose':'equivalent changed radical/denominator'}, {'submitted':f'sqrt({n})','expected':'rejected','purpose':'parallelogram norm without half'}, {'submitted':'-1','expected':'rejected','purpose':'negative area'}]
 return {'label':label,'record':r,'checks':cases}

def write(name,obj):(D/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def main():
 lesson=json.loads((ROOT/'generate/runs/current/lessons/17592186049108.json').read_text())['record'][0];steps={x[':db/id']:x for x in lesson[':activity/steps']};at=lesson[':activity/first-step'][':db/id'];route=[]
 while at:
  step=steps[at];route.append(step[':step/content'][':db/id']);at=step.get(':step/next',{}).get(':db/id')
 assert route==[17592186107073,17592186105732,17592186105733,17592186105734]
 cases=[];ledger=[];reviews=[];native=[];matched=0;refs=0;solutions=0;distractors=0
 for sid,q in g.SOURCES.items():
  ft=g.TEMPLATES[sid][1];profile='blank' if ft=='blank' else ('raw/'+sid if sid=='q-127908' else 'observed/'+sid)
  case={'source_id':sid,'template':sid,'parameters':{'vertices':g.vertices(q)},'bank_profile':profile,'level':'moderate'};cases.append(case)
  r=g.generate('moderate',template=sid,parameters=case['parameters'],profile=profile);inspect(r)
  f=r['question'][':question/answer-fields'][0];old=q[':question/answer-fields'][0]
  assert r['question'][':question/problem']==q[':question/problem']
  original=sorted([math(a[':answer/value']) for a in old[':answer-field/choices']],key=str);new=sorted([math(a[':answer/value']) for a in f[':answer-field/choices']],key=str);assert original==new
  matched+=len(original);distractors+=len(original)-1
  if old.get(':answer-field/correct'):
   correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);equal(math(correct),math(old[':answer-field/correct'][':answer/value']));refs+=1
  if q.get(':question/worked-solution'):
   assert q[':question/worked-solution']==r['question'][':question/worked-solution'];solutions+=1
  ledger.append({'source_id':sid,'complete_bank':True,'values':len(original),'prompt_raw_exact':True,'solution_raw_exact':bool(q.get(':question/worked-solution')),'correct_designation_matched':bool(old.get(':answer-field/correct')),'duplicate_wrong_values':sid=='q-127908'})
  reviews.append({'label':'Original replay '+sid,'record':r});native.append(checks(r,'source/'+sid))
  for seed in (37,43):
   rr=g.generate('moderate',seed,template=sid,profile=profile);inspect(rr);reviews.append({'label':'Generated observed template/profile '+sid+'/'+str(seed),'record':rr});native.append(checks(rr,'changed/'+sid+'/'+str(seed)))
  if sid=='q-127908':
   repaired=g.generate('moderate',template=sid,parameters=case['parameters'],profile='observed/'+sid);inspect(repaired);reviews.append({'label':'Minimal duplicate-bank repair q-127908','record':repaired});native.append(checks(repaired,'repaired/q-127908'))
 write('source-cases.json',cases)
 diversity={lv:set() for lv in ('easy','moderate','hard')};sampled=0
 for template,(lv,ft) in g.TEMPLATES.items():
  if not template.startswith('authored_'):continue
  for seed in range(24):
   r=g.generate(lv,seed,template=template);inspect(r);sampled+=1;diversity[lv].add(r['generation']['parameter_fingerprint'])
   assert r==g.generate(lv,seed,template=template)
   replay=g.generate(lv,seed+100,template=template,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile']);assert r['question'][':question/id']==replay['question'][':question/id']
   native.append(checks(r,template+'/'+str(seed)))
   if seed<2:reviews.append({'label':'Authored '+lv+' '+ft+' peer '+str(seed),'record':r})
 for lv,seen in diversity.items():assert len(seen)>20,(lv,len(seen))
 # Explicit guards on reduced objects, signed/boundary coordinates and collisions.
 bad=[('easy',[[0,0,0],[3,1,0],[0,1,1]]),('easy',[[0,0,0],[1,1,1],[1,-1,1]]),('moderate',[[0,0,0],[6,1,1],[1,2,1]]),('hard',[[0,0,0],[2,3,1],[-1,1,2]]),('hard',[[0,0,0],[7,0,1],[2,-3,4]]),('hard',[[0,0,0],[7,7,7],[-7,7,-7]]),('moderate',[[0,0,0],[1,1,1],[2,2,2]]),('easy',[[0,0,0],[1,0,0],[0,1,0]])]
 for lv,pts in bad:
  try:g.generate(lv,parameters={'vertices':pts})
  except ValueError:pass
  else:raise AssertionError(('invalid explicit accepted',lv,pts))
 # Translation/permutation canonical fingerprint; identity follows displayed content.
 r=g.generate_moderate(seed=9,field_type='blank');pts=r['generation']['parameters']['vertices'];key=g.task_key({'vertices':pts})
 for perm in itertools.permutations(pts):
  translated=[[x+1 for x in v] for v in perm];assert g.task_key({'vertices':translated})==key
  rr=g.generate_moderate(field_type='blank',parameters={'vertices':translated});inspect(rr)
 # Bank aliases don't create new IDs. Shuffling exercises all correct positions.
 src=g.SOURCES['q-20026'];p={'vertices':g.vertices(src)}
 a=g.generate_moderate(template='q-20026',parameters=p,profile='raw/q-20026');b=g.generate_moderate(template='q-20026',parameters=p,profile='observed/q-20026');assert a['question'][':question/id']==b['question'][':question/id']
 p=g.generate_easy(seed=9)['generation']['parameters'];positions=set()
 for seed in range(30):
  rr=g.generate_easy(seed=seed,parameters=p);inspect(rr);f=rr['question'][':question/answer-fields'][0];positions.add(next(j for j,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
 assert positions==set(range(5))
 write('review.json',reviews)
 lines=['# Original and generated review','', 'All originals replay through the public parameterized API. q-20016 includes a separately authored missing solution and inferred key. Raw q-127908 retains its duplicate wrong alternatives; the repair is shown separately. Generated examples are labelled explicitly.','']
 for item in reviews:
  rr=item['record'];qq=rr['question'];ff=qq[':question/answer-fields'][0];lines += ['## '+item['label'],'', 'Template: `'+rr['generation']['template']+'`; profile: `'+rr['generation']['bank_profile']+'`.','',qq[':question/problem'],'']
  for answer in ff[':answer-field/choices']:lines.append('- $'+answer[':answer/value']+'$'+(' — correct' if answer[':answer/id']==ff[':answer-field/correct'][1] else ''))
  lines += ['',qq[':question/worked-solution'],'']
 (D/'review.md').write_text('\n'.join(lines)+'\n')
 write('engine-input.json',native)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 eng=json.loads((D/'engine-report.json').read_text())
 sha=lambda path:hashlib.sha256(Path(path).read_bytes()).hexdigest()
 report={'passed':True,'database_writes':0,'source_provenance':{k:g.CAPTURE[k] for k in ('database','basis','lineage')},'source_questions':19,'complete_banks_matched':19,'answer_values_matched':matched,'answer_values_total':matched,'distractors_matched':distractors,'correct_designations_matched':refs,'present_correct_designations_total':18,'missing_correct_designations_inferred':1,'raw_exact_prompts':19,'raw_exact_present_solutions':solutions,'present_solutions_total':18,'missing_solutions_authored':1,'unrated_moderate_assignment_authored':1,'raw_ambiguous_duplicate_banks':1,'minimal_normal_bank_repairs':1,'source_results':ledger,'route_content_ids':route,'finite_domain':json.loads((D/'semantic-domain.json').read_text()),'generated_default_records_checked':sampled,'distinct_sampled_mathematical_tasks':{lv:len(v) for lv,v in diversity.items()},'explicit_guard_rejections':len(bad),'printed_math_stages_independently_checked':True,'native_grading':{k:eng[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'freeze':{'generator_sha256':sha(D.with_suffix('.py')),'validator_sha256':sha(__file__),'source_sha256':sha(D/'source.json'),'widget_evidence_sha256':sha(D/'source-widget-evidence.json'),'extraction_sha256':sha(D/'extraction-data.json'),'domain_sha256':sha(D/'semantic-domain.json'),'engine_sha256':sha(ROOT/'generate/runs/current/check-engine'),'engine_source_sha256':sha(ROOT/'generate/runs/current/check-engine.rs')},'limitations':['Scalar source distractor intent underdetermined; observed homogeneous expression replay only.','Easy and hard workload assignments are authored, not source labels.','q-20016 has no captured solution/correct designation; inferred values not counted as matches.','q-127908 duplicate incorrect scalar choices retained only in raw evidence profile.']}
 write('validation.json',report)
 print(json.dumps({k:report[k] for k in ('passed','complete_banks_matched','answer_values_matched','raw_exact_present_solutions','native_grading')},indent=2))
if __name__=='__main__':main()
