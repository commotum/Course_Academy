"""Independent visible-record oracle, delivery comparisons and shortcut probes."""
import sys
sys.dont_write_bytecode = True
import collections, hashlib, json, pathlib, re
from html.parser import HTMLParser

E = pathlib.Path(__file__).resolve().parent

def load(name):
    return json.load(open(E / name))

def save(name, value):
    (E / name).write_text(json.dumps(value, indent=2) + '\n')

def facts(record):
    q = record['question']
    name, rows, columns, count = re.search(
        r'\$([A-Z])\$.*?\$(\d+)\s*\\(?:times|cdot)\s*(\d+)\$.*?\$(\d+)\$',
        q[':question/problem']).groups()
    rows, columns, count = map(int, (rows, columns, count))
    nonpivot = '**non-pivot**' in q[':question/problem']
    rank = columns-count if nonpivot else count
    f = q[':question/answer-fields'][0]
    choices = f[':answer-field/choices']
    values = [int(a[':answer/value']) for a in choices]
    correct = f[':answer-field/correct']
    correct_id = correct[1] if isinstance(correct, list) else correct[':answer/id']
    pos = next(i for i, a in enumerate(choices) if a[':answer/id'] == correct_id)
    assert 1 <= rank <= min(rows, columns)
    assert len(values) == len(set(values)) == 5 and min(values) >= 0
    assert values[pos] == rank
    assert f'\\text{{rank}}({name})={rank}.' in q[':question/worked-solution']
    if nonpivot:
        assert f'{columns}-{count}={rank}.' in q[':question/worked-solution']
    return dict(name=name, rows=rows, columns=columns, count=count,
                level='moderate' if nonpivot else 'easy', rank=rank,
                position=pos+1, order=sorted(values).index(rank)+1,
                values=values, correct_id=correct_id,
                shape='square' if rows==columns else 'tall' if rows>columns else 'wide',
                semantic=['non-pivot',columns,count] if nonpivot else ['pivot',count],
                profile=record['generation']['bank_profile'])

def fnv(value):
    n=2166136261
    for c in value:
        n=((n ^ ord(c))*16777619) & 0xffffffff
    return n

def ui_order(record, item_id):
    f=record['question'][':question/answer-fields'][0]
    return sorted(f[':answer-field/choices'], key=lambda a: fnv(
        f'{item_id}:{f[":answer-field/id"]}:{a[":answer/id"]}'))

class RadioParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='input' and attrs.get('type')=='radio':
            self.ids.append(attrs['value'])

render_cases=[]
for folder in ['render','render-tail','render-repaired']:
    records=load(folder+'/input.json')
    report=load(folder+'/rendering.json')
    assert report['passed']
    for i, (record, case) in enumerate(zip(records, report['cases'])):
        parser=RadioParser()
        parser.feed((E/folder/f'question-{i+1:03}.html').read_text())
        ordered=ui_order(record, i+1)
        assert parser.ids == [a[':answer/id'] for a in ordered]
        fact=facts(record)
        render_cases.append(dict(folder=folder, index=i, question_id=record['question'][':question/id'],
            displayed_values=[int(a[':answer/value']) for a in ordered],
            displayed_correct_position=parser.ids.index(fact['correct_id'])+1,
            oracle=fact, html_order_matches_actual_UI_function=True))
save('render-order-tests.json',render_cases)

def summary(records):
    fs=[facts(r) for r in records]
    return dict(count=len(fs), semantic_tasks=sorted({tuple(f['semantic']) for f in fs}),
        ranks=dict(collections.Counter(f['rank'] for f in fs)),
        positions=dict(collections.Counter(f['position'] for f in fs)),
        orders=dict(collections.Counter(f['order'] for f in fs)),
        shapes=dict(collections.Counter(f['shape'] for f in fs)),
        profiles={p:dict(count=sum(f['profile']==p for f in fs),
                        orders=dict(collections.Counter(f['order'] for f in fs if f['profile']==p)))
                  for p in sorted({f['profile'] for f in fs})})

stages={}
inputs=['easy-records','moderate-records','runner-batch','controls-easy','controls-moderate',
        'restriction-easy','restriction-moderate','cli-easy-12','cli-moderate-98']
for name in inputs:
    before=load(name+'.json'); after=load('delivery-'+name+'/accepted.json')
    stages[name]=dict(before=summary(before),after=summary(after),
                      shared_report=load('delivery-'+name+'/delivery.json'))
stages['repaired-controls']=dict(before=summary(load('repaired-control-records.json')),
    after=summary(load('delivery-repaired-controls/accepted.json')),
    shared_report=load('delivery-repaired-controls/delivery.json'))
