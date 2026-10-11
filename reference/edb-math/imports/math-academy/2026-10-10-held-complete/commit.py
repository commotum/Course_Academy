"""Commit fully reviewed remaining questions authorized by the user.

Uses frozen hashes, basis guards, durable request keys and exact retry intents.
The held index is changed only after committed readback verification succeeds.
"""
import collections,hashlib,json,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[4]/'scripts/question_capture'))
from capture import arguments
from database import Database,TOPIC_QUERY
from core import atomic_json,stable_id
from edn import dumps,loads,kw
from math_content import build_math_content,field_signature
from math_database import SOURCE,validate_receipt

def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest=read(ROOT/'manifest.json');selected=read(ROOT/'selected-content.json');SNAP=ROOT/'snapshot';index=ROOT.parent/'held-questions.json'
old={q[':question/math-academy-id']:q for [q] in loads((SNAP/'questions.edn').read_text())}
attributes=loads((SNAP/'attributes.edn').read_text());source_id=dict((str(i),e) for e,i in loads((SNAP/'idents.edn').read_text()))[SOURCE]
db=Database(arguments(['run']));assert db.args.database=='math' and db.args.source==SOURCE
basis=manifest['basis_prepared_against'];assert basis==165
end_basis=basis+len(manifest['batches'])
assert read(ROOT/'verification.json')['valid'] and read(ROOT/'preview-verification.json')['valid']
for batch in manifest['batches']:
 assert sha(batch['file'])==sha(batch['reference_file'])==batch['sha256']
assert sha(index)==manifest['held_index_sha256'] or read(index).get('resolved_by_held_complete',{}).get('basis_after')==end_basis
for ref,info in read(ROOT/'image-verification.json')['references'].items():assert sha(Path(db.args.math_root)/ref)==info['sha256']

def verify_content(ids,basis,directory):
 directory.mkdir(parents=True,exist_ok=True)
 current=db.questions(ids,directory,basis=basis)
 tids=sorted({selected[m]['question']['topic_id'] for m in ids})
 topics={t[':topic/math-academy-id']:t for [t] in db.query(TOPIC_QUERY.replace(':in $ ?id',':in $ [?id ...]'),[tids],directory,'topics',basis)}
 rows=db.query('''[:find ?mid ?key ?s :in $ [?mid ...] :where [?q :question/math-academy-id ?mid] [?q :question/answer-fields ?f] [?f :answer-field/key ?key] [?f :answer-field/correct ?a _ ?s]]''',[ids],directory,'answer-sources',basis)
 sources=collections.defaultdict(set)
 for mid,key,s in rows:sources[mid,key].add(s)
 reports=[]
 for mid in ids:
  q=selected[mid]['question'];found=current[mid];previous=old.get(mid,{})
  assert found[':question/id']==(previous.get(':question/id') or stable_id('question',mid)),(mid,'UUID')
  for key,attr in [('problem',':question/problem'),('worked_solution',':question/worked-solution')]:assert found[attr]==q[key],(mid,key)
  assert {f[':answer-field/key']:field_signature(f,stored=True) for f in found[':question/answer-fields']}=={f['key']:field_signature(f) for f in q['answer_fields']},(mid,'fields')
  assert len(found[':question/answer-fields'])==len(q['answer_fields'])
  owners={str(p[':knowledge-point/id']) for p in found.get(':knowledge-point/_questions',[])}
  assert owners=={q['knowledge_point_id']} and not found.get(':knowledge-point/_canonical-example'),(mid,'KP')
  for f in q['answer_fields']:assert source_id in sources[mid,f['key']],(mid,'source',f['key'])
  forms,_=build_math_content({'task_type':'review','topic_id':q['topic_id'],'questions':[q],'canonical_examples':[]},topics,current)
  assert not forms,(mid,'reimport must be a no-op')
  reports.append({'question':mid,'uuid':str(found[':question/id']),'fields':len(q['answer_fields']),'exact_content':True,'source_verified':True,'KP_verified':True,'reimport_noop':True})
 atomic_json(directory/'verification.json',{'verified':True,'basis':basis,'questions':reports})
 return reports

