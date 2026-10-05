#!/usr/bin/env python3
"""Apply an audited response-format repair without altering learner evidence.

The original import remains immutable. Replace only unused question-owned fields;
retain their old answer entities, and check exact old content before planning.
"""
import argparse,copy,hashlib,json,re,sys,uuid
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from core import atomic_json,stable_id
from database import Database,fingerprint
from edn import dumps,kw,loads
OUT=ROOT/'reference/mathacademy/history-question-import-2026-10-04/format-audit'


def db_instance():return Database(SimpleNamespace(edb_bin=str(ROOT.parent/'EDB/target/release/edb'),database='course-academy-v2',endpoint='/tmp/course-academy-edb-v2/writer.sock'))

def format_signature(q):
 if 'answer_fields' in q:
  return {'problem':q['problem'],'solution':q['worked_solution'],'difficulty':q['difficulty'],'fields':sorted([{'key':f['key'],'type':f['type'],'correct':f['correct_value'],'choices':sorted((c['type'],c['value']) for c in f['choices'])} for f in q['answer_fields']],key=lambda f:f['key'])}
 return {'problem':q[':question/problem'],'solution':q[':question/worked-solution'],'difficulty':q[':question/difficulty'][':db/ident'].split('/')[-1],'fields':sorted([{'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'correct':f[':answer-field/correct'][':answer/value'],'choices':sorted((a[':answer/type'][':db/ident'].split('/')[-1],a[':answer/value']) for a in f[':answer-field/choices'])} for f in q[':question/answer-fields']],key=lambda f:f['key'])}


def read_questions(db,ids,out,prefix,basis):
 result={}
 for start in range(0,len(ids),100):result.update(db.questions(ids[start:start+100],out,prefix+'-'+str(start),basis))
 return result


def check_receipt(receipt,attrs,allowed_subjects=None):
 allowed_names={'question/problem','question/answer-fields','answer-field/id','answer-field/key','answer-field/type','answer-field/choices','answer-field/correct','answer/id','answer/type','answer/value','db/txInstant'}
 names={a:str(name)[1:] for a,name in attrs}
 for row in receipt[':edb/tx-data']:
  name=names[row[1]]
  assert name in allowed_names,('Unexpected attribute',name)
  if row[-1] is False:assert name in ('question/problem','question/answer-fields'),('Unexpected retraction',name)
  if name in ('question/problem','question/answer-fields') and allowed_subjects is not None:assert row[0] in allowed_subjects


def plan(db,out):
 repairs=json.loads((OUT/'repairs.json').read_text())['questions'];basis=db.basis();all_q=json.loads((OUT/'questions.json').read_text())['questions'];ids=[q['math_academy_id'] for q in all_q]
 existing=read_questions(db,ids,out,'before-questions',basis)
 usage={}
 for name,where in [('presentations','[?item :task-item/content ?q]'),('responses','[?q :question/answer-fields ?f] [?f :answer-field/choices ?a] [?item :task-item/responses ?a]')]:
  rows=db.query('[:find ?mid ?item :in $ [?mid ...] :where [?q :question/math-academy-id ?mid] '+where+']',[ids],out,'existing-'+name,basis)
  for mid,item in rows:usage.setdefault(mid,[]).append({'kind':name,'entity':item})
 tx=[];applied=[];deferred=[];already=[]
 for repair in repairs:
  mid=repair['id'];old=existing[mid];before,after=repair['before'],repair['after']
  if format_signature(old)==format_signature(after):already.append(mid);continue
  if usage.get(mid):deferred.append({'id':mid,'reason':'Question already presented or answered; retain historical response semantics','references':usage[mid]});continue
  if format_signature(old)!=format_signature(before):deferred.append({'id':mid,'reason':'Content has changed since original import; preserve newer evidence'});continue
  assert not old.get(':knowledge-point/_canonical-example')
  assert {str(k[':knowledge-point/id']) for k in old[':knowledge-point/_questions']}=={after['knowledge_point_id']}
  # Versioned identities allow exact choice replacement without changing any
  # prior field/answer value. Detach ownership only; never retractEntity.
  digest=hashlib.sha256(json.dumps(after['answer_fields'],sort_keys=True).encode()).hexdigest()[:16]
  field_links=[]
  for f in after['answer_fields']:
   token=mid+'/format-repair-v1/'+digest+'/'+f['key'];fid='field-'+token;answers=[];correct=None
   for choice in f['choices']:
    atoken=token+'/'+hashlib.sha256((choice['type']+':'+choice['value']).encode()).hexdigest();aid='answer-'+atoken
    tx.append({kw('db/id'):aid,kw('answer/id'):stable_id('answer',atoken),kw('answer/type'):kw('answer.type/'+choice['type']),kw('answer/value'):choice['value'],kw('db/ensure'):[kw('answer/validate')]});answers.append(aid)
    if choice['value']==f['correct_value']:correct=aid
   assert correct is not None
   tx.append({kw('db/id'):fid,kw('answer-field/id'):stable_id('field',token),kw('answer-field/key'):f['key'],kw('answer-field/type'):kw('answer-field.type/'+f['type']),kw('answer-field/choices'):answers,kw('answer-field/correct'):correct,kw('db/ensure'):[kw('answer-field/validate')]});field_links.append(fid)
  for f in old[':question/answer-fields']:tx.append([kw('db/retract'),old[':db/id'],kw('question/answer-fields'),f[':db/id']])
  tx.append({kw('db/id'):old[':db/id'],kw('question/problem'):after['problem'],kw('question/answer-fields'):field_links,kw('db/ensure'):[kw('question/validate')]});applied.append(mid)
 attrs=db.attributes(out,basis);protected=db.protected(attrs,out,'protected-before',basis)
 atomic_json(out/'plan.json',{'basis':basis,'applied':applied,'deferred':deferred,'already_repaired':already,'protected_fact_count':len(protected),'protected_sha256':fingerprint(protected),'usage':usage})
 path=out/'transaction.edn';path.write_text(dumps(tx)+'\n')
 if tx:
  preview=db.command('with','--file',path);(out/'preview.edn').write_text(preview);receipt=loads(preview)
  assert receipt[':edb/db-before-t']==basis,'Database advanced during planning; repeat preview'
  check_receipt(receipt,attrs,{existing[mid][':db/id'] for mid in applied})
  atomic_json(out/'preview.json',{'basis':basis,'question_count':len(applied),'transaction_datoms':len(receipt[':edb/tx-data']),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'learner_and_engine_attributes_excluded':True,'database_writes':0})
 print(json.dumps({'basis':basis,'repairs_planned':len(applied),'already_repaired':len(already),'deferred':len(deferred),'database_writes':0}))
 return path,basis,protected,attrs


def commit(db,out):
 intent_file=out/'commit-intent.json';tx=out/'transaction.edn'
 if not intent_file.exists():
  preview=json.loads((out/'preview.json').read_text());plan_data=json.loads((out/'plan.json').read_text());digest=hashlib.sha256(tx.read_bytes()).hexdigest();assert digest==preview['sha256']
  assert db.basis()==preview['basis'],'Database advanced after preview; replan before committing'
  intent={'database':db.args.database,'endpoint':db.args.endpoint,'basis':preview['basis'],'sha256':digest,'request_key':'ma-history-format-repair-'+digest,'protected_sha256':plan_data['protected_sha256'],'repair_sha256':hashlib.sha256((OUT/'repairs.json').read_bytes()).hexdigest()}
  atomic_json(intent_file,intent)
 intent=json.loads(intent_file.read_text());assert intent['sha256']==hashlib.sha256(tx.read_bytes()).hexdigest();assert intent['repair_sha256']==hashlib.sha256((OUT/'repairs.json').read_bytes()).hexdigest()
 receipt=db._commit(intent,tx,out);before,after=receipt[':edb/db-before-t'],receipt[':edb/db-after-t'];assert before==intent['basis']
 attrs=db.attributes(out,before);check_receipt(receipt,attrs)
 protected=db.protected(attrs,out,'protected-after',after);assert fingerprint(protected)==intent['protected_sha256']
 plan_data=json.loads((out/'plan.json').read_text());all_q=json.loads((OUT/'questions.json').read_text())['questions'];existing=read_questions(db,[q['math_academy_id'] for q in all_q],out,'after-questions',after)
 applied=set(plan_data['applied']);prior={}
 for p in out.glob('before-questions-*.edn'):
  if re.fullmatch(r'before-questions-\d+\.edn',p.name):
   for row in loads(p.read_text()):prior[row[0][':question/math-academy-id']]=row[0]
 old_component_ids={f[':db/id'] for q in prior.values() for f in q[':question/answer-fields']}
 old_component_ids.update(a[':db/id'] for q in prior.values() for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])
 assert not any(row[0] in old_component_ids for row in receipt[':edb/tx-data']), 'A preexisting answer or field was changed'
 for q in all_q:
  mid=q['math_academy_id'];assert mid in existing
  if mid in applied:assert format_signature(existing[mid])==format_signature(q),mid
  else:assert existing[mid]==prior[mid],('Unselected question changed',mid)
  old,new=prior[mid],existing[mid]
  assert old[':question/id']==new[':question/id'] and old[':question/worked-solution']==new[':question/worked-solution'] and old[':question/difficulty']==new[':question/difficulty']
  assert old.get(':knowledge-point/_questions')==new.get(':knowledge-point/_questions')
 verification={'committed':True,'basis_before':before,'basis_after':after,'questions_repaired':len(applied),'questions_deferred':len(plan_data['deferred']),'all_1506_questions_verified':True,'question_ids_solutions_difficulties_and_kp_links_unchanged':True,'preexisting_answer_and_field_entities_unchanged':True,'reapplication_is_noop':all(format_signature(existing[r['id']])==format_signature(r['after']) for r in json.loads((OUT/'repairs.json').read_text())['questions']),'unselected_questions_unchanged':True,'learner_and_engine_facts_unchanged':True,'protected_fact_count':len(protected),'protected_facts_sha256':fingerprint(protected),'transaction_sha256':intent['sha256']}
 atomic_json(out/'verification.json',verification);print(json.dumps(verification,indent=2))


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--commit',action='store_true');args=parser.parse_args();out=OUT/'database-repair';out.mkdir(exist_ok=True);db=db_instance()
 if args.commit:commit(db,out)
 else:
  assert not (out/'commit-intent.json').exists(),'Resolve saved commit intent before replanning'
  plan(db,out)
if __name__=='__main__':main()
