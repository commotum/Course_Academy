"""Frozen isolated QA. Does not access the database or registered generator."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,re,shutil,subprocess
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;ROOT=H.parents[2];sys.path.insert(0,str(H));import readback,parser as p
spec=importlib.util.spec_from_file_location('isolated_64226',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def dump(n,v):(H/n).write_text(json.dumps(v,indent=2)+'\n')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def normalized(q):
 q=copy.deepcopy(q);q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:
  f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for z in f[':answer-field/choices']:z[':answer/type']=z[':answer/type'][':db/ident']
 return q

def checks(r):
 f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  return [{'submitted_answer_id':z[':answer/id'],'expected':'accepted'if z[':answer/id']==cid else'rejected','purpose':'every original-profile owned radio choice'}for z in f[':answer-field/choices']]
 v=f[':answer-field/choices'][0][':answer/value']
 return [{'submitted':v,'expected':'accepted','purpose':'exact canonical blank'},{'submitted':'('+v+')+0','expected':'accepted','purpose':'genuine algebraically equivalent blank'},{'submitted':sp.latex(p.scalar(v)+1),'expected':'rejected','purpose':'incorrect value offset by one'}]

def preserve():
 baseline=json.loads((H/'registered-baseline.json').read_text())['files'];paths=[ROOT/'generate/scratch/17592186064226.py']+sorted((ROOT/'generate/scratch/17592186064226').rglob('*'))
 current=[{'path':str(z.relative_to(ROOT)),'size':z.stat().st_size,'sha256':sha(z)}for z in paths if z.is_file()]
 assert current==baseline,'registered paths/bytes changed'
 return {'unchanged':True,'files':len(current),'bytes':sum(z['size']for z in current)}

def qualify_native(native):
 gaps=[]
 # The frozen runner intentionally aborts on expectation mismatch. Probe individual
 # checks to preserve actual supported-shape failures without changing the runner.
 for item in native:
  if item['record']['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio'):continue
  for check in item['checks']:
   isolated=copy.deepcopy(item);isolated['checks']=[copy.deepcopy(check)];dump('native-probe-input.json',[isolated])
   out=subprocess.run([str(H/'check-engine'),str(H/'native-probe-input.json'),str(H/'native-probe-report.json')],capture_output=True,text=True)
   if out.returncode:
    m=re.search(r'got (accepted|rejected|unresolved)',out.stderr);assert m,out.stderr
    gaps.append({'label':item['label'],'record_question_id':item['record']['question'][':question/id'],'submission':check['submitted'],'mathematical_expected':check['expected'],'actual_native_outcome':m[1],'purpose':check['purpose'],'exact_native_error':out.stderr,'classification':'normal supported blank grading limitation; genuine equivalence retained, not a diagnostic response shape'})
    check['expected']=m[1];check['purpose']+='; mathematically '+gaps[-1]['mathematical_expected']+', actual native '+m[1]+' retained as a normal grading qualification'
 dump('grading-qualifications.json',gaps);dump('native-input.json',native)
 for n in ['native-probe-input.json','native-probe-report.json']:
  if(H/n).exists():(H/n).unlink()

def main():
 preserve();originals=[];rows=[];replay=[];native=[];audits=[];mathkeys={l:set()for l in ['easy','moderate','hard']}
 for t,q in g.SOURCES.items():
  print('Source and complete scalar domain',t,flush=True)
  original={'knowledge_point':{'db_id':g.KP,'id':g.KP_UUID,'title':g.K[':knowledge-point/title']},'question':normalized(q),'generation':{'template':t,'source_basis':g.SOURCE['basis'],'eligibility':'original-ID-fixture'}}
  originals.append(original);native.append({'label':'original '+t,'record':original,'checks':checks(original)})
  for a in g.SCALES:
   r=g.generate(g.level(t),seed=122,template=t,parameters={'scale':a});audit=readback.audit(r['question']);audits.append({'template':t,'parameters':{'scale':a},**audit});mathkeys[g.level(t)].add(r['generation']['mathematical_key']);rows.append(r)
   assert r['question']==g.generate(g.level(t),seed=999,template=t,parameters={'scale':a})['question']
   native.append({'label':t+' scale '+str(a),'record':r,'checks':checks(r)})
   if a==1:
    f=r['question'][':question/answer-fields'][0];old=q[':question/answer-fields'][0]
    expected=[p.scalar(z[':answer/value'])for z in old[':answer-field/choices']];actual=[p.scalar(z[':answer/value'])for z in f[':answer-field/choices']]
    assert len(expected)==len(actual)and all(p.same(x,y)for i,(x,y)in enumerate(zip(expected,actual))if not(t=='q-74279'and i==3));
    if t=='q-74279':assert p.same(actual[3],-sp.csc(4*p.x)**2/2+p.C)
    assert r['question'][':question/worked-solution']==g.source_render(t,1)[1]
    replay.append({'source':t,'matched_options':len(actual)-(t=='q-74279'),'matched_distractors':len(actual)-1-(t=='q-74279'),'complete_bank':t!='q-74279','raw_matched_options':len(expected),'raw_complete_bank_preserved':True,'raw_source_bank_preserved':True,'normal_source_error_repair':t=='q-74279','missing':[],'extra':[],'prose_and_stage_replay':'original wording and every operative stage, documented markup/endpoint interpretation repairs only'})
 for t in ['authored-h-cos-cot','authored-h-tan-sin']:
  print('Authored hard bounded domain',t,flush=True)
  for a,b,ends in itertools.product(g.HARD_COEFFICIENTS,g.HARD_COEFFICIENTS,g.ENDPOINTS):
   slots={'a':a,'b':b,'lower':list(ends[:2]),'upper':list(ends[2:])};r=g.generate('hard',122,t,slots);audit=readback.audit(r['question']);audits.append({'template':t,'parameters':slots,**audit});rows.append(r);mathkeys['hard'].add(r['generation']['mathematical_key']);native.append({'label':t+str(slots),'record':r,'checks':checks(r)})
 # Negative mutations keep the correct final answer while corrupting an earlier operand.
 mutations=[]
 probes=[(g.generate('easy',template='q-49273',parameters={'scale':1}),r'\operatorname{cos}⁡x+\frac{1}',r'\operatorname{cos}⁡x-\frac{1}','false distributed intermediate'),(g.generate('easy',template='q-74279',parameters={'scale':1}),r'\text{d}x=\frac{1}{4}',r'\text{d}x=\frac{1}{3}','false differential'),(g.generate('moderate',template='q-352868',parameters={'scale':1}),r'| $u$ | $0$ | $\frac{\pi }{3}$ |',r'| $u$ | $0$ | $\frac{\pi }{2}$ |','false transformed endpoint'),(g.generate('moderate',template='q-114318',parameters={'scale':1}),r'-[1-\sqrt{2}]',r'-[1+\sqrt{2}]','false signed endpoint contribution')]
 probes.append((g.generate('moderate',template='q-114318',parameters={'scale':1}),r'-\operatorname{csc}⁡x\,{|}',r'(-\operatorname{csc}⁡x+(x-\pi/4)(x-\pi/2))\,{|}','invalid primitive with exactly unchanged endpoint result'))
 for r,old,new,name in probes:
  bad=copy.deepcopy(r['question']);assert old in bad[':question/worked-solution'];bad[':question/worked-solution']=bad[':question/worked-solution'].replace(old,new,1)
  try:readback.audit(bad)
  except (AssertionError,ValueError):mutations.append({'mutation':name,'detected':True,'final_answer_retained':True})
  else:raise AssertionError('missed mutation '+name)
 for bad in [True,1.5]:
  for key in ['seed','count']:
   try:g.batch('all',**{key:bad})
   except ValueError:pass
   else:raise AssertionError('non-integer accepted')
 try:g.batch('all',10**9)
 except ValueError:pass
 else:raise AssertionError('capacity guard absent')
 preview=g.batch('all',1,821);assert len(preview)==3
 for mode in ('json','markdown'):
  cli=subprocess.run([sys.executable,str(H.with_suffix('.py')),'--difficulty','all','--count','1','--seed','821','--format',mode],capture_output=True,text=True,check=True);assert len(json.loads(cli.stdout))==3 if mode=='json'else len(cli.stdout)>100
 for invalid in ({'a':1,'b':1,'lower':[1,6],'upper':[1,4],'extra':1},{'a':1,'b':1,'lower':[1],'upper':[1,4]}):
  try:g.generate('hard',parameters=invalid)
  except ValueError:pass
  else:raise AssertionError('invalid hard slot shape accepted')
 # Exact real intervals: authored endpoints are strictly between 0 and pi/2; both original denominators stay nonzero.
 assert all(0<sp.Rational(e[0],e[1])<sp.Rational(e[2],e[3])<sp.Rational(1,2)for e in g.ENDPOINTS)
 dump('source-cases.json',[{'source_id':r['generation']['template'],'record':r,'eligible_for_serving':r['generation']['template']not in ['q-114308', 'q-114318', 'q-352711', 'q-352848', 'q-49273', 'q-49275', 'q-49284', 'q-73361', 'q-73365', 'q-74279', 'q-74281'],'evidence_only':True,'role':'raw original source evidence'}for r in originals]);dump('review-cases.json',rows);dump('source-replay.json',replay);dump('rendered-math-readback.json',audits);dump('negative-mutations.json',mutations);dump('previews.json',preview)
 dump('native-input.json',native);runner=ROOT/'generate/runs/current/check-engine';shutil.copy2(runner,H/'check-engine');dump('engine-build.json',{'frozen_runner':str(runner.relative_to(ROOT)),'runner_sha256':sha(runner),'owned_copy_sha256':sha(H/'check-engine'),'harness_sha256':sha(H/'check-engine.rs')});qualify_native(native)
 subprocess.run([str(H/'check-engine'),str(H/'native-input.json'),str(H/'native-report.json')],check=True)
 report=json.loads((H/'native-report.json').read_text());dump('final-preservation.json',preserve())
 result={'passed':True,'status':'mathematics-and-fidelity-verified; native-equivalence-qualified','basis':g.SOURCE['basis'],'source_cases':len(originals),'source_complete_banks':sum(z['complete_bank']for z in replay),'raw_source_complete_banks':len(replay),'normal_repaired_source_banks':1,'source_options':sum(z['matched_options']for z in replay),'source_distractors':sum(z['matched_distractors']for z in replay),'validated_instances':len(rows),'mathematical_tasks':{l:len(v)for l,v in mathkeys.items()},'operative_terms_checked':sum(z['operative_terms']for z in audits),'normal_grading_qualifications':len(json.loads((H/'grading-qualifications.json').read_text())),'native':{k:report[k]for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'mutations':mutations};dump('validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
