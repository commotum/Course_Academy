"""Consume immutable authored review packages through the normal locked pipeline."""
from pathlib import Path
import argparse, hashlib, json, threading, time
import run_later_repairs as driver  # Installs the existing authored-only solver contract.
from scripts.browser.adapter import EXTRACT
from scripts.config import Config
from scripts.storage import atomic_json, read_json, file_lock
from scripts.database.pipeline import DatabasePipeline
from scripts.database.evidence import authoritative_question
from scripts.activity.evidence import capture_gaps
from scripts.outbox import target_id

ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'reviewed21-apply-manifest.json'
RESULTS=ROOT/'later-repair-run-reviewed21.json'
DELTAS={('14110945','q-162649','own_source'),('14120023','q-114506','own_external_solution')}
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def check(condition, message):
    if not condition:raise ValueError(message)
def config_for(account):
    return Config(account=account,solver_model='gpt-6.1-sol',codex_bin=str(ROOT/'archived-codex'))
def spool_for(config,directory):
    key=hashlib.sha256((target_id(config)+'\n'+str(directory)).encode()).hexdigest()
    return config.spool_root/(key+'.json')
def protected_files(config,directory):
    paths=[directory/name for name in ['checkpoint.json','capture-complete.json','post-activity.json']]
    paths += [config.state_root/name for name in ['xp.json','daily-xp.json','completed.json','active.json','retakes.json','xp-ledger.json']]
    return {str(path):sha(path) for path in paths if path.is_file()}
def latest_stages():
    latest={}
    for path in ROOT.glob('later-source-review-literal-braces*.json'):
        for row in read_json(path,[]):
            key=(row['account'],row['task_id'])
            if row.get('completed_at',0)>latest.get(key,{}).get('completed_at',0):latest[key]=row
    return latest
def equivalence_certificate():
    path=ROOT/'decorated-phantom-final-frozen-archive-extractor-equivalence.json'
    certificate=read_json(path)
    check(certificate and certificate['roots']==729,'Missing final 729-root equivalence certificate')
    changed={(r['task_id'],r['id'],r['kind']) for r in certificate['records'] if not r['equivalent']}
    check(changed==DELTAS,'Unexpected extractor source deltas')
    check(not any(r.get('error') for r in certificate['records']),'Unbound original root in equivalence certificate')
    check(sha(ROOT/'literal-brace-final-extract-frozen.js')==certificate['baseline_extractor_sha256'],'Frozen old extractor bytes changed')
    check(sha(ROOT/'decorated-phantom-final-extract-reviewed.js')==certificate['candidate_extractor_sha256'],'Frozen reviewed candidate bytes changed')
    check(hashlib.sha256(EXTRACT.encode()).hexdigest()==certificate['candidate_extractor_sha256'],'Current extractor differs from reviewed final candidate')
    for row in certificate['records']:
        check(sha(row['path'])==row['source_html_sha256'],'Equivalence source HTML changed')
    return {'path':str(path),'sha256':sha(path),'baseline_extractor_sha256':certificate['baseline_extractor_sha256'],
            'candidate_extractor_sha256':certificate['candidate_extractor_sha256'],'unchanged_roots':727,'targeted_changed_roots':2}
