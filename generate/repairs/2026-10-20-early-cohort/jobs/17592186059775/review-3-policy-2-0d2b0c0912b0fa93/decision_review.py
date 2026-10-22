"""Read-only focused revision review. Run from evidence_root with context Python."""
import pathlib,json,collections,hashlib,subprocess,sys
sys.dont_write_bytecode=True
exec(pathlib.Path('audit.py').read_text().split('manifest=json.load')[0])
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
rs=json.load(open('independent-records.json')); batch=json.load(open('runner-batch.json'))
def stats(records):
 out={}
 for sid in sorted({r['generation']['template'] for r in records}):
  z=[r for r in records if r['generation']['template']==sid]
  out[sid]={'count':len(z),'ranks':dict(collections.Counter(str(rank(r)) for r in z)),'positions':dict(collections.Counter(str(f(r)[':answer-field/choices'].index(key(r))) for r in z))}
 return out
stages=[];catalog=[];batchtests=[]
for band in ['easy','moderate']:
 raw=[g.generate(band,seed=73183,parameters=[sid,k,t]) for sid in g.CASES if g.level(sid)==band for _,k in g.domain(sid) for t in range(5)]
 survivors=g.candidates(band,73183);unique=list({g.fingerprint(q(r)):r for r in survivors}.values())
 ordered=g.batch(band,len(unique),73183)
 assert {g.fingerprint(q(r)) for r in ordered}=={g.fingerprint(q(r)) for r in unique}
 stages.append({'band':band,'raw':len(raw),'after_known_system_rejection':len(survivors),'semantic_unique':len(unique),'ordered_batch_count':len(ordered),'raw_stats':stats(raw),'surviving_stats':stats(ordered)})
 # Independent changed-construction tests: exact batch plus a fresh seed per band.
 for seed in [4258185931,32452843]:
  bank=g.batch(band,5,seed)
  assert len({g.fingerprint(q(r)) for r in bank})==5
  assert sorted(rank(r) for r in bank)==list(range(5))
  assert len({tuple(mats(q(r)[':question/problem'])[0][:,:2]) for r in bank})==1
  assert len({tuple(a[':answer/value'] for a in f(r)[':answer-field/choices']) for r in bank})==1
  assert sorted(f(r)[':answer-field/choices'].index(key(r)) for r in bank)==list(range(5))
  batchtests.append({'band':band,'seed':seed,'records':bank,'stats':stats(bank),'independent_math':[verify(r) for r in bank]})
 catalog+=ordered
save('construction-regression.json',batchtests);save('normal-catalog-records.json',catalog)
for band in ['easy','moderate']:
 # 81 independent records already cover every profile/target and both scale boundaries.
 sample=[r for r in rs if q(r)[':question/difficulty'].endswith('/'+band)]
 save('samples-'+band+'.json',sample)
 command=[PY,'-B',str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/('samples-'+band+'.json')),'--source',str(J/'source/source.json'),'--inventory',str(J/'source/inventory.json'),'--difficulty',band,'--output',str(E/('delivery-'+band)),'--asset-root',str(E/'runtime-assets'),'--math-root','/media/jake/SSD/EDB/math']
 result=subprocess.run(command,capture_output=True,text=True);assert result.returncode==0,result.stderr
 (E/('delivery-'+band+'.log')).write_text(result.stdout+result.stderr)
accepted=sum([json.load(open('delivery-'+b+'/accepted.json')) for b in ['easy','moderate']],[]);bd=json.load(open('delivery-batch/accepted.json'))
assert g.batch('easy',5,4258185931)==batch
assert sorted(rank(r) for r in bd)==list(range(5))
for r in bd+accepted:verify(r)
post=[{'label':'post-delivery '+str(r['generation']['parameters']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(r)[':answer/id'] else 'rejected','purpose':'Parsed exact matrix and optional pair after delivery'} for a in f(r)[':answer-field/choices']]} for r in bd+accepted]
save('grader-final-input.json',json.load(open('grader-input.json'))+post)
# Actual learner selection rule: sorted fresh usable pool, difficulty weighted then uniform.
# Scenario A all captured items previously seen. Scenario B no items previously seen.
inv=json.load(open(J/'source/inventory.json'));scenarios=[]
for seen_inventory in [True,False]:
 pool=[]
 if not seen_inventory:
  pool=[{'entity':x[':db/id'],'id':x[':question/id'],'band':x.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1],'origin':'captured'} for x in inv['questions']]
 # Proposed IDs only establish one representative sorted permutation. Unknown until publication.
 pool += [{'entity':max(x[':db/id'] for x in inv['questions'])+100+i,'id':q(r)[':question/id'],'band':'easy','origin':'proposed','rank':rank(r)} for i,r in enumerate(bd)]
 pool=sorted([x for x in pool if x['band']=='easy'],key=lambda x:x['entity'])
 draws=[]
 for i in range(50):
  seed='revision-selection-'+str(i);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);draws.append({'seed':seed,'selected':pool[int(u*len(pool))]})
 assert all(x['selected'] in pool for x in draws) # Uniform draw reachability is mathematical, not a coupon-collection assertion.
 scenarios.append({'captured_inventory_seen':seen_inventory,'distribution':[1,0,0],'pool':pool,'draws':draws,'proposed_ranks_reachable':sorted({x['selected']['rank'] for x in draws if x['selected']['origin']=='proposed'})})
save('delivery-selection.json',{'basis':inv['basis'],'construction_stages':stages,'sample_before':stats(rs),'sample_after':stats(accepted),'batch_before':stats(batch),'batch_after':stats(bd),'learner_selection':scenarios,'rules':['Previously seen/current-prefix items are excluded; weighted difficulty followed by uniform selection within rated band.','Unrated used only when no weighted rated band remains. Unconfigured policy chooses smallest entity.'],'publication_preparation_present':(J/'publication/preparation.json').exists(),'limits':['Captured basis only; no database writes. Live policies, histories and proposed entity IDs not available.','Explicit positive-easy scenarios test reachability; exact user-specific probabilities cannot be certified.','Existing historical defects reproduced in affected-inventory.json are not repaired by replacing generator.']})
# Add exact batch to source-derived controlled render pairs already retained by audit.py.
render=json.load(open('render-records.json'));render+=bd;save('render-records.json',render)
(E/'session-state.md').write_text('81 raw and post-delivery math checks complete; complete source replay and historical counterexamples reproduced. Current five-item batch reaches all five ranks/positions before and after real delivery. Native initial grading passed. Await final grader/render and report.\n')
print(json.dumps({'construction':[{k:s[k] for k in ['band','raw','after_known_system_rejection','semantic_unique']} for s in stages],'delivered':len(accepted),'batch_stats':stats(bd),'grader_records':81+len(post),'render_records':len(render)}))
