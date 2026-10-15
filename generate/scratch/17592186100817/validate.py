#!/usr/bin/env python3
"""Validate actual rendered mathematics independently and preserve all native gaps."""
import sys
sys.dont_write_bytecode=True
import json,hashlib,copy,re,subprocess,importlib.util
from pathlib import Path
import sympy as s
H=Path(__file__).parent;ROOT=H.parents[2]
def load(name,p):
 z=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('otherlog_generate',H.with_suffix('.py'));P=load('otherlog_reader',H/'readback.py');x,u=P.x,P.u

def write(name,data):(H/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def fullsame(a,b):
 positive=s.Symbol('positive_x',positive=True)
 return s.simplify(s.expand_log((a-b).subs(x,positive)))==0
sources=[];variants=[];ledger=[];totals={'originals':0,'source_choices':0,'matched_source_choices':0,'complete_source_banks':0,'operative_stages':0,'variant_records':0};source_errors=[]
for index,(sid,(level,orig))in enumerate(G.CONFIG.items()):
 p=G.parameters(orig);r=G.generate(level,index,template=sid,parameters=p,profile='observed');sources.append(r)
 F,U,n=P.check(r,allow_source_error=sid in G.ERRORS);totals['originals']+=1;totals['operative_stages']+=n['integral_sides']+n['primitive_sides'];print('original',sid,flush=True)
 raw=G.QS[sid];sf=raw[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0]
 # Source fidelity is full rendered mathematical value and ordered stage counts;
 # source notation is normalized rather than returned from a literal payload branch.
 rawcopy=copy.deepcopy(r);rawcopy['question'][':question/problem']=raw[':question/problem'];rawcopy['question'][':question/worked-solution']=raw[':question/worked-solution']
 _,_,rawstages=P.check(rawcopy,allow_source_error=sid in G.ERRORS)
 assert (n['integral_sides'],n['primitive_sides'])==(rawstages['integral_sides'],rawstages['primitive_sides'])
 def signature(sol):
  z=[]
  for block in re.findall(r'\$\$(.*?)\$\$',P.preprocess(sol),re.S):
   if r'\int'not in block:continue
   for row in re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','').split(r'\\'):
    for part in row.split('='):
     if not part.strip():continue
     v,formal=P.E.side(part,x,U);z.append(('integral',str(formal[0][1]))if formal else('primitive','u'if re.search(r'(?<![A-Za-z])u(?![A-Za-z])',part)else'x'))
  return z
 assert signature(r['question'][':question/worked-solution'])==signature(raw[':question/worked-solution']),('source stage order',sid)
 vals,key=G.bank(sid,p);choices=[]
 for i,(a,recipe)in enumerate(zip(sf[':answer-field/choices'],vals)):
  actual=P.scalar(a[':answer/value']);rendered=G.tex(recipe)+'+C';pred=P.scalar(rendered)
  matched=fullsame(actual,pred)
  assert matched,('unmapped full original option',sid,i,a[':answer/value'],rendered,actual,pred)
  symbolic=G.recipes(sid,*s.symbols('b a m n k d',positive=True))[0][i]
  choices.append({'expression_with_slots':str(symbolic),'source_answer_id':a[':answer/id'],'source_field_id':sf[':answer-field/id'],'source_value':a[':answer/value'],'source_parameters':p,'recipe_index':i,'parameterized_recipe':str(recipe),'rendered_at_source':rendered,'complete_value_matched':matched,'interpretation':'observed algebraic pattern; no misconception intent asserted'})
  totals['source_choices']+=1;totals['matched_source_choices']+=matched
 ledger.append({'source_id':sid,'profile':sid+'-observed','difficulty':level,'choices':choices});totals['complete_source_banks']+=1
 if sid in G.ERRORS:
  repaired=G.generate(level,index+500,template=sid,parameters=p,profile='repaired');P.check(repaired);variants.append(repaired)
  source_errors.append({'source_id':sid,'problem':G.ERRORS[sid],'raw_record':r,'raw_validation':n,'repair':repaired,'repair_reason':'repair only the minimum duplicate choices: q31395 two of three duplicate distractors, q210752 one duplicate-correct distractor; other recipes/key preserved'})
 for j in range(2):
  r=G.generate(level,1000+index*37+j,template=sid);P.check(r);variants.append(r);totals['variant_records']+=1
write('source-cases.json',[{'source_id':r['generation']['template'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'bank_profile':r['generation']['bank_profile'],'profile':'observed','level':r['question'][':question/difficulty'].split('/')[-1],'record':r}for r in sources]);write('review-cases.json',variants);write('choice-ledger.json',ledger);write('source-errors-and-repairs.json',source_errors)

# Correct final key is held unchanged for every mutation; stages must stand on their own.
mutants=[]
for name,replace in[
 ('wrong-substitution',lambda t:t.replace('Let $u=', 'Let $u=2\\cdot ',1)),
 ('wrong-differential',lambda t:t.replace(r'\frac{\text{d}x}{x}',r'2\frac{\text{d}x}{x}',1)),
 ('wrong-formal-integrand',lambda t:t.replace(r'\int',r'2\int',1)),
 ('wrong-constant-extraction',lambda t:t.replace(r'\int u',r'2\int u',1)),
 ('wrong-primitive',lambda t:t.replace('+C',r'+x+C',1)),
 ('nonconstant-C',lambda t:t.replace('+C',r'+x',1)),
 ('stale-differential-variable',lambda t:t.replace(r'\text{d}u',r'\text{d}x',1)),
]:
 row=copy.deepcopy(variants[2]);original=row['question'][':question/worked-solution'];changed=replace(original);assert changed!=original,(name,original);row['question'][':question/worked-solution']=changed
 try:P.check(row)
 except (AssertionError,ValueError,StopIteration,IndexError)as e:mutants.append({'name':name,'caught':True,'reason':str(e)[:300],'record':row})
 else:raise AssertionError(('mutation escaped',name))
write('mutation-probes.json',mutants)
# Fresh batch uniqueness uses actual mathematics identity, excluding profile and seed.
batch=G.batch('all',2275,10);assert len(batch)==30 and len({r['generation']['math_fingerprint']for r in batch})==30
for r in batch:P.check(r)
assert len({P.mathematical_task(r)for r in batch})==30
write('actual-task-inventory.json',[{'mathematical_task':P.mathematical_task(r),'claimed_math_fingerprint':r['generation']['math_fingerprint']}for r in batch])
for value in [True,False,1.5,'1',None]:
 try:G.generate('easy',value)
 except ValueError:pass
 else:raise AssertionError('accepted noninteger seed')
 for args in[('all',1,value),('all',value,1)]:
  try:G.batch(*args)
  except ValueError:pass
  else:raise AssertionError('accepted noninteger batch input')
for args in[('all',1,0),('all',1,501)]:
 try:G.batch(*args)
 except ValueError:pass
 else:raise AssertionError('capacity or zero count accepted')
assert G.batch('all',3,1)==G.batch('all',3,1)
cli=json.loads(subprocess.check_output([sys.executable,'-B',str(H.with_suffix('.py')),'--difficulty','all','--count','1','--seed','2275']));assert isinstance(cli,list)and len(cli)==3
write('batch-cases.json',batch)

# Native radio checks retain source field contract, including known bad sourcebanks.
engine=ROOT/'generate/runs/current/check-engine';expected=json.loads((H/'pre-import-baseline.json').read_text())['engine_sha256'];assert hashlib.sha256(engine.read_bytes()).hexdigest()==expected
write('independent-inventory.json',{'database':'math','basis':G.SOURCE['basis'],'lineage':G.SOURCE['lineage'],'questions':[],'description':'Captured non-Math Academy records only: none at basis2275. Synthetic blank probes are separate.'})
inputs=[]
for i,r in enumerate(sources+variants):
 f=r['question'][':question/answer-fields'][0];checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'full original radio bank identity contract'if i<len(sources)else'full variant radio bank identity contract'}for a in f[':answer-field/choices']];inputs.append({'label':str(i)+' '+r['generation']['template'],'record':r,'checks':checks})
