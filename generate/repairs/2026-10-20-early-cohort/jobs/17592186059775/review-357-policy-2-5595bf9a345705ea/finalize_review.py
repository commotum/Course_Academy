from review_helpers import *
from html.parser import HTMLParser
import collections
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PREV=J/'review-3-policy-2-0d2b0c0912b0fa93'
def read(n):return json.load(open(E/n))
def stats(rs):
    out={}
    for sid in sorted({r['generation']['template'] for r in rs}):
        z=[r for r in rs if r['generation']['template']==sid]
        out[sid]={'count':len(z),'ranks':dict(collections.Counter(str(rank(r)) for r in z))}
    return out

# Current UI ordering depends on preview item IDs as well as choice IDs.
class Radios(HTMLParser):
    def __init__(self):super().__init__();self.values=[]
    def handle_starttag(self,t,attrs):
        d=dict(attrs)
        if t=='input' and d.get('type')=='radio':self.values.append(d['value'])
positions=[]
for i,r in enumerate(read('fresh-render-records.json'),1):
    parser=Radios();parser.feed((E/'fresh-render'/f'question-{i:03d}.html').read_text())
    assert set(parser.values)=={a[':answer/id'] for a in f(r)[':answer-field/choices']}
    positions.append({'index':i,'parameters':r['generation']['parameters'],'position':parser.values.index(key(r)[':answer/id']),'choice_ids':parser.values})
save('fresh-ui-order.json',{'records':positions,'exact_batch_positions':[p['position'] for p in positions[:5]],'limitation':'Preview item IDs affect hash order; live item IDs are unknown.'})
save('fresh-render-inspection.json',{'report_passed':read('fresh-render/rendering.json')['passed'],'count':11,'screenshots_inspected':['fresh-render/question-001.png','fresh-render/question-005.png','fresh-render/question-009.png','fresh-render/question-010.png','fresh-render/question-011.png','render/question-001.png'],'observations':['All inspected augmented matrices, radio controls, fraction signs and worked operations are readable without clipping.','Exact batch endpoint RHS -18 versus 42 updates the final y from -9 to 3.','Moderate controlled RHS -24 versus 40 updates final y from -19/16 to 45/16.','Moderate irrelevant permutation keeps RHS -24 and y=-19/16 while moving the selected radio option.','Reused solve-family screenshot displays the full back-substitution and correct x=105,y=-65.'],'ui_binding_unchanged':read('fresh-render/ui-hashes.json')==read('render/ui-hashes.json')})

# Reuse unchanged construction-stage coverage; refresh every inventory-dependent stage.
old=json.load(open(PREV/'delivery-selection.json'))
shutil.copy2(PREV/'batch-selection-regression.json',E/'batch-selection-regression.json')
inv=json.load(open(J/'source/inventory.json'));batch=read('runner-batch.json');accepted=read('delivery-batch/accepted.json');raw=read('fresh-records.json')
eligible=[];excluded=[]
for z in inv['questions']:
    reason='retired' if z.get(':question/retired') else 'missing correct answer' if any(not a.get(':answer-field/correct') for a in z[':question/answer-fields']) else None
    if reason:excluded.append({'id':z[':question/id'],'reason':reason});continue
    eligible.append({'entity':z[':db/id'],'id':z[':question/id'],'band':z.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1],'origin':'captured'})
