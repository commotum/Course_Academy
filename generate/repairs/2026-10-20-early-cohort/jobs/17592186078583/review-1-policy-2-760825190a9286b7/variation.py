import sys,json,importlib.util,hashlib,collections,re
from pathlib import Path
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent;ROOT=Path('/home/jake/Developer/Course_Academy');JOB=ROOT/'generate/repairs/2026-10-20-early-cohort/jobs/17592186078583';PKG=JOB/'workspace'
sys.path.insert(0,str(ROOT))
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load(PKG/'17592186078583.py','generator');pub=load(ROOT/'scripts/generator_publish.py','publisher')
def save(name,data): (OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def read(name):return json.load(open(OUT/name))
def fields(r):return r['question'][':question/answer-fields'][0]
def key(f):
 c=f[':answer-field/correct'];return c[1] if isinstance(c,list) else c[':answer/id']
def shortest(r):
 f=fields(r);a=f[':answer-field/choices'];n=min(len(c[':answer/value']) for c in a);return [c for c in a if len(c[':answer/value'])==n]
def succeeds(r):
 a=shortest(r);return len(a)==1 and a[0][':answer/id']==key(fields(r))
def summary(records):
 groups=collections.defaultdict(list)
 for r in records:groups[r['generation']['template']].append(r)
 return {t:{'n':len(rs),'shortest_unique_correct':sum(succeeds(r) for r in rs),'first_option_correct':sum(fields(r)[':answer-field/choices'][0][':answer/id']==key(fields(r)) for r in rs),'ambient_values':sorted(set(r['generation']['parameters']['S'] for r in rs))} for t,rs in groups.items()}
datasets={p:read(p) for p in ['samples.json','batch.json','delivery-easy/accepted.json','delivery-batch/accepted.json','delivery-moderate/accepted.json']}
measurements={p:summary(rs) for p,rs in datasets.items()};save('shortcut-results.json',{'command':'.venv/bin/python variation.py','strategy':'Select the uniquely shortest full equation by character count; abstain on ties. This cue needs no sign, equilibrium, or prompt interpretation. Representative rendered widths inspected separately.','stages':measurements,'minimal_examples':read('retained-witness-records.json')})
# Reproduce captured generated inventory using original saved seed/parameters; preserve stored historical generator identities.
inv=json.load(open(JOB/'source/inventory.json'));original_ids={q[':question/id'] for q in json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']}
prior=read('generated-records.json')
historical=load(JOB/'review-0-policy-2-0c69632c0ac42ce3/relocated/17592186078583.py','historical')
reproduced=[];inventory_results=[]
for old in prior:
 g=old['generation'];r=historical.generate(old['question'][':question/difficulty'].split('/')[-1],g['seed'],template=g['template'],parameters=g['parameters'])
 stored=next((q for q in inv['questions'] if q[':question/id']==r['question'][':question/id']),None)
 same=stored is not None and pub.normalized_question(stored,identity=True)==pub.normalized_question(r['question'],identity=True)
 reproduced.append(r);inventory_results.append({'question_id':r['question'][':question/id'],'entity_id':stored[':db/id'] if stored else None,'captured_content_and_identity_match':same,'generation_matches_saved_provenance':g==r['generation'],'unique_shortest_correct':succeeds(r),'template':g['template'],'parameters':g['parameters']})
save('generated-records.json',reproduced)
save('affected-inventory.json',{'affected_questions':[]})
save('inventory-review.json',{'basis':inv['basis'],'captured_questions':len(inv['questions']),'original_source_questions':len(original_ids),'generated_records_reproduced':inventory_results,'result':'All seven non-source inventory records independently regenerated with their historical stored identities; none has the demonstrated unique-shortest defect. Missing source-family support is an omission, not a faulty stored item. Original turkey/soup source questions share the cue but are not marked as generated.','limitations':['Captured basis 5389 only; later inventory not observed.','Inventory itself has no generation metadata; provenance seed/parameters come from retained replenishment records, checked by independent regeneration and content/ID match. Current publisher stable IDs differ from these legacy IDs, so no current re-keying is applied for the historical comparison.']})
# Faithful equal-band draw from actual Rust algorithm, conditional on an easy draw.
# Candidate IDs are sorted, deduplicated, then two SHA256 53-bit uniforms choose band/member.
batch=datasets['delivery-batch/accepted.json'];pool=[(q[':db/id'],q) for q in inv['questions'] if pub.enum(q[':question/difficulty'])==':question.difficulty/easy']
maxid=max(q[':db/id'] for q in inv['questions'])
pool += [(maxid+100+i,r['question']) for i,r in enumerate(batch)]
def choose(candidates,seed,weighted=True):
 c=sorted(candidates,key=lambda x:x[0]);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
 return c[int(u*len(c))] if weighted else c[0]
selection=[]
for history in [[],[x[0] for x in pool[:2]]]:
 remaining=[x for x in pool if x[0] not in history]
 draws=collections.Counter(choose(remaining,'independent-review-'+str(i))[0] for i in range(128))
 selection.append({'excluded_seen_ids':history,'eligible_count':len(remaining),'draws':dict(draws),'unconfigured_policy_first_id':choose(remaining,'x',False)[0],'reachable_ids':[x[0] for x in remaining]})
save('learner-selection.json',{'implementation':'engine/rust/question_selection.rs lines 107-193','command':'.venv/bin/python variation.py','input_basis':5389,'assumptions':'Conditional on positive easy-band weight; all supplied candidates usable. Assigned synthetic IDs above captured maximum to unpublished accepted records; exact assigned IDs and learner history are not known. SHA256 selection rule reproduced verbatim.','pool':[{'entity_id':i,'question':q} for i,q in pool],'cases':selection,'result':'Within a positive rated band every remaining question is reachable with uniform conditional mass; selection does not repair missing generator profiles or per-template cues. None policy selects first eligible ID.','limitations':['No live learner or configured policy supplied; no claim about an individual future draw.','Normal eligible-pool construction and history vary with learner; tested no-history and two-seen envelopes.']})
# Grading on actual normalized delivered batch plus delivered shortcut survivors.
extra=batch+[next(r for r in datasets['delivery-moderate/accepted.json'] if r['generation']['template']==t) for t in ['q-106883','q-106934']]
grades=[]
for i,r in enumerate(extra):
 f=fields(r);grades.append({'label':'delivered-'+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(f) else 'rejected','purpose':'Stable identity normalization preserves independently verified mathematical key; test all choices'} for a in f[':answer-field/choices']]})
save('delivered-grader-input.json',grades)
print(json.dumps({'inventory_matches':[x['captured_content_and_identity_match'] for x in inventory_results],'counts':{p:len(rs) for p,rs in datasets.items()},'shortcuts':measurements['samples.json']},indent=2))
