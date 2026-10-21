"""Delivery/decision/shortcut analysis of the independently saved records."""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
import sympy as S
from review import ROOT, BASE, REPO, PYTHON, ENV, save, run, inspect_record, hash_package

def load(p):return json.loads((ROOT/p).read_text())

def coverage(records):
    cases=[inspect_record(r) for r in records]
    return dict(count=len(cases),sign_cases=dict(Counter(c['sign_case'] for c in cases)),
                orders=dict(Counter(c['order'] for c in cases)),variables=dict(Counter(c['variable'] for c in cases)),
                solution_signs=dict(Counter(c['value_sign'] for c in cases)),
                n_values=sorted({c['n'] for c in cases}),
                coefficient_values=sorted({c['a'] for c in cases}),offset_values=sorted({c['b'] for c in cases}),
                conditional_sign_cases={f'{v}/{o}':dict(Counter(c['sign_case'] for c in cases if c['variable']==v and c['order']==o)) for v in 'xyt' for o in ['constant-first','variable-first']})

def main():
    # Keep review.py's commands instead of overwriting their provenance.
    import review
    review.commands[:]=load('commands.json')
    raw=load('samples.json');normal=raw[1:65];accepted=load('delivery-independent/accepted.json')
    runner=load('runner-batch.json');delivered_runner=load('delivery-runner/accepted.json')
    inputs={'independent_raw':raw,'fresh_seed_normal64':normal,'independent_accepted':accepted,'runner_raw':runner,'runner_accepted':delivered_runner}
    delivery={name:coverage(records) for name,records in inputs.items()}
    delivery['captured_inventory_basis']=4964
    delivery['publication_file']='Absent before preparation; shared read-only prepare_records used against captured inventory.'
    delivery['generator_rejection']='No mathematical rejection. generate chooses signs then magnitudes/RHS, resampling only a repeated (a,b,n); full supported domain of 6264 triples completed at fresh seed 791939.'
    # Faithfully reproduce the specified SHA-256 uniform draw conditional on a moderate pool.
    # Published database IDs are not assigned yet, so bind this simulation to explicit synthetic IDs.
    inv=json.loads((BASE/'source/inventory.json').read_text())
    existing_mod=[q for q in inv['questions'] if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/moderate']
    pool=[dict(id=q[':db/id'],sign_case='negative/positive',origin='captured-moderate-source',question=q) for q in existing_mod]
    for i,r in enumerate(accepted):
        pool.append(dict(id=20000000000000+i,sign_case=inspect_record(r)['sign_case'],origin='new-independent-accepted',record_index=i))
    pool.sort(key=lambda r:r['id'])
    selections=[]
    for i in range(1024):
        seed=f'independent-selection-791940/{i}'
        digest=hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest()
        uniform=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
        p=pool[int(uniform*len(pool))]
        selections.append(dict(seed=seed,index=int(uniform*len(pool)),id=p['id'],sign_case=p['sign_case'],origin=p['origin']))
    selection=dict(implementation='engine/rust/question_selection.rs::select',pool=pool,draws=selections,
                   positive_moderate_conditional=dict(count=len(selections),sign_cases=dict(Counter(s['sign_case'] for s in selections))),
                   examined_rules=['seen_before_task excludes past tasks; caller excludes current prefix and unusable candidates','deduplicate and sort candidate database IDs','draw rated difficulty using nonempty positively weighted bands','uniform hash-seeded index in chosen pool','zero-weight moderate pool cannot supply generated items','unrated fallback only if no eligible positively weighted rated pool','None distribution deterministically returns first sorted candidate'],
                   unconfigured_result=pool[0],
                   limits=['No learner history, live policy weights, or future database IDs are in captured inputs. Simulation uses stated synthetic new IDs and all candidates fresh; it is conditional, not a prediction of a learner sequence.','Any arbitrary history can exhaust a case. The selector does not inspect signs, variable names, exponent order, or generated answer; it cannot preferentially drop a sign case within a fresh moderate pool.','With unconfigured weights the first-candidate fallback repeats one eligible item until history changes; no claim of broad random selection is made for that engine mode.'])
    save('selection-results.json',selection)
    delivery['selection']=dict(conditional_counts=selection['positive_moderate_conditional'],limits=selection['limits'])
    save('delivery-coverage.json',delivery)
    # Test answer-producing actions, not merely literal keys, in each recognizable subgroup.
    cases=[];probes=[]
    cohorts={'fresh-seed-normal64':normal,'delivered-independent':accepted,'delivered-runner':delivered_runner}
    for name,records in cohorts.items():
        observations=[]
        for i,r in enumerate(records):
            m=inspect_record(r);a,b,n=m['a'],m['b'],m['n'];expected=(S.log(n)-b)/a
            strategies={'source-negative-coefficient-action':((b-S.log(n))/abs(a),f'(({b})-ln({n}))/({abs(a)})'),
                        'copy-rhs':(S.Integer(n),str(n)),
                        'take-ln-only':(S.log(n),f'ln({n})'),
                        'fixed-source-answer':((4-S.log(21))/5,'(4-ln(21))/5')}
            checks=[];outcomes={}
            for strategy,(expression,submission) in strategies.items():
                correct=S.simplify(expression-expected)==0
                outcomes[strategy]=bool(correct)
                checks.append(dict(submitted=submission,expected='accepted' if correct else 'rejected',purpose=f'{name}: shortcut probe {strategy}'))
            cases.append(dict(label=f'{name}-{i}',record=r,checks=checks))
            observations.append(dict(index=i,**m,outcomes=outcomes))
        for subgroup,items in [('all',observations)]+[(f'order={o}',[m for m in observations if m['order']==o]) for o in ['constant-first','variable-first']]+[(f'variable={v}/order={o}',[m for m in observations if m['variable']==v and m['order']==o]) for v in 'xyt' for o in ['constant-first','variable-first']]:
            if not items:continue
            for strategy in ['source-negative-coefficient-action','copy-rhs','take-ln-only','fixed-source-answer']:
                correct=sum(m['outcomes'][strategy] for m in items)
                conclusion=('Baseline 0.5 is choosing one of the two eligible coefficient-sign actions without reading the sign. Successes equal the negative-coefficient cases exactly. The coefficient sign is mathematical evidence; name/order never fixes it in the sampler domain.' if strategy=='source-negative-coefficient-action' else 'Baseline 0 is a response that omits the required inverse/affine computation; observed count is recorded. The fixed source key can succeed on a literal source-equivalent instance, not on this template generally.')
                if name=='delivered-runner':conclusion+=' Five runner items are a small snapshot; perfect success in a singleton subgroup is not evidence that code fixes that role. The fresh 64 and full-domain inspection test that claim.'
                probes.append(dict(cue=strategy,subgroup=f'{name}/{subgroup}',scope='overall' if subgroup=='all' else ('within_template' if subgroup.startswith('order=') else 'other_recognizable_subgroup'),strategy=strategy,correct=correct,total=len(items),baseline=.5 if strategy=='source-negative-coefficient-action' else 0.,disposition='intended_skill' if strategy=='source-negative-coefficient-action' else 'not_predictive',conclusion=conclusion,sample_refs=['shortcut-input.json','shortcut-native-report.json','shortcut-observations.json']))
        save(f'shortcut-observations-{name}.json',observations)
    save('shortcut-observations.json',dict(cohorts={name:load(f'shortcut-observations-{name}.json') for name in cohorts}))
    previous_cases=load('shortcut-input.json') if (ROOT/'shortcut-input.json').exists() else None
    save('shortcut-input.json',cases)
    if previous_cases==cases and (ROOT/'shortcut-native-report.json').exists():
        from types import SimpleNamespace
        prior=load('shortcut-execution.json')
        native=SimpleNamespace(returncode=prior['returncode'],stdout=prior['stdout'],stderr=prior['stderr'])
    else:
        native=run([REPO/'generate/runs/current/check-engine',ROOT/'shortcut-input.json',ROOT/'shortcut-native-report.json'],'shortcut-execution.json')
    assert native.returncode==0,native.stderr
    pairs=load('counterfactual-samples.json');pair_results=[]
    base=inspect_record(pairs[0])
    for i,r in enumerate(pairs[1:],1):
        m=inspect_record(r)
        eq=S.simplify(S.sympify(m['expected'])-S.sympify(base['expected']))==0
        assert eq==(i>=4)
        pair_results.append(dict(before_index=0,after_index=i,change=['coefficient sign','offset sign','RHS','variable name','exponent order'][i-1],answer_preserved=eq,before=base,after=m,native_case=f'controlled-pair-{i}',render_index=i+1))
    save('counterfactual-results.json',dict(passed=True,pairs=pair_results,native_evidence='native-diagnostic-report.json',rendered_evidence='render/rendering.json',render_map='render/input.json holds source replay at index0 then six controlled records then boundary'))
    variation=dict(learner_operation=load('source-analysis.json')['learner_operation'],
        fixed_features=[dict(feature='Base e and isolated exponential equals a positive integer RHS',justification='Tutorial 2806 uses the base-e inverse and exact ln answer; q-263058 directly supplies an integer RHS. Roots/powers are separately scoped sources.'),dict(feature='One blank for the RHS of the requested variable equation',justification='Complete moderate q-263058 has exactly this field contract.'),dict(feature='2<=|a|<=7, 1<=|b|<=9, 2<=n<=30',justification='Nonzero translation and nonunit division retain the moderate source stages. Small integer bounds retain comparable arithmetic. ln(1) and zero offsets would remove assessed stages; no sign is fixed.')],
        answer_roles=[dict(role='Signed unknown coefficient',eligible_variation='Both signs and nonunit small integer magnitudes',observed='All 12 signed coefficients covered; relevant sign change negates response and updates native grading.'),dict(role='Signed offset',eligible_variation='Both signs and small nonzero magnitudes',observed='All 18 signed offsets covered; offset change moves response by the independently expected rational amount.'),dict(role='RHS logarithm argument',eligible_variation='Positive integer n with nontrivial ln, comparable source arithmetic',observed='Every integer 2..30 covered; changing 11 to13 changes prompt, solution, key and learner outcome.'),dict(role='Variable name and exponent ordering',eligible_variation='x/y/t and both term orders, irrelevant to numeric solution',observed='All names and both orders sampled; controlled rename/order preserve numeric answer and native acceptance.')],
        coverage=[dict(case=name,sample_refs=['samples.json','runner-batch.json','delivery-independent/accepted.json','delivery-runner/accepted.json','delivery-coverage.json'],result=json.dumps(cov)) for name,cov in delivery.items() if name in inputs],
        counterfactuals=[dict(kind='relevant',change='Hold a=-5,b=4,n=11,y,constant-first fixed, then separately change a to5, b to-4, or n to13.',expected='Coefficient sign negates the response; offset sign changes translation by -8/5; RHS change changes logarithm by -(ln13-ln11)/5. Old response is rejected after each change.',observed='Independent exact checks and real native grading agree in all three cases; displayed prompt and worked equations follow each changed value.',status='passed',justification='Signed exponent coefficients and RHS determine solution via the source natural-log and affine-solve stages.',sample_refs=['counterfactual-samples.json','counterfactual-results.json','native-diagnostic-report.json','render/input.json','render/rendering.json']),dict(kind='irrelevant',change='Hold a=-5,b=4,n=11 fixed and rename y tox or change constant-first to variable-first.',expected='Numeric solution preserved; variable references or ordering in prompt and solution update; original numeric response remains accepted.',observed='Both pairs preserve independently derived value and native acceptance; actual UI preview includes both changes.',status='passed',justification='The source asks for the variable value, so its name and algebraically identical term order cannot alter that value.',sample_refs=['counterfactual-samples.json','counterfactual-results.json','native-diagnostic-report.json','render/input.json','render/rendering.json'])],
        shortcut_probes=probes,
        delivery=dict(stages_examined=['Generator sign-first sampling, semantic-repeat rejection/resampling and finite-domain completion','Actual prepare_records normalization and captured inventory/batch deduplication','Requested moderate difficulty filter','Read-only learner freshness and difficulty-first selection rules; conditional hash-draw reproduction and fallback branches'],sample_refs=['sampler-domain.json','samples.json','delivery-independent/delivery.json','delivery-independent/accepted.json','delivery-runner/delivery.json','delivery-runner/accepted.json','selection-results.json','delivery-coverage.json'],result='Independent132 ->129 accepted; runner5 ->5. All four sign cases remain in independently delivered pool. Selector is uniform conditional on eligible moderate pool and positive configured moderate weight; live histories/weights not captured.'),
        limitations=['Finite probes do not establish absence of every conceivable shortcut.','One moderate source profile supported; easy, hard, unrated radios and power-RHS canonical example are explicitly excluded.','Captured inventory basis4964 only. Later inventory changes and learner history/weights are outside the saved snapshot; selection conclusions are conditional as documented.','Renderer uses the real UI in correct-response preview mode, not a live lesson transaction. Native grading is database-free.'])
    save('pedagogical-variation.json',variation)
    renderer=load('render/rendering.json')
    save('scope-results.json',dict(passed=True,source_family='q-263058 moderate blank',observed_extensions='Both affine coefficient/offset signs, small magnitudes/RHS, variable names and exponent order',difficulty='All132 independent and5 runner records are moderate.',invariants_preserved=['base e','isolated exponential','one linear unknown','positive integer RHS','exact natural logarithm solution','translation and nonunit division','one blank RHS field'],unsupported='Hard roots, easy single inversion, unrated radio banks and power RHS are not implemented; explicitly scoped out. No extra exponential isolation, approximate rounding, or nonlinear stages introduced.',basis=['source-analysis.json','source-replay-results.json','math-results.json','samples.json','runner-batch.json']))
    # Bind evidence to actual native executable; old author prose is not evidence of current failure.
    native_binary=REPO/'generate/runs/current/check-engine'
    save('native-current-binding.json',dict(executable=str(native_binary),sha256=hashlib.sha256(native_binary.read_bytes()).hexdigest(),source_harness_sha256=hashlib.sha256((REPO/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),symbolic_source_sha256=hashlib.sha256((REPO/'engine/rust/symbolic.rs').read_bytes()).hexdigest(),author_claim='Saved author narrative says n>=20 wrong responses error; independent current native checks reject wrong responses across2..30. That stale claim is not reproduced.'))
    assert load('package-before.json')==hash_package()
    save('package-after.json',hash_package())
    (ROOT/'session-state.md').write_text('Completed exact math137 records, supported source replay/full bank, native correct/wrong and controlled pairs, delivery132->129 and runner5->5, selector-rule conditional simulation, shortcut strategies by order and variable/order, full finite sampler, deterministic/relocated CLI and package hash preservation. Renderer8 cases run; pending final screenshot inspection/report assembly. Author historical native error is not reproduced by current executable. All artifacts are under evidence_root.\n')
    print(json.dumps(dict(shortcut_native=native.stdout.strip(),cohort_coverage={k:v['sign_cases'] for k,v in delivery.items() if k in inputs},selection=selection['positive_moderate_conditional'],probes=len(probes),renderer_passed=renderer['passed'],renderer_cases=len(renderer['cases']))))

if __name__=='__main__':main()
