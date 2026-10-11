"""Prepare and speculatively validate the reviewed batch. No commit path exists."""
import collections,copy,hashlib,json,re,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[4]
sys.path.insert(0,str(REPO/'scripts/question_capture'))
from capture import arguments
from database import Database,TOPIC_QUERY
from edn import dumps,loads,kw
from core import stable_id
from math_content import resolve_knowledge_points,build_math_content
from math_database import SOURCE,validate_receipt
from image_library import ImageLibrary,image_format
from bs4 import BeautifulSoup
class PreviewDatabase(Database):
 def command(self,command,*options):
  if command not in {'status','query','with'}:raise RuntimeError('This pass forbids durable transactions: '+command)
  return super().command(command,*options)
def read(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str)+'\n')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
SNAP=ROOT/'snapshot';SNAP.mkdir(exist_ok=True)
VALID=ROOT/'validation';VALID.mkdir(exist_ok=True)
TX=ROOT/'transactions';TX.mkdir(exist_ok=True)
DEST=Path('/media/jake/SSD/EDB/math/imports/math-academy/2026-10-10-held-complete')
INDEX=ROOT.parent/'held-questions.json';index_hash=digest(INDEX);index=read(INDEX);held={q['math_academy_id'] for q in index['questions']}
assert len(held)==839
source=read(ROOT/'recovery-input.json');review=read(ROOT/'answer-review.json');assert set(review)<=held
# Check basis BEFORE content planning, as well as after all speculative checks.
db=PreviewDatabase(arguments(['run']));assert db.args.database=='math' and db.args.source==SOURCE
basis=db.basis();assert basis==165,('Basis changed; review and replan explicitly',basis)
save(SNAP/'basis.json',{'basis':basis,'database':db.args.database,'source':SOURCE,'endpoint':db.args.endpoint,'held_index_sha256':index_hash})
(SNAP/'held-index.json').write_bytes(INDEX.read_bytes())
ids=sorted(review);topicids=sorted({next(o for o in source[mid]['occurrences'] if o['directory']==review[mid]['directory'])['topic_id'] for mid in ids})
existing=db.questions(ids,SNAP,basis=basis)
topics={t[':topic/math-academy-id']:t for [t] in db.query(TOPIC_QUERY.replace(':in $ ?id',':in $ [?id ...]'),[topicids],SNAP,'topics',basis)}
attributes=db.attributes(SNAP,basis)
idents=db.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],SNAP,'idents',basis)
ident_ids={str(i):e for e,i in idents};names={e:str(i) for e,i in attributes};source_id=ident_ids[SOURCE]
history_schema=db.query('[:find ?i ?v :where [?a :db/ident ?i] [?a :db/noHistory ?v]]',[],SNAP,'no-history',basis)
assert not any(v and str(i).split('/')[0] in {':question',':answer-field',':answer'} for i,v in history_schema)
selected={};image_rows={};library=ImageLibrary(db.args.math_root);groups={};guards={};noops=[];layout_checks=[];kp_eids={}
for t in topics.values():
 for p in t[':topic/knowledge-points']:kp_eids[str(p[':knowledge-point/id'])]=p[':db/id']
