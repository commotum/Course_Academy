"""Archived repair driver: saved authored evidence only; no live browser profiles."""
from copy import deepcopy
from pathlib import Path
import argparse, hashlib, json, shutil, threading, time, traceback
from contextlib import contextmanager
from historical_solution_supplement import supplement_q181775, validate_cached_graphics
from quiz7_source_reconstruction import reconstruct_quiz7
from literal_brace_source_supplement import refresh_source as refresh_literal_source
from playwright.sync_api import sync_playwright
from scripts import recovery
from scripts.config import Config
from scripts.activity import capture as capture_module, solver as solver_module
from scripts.activity.task_payload import task_payload
from scripts.storage import atomic_json, read_json

ROOT=Path(__file__).resolve().parent
IMPORTED_LITERAL_SUPPLEMENT=(ROOT/'literal_brace_source_supplement.py').read_bytes()
IMPORTED_HISTORICAL_SUPPLEMENT=(ROOT/'historical_solution_supplement.py').read_bytes()+b'literal-ma-evidence-focus-v1'
IMPORTED_QUIZ7_SUPPLEMENT=(ROOT/'quiz7_source_reconstruction.py').read_bytes()
IMPORTED_DRIVER_SOURCE=Path(__file__).read_bytes()
# Pin the imported extractor/reviewer generation for this fresh singleton.
# Shared source files may change while an authored review is running.
IMPORTED_RECOVERY_VERSION=recovery.version()
recovery.version=lambda:IMPORTED_RECOVERY_VERSION
ENABLE_LITERAL_SOURCE_REFRESH=False
ACTIVE_PAGE=None
CURRENT_SOURCE_ORIGINALS={}
CURRENT_SOURCE_REPAIR=None
FORBIDDEN={'presentations','previous_submissions','submissions','responses','attempts','current_feedback',
    'source_selected','source_correct','source_result','grade','source_grade','result','field_grades','correct_value',
    'correct_option','correct_origin','correct_evidence','evidence','judgment','proof_feedback',
    'screenshot','screenshot_path','feedback','status','answers'}

def authored_only(value):
    if isinstance(value, list):return [authored_only(v) for v in value]
    if isinstance(value,dict):
        return {k:authored_only(v) for k,v in value.items() if k not in FORBIDDEN}
    return value

original_reextract=recovery.reextract_record
def supplemented_reextract(record,page,repair,**kwargs):
    question=original_reextract(record,page,repair,**kwargs)
    question=reconstruct_quiz7(record,question,page,repair,original_reextract)
    if ENABLE_LITERAL_SOURCE_REFRESH:question=refresh_literal_source(record,question,page,repair)
    return validate_cached_graphics(supplement_q181775(question,repair),repair)
recovery.reextract_record=supplemented_reextract

OriginalSolver=solver_module.SolverClient
class ArchivedSolver(OriginalSolver):
    def _conversation(self, task, payload):
        return []
    def request(self,task,payload,**kwargs):
        payload=authored_only(task_payload(task,payload))
        if task=='judge_question' and (payload.get('question') or {}).get('math_academy_id')=='q-161133' and payload.get('gap'):
            payload['recovery']=str(payload.get('recovery',''))+' Return ma_evidence as ONLY a contiguous verbatim substring of the provided worked_solution. Do not prepend an explanation, label, quotation marks, or Markdown fence. Match the exact current typed source choice for ma_value and correct_value.'
        if task=='judge_question' and (payload.get('question') or {}).get('math_academy_id') in ('q-331821','q-37456'):
            payload['recovery']=str(payload.get('recovery',''))+' Independently solve this original live authored problem using its own worked solution and exact typed choices. This source reconstruction is bound to permanent original question ID and all original control IDs. Do not infer any learner grade. For q-37456 derive the Hessian determinant and check each I/II/III statement; preserve the live bold Hessian f variant. Return each ma_evidence as only a contiguous verbatim source solution span.'
        # Keep authored worked_solution, unselected control choices and original assets.
        audit={'task':task,'restriction':'Authored problem, solution, controls and diagrams only; no learner attempts, credentials, profiles or full checkpoints',
               'payload_sha256':hashlib.sha256(json.dumps(payload,sort_keys=True,default=str).encode()).hexdigest()}
        atomic_json(self.directory/(audit['payload_sha256']+'-restriction.json'),audit)
        try:
            return super().request(task,payload,**kwargs)
        except solver_module.SolverUnavailable as error:
            if 'already has an active writer' not in str(error):raise
            self.state['session_id']=None;self.state['generation']=self.state.get('generation',0)+1
            atomic_json(self.state_path,self.state)
            return super().request(task,payload,**{**kwargs,'force_new':True})
