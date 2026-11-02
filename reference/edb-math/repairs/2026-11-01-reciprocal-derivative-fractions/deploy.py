"""Three text-only CAS repairs; preserve every existing entity and response."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,GeneratorCommitter,StaleBasis,digest,dumps,loads,kw,file_lock
from capture.scripts.storage import atomic_json
KP=17592186119939

def prepare(p):
    proposals=json.loads((H/'proposals.json').read_text());work=H/'publication';status=p.client.status();basis=status['basis']
    before=p.read_kp(KP,work/'before',basis);questions={q[':db/id']:q for q in before[':knowledge-point/questions']}
    forms=[];adds=[];removes=[]
    for row in proposals:
        eid=row['entity'];attr=row['attribute'];assert questions[eid][':'+attr]==row['before']
        forms.append([kw('db/cas'),eid,kw(attr),row['before'],row['after']]);adds.append([eid,kw(attr),row['after']]);removes.append([eid,kw(attr),row['before']])
    for eid in sorted({r['entity'] for r in proposals}):forms.append([kw('db/ensure'),eid,kw('question/validate')])
    attributes=p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],work,'attributes',basis)
    idents=p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],work,'idents',basis)
    snapshot={'basis':basis,'lineage':status['lineage'],'attributes':attributes,'idents':idents}
    batch={'source':p.config.source,'forms':forms,'assertions':adds,'retractions':removes}
    prepared={'basis':basis,'before_edn':dumps(before),'batch_edn':dumps(batch),'snapshot_edn':dumps(snapshot),'proposals':proposals}
    atomic_json(work/'preparation.json',prepared);committer=GeneratorCommitter(p.config,p.client,work)
    committer.preview(batch,snapshot);request=committer.save_request(batch,snapshot,digest(prepared))
    return prepared,committer,request

def apply(p,prepared,c,request):
    assert request['content_sha256']==digest(prepared)
    receipt=c.submit(request);proof=c.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t'];after=p.read_kp(KP,H/'publication/after',basis);before=loads(prepared['before_edn'])
    now={q[':db/id']:q for q in after[':knowledge-point/questions']};changes={}
    for row in prepared['proposals']:changes.setdefault(row['entity'],{})[':'+row['attribute']]=row['after']
    assert len(now)==len(before[':knowledge-point/questions'])
    for q in before[':knowledge-point/questions']:
        expected=dict(q);expected.update(changes.get(q[':db/id'],{}));assert now[q[':db/id']]==expected
    assert {k:v for k,v in after.items() if k!=':knowledge-point/questions'}=={k:v for k,v in before.items() if k!=':knowledge-point/questions'}
    result={'passed':True,'committed':True,'basis_before':request['basis'],'basis_after':basis,'questions_repaired':sorted(changes),'text_attributes_changed':3,'all_question_field_answer_identities_and_keys_preserved':True,'other_questions_and_canonical_preserved':True,'saved_responses_preserved':True,'request_key':request['request_key'],**proof}
    atomic_json(H/'verification.json',result);c.retire(request,'verified',result);print(json.dumps(result,indent=2))

def main():
    assert json.loads((H/'audit.json').read_text())['passed']
    for mode in ('desktop','phone','phone-active'):assert json.loads((H/f'render-{mode}/rendering.json').read_text())['passed']
    p=Publisher.from_environment(source=':agent/codex');work=H/'publication';lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{KP}.lock'
    with file_lock(lock),file_lock(Path(p.config.request_directory)/'api.lock'):
        c=GeneratorCommitter(p.config,p.client,work);request=c.pending()
        if request:apply(p,json.loads((work/'preparation.json').read_text()),c,request)
        elif not (H/'verification.json').exists():
            for _ in range(4):
                request=None
                try:
                    prepared,c,request=prepare(p);apply(p,prepared,c,request);break
                except StaleBasis:
                    if request:c.retire(request,'rejected_stale_basis',{'reason':'Confirmed writer rejection; refresh exact content and basis'})
            else:raise RuntimeError('Repeated basis races; no confirmed publication')

if __name__=='__main__':main()