def freeze_stage(row,config,directory):
    repair=Path(row['repair']);generation=read_json(repair/'frozen-source-generation.json')
    check(row['status']=='prepared','Stage is not a completed authored review')
    protected=row['source_only_completion_assertions']['protected_sha256']
    for name,digest in protected.items():check(sha(directory/name)==digest,'Original capture changed after source review')
    check(generation and generation['package_version'].startswith(repair.name.removeprefix('completeness-')),'Stage version is unbound')
    immutable={str(repair/name):sha(repair/name) for name in ['content.json','checkpoint.json','validation.json',
               'literal-brace-source-supplement.py','run-later-repairs-frozen.py','frozen-source-generation.json','original-hashes.json']}
    for path in list((repair/'literal-brace-source-proofs').glob('*.json'))+[repair/'decorated-phantom-old-extract.js']:
        if path.is_file():immutable[str(path)]=sha(path)
    check(sha(repair/'literal-brace-source-supplement.py')==generation['literal_supplement_sha256'],'Frozen helper mismatch')
    check(sha(repair/'run-later-repairs-frozen.py')==generation['driver_sha256'],'Frozen driver mismatch')
    content=read_json(repair/'content.json');validation=read_json(repair/'validation.json')
    check(not capture_gaps(content) and not validation['gaps'],'Reviewed source has gaps')
    for bucket in ['questions','canonical_examples']:
        for question in content.get(bucket,[]):
            check(question.get('answer_validation',{}).get('status')=='supported','Unconfirmed authored answer')
            authoritative_question(question,example=bucket=='canonical_examples')
            source=Path(question['html_path']);check(sha(source)==question['recovery']['source_sha256'],'Authored source SHA changed')
            immutable[str(source)]=sha(source)
            external=question.get('solution_evidence')
            if isinstance(external,str) and Path(external).is_file():immutable[external]=sha(external)
            for asset in question.get('assets',[]):
                path=asset.get('path')
                if path and Path(path).is_file():
                    check(not asset.get('sha256') or sha(path)==asset['sha256'],'Original asset SHA changed')
                    immutable[path]=sha(path)
    return {'account':row['account'],'task_id':directory.name,'directory':str(directory),'repair':str(repair),
            'review_version':generation['package_version'],'frozen_generation':generation,'immutable_stage_files':immutable,
            'protected_files':protected_files(config,directory),'original_content_sha256':protected['content.json'],
            'staged_content_sha256':sha(repair/'content.json'),'target_id':target_id(config),
            'review_method':'Fresh targeted changed source' if directory.name in {'14110945','14120023'} else 'Retained reviewed generation with exact old/new source-output equivalence'}
def guard(entry,config,*,allow_staged=False):
    directory=Path(entry['directory']);repair=Path(entry['repair'])
    check(directory.parent==config.output_root and directory.name==entry['task_id'],'Capture directory/account identity mismatch')
    active=read_json(config.state_root/'active.json',{}) or {}
    check(active.get('directory')!=str(directory),'Capture is active')
    check(not config.capture_only,'Current configuration does not authorize database import')
    check(target_id(config)==entry['target_id'],'Database target identity changed')
    for path,digest in entry['immutable_stage_files'].items():check(sha(path)==digest,'Immutable reviewed file changed: '+path)
    for path,digest in entry['protected_files'].items():check(sha(path)==digest,'Protected learner/completion file changed: '+path)
    allowed={entry['original_content_sha256']}
    if allow_staged:allowed.add(entry['staged_content_sha256'])
    check(sha(directory/'content.json') in allowed,'Current completed content changed unexpectedly')
    spool=spool_for(config,directory);item=read_json(spool);status=read_json(directory/'import-status.json')
    check(item and item.get('target_id')==entry['target_id'] and item.get('capture_directory')==str(directory),'Original outbox target mismatch')
    check(not item.get('capture_only') and not status.get('capture_only'),'Original capture-only flag excludes database import')
    check(status.get('target_id')==entry['target_id'],'Completed package target differs from original outbox')
    resumed=allow_staged and sha(directory/'content.json')==entry['staged_content_sha256'] and item.get('recovery_version')==entry['review_version']
    check(item.get('status') in {'verified','no_changes'} or resumed,'Original outbox has unclassified pending work')
    return directory,repair,spool,item
def authored_diff(entry):
    before=read_json(Path(entry['directory'])/'content.json');after=read_json(Path(entry['repair'])/'content.json');counts={}
    for bucket in ['questions','canonical_examples']:
        old={q.get('source_id') or q.get('math_academy_id'):q for q in before.get(bucket,[])}
        for q in after.get(bucket,[]):
            previous=old.get(q.get('source_id') or q.get('math_academy_id'),{})
            for key in ['problem','worked_solution','answer_fields_complete']:
                if previous.get(key)!=q.get(key):counts[key]=counts.get(key,0)+1
            def fields(record):
                return [{'key':f['key'],'type':f['type'],'choices':[(c['type'],c['value']) for c in f.get('choices',[])],
                         'correct_value':f.get('correct_value')} for f in record.get('answer_fields',record.get('fields',[]))]
            if fields(previous)!=fields(q):counts['typed_fields']=counts.get('typed_fields',0)+1
    return counts
