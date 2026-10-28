import collections,json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());Q={q[':db/id']:q for q in D['questions']};dups=json.loads((H/'duplicate-field-keys.json').read_text());M=json.loads((H/'source-manifest.json').read_text());old=[]
for r in dups:
 bad=[f for f in r['fields']if f['correct']is None];good=[f for f in r['fields']if f['correct']is not None];assert len(bad)==len(good)==1;old.append((r,bad[0]['id'],good[0]['id']))
answers=[a[':db/id']for r,b,g in old for f in Q[r['question']][':question/answer-fields']if f[':db/id']==b for a in f[':answer-field/choices']];db=connection();refs={}
for hist in (False,True):
 refs['content-history'if hist else'content-current']=db.query('[:find ?q ?item ?tx ?op :in $ [?q ...] :where [?item :task-item/content ?q ?tx _ ?op]]',[sorted({r['question']for r,b,g in old})],H,'duplicate-fields-content-'+str(hist),9122,history=hist)
 refs['responses-history'if hist else'responses-current']=db.query('[:find ?a ?item ?tx ?op :in $ [?a ...] :where [?item :task-item/responses ?a ?tx _ ?op]]',[answers],H,'duplicate-fields-responses-'+str(hist),9122,history=hist)
assert refs['responses-current']==refs['responses-history']==[],refs
props=[];evidence=[]
for r,b,g in old:
 q=Q[r['question']];paths=M.get(r['source'],[]);p=next((p for p in paths if p.endswith('-before.json')),None);raw=json.loads(Path(p).read_text())if p else {};srcfields=raw.get('fields',[]);assert sum(f['key']==r['key']for f in srcfields)==1,(r,p,[f['key']for f in srcfields]);bad=next(f for f in q[':question/answer-fields']if f[':db/id']==b);good=next(f for f in q[':question/answer-fields']if f[':db/id']==g)
 props.append({'operation':'db/retract','entity':q[':db/id'],'attribute':'question/answer-fields','value':b,'expected_before_field_ids':sorted(f[':db/id']for f in q[':question/answer-fields']),'reason':'Remove only the unused legacy duplicate field membership; the complete same-key field matches the original one-field-per-key response structure. Retain all field and answer entities.','evidence':{'source_identity':r['source'],'path':p,'key':r['key'],'retained_complete_field':g,'retained_correct':good[':answer-field/correct'][':db/id'],'source_field_count':len(srcfields),'source_key_occurrences':1,'no_current_or_historical_response_refs_to_legacy_bank_at_basis':9122,'all_entities_retained':True},'confidence':'high'})
 evidence.append({'question':q[':db/id'],'source_identity':r['source'],'source_path':p,'source_fields':srcfields,'removed_membership_field_record':bad,'retained_complete_field_record':good})
(H/'duplicate-field-membership-proposals.json').write_text(json.dumps(props,indent=2));(H/'duplicate-field-source-evidence.json').write_text(json.dumps(evidence,indent=2));(H/'duplicate-field-reference-evidence.json').write_text(json.dumps(refs,indent=2));print('legacy field detaches',len(props),'question content refs',len(refs['content-current']),'historical',len(refs['content-history']),'legacy responses0')
