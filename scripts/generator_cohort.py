"""Date-gated, resumable review/repair of existing generators only.

Uses the established author/reviewer/publication pipeline. Legacy scripts first
receive a mechanical runtime package; authoring starts only after a concrete
packaging, sampling or review failure. The normal inventory workers stay separate.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from contextlib import contextmanager
from datetime import datetime
import fcntl
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time

from generator_packages import resolve_registered_script
from generator_pipeline import Pipeline, CodexSession, SessionRetryExhausted, digest, read, source_identity
from generator_publish import Publisher
from generator_review import REVIEW_POLICY_VERSION, validate_review
from inventory_jobs import save

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CUTOFF = '2026-10-16T14:51:26-07:00'
TERMINAL = {'verified', 'skipped_current', 'needs_repair', 'failed', 'blocked'}
STOP_EXIT = 78
MAX_WORKER_RESTARTS = 3


class CapacityUnavailable(RuntimeError):
    pass


def capacity_failure(text):
    return bool(re.search(r'usage_limit_reached|insufficient_quota|rate_limit_exceeded|hit your usage limit',text,re.I))


class CohortSession(CodexSession):
    def __call__(self, role, context, directory):
        try:return super().__call__(role,context,directory)
        except (OSError,ValueError,subprocess.SubprocessError,SessionRetryExhausted) as error:
            log=Path(directory)/'events.jsonl'
            if log.is_file():
                with log.open('rb') as stream:
                    stream.seek(max(0,log.stat().st_size-96_000));tail=stream.read().decode(errors='replace')
                if capacity_failure(tail):
                    raise CapacityUnavailable('Campaign stopped at the provider capacity limit; remaining generators were not attempted. Saved session: '+str(directory)) from error
            raise


def first_seen(text):
    dates = {}; current = None
    for line in text.splitlines():
        if line.startswith('DATE '):
            current = datetime.fromisoformat(line[5:]).timestamp()
        elif line.startswith('generate/scratch/') and current is not None:
            dates[line] = min(dates.get(line, current), current)
    return dates


def in_cohort(timestamp, cutoff):
    # Unknown age cannot establish that the latest verification was present.
    return timestamp is None or timestamp < cutoff


def build_cohort(registrations, course_topics, historical_jobs, dates, cutoff):
    subjects = {}
    for _, title, topic in course_topics:
        subjects.setdefault(topic, set()).add(title)
    legacy = {j['kp_id']: j for j in historical_jobs}
    order = {j['kp_id']: i for i,j in enumerate(historical_jobs)}
    items = {}
    for kp, title, topic, topic_title, script in registrations:
        old = legacy.get(kp, {})
        known = [dates[p] for p in [script, old.get('script')] if p in dates]
        built = min(known) if known else None
        if not in_cohort(built, cutoff):
            continue
        items[kp] = {'kp':kp,'title':title,'topic':topic,'topic_title':topic_title,
            'initial_registration':script,'first_built_at':built,
            'age_evidence':'git_first_seen' if known else 'unknown_included',
            'priority_subjects':sorted(subjects.get(topic, set())),
            'original_order':order.get(kp, len(order)),'state':'pending'}
    return sorted(items.values(), key=lambda r:(not bool(r['priority_subjects']),r['original_order'],r['kp']))


def current_approval(snapshot, math_root):
    script = (snapshot.get('registered_generator') or {}).get(':question-generator/script','')
    parts = Path(script).parts
    if len(parts) < 4 or parts[0] != 'generators':
        return None
    path = Path(math_root)/'generators/approvals'/parts[2]/f'{snapshot["kp_id"]}.json'
    if not path.is_file():return None
    try:
        certificate = read(path)
        identity = {**source_identity(snapshot),'package_sha256':parts[2],'registration':script}
        if certificate.get('format') != 1 or certificate.get('identity') != identity:return None
        bands=[]
        for band, approval in certificate.get('bands',{}).items():
            if approval.get('review_policy_version') != REVIEW_POLICY_VERSION or not approval.get('publication',{}).get('passed'):continue
            evidence=Path(approval.get('evidence',''))
            if not evidence.is_file():continue
            result=read(evidence);validate_review(result,evidence.parent)
            if result.get('verdict')=='accepted' and digest(result)==approval.get('review_sha256'):
                bands.append(band)
        return {'path':str(path),'bands':sorted(bands),'registration':script} if bands else None
    except (OSError,ValueError,KeyError,TypeError):
        return None


def mechanical_package(script, workspace, source):
    """Copy the existing script/resource closure without changing its code.

    Explicit resource trees preserve Path(__file__).with_suffix('') layouts.
    Relocation and the independent review still must establish completeness.
    Unresolved imports/paths become repair findings, never silent omissions.
    """
    script=Path(script).resolve();workspace=Path(workspace);workspace.mkdir(parents=True,exist_ok=True)
    files=set();imports=set();pending=[(script,Path(script.name),True)];seen=set();parsed=set()
    resource=script.with_suffix('')
    if resource.is_dir():
        for path in resource.rglob('*'):
            if path.is_file() and not any(p in {'__pycache__','.git','.venv'} for p in path.relative_to(resource).parts):
                pending.append((path,Path(resource.name)/path.relative_to(resource),False))
    while pending:
        original,name,analyze=pending.pop()
        if original.is_symlink():raise ValueError('Runtime symlink needs explicit packaging: '+str(original))
        if name.as_posix() not in seen:
            seen.add(name.as_posix());target=workspace/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(original,target);files.add(name.as_posix())
        if not analyze or original.suffix!='.py' or name.as_posix() in parsed:continue
        parsed.add(name.as_posix())
        tree=ast.parse(original.read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.endswith(('.json','.csv','.svg','.png','.ttf','.woff2')):
                candidate=original.parent/node.value
                if candidate.is_file() and not Path(node.value).is_absolute() and '..' not in Path(node.value).parts:
                    pending.append((candidate,name.parent/node.value,False))
            names=[a.name for a in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) and node.module else []
            for module in names:
                top=module.split('.')[0]
                if top in sys.stdlib_module_names or top=='__future__':continue
                candidates=[(original.parent/(top+'.py'),name.parent/(top+'.py')),
                    (ROOT/'scripts'/f'{top}.py',Path(f'{top}.py')),
                    (ROOT/'scripts/question_capture'/f'{top}.py',Path(f'{top}.py'))]
                found=next(((p,n) for p,n in candidates if p.is_file()),None)
                if found:pending.append((*found,True))
                else:imports.add(top)
    packages={}
    mapping=importlib.metadata.packages_distributions()
    local={Path(f).stem for f in files if '/' not in f and f.endswith('.py')}
    for name in sorted(imports-local):
        distributions=mapping.get(name,[])
        if not distributions:raise ValueError('Undeclared/unresolved runtime import: '+name)
        for distribution in distributions:packages[distribution]=importlib.metadata.version(distribution)
    bands=source.get('available_difficulties',[])
    default=next((b for b in ['easy','moderate','hard'] if b in bands),None)
    if default is None:raise ValueError('Source has no calibrated difficulty; classification needs repair')
    manifest={'entrypoint':script.name,'files':sorted(files),
        'dependencies':{'python':platform.python_version(),'packages':packages},'default_difficulty':default}
    save(workspace/'package.json',manifest)
    return manifest


class CohortPipeline(Pipeline):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if isinstance(self.session,CodexSession):
            self.session=CohortSession(self.root,self.environment)

    def repair_inventory(self, evidence=None):
        """Resolve reviewed historical defects before reviewing fresh delivery.

        Reports must come from an independently validated reviewer associated
        with this source. Authors cannot nominate arbitrary database changes.
        Retirement uses the existing exact-request/preview/readback transport.
        """
        roots=set()
        if evidence is not None:
            previous=self.state.get('previous_review',{})
            if (Path(previous.get('directory','')).resolve()!=Path(evidence).resolve()
                    or previous.get('binding',{}).get('source_hash')!=self.state.get('source_hash')):
                raise ValueError('Inventory repair requires a review bound to this instructional source')
            roots.add(Path(evidence).resolve())
        history=self.directory/'repair-history.json'
        if history.exists():
            for row in read(history)['findings']:
                if (row['finding']['kind']=='inventory' and row.get('source_hash')==self.state.get('source_hash')
                        and row.get('review_directory')):
                    roots.add(Path(row['review_directory']).resolve())
        reports=[];inputs=[]
        for root in sorted(roots):
            if root.parent!=self.directory or not root.name.startswith('review-'):
                raise ValueError('Inventory repair requires this job\'s independent review evidence')
            validate_review(read(root/'result.json'),root)
            report=root/'affected-inventory.json'
            if not report.is_file() or not read(report).get('affected_questions'):continue
            reports.append(report)
            inputs.append({'report':str(report.relative_to(self.directory)),'sha256':digest(read(report))})
        if not reports:return None
        key=digest(inputs)
        previous=self.state.get('pool_repair',{})
        if self.state.get('pool_repair_input')==key and not previous.get('unresolved'):
            return {**previous,'inventory_changed':False}
        if (self.directory/'publication/request.json').exists():
            raise ValueError('Resolve the saved publication request before changing inventory review inputs')
        from generator_pool_repair import repair_pool
        directory=self.directory/'pool-repair'
        directory.mkdir(exist_ok=True)
        inventory_path=self.directory/'source/inventory.json'
        before=read(inventory_path)
        baseline=directory/('inventory-before-'+digest(before)+'.json')
        if not baseline.exists():save(baseline,before)
        result=repair_pool(self.publisher,self.state['request']['kp'],reports,directory)
        inventory=self.publisher.extract_inventory(self.state['request']['kp'],inventory_path.parent)
        source=read(self.directory/'source/source.json')
        if any(inventory.get(k)!=source.get(k) for k in ('database','lineage','kp_id')):
            raise ValueError('Repaired inventory does not match the instructional source identity')
        changed=digest(inventory)!=digest(before)
        result={**result,'inventory_changed':changed,'baseline':str(baseline),
                'reports':[str(p) for p in reports],'inventory_sha256':digest(inventory)}
        save(directory/'review-handoff.json',result)
        self.persist(pool_repair=result,pool_repair_input=key,inventory_hash=digest(inventory),
                     approval_recorded=False)
        return result

    def block_inventory(self, result):
        self.block('inventory_repair_blocked',{
            'owner':'inventory',
            'error':'Stored-question repair needs intervention; see pool-repair/verification.json.',
            'unresolved':result.get('unresolved',[])},'validate')

    def review_candidate(self, evidence):
        result=super().review_candidate(evidence)
        # An accepted report may still list demonstrated historical defects.
        # Complete those repairs and review the changed delivery snapshot before
        # allowing publication; never repair after declaring the job verified.
        if result is not None and result['verdict']=='accepted':
            repaired=self.repair_inventory(evidence)
            if repaired and repaired.get('unresolved'):
                self.block_inventory(repaired)
                return None
            if repaired and repaired['inventory_changed']:
                self.persist(stage='validate',needs_repair=True)
                return None
        return result

    def repair(self, reason):
        findings=reason.get('findings',[])
        if not any(row.get('kind')=='inventory' for row in findings):
            return super().repair(reason)
        self.remember_repair(reason)
        repaired=self.repair_inventory()
        if not repaired or repaired.get('unresolved'):
            self.block_inventory(repaired or {'unresolved':['Missing reviewed affected-inventory.json evidence']})
            return
        content=[row for row in findings if row.get('kind')!='inventory']
        if content:
            return super().repair({**reason,'findings':content})
        if not repaired['inventory_changed']:
            self.block_inventory({'unresolved':['Review still rejects inventory already repaired; no delivery evidence changed.']})
            return
        # Inventory-only fixes do not require a runtime code change. Retain all
        # actual generator counterexamples, then independently review the newly
        # captured eligible pool under a different inventory binding.
        self.check_repair_regressions()
        self.sample()
        self.persist(stage='validate',package_hash=self.candidate_hash(),needs_repair=True)

    def sample(self):
        root,manifest=self.manifest()
        default=self.state.get('adopted_default_difficulty')
        if self.state['request']['difficulty']=='unclassified' and manifest.get('default_difficulty') not in {'easy','moderate','hard'} and default in {'easy','moderate','hard'}:
            # Preserve the source-calibrated adoption metadata if a repair
            # rewrites the packaging manifest but omits this nonruntime field.
            manifest['default_difficulty']=default
            save(root/Path(self.state['manifest']).name,manifest)
        return super().sample()

    def publication_records(self):
        source=read(self.directory/'source/source.json')
        script=(source.get('registered_generator') or {}).get(':question-generator/script','')
        parts=Path(script).parts
        if len(parts)>=4 and parts[0]=='generators' and parts[2]==self.state['package_hash']:
            # Local samples still bind the review. The existing immutable
            # registration can be verified without publishing another batch.
            return []
        return super().publication_records()

    def context(self, evidence):
        context=super().context(evidence)
        context['retrospective_review']={
            'purpose':'Review an existing generator for structural bypasses; repair only demonstrated failures.',
            'cohort_cutoff':DEFAULT_CUTOFF,
            'existing_pool':'Also inspect inventory_file for already stored instances of any demonstrated weakness. Report historical stored-pool defects as kind inventory, separately from runtime generator findings. Save affected-inventory.json as {"affected_questions": [{"question_id":"UUID", "entity_id":123, "finding":"specific defect", "reproduction":"exact command/parameters", "evidence_path":"generated-records.json"}]}. evidence_path must be relative to evidence_root and contain reproduced complete generated records with question/id and generation metadata matching the stored question. The runner repairs proven eligible stored records, refreshes inventory, and requests a new independent review before publication. Retired questions are preserved history, not selectable practice; check actual eligibility. An empty array means none demonstrated; distinguish untested inventory from a verified absence. Do not modify the database or mark original source questions as generated.',
            'engine_limitations':'Do not remove source families or constrain valid learner notation to conceal an engine limitation. Retain strict failing acceptance/rejection tests and identify the missing engine capability.'}
        return context


def report(directory, campaign):
    counts=Counter(item['state'] for item in campaign['items'])
    active_jobs=[]
    for item in campaign['items']:
        if item['state']!='running':continue
        entry=dict(item)
        job=directory/'jobs'/str(item['kp'])/'job.json'
        if job.exists():entry['pipeline_stage']=read(job).get('stage')
        active_jobs.append(entry)
    value={'cutoff':campaign['cutoff'],'captured_basis':campaign['captured_basis'],
        'total':len(campaign['items']),'states':dict(counts),
        'priority_total':sum(bool(i['priority_subjects']) for i in campaign['items']),
        'worker_count':campaign.get('worker_count',1),'active_jobs':active_jobs,
        'active':active_jobs[0] if active_jobs else None,'updated':time.time()}
    if active_jobs:value['active_pipeline']=active_jobs[0].get('pipeline_stage')
    if campaign.get('capacity_error'):value['capacity_error']=campaign['capacity_error']
    if campaign.get('campaign_error'):value['campaign_error']=campaign['campaign_error']
    value['blocked_jobs']=[{'kp':item['kp'],'state':item['state'],'error':item.get('error')}
        for item in campaign['items'] if item['state'] in {'needs_repair','failed','blocked'}]
    save(directory/'status.json',value)
    return value


class CampaignStore:
    """Serialize short state changes; hold normal KP locks throughout real work."""
    def __init__(self,directory):
        self.directory=Path(directory).resolve()
        self.path=self.directory/'cohort.json'

    @contextmanager
    def locked(self):
        with (self.directory/'cohort.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            yield read(self.path)

    def write(self,campaign):
        # Only called while locked, including report's shared atomic temp file.
        save(self.path,campaign)
        return report(self.directory,campaign)

    def status(self):
        with self.locked() as campaign:return report(self.directory,campaign)

    def update(self,item,**campaign_updates):
        with self.locked() as campaign:
            target=next(i for i in campaign['items'] if i['kp']==item['kp'])
            target.update(item)
            campaign.update(campaign_updates)
            return self.write(campaign)

    def resume(self,kp,reason):
        """Explicitly rearm one repaired job without starting any workers."""
        if not isinstance(reason,str) or not reason.strip():
            raise ValueError('Resume requires a nonempty reason describing the repair')
        with self.locked() as campaign:
            item=next((i for i in campaign['items'] if i['kp']==kp),None)
            if item is None:raise ValueError('Knowledge point is not in this cohort')
            if item['state'] not in {'blocked','needs_repair','failed'}:
                raise ValueError('Only a blocked or failed cohort item can be resumed')
            directory=self.directory/'jobs'/str(kp)
            with (directory/'worker.lock').open('a') as lock:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                state=read(directory/'job.json')
                pipeline=CohortPipeline(directory,state['request'],None,max_attempts=item.get('max_attempts',3))
                pipeline.resume_blocked(reason)
            item.update(state='pending',error=None,resumed=time.time(),resume_reason=reason.strip())
            if campaign.get('campaign_error',{}).get('kp')==kp:
                campaign.pop('campaign_error',None)
            return self.write(campaign)

    def claim(self,locks,slot):
        with self.locked() as campaign:
            if ((self.directory/'stop-after-current').exists() or campaign.get('capacity_error')
                    or campaign.get('campaign_error')):return None
            blocked=next((item for item in campaign['items']
                if item['state'] in {'needs_repair','failed','blocked'}),None)
            if blocked is not None:
                campaign['campaign_error']={'kp':blocked['kp'],'state':blocked['state'],
                    'error':blocked.get('error'),'stopped':time.time(),
                    'instruction':'A saved failure requires explicit repair and resume.'}
                self.write(campaign)
                return None
            for item in campaign['items']:
                if item['state'] in TERMINAL:continue
                kp_lock=(locks/f'kp-{item["kp"]}.lock').open('a')
                try:fcntl.flock(kp_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                except BlockingIOError:
                    kp_lock.close()
                    continue
                # A running entry is recoverable only after its actual process
                # (and any inherited agent descriptors) releases the KP lock.
                claimed=dict(item)
                claimed.update(state='running',started=item.get('started',time.time()),
                    claimed=time.time(),worker_slot=slot,worker_pid=os.getpid())
                try:
                    item.update(claimed)
                    self.write(campaign)
                except BaseException:
                    kp_lock.close()
                    raise
                return claimed,kp_lock
        return None


def slot_lock_path(directory,slot):
    if slot not in range(3):raise ValueError('Worker slot must be 0, 1 or 2')
    # Preserve the legacy worker's exclusion lock during upgrades.
    return directory/('worker.lock' if slot==0 else f'worker-{slot}.lock')


def process_item(directory,item,publisher,worker,kp_lock,store):
    jobdir=directory/'jobs'/str(item['kp']);jobdir.mkdir(parents=True,exist_ok=True)
    try:
        job=jobdir/'job.json'
        if job.exists():
            state=read(job)
            pipeline=CohortPipeline(jobdir,state['request'],publisher,environment=publisher.client.environment,
                max_attempts=item.get('max_attempts',3))
        else:
            source=publisher.extract_source(item['kp'],jobdir/'source');save(jobdir/'source/source.json',source)
            approval=current_approval(source,publisher.config.math_root)
            if approval:
                item.update(state='skipped_current',approval=approval,completed=time.time());store.update(item);return
            script=(source.get('registered_generator') or {}).get(':question-generator/script')
            if not script:
                item.update(state='blocked',error='No current registered generator; do not invent a new cohort member.',completed=time.time());store.update(item);return
            existing=None if script.startswith('generators/') else str(resolve_registered_script(script,ROOT,publisher.config.math_root))
            request={'kp':item['kp'],'difficulty':'unclassified','count':5,'existing_entrypoint':existing,'job_kind':'build'}
            pipeline=CohortPipeline(jobdir,request,publisher,environment=publisher.client.environment)
            pipeline.persist(source_hash=digest(source),inventory_hash=digest(read(jobdir/'source/inventory.json')))
            try:
                if script.startswith('generators/'):pipeline.load_registered_package(script)
                else:
                    mechanical_package(existing,jobdir/'workspace',source)
                    pipeline.persist(manifest='package.json')
                pipeline.persist(adopted_default_difficulty=pipeline.manifest()[1].get('default_difficulty'))
                pipeline.sample();pipeline.persist(stage='validate',package_hash=pipeline.candidate_hash())
            except (OSError,ValueError,RuntimeError) as error:
                pipeline.repair({'code':'legacy_packaging_or_sampling','error':str(error),'instruction':'Repair the existing runtime closure or concrete sample failure. Preserve the original assessed skill.'})
        # Protect both slot and KP until the actual agent child exits.
        pipeline.inherited_lock_fds=(worker.fileno(),kp_lock.fileno())
        result=pipeline.run('push')
        # A returned repair/blocked stage exhausted a durable pipeline budget or
        # needs another owner. Calling run again cannot change that condition.
        state='verified' if result['stage']=='verified' else 'blocked'
        item.update(state=state,pipeline=str(job),error=result.get('error'),registration=result.get('registration'),completed=time.time())
        if state=='blocked' and not item['error']:
            item['error']={'code':'pipeline_incomplete','stage':result['stage'],
                           'error':'Pipeline stopped before verification; explicit repair and resume are required.'}
        if state=='verified':
            pool_reports=list(jobdir.glob('review-*/affected-inventory.json'))
            item['pool_review_reports']=[str(p) for p in pool_reports]
            if result.get('pool_repair'):item['pool_repair']=result['pool_repair']
    except CapacityUnavailable as error:
        item.update(state='pending',error=str(error),interrupted=time.time())
        store.update(item,capacity_error=str(error))
        print(str(error),flush=True);return
    except Exception as error:
        item.update(state='failed',error=str(error),completed=time.time())
    updates={}
    if item['state'] in {'needs_repair','failed','blocked'}:
        updates['campaign_error']={'kp':item['kp'],'state':item['state'],
            'error':item.get('error'),'stopped':time.time(),
            'instruction':'Fix the saved blocker and explicitly resume; no new jobs will be claimed.'}
    store.update(item,**updates)
    print(json.dumps({'kp':item['kp'],'state':item['state'],'worker_slot':item['worker_slot'],'error':item.get('error')},default=str),flush=True)


def run(directory,slot=0):
    directory=Path(directory).resolve();store=CampaignStore(directory)
    with slot_lock_path(directory,slot).open('a') as worker:
        fcntl.flock(worker,fcntl.LOCK_EX)
        save(directory/f'worker-{slot}.json',{'pid':os.getpid(),'slot':slot,'started':time.time()})
        publisher=Publisher.from_environment()
        with store.locked() as campaign:
            locks=ROOT/'.local/learning/inventory'/publisher.config.database/campaign['learner']
        locks.mkdir(parents=True,exist_ok=True)
        while True:
            claim=store.claim(locks,slot)
            if claim is None:break
            item,kp_lock=claim
            with kp_lock:process_item(directory,item,publisher,worker,kp_lock,store)
        status=store.status()
        return STOP_EXIT if status.get('campaign_error') or status.get('capacity_error') else 0


def supervise(directory,workers):
    """Restart interrupted slots independently without disturbing healthy jobs."""
    if workers not in range(1,4):raise ValueError('Worker count must be 1, 2 or 3')
    directory=Path(directory).resolve()
    with (directory/'supervisor.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        store=CampaignStore(directory)
        with store.locked() as campaign:
            campaign['worker_count']=workers
            store.write(campaign)
        children={};retry={slot:0 for slot in range(workers)}
        restarts=Counter();stopped=False
        while retry or children:
            for slot,deadline in list(retry.items()):
                if time.monotonic()<deadline:continue
                children[slot]=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),
                    'run','--directory',str(directory),'--slot',str(slot)])
                del retry[slot]
            for slot,child in list(children.items()):
                code=child.poll()
                if code is None:continue
                del children[slot]
                if code==STOP_EXIT:
                    stopped=True;retry.clear()
                elif code and not stopped:
                    restarts[slot]+=1
                    if restarts[slot]>MAX_WORKER_RESTARTS:
                        with store.locked() as campaign:
                            campaign['campaign_error']={'worker_slot':slot,'exit_code':code,
                                'error':'Worker restart limit exhausted','restarts':MAX_WORKER_RESTARTS}
                            store.write(campaign)
                        stopped=True;retry.clear()
                        continue
                    print(json.dumps({'worker_slot':slot,'exit_code':code,'restart_in_seconds':15}),flush=True)
                    retry[slot]=time.monotonic()+15
            if retry or children:time.sleep(1)
        return STOP_EXIT if stopped else 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['init','run','status','resume'])
    parser.add_argument('--directory',type=Path,required=True)
    parser.add_argument('--cutoff',default=DEFAULT_CUTOFF)
    parser.add_argument('--workers',type=int,choices=range(1,4),default=1)
    parser.add_argument('--slot',type=int,choices=range(3))
    parser.add_argument('--kp',type=int,help='One blocked knowledge point to explicitly resume')
    parser.add_argument('--resume-reason',help='Describe the completed change that resolves its saved blocker')
    args=parser.parse_args();directory=args.directory.resolve()
    if args.action=='init':
        path=directory/'cohort.json'
        if path.exists():raise ValueError('Cohort is immutable; resume it instead of overwriting')
        inv=directory/'inventory';identity=read(inv/'identity.json')
        cutoff=datetime.fromisoformat(args.cutoff).timestamp()
        items=build_cohort(read(inv/'registered.json'),read(inv/'priority-course-topics.json'),
            read(ROOT/'generate/runs/current/manifest.json')['jobs'],first_seen((inv/'git-first-seen.txt').read_text()),cutoff)
        learners=list((ROOT/'.local/learning/inventory'/identity['database']).iterdir())
        learners=[p.name for p in learners if p.is_dir() and (p/'cursor.json').exists()]
        if len(learners)!=1:raise ValueError('Select the intended learner lock namespace explicitly')
        campaign={'cutoff':args.cutoff,'captured_basis':identity['basis'],'lineage':identity['lineage'],'learner':learners[0],'created':time.time(),'items':items}
        save(path,campaign);print(json.dumps(report(directory,campaign)))
    elif args.action=='run':
        if args.slot is not None:raise SystemExit(run(directory,args.slot))
        else:raise SystemExit(supervise(directory,args.workers))
    elif args.action=='resume':
        if args.kp is None or not args.resume_reason:parser.error('resume requires --kp and --resume-reason')
        print(json.dumps(CampaignStore(directory).resume(args.kp,args.resume_reason),indent=2))
    else:print(json.dumps(CampaignStore(directory).status(),indent=2))


if __name__=='__main__':main()