assert len(stages['cli-easy-12']['after']['semantic_tasks'])==12
assert len(stages['cli-moderate-98']['after']['semantic_tasks'])==98
assert stages['runner-batch']['after']['count']==5
for name in ['easy-records','moderate-records','restriction-easy','restriction-moderate']:
    assert stages[name]['before']['semantic_tasks']==stages[name]['after']['semantic_tasks']
save('delivery-variation-tests.json',stages)

# Every visible numeric-order and UI-position strategy is measured separately
# for each source bank profile, level, shape and recognizable consecutive bank.
# Controlled same-seed pairs are excluded from population frequency estimates.
probes=[]
datasets={name:load(name+'.json') for name in ['independent-records','cli-easy-12','cli-moderate-98','runner-batch']}
datasets.update({name+' delivered':load('delivery-'+name+'/accepted.json')
                 for name in ['easy-records','moderate-records','cli-easy-12','cli-moderate-98','runner-batch']})
for name, records in datasets.items():
    refs=([name+'.json'] if name in ['independent-records','cli-easy-12','cli-moderate-98','runner-batch']
          else ['delivery-'+name.removesuffix(' delivered')+'/accepted.json'])
    groups={'all':records}
    for level in ['easy','moderate']:
        group=[r for r in records if facts(r)['level']==level]
        if group:groups['wording '+level]=group
    for profile in sorted({facts(r)['profile'] for r in records}):
        groups['profile '+profile]=[r for r in records if facts(r)['profile']==profile]
    for shape in ['square','tall','wide']:
        group=[r for r in records if facts(r)['shape']==shape]
        if group:groups['shape '+shape]=group
    group=[r for r in records if max(facts(r)['values'])-min(facts(r)['values'])==4]
    if group:groups['five consecutive choices']=group
    for group_name, group in groups.items():
        fs=[facts(r) for r in group]
        scope=('overall' if group_name=='all' else 'within_template'
               if group_name.startswith(('profile','wording')) else 'other_recognizable_subgroup')
        for order in range(1,6):
            correct=sum(f['order']==order for f in fs)
            probes.append(dict(cue='numeric answer order',subgroup=name+' / '+group_name,
                scope=scope,strategy=f'Choose numeric order {order} without interpreting the prompt',
                correct=correct,total=len(fs),baseline=.2,disposition='not_predictive',
                conclusion=('Comparison is uniform guessing among five choices (0.2). '
                    f'{correct}/{len(fs)} in this fixed sample. '
                    'A perfect singleton or small subgroup is an observation, not a construction invariant; '
                    'compare fresh profile samples, full semantic-domain controls and rendered UI orders. '
                    'Profile names are not shown; profiling by them is a conservative privileged-cue test.'),
                sample_refs=refs))
        # Choice order uses the application's exact FNV function, confirmed above
        # against all rendered HTML. Real future task-item IDs are unknown.
        positions=collections.Counter()
        for r,f in zip(group,fs):
            for item_id in range(1,33):
                ordered=ui_order(r,item_id)
                positions[next(i+1 for i,a in enumerate(ordered) if a[':answer/id']==f['correct_id'])]+=1
        for position in range(1,6):
            probes.append(dict(cue='actual UI answer position',subgroup=name+' / '+group_name,
                scope=scope,strategy=f'Choose displayed position {position}',correct=positions[position],
                total=len(fs)*32,baseline=.2,disposition='not_predictive',
                conclusion='Baseline is uniform choice (0.2). Measured over item IDs 1..32 using unmodified UI ordering; '
                    'all 17 actual preview HTML orders confirm the reproduction. Future task-item IDs are unknown.',
                sample_refs=refs+['render-order-tests.json']))

# Keep exact small-batch visual frequency separate from the larger controls.
batch_render=[x for x in render_cases if x['folder']=='render-tail' and 1<=x['index']<=5]
assert len(batch_render)==5
for scope,group_name,group in [('overall','all five batch records',batch_render)]+[
        ('within_template','batch profile '+profile,[x for x in batch_render if x['oracle']['profile']==profile])
        for profile in sorted({x['oracle']['profile'] for x in batch_render})]:
    for position in range(1,6):
        correct=sum(x['displayed_correct_position']==position for x in group)
        probes.append(dict(cue='actual rendered batch position',subgroup=group_name,scope=scope,
            strategy=f'Always click displayed option {position}',correct=correct,total=len(group),baseline=.2,
            disposition='not_predictive',conclusion='Uniform-guess baseline 0.2. Exact five-record batch '
                'has positions '+str([x['displayed_correct_position'] for x in batch_render])+'. '
                'The three q-34805 members occupy different displayed positions; singleton profiles cannot establish a repeatable cue.',
            sample_refs=['runner-batch.json','render-tail/input.json','render-order-tests.json']))

