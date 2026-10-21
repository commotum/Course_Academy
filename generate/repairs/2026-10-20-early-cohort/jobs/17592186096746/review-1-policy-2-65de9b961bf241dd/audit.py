"""Bounded independent revision review; outputs only in this script's directory."""
import os,sys,json,copy,re,random,subprocess,hashlib,platform,shutil,collections,importlib.util
sys.dont_write_bytecode=True
import review as t
from shortcut import measure,sign_strategy
E=t.E;W=t.W;J=t.J;R=t.R;PY=t.PY
save=t.save

def operations(r):
 current=pending=None;steps=0
 for b in re.findall(r'\$\$(.*?)\$\$',r['question'][':question/worked-solution'],re.S):
  if '\\begin{array}' in b:
   nxt=t.matrix(b)
   if current is not None:
    assert pending,'operation absent';a=copy.deepcopy(current);op=pending.replace(' ','')
    sw=re.fullmatch(r'R_(\d)\\leftrightarrowR_(\d)',op);add=re.fullmatch(r'R_(\d):=R_\1\+\((.*?)\)R_(\d)',op);scale=re.fullmatch(r'R_(\d):=\((.*?)\)R_\1',op)
    if sw:
     i,j=[int(v)-1 for v in sw.groups()];a[i],a[j]=a[j],a[i]
    elif add:
     i,f,j=add.groups();i=int(i)-1;j=int(j)-1;a[i]=[x+t.scalar(f)*y for x,y in zip(a[i],a[j])]
    elif scale:
     i,f=scale.groups();i=int(i)-1;a[i]=[t.scalar(f)*x for x in a[i]]
    else:raise AssertionError('unparsed '+op)
    assert a==nxt,op;steps+=1
   current=nxt;pending=None
  elif b.strip().startswith('R_'):pending=b.strip()
 assert current==t.rref(t.equations(r['question'][':question/problem']))
 return steps

def value(r):
 f=r['question'][':question/answer-fields'][0]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])