for mid in ids:
 audit=review[mid];path=Path(audit['directory']);o=next(o for o in source[mid]['occurrences'] if o['directory']==str(path))
 assert all(digest(p)==h for p,h in audit['source_hashes'].items()),mid
 raw=read(path/'content.json');state=read(path/'state.json');rec=state['questions'][mid];before=rec['before']
 assert hashlib.sha256(json.dumps(before,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==audit['before_layout_sha256']
 assert audit['source_quote']==o['worked_solution'] and audit['source_problem']==o['source_problem']
 soup=BeautifulSoup(before['html'],'html.parser')
 assert len(before['fields'])==len(audit['fields'])==len(o['before_fields'])
 q=copy.deepcopy(o['prepared_question']);q.pop('is_example',None);q['topic_id']=o['topic_id'];q['problem']=audit.get('restored_problem',o['source_problem']);q['worked_solution']=o['worked_solution'];q['answer_fields']=[]
 for f,rf in zip(before['fields'],audit['fields']):
  assert f['key']==rf['key'];choices=[{k:c[k] for k in ('type','value')} for c in f['choices']]
  assert rf['answer']==choices[rf['choice_index']]
  assert len(choices)>=2 and all(c['value'].strip(' $\t\r\n') for c in choices)
  if f['type']=='radio':
   nodes=soup.select('.questionWidget-choiceText, .choiceText');assert len(nodes)==len(choices),(mid,'radio choice layout',len(nodes),len(choices))
  else:
   node=soup.find(id=f['dom_id']);assert node is not None
   assert len(node.select('.selectListOption'))==len(choices),(mid,f['key'],'select choice layout')
   assert q['problem'].count('{{'+f['key']+'}}')==1,(mid,'missing or repeated field slot',f['key'])
  q['answer_fields'].append({'key':f['key'],'type':f['type'],'choices':choices,'correct_value':rf['answer']['value']})
 q=library.prepare_content(q,path)
 for f,rf in zip(q['answer_fields'],audit['fields']):
  assert f['correct_value']==f['choices'][rf['choice_index']]['value']
 raw_q=copy.deepcopy(q)
 context={'task_type':'review','topic_id':q['topic_id'],'questions':[q],'canonical_examples':[c for c in raw.get('canonical_examples',[]) if c.get('knowledge_point_id')==q['knowledge_point_id']],'new_knowledge_points':raw.get('new_knowledge_points',[])}
 resolved=resolve_knowledge_points(context,topics,existing);assert not resolved.get('new_knowledge_points')
 q=resolved['questions'][0];content={'task_type':'review','topic_id':q['topic_id'],'questions':[q],'canonical_examples':[]}
 forms,report=build_math_content(content,topics,existing)
 selected[mid]={'question':q,'path':str(path),'source':SOURCE,'review':str(ROOT/'answer-review.json'),'original_knowledge_point_id':raw_q['knowledge_point_id'],'resolved_knowledge_point_id':q['knowledge_point_id']}
 layout_checks.append({'question':mid,'fields':len(q['answer_fields']),'all_original_choices_preserved':True,'source_layout_matches':True,'recovered_from_html':'layout_recovery' in audit})
 if forms:groups[mid]=forms;guards[mid]=report['retractions']
 else:noops.append(mid)
 # Validate all normalized images by bytes and hash, including choice values.
 serialized=json.dumps(q,ensure_ascii=False)
 for ref in set(re.findall(r'images/[0-9a-f]{2}/[0-9a-f]{64}\.(?:png|jpg|gif|webp|svg)',serialized)):
  p=Path(db.args.math_root)/ref;data=p.read_bytes();assert digest(p)==p.stem and p.parent.name==p.stem[:2] and image_format(data)==p.suffix[1:]
  image_rows[ref]={'sha256':p.stem,'bytes':len(data)}
 for key in ('problem','worked_solution'):
  for url in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',q[key]):assert url in image_rows,(mid,key,url)
 for f in q['answer_fields']:
  for c in f['choices']:
   if c['type']=='image':assert c['value'] in image_rows
save(ROOT/'selected-content.json',selected);save(ROOT/'field-layout-verification.json',layout_checks)
save(ROOT/'image-verification.json',{'valid':True,'references':image_rows,'unique_images':len(image_rows)})
# Exact immutable entity guards: all earlier field/answer definitions survive.
immutable_answers={a[':db/id'] for q in existing.values() for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])}
immutable_fields=[(f[':db/id'],kw(a)) for q in existing.values() for f in q.get(':question/answer-fields',[]) for a in ['answer-field/id','answer-field/key','answer-field/type','answer-field/correct','answer-field/choices'] if ':'+a in f]
# Materialize only relevant base graph facts for exact speculative readback.
def seed_entity(graph,obj):
 eid=obj.get(':db/id')
 if eid is None:return
 for a,v in obj.items():
  if a==':db/id' or '/_' in a:continue
  vals=v if isinstance(v,list) else [v]
  for value in vals:
   if isinstance(value,dict):
    if ':db/id' in value:seed_entity(graph,value);value=value[':db/id']
    elif ':db/ident' in value:value=ident_ids[value[':db/ident']]
    else:continue
   graph[eid][str(a)].add(value)
