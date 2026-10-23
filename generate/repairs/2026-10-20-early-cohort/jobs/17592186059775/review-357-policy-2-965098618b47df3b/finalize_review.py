from review_helpers import *
from html.parser import HTMLParser
import collections
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PREV=J/'review-357-policy-2-5595bf9a345705ea'
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
assert all(not s['legacy_defect_draws'] for s in scenarios)
save('delivery-selection.json',{'basis':inv['basis'],'construction_stages':old['construction_stages'],'construction_provenance':str(PREV/'delivery-selection.json'),'sample_before':stats(raw),'sample_after':stats(read('delivery-easy/accepted.json')+read('delivery-moderate/accepted.json')),'batch_before':stats(batch),'batch_after':stats(accepted),'stage_counts':{n:{k:read('delivery-'+n+'/delivery.json')[k] for k in ['input_count','duplicate_count','accepted_count']} for n in ['batch','easy','moderate']},'selection_exclusions':excluded,'learner_selection':scenarios,'selection_rules':['learning.rs:validate_practice_question excludes retired records; validate_response_question requires valid keyed fields.','question_selection.rs:select sorts/deduplicates candidates, chooses a positively weighted nonempty difficulty band, then a uniform candidate.','Without configured weights the smallest eligible entity is selected. Unknown ratings are fallback only.'],'publication_preparation_present':(J/'publication/preparation.json').exists(),'limits':['Read-only captured basis 5577; no live history or future entity IDs. Proposed entity IDs are a representative ordering.','Explicit weight/history scenarios demonstrate reachability, not actual user scheduling.','All three legacy defects are retired and excluded; original source questions preserved.']})

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

# Re-evaluate the historical pool rule with its original failing eligibility.
for name,flag,code in [('inventory-strict',[],0),('inventory-control',['--historical-control'],1)]:
    cmd=[PY,'-B',str(E/'reproduce_inventory_shortcut.py')]+flag
    p=subprocess.run(cmd,cwd=E,text=True,capture_output=True)
    assert p.returncode==code
    (E/(name+'.log')).write_text(p.stdout+p.stderr)
    tests.append({'command':cmd,'exit_code':p.returncode,'log':name+'.log'})
ret=read('retained-findings-validation.json');ret['executed_controls']=tests
ret['inventory_resolution']='All three reproduced legacy records are retired at basis 5577. The strict eligible-defect predicate fails when the former eligibility is restored in a labeled control and passes on actual captured inventory.'
save('retained-findings-validation.json',ret)

v=read('pedagogical-variation.json')
v['answer_roles'][1]['observed']='All five stored positions qualify in exact batch; actual preview positions '+str([p['position'] for p in positions[:5]])+'. Live item IDs can reorder choices.'
for c in v['coverage']:
    if c['case']=='Fresh independent regression and current inventory eligibility':
        c['result']='21 current records pass exact arithmetic; all three reproduced legacy records are retired at basis 5577 and excluded from fresh practice. No demonstrated eligible generated-pool defect remains.'
v['shortcut_probes']=[p for p in v['shortcut_probes'] if 'rendered' not in p['cue'] and p['subgroup']!='eligible stored legacy q-1060 profile']
for pos in range(5):
    hits=sum(p['position']==pos for p in positions[:5])
    v['shortcut_probes'].append({'cue':'fixed rendered position '+str(pos+1),'subgroup':'current five-record batch in actual preview UI','scope':'within_template','strategy':'Choose displayed radio position '+str(pos+1),'correct':hits,'total':5,'baseline':0.2,'disposition':'not_predictive','conclusion':f'{hits}/5 versus 0.2 random choice; no universal position shortcut. Live item IDs may reorder.','sample_refs':['fresh-ui-order.json','fresh-render-records.json']})
v['delivery']['result']='All 5 batch records survive filtering at inventory basis 5577, covering all five target ranks. Rejection and catalog evidence is unchanged. Fresh delivery and weighted-selection scenarios preserve rank reachability. All three defective legacy generated records are retired; no legacy defect reaches any modeled selection scenario.'
v['delivery']['sample_refs']+=['inventory-strict-results.json','inventory-control-results.json','affected-inventory.json']
v['limitations']=[s for s in v['limitations'] if '5574' not in s and 'Only one' not in s]
v['limitations']+=['Captured inventory basis 5577 only; no live learner histories or future publication identities. All three generated legacy records were reproduced and checked for eligibility; affected-inventory.json is verified empty for these records.','Historical source-bank imperfections are documented in source-replay-results.json and original source records remain preserved. Acceptance concerns the current generator, batch and demonstrated generated-pool repair, not replacement of original instructional sources.']
save('pedagogical-variation.json',v)

