"""Self-contained provenance guard bundled with repaired generator runtimes."""
from functools import wraps
import hashlib
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys

from ca_source_policy import reject_excluded_sources, source_references


class ExcludedSource(ValueError):
    pass


def _policy(path):
    return json.loads(Path(path).read_text())


def _records(value):
    if isinstance(value,dict) and isinstance(value.get('question'),dict):
        return [value]
    if isinstance(value,list):
        return [r for r in value if isinstance(r,dict) and isinstance(r.get('question'),dict)]
    if isinstance(value,dict) and isinstance(value.get('instances'),list):
        return _records(value['instances'])
    return []


def check(value,policy):
    records=_records(value)
    for record in records:
        generation=record.get('generation',{})
        # A reviewed independent family may have overinclusive historical
        # citations. Its replacement support is explicit and retained in policy.
        support=policy.get('independent_support',{}).get(str(generation.get('template')))
        if support and not generation.get('replay_only') and not generation.get('evidence_only'):
            generation['source_ids']=support['source_ids']
            generation['source_eligibility_support']=support['justification']
        try:reject_excluded_sources([record],policy['excluded'])
        except ValueError as error:raise ExcludedSource(str(error)) from error
    return value


def install(namespace,policy_file):
    """Guard public record/batch APIs; original archive packages stay unchanged."""
    policy=_policy(policy_file)
    blocked={str(row[k]) for row in policy['excluded'] for k in (':db/id',':question/id',':question/math-academy-id') if k in row}
    selectors=('PROFILES','TEMPLATES','FAMILIES','CASES','SPECS','MODELS','BASE','DATA','LEVELS','LEVEL','NORMAL','FAMILY_IDS','SOURCE_REFERENCES','SOURCE_IDS','SOURCES','ORIGINALS','QUESTIONS','BY_ID')
    removed=set()
    def tied(value):
        if isinstance(value,(str,int)):return str(value) in blocked or str(value) in removed
        if isinstance(value,(tuple,list)):return any(tied(v) for v in value)
        if isinstance(value,dict):
            if value.get(':question/math-academy-id') in blocked:return True
            refs=source_references({'generation':value})
            return bool(refs & blocked)
        return False
    # Prune runtime dispatch tables; on-disk source evidence stays unchanged.
    # Propagate explicitly tied family names to level/normal selectors.
    for _ in range(3):
        for name in selectors:
            value=namespace.get(name)
            if isinstance(value,dict):
                for key,entry in list(value.items()):
                    if str(key) in blocked or str(key) in removed or (name not in ('LEVELS','NORMAL') and tied(entry)):
                        removed.add(str(key));del value[key]
                for key,entry in list(value.items()):
                    if name in ('LEVELS','NORMAL') and isinstance(entry,list):value[key]=[v for v in entry if not tied(v)]
            elif name in ('CASES','TEMPLATES','FAMILIES') and isinstance(value,(list,tuple)):
                kept=[]
                for entry in value:
                    if tied(entry):
                        if isinstance(entry,(list,tuple)) and entry:removed.add(str(entry[0]))
                    else:kept.append(entry)
                namespace[name]=type(value)(kept)
    for name,fn in list(namespace.items()):
        if not inspect.isfunction(fn) or not (name.startswith('generate') or name in ('batch','make_record')):
            continue
        if getattr(fn,'_source_guarded',False):continue
        def wrap(original):
            @wraps(original)
            def guarded(*args,**kwargs):
                band=kwargs.get('difficulty',kwargs.get('level',args[0] if args else None))
                if band in policy.get('unsupported_bands',[]):
                    raise ExcludedSource('No eligible standalone source family in band '+str(band))
                for key in ('template','profile','source_id'):
                    if str(kwargs.get(key)) in blocked|removed:
                        raise ExcludedSource('Excluded standalone template: '+str(kwargs[key]))
                try:result=original(*args,**kwargs)
                except KeyError as error:
                    if str(error.args[0]) in blocked|removed:raise ExcludedSource('Excluded standalone template: '+str(error.args[0])) from error
                    raise
                except IndexError as error:
                    if 'empty sequence' in str(error):raise ExcludedSource('No eligible standalone source family in this band') from error
                    raise
                return check(result,policy)
            guarded._source_guarded=True
            return guarded
        namespace[name]=wrap(fn)


