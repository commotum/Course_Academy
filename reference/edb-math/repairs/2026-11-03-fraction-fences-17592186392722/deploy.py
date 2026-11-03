"""Apply the reviewed lesson fence changes with exact CAS and readback."""
import importlib.util,json,sys
from contextlib import ExitStack
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,StaleBasis,digest,dumps,loads,kw,file_lock,jsonable
from capture.scripts.database.commit import Committer
from capture.scripts.storage import atomic_json
spec=importlib.util.spec_from_file_location('native_format_reader',H.parent/'2026-11-03-operator-notation-database/deploy.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
KPS=(17592186198355,17592186198356,17592186198473)

def read_lessons(p,work,basis,label):
    return p.client.query((H/'capture/lessons-query.edn').read_text(),loads((H/'capture/lessons-inputs.edn').read_text()),work,label,basis)

def prepare(p):
    work=H/'publication';rows=json.loads((H/'proposals.json').read_text());status=p.client.status();basis=status['basis']
    before=reader.read_entities(p,work,'before',sorted({r['entity'] for r in rows}),basis);by_id={r[':db/id']:r for r in before}
    kps={str(k):p.read_kp(k,work/'kp-before'/str(k),basis) for k in KPS};forms=[];adds=[];removes=[]
    for row in rows:
        assert by_id[row['entity']][':'+row['attribute']]==row['before']
        forms.append([kw('db/cas'),row['entity'],kw(row['attribute']),row['before'],row['after']]);adds.append([row['entity'],kw(row['attribute']),row['after']]);removes.append([row['entity'],kw(row['attribute']),row['before']])
    for q in json.loads((H/'audit.json').read_text())['questions_affected']:forms.append([kw('db/ensure'),q['entity'],kw('question/validate')])
    attrs=p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],work,'attributes',basis)
    idents=p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],work,'idents',basis)
    snapshot={'basis':basis,'lineage':status['lineage'],'attributes':attrs,'idents':idents};batch={'source':p.config.source,'forms':forms,'assertions':adds,'retractions':removes}
    lessons=read_lessons(p,work,basis,'lessons-before')
    prepared={'basis':basis,'before_edn':dumps(before),'kps_edn':dumps(kps),'lessons_edn':dumps(lessons),'proposals':rows,'snapshot_edn':dumps(snapshot),'batch_edn':dumps(batch)}
    atomic_json(work/'preparation.json',prepared);c=Committer(p.config,p.client,work);c.preview(batch,snapshot);request=c.save_request(batch,snapshot,digest(prepared));return prepared,c,request

def apply(p,prepared,c,request):
    assert request['content_sha256']==digest(prepared)
    receipt=c.submit(request);proof=c.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t'];old=loads(prepared['before_edn'])
    after=reader.read_entities(p,H/'publication','after',[r[':db/id'] for r in old],basis)
    assert {r[':db/id']:r for r in after}=={r[':db/id']:r for r in reader.patched(old,prepared['proposals'])}
    for kp,k in loads(prepared['kps_edn']).items():assert p.read_kp(int(kp),H/'publication/kp-after'/kp,basis)==reader.patched(k,prepared['proposals'])
    assert read_lessons(p,H/'publication',basis,'lessons-after')==reader.patched(loads(prepared['lessons_edn']),prepared['proposals'])
    result={'passed':True,'committed':True,'basis_before':request['basis'],'basis_after':basis,
        'questions_repaired':len(json.loads((H/'audit.json').read_text())['questions_affected']),'fields_repaired':len(prepared['proposals']),
        'only_fence_sizing_and_equivalent_angle_spelling_changed':True,'all_math_answers_identities_links_and_learner_history_preserved':True,
        'all_three_kps_verified':True,'request_key':request['request_key'],**proof}
    atomic_json(H/'verification.json',result);c.retire(request,'verified',result);print(json.dumps(result,indent=2))

def main():
    for name in ('audit.json','preflight.json','render-verification.json'):assert json.loads((H/name).read_text())['passed']
    p=Publisher.from_environment(source=':agent/codex');work=H/'publication'
    with ExitStack() as stack:
        for kp in KPS:stack.enter_context(file_lock(ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'))
        stack.enter_context(file_lock(Path(p.config.request_directory)/'api.lock'));c=Committer(p.config,p.client,work);request=c.pending()
        if request:apply(p,json.loads((work/'preparation.json').read_text()),c,request)
        elif not (H/'verification.json').exists():
            for _ in range(5):
                request=None
                try:
                    prepared,c,request=prepare(p);apply(p,prepared,c,request);break
                except StaleBasis:
                    if request:c.retire(request,'rejected_stale_basis',{'reason':'Confirmed basis rejection; refresh exact content'})
            else:raise RuntimeError('Repeated basis races; repair incomplete')

if __name__=='__main__':main()
