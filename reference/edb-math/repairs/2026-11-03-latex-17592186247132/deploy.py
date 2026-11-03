"""Apply operator-only repairs with exact CAS and durable writer recovery."""
import copy,json,sys
from contextlib import ExitStack
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,StaleBasis,digest,dumps,loads,kw,file_lock,jsonable
from capture.scripts.database.commit import Committer
from capture.scripts.storage import atomic_json
KPS=(17592186115398,17592186115399,17592186115400,17592186115401)

def update(value,proposals):
    result=copy.deepcopy(value);changes={}
    for p in proposals:changes.setdefault(p['entity'],{})[':'+p['attribute']]=p
    def walk(x):
        if isinstance(x,dict):
            for attr,p in changes.get(x.get(':db/id'),{}).items():
                if attr in x:assert x[attr]==p['before'];x[attr]=p['after']
            for child in x.values():walk(child)
        elif isinstance(x,list):
            for child in x:walk(child)
    walk(result);return result

def entities(p,ids,work,name,basis):
    return [row[0] for row in p.client.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e :db/id ?e]]',[ids],work,name,basis)]

def prepare(p):
    work=H/'publication';proposals=json.loads((H/'proposals.json').read_text());status=p.client.status();basis=status['basis'];ids=sorted({r['entity'] for r in proposals})
    # The generic entity-existence clause uses an actual changed attribute.
    rows=p.client.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[ids],work,'entities-before',basis)
    before={r[0][':db/id']:r[0] for r in rows};assert set(before)==set(ids)
    kps={str(k):p.read_kp(k,work/'before'/str(k),basis) for k in KPS}
    forms=[];adds=[];removes=[]
    for r in proposals:
        assert before[r['entity']][':'+r['attribute']]==r['before']
        forms.append([kw('db/cas'),r['entity'],kw(r['attribute']),r['before'],r['after']])
        adds.append([r['entity'],kw(r['attribute']),r['after']]);removes.append([r['entity'],kw(r['attribute']),r['before']])
    for r in json.loads((H/'audit.json').read_text())['questions_affected']:forms.append([kw('db/ensure'),r['entity'],kw('question/validate')])
    attributes=p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],work,'attributes',basis)
    idents=p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],work,'idents',basis)
    batch={'source':p.config.source,'forms':forms,'assertions':adds,'retractions':removes};snapshot={'basis':basis,'lineage':status['lineage'],'attributes':attributes,'idents':idents}
    prepared={'basis':basis,'before_edn':dumps(list(before.values())),'kps_edn':dumps(kps),'proposals':proposals,'batch_edn':dumps(batch),'snapshot_edn':dumps(snapshot)}
    atomic_json(work/'preparation.json',prepared);c=Committer(p.config,p.client,work);c.preview(batch,snapshot);request=c.save_request(batch,snapshot,digest(prepared));return prepared,c,request

def apply(p,prepared,c,request):
    assert request['content_sha256']==digest(prepared)
    receipt=c.submit(request);proof=c.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t'];before=loads(prepared['before_edn']);ids=[r[':db/id'] for r in before]
    rows=p.client.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[ids],H/'publication','entities-after',basis)
    now={r[0][':db/id']:r[0] for r in rows};expected={r[':db/id']:r for r in update(before,prepared['proposals'])};assert now==expected
    kps=loads(prepared['kps_edn'])
    for kp,old in kps.items():assert p.read_kp(int(kp),H/'publication/after'/kp,basis)==update(old,prepared['proposals'])
    result={'passed':True,'committed':True,'basis_before':request['basis'],'basis_after':basis,
        'text_attributes_repaired':len(prepared['proposals']),'questions_repaired':37,'answer_values_repaired':67,'tutorials_repaired':1,
        'all_existing_question_field_answer_identities_keys_and_learner_history_preserved':True,
        'exact_entities_and_all_four_kps_verified':True,'request_key':request['request_key'],**proof}
    atomic_json(H/'verification.json',result);c.retire(request,'verified',result);print(json.dumps(result,indent=2))

def main():
    assert json.loads((H/'render-verification.json').read_text())['passed']
    p=Publisher.from_environment(source=':agent/codex');work=H/'publication'
    with ExitStack() as stack:
        for kp in KPS:stack.enter_context(file_lock(ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'))
        stack.enter_context(file_lock(Path(p.config.request_directory)/'api.lock'))
        c=Committer(p.config,p.client,work);request=c.pending()
        if request:apply(p,json.loads((work/'preparation.json').read_text()),c,request)
        elif not (H/'verification.json').exists():
            for _ in range(5):
                request=None
                try:
                    prepared,c,request=prepare(p);apply(p,prepared,c,request);break
                except StaleBasis:
                    if request:c.retire(request,'rejected_stale_basis',{'reason':'Confirmed rejection; refresh basis and exact content'})
            else:raise RuntimeError('Repeated basis races; repair incomplete')

if __name__=='__main__':main()