def run():
 # Reproduce retained defects using the actual preserved original runtime.
 oldpath=W/'evidence/before-package/generator.py'
 spec=importlib.util.spec_from_file_location('pre_repair',oldpath);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
 source=json.load(open(J/'source/source.json'))['material']['kp'];expected={q[':question/id'] for q in source[':knowledge-point/questions']}
 oldreplay=old.replay();oldmin=old.generate('easy',1,913771);oldbatch=old.generate('easy',5,4221100018)
 save('historical-failing-records.json',oldmin+oldbatch)
 before={'command':str(PY)+' '+str(E/'audit.py'),'snapshot_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),'missing_source':sorted(expected-{r['generation']['parameters']['source_id'] for r in oldreplay}),'minimal':measure(oldmin),'batch':measure(oldbatch)}
 assert before['missing_source']==['693512da-f45c-5aae-999f-b43069296756'];assert before['minimal']['successes']==1 and before['batch']['successes']==5
 save('historical-failure-results.json',before)
 # Current minimal seed, exact runner batch and independently selected fresh seeds.
 minimal=t.g.generate('easy',1,913771);batch=json.load(open(J/'samples.json'));easy=t.g.generate('easy',40,2026102107);moderate=t.g.generate('moderate',16,2026102173);replay=t.g.replay()
 save('minimal.json',minimal);save('batch.json',batch);save('fresh-easy.json',easy);save('fresh-moderate.json',moderate);save('source-replay.json',replay)
 assert t.g.generate('easy',5,4221100018)==batch
 mapped={r['generation']['parameters']['source_id']:r for r in replay};reps=[]
 for q in source[':knowledge-point/questions']:
  sid=q[':question/id'];assert sid in mapped,sid;r=mapped[sid];band=q.get(':question/difficulty',{}).get(':db/ident');iseasy=band==':question.difficulty/easy';sf=q[':question/answer-fields'][0];gf=r['question'][':question/answer-fields'][0]
  def norm(s):
   s=s.replace('\\\\begin','\\begin').replace('\\\\end','\\end').replace('\\\\\\\\','\\\\');return s if s=='No solution' else str(t.matrix(s) if iseasy else t.vector_parts(s))
  assert t.equations(q[':question/problem'])==t.equations(r['question'][':question/problem'])
  assert [norm(a[':answer/value']) for a in sf[':answer-field/choices']]==[norm(a[':answer/value']) for a in gf[':answer-field/choices']]
  assert r['question'].get(':question/difficulty')==band
  sk=sf.get(':answer-field/correct')
  if sk:
   si=next(i for i,a in enumerate(sf[':answer-field/choices']) if a[':answer/id']==sk[':answer/id']);assert gf[':answer-field/choices'][si][':answer/id']==gf[':answer-field/correct'][1]
  reps.append({'source_id':sid,'prompt_math_equal':True,'complete_bank_equal':True,'choices':len(sf[':answer-field/choices']),'stored_key_equal':True if sk else 'not captured; inferred independently','difficulty_equal':True})
 restored=mapped['693512da-f45c-5aae-999f-b43069296756'];assert 'R_3:=R_3+(-16)R_1' in restored['question'][':question/worked-solution'];assert operations(restored)==3
 cp=dict(profile='q-74536',source_id=source[':knowledge-point/canonical-example'][':question/id'],difficulty='easy',b=-3,c=1,d=4,scales=[2,-6,4],plan='normalize');canonical=t.g.build(cp,source_replay=True)
 assert t.equations(source[':knowledge-point/canonical-example'][':question/problem'])==t.equations(canonical['question'][':question/problem'])
 save('canonical-replay.json',[canonical]);save('source-replay-results.json',{'passed':True,'cases':reps,'total':16,'choices':80,'canonical_prompt_math_equal':True,'corrected_source_annotation':True,'solution_fidelity':'Original normalize/swap/eliminate stages retained; 693512da final operation corrected. Unclassified source lacks solution/key; replay supplies algebraically verified inference. Canonical has no answer bank.'})
 assert measure(minimal)['successes']==0 and measure(batch)['successes']==0
 save('retained-finding-results.json',{'passed':True,'prior_missing_source_reproduced':True,'prior_sign_shortcut_reproduced':True,'current_sources':len(replay),'current_seed_913771':measure(minimal),'current_exact_batch':measure(batch)})
 # Fixed banks, vary eligible member; irrelevant change rescales every input row.
 counter=[];relations=[]
 for band in ('easy','moderate'):
  for profile in ('b','c','d','all'):
   triples=[[-2,1,-3],[-4,3,-6],[-6,5,-9],[-8,7,-12],[-10,9,-18]]
   if profile!='all':
    j=('b','c','d').index(profile);triples=[[v if k==j else (-2,3,-6)[k] for k,v in enumerate(row)] for row in triples]
   p=dict(difficulty=band,profile='normalize-'+profile,scales=[-10,3,8],plan='normalize')
   rs=[t.g.numerical_bank(p,triples,i) for i in range(5)];p2=copy.deepcopy(p);p2['scales']=[10,-3,-8];rs.append(t.g.numerical_bank(p2,triples,0))
   banks=lambda r:[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
   assert all(banks(r)==banks(rs[0]) for r in rs)
   assert len({value(r) for r in rs[:5]})==5
   assert len({r['question'][':question/problem'] for r in rs[:5]})==5
   assert len({r['question'][':question/worked-solution'] for r in rs[:5]})==5
   assert value(rs[5])==value(rs[0]);assert rs[5]['question'][':question/problem']!=rs[0]['question'][':question/problem']
   start=len(counter);counter+=rs
   relations.append({'band':band,'profile':profile,'record_indices':list(range(start,start+6)),'relevant_distinct_responses':5,'bank_held_fixed':True,'prompt_solution_changed':True,'irrelevant_response_preserved':True,'grader_labels':['counter-'+str(i) for i in range(start,start+6)]})
 save('counterfactual-records.json',counter);save('counterfactual-results.json',{'command':str(PY)+' '+str(E/'audit.py'),'relations':relations,'native_grader_required':'grader-results.json','render_required':'render/rendering.json'})
 sets={'minimal':minimal,'batch':batch,'easy':easy,'moderate':moderate,'replay':replay,'canonical':[canonical],'counter':counter};math=[];cases=[]
 for name,rs in sets.items():
  for i,r in enumerate(rs):
   result=t.analyze(r);assert not result['errors'],result;result.update(set=name,index=i,displayed_operations=operations(r));math.append(result)
   f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
   cases.append({'label':name+'-'+str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'Independent visible-equation exact RREF / affine substitution determines unique correct choice.'} for a in f[':answer-field/choices']]})
 save('math-results.json',{'command':str(PY)+' '+str(E/'audit.py'),'passed':True,'tested':len(math),'failures':[],'results':math});save('grader-cases.json',cases)
 # Include exact batch, changed easy member, scale-only and restored moderate solution.
 render=batch+[counter[0],counter[4],counter[5],restored,counter[24],counter[28],counter[29]]
 save('render-records.json',render)
 coverage={name:dict(collections.Counter(r['generation']['profile'] for r in rs)) for name,rs in [('easy',easy),('moderate',moderate),('batch',batch)]}
 save('coverage.json',{'command':str(PY)+' '+str(E/'audit.py'),'seeds':{'easy':2026102107,'moderate':2026102173,'batch':4221100018},'profiles':coverage,'plans':{n:dict(collections.Counter(r['generation']['parameters']['plan'] for r in rs)) for n,rs in [('easy',easy),('moderate',moderate),('batch',batch)]},'correct_positions':{n:dict(collections.Counter(r['generation']['correct_index'] for r in rs)) for n,rs in [('easy',easy),('moderate',moderate),('batch',batch)]},'source_profile_policy':'16 observed complete profiles replayable; four numerical extensions are the random family. Selection among same-sign magnitude alternatives retains the same normalization method.','fixed_x':'Conservative observed specialization; shifting pivot to y/z need not be demanded to teach this x-pivot reduction skill.'})
 # Packaging, no writes outside evidence; relocation from declared files only.
 manifest=json.load(open(W/'package.json'));assert platform.python_version()==manifest['dependencies']['python'];assert manifest['dependencies']['packages']=={}
 rel=E/'relocated';rel.mkdir(exist_ok=True);assets=E/'output-assets';assets.mkdir(exist_ok=True)
 for n in manifest['files']:shutil.copyfile(W/n,rel/n)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(assets));env.pop('PYTHONPATH',None)
 def cli(path,args):return subprocess.run([str(PY),str(path),*args],cwd=str(E),env=env,capture_output=True,text=True)
 args=['--difficulty','easy','--count','5','--seed','4221100018','--format','json'];a=cli(W/'generator.py',args);b=cli(rel/'generator.py',args);assert a.returncode==b.returncode==0 and a.stdout==b.stdout
 invalid={}
 for name,args in [('negative',['--count','-1']),('hard',['--difficulty','hard'])]:
  x=cli(rel/'generator.py',args);assert x.returncode!=0;invalid[name]={'returncode':x.returncode,'stderr':x.stderr}
 assert t.g.generate('easy',0,2)==[];assert t.g.generate('easy',40,2026102107)==easy
 original=t.g.sample_parameters;one=original(random.Random(9814),'easy');two=original(random.Random(6178),'easy');draws=iter([one,one,two]);t.g.sample_parameters=lambda rng,band:next(draws)
 try:
  rr=t.g.generate('easy',2,27);assert rr[1]['generation']['draw']==3 and rr[1]['generation']['rejections']==1
 finally:t.g.sample_parameters=original
 t.g.sample_parameters=lambda rng,band:one
 try:
  try:t.g.generate('easy',2,27)
  except RuntimeError:bounded=True
  else:bounded=False
 finally:t.g.sample_parameters=original
 assert bounded
 save('resampling-records.json',rr)
 save('packaging.json',{'passed':True,'python':platform.python_version(),'manifest':manifest,'relocation_deterministic':True,'fresh_deterministic':True,'runner_batch_replayed':True,'invalid_inputs':invalid,'zero_count':True,'duplicates_resampled':True,'bounded_duplicate_failure':True,'relocated_files':[p.name for p in rel.iterdir()],'external_asset_count':len(list(assets.iterdir())),'fresh_rejections':sum(r['generation']['rejections'] for r in easy+moderate),'runtime_imports':'ast inspection: standard library + declared math_format.py only; packages empty'})
 save('scope-results.json',{'passed':True,'records':len(math),'reasoning':'Three equations; all proportional to a single row; one normalized x pivot, two zero rows. Easy chooses matrix and moderate chooses affine solution. Numerical-coordinate discrimination may simplify to one quotient, which directly exercises source pivot normalization.','arithmetic_bounds':'Fresh |b|,|c| <=10; |d|<=18; nonzero row multipliers <=10, source replay retains scale16.','unsupported':'hard deliberately rejected, no source hard questions; neighboring rank-two/three examples are lesson context, not this KP.'})
 (E/'session-state.md').write_text('Completed: historical failures reproduced from preserved runtime; retained findings pass current source and exact batch; 16 complete banks/80 choices plus canonical; fresh 40 easy+16 moderate; 48 fixed-bank counterfactuals; exact visible arithmetic and displayed row-operation execution; deterministic relocation and resampling. Native grader, delivery, conditional shortcut/selection and UI inspection remain.\n')
 print(json.dumps({'source_banks':len(replay),'math_records':len(math),'grader_checks':sum(len(c['checks']) for c in cases),'profiles':coverage,'historical_shortcut':before['minimal']['successes'],'current_shortcut':measure(minimal)['successes']}))
if __name__=='__main__':run()