results=[];connection_hash=hashlib.sha256(db.env['EDB_POSTGRES_URL'].encode()).hexdigest()
for i,b in enumerate(manifest['batches']):
 path=Path(b['file']);directory=ROOT/'commits'/path.stem;directory.mkdir(parents=True,exist_ok=True);before=basis+i
 guard=ROOT/'validation'/(path.name+'.guards.edn');guards=loads(guard.read_text())
 intent={'database':'math','endpoint':db.args.endpoint,'source':SOURCE,'source_eid':source_id,'basis':before,'file':str(path),'sha256':b['sha256'],'connection_sha256':connection_hash,'reconciliation_sha256':sha(guard),'request_key':'ma-held-complete-2026-10-10-'+str(before)+'-'+b['sha256']}
 saved=directory/'commit-intent.json'
 if saved.exists():assert read(saved)==intent
 else:
  assert db.basis()==before,('Database advanced; do not replay a stale plan',db.basis(),before)
  text=db.command('with','--file',path,'--source',SOURCE);receipt=loads(text)
  assert receipt[':edb/db-before-t']==before
  validate_receipt(receipt,attributes,source_id,guards['retractions'],guards['immutable_answers'],guards['immutable_fields'])
  (directory/'preview.edn').write_text(text);atomic_json(saved,intent)
 receipt=db._commit(intent,path,directory)
 assert receipt[':edb/committed'] is True and receipt[':edb/db-before-t']==before and receipt[':edb/db-after-t']==before+1
 validate_receipt(receipt,attributes,source_id,guards['retractions'],guards['immutable_answers'],guards['immutable_fields'])
 verify_content(b['questions'],before+1,directory/'readback')
 result={'file':str(path),'sha256':b['sha256'],'basis_before':before,'basis_after':before+1,'source':SOURCE,'committed':True,'verified':True,'questions':len(b['questions']),'datoms':len(receipt[':edb/tx-data']),'retractions':sum(not d[-1] for d in receipt[':edb/tx-data'])}
 atomic_json(directory/'verification.json',result);results.append(result)
 atomic_json(ROOT/'commit-verification.json',{'all_batches_committed':len(results)==len(manifest['batches']),'basis_before':basis,'basis_after':before+1,'source':SOURCE,'batches':results})
 print(json.dumps(result),flush=True)
assert db.basis()==end_basis
all_reports=verify_content(sorted(selected),end_basis,ROOT/'readback')
# Retained component entities are still exactly their old definitions.
component_ids=sorted({e for q in old.values() for f in q.get(':question/answer-fields',[]) for e in [f[':db/id']]+[a[':db/id'] for a in f.get(':answer-field/choices',[])]})
query='[:find ?e ?a ?v ?s :in $ [?e ...] :where [?e ?a ?v _ ?s]]'
prior=db.query(query,[component_ids],ROOT/'readback','old-components-before',basis)
current=db.query(query,[component_ids],ROOT/'readback','old-components-after',end_basis)
assert {dumps(r) for r in prior}=={dumps(r) for r in current}
# Every changed question/component belongs to the prepared set. Content only.
allowed_questions={q[':db/id'] for [q] in loads((ROOT/'readback/questions.edn').read_text())}
allowed_fields={f[':db/id'] for [q] in loads((ROOT/'readback/questions.edn').read_text()) for f in q[':question/answer-fields']}
allowed_answers={a[':db/id'] for [q] in loads((ROOT/'readback/questions.edn').read_text()) for f in q[':question/answer-fields'] for a in f[':answer-field/choices']}
names={a:str(n) for a,n in attributes}
for b in manifest['batches']:
 receipt=loads((ROOT/'commits'/Path(b['file']).stem/'commit.edn').read_text())
 for e,a,v,t,s,added in receipt[':edb/tx-data']:
  name=names[a];assert s==source_id
  if name.startswith(':question/'):assert e in allowed_questions
  elif name.startswith(':answer-field/'):assert e in allowed_fields
  elif name.startswith(':answer/'):assert e in allowed_answers
  elif name==':knowledge-point/questions':assert v in allowed_questions
  else:assert name==':db/txInstant',name
