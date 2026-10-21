#!/usr/bin/env python3
"""Measure actual shared delivery records and conditional native selection rules."""
import sys
sys.dont_write_bytecode=True
import json,hashlib,subprocess,shutil,platform,re
from pathlib import Path
from collections import Counter
from fractions import Fraction
import sympy
R=Path(__file__).resolve().parent;J=R.parent;P=J/'workspace'
def load(p):return json.loads(Path(p).read_text())
def save(n,x):(R/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def value(a):return Fraction(re.search(r'-?\d+(?:\.\d+)?',a[':answer/value'])[0])
def measures(r):
 q=r['question'];f=q[':question/answer-fields'][0];key=f.get(':answer-field/correct');key=key.get(':answer/id') if isinstance(key,dict) else key[1] if key else None;a=f[':answer-field/choices'];vals=[value(a) for a in a];i=next((i for i,x in enumerate(a) if x[':answer/id']==key),None)
 if i is None:return None
 avg=sum(vals)/len(vals)
 eligible=[j for j,v in enumerate(vals) if all(abs(v-w)<=2 for w in vals)]
 return {'id':q[':question/id'],'template':r.get('generation',{}).get('template','captured source'),'rank':sorted(vals).index(vals[i])+1,'position':i+1,'nearest_mean':abs(vals[i]-avg)==min(abs(v-avg) for v in vals),'span':str(max(vals)-min(vals)),'radius_singleton':len(eligible)==1,'radius_shortcut_correct':len(eligible)==1 and eligible[0]==i}
def measure(rs):
 ms=[measures(r) for r in rs];ms=[x for x in ms if x];return {'count':len(rs),'ranks':dict(Counter(x['rank'] for x in ms)),'positions':dict(Counter(x['position'] for x in ms)),'radius_singletons':sum(x['radius_singleton'] for x in ms),'radius_shortcut_correct':sum(x['radius_shortcut_correct'] for x in ms),'median_success':sum(x['rank']==3 for x in ms),'nearest_mean_success':sum(x['nearest_mean'] for x in ms),'rows':ms}
stages={n:measure(load(R/file)) for n,file in [('sample before','sample-records.json'),('sample after','delivery-sample/accepted.json'),('batch before','batch-records.json'),('batch after','delivery-batch/accepted.json')]}
for a,b in [('sample before','sample after'),('batch before','batch after')]:
 assert {k:v for k,v in stages[a].items() if k!='rows'}=={k:v for k,v in stages[b].items() if k!='rows'}
 assert [{k:v for k,v in x.items() if k!='id'} for x in stages[a]['rows']]==[{k:v for k,v in x.items() if k!='id'} for x in stages[b]['rows']]
normal=load(R/'delivery-sample/accepted.json');ba=load(R/'delivery-batch/accepted.json');controls=load(R/'rank-controlled-records.json')
# Independently measure fixed bank-role seeds from minimal reported case.
save('sampling-summary.json',{'command':sys.argv,'stages':stages,'by_template':{t:measure([x for x in normal if x['generation']['template']==t]) for t in sorted({x['generation']['template'] for x in normal})},'controlled_bank_only':measure(controls),'construction_assessment':'Rank is drawn before physical parameters and four exchangeable adjacent gaps and translation implement that rank. Shuffling changes display position. Guard resampling cannot force rank; easy accepted masses admit all ranks. Historical fixed inequalities no longer define normal banks. Controlled bank-only cases are not counted as different physical tasks.','sampling_limit':'44 physical examples cover eleven source contexts. One seed per context is shared to compare equivalent mask slots; the other three use template-specific fresh seeds. Five bank-only controls cover all numerical ranks. This is bounded evidence, not proof against every cue.'})
# Current inventory has original sources and ten old generated records. Preserve origin explicitly.
inv=load(J/'source/inventory.json');old={x['question'][':question/id']:x for x in load(R/'generated-records.json')};pool=[];pool_records=[];excluded=[]
for q in inv['questions']:
 r=old.get(q[':question/id'],{'question':q});m=measures(r)
 if m is None:excluded.append(q[':question/id']);continue
 d=q.get(':question/difficulty','unrated');d=d.get(':db/ident') if isinstance(d,dict) else d
 pool.append({'entity_id':q[':db/id'],'id':q[':question/id'],'band':d.split('/')[-1],'origin':'old generated' if q[':question/id'] in old else 'original source','measurement':m});pool_records.append(r)
maxid=max(x['entity_id'] for x in pool)
new=[{'entity_id':maxid+i+1,'id':r['question'][':question/id'],'band':'easy','origin':'current batch','measurement':measures(r)} for i,r in enumerate(ba)];save('selection-pool-records.json',pool_records+ba)
def select(pool,weights,seed):
 pool=sorted(pool,key=lambda x:x['entity_id'])
 if weights is None:return pool[0] if pool else None
 bands=[[q for q in pool if q['band']==b] for b in ['easy','moderate','hard']];unrated=[q for q in pool if q['band']=='unrated'];total=sum(w for w,b in zip(weights,bands) if b)
 raw=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=lambda i:(int.from_bytes(raw[i:i+8],'big')>>11)/(1<<53)
 if total:
  draw=u(0)*total;b=[]
  for w,band in zip(weights,bands):
   if not band or not w:continue
   b=band
   if draw<w:break
   draw-=w
 else:b=unrated
 return b[int(u(8)*len(b))] if b else None
scenarios=[]
for name,pp,weights in [('new batch after prior inventory seen',new,[1,0,0]),('captured fresh bank',pool,[1,1,1]),('captured plus batch easy',pool+new,[1,0,0]),('sources seen; old and current generated easy',[x for x in pool+new if x['origin']!='original source'],[1,0,0]),('unconfigured policy fallback',pool+new,None)]:
 draws=[select(pp,weights,'revision-41071-'+str(i)) for i in range(100)];selected=[x for x in draws if x]
 # Complete pool enumeration preserves visibility of every eligible decision case.
 scenarios.append({'case':name,'assumed_weights':weights,'fresh_candidate_ids':[x['id'] for x in pp],'draw_count':100,'selected_origin_counts':dict(Counter(x['origin'] for x in selected)),'radius_shortcut_correct_draws':sum(x['measurement']['radius_shortcut_correct'] for x in selected),'selected_rank_counts':dict(Counter(x['measurement']['rank'] for x in selected)),'selected_records':selected,'eligible_band_counts':dict(Counter(x['band'] for x in pp))})
save('delivery-selection-results.json',{'command':sys.argv,'captured_basis':inv['basis'],'stages':{k:{kk:vv for kk,vv in v.items() if kk!='rows'} for k,v in stages.items()},'actual_filter_reports':['delivery-sample/delivery.json','delivery-batch/delivery.json'],'generator_rejection':'runtime-results.json contains failed candidate physical constraints and deterministic replay. Chosen rank precedes sample rejection; whole-shape positivity resampling retains the chosen rank; independent low-mass checks recorded separately.','learner_selection_implementation':'engine/rust/question_selection.rs::select and seen_before_task (read-only faithful reproduction)','engine_sha256':hashlib.sha256(Path('/home/jake/Developer/Course_Academy/engine/rust/question_selection.rs').read_bytes()).hexdigest(),'scenarios':scenarios,'incomplete_source_excluded':excluded,'limitations':['Publication/preparation.json absent; actual shared delivery normalization/deduplication was reproduced read-only with captured inventory basis 5395.','No live learner histories or active policy are captured. Scenarios declare weights, eligibility and freshness; hypothetical new entity IDs exceed existing IDs, so unconfigured policy first-ID behavior remains explicit.','Ten historical generated records retain the old median defect and remain exposed in inventory scenarios. This is retained inventory debt, separate from the repaired generator and its five new accepted records. No database changes made.','Future inventory may differ. No finite sample certifies absence of all incidental cues.']})
# Exact dependency contract and relocation to a self-contained manifest-only copy.
manifest=load(P/'package.json');dest=R/'relocated-package';dest.mkdir(exist_ok=True)
for f in manifest['files']+['package.json']:
 out=dest/f;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/f,out)
