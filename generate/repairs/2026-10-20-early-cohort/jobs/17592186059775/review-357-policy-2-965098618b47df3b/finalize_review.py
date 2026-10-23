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