solver_module.SolverClient=ArchivedSolver
capture_module.SolverClient=ArchivedSolver
recovery.SolverClient=ArchivedSolver
original_review=capture_module.ActivityCapture._review
original_finalize=capture_module.finalize_answers

def source_bound_finalize(question,presentations,judgment):
    finalized=original_finalize(question,presentations,judgment)
    identity=finalized.get('math_academy_id')
    if ENABLE_LITERAL_SOURCE_REFRESH and identity in CURRENT_SOURCE_ORIGINALS:
        # Finalization synthesizes grade evidence from preserved historical
        # presentations. Rebind that exact physical control only after synthesis.
        finalized=refresh_literal_source(CURRENT_SOURCE_ORIGINALS[identity],finalized,ACTIVE_PAGE,CURRENT_SOURCE_REPAIR)
    return finalized
capture_module.finalize_answers=source_bound_finalize

def fresh_review(self):
    global CURRENT_SOURCE_ORIGINALS,CURRENT_SOURCE_REPAIR
    self.state['judgments']={}
    self.state['answer_evidence_reviews']={}
    if ENABLE_LITERAL_SOURCE_REFRESH:
        original_merge=self._merge_history
        originals=read_json(self.checkpoint_path.parent/'originals/content.json')
        CURRENT_SOURCE_ORIGINALS={q['math_academy_id']:q for bucket in ('questions','canonical_examples') for q in originals.get(bucket,[]) if q.get('math_academy_id')}
        CURRENT_SOURCE_REPAIR=self.checkpoint_path.parent
        def source_bound_merge(history):
            content=original_merge(history)
            for bucket in ('questions','canonical_examples'):
                owned={q.get('math_academy_id'):q for q in originals.get(bucket,[]) if q.get('math_academy_id')}
                content[bucket]=[refresh_literal_source(owned[q['math_academy_id']],q,ACTIVE_PAGE,self.checkpoint_path.parent)
                    if q.get('math_academy_id') in owned else q for q in content.get(bucket,[])]
            return content
        self._merge_history=source_bound_merge
    return original_review(self)
capture_module.ActivityCapture._review=fresh_review

def package_version(task_id, base, historical, quiz7):
    """Each package starts from one frozen base; versions never chain across packages."""
    if task_id not in ('14120023','14114807','14118927','14111253'):return base
    source=historical+(quiz7 if task_id=='14111253' else b'')
    return hashlib.sha256(base.encode()+source).hexdigest()