proposed=[{'entity':max(x[':db/id'] for x in inv['questions'])+100+i,'id':q(r)[':question/id'],'band':'easy','origin':'proposed','rank':rank(r)} for i,r in enumerate(accepted)]
scenarios=[]
for weights,seen in [([1,0,0],False),([1,0,0],True),([0,1,0],False),([1,1,0],False)]:
    pool=sorted(([] if seen else eligible)+proposed,key=lambda x:x['entity']);bands=[[x for x in pool if x['band']==b] for b in ['easy','moderate','hard']];draws=[]
    for i in range(128):
        seed='independent-review-357-'+str(i);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
        u=[(int.from_bytes(digest[o:o+8],'big')>>11)/(1<<53) for o in [0,8]]
        total=sum(w for b,w in zip(bands,weights) if b);draw=u[0]*total;chosen=None
        for b,w in zip(bands,weights):
            if not b or not w:continue
            chosen=b
            if draw<w:break
            draw-=w
        if chosen is None:chosen=[x for x in pool if x['band']=='unrated']
        draws.append({'seed':seed,'selected':chosen[int(u[1]*len(chosen))] if chosen else None})
    scenarios.append({'weights':weights,'captured_inventory_seen':seen,'pool':pool,'draws':draws,'proposed_ranks_reached':sorted({d['selected']['rank'] for d in draws if d['selected'] and d['selected']['origin']=='proposed'}),'legacy_defect_draws':[d['seed'] for d in draws if d['selected'] and d['selected']['id']=='f98461ac-7c48-536e-aa56-fcc53a0bd592']})
assert scenarios[0]['proposed_ranks_reached']==list(range(5)) and scenarios[1]['proposed_ranks_reached']==list(range(5))
assert scenarios[2]['legacy_defect_draws']
save('delivery-selection.json',{'basis':inv['basis'],'construction_stages':old['construction_stages'],'construction_provenance':str(PREV/'delivery-selection.json'),'sample_before':stats(raw),'sample_after':stats(read('delivery-easy/accepted.json')+read('delivery-moderate/accepted.json')),'batch_before':stats(batch),'batch_after':stats(accepted),'stage_counts':{n:{k:read('delivery-'+n+'/delivery.json')[k] for k in ['input_count','duplicate_count','accepted_count']} for n in ['batch','easy','moderate']},'selection_exclusions':excluded,'learner_selection':scenarios,'selection_rules':['learning.rs:validate_practice_question excludes retired records; validate_response_question requires valid keyed fields.','question_selection.rs:select sorts/deduplicates candidates, chooses a positively weighted nonempty difficulty band, then a uniform candidate.','Without configured weights the smallest eligible entity is selected. Unknown ratings are fallback only.'],'publication_preparation_present':(J/'publication/preparation.json').exists(),'limits':['Read-only captured basis 5574; no live history or future entity IDs. Proposed entity IDs are a representative ordering.','Explicit weight/history scenarios demonstrate reachability, not actual user scheduling.','Historical moderate shortcut survives eligibility; two retired easy defects are preserved history.']})

# Retained executable preflight probe on its failure and current output; no author writes.
tests=[]
for label,inp,expected in [('author-current','runner-batch.json',0),('author-historical','previous-runner-batch.json',1)]:
    cmd=[PY,'-B',str(W/'checks/check_batch_selection.py'),'--input',str(E/inp)]
    p=subprocess.run(cmd,cwd=E,text=True,capture_output=True);assert p.returncode==expected
    (E/(label+'.log')).write_text(p.stdout+p.stderr);tests.append({'command':cmd,'exit_code':p.returncode,'log':label+'.log'})
cmd=[PY,'-B',str(W/'evidence/legacy/17592186059775.py'),'--format','json']
p=subprocess.run(cmd,cwd=E,text=True,capture_output=True);assert p.returncode==2 and 'unrecognized arguments' in p.stderr
tests.append({'command':cmd,'exit_code':p.returncode,'stderr':p.stderr})
save('retained-findings-validation.json',{'all_retained_findings':json.load(open(J/'repair-history.json'))['findings'],'preflight':json.load(open(J/'repair-preflight.json')),'executed_controls':tests,'evidence_issue':'Prior wrong-root/missing-provenance failure is a report contract defect, not a generator defect. This review is authored directly at evidence_root and validated below. Author installation/handoff checks are not executed because they write workspace evidence and concern runner handoff; no generator repair is requested for this old report issue.'})

