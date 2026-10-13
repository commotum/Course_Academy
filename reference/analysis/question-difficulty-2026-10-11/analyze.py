"""Compare the captured source appearances with one immutable EDB snapshot."""
from pathlib import Path
import sys, json, collections, csv, html
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import loads
BANDS=['easy','moderate','hard']
def read(name):return loads((OUT/(name+'.edn')).read_text())
def csv_write(name,rows):
 if not rows:return
 with (OUT/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def dist(ds):
 c=collections.Counter(ds);n=sum(c[b] for b in BANDS)
 return {'n':n,'counts':{b:c[b] for b in BANDS},'percent':{b:100*c[b]/n if n else None for b in BANDS}}
allq=set(read('questions')); ids=dict(read('question-identifiers')); diff={e:str(d).split('/')[-1] for e,d in read('question-difficulties')}
assert set(diff).issubset(allq) and set(diff.values())<=set(BANDS)
assert all(ids.get(e,'').startswith('q-') for e in diff)
qbyid={ids[e]:e for e in diff}
tasks={x['task_id']:x for x in json.loads((OUT/'source-tasks.json').read_text())}
raw=[json.loads(line) for line in (OUT/'source-appearances.jsonl').open()]
qrows=collections.defaultdict(list); appearances=[]; conflicts=[]
for row in raw:
 mid=row['question_mid']
 if mid not in qbyid:continue
 row=dict(row);row['entity_id']=qbyid[mid];row['database_difficulty']=diff[row['entity_id']]
 if row['source_difficulty'] and row['source_difficulty']!=row['database_difficulty']:conflicts.append(row)
 if row['activity_type'] in ('lesson','review') and row['position_in_sequence']:
  cutoff=2 if row['activity_type']=='lesson' else 3
  row['phase']='initial' if row['position_in_sequence']<=cutoff else 'additional'
 else:row['phase']='unclassified' if row['activity_type'] in ('lesson','review') else 'fixed'
 qrows[mid].append(row);appearances.append(row)
missing=sorted(set(qbyid)-set(qrows))
unique=[]
for mid,e in sorted(qbyid.items()):
 rs=qrows[mid];types=sorted({r['activity_type'] for r in rs})
 unique.append({'question_mid':mid,'entity_id':e,'difficulty':diff[e],'source_types':';'.join(types) or 'unknown','source_task_count':len({r['task_id'] for r in rs}),'source_streams':';'.join(sorted({r['stream'] for r in rs})),'source_files':';'.join(sorted({r['source_file'] for r in rs}))})
csv_write('rated-questions.csv',unique);csv_write('rated-appearances.csv',appearances)
unique_types={t:dist(r['difficulty'] for r in unique if t in r['source_types'].split(';')) for t in ['lesson','review','assessment','multistep','diagnostic','unknown']}
exclusive={t:dist(r['difficulty'] for r in unique if r['source_types']==t) for t in sorted({r['source_types'] for r in unique})}
phase_stats={}; phase_rows=[];completed=[r for r in appearances if r['complete']]
for stream in ['all','older-automated','recent-automated','human-history','manual-capture']:
 for typ in ['lesson','review','assessment','multistep','diagnostic']:
  for phase in (['all','initial','additional','unclassified'] if typ in ('lesson','review') else ['all']):
   selected=[r for r in completed if (stream=='all' or r['stream']==stream) and r['activity_type']==typ and (phase=='all' or r['phase']==phase)]
   stat=dist(r['database_difficulty'] for r in selected)
   stat['task_count']=len({r['task_id'] for r in selected});stat['sequence_count']=len({(r['task_id'],r['kp_key'] if typ=='lesson' else 'whole-task') for r in selected})
   if not stat['n']:continue
   key=f'{stream}/{typ}/{phase}';phase_stats[key]=stat
   phase_rows.append({'stream':stream,'activity_type':typ,'phase':phase,'questions':stat['n'],'tasks':stat['task_count'],'sequences':stat['sequence_count'],**{b+'_count':stat['counts'][b] for b in BANDS},**{b+'_percent':stat['percent'][b] for b in BANDS}})
csv_write('phase-distributions.csv',phase_rows)
policy=read('policy')[0][0]
weights={}
for child in policy[':policy/question-selection-weights']:
 typ=str(child[':question-weights/activity-type'][':db/ident']).split('/')[-1]
 for phase in ['initial','remedial']:
  weights[f'{typ}/{phase}']={b:child[f':question-weights/{phase}-{b}'] for b in BANDS}
# Source sequence coverage: missing imported questions must not shorten a sequence.
full_sequences=collections.defaultdict(list)
for r in raw:
 if r['complete'] and r['activity_type'] in ('lesson','review'):
  key=(r['task_id'],r['kp_key'] if r['activity_type']=='lesson' else 'whole-task');full_sequences[key].append(r)
sequence_audit=[]
for (tid,kp),rs in full_sequences.items():
 typ=rs[0]['activity_type'];cutoff=2 if typ=='lesson' else 3
 sequence_audit.append({'task_id':tid,'type':typ,'stream':rs[0]['stream'],'kp':kp,'source_questions':len(rs),'rated_database_questions':sum(r['question_mid'] in qbyid for r in rs),'missing_rated_database_questions':sum(r['question_mid'] not in qbyid for r in rs),'has_position':all(r['position_in_sequence'] for r in rs),'initial_slots_covered':sum(r['position_in_sequence'] is not None and r['position_in_sequence']<=cutoff and r['question_mid'] in qbyid for r in rs)})
csv_write('sequence-coverage.csv',sequence_audit)
# KP bank coverage uses current rated membership, not assumptions about MA's full bank.
kpq=collections.defaultdict(set);qkp=collections.defaultdict(set)
for kp,q in read('knowledge-questions'):
 if q in diff:kpq[kp].add(q);qkp[q].add(kp)
topics={e:(tid,title) for e,tid,title in read('topics')};kptopic={kp:topics.get(t,('', '')) for t,kp in read('knowledge-point-topics')}
kprows=[]
for kp,qs in sorted(kpq.items()):
 stat=dist(diff[q] for q in qs);tid,title=kptopic.get(kp,('',''))
 kprows.append({'knowledge_point_entity':kp,'topic_mid':tid,'topic_title':title,'rated_questions':len(qs),'available_bands':';'.join(b for b in BANDS if stat['counts'][b]),**{b+'_count':stat['counts'][b] for b in BANDS}})
csv_write('knowledge-point-banks.csv',kprows)
kp_band_counts=dict(collections.Counter(r['available_bands'] for r in kprows))
# Resolve direct activity structures locally. Shared KP membership does not establish task origin.
step_content=dict(read('step-content'));multi=collections.defaultdict(list)
for m,s in read('multistep-steps'):multi[m].append(step_content[s])
assigned=dict(read('assigned-content'));act={a:str(typ).split('/')[-1] for a,_,_,typ in read('activities')}
def expand(e,seen=None):
 seen=set() if seen is None else seen
 if e in seen:return set()
 seen.add(e)
 if e in diff:return {e}
 if e in assigned:return expand(assigned[e],seen)
 return set().union(*(expand(c,seen) for c in multi.get(e,[])))
direct=collections.defaultdict(set)
for a,s in read('activity-steps'):
 for q in expand(step_content[s]):direct[q].add(act[a])
canonical={q for kp,q in read('canonical-questions')}
summary={'snapshot':json.loads((OUT/'snapshot.json').read_text()),'question_count':len(allq),'rated_question_count':len(diff),'unrated_question_count':len(allq)-len(diff),'all_rated_distribution':dist(diff.values()),'source_classified_questions':len(qrows),'missing_source_questions':missing,'source_difficulty_conflicts':len(conflicts),'multi_type_questions':sum(';' in r['source_types'] for r in unique),'all_source_tasks':len(tasks),'rated_source_tasks':len({r['task_id'] for r in appearances}),'rated_completed_tasks':len({r['task_id'] for r in completed}),'rated_appearances':len(appearances),'rated_completed_appearances':len(completed),'unique_by_source_type':unique_types,'exclusive_source_combinations':exclusive,'phase_distributions':phase_stats,'engine_weights':weights,'knowledge_point_bank_count':len(kprows),'knowledge_point_band_availability':kp_band_counts,'rated_without_kp_membership':len(set(diff)-set(qkp)),'rated_canonical_examples':len(set(diff)&canonical),'direct_activity_question_count':len(direct),'direct_activity_types':dict(collections.Counter(t for ts in direct.values() for t in ts)),'source_task_links_in_database':len(read('question-task-links')),'sequence_coverage':{'sequences':len(sequence_audit),'missing_question_sequences':sum(s['missing_rated_database_questions']>0 for s in sequence_audit),'missing_positions':sum(not s['has_position'] for s in sequence_audit)}}
good_sequences={(r['task_id'],r['kp']) for r in sequence_audit if not r['missing_rated_database_questions'] and r['has_position']}
summary['complete_sequence_sensitivity']={}
for typ in ['lesson','review']:
 for phase in ['initial','additional']:
  subset=[r for r in completed if r['activity_type']==typ and r['phase']==phase and (r['task_id'],r['kp_key'] if typ=='lesson' else 'whole-task') in good_sequences]
  summary['complete_sequence_sensitivity'][typ+'/'+phase]=dist(r['database_difficulty'] for r in subset)
assert not missing and not conflicts
assert sum(x['n'] for x in exclusive.values())==len(diff)
assert len({(r['task_id'],r['question_mid']) for r in appearances})==len(appearances)
assert sum(phase_stats['all/'+typ+'/all']['n'] for typ in ['lesson','review','assessment','multistep','diagnostic'])==len(completed)
# Availability is an illustration, not a live eligibility or MA probability model.
topic_banks=collections.defaultdict(set)
for kp,qs in kpq.items():topic_banks[str(kptopic.get(kp,('', ''))[0])].update(qs)
rated_sequences=collections.defaultdict(list)
for r in completed:
 if r['activity_type'] in ('lesson','review'):
  rated_sequences[r['task_id'],r['kp_key'] if r['activity_type']=='lesson' else 'whole-task'].append(r)
availability={}
for _,seq in rated_sequences.items():
 seen=set()
 for r in sorted(seq,key=lambda x:x['task_position']):
  q=r['entity_id'];typ=r['activity_type'];phase='initial' if r['phase']=='initial' else 'remedial'
  bank=set().union(*(kpq[kp] for kp in qkp[q])) if typ=='lesson' else topic_banks[str(tasks[r['task_id']].get('topic_id'))]
  candidates=bank-seen;seen.add(q);bands={diff[x] for x in candidates};w=weights[typ+'/'+phase];total=sum(w[b] for b in bands)
  stat=availability.setdefault(typ+'/'+phase,{'slots':0,'no_positive_rated_band':0,'sum':collections.Counter(),'band_mix':collections.Counter()})
  stat['band_mix'][';'.join(sorted(bands))]+=1
  if total:
   stat['slots']+=1
   for b in BANDS:stat['sum'][b]+=100*w[b]/total if b in bands else 0
  else:stat['no_positive_rated_band']+=1
for v in availability.values():
 v['percent']={b:v['sum'][b]/v['slots'] for b in BANDS};v['sum']=dict(v['sum']);v['band_mix']=dict(v['band_mix'])
(OUT/'availability-illustration.json').write_text(json.dumps(availability,indent=2)+'\n')
(OUT/'missing-source-ids.json').write_text(json.dumps(missing)+'\n')
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['phase_distributions','exclusive_source_combinations']},indent=2))
for row in phase_rows:print(row)
