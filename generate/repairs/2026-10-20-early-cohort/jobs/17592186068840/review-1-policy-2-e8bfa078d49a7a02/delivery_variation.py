"""Read-only distribution, shortcut and historical-inventory checks."""
import collections,hashlib,importlib.util,json,pathlib,sys
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;R=pathlib.Path('/home/jake/Developer/Course_Academy')
def load(p):return json.loads((E/p).read_text())
def save(p,x):(E/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
 f=field(r);return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def old_cue(v):return '^{2}' in v and 'C +' in v and (v.startswith(r'y=\sqrt[3]{C +') or v.startswith(r'y=\ln{\left(C +') or (v.startswith(r'y=\left(C +') and v.endswith('^{3}')))
def probes(rows,label):
 result=[]
 for n in sorted({r['generation']['template'] for r in rows}):
  part=[r for r in rows if r['generation']['template']==n]
  pos=collections.Counter(next(i for i,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==field(r)[':answer-field/correct'][1]) for r in part)
  old=[]
  for r in part:
   ch=[a for a in field(r)[':answer-field/choices'] if old_cue(a[':answer/value'])];old.append({'id':r['question'][':question/id'],'matching_shapes':len(ch),'success':len(ch)==1 and ch[0][':answer/value']==key(r)})
  # Lexicographic text choices and constant-position are independent of equation.
  eqblind=collections.Counter(key(r) for r in part)
  result.append({'template':n,'total':len(part),'correct_positions':dict(pos),'old_unique_plus_square_success':sum(x['success'] for x in old),'old_cue_cases':old,'first_option_success':pos[0],'lexicographic_first_success':sum(key(r)==min(a[':answer/value'] for a in field(r)[':answer-field/choices']) for r in part),'fixed_visible_answer_best_success':max(eqblind.values()),'distinct_keys':len(eqblind),'limitation':'Short batch subgroups of size one are descriptive and do not establish a universal predictor.'})
 return {'stage':label,'count':len(rows),'by_template':result,'counts':dict(collections.Counter(r['generation']['template'] for r in rows)),'signs':dict(collections.Counter('negative' if r['generation']['parameters']['a']<0 else 'positive' for r in rows))}
sets={'raw':load('independent-easy-current.json'),'delivered':load('delivery-independent/accepted.json'),'batch':load('batch-records.json'),'batch_delivered':load('delivery-batch/accepted.json')}
report={k:probes(v,k) for k,v in sets.items()}
# Controlled bank held exactly constant; each answer-bearing coefficient is possible.
groups=[]
for n in ['autonomous_tan','reciprocal_cube','negative_exp','cube_power','affine_root']:
 for stage in ['raw','delivered']:
  part=[r for r in sets[stage] if r['generation']['template']==n and r['generation']['seed']==82711]
  banks={tuple(sorted(a[':answer/value'] for a in field(r)[':answer-field/choices'])) for r in part}
  keys=collections.Counter(key(r) for r in part)
  groups.append({'template':n,'stage':stage,'records':len(part),'bank_sets':len(banks),'distinct_correct_candidates':len(keys),'fixed_answer_best_success':max(keys.values()) if keys else 0,'baseline':.2,'passed':len(part)==5 and len(banks)==1 and len(keys)==5})
assert all(t['passed'] for t in groups)
report['controlled_identical_banks']=groups;save('shortcut-results.json',report)
# Historical inventory reproduction uses frozen original implementation, not changed generator.
sp=importlib.util.spec_from_file_location('baseline',E/'baseline/17592186068840.py');oldg=importlib.util.module_from_spec(sp);sp.loader.exec_module(oldg)
original=load('generated-records.json');inv=json.loads((J/'source/inventory.json').read_text());by={q[':question/id']:q for q in inv['questions']};tested=[];records=[];affected=[]
for captured in original:
 m=captured['generation'];r=oldg.generate(captured['question'][':question/difficulty'].split('/')[-1],m['seed'],m['template'],parameters=m['parameters'],profile=m['bank_profile']);assert r==captured
 qid=r['question'][':question/id'];stored=by[qid];assert ':question/math-academy-id' not in stored
 assert all(stored[k]==r['question'][k] for k in [':question/problem',':question/worked-solution'])
 sf=stored[':question/answer-fields'][0];f=field(r)
 assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
 # Inventory key may be nested map; compare its visible correct family too.
 sc=sf[':answer-field/correct'];assert sc[':answer/value']==key(r)
 records.append(r);selected=[a for a in f[':answer-field/choices'] if old_cue(a[':answer/value'])];hit=len(selected)==1 and selected[0][':answer/value']==key(r)
 tested.append({'question_id':qid,'entity_id':stored[':db/id'],'all_content_and_generation_recipe_reproduced':True,'exact_historical_cue_success':hit})
 if hit:affected.append({'question_id':qid,'entity_id':stored[':db/id'],'finding':'Historical generated easy reciprocal-cube item is answerable by unique C + squared expression shape without inspecting ODE. Current revised coefficient-peer generator no longer exhibits that cue.','reproduction':str(R/'.venv/bin/python')+' -B delivery_variation.py; baseline generate('+repr(captured['question'][':question/difficulty'].split('/')[-1])+', '+str(m['seed'])+', '+repr(m['template'])+', parameters='+repr(m['parameters'])+', profile='+repr(m['bank_profile'])+')','evidence_path':'generated-records.json'})
save('generated-records.json',records);save('affected-inventory.json',{'affected_questions':affected});save('inventory-audit.json',{'basis':inv['basis'],'lineage':inv['lineage'],'captured_questions':len(inv['questions']),'tested_generated':tested,'source_question_count_excluded':sum(':question/math-academy-id' in q for q in inv['questions']),'affected':len(affected),'limits':'All six stored generated recipes reproduced. Exact retained easy shortcut demonstrated on one. Other five generated hard records tested only for this cue; not certified shortcut-free. No database changes requested or performed.'})
# Same selector source as preceding review; faithful easy-only selection reproduction.
sel=R/'engine/rust/question_selection.rs';oldsel=json.loads((J/'review-0-policy-2-f6d92a4daf8eee94/selection-analysis.json').read_text());sha=hashlib.sha256(sel.read_bytes()).hexdigest();assert sha==oldsel['source_sha256']
batch=sets['batch_delivered'];draws=[]
for i in range(40):
 seed='review-v1-selection-'+str(i);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);index=int(u*len(batch));r=batch[index]
 draws.append({'seed':seed,'synthetic_entity':index+1,'question_id':r['question'][':question/id'],'template':r['generation']['template'],'coefficient':r['generation']['parameters']['a']})
save('selection-analysis.json',{'source_file':str(sel),'source_sha256':sha,'unchanged_rules_reused_from':str(J/'review-0-policy-2-f6d92a4daf8eee94/selection-analysis.json'),'rules':oldsel['rules'],'capture_basis':inv['basis'],'distribution_assumption':'All prospective records easy. Positive easy weight selects uniformly within easy using SHA256 second draw; zero easy weight excludes them. Synthetic monotonic entity IDs used solely for reachability.','batch_stage_counts':{k:len(v) for k,v in sets.items()},'draws':draws,'reachable':sorted(set(x['synthetic_entity'] for x in draws)),'history_effect':'Seen/current-prefix exclusion can reduce coverage for a learner; selector has no answer-role preference or balancing. No mathematical/answer feature enters within-band selection.','limitations':['Live learner history, future entity IDs and policy weights unavailable; exact future learner distribution not predicted.','Publication preparation absent. Actual shared prepare_records run read-only against captured basis 5366.','Later changing inventory can change availability; claims bounded to captured inventory.']})
print(json.dumps({'controlled_bank_groups_passed':len(groups),'raw':len(sets['raw']),'delivered':len(sets['delivered']),'batch':len(batch),'inventory_affected':len(affected)}))