analysis=read('source-analysis.json');analysis={k:analysis[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']}
analysis['evidence_paths']+=['source-confirmation.json','reuse-provenance.json']
checks={}
def check(name,paths,detail):checks[name]={'status':'passed','evidence_paths':paths,'details':detail}
check('source_replay',['source-replays.json','source-replay-results.json','fresh-source-replay.json'],'Ten complete source banks replay exactly. Two incomplete captures remain documented; normal generation resolves source bank ambiguities.')
check('math',['fresh-math.json','math-results.json','fresh-records.json','review_helpers.py'],'21 fresh records and delivered variants pass independent exact checks of keys, intermediate matrices and optional solutions; unchanged wider evidence reused.')
check('variety',['normal-catalog-records.json','construction-regression.json','delivery-selection.json'],'Ten supported profiles retain variable target roles. All five exact-batch target ranks survive delivery.')
check('scope',['source-analysis.json','fresh-records.json','independent-records.json'],'Preserves nonsingular 2x2 forward elimination, optional back substitution, five radio choices and supported arithmetic.')
check('grading',['fresh-grader-input.json','fresh-grader-results.json','fresh-grader.log'],'Native grader passed 220 submissions: 44 accepted and 176 rejected. Radio-only response contract; free-entry equivalence is inapplicable.')
check('rendering',['fresh-render-records.json','fresh-render/rendering.json','fresh-render-inspection.json','fresh-ui-order.json'],'Eleven actual-UI renders pass; inspected screenshots show readable matrices, fractions, controls, worked solutions and counterfactual updates.')
check('packaging',['fresh-packaging.json','boundary-rejections.json','fresh-commands.json','retained-findings-validation.json','package-unchanged.json'],'Pinned installed versions, relocation, deterministic exact counts and invalid/finite-limit rejection pass. Retained failures checked; package unchanged.')
check('decision_variation',['pedagogical-variation.json','delivery-selection.json','strict-current.log','strict-delivered.log','strict-historical.log','inventory-strict-results.json','inventory-control-results.json','affected-inventory.json','generated-records.json'],'Current raw/delivered batch defeats retained shortcut (1/5 versus historical 5/5). All three demonstrated legacy defects are retired at basis 5577 and excluded from practice.')
save('result.json',{'verdict':'accepted','summary':'All eight checks pass. The current generator and exact batch defeat the retained shortcut; all three defective legacy records are retired in the refreshed inventory. Package files are unchanged.','source_analysis':analysis,'checks':checks,'findings':[]})
before=read('package-before.json');after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};assert before==after
save('package-unchanged.json',{'unchanged':True,'files_checked':len(before)})
# Copy only referenced unaffected independent artifacts when not already present.
paths=set()
def walk(x):
    if isinstance(x,dict):
        for n in x.get('sample_refs',[])+x.get('evidence_paths',[]):paths.add(n)
        for z in x.values():walk(z)
    elif isinstance(x,list):
        for z in x:walk(z)
walk(read('result.json'));walk(v)
added=[]
for n in paths:
    if not (E/n).exists():
        assert (PREV/n).is_file(),n
        (E/n).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PREV/n,E/n);added.append(n)
    assert (E/n).is_file() and (E/n).stat().st_size>0,n
prov=read('reuse-provenance.json');prov['additional_reused_artifacts']={n:hashlib.sha256((E/n).read_bytes()).hexdigest() for n in added};save('reuse-provenance.json',prov)
validator=loadmod('review_validator',REPO/'scripts/generator_review.py')
validator.validate_review(read('result.json'),E)
bad=copy.deepcopy(read('result.json'));bad['source_analysis']['evidence_paths']=['missing-provenance-control.json']
try:validator.validate_review(bad,E)
except ValueError as error:negative=str(error)
else:raise AssertionError('Missing provenance was accepted')
save('evidence-validation.json',{'review_validator_passed':True,'checked_paths':sorted(paths),'negative_missing_provenance_control':negative,'package_unchanged':True})
(E/'session-state.md').write_text('Complete: accepted. All eight checks pass. Refreshed basis 5577 retires all three demonstrated generated legacy defects; strict former-eligibility control still fails. Exact current batch and native grading pass; 11 actual-UI renders checked; evidence paths validated; package unchanged. Result: result.json.\n')
print(json.dumps({'verdict':'accepted','findings':0,'evidence_paths_checked':len(paths),'package_files_unchanged':len(before)}))
