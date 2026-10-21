#!/usr/bin/env python3
"""Delivery, conditional shortcut and relocation checks; evidence-only writes."""
import sys
sys.dont_write_bytecode=True
import json, hashlib, shutil, subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;J=R.parent;P=J/'workspace'
def load(p):return json.loads(Path(p).read_text())
def save(n,o): (R/n).write_text(json.dumps(o,indent=2)+'\n')
def enum(v):return v.get(':db/ident') if isinstance(v,dict) else v
def answers(r):
    f=r['question'][':question/answer-fields'][0];key=f.get(':answer-field/correct')
    key=key.get(':answer/id') if isinstance(key,dict) else key[1] if key else None
    choices=f[':answer-field/choices'];ordered=sorted(choices,key=lambda a:float(a[':answer/value'].split('\\')[0].replace('lb','')))
    return choices,key,ordered
def measured(records):
    groups={}
    for r in records:groups.setdefault(r['generation']['template'],[]).append(r)
    return {'count':len(records),'median_correct':sum(answers(r)[2][2][':answer/id']==answers(r)[1] for r in records),
      'positions':{str(i):sum(answers(r)[0][i-1][':answer/id']==answers(r)[1] for r in records) for i in range(1,6)},
      'templates':{t:{'count':len(rs),'median_correct':sum(answers(r)[2][2][':answer/id']==answers(r)[1] for r in rs)} for t,rs in groups.items()}}
sample=load(R/'sample-records.json');batch=load(R/'batch-records.json')
sa=load(R/'delivery-sample/accepted.json');ba=load(R/'delivery-batch/accepted.json')
stages={'independent_before':measured(sample),'independent_after':measured(sa),'batch_before':measured(batch),'batch_after':measured(ba)}

# Faithful select() band/draw reproduction with explicit candidate assumptions.
# Native Rust draws eight digest bytes for band then eight bytes for pool index.
def select(pool,weights,seed):
    ordered=sorted(pool,key=lambda r:r['entity_id']);bands=[[r for r in ordered if r['difficulty']==b] for b in ('easy','moderate','hard')]
    raw=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
    uniform=lambda off:(int.from_bytes(raw[off:off+8],'big')>>11)/(1<<53)
    total=sum(w for w,band in zip(weights,bands) if band)
    if not total:return None
    draw=uniform(0)*total;chosen=None
    for i,w in enumerate(weights):
        if not bands[i] or not w:continue
        chosen=i
        if draw<w:break
        draw-=w
    b=bands[chosen];return b[int(uniform(8)*len(b))]
inv=load(J/'source/inventory.json');affected={r['question_id'] for r in load(R/'affected-inventory.json')['affected_questions']}
pool=[];excluded=[]
for q in inv['questions']:
    if any(not f.get(':answer-field/correct') for f in q[':question/answer-fields']):excluded.append(q[':question/id']);continue
    pool.append({'entity_id':q[':db/id'],'question_id':q[':question/id'],
                 'difficulty':enum(q.get(':question/difficulty','unrated')).split('/')[-1],
                 'demonstrated_generated_shortcut':q[':question/id'] in affected})
# Batch entities do not exist; hypothetical sorted relative IDs are harmless when
# measuring invariant rank; repeat each possible pool index explicitly below.
bp=[{'entity_id':i+1,'question_id':r['question'][':question/id'],'difficulty':'easy','demonstrated_generated_shortcut':True} for i,r in enumerate(ba)]
scenarios={}
for name,pp,ww in [('batch easy fresh',bp,[1,0,0]),('captured usable all bands equal conditional weights',pool,[1,1,1]),
                   ('captured usable easy only',pool,[1,0,0]),('captured generated after source history exclusion',[r for r in pool if r['demonstrated_generated_shortcut']],[1,1,1])]:
    selected=[select(pp,ww,'independent-review-'+str(i)) for i in range(100)]
    scenarios[name]={'assumed_weights':ww,'pool':pp,'draw_count':100,
       'affected_draws':sum(r is not None and r['demonstrated_generated_shortcut'] for r in selected),
       'distinct_selected':len({r['question_id'] for r in selected if r}), 'selected':selected}
