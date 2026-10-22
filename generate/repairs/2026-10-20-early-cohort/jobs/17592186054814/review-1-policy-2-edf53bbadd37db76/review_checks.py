"""Independent revision review. Run from evidence_root with the job Python and -B."""
import sys,os,json,pathlib,hashlib,subprocess,re,shutil,platform,collections,importlib.util
from fractions import Fraction
from math import isqrt
sys.dont_write_bytecode=True
os.environ['PYTHONDONTWRITEBYTECODE']='1'
R=pathlib.Path(__file__).resolve().parent; J=R.parent; P=J/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy'); PY=REPO/'.venv/bin/python'; PREV=J/'review-0-policy-2-0209d130634fb923'
sys.path.insert(0,str(P)); import generator as g

def save(n,x): (R/n).write_text(json.dumps(x,indent=2,ensure_ascii=False))
def hashes(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file()}
def selected(f):
 ref=f[':answer-field/correct']; aid=ref[1] if isinstance(ref,list) else ref[':answer/id']
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def semantic(r):
 fs=r['question'][':question/answer-fields']
 if fs[0][':answer-field/type']==':answer-field.type/radio':return ''.join(x for x in 'NZQRC' if re.search(r'(?<![A-Za-z])'+x+r'(?![A-Za-z])',selected(fs[0])))
 ans={re.search(r'\(\$([NZQRC])\$\)',f[':answer-field/key'])[1]:selected(f)=='true' for f in fs}
 assert set(ans)==set('NZQRC')
 return ''.join(s for s in 'NZQRC' if ans[s])
def tex(r):return re.search(r'number \$(.*?)\$ belong',r['question'][':question/problem'])[1].strip()
def family(r):
 t=tex(r)
 return 'radical' if 'sqrt' in t else 'fraction' if 'frac' in t else 'pi' if 'pi' in t else 'decimal' if '.' in t else 'integer'
def oracle(r):
 t=tex(r).replace(' ','')
 if t in [r'\pi',r'-\pi']:return 'RC'
 if t.startswith(r'\sqrt'):
  n=int(re.search(r'\{(-?\d+)\}',t)[1])
  if n<0:return 'C'
  rt=isqrt(n)
  if rt*rt!=n:return 'RC'
  x=Fraction(rt)
 elif 'frac' in t:
  n,d=map(int,re.search(r'frac\{(\d+)\}\{(\d+)\}',t).groups());x=Fraction(-n if t.startswith('-') else n,d)
 else:x=Fraction(t)
 return 'NZQRC' if x.denominator==1 and x>0 else 'ZQRC' if x.denominator==1 else 'QRC'
def imaginary(r):
 t=tex(r);n=int(re.search(r'\{(-?\d+)\}',t)[1]); s=r['question'][':question/worked-solution']
 m=re.search(re.escape(t)+r'=(.*?)\\text\{i\}',s);assert m,(t,'missing equality')
 coefficient=m[1];root=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',coefficient)
 squared=(int(root[1] or '1')**2*int(root[2])) if root else int(coefficient or '1')**2
 assert squared==-n,(t,coefficient,squared)
 assert 'nonzero' in s and semantic(r)==oracle(r)=='C'
 return {'tex':t,'coefficient':coefficient,'squared':squared,'memberships':'C'}

