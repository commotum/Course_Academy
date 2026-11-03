"""Bounded operator-only CAS batches with exact durable recovery/readback."""
import json,sys,subprocess
from collections import defaultdict
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,StaleBasis,digest,dumps,loads,kw,file_lock
from capture.scripts.database.commit import Committer
from capture.scripts.storage import atomic_json

def read_entities(p,work,label,ids,basis):
    # Direct Pull avoids multiplying large content strings by every matching
    # datom in a Datalog query, which can exceed its intermediate-value budget.
    assert str(p.config.database)=='math'
    directory=work/label;directory.mkdir(parents=True,exist_ok=True)
    (directory/'native-pulls.edn').write_text(dumps([['entities','[*]',ids]])+'\n')
    binary=ROOT/'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'
    result=subprocess.run([str(binary),str(directory),str(basis)],env=p.client.environment,capture_output=True,text=True,timeout=180)
    (directory/'read.log').write_text(result.stderr);result.check_returncode()
    return loads((directory/'entities.edn').read_text())

def plan():
    proposals=json.loads((H/'proposals.json').read_text());groups=defaultdict(list)
    for row in proposals:groups[row['entity']].append(row)
    batches=[];current=[];size=0
    for entity,group in sorted(groups.items()):
        cost=sum(len(dumps([kw('db/cas'),r['entity'],kw(r['attribute']),r['before'],r['after']]).encode())+2 for r in group)
        if current and size+cost>2*1024*1024:batches.append(current);current=[];size=0
        current+=group;size+=cost
    if current:batches.append(current)
    out={'proposals_sha256':digest(proposals),'batches':batches};atomic_json(H/'plan.json',out);return out

def prepare(p,work,rows,schema):
    status=p.client.status();basis=status['basis'];ids=sorted({r['entity'] for r in rows})
    result=read_entities(p,work,'native-before',ids,basis)
    before={r[':db/id']:r for r in result};assert set(before)==set(ids)
    forms=[];adds=[];removes=[];changed=[];already=[]
    for r in rows:
        value=before[r['entity']][':'+r['attribute']]
        if value==r['after']:already.append(r);continue
        assert value==r['before'],('Concurrent content edit needs review',r['entity'],r['attribute'])
        forms.append([kw('db/cas'),r['entity'],kw(r['attribute']),r['before'],r['after']]);changed.append(r)
        adds.append([r['entity'],kw(r['attribute']),r['after']]);removes.append([r['entity'],kw(r['attribute']),r['before']])
    batch={'source':p.config.source,'forms':forms,'assertions':adds,'retractions':removes}
    snapshot={'basis':basis,'lineage':status['lineage'],**schema}
    prepared={'basis':basis,'before_edn':dumps(list(before.values())),'changed':changed,'already':already,'batch_edn':dumps(batch),'snapshot_edn':dumps(snapshot)}
    atomic_json(work/'preparation.json',prepared);c=Committer(p.config,p.client,work);c.preview(batch,snapshot);request=c.save_request(batch,snapshot,digest(prepared));return prepared,c,request

def apply(p,work,prepared,c,request):
    assert request['content_sha256']==digest(prepared)
    receipt=c.submit(request);proof=c.verify_receipt(request,receipt);basis=receipt[':edb/db-after-t'];before=loads(prepared['before_edn'])
    result=read_entities(p,work,'native-after',[r[':db/id'] for r in before],basis)
    now={r[':db/id']:r for r in result};expected={r[':db/id']:r for r in before}
    for row in prepared['changed']:expected[row['entity']][kw(row['attribute'])]=row['after']
    assert now==expected
    result={'passed':True,'committed':True,'basis_before':request['basis'],'basis_after':basis,
        'fields_repaired':len(prepared['changed']),'already_repaired':len(prepared['already']),
        'every_other_entity_attribute_unchanged':True,'request_key':request['request_key'],**proof}
    atomic_json(work/'verification.json',result);c.retire(request,'verified',result)
    print(json.dumps({k:result[k] for k in ('basis_after','fields_repaired','already_repaired')}),flush=True)

def main():
    for filename in ('audit.json','preflight.json','render-verification.json'):assert json.loads((H/filename).read_text())['passed']
    assert not json.loads((H/'excluded.json').read_text())
    p=Publisher.from_environment(source=':agent/codex');current=plan();schema=None;results=[]
    with file_lock(Path(p.config.request_directory)/'api.lock'):
        for i,rows in enumerate(current['batches']):
            work=H/'batches'/str(i);work.mkdir(parents=True,exist_ok=True);c=Committer(p.config,p.client,work);request=c.pending()
            if request:apply(p,work,json.loads((work/'preparation.json').read_text()),c,request)
            elif not (work/'verification.json').exists():
                if schema is None:
                    basis=p.client.status()['basis']
                    schema={'attributes':p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],H/'schema','attributes',basis),
                            'idents':p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],H/'schema','idents',basis)}
                for _ in range(5):
                    request=None
                    try:
                        prepared,c,request=prepare(p,work,rows,schema);apply(p,work,prepared,c,request);break
                    except StaleBasis:
                        if request:c.retire(request,'rejected_stale_basis',{'reason':'Confirmed rejection; refresh exact basis and values'})
                else:raise RuntimeError('Repeated basis races; repair remains incomplete')
            results.append(json.loads((work/'verification.json').read_text()))
    result={'passed':True,'committed':True,'fields_repaired':sum(r['fields_repaired'] for r in results),'already_repaired':sum(r['already_repaired'] for r in results),
        'basis_after':results[-1]['basis_after'],'batches':len(results),'entities':json.loads((H/'audit.json').read_text())['repair_entities'],
        'only_operator_commands_and_spacing_changed':True,'identities_keys_response_links_grades_and_all_other_attributes_preserved':True,'results':results}
    atomic_json(H/'verification.json',result);print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))

if __name__=='__main__':main()
