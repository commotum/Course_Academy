"""Runner-owned retirement of reviewed historical inventory defects.

Independent review supplies exact generated-record proof. The runner owns the
preview, guarded submission, fresh readback, and delivery review invalidation.
"""
from pathlib import Path

from generator_review import validate_review
from inventory_jobs import save


def repair_inventory(pipeline, evidence=None):
    """Resolve reviewed historical defects before reviewing fresh delivery.

    Reports must come from an independently validated reviewer associated
    with this source. Authors cannot nominate arbitrary database changes.
    Retirement uses the existing exact-request/preview/readback transport.
    """
    from generator_pipeline import digest, read
    roots=set()
    if evidence is not None:
        previous=pipeline.state.get('previous_review',{})
        if (Path(previous.get('directory','')).resolve()!=Path(evidence).resolve()
                or previous.get('binding',{}).get('source_hash')!=pipeline.state.get('source_hash')):
            raise ValueError('Inventory repair requires a review bound to this instructional source')
        roots.add(Path(evidence).resolve())
    history=pipeline.directory/'repair-history.json'
    if history.exists():
        for row in read(history)['findings']:
            if (row['finding']['kind']=='inventory' and row.get('source_hash')==pipeline.state.get('source_hash')
                    and row.get('review_directory')):
                roots.add(Path(row['review_directory']).resolve())
    from generator_pool_repair import POOL_REPAIR_POLICY_VERSION, generated_proof, repair_pool
    reports=[];inputs={}
    for root in sorted(roots):
        if root.parent!=pipeline.directory or not root.name.startswith('review-'):
            raise ValueError('Inventory repair requires this job\'s independent review evidence')
        validate_review(read(root/'result.json'),root)
        report=root/'affected-inventory.json'
        if not report.is_file() or not read(report).get('affected_questions'):continue
        reports.append(report)
        for row in read(report)['affected_questions']:
            proved=generated_proof(row,root)
            identity={'question_id':row.get('question_id'),'entity_id':row.get('entity_id'),
                'proof':digest(read(root/row['evidence_path'])) if proved else None,
                **({'unproved_claim':row} if not proved else {})}
            inputs[digest(identity)]=identity
    if not reports:return None
    key=digest({'policy_version':POOL_REPAIR_POLICY_VERSION,
                'claims':[inputs[key] for key in sorted(inputs)]})
    previous=pipeline.state.get('pool_repair',{})
    if pipeline.state.get('pool_repair_input')==key and not previous.get('unresolved'):
        return {**previous,'inventory_changed':False}
    if (pipeline.directory/'publication/request.json').exists():
        raise ValueError('Resolve the saved publication request before changing inventory review inputs')
    directory=pipeline.directory/'pool-repair'
    directory.mkdir(exist_ok=True)
    inventory_path=pipeline.directory/'source/inventory.json'
    before=read(inventory_path)
    baseline=directory/('inventory-before-'+digest(before)+'.json')
    if not baseline.exists():save(baseline,before)
    source=read(pipeline.directory/'source/source.json')
    status=pipeline.publisher.client.status()
    if any(status.get(k)!=source.get(k) for k in ('database','lineage')):
        raise ValueError('Inventory repair target does not match the reviewed database and lineage')
    result=repair_pool(pipeline.publisher,pipeline.state['request']['kp'],reports,directory)
    inventory=pipeline.publisher.extract_inventory(pipeline.state['request']['kp'],inventory_path.parent)
    if any(inventory.get(k)!=source.get(k) for k in ('database','lineage','kp_id')):
        raise ValueError('Repaired inventory does not match the instructional source identity')
    # An unrelated transaction advances the database basis without changing
    # this KP's delivery pool. It must not buy another independent review.
    changed=digest({k:v for k,v in inventory.items() if k!='basis'})!=digest(
        {k:v for k,v in before.items() if k!='basis'})
    fresh=directory/('inventory-after-'+digest(inventory)+'.json')
    save(fresh,inventory)
    if not changed:
        save(inventory_path,before)
        inventory=before
    result={**result,'policy_version':POOL_REPAIR_POLICY_VERSION,
            'inventory_changed':changed,'baseline':str(baseline),
            'fresh_inventory':str(fresh),'reports':[str(p) for p in reports],
            'inventory_sha256':digest(inventory)}
    save(directory/'review-handoff.json',result)
    pipeline.persist(pool_repair=result,pool_repair_input=key,inventory_hash=digest(inventory),
                 approval_recorded=False)
    return result

def block_inventory(pipeline, result):
    pipeline.block('inventory_repair_blocked',{
        'owner':'inventory',
        'error':'Stored-question repair needs intervention; see pool-repair/verification.json.',
        'unresolved':result.get('unresolved',[])},'validate')