v=read('pedagogical-variation.json')
v['answer_roles'][1]['observed']='All five stored positions qualify within the exact batch; fresh rendered positions are '+str([p['position'] for p in positions[:5]])+'. No fixed rendered position answers all five; live item IDs can reorder again.'
v['coverage'].append({'case':'Fresh independent regression and current inventory eligibility','sample_refs':['fresh-records.json','fresh-math.json','fresh-counterfactuals.json','inventory-results.json','generated-records.json'],'result':'21 current records pass exact arithmetic; one moderate stored legacy shortcut remains eligible; two easy legacy defects are retired.'})
for c in v['counterfactuals']:
    c['sample_refs']+=['fresh-counterfactuals.json','fresh-grader-input.json','fresh-grader-results.json','fresh-render/rendering.json','fresh-render-inspection.json']
v['shortcut_probes']=[p for p in v['shortcut_probes'] if 'rendered' not in p['cue']]
for pos in range(5):
    hits=sum(p['position']==pos for p in positions[:5])
    v['shortcut_probes'].append({'cue':'fixed rendered position '+str(pos+1),'subgroup':'current five-record batch in actual preview UI','scope':'within_template','strategy':'Choose displayed radio position '+str(pos+1),'correct':hits,'total':5,'baseline':0.2,'disposition':'not_predictive','conclusion':f'{hits}/5 versus 0.2 random choice; no universal position shortcut. Live item IDs may reorder.','sample_refs':['fresh-ui-order.json','fresh-render-records.json']})
legacy=read('inventory-strict-results.json')
v['shortcut_probes'].append({'cue':'median candidate lower-right value','subgroup':'eligible stored legacy q-1060 profile','scope':'within_template','strategy':'Sort the five candidate lower-right entries and choose the median, ignoring input M.','correct':legacy['family_correct'],'total':legacy['family_total'],'baseline':0.2,'disposition':'defect','conclusion':'All three permitted legacy scales fix the median as correct, versus 1/5 random guessing. The captured scale-3 record remains selectable for moderate practice. This is an inventory defect; current generation varies the target rank.','sample_refs':['legacy-family-records.json','generated-records.json','inventory-strict-results.json','inventory-results.json']})
v['delivery']['result']='Current batch: 5 input, 5 accepted, all five target ranks retained. Fresh delivery/selection scenarios preserve current rank reachability. The refreshed pool excludes two retired easy records but still permits the legacy moderate median shortcut under positive moderate weights.'
v['delivery']['sample_refs']+=['inventory-results.json','fresh-ui-order.json','fresh-commands.json']
v['limitations']=[s for s in v['limitations'] if '5461' not in s and 'Three legacy' not in s]
v['limitations']+=['Inventory captured at basis 5574. Only one demonstrated generated defect remains eligible; affected-inventory.json excludes retired history.','Unchanged independent construction and full-profile evidence reused with provenance; fresh tests focus on the exact batch, prior failure, counterfactuals and changed inventory.']
save('pedagogical-variation.json',v)