base=collections.defaultdict(lambda:collections.defaultdict(set))
for mid,q in existing.items():
 seed_entity(base,q)
 for p in q.get(':knowledge-point/_questions',[]):base[kp_eids[str(p[':knowledge-point/id'])]][':knowledge-point/questions'].add(q[':db/id'])
def verify_preview(receipt,mids,rs):
 assert receipt[':edb/db-before-t']==basis and receipt[':edb/db-after-t']==basis+1
 validate_receipt(receipt,attributes,source_id,rs,immutable_answers,immutable_fields)
 g=copy.deepcopy(base)
 for e,a,v,t,s,added in receipt[':edb/tx-data']:
  attr=names[a]
  assert s==source_id
  assert attr==':db/txInstant' or attr.split('/')[0] in {':question',':answer',':answer-field',':knowledge-point'},attr
  if attr.startswith(':knowledge-point/'):assert attr==':knowledge-point/questions'
  if added:g[e][attr].add(v)
  else:g[e][attr].discard(v)
 qids={next(iter(attrs[':question/math-academy-id'])):eid for eid,attrs in g.items() if attrs.get(':question/math-academy-id')}
 def one(e,a):
  values=g[e][a];assert len(values)==1,(e,a,values);return next(iter(values))
 reports=[]
 for mid in mids:
  q=selected[mid]['question'];eid=qids[mid];old=existing.get(mid)
  assert one(eid,':question/id')==(old[':question/id'] if old else stable_id('question',mid))
  assert one(eid,':question/problem')==q['problem'];assert one(eid,':question/worked-solution')==q['worked_solution']
  if q.get('difficulty'):assert one(eid,':question/difficulty')==ident_ids[':question.difficulty/'+q['difficulty']]
  fs=g[eid][':question/answer-fields'];assert len(fs)==len(q['answer_fields'])
  bykey={one(f,':answer-field/key'):f for f in fs};assert len(bykey)==len(fs)
  for f in q['answer_fields']:
   fe=bykey[f['key']];assert one(fe,':answer-field/type')==ident_ids[':answer-field.type/'+f['type']]
   want={(ident_ids[':answer.type/'+c['type']],c['value']) for c in f['choices']}
   found={(one(a,':answer/type'),one(a,':answer/value')) for a in g[fe][':answer-field/choices']}
   assert found==want,(mid,'choices')
   ce=one(fe,':answer-field/correct');assert ce in g[fe][':answer-field/choices'] and one(ce,':answer/value')==f['correct_value']
   assert (one(ce,':answer/type'),one(ce,':answer/value')) in want
  owners={k for k,attrs in g.items() if eid in attrs.get(':knowledge-point/questions',set())}
  assert owners=={kp_eids[q['knowledge_point_id']]},(mid,'KP',owners)
  reports.append({'question':mid,'uuid':str(one(eid,':question/id')),'existing_uuid_preserved':bool(old),'all_fields_and_choices_exact':True,'knowledge_point_exact':True})
 # Reject any datom touching a question outside this batch or its old components.
 allowed_q={qids[m] for m in mids};allowed_f={f for m in mids for f in g[qids[m]][':question/answer-fields']};allowed_a={a for f in allowed_f for a in g[f][':answer-field/choices']}
 for e,a,v,t,s,added in receipt[':edb/tx-data']:
  attr=names[a]
  if attr.startswith(':question/'):assert e in allowed_q
  if attr.startswith(':answer-field/'):assert e in allowed_f
  if attr.startswith(':answer/'):assert e in allowed_a
  if attr==':knowledge-point/questions':assert v in allowed_q
 return reports
