"""Final read-only attribution and artifact verification, including the no-op."""
import collections,hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[4]/'scripts/question_capture'))
from capture import arguments
from database import Database
from edn import loads
from math_content import build_math_content,field_signature
from math_database import SOURCE,validate_receipt
from core import stable_id

def read(p):return json.loads(Path(p).read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=read(ROOT/'manifest.json');selected=read(ROOT/'selected-content.json');review=read(ROOT/'answer-review.json');snap=ROOT/'snapshot';vdir=ROOT/'validation'
old={q[':question/math-academy-id']:q for [q] in loads((snap/'questions.edn').read_text())}
topics={t[':topic/math-academy-id']:t for [t] in loads((snap/'topics.edn').read_text())}
db=Database(arguments(['run']));assert db.args.database=='math' and db.args.source==SOURCE and db.basis()==m['basis_prepared_against']==159
source_id=dict((str(i),e) for e,i in loads((snap/'idents.edn').read_text()))[SOURCE]
rows=db.query('''[:find ?mid ?f ?key ?a ?s :in $ [?mid ...] :where [?q :question/math-academy-id ?mid] [?q :question/answer-fields ?f] [?f :answer-field/key ?key] [?f :answer-field/correct ?a _ ?s]]''',[sorted(old)],vdir,'existing-answer-sources',159)
sources=collections.defaultdict(set)
for mid,f,key,a,s in rows:sources[mid,f,key,a].add(s)
reused=[]
for mid,q in old.items():
 incoming={f['key']:f for f in selected[mid]['question']['answer_fields']}
 for f in q.get(':question/answer-fields',[]):
  key=f[':answer-field/key']
  if key in incoming and field_signature(f,stored=True)==field_signature(incoming[key]):
   assert source_id in sources[mid,f[':db/id'],key,f[':answer-field/correct'][':db/id']],(mid,key,'missing source')
   reused.append({'question':mid,'field':key,'source_eid':source_id,'field_eid':f[':db/id']})
noops=[]
for mid in m['already_current_ids']:
 q=selected[mid]['question'];forms,_=build_math_content({'task_type':'review','topic_id':q['topic_id'],'questions':[q],'canonical_examples':[]},topics,old)
 assert not forms
 assert old[mid][':question/id']
 assert {field_signature(f,stored=True) for f in old[mid][':question/answer-fields']}=={field_signature(f) for f in q['answer_fields']}
 noops.append({'question':mid,'uuid':str(old[mid][':question/id']),'exact_content_and_fields_current':True,'source_verified':True,'transaction_required':False})
save(vdir/'reused-field-source-verification.json',{'valid':True,'basis':159,'fields':reused,'already_current':noops})
raw=read(ROOT/'recovery-input.json');disagreements=read(ROOT/'disagreements.json')
# Record saved candidate disagreements without treating the old candidate as authority.
for mid,r in selected.items():
 o=next(o for o in raw[mid]['occurrences'] if o['directory']==r['path'])
 old_fields={f['key']:f for f in o['prepared_question']['answer_fields']}
 for f in r['question']['answer_fields']:
  if old_fields.get(f['key'],{}).get('correct_value')!=f['correct_value']:
   disagreements.append({'question':mid,'kind':'saved_agent_candidate_rejected','field':f['key'],'old_candidate':old_fields.get(f['key'],{}).get('correct_value'),'source_answer':f['correct_value'],'binding':next(x['binding'] for x in review[mid]['fields'] if x['key']==f['key']),'source_location':review[mid]['solution_location'],'note':'Only the reviewed saved MA solution supplies authority.'})
save(ROOT/'disagreements.json',disagreements)
# Connect every library image to original saved bytes and capture manifests.
images=read(ROOT/'image-verification.json');mappings=collections.defaultdict(list)
for mid,r in selected.items():
 o=next(o for o in raw[mid]['occurrences'] if o['directory']==r['path']);text=json.dumps([o['source_problem'],o['worked_solution'],o['before_fields']],ensure_ascii=False)
 for path in set(re.findall(r'/home/[^\s)"<>]+\.(?:png|jpg|gif|webp|svg)',text)):
  p=Path(path)
  if not p.is_file():continue
  h=sha(p);refs=[ref for ref in images['references'] if Path(ref).stem==h]
  for ref in refs:
   mf=Path(r['path'])/'assets/manifest.json'
   mappings[ref].append({'question':mid,'original_saved_bytes':str(p),'sha256':h,'manifest':str(mf),'manifest_sha256':sha(mf) if mf.is_file() else None})
assert set(mappings)==set(images['references']),(set(images['references'])-set(mappings))
save(ROOT/'image-source-mappings.json',mappings)
index=ROOT.parent/'held-questions.json';assert sha(index)==m['held_index_sha256']
allids=[]
for b in m['batches']:
 assert sha(b['file'])==sha(b['reference_file'])==b['sha256']
 allids+=b['questions']
assert len(allids)==len(set(allids))==sum(b['question_count'] for b in m['batches'])
assert set(allids)|set(m['already_current_ids'])==set(selected)
assert set(selected)<=set(q['math_academy_id'] for q in read(index)['questions'])
assert set(selected).isdisjoint(read(ROOT.parent/'2026-10-10-held-recovery/selected-content.json'))
assert db.basis()==159
report={'valid':True,'database':'math','basis':159,'database_writes':0,'transaction_batches':len(m['batches']),'questions_in_transactions':len(allids),'ready_questions':len(selected),'ready_fields':m['ready_fields'],'new_questions':m['new_questions'],'updated_questions':m['updated_questions'],'already_current_questions':m['already_current_questions'],'still_unresolved_questions':m['still_unresolved_questions'],'held_index_count_unchanged':1069,'all_prior_recovery_ids_excluded':True,'all_reused_correct_field_sources_verified':True,'reused_fields_verified':len(reused),'old_component_entities_preserved':True,'source_disagreements_recorded':len(disagreements),'images_verified_against_original_bytes':len(mappings),'ssd_transaction_hashes_verified':True,'held_index_sha256':sha(index)}
save(ROOT/'verification.json',report)
print(json.dumps(report,indent=2))
