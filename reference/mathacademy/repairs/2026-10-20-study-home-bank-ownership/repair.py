"""Restore detached bank links as retired questions; preserve reserved reviews."""
import json, runpy, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import Publisher, GeneratorCommitter, digest, dumps, loads, kw, file_lock, StaleBasis

H=Path(__file__).resolve().parent
helper=runpy.run_path(str(ROOT/'reference/mathacademy/repairs/2026-10-20-integration-lesson-quality/read.py'))
native=helper['native']

def save(name,value):
    (H/name).write_text(json.dumps(value,indent=2,default=str)+'\n')

def main():
    p=Publisher.from_environment(source=':agent/codex')
    c=GeneratorCommitter(p.config,p.client,H)
    proofs=[]; owners={}
    for path in sorted((ROOT/'generate/repairs').glob('*/jobs/*/pool-repair/verification.json')):
        v=json.loads(path.read_text())
        if not v.get('retired'):continue
        kp=int(path.parents[1].name)
        tx=loads((path.parent/'transaction.edn').read_text())
        for form in tx:
            if str(form[0])==':db/retract' and str(form[2])==':knowledge-point/questions':
                assert form[1]==kp and form[3] in v['retired']
                assert form[3] not in owners or owners[form[3]]==kp
                owners[form[3]]=kp
        proofs.append({'path':str(path.relative_to(ROOT)),'basis':v['basis'],'retired':v['retired']})
    assert len(owners)==17
    save('evidence.json',{'original_detachment_receipts':proofs,'owners':owners})
    groups=[['questions',helper['QUESTION'],sorted(owners)],
            ['kps','[*]',sorted(set(owners.values()))],
            ['reserved-steps','[*]',[17592186666223,17592186670968]]]
    with file_lock(p.config.request_directory/'api.lock'):
        request=c.pending()
        if not request:
            status=p.client.status();basis=status['basis']
            before=native(H/'before',basis,groups);save('before.json',before)
            assert {q[':db/id']for q in before['questions']}==set(owners)
            assert all(not q.get(':question/math-academy-id') and ':question/retired' not in q for q in before['questions'])
            links=p.client.query('[:find ?q ?kp :in $ [?q ...] :where [?kp :knowledge-point/questions ?q]]',[sorted(owners)],H,'owners-before',basis)
            assert not links,links
            attributes=p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],H,'attributes',basis)
            idents=p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],H,'idents',basis)
            snapshot={'basis':basis,'lineage':status['lineage'],'attributes':attributes,'idents':idents}
            assertions=[];forms=[]
            for q,kp in sorted(owners.items()):
                assertions.extend([[kp,kw('knowledge-point/questions'),q],[q,kw('question/retired'),True]])
                forms.extend([[kw('db/add'),kp,kw('knowledge-point/questions'),q],[kw('db/cas'),q,kw('question/retired'),None,True]])
            forms.extend([[kw('db/ensure'),kp,kw('knowledge-point/validate')]for kp in sorted(set(owners.values()))])
            batch={'source':p.config.source,'assertions':assertions,'retractions':[],'forms':forms}
            c.preview(batch,snapshot)
            request=c.save_request(batch,snapshot,digest(batch))
        receipt=c.submit(request);proof=c.verify_receipt(request,receipt)
        after=native(H/'after',receipt[':edb/db-after-t'],groups);save('after.json',after)
        before=loads((H/'before/questions.edn').read_text())
        for q,old in zip(after['questions'],before):
            assert q.pop(':question/retired') is True
            assert q==old
        assert loads((H/'before/reserved-steps.edn').read_text())==after['reserved-steps']
        links=p.client.query('[:find ?q ?kp :in $ [?q ...] :where [?kp :knowledge-point/questions ?q]]',[sorted(owners)],H,'owners-after',receipt[':edb/db-after-t'])
        assert dict(links)==owners and len(links)==len(owners)
        historical=native(H/'historical',request['basis'],groups)
        assert historical['questions']==before
        result={'committed':True,'basis_before':request['basis'],'basis_after':receipt[':edb/db-after-t'],'restored_and_retired':len(owners),'reserved_steps_unchanged':True,'question_content_and_answers_unchanged':True,'historical_snapshot_verified':True,**proof}
        save('verification.json',result);print(json.dumps(result));c.retire(request,'verified',result)

if __name__=='__main__':main()