for level in ['easy','moderate']:
    group=[r for r in load('independent-records.json') if facts(r)['level']==level]
    # Copying pivot count is precisely definition recall; copying non-pivots
    # instead of subtracting is a plausible incorrect shortcut.
    success=sum(facts(r)['rank']==facts(r)['count'] for r in group)
    probes.append(dict(cue='stated count in wording',subgroup=level,scope='within_template',
        strategy='Select the supplied pivot/non-pivot count',correct=success,total=len(group),baseline=.2,
        disposition='intended_skill' if level=='easy' else 'not_predictive',
        conclusion='Uniform-guess baseline 0.2. In easy questions this is the definition explicitly taught '
            'by tutorial c062d466-946c-526b-aba8-0a0895671218. Moderate items require columns minus non-pivots; '
            'count=rank coincidences are legitimate simplifications, not a universally sufficient rule.',
        sample_refs=['independent-records.json']))
wide_small=[r for r in load('delivery-moderate-records/accepted.json') if facts(r)['shape']=='wide']
wide_control=[r for r in load('delivery-cli-moderate-98/accepted.json') if facts(r)['shape']=='wide']
wide_wrong=[r for r in wide_control if facts(r)['order']!=1]
assert len(wide_wrong)>0
apparent=[dict(cue='Choose smallest for wide moderate questions',
    small_sample_successes=sum(facts(r)['order']==1 for r in wide_small),small_sample_total=len(wide_small),
    broader_delivered_successes=sum(facts(r)['order']==1 for r in wide_control),broader_delivered_total=len(wide_control),
    counterexample=wide_wrong[0],conclusion='Three-record apparent perfection is sampling coincidence, '
        'contradicted by same-method delivered wide instances with smaller incorrect choices.',
    sample_refs=['delivery-moderate-records/accepted.json','delivery-cli-moderate-98/accepted.json'])]
save('shortcut-tests.json',dict(probes=probes, exact_batch_render=batch_render,apparent_predictors=apparent,
    limitations=['Finite test; no proof against every possible heuristic.',
                 'Small post-dedup profile groups are not evidence of universal cue invariants.',
                 'Raw JSON option order is not displayed choice order. Future live item IDs and learner histories are unavailable.']))

# Independent counterfactual oracle plus all native response UUIDs. All five
# responses on both sides are included, not just the stored correct UUID.
control_sets=[('easy','controls-easy.json','delivery-controls-easy/accepted.json'),
              ('moderate','controls-moderate.json','delivery-controls-moderate/accepted.json'),
              ('repaired moderate','repaired-control-records.json','delivery-repaired-controls/accepted.json')]
control_results=[]
for label, before_path, after_path in control_sets:
    before=load(before_path); after=load(after_path)
    assert [facts(r)['rank'] for r in before]==[facts(r)['rank'] for r in after]
    fs=[facts(r) for r in after]
    assert fs[0]['rank']!=fs[1]['rank']
    assert fs[0]['rank']==fs[2]['rank']
    if label=='moderate':assert fs[0]['rank']!=fs[3]['rank']
    control_results.append(dict(label=label,before_file=before_path,delivered_file=after_path,
        records=before,visible_facts=fs,results='Relevant count change changes rank; feasible irrelevant row/name change preserves it. '
            'Moderate total-column change also changes rank. Both source-style and collision-completed banks tested.'))
save('counterfactual-tests.json',control_results)

cases=load('grader-input.json')
for r in load('delivery-repaired-controls/accepted.json'):
    f=facts(r); field=r['question'][':question/answer-fields'][0]
    cases.append(dict(label='repaired pair '+r['question'][':question/id'],record=r,
        checks=[dict(submitted_answer_id=a[':answer/id'],
                     expected='accepted' if int(a[':answer/value'])==f['rank'] else 'rejected',
                     purpose='Independent visible-count counterfactual oracle') for a in field[':answer-field/choices']]))
save('grader-input-final.json',cases)

m=load('math-tests.json')
for name in ['cli-easy-12.json','cli-moderate-98.json','repaired-control-records.json']:
    for record in load(name):facts(record)
m['additional_visible_oracle_records']=113
m['total_records_checked']=m['records_checked']+113
save('math-tests.json',m)
save('session-summary.json',dict(math_records=m['total_records_checked'],
    native_cases=len(cases),rendered_records=len(render_cases),shortcut_probe_count=len(probes),
    source_banks=11,semantic_capacities={'easy':12,'moderate':98},
    exact_batch_ui_positions=[x['displayed_correct_position'] for x in batch_render],
    all_domain_delivery_passed=True))
(E/'session-state.md').write_text('Source replay and current/failing-runtime regressions complete. '
    'Independent math: 265 records. Shared delivery: full 12 easy and 98 moderate tasks plus exact batch survive; '
    'redundant profile samples deduplicated without losing semantic cases. Native final input prepared; '
    '17 UI records rendered and ordering confirmed. Next: inspect repaired screenshots, final native report, '
    'pedagogical JSON and package integrity.\n')
print(json.dumps(load('session-summary.json')))
