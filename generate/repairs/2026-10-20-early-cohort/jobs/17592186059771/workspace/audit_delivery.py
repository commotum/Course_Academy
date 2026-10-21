"""Inspect shared-filtered records, controlled key changes, inventory and packaging."""
import sys
sys.dont_write_bytecode=True
import shutil,os
from pathlib import Path
from validation_helpers import *
OUT=E/'evidence'
def save(n,x): (OUT/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def read(n):return json.loads((OUT/n).read_text())
def rowsig(r):
    o=ops(r['question'][':question/problem'])
    return [[t,s] for _,t,s,_ in o]
def features(r):
    q=r['question']; f=q[':question/answer-fields'][0]; choices=f[':answer-field/choices'];mats=[mat(a[':answer/value']) for a in choices]
    original=mat(q[':question/problem'])
    scores={
        'norm':[sum(abs(v) for row in m for v in row) for m in mats],
        'zeros':[sum(v==0 for row in m for v in row) for m in mats],
        'unchanged_rows':[sum(a==b for a,b in zip(m,original)) for m in mats],
        'negative_entries':[sum(v<0 for row in m for v in row) for m in mats],
        'integral_entries':[sum(v.denominator==1 for row in m for v in row) for m in mats],
    }
    actual=next(i for i,a in enumerate(choices) if a[':answer/id']==key(q)[':answer/id'])
    return actual,scores

def coverage(records):
    groups={}
    for profile in sorted({r['generation']['profile'] for r in records}):
        group=[r for r in records if r['generation']['profile']==profile]
        observations=[features(r) for r in group]
        result={'count':len(group),'semantic_instances':len({r['generation']['mathematical_fingerprint'] for r in group}),
                'positions':dict(collections.Counter(i for i,_ in observations)),
                'row_roles':dict(collections.Counter(str(rowsig(r)) for r in group)),
                'sampling_attempts':dict(collections.Counter(r['generation']['sampling_attempts'] for r in group))}
        result['cue_successes']={'first_position':sum(i==0 for i,_ in observations)}
        for feature in observations[0][1]:
            for direction,which in [('minimum',min),('maximum',max)]:
                # Count only uniquely predicted choices; ties supply no clue.
                hits=unique=0
                for i,scores in observations:
                    values=scores[feature]; best=which(values)
                    if values.count(best)==1:
                        unique+=1;hits+=values[i]==best
                result['cue_successes'][direction+'_'+feature]={'unique_predictions':unique,'correct':hits,'total':len(group)}
        groups[profile]=result
    return groups

stages={}
for d in ['easy','hard']:
    raw=read(d+'-records.json');accepted=read('delivery-'+d+'/accepted.json')
    stages[d]={'raw':coverage(raw),'accepted':coverage(accepted),
               'delivered_math_failures':[verify(r) for r in accepted if not all(verify(r)[k] for k in ['key_correct','unique_correct','five_unique','solution_final_correct'])]}
    assert not stages[d]['delivered_math_failures']
    assert set(stages[d]['raw'])==set(stages[d]['accepted'])
# With fixed input entries, each of the five distinct hard responses remains eligible
# under either relationship, AFTER actual normalization/deduplication.
controls=read('control-records.json');accepted=read('delivery-hard/accepted.json')
controlled=[]
delivered_grader=[]
for start,label in [(0,'shared-target'),(7,'shared-donor')]:
    originals=controls[start:start+5]
    # Normalization can change owned UUIDs; identify by generation fingerprint.
    group=[next(r for r in accepted if r['generation']['mathematical_fingerprint']==o['generation']['mathematical_fingerprint']) for o in originals]
    banks=[sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']) for r in group]
    keys={key(r['question'])[':answer/value'] for r in group}
    test={'relationship':label,'all_five_survived':len(group)==5,'same_bank':all(x==banks[0] for x in banks),'distinct_correct_responses':len(keys),
          'bank_only_shortcut_bound':'Any deterministic strategy using only this fixed matrix and unordered bank can answer at most one of the five controlled tasks.'}
    assert test['same_bank'] and len(keys)==5
    controlled.append(test)
    delivered_grader.extend(group)

# The exact five-item requested-band batch also passes the shared filtering path.
batch=read('batch-records.json')
batch_ids={r['generation']['mathematical_fingerprint'] for r in batch}
passed_batch=[r for r in read('delivery-easy/accepted.json') if r['generation']['mathematical_fingerprint'] in batch_ids]
assert len(passed_batch)==5
delivered_grader.extend(passed_batch)
gcases=read('grader-input.json')
for i,r in enumerate(delivered_grader):
    q=r['question']; expected=calc(q)
    gcases.append({'label':'after delivery '+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if mat(a[':answer/value'])==expected else 'rejected','purpose':'Independent arithmetic after delivery normalization'} for a in q[':question/answer-fields'][0][':answer-field/choices']]})