def build_manifest():
    certificate=equivalence_certificate();latest=latest_stages();entries=[]
    for candidate in read_json(ROOT/'literal-brace-final-apply-candidates.json'):
        directory=Path(candidate['directory']).parents[1];config=config_for(candidate['account'])
        check(not (directory/'database/request.json').exists(),'Unresolved immutable request excludes manifest preparation')
        stage=latest[(candidate['account'],directory.name)]
        entry=freeze_stage(stage,config,directory);guard(entry,config)
        if directory.name in {'14110945','14120023'}:
            content=read_json(Path(entry['repair'])/'content.json')
            check(all(q['recovery']['extractor_sha256']==certificate['candidate_extractor_sha256']
                      for bucket in ['questions','canonical_examples'] for q in content.get(bucket,[])),
                  'Targeted changed package was not re-extracted with the final candidate')
        entries.append(entry)
    check(len(entries)==21,'Prepared archive scope is not exactly21 packages')
    manifest={'created_at':time.time(),'equivalence_certificate':certificate,'entries':entries,
              'policy':'Only immutable reviewed content; no re-extraction/re-review or attribution restamping during import'}
    atomic_json(MANIFEST,manifest)
    return manifest
def apply_one(entry,config):
    with file_lock(config.database_lock):
        directory,repair,spool,item=guard(entry,config,allow_staged=True)
        pipeline=DatabasePipeline(config,threading.Event())
        # A pending immutable request is always recovered from its own saved
        # content before any authored package/outbox mutation.
        if (directory/'database/request.json').exists():
            recovery=pipeline.process(directory,apply=True)
            check(not (directory/'database/request.json').exists() and recovery.get('status') in {'verified','no_changes'},
                  'Original immutable database request remains unresolved')
            directory,repair,spool,item=guard(entry,config,allow_staged=True)
        atomic_json(repair/'prepared-apply-original-outbox.json',item)
        content=read_json(repair/'content.json');checkpoint=read_json(repair/'checkpoint.json')
        atomic_json(directory/'content.json',content);atomic_json(directory/'history-content.json',checkpoint['history'])
        item.update(status='pending',next_attempt_at=0,recovery_version=entry['review_version']);item.pop('result',None);item.pop('error',None)
        atomic_json(spool,item)
        outcome=pipeline.process(directory,apply=True)
        item.update(status=outcome['status'] if outcome['status'] in {'verified','no_changes'} else 'pending',result=outcome)
        atomic_json(spool,item);atomic_json(directory/'import-status.json',item)
        for path,digest in entry['protected_files'].items():check(sha(path)==digest,'Normal import changed protected history')
        check(item['target_id']==entry['target_id'] and not item.get('capture_only'),'Normal import changed target/authorization')
        result={'status':'verified' if item['status'] in {'verified','no_changes'} else 'pending','account':entry['account'],
                'task_id':entry['task_id'],'directory':str(directory),'repair':str(repair),'version':entry['review_version'],
                'completed_at':time.time(),'omissions':outcome.get('omissions',[]),'questions':len(content.get('questions',[])),
                'prepared_source_generation_preserved':True,'review_method':entry['review_method'],'normal_pipeline_result':outcome}
        atomic_json(repair/'result.json',result);return result
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--build-manifest',action='store_true');parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    manifest=build_manifest() if args.build_manifest else read_json(MANIFEST)
    check(manifest,'No immutable reviewed apply manifest')
    certificate=manifest['equivalence_certificate'];check(sha(certificate['path'])==certificate['sha256'],'Approved equivalence certificate changed')
    results=read_json(RESULTS,[])
    for entry in manifest['entries']:
        if not args.apply:
            config=config_for(entry['account']);guard(entry,config)
            print(json.dumps({'status':'guarded_preview','task_id':entry['task_id'],'account':entry['account'],
                              'repair':entry['repair'],'staged_content_sha256':entry['staged_content_sha256'],
                              'review_method':entry['review_method'],'authored_changes':authored_diff(entry),
                              'database_writes':0,'native_preview':'Performed by unchanged normal pipeline immediately before each commit'}),flush=True);continue
        previous=next((r for r in results if r['task_id']==entry['task_id']),None)
        if previous and previous['status']=='verified':continue
        print(json.dumps({'event':'apply_start','task_id':entry['task_id'],'account':entry['account']}),flush=True)
        result=apply_one(entry,config_for(entry['account']))
        results=[r for r in results if r['task_id']!=entry['task_id']]+[result];atomic_json(RESULTS,results)
        print(json.dumps(result),flush=True)
        if result['status']!='verified':break
if __name__=='__main__':main()