blanks=[]
for level in('easy','moderate','hard'):
 r=copy.deepcopy(next(z for z in variants if z['question'][':question/difficulty'].endswith('/'+level)));f=r['question'][':question/answer-fields'][0];correct=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);f[':answer-field/type']=':answer-field.type/blank';f[':answer-field/key']='field-1';f[':answer-field/choices']=[correct];r['question'][':question/problem']+='\n{{field-1}}';r['generation']['synthetic_probe']=True;r['generation']['eligible']=False;r['generation']['evidence_only']=True
 probeid=G.uid('synthetic-blank:'+r['question'][':question/id']);r['question'][':question/id']=probeid;f[':answer-field/id']=G.uid(probeid+'field-1');correct[':answer/id']=G.uid(f[':answer-field/id']+correct[':answer/value']);f[':answer-field/correct']=[':answer/id',correct[':answer/id']];r['generation']['content_fingerprint']=G.digest(r['question'])
 canonical=correct[':answer/value'];equivalent='('+canonical.removesuffix('+C')+')+C+7';wrong='('+canonical.removesuffix('+C')+')+x+C'
 algebraic=s.latex(s.expand_log(P.scalar(canonical)).subs(P.C,s.Symbol('C'))).replace(r'\log',r'\ln')
 assert fullsame(P.scalar(canonical),P.scalar(algebraic))
 checks=[{'submitted':algebraic,'expected':'accepted','purpose':'genuine change-of-base algebraic equivalent primitive'},{'submitted':canonical,'expected':'accepted','purpose':'synthetic full-answer blank canonical primitive including C'},{'submitted':equivalent,'expected':'accepted','purpose':'genuine constant-offset equivalent antiderivative'},{'submitted':wrong,'expected':'rejected','purpose':'incorrect extra x has nonzero derivative'}]
 blanks.append({'label':'synthetic '+level+' blank','record':r,'checks':checks,'description':'Synthetic grading probe of the same normal rendered integral; source and normal generated formats are radio only.'});inputs.append({k:v for k,v in blanks[-1].items()if k!='description'})