verification={'verified':True,'database':'math','source':SOURCE,'basis_before':basis,'basis_after':end_basis,'questions_verified':len(all_reports),'fields_verified':sum(r['fields'] for r in all_reports),'new_questions':manifest['new_questions'],'updated_questions':manifest['updated_questions'],'already_current_questions':manifest['already_current_questions'],'all_reimports_noop':True,'old_component_entities_preserved':len(component_ids),'old_component_facts_preserved':len(prior),'remaining_held_untouched_by_receipts':True,'receipt_retractions_verified':sum(x['retractions'] for x in results)}
atomic_json(ROOT/'committed-content-verification.json',verification)
manifest.update(transacted=True,verified=True,basis_after=end_basis,database_writes=len(manifest['batches']),committed_content_verification=str(ROOT/'committed-content-verification.json'))
atomic_json(ROOT/'manifest.json',manifest)
# Update only after every committed item is verified.
d=read(index)
if not d.get('resolved_by_held_complete'):
 assert sha(index)==manifest['held_index_sha256']
 (ROOT/'held-index-before-commit.json').write_bytes(index.read_bytes())
 d['questions']=[q for q in d['questions'] if q['math_academy_id'] not in selected]
 assert len(d['questions'])==manifest['still_unresolved_questions']
 old_ids={q['math_academy_id'] for q in d['questions'] if any(h['import']=='newer-captures' for h in q['holds'])}
 latest={q['math_academy_id'] for q in d['questions'] if any(h['import']=='2026-10-10-pre-refactor' for h in q['holds'])}
 d['counts'].update(previous_held_remaining=len(old_ids),latest_held=len(latest),overlap_remaining=len(old_ids&latest),latest_only=len(latest-old_ids),unique_held_questions=len(d['questions']),resolved_by_held_complete=len(selected))
 d['database_basis_reviewed']=end_basis;d['updated_at']=datetime.now(timezone.utc).isoformat()
 d['resolved_by_held_complete']={'source':SOURCE,'basis_after':end_basis,'manifest':str(ROOT/'manifest.json'),'verification':str(ROOT/'committed-content-verification.json'),'question_ids':sorted(selected)}
 rows=read(ROOT.parent/'2026-10-10-held-next/remaining-analysis/questions.json')
 remaining={q['math_academy_id']:rows[q['math_academy_id']] for q in d['questions']}
 counts=collections.Counter(r['category'] for r in remaining.values())
 d['remaining_pattern_counts']={'radio_mixed_prose_and_math':counts['text_choice_with_embedded_math'],'radio_prose_only':counts['prose_choice_requires_statement_matching'],'radio_complete_formula_needs_answer_binding':counts['math_candidate_literal_present_but_not_bound_to_answer'],'radio_other_math_matching':counts['math_candidate_requires_representation_or_conclusion_review'],'select_questions':counts['select_field_binding'],'select_questions_needing_one_field':sum(len(r.get('unconfirmed_fields',[]))==1 for r in remaining.values()),'select_questions_needing_multiple_fields':sum(len(r.get('unconfirmed_fields',[]))>1 for r in remaining.values()),'select_unconfirmed_fields':sum(len(r.get('unconfirmed_fields',[])) for r in remaining.values()),'select_questions_with_normalized_prompt_placement_gaps':0,'radio_set_brace_normalization_ambiguity':0}
 d['remaining_analysis']={'basis':end_basis,'questions':str(ROOT/'remaining-questions.json'),'summary':str(ROOT/'remaining-summary.json'),'previous_detailed_report':str(ROOT.parent/'2026-10-10-held-next/remaining-analysis/REPORT.txt'),'note':'Current IDs only; older report is historical.'}
 atomic_json(ROOT/'remaining-questions.json',remaining)
 atomic_json(ROOT/'remaining-summary.json',{'basis':end_basis,'held':len(remaining),'patterns':d['remaining_pattern_counts']})
 d['status_note']=f'All 839 previously held questions were individually reviewed. {len(selected)} additional source-supported questions verified at basis {end_basis}; remaining IDs have explicit per-question content-error, ambiguity, or authoritative-evidence findings in held-review.json.'
 holds=read(ROOT/'held-review.json')
 for question in d['questions']:
  mid=question['math_academy_id'];finding=holds[mid]
  question['current_review']={'source':SOURCE,'basis':end_basis,'reason':finding['hold_reason'],'explanation':finding['explanation'],'evidence_file':str(ROOT/'held-review.json')}
 d['remaining_content_reason_counts']=dict(collections.Counter(h['hold_reason'] for h in holds.values()))
 atomic_json(index,d)
assert len(read(index)['questions'])==manifest['still_unresolved_questions'] and set(q['math_academy_id'] for q in read(index)['questions']).isdisjoint(selected)
atomic_json(ROOT/'held-index-update-verification.json',{'verified':True,'basis':end_basis,'before':839,'removed_verified_ids':len(selected),'remaining':len(read(index)['questions']),'index_sha256':sha(index)})
manifest['held_index_unchanged_during_preparation']=manifest.pop('held_index_unchanged',True)
manifest.update(held_index_updated_after_verified_commit=True,held_index_remaining=manifest['still_unresolved_questions'],commit_note='All numbered transaction batches committed and read back; already-current questions verified without writes; only verified resolved IDs removed from held index.')
atomic_json(ROOT/'manifest.json',manifest)
print('COMMITTED, VERIFIED, AND INDEX UPDATED',json.dumps(verification),flush=True)
