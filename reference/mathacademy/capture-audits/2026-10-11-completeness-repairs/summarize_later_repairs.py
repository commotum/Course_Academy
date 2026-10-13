"""Collect checked import results, pinned readbacks and preservation evidence."""
from pathlib import Path
import hashlib,json
from scripts.database.edn import loads
from scripts.storage import atomic_json,read_json
ROOT=Path(__file__).resolve().parent
runs={}
for path in ROOT.glob('later-repair-run-*.json'):
    for row in read_json(path,[]):
        identity=(row['account'],row['task_id'])
        if identity not in runs or row.get('completed_at',0)>runs[identity].get('completed_at',0):runs[identity]=row
rows=[]
for identity,row in sorted(runs.items()):
    outcome={**row};outcome.pop('traceback',None)
    directory=Path(row.get('directory') or ROOT.parents[1]/'capture'/row['account']/row['task_id'])
    repair=Path(row['repair']) if row.get('repair') else None
    if repair and (repair/'originals').exists():
        checks={name:(directory/name).read_bytes()==(repair/'originals'/name).read_bytes()
            for name in ['checkpoint.json','capture-complete.json','post-activity.json'] if (repair/'originals'/name).exists()}
        original=read_json(repair/'originals/content.json',{});content=read_json(directory/'content.json',{})
        checks['completion_fields']=all(content.get(k)==original.get(k) for k in ['completion','base_xp','captured_at','policy','topic_context','pipeline','capture_version'])
        outcome['preservation']=checks
        result=read_json(directory/'database/result.json',{})
        verify=read_json(directory/'database/verification.json',{})
        outcome['database_result']={k:result.get(k) for k in ['status','basis']}
        outbox=read_json(directory/'import-status.json',{})
        original_outbox=read_json(repair/'originals/import-status.json',{})
        checks['capture_only_flag']=outbox.get('capture_only')==original_outbox.get('capture_only')
        checks['target_identity']=outbox.get('target_id')==original_outbox.get('target_id')
        outcome['completed_package_outbox']={'capture_directory_matches':outbox.get('capture_directory')==str(directory),
            'terminal_status':outbox.get('status'),'capture_only':outbox.get('capture_only'),
            'omissions':outbox.get('result',{}).get('omissions',[]),
            'omissions_match_current_database':outbox.get('result',{}).get('omissions',[])==result.get('omissions',[])}
        outcome['normal_reimport_is_noop']=result.get('status')=='no_changes' or verify.get('reimport_is_noop') is True
        outcome['commit_verification']={k:verify.get(k) for k in ['basis_before','basis_after','reimport_is_noop','learner_and_engine_facts_unchanged'] if k in verify}
        basis=result.get('basis');snapshot=directory/'database'/f'snapshot-{basis}'
        observed={}
        def collect(x):
            if isinstance(x,dict):
                if x.get(':question/math-academy-id'):observed[x[':question/math-academy-id']]=x
                for v in x.values():collect(v)
            elif isinstance(x,list):
                for v in x:collect(v)
        for path in snapshot.glob('questions-*.edn'):
            if '-inputs' not in path.name and '-query' not in path.name:collect(loads(path.read_text()))
        omissions=[o for o in row.get('omissions',[]) if o.get('kind')=='question']
        readbacks=[]
        for bucket in ['questions','canonical_examples']:
            for q in content.get(bucket,[]):
                source=q.get('math_academy_id');capture_key=q.get('source_id') or source
                omitted=any(o.get('record_kind') in (None,bucket) and (o.get('capture_key')==capture_key if o.get('capture_key') else o.get('id')==source and source is not None) for o in omissions)
                db=observed.get(source,{})
                expected=len(q.get('answer_fields',q.get('fields',[])))
                observed_fields=len(db.get(':question/answer-fields',[]))
                check={'id':source,'capture_key':capture_key,'record_kind':bucket,'omitted':omitted,'present':bool(db),
                    'capture_fields':expected,'database_fields':observed_fields}
                if not omitted:check['field_count_matches']=expected==observed_fields if q.get('answer_fields_complete') else expected<=observed_fields
                readbacks.append(check)
        outcome['pinned_readback']={'basis':basis,'directory':str(snapshot),'questions':readbacks,
             'supported_records_present':all(q['present'] and q.get('field_count_matches') for q in readbacks if not q['omitted'])}
    rows.append(outcome)
summary={'captures':len(rows),'verified':sum(r['status']=='verified' for r in rows),
 'zero_omission_captures':sum(r['status']=='verified' and not r.get('omissions') for r in rows),
 'omissions':sum(len(r.get('omissions',[])) for r in rows),'results':rows}
additional_ids={'14121715','14121869','14121047'}
original_ids={Path(r['directory']).parents[1].name for r in read_json(ROOT/'later-source-candidates.json')}|{'14120884'}
for name,group in [('original36',[r for r in rows if r['task_id'] in original_ids]),('finite_additional3',[r for r in rows if r['task_id'] in additional_ids]),('frozen318_source_gaps',[r for r in rows if r['task_id'] not in original_ids|additional_ids])]:
 summary[name]={'captures':len(group),'verified':sum(r['status']=='verified' for r in group),'zero_omission_captures':sum(r['status']=='verified' and not r.get('omissions') for r in group),'omissions':sum(len(r.get('omissions',[])) for r in group)}
atomic_json(ROOT/'later-verified-repairs.json',summary)
print(json.dumps({k:v for k,v in summary.items() if k!='results'}))
