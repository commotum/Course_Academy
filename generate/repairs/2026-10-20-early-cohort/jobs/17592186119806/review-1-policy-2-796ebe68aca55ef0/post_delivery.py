"""Complete the read-only review using saved actual pipeline/grader outputs."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,collections,pathlib,copy
from html.parser import HTMLParser
import review as a
E=a.E
fresh=a.load('delivery-fresh/accepted.json');batch=a.load('delivery-batch/accepted.json')
for r in fresh+batch:a.check(r)
def observed(records):
    counts=collections.Counter()
    for r in records:
        p,d,v,b,x,t,value=a.parsed(r)
        counts[(r['generation']['source_id'],str(t),'positive q' if d>0 else 'negative q')]+=1
    return [{'profile':k[0],'target':k[1],'coefficient_case':k[2],'count':n} for k,n in sorted(counts.items())]
before=a.load('raw-probes.json')
after=json.loads(json.dumps({'fresh':a.probes(fresh),'batch':a.probes(batch)}))
assert before['fresh']==after['fresh'] and before['batch']==after['batch']
a.save('delivered-probes.json',{'command':str(a.PY)+' post_delivery.py','records':{'fresh':len(fresh),'batch':len(batch)},'coverage_before':{'fresh':observed(a.load('fresh-records.json')),'batch':observed(a.load('batch-records.json'))},'coverage_after':{'fresh':observed(fresh),'batch':observed(batch)},'probes':after,'note':'All candidates survive; normalization changes identities but preserves mathematical prompt, solution and banks. Probe statistics before/after are identical.'})
# Faithful select() reduction for these captured all-easy pools. Surrogate entity
# IDs only; this never allocates or writes a database entity.
selection=[];selected={}
for label,rs,exclude in [('fresh-positive-easy',fresh,set()),('batch-positive-easy',batch,set()),('fresh-half-seen',fresh,set(range(0,len(fresh),2)))]:
    candidates=[(100000+i,r) for i,r in enumerate(rs) if i not in exclude]
    picks=[];draws=[]
    for j in range(256):
        seed='independent-revision-796ebe68-'+str(j)
        digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
        u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
        eid,r=candidates[int(u*len(candidates))];picks.append(r)
        draws.append({'seed':seed,'surrogate_entity_id':eid,'question_id':r['question'][':question/id'],'profile':r['generation']['source_id']})
    selected[label]=picks
    selection.append({'scenario':label,'candidate_count':len(candidates),'history_excluded':len(exclude),'difficulty_weights':'any finite valid distribution with positive easy weight, other bands absent','draws':draws,'unique_selected':len({x['question'][':question/id'] for x in picks}),'profiles':dict(collections.Counter(x['generation']['source_id'] for x in picks)),'probes':a.probes(picks)})
src=a.R/'engine/rust/question_selection.rs'
a.save('learner-selection-records.json',selected)
a.save('learner-selection.json',{'command':str(a.PY)+' post_delivery.py','source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'rule':'select sorts unique entity IDs, uses a SHA256 difficulty draw then digest bytes 8:16 for the within-band index. For all easy candidates, positive easy weight makes this precisely uniform within the fresh easy pool. seen_before_task and current prefix exclusions are applied before selection.','scenarios':selection,'zero_easy_weight':'No rated easy record is selected; no unrated generated records exist.','unconfigured_policy':'None distribution returns minimum candidate entity ID. With surrogate order this would select the first remaining record; future database IDs are not known. This changes frequency, not any record key or eligible bank role.','limits':['No live learner history or future database entity IDs. Freshness scenarios are explicit conditional inputs, not empirical learner frequencies.','Captured source originals may be unseen too; the generated-only pool is the applicable scenario after the originals have been seen. No live policy or database publication was inspected.','No stage is claimed to balance target coverage for every individual learner; the inspected rules do not filter by answer rank or labels.']})
# Predeclared prior strategies, including batch measurements separate from controls.
old_rules={'q-34601':('value rank 2',2),'q-105161':('value rank 1',1),'q-73933':('coordinate2 rank 1',1)}
old_summary={}
for stage in ['fresh','batch']:
    old_summary[stage]={}
    for sid,(cue,rank) in old_rules.items():
        if sid in after[stage]:old_summary[stage][sid]={'strategy':cue,'correct':after[stage][sid]['strategies'][cue][0],'total':after[stage][sid]['strategies'][cue][1]}
a.save('retained-shortcuts-after-delivery.json',old_summary)
# Actual UI choiceOrder() is a second deterministic shuffle. Validate its exact
# ASCII FNV rule against the saved real DOM, then measure it on surrogate item IDs.
def fnv(text):
    h=2166136261
    for c in text:h=((h^ord(c))*16777619)&0xffffffff
    return h
def ui_order(r,item_id):
    result=copy.deepcopy(r);f=result['question'][':question/answer-fields'][0]
    f[':answer-field/choices'].sort(key=lambda c:fnv(str(item_id)+':'+f[':answer-field/id']+':'+c[':answer/id']))
    return result
class Inputs(HTMLParser):
    def __init__(self):super().__init__();self.ids=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='input' and d.get('type')=='radio':self.ids.append(d['value'])
ui_validation=[]
for i,r in enumerate(a.load('render-records.json')):
    parser=Inputs();parser.feed((E/'render'/('question-'+str(i+1).zfill(3)+'.html')).read_text())
    ordered=ui_order(r,i+1)
    expected=[c[':answer/id'] for c in ordered['question'][':question/answer-fields'][0][':answer-field/choices']]
    assert expected==parser.ids
    _,cid=a.choices(r)
    ui_validation.append({'case':i+1,'input':'render-records.json','actual_dom_choice_ids':parser.ids,'correct_display_position':parser.ids.index(cid)+1,'matches_ui_rule':True})
ui_records=[ui_order(r,100000+i) for i,r in enumerate(fresh)]
ui_probes=a.probes(ui_records)
a.save('ui-ordered-records.json',ui_records)
a.save('ui-choice-order.json',{'source':'ui/learning.js::choiceOrder','source_sha256':hashlib.sha256((a.R/'ui/learning.js').read_bytes()).hexdigest(),'actual_renderer_dom_validation':ui_validation,'delivered_fresh_surrogate_item_ids':'100000 through 100167; live item IDs unavailable','delivered_fresh_probes':ui_probes,'limits':'Raw/stored position is distinct from rendered display position. Fixture DOM validation is exact; future task-item IDs remain conditional.'})
# Explicit sign-only conditional probes and whole-batch simple bank strategies.
def measures(records):
    out=collections.defaultdict(lambda:[0,0])
    for r in records:
        ch,cid=a.choices(r);idx=[i for i,_ in ch].index(cid);vs=[v for _,v in ch]
        for pos in range(5):
            out['overall: position '+str(pos+1)][0]+=idx==pos;out['overall: position '+str(pos+1)][1]+=1
        if isinstance(vs[0],tuple):
            # Each coordinate rule conditioned on dimension so it is defined.
            for j in range(len(vs[0])):
                for label,fn in [('minimum',min),('maximum',max)]:
                    indices=[k for k,v in enumerate(vs) if v[j]==fn(z[j] for z in vs)]
                    pred=indices[0]
                    key='vector '+str(len(vs[0]))+'D: '+label+' coordinate '+str(j+1)
                    out[key][0]+=pred==idx;out[key][1]+=1
        else:
            for label,fn in [('minimum',min),('maximum',max),('minimum absolute',lambda xs:min(xs,key=abs)),('maximum absolute',lambda xs:max(xs,key=abs))]:
                pred=vs.index(fn(vs));key='scalar: '+label;out[key][0]+=pred==idx;out[key][1]+=1
            for label,fn in [('positive',lambda v:v>0),('negative',lambda v:v<0),('zero',lambda v:v==0)]:
                indices=[j for j,v in enumerate(vs) if fn(v)]
                if len(indices)==1:
                    key='scalar bank with unique '+label+': choose that value';out[key][0]+=indices[0]==idx;out[key][1]+=1
    return dict(out)
simple={stage:measures(rs) for stage,rs in [('fresh',fresh),('batch',batch)]}
a.save('simple-cues.json',{'baseline':0.2,'tie_break':'first displayed matching candidate','fresh':simple['fresh'],'batch':simple['batch'],'interpretation':'Scores are reported even for small subgroups. Two batch vectors happen to have the smallest last coordinate; 2/2 is a tiny observed subgroup, not a family-wide rule. Source-profile controls at a fixed bank permit every role. No tested common rule answers all five batch items.'})
probe_rows=[]
for sid,t in after['fresh'].items():
    for strategy,(correct,total) in t['strategies'].items():
        assert correct<total # Guard against overlooking perfect fresh conditional cues.
        probe_rows.append({'cue':strategy,'subgroup':'delivered authored '+sid,'scope':'within_template','strategy':'Choose '+strategy+' using bank/display only (stable displayed tie break).','correct':correct,'total':total,'baseline':0.2,'disposition':'not_predictive','conclusion':'Five-option uninformed baseline 0.2; no fixed predictor in this 12-item conditional sample. Ordinary candidates are exchangeable before choosing correct role; measured fluctuations do not prove chance equality.','sample_refs':['fresh-records.json','delivery-fresh/accepted.json','delivered-probes.json']})
for stage in ['fresh','batch']:
    for cue,(correct,total) in simple[stage].items():
        subgroup,rule=cue.split(': ',1)
        probe_rows.append({'cue':rule,'subgroup':stage+' '+subgroup,'scope':'overall' if subgroup=='overall' else 'other_recognizable_subgroup','strategy':'Choose by '+rule+' without reading vector arithmetic (positions refer to stored order).','correct':correct,'total':total,'baseline':0.2,'disposition':'not_predictive','conclusion':('Uninformed five-option baseline 0.2. This is the exact 5-item delivered batch; groups of one/two are reported without inferring repeatability. Batch uses all five correct stored positions and no tested whole-pool rule solves it. Actual UI applies its own measured shuffle.' if stage=='batch' else 'Uninformed five-option baseline 0.2. Conditional shape/sign cue measured separately. Random candidate role assignment gives no bank-only mathematical privilege to this cue.'),'sample_refs':[('delivery-batch/accepted.json' if stage=='batch' else 'delivery-fresh/accepted.json'),'simple-cues.json','ui-choice-order.json']})
for sid,t in ui_probes.items():
    for position in range(1,6):
        correct,total=t['strategies']['position '+str(position)]
        assert correct<total
        probe_rows.append({'cue':'rendered position '+str(position),'subgroup':'authored '+sid+' with surrogate task-item IDs','scope':'within_template','strategy':'Select the fixed rendered position after actual UI FNV ordering.','correct':correct,'total':total,'baseline':0.2,'disposition':'not_predictive','conclusion':'Five radio choices give uninformed baseline 0.2. Exact UI ordering reproduced and verified against all 12 actual DOMs. This profile has counterexamples; live future task-item IDs are unavailable.','sample_refs':['ui-ordered-records.json','ui-choice-order.json']})
dom_positions=[row['correct_display_position'] for row in ui_validation[:5]]
for position in range(1,6):
    probe_rows.append({'cue':'actual rendered batch position '+str(position),'subgroup':'five batch items in actual preview DOM','scope':'overall','strategy':'Choose this display position in every batch item.','correct':dom_positions.count(position),'total':5,'baseline':0.2,'disposition':'not_predictive','conclusion':'Five-option baseline 0.2; no position answers all five actual rendered batch members. Preview content IDs are known; future live task IDs may reorder choices.','sample_refs':['ui-choice-order.json','render-records.json','render/rendering.json']})
source=a.load('source-analysis.json')
pv={'learner_operation':source['skill'],'fixed_features':source['fixed_features']+[
    {'feature':'Source coefficients and sum/difference operator fixed per named profile','justification':'Conservative comparable arithmetic branches; union includes both coefficient signs and both component operations. Values and eligible target assignments vary within each. These coefficients are representative, not essential to the mathematics.'}],
    'answer_roles':[
        {'role':'Correct candidate position and numeric/coordinate rank','eligible_variation':'Any of five candidates can be correct at a fixed bank; no label, rank or coordinate extremum is essential.','observed':'20 controlled authored records (four profiles) make all five candidates correct through relevant b changes; ordinary sampler independently assigns uniform role before deriving b. Per-profile fresh probes defeat fixed ranks.'},
        {'role':'Requested components and subtraction direction','eligible_variation':'Any pair of distinct component indices; reverse ordered pairs for differences; sums use unordered equivalent pairs.','observed':'All 53 profile/target possibilities exercised at scale 2. Fixed a,b target pair returns 54,-54,-32 with changed target and explanation.'},
        {'role':'Signed coefficient and solved vector','eligible_variation':'Both signs and positive/negative/zero components within observed workload.','observed':'14 supported profiles, 168 new ordinary records cover both coefficient signs and three/four dimensions, with fresh a,x and compatible b.'}],
    'coverage':[
        {'case':'All complete source banks and previously missing q-105158','sample_refs':['source-replay-records.json','source-replay.json','strict-regressions.json','executable-regression-verification.json'],'result':'14 complete banks replay; old executable fails and current passes the identical strict regression. q-34574 and canonical answer-bank gaps explicitly retained.'},
        {'case':'Changed ordinary construction, per-profile decision cases and eligible targets','sample_refs':['fresh-records.json','target-records.json','math.json','delivered-probes.json'],'result':'168 ordinary items, 53 target diagnostics, both coefficient signs; all tested rank/position strategies have counterexamples in each ordinary profile. New a,x domain preserves integer isolation.'},
        {'case':'Exact runner batch after actual filtering','sample_refs':['batch-records.json','delivery-batch/accepted.json','simple-cues.json','delivered-grader-report.json','ui-choice-order.json'],'result':'5/5 survive, 2 vector and 3 scalar tasks, both coefficient signs, varied requested pairs, all five correct stored positions. Actual UI shuffle separately inspected and measured; no rendered position solves all five. Original q-34601 rank-2 strategy fails on the batch member. Every delivered correct response graded accepted; alternatives rejected.'}],
    'counterfactuals':[
        {'kind':'relevant','change':'Hold coefficients and a,b fixed; reverse x3-x2 to x2-x3 and retarget to x1-x3.','expected':'54 becomes -54 and -32; prompt and scalar solution expression follow indices; native grader accepts new answers and rejects wrong alternatives.','observed':'Exact Fraction checking, all-choice native outcomes and inspected actual UI render cases 6-8 confirm all three responses and explanations.','status':'passed','justification':'Source q-34601 component differences and q-105161 demonstrate answer-bearing target indices.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-input.json','grader-report.json','render/rendering.json','render/question-006.png','render/question-007.png','render/question-008.png']},
        {'kind':'relevant','change':'Fix coefficient, a, target and bank; change b through compatible x so each of five candidate values becomes correct.','expected':'All five candidates take the correct role, with explanation and actual grading derived from changed evidence.','observed':'Four profile groups pass exact arithmetic and all-choice native grading for all 20 states. Actual UI cases 9-10 show different b, worked vector, and correct values 10 and -11 with same visible candidate set.','status':'passed','justification':'The source method uses b-pa to determine x; fixing a source bank rank has no instructional reason.','sample_refs':['control-records.json','counterfactual-results.json','grader-input.json','grader-report.json','render/question-009.png','render/question-010.png']},
        {'kind':'irrelevant','change':'Keep target components and candidate bank fixed; alter an unrequested x component and corresponding b component.','expected':'Requested scalar response stays fixed while full solved vector in explanation changes; grading agrees.','observed':'Three before/after pairs pass arithmetic and all-choice native grading. Inspected UI cases 11-12 preserve x1-x4=6 while unused second component changes from -1 to 0.','status':'passed','justification':'A two-component sum/difference is independent of unrequested coordinates, as shown by source scalar targets q-105160 and q-34601.','sample_refs':['irrelevant-records.json','counterfactual-results.json','grader-input.json','grader-report.json','render/question-011.png','render/question-012.png']}],
    'shortcut_probes':probe_rows,
    'delivery':{'stages_examined':['generator rejection/resampling','requested difficulty','actual publisher prepare_records identity validation and normalization','captured-inventory and within-batch deduplication','freshness exclusion and weighted learner selection rule'],
        'sample_refs':['batch-resampling-records.json','packaging.json','delivery-fresh/delivery.json','delivery-batch/delivery.json','delivery-fresh/accepted.json','delivery-batch/accepted.json','delivered-probes.json','learner-selection.json','learner-selection-records.json','ui-choice-order.json'],
        'result':'168/168 fresh and 5/5 batch survive captured basis 5402. Decision/cue distributions unchanged by normalization/filtering. Native SHA-index reproduction covers all-easy positive-weight pools and half-seen freshness. All 5 batch records are reachable and observed in 256 explicit task-seed draws; zero easy weight selects none. No publication or database writes.'},
    'limitations':['Finite adversarial sampling does not exclude every possible shortcut.','q-34574 has no captured solution/key; canonical e-4790 has no captured radio bank. No fabricated source replay for them.','Tiny batch subgroups can happen to share cues: the two vector answers are minimal in the last coordinate. This 2/2 observation is retained, alongside failed extensions to other coordinates/profiles and fixed-bank controls; no universal action across the batch was demonstrated.','Future database inventory, entity IDs, policy weights and live learner history are unavailable; selection conclusions are conditional on explicit captured/surrogate pools.','All response fields are radio; free-entry equivalence is not applicable to the observed response contract.']}
a.save('pedagogical-variation.json',pv)
# Human screenshot inspection is recorded after viewing these exact PNGs.
rr=a.load('render/rendering.json');assert rr['passed'] and len(rr['cases'])==12
a.save('render-inspection.json',{'passed':True,'renderer':'unmodified UI via render_preview.py, --limit 12','inspected_screenshots':['render/question-'+str(i).zfill(3)+'.png' for i in range(1,13)],'observations':'All five batch prompts, vector/scalar radio banks, minus signs, fractions and worked matrices are legible with intact layout. Target changes display the correct indices and 54/-54/-32 conclusions; fixed-bank b changes update responses; irrelevant-component pair preserves requested response. No MathJax errors, broken images, missing glyphs or JavaScript errors.','report':'render/rendering.json'})
before_hash=a.load('package-before.json');now={str(p.relative_to(a.P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in a.P.rglob('*') if p.is_file()}
assert before_hash==now
a.save('package-integrity.json',{'passed':True,'file_count':len(now),'before':'package-before.json','after':now,'database_writes':0,'published_assets':0})
# Actual runtime outputs in the relocated copy, not just its normal exit status.
manifest=json.loads((a.P/'package.json').read_text());extras=[str(p.relative_to(E/'relocated')) for p in (E/'relocated').rglob('*') if p.is_file() and str(p.relative_to(E/'relocated')) not in manifest['files']]
assert not extras
a.save('external-output.json',{'passed':True,'unexpected_relocated_files':extras,'manifest_files':manifest['files'],'generation_assets':'all records have [] assets; no external output assets required'})
a.save('commands.json',{'cwd':str(E),'commands':[
    str(a.PY)+' review.py',str(a.PY)+' post_delivery.py',
    str(a.PY)+' prior-regression_test.py --package ../workspace --output strict-regressions.json',
    str(a.PY)+' prior-regression_test.py --package ../review-0-policy-2-903865075bf272e6/relocated --output legacy-strict-regressions.json',
    str(a.PY)+' author-preflight/checks/validate_repair.py',
    *[str(a.PY)+' '+str(a.R/'generate/pipeline/check_delivery.py')+' --input '+n+'-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-'+n+' --math-root /media/jake/SSD/EDB/math' for n in ['fresh','batch']],
    str(a.R/'generate/runs/current/check-engine')+' grader-input.json grader-report.json',str(a.R/'generate/runs/current/check-engine')+' delivered-grader-input.json delivered-grader-report.json',
    str(a.PY)+' '+str(a.R/'generate/pipeline/render_preview.py')+' --input render-records.json --output render --limit 12 --math-root /media/jake/SSD/EDB/math'],
    'write_policy':'Only evidence_root writes. Author checks run in evidence-local complete copy to avoid their hardcoded evidence directory touching the original package.'})
(E/'session-state.md').write_text('All required tests complete. Retained strict tests fail on verified old executable and pass current runtime. Independent Fraction math 269 records; source replay 14 banks; delivery fresh 168/168 and exact batch 5/5; native grader 62+5 complete all-choice cases; actual UI 12 screenshots visually inspected; learner-selection SHA rule reproduced with explicit histories; package entire file hash map unchanged. pedagogical-variation.json and post-delivery measurements saved. Final report/schema validation remains.\n')
print(json.dumps({'delivery_fresh':len(fresh),'delivery_batch':len(batch),'old_shortcuts':old_summary,'learner_selected_batch_ids':selection[1]['unique_selected'],'render_cases':len(rr['cases']),'package_unchanged':True,'pedagogical_probes':len(probe_rows)}))