def cli(entrypoint,policy_file):
    """Filter/resample the existing seeded CLI without reimplementing its math."""
    policy=_policy(policy_file);argv=sys.argv[1:]
    def value(key,default):
        if key in argv:return argv[argv.index(key)+1]
        return default
    count=int(value('--count','1'));seed=int(value('--seed','0'));fmt=value('--format','json')
    if value('--difficulty',value('--level','')) in policy.get('unsupported_bands',[]):
        raise SystemExit('No eligible standalone source family in this difficulty band')
    output=value('--output',None)
    explicit=any(k in argv for k in ('--template','--profile','--parameters','--source-id'))
    def command(n=None,s=None):
        args=list(argv)
        if '--output' in args:
            pos=args.index('--output');del args[pos:pos+2]
        for key,val in [('--count',str(n)),('--seed',str(s)),('--format','json')]:
            if val=='None':continue
            if key in args:args[args.index(key)+1]=val
            else:args.extend([key,val])
        env=os.environ.copy();env['_CA_SOURCE_POLICY_CHILD']='1'
        return subprocess.run([sys.executable,str(entrypoint),*args],env=env,capture_output=True,text=True)
    first=command();rows=[];seen=set();last_error='';envelope=None
    def emit(records):
        if fmt=='json':
            result={**envelope,'instances':records} if envelope is not None else records
            payload=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
        else:
            pieces=[]
            for r in records:
                q=r['question'];text=q[':question/problem']
                for f in q[':question/answer-fields']:
                    for a in f[':answer-field/choices']:text+='\n\n- $'+a[':answer/value']+'$'
                pieces.append(text+'\n\n'+q.get(':question/worked-solution',''))
            payload='\n\n---\n\n'.join(pieces)+'\n'
        if output:Path(output).write_text(payload)
        else:sys.stdout.write(payload)
    if first.returncode==0:
        try:
            original=json.loads(first.stdout)
            if isinstance(original,dict) and isinstance(original.get('instances'),list):envelope=original
            values=_records(original)
            if '--count' not in argv and values:count=len(values)
            if values and all(_records(v) for v in values):
                for record in values:check(record,policy)
                emit(values);return  # Preserve all-band and finite-batch semantics.
        except (ValueError,ExcludedSource):pass
    elif not any(word in first.stderr for word in ('ExcludedSource','excluded standalone source')):
        sys.stderr.write(first.stderr);raise SystemExit(first.returncode)
    def retain(result):
        nonlocal last_error
        if result.returncode:
            last_error=result.stderr[-1800:]
            return
        try:values=_records(json.loads(result.stdout))
        except ValueError:
            last_error='Generator did not emit the declared JSON record interface';return
        for record in values:
            try:check(record,policy)
            except ExcludedSource as error:last_error=str(error);continue
            if not _records(record):continue
            generation=record.get('generation',{})
            key=generation.get('mathematical_fingerprint') or generation.get('parameter_fingerprint')
            if not key:key=hashlib.sha256(json.dumps(record['question'],sort_keys=True).encode()).hexdigest()
            if key not in seen:rows.append(record);seen.add(key)
    retain(first)
    if (explicit or value('--difficulty','')=='all') and (first.returncode or len(rows)<count):
        raise SystemExit('Source-eligibility policy rejects this explicit request: '+last_error)
    # Preserve the original batch exactly when eligible. Retry only a batch
    # containing excluded parts; do not fabricate a replacement source family.
    for offset in range(1,max(16,count*16)+1):
        if len(rows)>=count:break
        retain(command(1,seed+offset))
    if len(rows)<count:
        raise SystemExit('Standalone source shortage after excluding multistep/retired templates; '
                         f'found {len(rows)} of {count}. '+last_error)
    rows=rows[:count]
    emit(rows)