write('diagnostic-blank-cases.json',blanks);write('native-input.json',inputs)
engine_dir=H/'engine';engine_dir.mkdir(exist_ok=True);reports=[];failures=[]
for i in range(0,len(inputs),3):
 records=inputs[i:i+3];inp=engine_dir/('batch-'+str(i//3)+'-input.json');out=engine_dir/('batch-'+str(i//3)+'-report.json');inp.write_text(json.dumps(records,indent=2)+'\n');out.unlink(missing_ok=True);p=subprocess.run([str(engine),str(inp),str(out)],text=True,capture_output=True);process={'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr};write('engine/batch-'+str(i//3)+'-process.json',process)
 if p.returncode==0:reports.append(json.loads(out.read_text()))
 else:
  failures.append({'input':str(inp.relative_to(H)),'requested_records':records,**process})
  # Isolate requests unchanged. No expected-result rewriting or pruning.
  for j,row in enumerate(records):
   for k,check in enumerate(row['checks']):
    one=copy.deepcopy(row);one['checks']=[check];name='probe-'+str(i+j)+'-'+str(k);inp=engine_dir/(name+'-input.json');out=engine_dir/(name+'-report.json');inp.write_text(json.dumps([one],indent=2)+'\n');out.unlink(missing_ok=True);p=subprocess.run([str(engine),str(inp),str(out)],text=True,capture_output=True);pr={'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr};write('engine/'+name+'-process.json',pr)
    if p.returncode==0:reports.append(json.loads(out.read_text()))
    else:failures.append({'isolated':True,'label':one['label'],'check':check,**pr})
write('native-grading.json',{'engine_sha256':expected,'database_writes':0,'batch_max_records':3,'reports':reports,'failures':failures,'requested_checks':sum(len(i['checks'])for i in inputs),'passed_checks':sum(r['accepted_checks']+r['rejected_checks']+r['documented_unresolved_checks']for r in reports),'qualification':'Radio identity grading checked with actual native runner. All genuine blank requests and failures retained unchanged; no diagnostic outcome relabeling.'})
write('validation.json',{'status':'mathematics passed; native qualified'if failures else'passed','totals':totals,'source_error_banks':len(source_errors),'eligible_original_banks':len(sources)-len(source_errors),'mutants_caught':len(mutants),'native_requested_checks':sum(len(i['checks'])for i in inputs),'native_failures_including_batch_and_isolation':len(failures),'engine_sha256':expected,'actual_distinct_batch_tasks':len({P.mathematical_task(r)for r in batch}),'actual_distinct_source_tasks':len({P.mathematical_task(r)for r in sources}),'actual_distinct_review_tasks':len({P.mathematical_task(r)for r in variants}),'database_writes':0,'no_plots':True})
print(json.dumps(json.loads((H/'validation.json').read_text()),indent=2))