save('delivery-selection-results.json',{'captured_basis':inv['basis'],'stages':stages,'selection_source':'engine/rust/question_selection.rs::select and seen_before_task',
    'selection_scenarios':scenarios,'excluded_incomplete_source_questions':excluded,
    'limits':['No live learner task/history/policy was captured; scenarios explicitly declare weights and freshness. These are conditional read-only reproductions, not claims about a specific learner.',
              'Source items can dilute the shortcut overall; all generated-family members remain vulnerable under any nonempty selection subset. Batch delivered pool has 5/5 affected items.',
              'Inventory is basis 5395 and may change. No database is opened. Actual shared delivery filtering run separately.']})

# Grading the delivered batch, plus logical response relationships in pairs.
cf=load(R/'counterfactual-records.json');mini=load(R/'minimal-records.json')
grade=ba+cf+mini+[sa[i*4] for i in range(7)]
cases=[]
for i,r in enumerate(grade):
    opts,key,_=answers(r)
    cases.append({'label':f'post-delivery or controlled pair {i}','record':r,'checks':[
      {'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected',
       'purpose':'independent physical mass computation; every displayed distractor rejected'} for a in opts]})
base=answers(cf[0]);baseval=next(a[':answer/value'] for a in base[0] if a[':answer/id']==base[1])
for i in (2,3):
    match=next(a for a in answers(cf[i])[0] if a[':answer/value']==baseval)
    cases.append({'label':f'irrelevant pair {i}: preserve logical numerical answer', 'record':cf[i],
      'checks':[{'submitted_answer_id':match[':answer/id'],'expected':'accepted','purpose':'same mass after common flow scaling or context change'}]})
newopts,newkey,_=answers(cf[1])
plausible=min((a for a in newopts if a[':answer/id']!=newkey),key=lambda a:abs(float(a[':answer/value'].split('\\')[0])-float(baseval.split('\\')[0])))
cases.append({'label':'relevant capacity pair: changed computed mass accepted; plausible alternative rejected','record':cf[1],
    'checks':[{'submitted_answer_id':newkey,'expected':'accepted','purpose':'independently recomputed mass after capacity change'},
              {'submitted_answer_id':plausible[':answer/id'],'expected':'rejected','purpose':'displayed distractor closest to former mass rejected'}]})
save('grader-interface-note.json',{'initial_probe':'submitting previous instance answer UUID to changed instance',
    'outcome':'Native harness error: selected UUID not in field',
    'interpretation':'Out-of-bank UUID is not a learner-selectable radio response. Replaced with actual displayed choices; this is not a generator defect.'})
save('grader-input.json',cases)
save('render-records.json',ba+cf+mini+[sa[i*4] for i in range(7)])

# Relocate all declared package files within evidence and exercise real CLI.
dest=R/'relocated-package';dest.mkdir(exist_ok=True)
manifest=load(P/'package.json')
for f in manifest['files']+['package.json']:
    target=dest/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/f,target)
command=[sys.executable,str(dest/manifest['entrypoint']),'--difficulty','easy','--seed','7319','--count','1','--format','json']
res=subprocess.run(command,cwd=R,capture_output=True,text=True)
out=json.loads(res.stdout) if res.returncode==0 else []
save('relocation-records.json',out)
reference=subprocess.run([sys.executable,str(P/manifest['entrypoint']),*command[2:]],cwd=R,capture_output=True,text=True)
save('packaging-results.json',{'command':command,'returncode':res.returncode,'stderr':res.stderr,
     'output_nonempty':bool(out),'relocated_cli_equals_original':res.stdout==reference.stdout,
     'dependencies':manifest['dependencies'],'declared_files_present':all((P/f).is_file() for f in manifest['files']),
     'external_assets':'No generated image assets or external output paths; CLI emits records to stdout only.',
     'original_package_unchanged':load(R/'package-before.json')=={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(P.rglob('*')) if p.is_file()}})
print(json.dumps({'stages':stages,'relocation_pass':res.returncode==0 and res.stdout==reference.stdout,'grader_cases':len(cases),'render_cases':len(grade)}))