def main():
 save('package-before.json',hashes(P))
 # Keep a working copy of earlier independent acceptance code and execute on BOTH packages.
 old=(PREV/'source_acceptance.py').read_text()
 (R/'prior-source-acceptance-original.py').write_text(old)
 adapted=old.replace("str(root.parent/'workspace')","sys.argv[1] if len(sys.argv)>1 else str(root.parent/'workspace')").replace("root/'source-acceptance-results.json'","root/(sys.argv[2] if len(sys.argv)>2 else 'source-acceptance-results.json')")
 (R/'source_acceptance.py').write_text(adapted)
 checks=[]
 for package,name in [(PREV/'relocated-package','retained-failing-example.json'),(P,'retained-current-results.json')]:
  c=subprocess.run([str(PY),'-B',str(R/'source_acceptance.py'),str(package),name],capture_output=True,text=True)
  checks.append({'package':str(package),'command':c.args,'exit_code':c.returncode,'stdout':c.stdout,'stderr':c.stderr,'results':name})
 assert checks[0]['exit_code']==1 and checks[1]['exit_code']==0
 # Author's named preflight is rerun in a disposable copy, retaining writes only here.
 ap=R/'preflight-package';shutil.copytree(P,ap,dirs_exist_ok=True)
 (ap/'evidence').mkdir(exist_ok=True)
 sources=json.load(open(J/'source/source.json'))['material']['kp'][':knowledge-point/questions']
 (ap/'evidence/source-questions.json').write_text(json.dumps(sources))
 c=subprocess.run([str(PY),'-B',str(ap/'source_acceptance.py')],capture_output=True,text=True)
 checks.append({'command':c.args,'exit_code':c.returncode,'stdout':c.stdout,'stderr':c.stderr,'note':'Author preflight only corroborates independent checks; executed against copied unchanged package.'})
 assert c.returncode==0
 save('repair-verification.json',{'retained_findings':[x['id'] for x in json.load(open(J/'repair-history.json'))['findings']],'preflight_claim':json.load(open(J/'repair-preflight.json')),'checks':checks,'provenance':{'independent_test':str(PREV/'source_acceptance.py'),'failing_package_hashes':hashes(PREV/'relocated-package'),'earlier_package_binding':'94348d46e4fb2ff9262468a94663358972bbfc28b9cdc052aec48958f79ca2d9'}})
 batch=json.load(open(J/'samples.json')); save('batch-records.json',batch)
 sample=g.generate(count=40,seed=731905);save('sample-records.json',sample)
 # Changed domain and its mathematical boundaries; independent exact coefficient witnesses.
 negatives=[g.build({'family':'radical','n':n},seed=731906) for n in range(-144,0)]
 save('negative-records.json',negatives)
 witnesses=[imaginary(r) for r in negatives]
 class Forced:
  def __init__(self,m):self.m=m
  def choice(self,values):return 'nonreal' if 'nonreal' in values else 'radical'
  def randint(self,low,high):assert (low,high)==(1,144);return self.m
 sampler=[]
 for m in range(1,145):
  p=g.sample_parameters(Forced(m));assert p=={'family':'radical','n':-m};sampler.append(p)
 save('negative-domain-results.json',{'command':str(PY)+' -B review_checks.py','domain':[-144,-1],'count':len(negatives),'failures':[],'visible_imaginary_witnesses':witnesses,'forced_sampler_parameters':sampler,'ordinary_sample_negative_nonsquares':[tex(r) for r in sample if tex(r).startswith(r'\sqrt{-') and isqrt(-int(re.search(r'\{(-?\d+)\}',tex(r))[1]))**2!=-int(re.search(r'\{(-?\d+)\}',tex(r))[1])]})
 params=[{'family':'radical','n':n} for n in [4,2,-2,-4,-143,-144,-1,0,1,144,150]]+[{'family':'fraction','n':n,'d':3} for n in [-7,7,6,0,-27]]+[{'family':'decimal','units':n} for n in [-2000,-1,0,1,2000,325]]+[{'family':'pi','sign':n} for n in [-1,1]]
 controlled=[g.build(p,seed=731907) for p in params]; save('controlled-records.json',controlled)
 replay=g.replay_sources();save('source-replay-records.json',replay)
 results=[]
 for source in sources:
  r=next(r for r in replay if r['generation']['source_replay']==source[':question/id']);q=r['question']
  fields=q[':question/answer-fields'];sf=source[':question/answer-fields']
  result={'id':source[':question/id'],'prompt':q[':question/problem']==g.normalize_prose(source[':question/problem']),'field_contract':[(f[':answer-field/type'],f[':answer-field/key']) for f in fields]==[(f[':answer-field/type'][':db/ident'],f[':answer-field/key']) for f in sf],'complete_ordered_banks':[[a[':answer/value'] for a in f[':answer-field/choices']] for f in fields]==[[a[':answer/value'] for a in f[':answer-field/choices']] for f in sf],'available_source_key':all(selected(f)==s[':answer-field/correct'][':answer/value'] for f,s in zip(fields,sf) if ':answer-field/correct' in s),'available_solution':not source.get(':question/worked-solution') or q[':question/worked-solution']==g.normalize_prose(source[':question/worked-solution']),'math':semantic(r)==oracle(r)}
  assert all(v for k,v in result.items() if k!='id'),result
  results.append(result)
 original=g.DATA['questions']
 try:
  g.DATA['questions']=list(reversed(original));reverse=g.replay_sources()
  assert {r['generation']['source_replay']:r['question'] for r in reverse}=={r['generation']['source_replay']:r['question'] for r in replay}
 finally:g.DATA['questions']=original
 save('source-replay-results.json',{'cases':results,'source_order_independent':True,'canonical_decimal':{'record_index':21,'actual':semantic(controlled[21]),'expected':'QRC'},'gaps':'Canonical example has no answer bank. sqrt(121) has no captured key, solution or difficulty; key/solution mathematically inferred and marked inferred_repair in replay. It remains archival.'})
 all_records=sample+batch+controlled+replay+negatives
 errors=[{'tex':tex(r),'expected':oracle(r),'actual':semantic(r)} for r in all_records if oracle(r)!=semantic(r)]
 assert not errors
 save('math-results.json',{'command':str(PY)+' -B review_checks.py','count':len(all_records),'oracle':'Independent visible-prompt Fraction arithmetic, integer-square tests, signed-pi classification; generated annotations not used. For all changed negative roots square the visible solution coefficient.','failures':errors,'counts':{'fresh_sample':len(sample),'runner_batch':len(batch),'controlled':len(controlled),'source_replay':len(replay),'negative_domain':len(negatives)}})
 # Actual grader, batched into one invocation. Independently verified keys above.
 cases=[]
 for i,r in enumerate(all_records):
  checks=[]
  for fi,f in enumerate(r['question'][':question/answer-fields']):
   for a in f[':answer-field/choices']:
    checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==selected(f) else 'rejected','purpose':'Full correct and plausible wrong selections after independently checking visible prompt.'})
  cases.append({'label':str(i),'record':r,'checks':checks})
 # Cross-submit the BEFORE full response on the AFTER record, by label/value rather than IDs.
 pairs=[('relevant',0,1,'sqrt(4) -> sqrt(2)','NZQRC','RC'),('relevant',1,2,'sqrt(2) -> sqrt(-2)','RC','C'),('irrelevant',2,3,'sqrt(-2) -> sqrt(-4)','C','C'),('irrelevant',11,12,'-7/3 -> 7/3','QRC','QRC'),('relevant',13,12,'6/3 -> 7/3','NZQRC','QRC')]
 cf=[]
 for kind,b,a,change,eb,ea in pairs:
  before,after=controlled[b],controlled[a];assert semantic(before)==eb and semantic(after)==ea
  checks=[]
  for i,f in enumerate(after['question'][':question/answer-fields']):
   letter=re.search(r'\(\$([NZQRC])\$\)',f[':answer-field/key'])[1];v=str(letter in eb).lower();choice=next(x for x in f[':answer-field/choices'] if x[':answer/value']==v)
   checks.append({'field_index':i,'submitted_answer_id':choice[':answer/id'],'expected':'accepted' if (letter in eb)==(letter in ea) else 'rejected','purpose':'Submit prior membership on changed evidence; require dependent fields to reconsider.'})
  label='pair-'+str(b)+'-'+str(a);cases.append({'label':label,'record':after,'checks':checks})
  cf.append({'kind':kind,'before_index':b,'after_index':a,'change':change,'expected_before':eb,'expected_after':ea,'observed_before':semantic(before),'observed_after':semantic(after),'cross_submission_grader_label':label,'before_prompt':before['question'][':question/problem'],'after_prompt':after['question'][':question/problem'],'before_solution':before['question'][':question/worked-solution'],'after_solution':after['question'][':question/worked-solution'],'passed':True})
 save('counterfactual-results.json',cf);save('grader-input.json',cases)
 # Include exact runner batch, the counterfactual pairs and all radio banks in actual UI.
 preview=batch+controlled[:4]+[controlled[i] for i in [11,12,13]]+[r for r in replay if r['question'][':question/answer-fields'][0][':answer-field/type']==':answer-field.type/radio']
 save('render-records.json',preview)
 # Deterministic package relocation; stdout-only external output.
 rel=R/'relocated-package';rel.mkdir(exist_ok=True)
 manifest=json.load(open(P/'package.json'))
 for name in ['package.json']+manifest['files']:shutil.copyfile(P/name,rel/name)
 a=subprocess.run([str(PY),'-B',str(P/'generator.py'),'--seed','942137','--count','5'],capture_output=True,text=True,check=True)
 b=subprocess.run([str(PY),'-B',str(rel/'generator.py'),'--seed','942137','--count','5'],cwd=R,capture_output=True,text=True,check=True)
 save('relocation-records.json',json.loads(b.stdout))
 invalid=[]
 for args in [['--difficulty','hard'],['--count','-1']]:
  c=subprocess.run([str(PY),'-B',str(P/'generator.py')]+args,capture_output=True,text=True);invalid.append({'command':c.args,'returncode':c.returncode,'stderr':c.stderr});assert c.returncode!=0
 assert a.stdout==b.stdout and platform.python_version()==manifest['dependencies']['python']
 assert manifest['dependencies']['packages']=={}
 assert json.loads(a.stdout)==g.generate(seed=942137,count=5)
 save('packaging-results.json',{'python':platform.python_version(),'manifest':manifest,'exact_dependency_versions':True,'stdlib_only':True,'deterministic_relocation':a.stdout==b.stdout,'invalid_requests':invalid,'empty_count':g.generate(count=0),'seed':942137,'max_sample_attempt':sample[-1]['generation']['sampling_attempt'],'sample_rejection_policy':'Unique printed number rejection only; every math class has C, so nonempty-checkbox wrapper cannot reject a valid instance. Negative root domain expands to every -1..-144. Standard library dependencies only; CLI produces JSON stdout and no assets.','unchanged_package':hashes(P)==json.load(open(R/'package-before.json'))})
 (R/'session-state.md').write_text('Source confirmed before author inspection. Retained tests fail against earlier bound package and pass current package. Current author preflight rerun in evidence copy. All eight source banks replay. Independent math and visible coefficient witnesses pass across 144 negative radicands plus fresh sample, boundaries, batch. Grader input and render input saved; next execute actual grader, delivery and renderer. Package unchanged.\n')
 print(json.dumps({'retained_prior_exit':json.load(open(R/'repair-verification.json'))['checks'][0]['exit_code'],'retained_current_exit':json.load(open(R/'repair-verification.json'))['checks'][1]['exit_code'],'math_records':len(all_records),'source_cases':len(replay),'negative_domain':len(negatives),'sample_memberships':dict(collections.Counter(semantic(r) for r in sample)),'render_records':len(preview)}))
if __name__=='__main__':main()