def main():
    global ENABLE_LITERAL_SOURCE_REFRESH,IMPORTED_RECOVERY_VERSION,ACTIVE_PAGE
    parser=argparse.ArgumentParser();parser.add_argument('--offset',type=int,default=0);parser.add_argument('--limit',type=int);parser.add_argument('--prepare-only',action='store_true');parser.add_argument('--include-finite-additions',action='store_true');parser.add_argument('--candidate-file',type=Path);parser.add_argument('--result-tag');parser.add_argument('--literal-brace-refresh',action='store_true')
    args=parser.parse_args();candidates=read_json(ROOT/'later-source-candidates.json')
    if args.literal_brace_refresh:
        ENABLE_LITERAL_SOURCE_REFRESH=True
        IMPORTED_RECOVERY_VERSION=hashlib.sha256(IMPORTED_RECOVERY_VERSION.encode()+IMPORTED_LITERAL_SUPPLEMENT+IMPORTED_DRIVER_SOURCE).hexdigest()
    candidates.append({'account':'multivariable','directory':str(ROOT.parents[1]/'capture/multivariable/14120884/repairs/source-candidates-v1')})
    if args.include_finite_additions:candidates.extend(read_json(ROOT/'later-finite-additional-candidates.json'))
    if args.candidate_file:candidates=read_json(args.candidate_file)
    selected=candidates[args.offset:args.offset+args.limit if args.limit else None]
    result_prefix='later-source-review' if args.prepare_only else 'later-repair-run'
    result_path=ROOT/f'{result_prefix}-{args.result_tag or args.offset}.json'
    results=read_json(result_path,[])
    if args.prepare_only:
        @contextmanager
        def source_only_archive_guard(path):
            yield None
        recovery.file_lock=source_only_archive_guard
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True);context=browser.new_context()
        context.route('**/*',lambda route:route.abort());page=context.new_page()
        ACTIVE_PAGE=page
        for number,candidate in enumerate(selected,args.offset+1):
            directory=Path(candidate['directory']).parents[1]
            frozen_version=package_version(directory.name,IMPORTED_RECOVERY_VERSION,IMPORTED_HISTORICAL_SUPPLEMENT,IMPORTED_QUIZ7_SUPPLEMENT)
            recovery.version=lambda frozen_version=frozen_version:frozen_version
            config=Config(account=candidate['account'],solver_model='gpt-6.1-sol',codex_bin=str(ROOT/'archived-codex'))
            print(json.dumps({'event':'start','number':number,'task_id':directory.name,'account':config.account}),flush=True)
            repair=directory/'repairs'/('completeness-'+recovery.version()[:16])
            if ENABLE_LITERAL_SOURCE_REFRESH:
                repair.mkdir(parents=True,exist_ok=True)
                (repair/'literal-brace-source-supplement.py').write_bytes(IMPORTED_LITERAL_SUPPLEMENT)
                (repair/'run-later-repairs-frozen.py').write_bytes(IMPORTED_DRIVER_SOURCE)
                atomic_json(repair/'frozen-source-generation.json',{'package_version':frozen_version,
                    'literal_supplement_sha256':hashlib.sha256(IMPORTED_LITERAL_SUPPLEMENT).hexdigest(),
                    'source_snapshot':str(repair/'literal-brace-source-supplement.py'),
                    'driver_sha256':hashlib.sha256(IMPORTED_DRIVER_SOURCE).hexdigest(),
                    'version_computation':'Immutable imported base plus only this package own historical/quiz7 supplements'})
            if not (repair/'solver/session.json').exists():
                sources=sorted((directory/'repairs').glob('completeness-*/solver'), key=lambda p:p.stat().st_mtime, reverse=True)
                sources=[p for p in sources if p.parent!=repair and list(p.glob('*-restriction.json'))]
                if sources:
                    repair.mkdir(parents=True,exist_ok=True)
                    shutil.copytree(sources[0],repair/'solver',dirs_exist_ok=True)
                    seeded=read_json(repair/'solver/session.json',{})
                    seeded['session_id']=None;seeded['generation']=seeded.get('generation',0)+1
                    seeded.pop('topic_catalog',None)
                    atomic_json(repair/'solver/session.json',seeded)
                    atomic_json(repair/'solver/active-process.json',{})
                    atomic_json(repair/'solver-cache-seed.json',{'from':str(sources[0]),'cache_policy':'Exact hash-validated authored-only requests only; changed source evidence reviewed afresh'})
            before={name:hashlib.sha256((config.state_root/name).read_bytes()).hexdigest() for name in ['xp-ledger.json','retakes.json'] if (config.state_root/name).exists()}
            try:
                if args.prepare_only:
                    if (directory/'database/request.json').exists():raise ValueError('Unresolved immutable request excludes source-only staging')
                    if (read_json(directory/'database/result.json',{}) or {}).get('status') not in ('verified','no_changes'):raise ValueError('Source-only staging requires a verified terminal import')
                    protected={name:hashlib.sha256((directory/name).read_bytes()).hexdigest() for name in ['checkpoint.json','capture-complete.json','content.json']}
                outcome=recovery.reprocess(config,directory,page,apply=not args.prepare_only)
                if args.prepare_only:
                    after={name:hashlib.sha256((directory/name).read_bytes()).hexdigest() for name in protected}
                    if after!=protected:raise ValueError('Shared completed package changed during source-only staging')
                    outcome['source_only_completion_assertions']={'protected_sha256':protected,'shared_completed_package_unchanged':True,'unresolved_request_absent':True,'completed_inactive_verified_capture':True}
                    atomic_json(Path(outcome['repair'])/'source-only-completion-assertions.json',outcome['source_only_completion_assertions'])
                outcome.update(account=config.account,task_id=directory.name)
            except Exception as error:
                outcome={'status':'error','account':config.account,'task_id':directory.name,'error':str(error),'traceback':traceback.format_exc()}
            outcome['completed_at']=time.time();results=[r for r in results if r['task_id']!=directory.name]+[outcome]
            atomic_json(result_path,results)
            print(json.dumps(outcome),flush=True)
        browser.close()
if __name__=='__main__':main()