analysis=read('source-analysis.json');analysis={k:analysis[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']}
checks={}
def check(name,paths,detail,status='passed'):checks[name]={'status':status,'evidence_paths':paths,'details':detail}
check('source_replay',['source-replays.json','source-replay-results.json','fresh-source-replay.json'],'Ten complete source banks replay exactly. Two incomplete captures remain documented; source REF ambiguities are corrected in normal generation.')
check('math',['fresh-math.json','math-results.json','fresh-records.json','review_helpers.py'],'21 fresh records and delivered variants pass independent exact-arithmetic checks of prompts, keys, row operations and optional solutions; unchanged wider evidence reused.')
check('variety',['normal-catalog-records.json','construction-regression.json','delivery-selection.json'],'Current finite catalog retains all ten profiles and five target ranks. Exact batch covers all ranks before and after delivery; changed inventory assessed separately.')
check('scope',['source-analysis.json','fresh-records.json','independent-records.json'],'Current variations preserve nonsingular 2x2 forward elimination, optional back substitution, five radio choices and supported arithmetic.')
check('grading',['fresh-grader-input.json','fresh-grader-results.json','fresh-grader.log'],'Native grader passed 225 fresh submissions: 45 accepted, 180 rejected. All fields are radio; free-entry equivalence is inapplicable.')
check('rendering',['fresh-render-records.json','fresh-render/rendering.json','fresh-render-inspection.json','fresh-ui-order.json'],'Eleven fresh actual-UI renders pass. Screenshots inspected for matrices, fractions, controls and counterfactual updates; unchanged solve-family render also inspected.')
check('packaging',['fresh-packaging.json','packaging-results.json','boundary-rejections.json','fresh-commands.json','retained-findings-validation.json','package-unchanged.json'],'Pinned versions, relocated closure, deterministic exact counts and invalid/finite-limit rejection pass. Retained failures checked; package unchanged.')
check('decision_variation',['pedagogical-variation.json','delivery-selection.json','strict-current.log','strict-delivered.log','strict-historical.log','inventory-strict-results.json','affected-inventory.json','generated-records.json'],'Current raw and delivered batch defeat the retained shortcut (1/5 versus historical 5/5), but one eligible stored moderate record retains a family-wide median-answer shortcut.','failed')
finding={'kind':'inventory','description':'Stored moderate question f98461ac-7c48-536e-aa56-fcc53a0bd592 (entity 17592186528070) remains eligible at basis 5574. Choosing the median candidate lower-right value answers it without Gaussian elimination; all three permitted scales of its legacy q-1060 family preserve that rank. The two easy legacy defects are retired and excluded from the repair list. Current generator/batch checks pass.','source_refs':['157d0b46-caa9-5e52-add3-341aa2ee9d01','tutorial 2112d3af-1fb0-5a70-ab99-59931db99930: normalize, eliminate, normalize'],'reproduction':'From evidence_root run /home/jake/Developer/Course_Academy/.venv/bin/python -B reproduce_inventory_shortcut.py (expected exit 1). Exact archived call: legacy.generate("moderate",59775,"q-1060",["q-1060",3]). Input [[-1,2,3],[5,6,24]]; candidate y values 27/16,33/16,39/16,45/16,51/16; keyed median 39/16. Complete matched record and generation metadata: generated-records.json; native acceptance: fresh-grader-results.json.','requested_change':'Runner-owned pool repair: retire or replace the eligible legacy record listed in affected-inventory.json, eliminating the fixed-median answer-role rule in selectable legacy practice. Preserve retired history and original source questions. Refresh inventory and independently verify eligibility. No current generator change or author database write is requested.'}
save('result.json',{'verdict':'revise','summary':'One eligible stored moderate question retains a reproducible median-answer shortcut. Current generator and exact five-question batch pass their checks; the remaining repair belongs to the stored pool.','source_analysis':analysis,'checks':checks,'findings':[finding]})
before=read('package-before.json');after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};assert before==after
save('package-unchanged.json',{'unchanged':True,'files_checked':len(before)})
# Validate evidence at its actual root, including a real wrong-root control.
validator=loadmod('review_validator',REPO/'scripts/generator_review.py')
validator.validate_review(read('result.json'),E)
bad=copy.deepcopy(read('result.json'));bad['source_analysis']['evidence_paths']=['missing-provenance-control.json']
try:validator.validate_review(bad,E)
except ValueError as error:negative=str(error)
else:raise AssertionError('Missing provenance was accepted')
paths=set()
def walk(x):
    if isinstance(x,dict):
        for n in x.get('sample_refs',[])+x.get('evidence_paths',[]):paths.add(n)
        for z in x.values():walk(z)
    elif isinstance(x,list):
        for z in x:walk(z)
walk(read('result.json'));walk(v)
for n in paths:assert (E/n).is_file() and (E/n).stat().st_size>0,n
save('evidence-validation.json',{'review_validator_passed':True,'checked_paths':sorted(paths),'negative_missing_provenance_control':negative,'package_unchanged':True})
(E/'session-state.md').write_text('Review complete: revise for one eligible historical moderate median shortcut only. Current generator/batch pass all applicable runtime checks; decision_variation fails due to stored-pool defect. All artifacts live under evidence_root; result.json and root-relative paths validated; package unchanged.\n')
print(json.dumps({'verdict':'revise','findings':1,'kind':'inventory','evidence_paths_checked':len(paths),'package_files_unchanged':len(before)}))