save('combined-grader-input.json',gcases)
save('shortcut-results.json',{'stages':stages,'controlled_hard_after_delivery':controlled,'exact_batch':coverage(passed_batch),
    'interpretation':'No profile or role relationship fixes the answer. Positions and unique extrema are measured per recognizable production profile. Small samples are descriptive; controlled fixed-bank key changes establish that bank-only cues cannot be universal.',
    'limits':['No claim about every conceivable strategy or a learner-specific live sequence.','Reading one decisive coordinate can legitimately eliminate distractors; the task does not require proving every coordinate independently.']})

inv=json.loads((J/'source/inventory.json').read_text())
originals=[q for q in inv['questions'] if ':question/math-academy-id' in q]
other=[q for q in inv['questions'] if ':question/math-academy-id' not in q]
inspection={'basis':inv['basis'],'captured_questions':len(inv['questions']),'source_questions':len(originals),'other_questions':len(other),
    'generation_metadata_available':any('generation' in q or any('generation' in k for k in q) for q in other),
    'assessment':'Both demonstrated findings are omissions in generator support. Neither establishes an incorrect stored instance. Eleven original sources include the previously unsupported banks and operation cases; these are not relabeled as generated.',
    'limits':'The sixteen other captured records have no generation metadata. They are not reproduced or certified defect-free; matching historical generated records cannot be established from this capture.'}
summaries=[]
for q in inv['questions']:
    text=q[':question/problem']
    if '↔' in text or r'\leftrightarrow' in text: family='single-row-swap'
    elif 'following row operations' in text:
        destinations=re.findall(r'\{R\}_\{(\d)\}\s*&\s*:=',text)
        family='hard-shared-target' if len(set(destinations))==1 else 'hard-shared-donor' if len(set(destinations))==2 else 'hard-unparsed'
    else: family='single-row-arithmetic'
    summaries.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'visible_family':family})
inspection['visible_family_counts']=dict(collections.Counter(q['visible_family'] for q in summaries))
inspection['question_summaries']=summaries
save('inventory-inspection.json',inspection)
(E/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2)+'\n')
# Inspect the selected band with the actual selection algorithm, conditional on a
# positive configured weight and unseen/usable records. No database reads needed.
existing=[q for q in inv['questions'] if q[':question/difficulty'][':db/ident'].endswith('/easy')]
ids=sorted({q[':db/id'] for q in existing})
def select(seed):
    digest=hashlib.sha256(('course-academy/question-selection/v1/'+str(seed)).encode()).digest()
    u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
    return ids[int(u*len(ids))]
counts=collections.Counter(select(i) for i in range(64))
save('selection-results.json',{'implementation':'engine/rust/question_selection.rs:107-192 inspected read-only',
    'conditional_easy_draws':dict(counts),'trials':64,'easy_candidate_ids':ids,
    'rule':'Configured positive bands are weighted first; sorted fresh usable entity IDs within the chosen band are selected by a SHA-256 uniform draw. Previous tasks are excluded separately. An unconfigured policy returns the first eligible ID.',
    'limits':['No live policy, learner history, future entity IDs or publication state is available. No claim that all bands receive positive live weight.','Shared delivery filters verify captured inventory and difficulty only; they do not execute live learner selection.']})

manifest=json.loads((E/'package.json').read_text())
assert manifest['dependencies']=={'python':platform.python_version(),'packages':{}}
assert 'package.json' not in manifest['files']
assert all(not Path(f).is_absolute() and '..' not in Path(f).parts and (E/f).is_file() for f in manifest['files'])
rel=OUT/'relocated';rel.mkdir(exist_ok=True)
for f in manifest['files']:
    dest=rel/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(E/f,dest)
env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str((OUT/'assets').resolve()),'PYTHONDONTWRITEBYTECODE':'1'}
env.pop('PYTHONPATH',None)
checks=[]
for d,profile in [('easy',None),('hard',None),('easy','q-10251'),('moderate','q-10243')]:
    args=['--difficulty',d,'--count','1' if profile else '5','--seed','20261021','--format','json']
    if profile:args+=['--profile',profile]
    command=[PY,'-B',str(rel/'generator.py'),*args]
    a=subprocess.run(command,cwd=OUT,env=env,capture_output=True,text=True,check=True)
    b=subprocess.run([PY,'-B',str(E/'generator.py'),*args],cwd=OUT,env=env,capture_output=True,text=True,check=True)
    assert json.loads(a.stdout)==json.loads(b.stdout)
    checks.append({'command':command,'relocation_equal':True,'count':len(json.loads(a.stdout))})
save('packaging-results.json',{'python':platform.python_version(),'dependencies':manifest['dependencies'],'runtime_files':manifest['files'],'cli_checks':checks,'passed':True,'writes':'No generated assets are needed; records are returned on stdout. Test outputs stay under workspace/evidence.'})
print(json.dumps({'profiles_after_delivery':{d:list(stages[d]['accepted']) for d in stages},'controlled_after_delivery':controlled,'packaging_checks':len(checks),'affected_inventory':0,'inventory_limit':inspection['limits']},default=str))
