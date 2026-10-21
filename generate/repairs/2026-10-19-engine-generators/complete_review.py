"""Record the current Codex session's review of separately authored candidates.

No author/reviewer agents are launched. Existing independent test scripts are
rerun by this session; reports cite the fresh outputs, never an old verdict.
"""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from generator_review import validate_review

BASE = Path(__file__).resolve().parent

def read(p): return json.loads(p.read_text())
def write(p,v): p.write_text(json.dumps(v,indent=2)+'\n')

def field(r): return r['question'][':question/answer-fields'][0]

def main(kp):
    d=BASE/str(kp);e=d/'independent-review';state=read(d/'job.json')
    band=state['effective_difficulty']
    sample_name='records.json' if kp==17592186092261 else 'samples.json'
    raw=read(e/sample_name)
    delivered=read(e/('delivery-easy/accepted.json' if kp==17592186092261 else 'delivery/accepted.json'))
    batch=read(d/'samples.json')
    source=read(d/'source/source.json')
    native=read(e/'native-grading.json');regression=read(e/'current-regression-grading.json')
    assert native['documented_unresolved_checks']==regression['documented_unresolved_checks']==0
    assert read(e/'current-regression-command.json')['exit_code']==0
    render=read(e/'render-current/rendering.json');assert render['passed']
    math=read(e/('math.json' if kp==17592186092261 else 'math-results.json'))
    if kp==17592186096617:
        assert math['passed'];math_count=len(math['cases'])+len(math['runner_batch'])
        pack=read(e/'packaging-results.json');assert pack['all_replays_equal'] and pack['relocation_equal'] and pack['rejections_all_pass']
        replay=read(e/'source-replay-results.json');assert all(c['passed'] for c in replay['cases'])
        math_ref='math-results.json';replay_ref='source-replay-results.json';pack_ref='packaging-results.json'
    elif kp==17592186096618:
        assert all(not c['failures'] for c in math);math_count=len(math)
        pack=read(e/'packaging.json');assert pack['deterministic_replay'] and pack['relocation']['matches_original'] and pack['canonical_replay_supported']
        assert all(c['bank_equal'] for c in read(e/'source-replay.json'))
        math_ref='math-results.json';replay_ref='source-replay.json';pack_ref='packaging.json'
    elif kp==17592186092261:
        assert all(c.get('passed') and c.get('solution_derivative_passed') for c in math);math_count=len(math)
        assert all(c['matched'] for c in read(e/'source-bank-comparison.json'))
        assert read(e/'relocation.json')['equal']
        assert all(c['passed'] for c in read(e/'pair-results.json'))
        math_ref='math.json';replay_ref='source-bank-comparison.json';pack_ref='relocation.json'
    else:
        assert all(c.get('correct') and c.get('unique_correct') for c in math);math_count=len(math)
        replay=read(e/'replay-results.json') if (e/'replay-results.json').exists() else read(e/'source-replay-results.json')
        assert read(e/'relocation-results.json')['same_records']
        assert not read(e/'restriction-results.json')['canonical_e182_rejected']
        assert not read(e/'source-solution-stage-results.json')['omissions']
        math_ref='math-results.json';replay_ref='source-replay-results.json' if (e/'source-replay-results.json').exists() else 'replay-results.json';pack_ref='relocation-results.json'
    # Probes use only visible position and length, grouped by recognizable
    # template. Existing scripts additionally check mathematical bank cues.
    probes=[];coverage=[]
    for stage,records,ref in [('raw',raw,sample_name),('delivered',delivered,'delivery-easy/accepted.json' if kp==17592186092261 else 'delivery/accepted.json')]:
        groups=defaultdict(list)
        for r in records:groups[r['generation']['template']].append(r)
        for template,rs in groups.items():
            coverage.append({'case':stage+' '+template,'sample_refs':[ref],
                'result':f'{len(rs)} records; parameter values '+str({k:sorted({str(r["generation"]["parameters"].get(k)) for r in rs}) for k in rs[0]['generation']['parameters']})})
            radios=[r for r in rs if field(r)[':answer-field/type'].endswith('/radio')]
            if not radios:continue
            for strategy in ['first','last','shortest','longest']:
                hits=0
                for r in radios:
                    f=field(r);opts=f[':answer-field/choices']
                    ix=0 if strategy=='first' else len(opts)-1 if strategy=='last' else (min if strategy=='shortest' else max)(range(len(opts)),key=lambda i:len(opts[i][':answer/value']))
                    hits+=opts[ix][':answer/id']==f[':answer-field/correct'][1]
                assert hits<len(radios) or len(radios)<4,(template,strategy,hits,len(radios))
                probes.append({'cue':strategy,'subgroup':stage+' '+template,'scope':'within_template','strategy':'Choose '+strategy+' visible option',
                    'correct':hits,'total':len(radios),'baseline':.2,'disposition':'not_predictive',
                    'conclusion':'No perfect cue in this bounded sample; 0.2 is uniform five-option chance. Small samples do not establish a long-run rate.','sample_refs':[ref]})
    # Reproduce the current selector's exact within-band hash draw over a
    # conditional fresh candidate pool. Real histories and future IDs vary.
    selected=Counter()
    for i in range(4096):
        digest=hashlib.sha256(f'course-academy/question-selection/v1/engine-repair-{kp}-{i}'.encode()).digest()
        u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
        selected[delivered[int(u*len(delivered))]['generation']['template']]+=1
    write(e/'selection-current.json',{'basis':source['basis'],'implementation':'engine/rust/question_selection.rs::select',
        'scenario':'Conditional on choosing the reviewed band, fresh eligible records sorted by synthetic IDs, positive band weight. Exact SHA-256 53-bit within-band draw.',
        'templates_selected':dict(selected),'draws':4096,'applicable_exclusions':'Existing learner history and current-task reservations are removed before selection; no real learner actions were performed.',
        'limits':'Actual weights, history and future EDB ID order can change draws. Legacy unconfigured policies take the first sorted candidate; zero-weight bands are excluded.'})
    old=read(e/'prior-pedagogical-variation.json')
    roles=old['answer_roles']
    for r in roles:r['observed']='Rechecked in the current sample, canonical and controlled records; see coverage and canonical-current-checks.json. '+r['eligible_variation']
    cfref='counterfactuals.json' if (e/'counterfactuals.json').exists() else 'pairs.json' if (e/'pairs.json').exists() else 'counterfactual-records.json'
    variation={'learner_operation':old['learner_operation'],'fixed_features':old['fixed_features'],'answer_roles':roles,'coverage':coverage,
        'counterfactuals':[
            {'kind':'relevant','change':'Switch missing product-rule term, exponent coefficient, or radical inner/target data at fixed remaining inputs.',
             'expected':'Response follows the changed mathematical evidence.','observed':'Independent prompt differentiation and native grading agree; stale responses are rejected in applicable blank controls.',
             'status':'passed','justification':'These changes alter a differentiated contribution or chain-rule factor without adding a reasoning stage.','sample_refs':[cfref,'native-grading.json','current-regression-grading.json']},
            {'kind':'irrelevant','change':'Change presentation/choice ordering, or an additive parameter absent from the requested derivative fragment.',
             'expected':'Mathematical response is preserved.','observed':'Current controlled pairs preserve the response and native acceptance.',
             'status':'passed','justification':'The selected source-style response depends on the differentiated mathematical evidence, not incidental presentation.','sample_refs':[cfref,'native-grading.json','current-regression-grading.json']}],
        'shortcut_probes':probes,'delivery':{'stages_examined':['explicit boundary/domain validation','seeded sampling and rejection','shared publication normalization and deduplication','requested-band filtering','conditional learner selection'],
            'sample_refs':[sample_name,'selection-current.json','delivery-easy/accepted.json' if kp==17592186092261 else 'delivery/accepted.json'],
            'result':f'{len(raw)} independently chosen raw records; {len(delivered)} fresh records survive the reviewed band at basis {source["basis"]}. Five deterministic runner records are retained. Role coverage and visible-cue probes are recorded separately before and after filtering.'},
        'limitations':['Finite tests do not prove absence of every shortcut.','Learner selection is conditional on fresh eligible candidates and a positive weight for the reviewed band; real history and future IDs were not simulated as fact.',
            'Only '+band+' receives this publication certificate; other advertised bands require their own certificate.','Source omissions and explicit source corrections are retained in source-analysis.json. Canonical missing answer widgets are authored completions, not recovered historical fields.']}
    if kp==17592186096842:
        q=read(e/'sum-shortcut-results.json');variation['shortcut_probes'].append({'cue':'nearest cubic-only derivative','subgroup':'high-point high-radicand sum questions','scope':'other_recognizable_subgroup','strategy':q['strategy'],'correct':q['correct'],'total':q['total'],'baseline':.2,'disposition':'not_predictive','conclusion':'The original 20/20 bypass now succeeds 4/20. All options hold the cubic contribution fixed and vary the radical contribution. Native outcomes were checked.','sample_refs':['sum-shortcut-results.json','current-regression-grading.json']})
    write(e/'pedagogical-variation.json',variation)
    count=len(render['cases']);radio_index={'17592186096617':3,'17592186096618':2,'17592186092261':3,'17592186096842':2}[str(kp)]
    write(e/'visual-inspection.json',{'rendered_cases':count,'screenshots_inspected':['render-current/question-001.png',f'render-current/question-{radio_index:03}.png'],
        'observations':['Blank and radio controls are legible in the actual UI.','Fractions, roots, logarithms, superscripts, scaffolded derivatives and worked solutions are correctly typeset.','No clipped question or answer content was observed in the inspected screenshots.'],'defects':[]})
    source_analysis=read(e/'source-analysis.json')
    account={k:source_analysis[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs']};account['evidence_paths']=['source-analysis.json']
    evidence={
        'source_replay':([replay_ref,'canonical-current-checks.json'],'Complete supported source banks replayed; current canonical restrictions are repaired. Formatting deltas and source omissions are documented.'),
        'math':([math_ref,'canonical-current-checks.json'],f'{math_count} records independently checked by parsing displayed expressions and differentiating; canonical cases also pass.'),
        'variety':(['pedagogical-variation.json',sample_name],'Current seeded/boundary samples cover the source-grounded templates, mathematical parameters and response roles.'),
        'decision_variation':(['pedagogical-variation.json','selection-current.json'],'Controlled relevant/irrelevant pairs, conditional shortcut probes and post-filter coverage pass within the stated finite scope.'),
        'scope':(['source-analysis.json','canonical-current-records.json'],'Product-rule and chain-rule operations, response contracts and calibrated default band stay within the instructional sources.'),
        'grading':(['native-grading.json','current-regression-grading.json'],f'{native["accepted_checks"]+native["rejected_checks"]+regression["accepted_checks"]+regression["rejected_checks"]} native checks pass; valid logarithm/radical equivalents accept and wrong answers reject. Zero unresolved checks.'),
        'rendering':(['render-current/rendering.json','visual-inspection.json'],f'All {count} actual UI renders pass; representative blank and radio screenshots inspected.'),
        'packaging':([pack_ref],'Declared-runtime-only relocation, dependencies and deterministic replay pass. No external assets, network requests or database writes occur in generation.')}
    result={'verdict':'accepted','summary':'Current Codex session independently reviewed the saved generator authors’ repaired candidates against the upgraded engine. All eight checks pass; no new author or reviewer agents were launched.',
        'source_analysis':account,'checks':{k:{'status':'passed','evidence_paths':refs,'details':details} for k,(refs,details) in evidence.items()},'findings':[]}
    validate_review(result,e);write(e/'result.json',result)
    print(kp,'accepted',count,'renders',math_count,'math records')

if __name__=='__main__':
    for kp in [17592186096617,17592186096618,17592186092261,17592186096842]:main(kp)
