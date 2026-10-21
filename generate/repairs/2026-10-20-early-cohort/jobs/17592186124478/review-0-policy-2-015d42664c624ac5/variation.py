# Run after audit.py and the delivery/grader/renderer commands in commands.md.
import sys,json,pathlib,re,collections,math,hashlib,random
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT.parent/'workspace'))
import generator as g
save=lambda n,v:(ROOT/n).write_text(json.dumps(v,indent=2)+'\n')
load=lambda n:json.load(open(ROOT/n))
def features(r):
 q=r['question'];body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1];m=[[int(c.strip()) for c in row.split('&')] for row in body.split(r'\\')];ps=[next(j for j,x in enumerate(row) if x) for row in m if any(row)];n=len(m[0]);return {'id':q[':question/id'],'shape':str([len(m),n]),'cols':n,'label':re.search(r'matrix \$(\w)\$',q[':question/problem'])[1],'non':tuple(j+1 for j in range(n) if j not in ps),'zero':tuple(j+1 for j in range(n) if all(row[j]==0 for row in m)),'rank':len(ps)}
groups={n:[features(r) for r in load(p)] for n,p in [('structural','structural-samples.json'),('fresh_raw','fresh-samples.json'),('fresh_delivered','delivery-fresh/accepted.json'),('batch_raw','runner-batch.json'),('batch_delivered','delivery-batch/accepted.json')]}
measure={};probes=[]
for name,fs in groups.items():
 measure[name]={'count':len(fs),'shapes':dict(collections.Counter(f['shape'] for f in fs)),'answers':{str(k):v for k,v in collections.Counter(f['non'] for f in fs).items()},'selection_counts':dict(collections.Counter(len(f['non']) for f in fs))}
 subgroups=[('all',fs,'overall')]+[('shape '+s,[f for f in fs if f['shape']==s],'other_recognizable_subgroup') for s in sorted({f['shape'] for f in fs})]+[('label '+s,[f for f in fs if f['label']==s],'other_recognizable_subgroup') for s in sorted({f['label'] for f in fs})]
 for desc,sub,scope in subgroups:
  pick,count=collections.Counter(f['non'] for f in sub).most_common(1)[0];baseline=sum(1/(math.comb(f['cols'],f['rank'])) for f in sub)/len(sub)
  probes.append({'cue':'matrix dimensions or letter; no entries','subgroup':name+': '+desc,'scope':scope,'strategy':'Always select columns '+str(pick),'correct':count,'total':len(sub),'baseline':baseline,'disposition':'not_predictive','conclusion':'Baseline is uniform guessing among subsets of the true rank-complement size (generously giving the guesser the rank). Best fitted fixed subset is reported; singleton subgroups cannot establish a systematic cue. No subgroup with repeated cases is perfectly predicted by this fixed action.' if count<len(sub) or len(sub)==1 else 'All observed answers agree; compare structural controls before drawing a conclusion.','sample_refs':[{'structural':'structural-samples.json','fresh_raw':'fresh-samples.json','fresh_delivered':'delivery-fresh/accepted.json','batch_raw':'runner-batch.json','batch_delivered':'delivery-batch/accepted.json'}[name]]})
 # Zero columns are non-pivot by the assessed definition, not a label shortcut.
 success=sum(f['zero']==f['non'] for f in fs)
 probes.append({'cue':'all-zero column vectors','subgroup':name,'scope':'within_template','strategy':'Select exactly the all-zero columns','correct':success,'total':len(fs),'baseline':sum(1/math.comb(f['cols'],f['rank']) for f in fs)/len(fs),'disposition':'intended_skill','conclusion':'Zero columns cannot contain a pivot; identifying them is a valid simplification of this skill, explicitly represented by source q-130948. This action fails on nonzero non-pivot columns in the controls and batch. Baseline is uniform guessing at true complement size.','sample_refs':[{'structural':'structural-samples.json','fresh_raw':'fresh-samples.json','fresh_delivered':'delivery-fresh/accepted.json','batch_raw':'runner-batch.json','batch_delivered':'delivery-batch/accepted.json'}[name]]})
save('shortcut-results.json',{'measurements':measure,'probes':probes})
# Reproduce raw proposals and internal structural resampling for a maximal finite batch.
full=g.batch('easy',58,824031);save('maximal-batch.json',full);raw=[];seen=set()
for offset in range(5000):
 r=g.generate(seed=824031+offset);f=features(r);key=(f['shape'],f['non']);raw.append({'seed':824031+offset,'id':f['id'],'shape':f['shape'],'non':f['non'],'accepted':key not in seen});seen.add(key)
 if len(seen)==58:break
save('resampling-results.json',{'command':'g.batch("easy",58,824031)','raw_proposals':raw,'accepted_count':len(full),'distinct_structures':len(seen),'batch_features':[features(r) for r in full],'rule':'Reject only duplicate shape and pivot positions; every matrix has a nonempty complement so nonempty wrapper does not resample.','same_as_stream':[(f['shape'],f['non']) for f in map(features,full)]==[(r['shape'],tuple(r['non'])) for r in raw if r['accepted']]})
# Faithful read-only selection for captured easy-only inventory, including history exclusion.
inv=json.load(open(ROOT.parent/'source/inventory.json'));candidates=sorted(q[':db/id'] for q in inv['questions']);assert all(q[':question/difficulty'][':db/ident']==':question.difficulty/easy' for q in inv['questions'])
def select(ids,seed,weighted=True):
 ids=sorted(set(ids))
 if not ids:return None
 if not weighted:return ids[0]
 d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53;return ids[int(u*len(ids))]
trials=[]
for seen in [[],candidates[:1],candidates[:5],candidates]:
 pool=[q for q in candidates if q not in seen];draws=[select(pool,str(i)) for i in range(400)]
 trials.append({'seen':seen,'eligible':pool,'draw_counts':dict(collections.Counter(draws)),'all_eligible_reached':set(draws)==set(pool) if pool else draws==[None]*400,'unconfigured_first':select(pool,'0',False)})
save('selection-results.json',{'source':'engine/rust/question_selection.rs::select and seen_before_task','inventory_basis':inv['basis'],'candidates':candidates,'trials':trials,'difficulty':'All captured questions are easy; all easy candidates remain reachable for every configured distribution with positive easy weight, independent of moderate/hard weights. Zero easy weight with no unrated questions yields no question. Unconfigured policy picks the first remaining entity, not a random sample.','limits':['No learner-specific history or active policy supplied; tested representative exclusions and conditional easy-positive policy, not a live learner session.','Future generated records have no entity IDs until publication. Shared delivery preserves all sampled records; once assigned IDs the same easy-only within-band rule applies.']})
cf=load('math-results.json')['counterfactual'];save('counterfactual-results.json',{'base':cf[0],'relevant':cf[1],'irrelevant':cf[2],'relevant_expected':[2,4],'irrelevant_expected':[3,4],'relevant_passed':cf[0]['non']==[3,4] and cf[1]['non']==[2,4],'irrelevant_passed':cf[0]['non']==cf[2]['non'],'native_grader':'grader-results.json; pairs label checks exercise both actual UI actions for every column on each record','renderer':'render-pairs/rendering.json; before/after prompts and solutions must match these matrices and changed membership'})
print(json.dumps({'stage_counts':{n:v['count'] for n,v in measure.items()},'batch_answers':measure['batch_delivered']['answers'],'repeated_perfect_cues':[p['subgroup'] for p in probes if p['correct']==p['total'] and p['total']>1 and p['disposition']=='not_predictive'],'raw_proposals_to_58':len(raw),'selection_all_reached':all(t['all_eligible_reached'] for t in trials)}))