cmd=[sys.executable,str(dest/manifest['entrypoint']),'--difficulty','easy','--seed','41073','--count','2','--format','json']
res=subprocess.run(cmd,cwd=R,capture_output=True,text=True);ref=subprocess.run([sys.executable,str(P/manifest['entrypoint']),*cmd[2:]],cwd=R,capture_output=True,text=True);assert res.returncode==ref.returncode==0 and res.stdout==ref.stdout
save('relocation-records.json',json.loads(res.stdout));deps=manifest['dependencies'];assert deps['python']==platform.python_version() and deps['packages']=={'sympy':sympy.__version__}
after={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in P.rglob('*') if f.is_file()};save('package-after.json',after);assert after==load(R/'package-before.json')
save('packaging-results.json',{'command':cmd,'exit_code':res.returncode,'relocated_equals_original':res.stdout==ref.stdout,'manifest_dependencies':deps,'actual_versions':{'python':platform.python_version(),'sympy':sympy.__version__},'declared_files_present':all((P/f).is_file() for f in manifest['files']),'original_package_unchanged':True,'external_outputs':'Standard output JSON only; no image assets or external output path. All imports used by public entrypoint are standard library or declared SymPy.','fixture_note':'Only isolated evidence copies were used to execute author checks and old negative controls.'})
print(json.dumps({'stages':{k:{kk:vv for kk,vv in v.items() if kk!='rows'} for k,v in stages.items()},'package_unchanged':True,'selection_scenarios':len(scenarios)}))
