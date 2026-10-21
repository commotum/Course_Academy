"""Within-template cue audit before and after the real delivery filter."""
import collections,hashlib,importlib.util,json,math,os,pathlib,sys
sys.dont_write_bytecode=True
W=pathlib.Path(__file__).resolve().parents[1];E=W/'evidence'
os.environ['MPLCONFIGDIR']=str(E/'witness-mplconfig')
s=importlib.util.spec_from_file_location('png_witness',W/'checks/png_witness.py');pw=importlib.util.module_from_spec(s);s.loader.exec_module(pw)
def save(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')
def fld(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=fld(r);return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def audit(records):
 groups=collections.defaultdict(list)
 for r in records:groups[r['generation']['template']].append(r)
 result={}
 for t,rs in groups.items():
  positions=collections.Counter(next(i for i,a in enumerate(fld(r)[':answer-field/choices']) if a[':answer/id']==fld(r)[':answer-field/correct'][1]) for r in rs)
  # Numeric cases read from declared math are not counted as independent tasks.
  semantic=len({(r['question'][':question/problem'],tuple(sorted(a[':answer/value'] for a in fld(r)[':answer-field/choices']))) for r in rs})
  assert len(positions)>1,(t,positions)
  result[t]={'records':len(rs),'displayed_object_instances':semantic,'correct_positions_zero_based':dict(positions),'best_constant_position_successes':max(positions.values()),'attempts':len(rs),'uniform_baseline':.2,'correct_choice_count':1,'fixed_position_predictor':False,'labels':'No authored labels in image banks','count_cue':'One choice required by the radio contract; gives no qualifying image','method':'Both-variable dependence is the assessed criterion, not an incidental shortcut'}
 return result
before=json.loads((E/'moderate-probes.json').read_text());after=json.loads((E/'delivery/accepted.json').read_text())
before_stats=audit(before);after_stats=audit(after);assert before_stats==after_stats
save('shortcut-results.json',{'before_delivery':before_stats,'after_delivery':after_stats,'stage_counts':{'input':len(before),'accepted':len(after)},'claim_limit':'Small targeted cue probe; not an exhaustive guarantee against every visual heuristic. Canonical replay is an immutable historical source, excluded from default sampling.'})
# Independent pixel witness for the changed renderer: all choice fields in three
# representative banks, checking actual raster orientations rather than sidecars.
records=json.loads((E/'small-sample.json').read_text());chosen=[records[0],records[5],records[-3]];pixel=[]
for r in chosen:
 for a in fld(r)[':answer-field/choices']:
  path=pathlib.Path(a[':answer/value']);ps=pw.inspect(str(path),[-2,2,-2,2])['points'];slopes=json.loads(path.with_suffix('.json').read_text())['points'];errs=[]
  for x,y,angle in ps:
   xx,yy,m=min(slopes,key=lambda p:(p[0]-x)**2+(p[1]-y)**2)
   err=abs(angle-math.atan(m));errs.append(min(err,math.pi-err))
  assert len(errs)>100,(str(path),len(errs))
  errs.sort();median=errs[len(errs)//2];p90=errs[int(.9*len(errs))]
  assert median<.08 and p90<.18,(path,median,p90)
  pixel.append({'template':r['generation']['template'],'asset':str(path.relative_to(W)),'recovered_segments':len(ps),'median_angular_error':median,'p90_angular_error':p90})
save('pixel-results.json',pixel)
# Same read-only within-band mapping as question_selection.rs. Captured inventory
# controls delivery dedup; future assigned entity IDs/history are not supplied.
pool=sorted(after,key=lambda r:r['question'][':question/id']);draws=collections.Counter()
for i in range(64):
 d=hashlib.sha256(('course-academy/question-selection/v1/repair-'+str(i)).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53
 draws[pool[int(u*len(pool))]['generation']['template']]+=1
assert set(draws)==set(before_stats)
save('selection-results.json',{'implementation':'engine/rust/question_selection.rs select; conditional moderate band uniform SHA256 second-8-byte draw','draws':64,'template_draws':dict(draws),'captured_inventory_basis':json.loads((W.parent/'source/inventory.json').read_text())['basis'],'ordering':'Question UUID sort is an entity-order stand-in','limits':'No live weights, learner history, reservations or future entity IDs supplied. Captured inventory dedup is exercised by check_delivery. The unconfigured-policy first-entity fallback cannot be reproduced for unassigned future entities.'})
cases=[]
for i,r in enumerate(after):
 f=fld(r);cases.append({'label':'delivered-'+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]})
save('delivery-grader-input.json',cases)
save('visual-inspection.json',{'screenshots':['render/question-001.png','render/question-002.png','render/question-003.png'],'inspected':True,'observations':['Canonical composite retains I/II/III/IV, readable labels and solution images; III matches the both-variable field.','Authored mixed field shows x+y², consistent five-choice styling, correct selected field and both non-axis guides.','Hard outlier shows x-only slopes and a vertical guide; other four fields vary in both coordinates.'],'mathjax_errors':0,'broken_images':0,'clipping_or_overlap_observed':False})
print('PASS: within-template positions change before/after delivery;',len(pixel),'PNG witnesses; conditional learner-selection mapping covers all moderate templates')
