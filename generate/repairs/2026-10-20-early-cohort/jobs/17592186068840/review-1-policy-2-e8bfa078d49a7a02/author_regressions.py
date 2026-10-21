#!/usr/bin/env python3
"""Executable retained findings, independent visible math, delivery and grading.
Only writes validation evidence. No package mutation or service/database access.
"""
import argparse,collections,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186068840/workspace');E=Path(__file__).resolve().parent/'author-rerun';E.mkdir(exist_ok=True);JOB=W.parent
REPO=next(p for p in W.parents if (p/'Cargo.toml').exists())
spec=importlib.util.spec_from_file_location('generator',W/'17592186068840.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from latex_reader import parse,equal,X,Y,C,K,s

def save(name,obj):(E/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def field(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=field(r);return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def cue(v):
 return '^{2}' in v and 'C +' in v and (v.startswith(r'y=\sqrt[3]{C +') or v.startswith(r'y=\ln{\left(C +') or (v.startswith(r'y=\left(C +') and v.endswith('^{3}')))
def shortcut(r):
 f=field(r);z=[a for a in f[':answer-field/choices'] if cue(a[':answer/value'])]
 return len(z)==1 and z[0][':answer/id']==f[':answer-field/correct'][1]
def presentation(t):
 t=t.replace(r'\left','').replace(r'\right','').replace('\u2061','').replace(r'\operatorname{ln}',r'\ln').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{tan}',r'\tan').replace(r'\operatorname{sec}',r'\sec').replace(r'\operatorname{arcsin}',r'\arcsin').replace(r'\operatorname{arctan}',r'\arctan')
 return re.sub(r'\s+','',t)
def source_params(n):
 if n=='temperature_blank':return {'rate':'0.03','ambient':25}
 if n in ('autonomous_tan','reciprocal_blank','context_log_blank'):return {'a':{'autonomous_tan':1,'reciprocal_blank':2,'context_log_blank':3}[n]}
 return {'h':0}
def replay():
 source=json.loads((JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
 by={q[':question/math-academy-id']:q for q in source};rows=[];checks=[]
 for n in g.NAMES:
  spec=g.TEMPLATES[n];q=by[spec['source'][':question/math-academy-id']]
  r=g.generate(spec['level'],3,n,parameters=source_params(n),profile='observed_'+n);f=field(r);f0=q[':question/answer-fields'][0]
  conditions={'prompt':presentation(r['question'][':question/problem'])==presentation(q[':question/problem']), 'solution':presentation(r['question'][':question/worked-solution'])==presentation(q[':question/worked-solution']), 'complete_bank':sorted(presentation(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(presentation(a[':answer/value']) for a in f0[':answer-field/choices']), 'key':presentation(correct(r))==presentation(f0[':answer-field/correct'][':answer/value']), 'field_type':f[':answer-field/type']==f0[':answer-field/type'][':db/ident'],'difficulty':r['question'][':question/difficulty']==q[':question/difficulty'][':db/ident']}
  checks.append({'source_id':q[':question/id'],'math_academy_id':q[':question/math-academy-id'],'template':n,'choice_count':len(f[':answer-field/choices']),'checks':conditions});rows.append(r)
 assert {q[':question/math-academy-id'] for q in source}=={g.TEMPLATES[n]['source'][':question/math-academy-id'] for n in g.NAMES}
 save('source-replay-records.json',rows);save('source-replay.json',{'cases':checks,'passed':all(all(q['checks'].values()) for q in checks)})
 failures=[q for q in checks if not all(q['checks'].values())];assert not failures,failures
 print('Source replay:',len(checks),'complete banks,',sum(c['choice_count'] for c in checks),'answers')
 return rows

def easy_grid():
 rows=[]
 for n in g.SIGNED_EASY:
  for i,a in enumerate([-2,-1,1,2,3]):
   p={'a':a}
   if n=='autonomous_tan':p['candidates']=[-2,-1,1,2,3]
   if n!='autonomous_tan':p['h']=0
   if n=='affine_root':p['b']=3
   rows.append(g.generate_easy(71101+i,n,parameters=p))
  if n!='autonomous_tan':
   for h,a in [(-8,-2),(8,3)]:
    p={'h':h,'a':a}
    if n=='affine_root':p['b']=-3
    rows.append(g.generate_easy(72000+h,n,parameters=p))
 # Retained positive bounds and a second mixed bank: every displayed candidate
 # can be correct while the entire visible option set is held constant.
 for candidates in [[1,2,3,4,5],[-2,1,3,4,5]]:
  for i,a in enumerate(candidates):
   rows.append(g.generate_easy(71500+i,'autonomous_tan',parameters={'a':a,'candidates':candidates}))
 return rows

def rhs_of(r):
 p=r['question'][':question/problem'];spans=re.findall(r'\$([^$]+)\$',p)
 eq=next(v for v in spans if '=' in v and ('′' in v or r'\frac' in v))
 return parse(eq.split('=',1)[1].rstrip('.'))
def solution_valid(v,rhs):
 if Y in v.free_symbols:return False
 if not ({C,K}&v.free_symbols):return False
 if isinstance(v,s.Pow) and v.exp==s.Rational(1,3):return equal(s.diff(v.base,X),3*Y**2*rhs)
 if isinstance(v,s.Pow) and v.exp==3:return equal(3*s.diff(v.base,X),rhs/s.Abs(Y)**s.Rational(2,3))
 if isinstance(v,s.Pow) and v.exp==s.Rational(1,2):return equal(s.diff(v.base,X),2*Y*rhs)
 return equal(s.diff(v,X),rhs.subs(Y,v))
def math_checks(rows):
 out=[]
 for r in rows:
  q=r['question'];f=field(r);rhs=rhs_of(r);answers=[]
  for a in f[':answer-field/choices']:
   v=parse(a[':answer/value'].split('=',1)[1]);truth=solution_valid(v,rhs);key=a[':answer/id']==f[':answer-field/correct'][1]
   answers.append({'value':a[':answer/value'],'is_solution':truth,'key':key});assert truth==key,(q[':question/problem'],a,truth)
  blocks=re.findall(r'\$\$\s*([\s\S]*?)\s*\$\$',q[':question/worked-solution']);last=blocks[-1].strip().rstrip('.')
  if r'\begin{aligned}' in last:
   last=last.split(r'\\')[-1].replace(r'\end{aligned}','').strip().replace(' & =','=')
  assert last.startswith('y='),(q[':question/id'],last)
  sol=parse(last[2:]);key=parse(correct(r).split('=',1)[1]);assert equal(sol,key),(sol,key)
  # Independently read the primitive row in the second aligned display.
  aligned=re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',q[':question/worked-solution'])
  prim=aligned[1].split(r'\\')[-1];left,right=prim.split(' & =');F,H=parse(left),parse(right)
  if F==Y**s.Rational(1,3):valid=equal(3*s.diff(H,X),rhs/s.Abs(Y)**s.Rational(2,3))
  else:valid=equal(s.diff(F,Y)*rhs,s.diff(H,X))
  assert valid,('primitive',F,H,rhs)
  out.append({'id':q[':question/id'],'template':r['generation']['template'],'rhs':str(rhs),'choices':answers,'primitive_derivative':True,'solution_matches_key':True,'both_root_signs':r['generation']['domain']=='root2'})
 save('math-results.json',{'method':'Parse visible ODE, each complete option, primitive row and final solution independently. Exact derivative equality; implicit squares/cubes establish both real branches on stated intervals. No use of generator data() or parameter metadata to determine correctness.','cases':out,'passed':True})
 print('Independent visible-math checks:',len(out),'records;',sum(len(o['choices']) for o in out),'choices')

def delivery(rows,name):
 inp=E/(name+'-input.json');save(inp.name,rows)
 command=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(inp),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty','easy','--output',str(E/name),'--asset-root',str(E/'assets'),'--math-root','/media/jake/SSD/EDB/math']
 result=subprocess.run(command,capture_output=True,text=True);save(name+'-execution.json',{'command':command,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr});assert result.returncode==0,result.stderr
 return json.loads((E/name/'accepted.json').read_text())

def probes(rows):
 result={}
 for n in g.SIGNED_EASY:
  part=[r for r in rows if r['generation']['template']==n]
  if not part:continue
  positions=collections.Counter(next(i for i,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==field(r)[':answer-field/correct'][1]) for r in part)
  # Same visible complete option set; each candidate must be correct for some ODE.
  groups=collections.defaultdict(list)
  for r in part:groups[tuple(sorted(a[':answer/value'] for a in field(r)[':answer-field/choices']))].append(r)
  group_results=[]
  for bank,rs in groups.items():
   keys=collections.Counter(correct(r) for r in rs)
   if len(rs)>=5:assert len(keys)==5,(n,keys)
   group_results.append({'bank':bank,'cases':len(rs),'distinct_correct_families':len(keys),'best_equation_blind_answer_successes':max(keys.values()),'baseline':1/5})
  assert max(positions.values())<len(part),(n,'fixed correct position')
  result[n]={'records':len(part),'old_cue_successes':sum(map(shortcut,part)),'positions':dict(positions),'visible_bank_groups':group_results}
 return result

def shortcut_checks():
 rows=easy_grid();save('easy-grid.json',rows)
 # Retain exact historical minimal parameters and all previously sampled easy cases.
 minimal=g.generate_easy(71101,'reciprocal_cube',parameters={'h':0});assert not shortcut(minimal)
 historical=json.loads((JOB/'review-0-policy-2-f6d92a4daf8eee94/independent-easy.json').read_text());replayed=[]
 for old in historical:
  m=old['generation'];r=g.generate_easy(m['seed'],m['template'],parameters=m['parameters'],profile=m['bank_profile']);replayed.append(r)
 for n in ['reciprocal_cube','negative_exp','cube_power']:
  part=[r for r in replayed if r['generation']['template']==n];assert part and not all(map(shortcut,part)),n
 save('retained-counterexamples-current.json',[minimal]+replayed)
 batch=[g.generate_easy(71101+i) for i in range(5)];save('batch.json',batch);assert not all(map(shortcut,batch))
 delivered=delivery(rows,'delivery-grid');delivered_batch=delivery(batch,'delivery-batch')
 # Coefficient-only counterfactuals preserve the bank but change equation/key/solution.
 pairs=[]
 for n in g.SIGNED_EASY:
  p={'a':-1};p2={'a':2}
  if n=='autonomous_tan':p['candidates']=p2['candidates']=[-2,-1,1,2,3]
  if n!='autonomous_tan':p['h']=p2['h']=0
  if n=='affine_root':p['b']=p2['b']=3
  a=g.generate_easy(119,n,parameters=p);b=g.generate_easy(119,n,parameters=p2)
  assert correct(a)!=correct(b)
  for key in [':question/problem',':question/worked-solution']:assert a['question'][key]!=b['question'][key]
  assert sorted(c[':answer/value'] for c in field(a)[':answer-field/choices'])==sorted(c[':answer/value'] for c in field(b)[':answer-field/choices'])
  other=g.generate_easy(120,n,parameters=p)
  assert correct(a)==correct(other) and a['question'][':question/problem']==other['question'][':question/problem'] and a['question'][':question/worked-solution']==other['question'][':question/worked-solution']
  pairs.extend([a,b,other])
 save('counterfactual-records.json',pairs)
 save('shortcut-results.json',{'raw':probes(rows),'delivered':probes(delivered),'retained_old_cases':{'count':len(replayed),'old_cue_successes':sum(map(shortcut,replayed))},'batch':{'count':len(batch),'old_cue_successes':sum(map(shortcut,batch))},'delivered_batch':{'count':len(delivered_batch),'old_cue_successes':sum(map(shortcut,delivered_batch))},'limitations':['Controlled banks test equation-independent signs, coefficients, ranks, inverse shape and constant placement. Does not rule out every possible strategy.','Live history, entity IDs and weights are not available; captured read-only inventory filters are tested. Native selector has no template/answer balancing; any positively weighted fresh easy candidate is reachable.','Historical observed-bank replay intentionally retains source banks and is excluded from fresh sampling.'],'passed':True})
 math_checks(rows+pairs[:2]+batch)
 print('Shortcut regressions: fixed shape removed from retained cases and batch; signed roles survive delivery')
 return rows,pairs,batch

def grading(easy,source,pairs,batch):
 records=easy+pairs+batch+source;cases=[];blank_math=[]
 # Additional signed blank coefficients and irrelevant ambient changes.
 for n in ['reciprocal_blank','context_log_blank']:
  for a in [-2,3]:records.append(g.generate_moderate(120,n,parameters={'a':a}))
 for b in [25,35]:records.append(g.generate_moderate(121,'temperature_blank',parameters={'rate':'0.03','ambient':b}))
 for n in ['linear_sin','linear_sec2','linear_cos','linear_power','linear_arcsin','linear_sectan','canonical_root','intro_log']:
  records.append(g.generate(g.TEMPLATES[n]['level'],31,n))
 for i,r in enumerate(records):
  f=field(r);checks=[];n=r['generation']['template']
  if f[':answer-field/type'].endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete bank choice'} for a in f[':answer-field/choices']]
  else:
   value=correct(r);v=parse(value)
   if n=='temperature_blank':
    rate=r['generation']['parameters']['rate'];rv=s.Rational(rate)
    checks=[{'submitted':z,'expected':out,'purpose':why} for z,out,why in [(value,'accepted','correct factor'),(r'\frac{1}{e^{'+rate+'t}}','accepted','retained reciprocal exponential'),('e^{-'+str(int(rv*100))+'t/100}','accepted','exact rational exponent'),('e^{'+rate+'t}','rejected','wrong sign'),('e^{-0.07t}','rejected','wrong rate')]]
    assert equal(s.diff(v,X),-rv*v)
   else:
    a=r['generation']['parameters']['a'];coefficient=-a if n=='reciprocal_blank' else a
    checks=[{'submitted':z,'expected':out,'purpose':why} for z,out,why in [(value,'accepted','correct fragment'),(str(2*coefficient)+'t/2','accepted','unreduced exact equivalent'),(str(-coefficient)+'t','rejected','wrong sign'),(str(coefficient+1)+'t','rejected','wrong coefficient')]]
    # Independently read the full ODE for normal records and construct its solution
    # from the displayed blank response, not from data(). Source contextual prompts
    # omit part 1, so their ODE is supplied by the captured worked solution.
    full=1/(v+K) if n=='reciprocal_blank' else s.log(v+C)
    assert equal(s.diff(full,X), a*full**2 if n=='reciprocal_blank' else a*s.exp(-full))
   # Independently read the displayed ODE; contextual source replays supply it
   # in the first worked-solution row because part 1 is absent from the capture.
   if not r['generation']['bank_profile'].startswith('observed_'):
    visible_rhs=rhs_of(r)
   else:
    body=re.search(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',r['question'][':question/worked-solution'])[1]
    visible_rhs=parse(body.split(r'\\')[0].split(' & =')[1])
   visible_rhs=visible_rhs.xreplace({z:Y for z in visible_rhs.free_symbols if z.name in ('s','p','T')})
   if n=='temperature_blank':
    prompt=r['question'][':question/problem']
    ambient=int(re.search(r'T=([0-9]+)',prompt)[1]) if not r['generation']['bank_profile'].startswith('observed_') else 25
    full=ambient+K*v
   # The s/p full expression above was reconstructed from the visible fragment.
   assert equal(s.diff(full,X),visible_rhs.subs(Y,full)),('visible blank ODE',value,full,visible_rhs)
   blank_math.append({'id':r['question'][':question/id'],'template':n,'value':value,'visible_rhs':str(visible_rhs),'derivative_checked':True})
  cases.append({'label':str(i)+' '+n,'record':r,'checks':checks})
 # Reuse the original exact failure input unchanged against the rebuilt grader.
 cases+=json.loads((E/'baseline-grader-reciprocal-input.json').read_text())
 save('grader-input.json',cases);save('blank-math.json',{'cases':blank_math,'passed':True})
 command=[str(REPO/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grader-results.json')]
 p=subprocess.run(command,capture_output=True,text=True);save('grader-execution.json',{'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,p.stderr
 print(p.stdout.strip())
 render_blanks=[next(r for r in reversed(records) if r['generation']['template']==n and not r['generation']['bank_profile'].startswith('observed_')) for n in ['reciprocal_blank','context_log_blank','temperature_blank']]
 save('render-records.json',[easy[0],easy[5],easy[12],easy[19],easy[26]]+render_blanks)

def inventory():
 # Original snapshot is an evidence-only frozen implementation; never a runtime file.
 spec=importlib.util.spec_from_file_location('original',E/'original-generator.py');oldg=importlib.util.module_from_spec(spec);spec.loader.exec_module(oldg)
 original=json.loads((E/'baseline-generated-records.json').read_text());inv=json.loads((JOB/'source/inventory.json').read_text());by={q[':question/id']:q for q in inv['questions']};reproduced=[];affected=[];tests=[]
 for old in original:
  m=old['generation'];r=oldg.generate(old['question'][':question/difficulty'].split('/')[-1],m['seed'],m['template'],parameters=m['parameters'],profile=m['bank_profile']);qid=r['question'][':question/id'];q=by.get(qid)
  assert r==old,('historical complete reproduction',qid)
  assert q and q[':question/problem']==r['question'][':question/problem'] and q[':question/worked-solution']==r['question'][':question/worked-solution']
  assert sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in field(r)[':answer-field/choices'])
  assert ':question/math-academy-id' not in q
  reproduced.append(r);tests.append({'question_id':qid,'entity_id':q[':db/id'],'exact_complete_record_reproduced':True})
  if shortcut(r):affected.append({'question_id':qid,'entity_id':q[':db/id'],'finding':'Unique C + square inside cube root predicts the correct choice without reading the ODE in the historical easy generated record.','reproduction':str(sys.executable)+' -B checks/regressions.py --finding inventory; original generate_easy('+str(m['seed'])+', '+repr(m['template'])+', parameters='+repr(m['parameters'])+', profile='+repr(m['bank_profile'])+')','evidence_path':'../workspace/evidence/generated-records.json'})
 # Keep all writes inside workspace; record paths relative to the supplied
 # author-1 evidence_root, which is a sibling of workspace.
 save('generated-records.json',reproduced);save('affected-inventory.json',{'affected_questions':affected})
 save('inventory-audit.json',{'basis':inv['basis'],'questions':len(inv['questions']),'tested':tests,'affected_count':len(affected),'limits':'All six captured generated recipes reproduced exactly; one stored easy item demonstrates the retained shortcut. Other five stored hard items were checked only for that exact cue, not certified free of other weaknesses. Fourteen original source questions are not marked as generated.'})
 print('Inventory: reproduced',len(reproduced),'historical generated entries;',len(affected),'demonstrated affected')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--finding',choices=['source','shortcut','grading','inventory','all'],default='all');a=ap.parse_args()
 if a.finding=='source':replay()
 elif a.finding=='shortcut':shortcut_checks()
 elif a.finding=='inventory':inventory()
 elif a.finding=='grading':grading(easy_grid(),[],[],[])
 else:
  source=replay();rows,pairs,batch=shortcut_checks();grading(rows,source,pairs,batch);inventory()
if __name__=='__main__':main()