batches=[];allforms=[];allrs=[];seen=set();checks=[]
ordered_ids=sorted(groups)
parts=[set(ordered_ids[i:i+40]) for i in range(0,len(ordered_ids),40)]
categories=[('resolved-'+str(i+1),lambda m,part=part:m in part) for i,part in enumerate(parts)]
for label,predicate in categories:
 mids=[m for m in sorted(groups) if predicate(m)];assert not seen&set(mids);seen.update(mids)
 if not mids:continue
 forms=[f for m in mids for f in groups[m]];rs=list({dumps(r):r for m in mids for r in guards[m]}.values())
 name=f'{len(batches)+1:03d}-{label}-questions.edn';p=TX/name;p.write_text('[\n'+'\n'.join(' '+dumps(f) for f in forms)+'\n]\n');assert loads(p.read_text())==forms
 (VALID/(name+'.guards.edn')).write_text(dumps({'retractions':rs,'immutable_answers':sorted(immutable_answers),'immutable_fields':immutable_fields})+'\n')
 preview_text=db.command('with','--file',p,'--source',SOURCE);(VALID/(name+'.preview.edn')).write_text(preview_text)
 receipt=loads(preview_text);reports=verify_preview(receipt,mids,rs);save(VALID/(name+'.verification.json'),reports)
 batch={'file':str(DEST/name),'reference_file':str(p),'source':SOURCE,'question_count':len(mids),'questions':mids,'sha256':digest(p),'forms':len(forms),'planned_retractions':len(rs),'preview_datoms':len(receipt[':edb/tx-data']),'preview_valid':True}
 batches.append(batch);allforms.extend(forms);allrs.extend(rs);checks.extend(reports);print('PREVIEWED',name,len(mids),flush=True)
assert seen==set(groups)
# Combined preview establishes that individually disjoint batches also compose.
combined=VALID/'combined-preview-input.edn';combined.write_text(dumps(allforms)+'\n')
combined_text=db.command('with','--file',combined,'--source',SOURCE);(VALID/'combined-preview.edn').write_text(combined_text)
verify_preview(loads(combined_text),sorted(groups),list({dumps(r):r for r in allrs}.values()))
assert db.basis()==basis and digest(INDEX)==index_hash
# Only transaction EDNs are copied to the SSD. Reports/evidence remain in repo.
DEST.mkdir(parents=True,exist_ok=True)
for b in batches:
 p=Path(b['file']);data=Path(b['reference_file']).read_bytes()
 if p.exists():assert p.read_bytes()==data,'Refuse to overwrite a different prepared transaction'
 else:p.write_bytes(data)
 assert digest(p)==b['sha256']
remaining=sorted(held-set(review));counts=collections.Counter()
rows=read(ROOT.parent/'2026-10-10-held-next/remaining-analysis/questions.json')
for mid in remaining:counts[rows[mid]['category']]+=1
manifest={'database':'math','source':SOURCE,'basis_prepared_against':basis,'basis_after_previews':db.basis(),'transacted':False,'database_writes':0,'ready_questions':len(review),'ready_fields':sum(len(q['fields']) for q in review.values()),'radio_questions':sum(review[m]['category']!='select_field_binding' for m in review),'select_questions':sum(review[m]['category']=='select_field_binding' for m in review),'restored_select_layouts':sum('layout_recovery' in q for q in review.values()),'restored_roman_statement_questions':sum('restored_problem' in q for q in review.values()),'new_questions':sum(m not in existing for m in review),'updated_questions':sum(m in existing for m in groups),'already_current_questions':len(noops),'already_current_ids':noops,'prepared_ids':sorted(review),'still_unresolved_questions':len(remaining),'still_unresolved_ids':remaining,'remaining_reasons':dict(counts),'held_index_questions':len(held),'held_index_unchanged':True,'held_index_sha256':index_hash,'batches':batches,'combined_preview_valid':True,'exact_retractions_verified':True,'earlier_field_and_answer_entities_immutable':True,'earlier_history_retained':True,'all_answer_fields_verified':True,'all_choices_preserved':True,'identities_verified':True,'knowledge_point_membership_verified':True,'image_references_verified':True,'unique_images':len(image_rows),'commit_note':'Prepared only. Do not remove IDs from held index until verified commit. Recheck basis and replan if needed before a later authorized commit; previews do not reserve entity IDs.'}
save(ROOT/'manifest.json',manifest)
save(ROOT/'preview-verification.json',{'valid':True,'basis':basis,'database_writes':0,'questions_verified':len(checks),'combined_preview_valid':True,'all_datom_sources':SOURCE,'exact_retractions_verified':True,'immutable_old_answers':len(immutable_answers),'immutable_old_field_attributes':len(immutable_fields),'question_uuid_and_field_and_KP_checks':str(VALID),'held_index_unchanged':digest(INDEX)==index_hash})
print(json.dumps({k:v for k,v in manifest.items() if not isinstance(v,(list,dict))},indent=2))
