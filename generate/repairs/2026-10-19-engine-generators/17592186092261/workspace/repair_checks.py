"""Targeted review repair and small regression; all writes stay in workspace.

Run with the job Python. A successful script means observations reproduced;
repair-summary.json deliberately remains unsupported if valid entries fail.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import sympy as sp
import generator as g
import audit_variation

P = Path(__file__).resolve().parent
E = P / 'evidence' / 'repair'
E.mkdir(parents=True, exist_ok=True)
REPO = Path('/home/jake/Developer/Course_Academy')
ENGINE = REPO / 'generate/runs/current/check-engine'
commands = []


def save(name, value):
    (E / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def run(args, name, expected_success=True, env=None, cwd=P):
    command = [str(v) for v in args]
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    commands.append({'command': command, 'exit_code': result.returncode,
                     'log': 'evidence/repair/' + name})
    (E / name).write_text(result.stdout + result.stderr)
    assert (result.returncode == 0) == expected_success, (name, result.stderr[-1500:])
    return result


def field(record):
    return record['question'][':question/answer-fields'][0]


def answer(record):
    f = field(record)
    return next(a for a in f[':answer-field/choices']
                if a[':answer/id'] == f[':answer-field/correct'][1])


def key_math(record):
    return sp.sympify(record['generation']['answer_math'][answer(record)[':answer/id']],
                      locals={'x': g.X})


def independent(p):
    x = g.X
    f = p['c'] * sp.Pow(p['b'], p['a'] * x**p['n'] + p['k']*x**2 + p['l']*x + p['d'])
    derivative = sp.diff(f, x)
    if p.get('equation'):
        t = sp.Rational(p['point'])
        return sp.expand(f.subs(x,t) + derivative.subs(x,t)*(x-t))
    if 'point' in p:
        return derivative.subs(x, sp.Rational(p['point']))
    if p.get('fragment'):
        return sp.cancel(derivative / sp.Pow(p['b'], p['a'] * x**p['n'] + p['l']*x + p['d']))
    return derivative


def grade_case(record, label):
    f = field(record)
    if f[':answer-field/type'].endswith('/radio'):
        checks = [{'submitted_answer_id': a[':answer/id'],
                   'expected': 'accepted' if a[':answer/id'] == answer(record)[':answer/id'] else 'rejected',
                   'purpose': 'all actual learner choice IDs'} for a in f[':answer-field/choices']]
    else:
        correct = answer(record)[':answer/value']
        checks = [{'submitted': value, 'expected': outcome, 'purpose': purpose}
                  for value, outcome, purpose in [
                      (correct, 'accepted', 'canonical derivative'),
                      ('2*(' + correct + ')/2', 'accepted', 'equivalent rescaling'),
                      ('-(' + correct + ')', 'rejected', 'wrong sign'),
                      ('(' + correct + ')+1', 'rejected', 'wrong offset')]]
    return {'label': label, 'record': record, 'checks': checks}


def fixture(value, tag):
    aid = g.uid([tag, value])
    return {'knowledge_point': g.KP, 'generation': {'template': 'independent-display-check'},
            'question': {':question/id': g.uid(tag), ':question/problem': 'Check {{field-1}}',
                         ':question/answer-fields': [{':answer-field/id': g.uid([tag, 'field']),
                            ':answer-field/key': 'field-1', ':answer-field/type': ':answer-field.type/blank',
                            ':answer-field/choices': [{':answer/id': aid, ':answer/type': ':answer.type/math',
                                                       ':answer/value': value}],
                            ':answer-field/correct': [':answer/id', aid]}]}}


# Preserve all 13 implemented replays and their complete fields/banks.
old = json.loads((P / 'evidence/source-replay.json').read_text())
replays = []
for previous in old:
    qid = previous['generation']['template']
    current = g.generate(g.SPECS[qid]['level'], seed=17, template=qid,
                         parameters=g.default_params(qid), profile='historical:' + qid)
    assert current['question'] == previous['question'], qid
    assert sp.simplify(key_math(current) - independent(g.complete(qid, None))) == 0
    replays.append(current)
canonical = g.generate('easy', seed=17, template='e-728', parameters=g.default_params('e-728'))
assert canonical['question'][':question/problem'].startswith(g.normalize_prose(g.normalized(g.CANONICAL[':question/problem'])))
assert canonical['question'][':question/worked-solution'] == g.normalize_prose(g.normalized(g.CANONICAL[':question/worked-solution']))
assert sp.simplify(key_math(canonical) + 3 * 2**(1-g.X) * sp.log(2)) == 0
replays.append(canonical)
save('source-replay.json', replays)
save('source-replay-results.json', {'unchanged_practice_replays': len(old),
     'previous_complete_bank_evidence': '../source-fidelity.json',
     'canonical_replayed': True, 'canonical_authored_blank': True, 'failures': []})

records = []
native = [grade_case(r, 'source replay ' + r['generation']['template']) for r in replays]
pairs = []


def add_record(record):
    p = g.complete(record['generation']['template'], record['generation']['parameters'])
    expected = independent(p)
    assert sp.simplify(key_math(record)-expected) == 0
    f = field(record)
    for a in f[':answer-field/choices']:
        v = sp.sympify(record['generation']['answer_math'][a[':answer/id']], locals={'x': g.X})
        if f[':answer-field/type'].endswith('/radio'):
            assert (sp.simplify(v-expected) == 0) == (a[':answer/id'] == answer(record)[':answer/id'])
    records.append(record)
    native.append(grade_case(record, 'targeted ' + str(len(records))))
    if record['generation']['template'] in ('e-728', 'q-107461'):
        # Independent construction checks visible function and final derivative,
        # using actual native parsing rather than trusting answer metadata.
        prompt = record['question'][':question/problem']
        visible = re.search(r'(?:f\(x\)|y)\s*=\s*(.*?)\$', prompt)[1].rstrip(',')
        function = p['c'] * sp.Pow(p['b'], p['a']*g.X + p['d'])
        aligned = re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', record['question'][':question/worked-solution'], re.S)
        final_rhs = aligned[0].split('\\\\')[-1].split('=', 1)[1].strip().rstrip('.')
        for label, reference, submitted in [('prompt', function, visible), ('solution', expected, final_rhs)]:
            native.append({'label': str(len(records)) + ' displayed ' + label,
                'record': fixture(g.tex(reference), [len(records), label]),
                'checks': [{'submitted': submitted, 'expected': 'accepted',
                            'purpose': 'independent calculus vs displayed ' + label}]})


# Controlled outside-multiplier evidence, with unchanged base, exponent and seed.
for qid in ('e-728', 'q-107461'):
    pair = [g.generate('easy', seed=401991, template=qid,
                      parameters={**g.default_params(qid), 'c': c}) for c in (1, 3)]
    assert sp.simplify(key_math(pair[1]) - 3*key_math(pair[0])) == 0
    for key in (':question/problem', ':question/worked-solution'):
        assert pair[0]['question'][key] != pair[1]['question'][key]
    pairs.append({'template': qid, 'changed_only': 'c: 1 -> 3', 'key_multiplier': 3,
                  'prompt_and_solution_changed': True, 'records': pair})
    for r in pair:
        add_record(r)
    if qid == 'e-728':
        for i, r in enumerate(pair):
            # Old response must cease to grade correctly when the multiplier changes.
            native.append({'label': 'scale cross-response ' + str(i), 'record': r,
                           'checks': [{'submitted': answer(pair[1-i])[':answer/value'],
                                       'expected': 'rejected', 'purpose': 'other multiplier response'}]})

# Canonical boundary slots, both signs, and unit/nonunit inner derivatives.
for base in range(2, 7):
    for sign in (-1, 1):
        p = {**g.default_params('e-728'), 'b': base, 'a': sign,
             'c': 1 if sign == -1 else 5, 'd': -5 if sign == -1 else 5}
        add_record(g.generate('easy', seed=810000+base*2+sign, template='e-728', parameters=p))
for qid in ('e-728', 'q-107461'):
    for seed in (10, 11, 12, 13, 14, 15):
        add_record(g.generate('easy', seed=seed, template=qid))

# Small regression across unchanged easy, moderate and hard families.
for qid, level in [('q-48565','easy'), ('q-71881','easy'), ('q-340969','moderate'),
                   ('q-340970','moderate'), ('q-107463','hard')]:
    add_record(g.generate(level, seed=820001, template=qid))
save('counterfactuals.json', pairs)
save('test-records.json', records)
save('grader-input.json', native)
run([ENGINE, E/'grader-input.json', E/'grading.json'], 'grading.log')

# Reproduce the exact review defect; neither alternative-bank completion nor
# switching the single canonical answer makes both valid spellings accepted.
defect = g.generate('easy', seed=782006, template='q-312462')
assert defect['generation']['parameters'] == {'b':4,'c':1,'a':-5,'n':3,'k':0,'l':0,'d':1}
canonical_text = r'-15x^2\ln(4)'
equivalent_text = r'-30x^2\ln(2)'
assert sp.simplify(-15*g.X**2*sp.log(4) + 30*g.X**2*sp.log(2)) == 0
alternate = copy.deepcopy(defect)
alt = {':answer/id':g.uid('review-repair-alternate'), ':answer/type':':answer.type/math',
       ':answer/value':equivalent_text}
field(alternate)[':answer-field/choices'].append(alt)
reverse = copy.deepcopy(alternate)
field(reverse)[':answer-field/correct'] = [':answer/id', alt[':answer/id']]
defect_records = [defect, alternate, reverse]
save('grading-limit-records.json', defect_records)


def defect_cases(rows):
    out = []
    for i, r in enumerate(rows):
        prime_canonical = '30' in answer(r)[':answer/value']
        checks = [{'submitted': canonical_text, 'expected': 'unresolved' if prime_canonical else 'accepted',
                   'purpose': 'valid source-base logarithm'},
                  {'submitted': equivalent_text, 'expected': 'accepted' if prime_canonical else 'unresolved',
                   'purpose': 'valid integer-log identity; unresolved is a blocking defect'},
                  {'submitted': '-15x^2' + (r'\ln(2)' if prime_canonical else r'\ln(4)'),
                   'expected': 'rejected' if prime_canonical else 'accepted',
                   'purpose': 'factor sensitivity'},
                  {'submitted': '15x^2' + (r'\ln(2)' if prime_canonical else r'\ln(4)'),
                   'expected': 'rejected', 'purpose': 'wrong sign in canonical log basis'},
                  {'submitted': '-14x^2' + (r'\ln(2)' if prime_canonical else r'\ln(4)'),
                   'expected': 'rejected', 'purpose': 'wrong coefficient'}]
        out.append({'label': 'grading blocker variant ' + str(i), 'record': r, 'checks': checks})
    return out


save('grading-limit-input.json', defect_cases(defect_records))
run([ENGINE, E/'grading-limit-input.json', E/'grading-limit.json'], 'grading-limit.log')
# Also retain the unsatisfied acceptance test as an actual failing command.
acceptance = [{'label':'required valid ln4=2ln2 response', 'record':defect,
              'checks':[{'submitted':equivalent_text, 'expected':'accepted',
                         'purpose':'review acceptance criterion; currently fails'}]}]
save('required-acceptance-input.json', acceptance)
run([ENGINE, E/'required-acceptance-input.json', E/'required-acceptance.json'],
    'required-acceptance-failure.log', expected_success=False)

accepted = []
deliveries = {}
for band in ('easy', 'moderate', 'hard'):
    save(band + '-records.json', [r for r in records if r['question'][':question/difficulty'].endswith('/'+band)])
    out = E / ('delivery-' + band)
    run([sys.executable, REPO/'generate/pipeline/check_delivery.py', '--input', E/(band+'-records.json'),
         '--source', P.parent/'source/source.json', '--inventory', P.parent/'source/inventory.json',
         '--difficulty', band, '--output', out, '--asset-root', E, '--math-root', '/media/jake/SSD/EDB/math'],
        'delivery-' + band + '.log')
    accepted.extend(json.loads((out/'accepted.json').read_text()))
    deliveries[band] = json.loads((out/'delivery.json').read_text())
save('accepted.json', accepted)
save('post-delivery-grader-input.json', [grade_case(r, 'delivered '+str(i)) for i,r in enumerate(accepted)])
run([ENGINE, E/'post-delivery-grader-input.json', E/'post-delivery-grading.json'], 'post-delivery-grading.log')
out = E/'delivery-grading-limit'
run([sys.executable, REPO/'generate/pipeline/check_delivery.py', '--input', E/'grading-limit-records.json',
     '--source', P.parent/'source/source.json', '--inventory', P.parent/'source/inventory.json',
     '--difficulty', 'easy', '--output', out, '--asset-root', E, '--math-root', '/media/jake/SSD/EDB/math'],
    'delivery-grading-limit.log')
delivered_defects = json.loads((out/'accepted.json').read_text())
save('post-delivery-grading-limit-input.json', defect_cases(delivered_defects))
run([ENGINE, E/'post-delivery-grading-limit-input.json', E/'post-delivery-grading-limit.json'],
    'post-delivery-grading-limit.log')

# Reuse existing within-template probes; supply the unfiltered answer-ID mapping.
audit_variation.REFERENCE = {(r['generation']['template'],json.dumps(r['generation']['parameters'],sort_keys=True),
                             r['generation']['seed']):r for r in records}
coverage = {}
for label, rows in [('before', records), ('after', accepted)]:
    report = {'templates':audit_variation.audit(rows), 'conditional_a_sign':{}}
    for sign in (-1,1):
        report['conditional_a_sign'][str(sign)] = audit_variation.audit(
            [r for r in rows if (1 if r['generation']['parameters']['a']>0 else -1)==sign])
    # The new family has a blank, so fixed correct response is the relevant
    # literal-answer shortcut; radio position/bank cues remain in q-107461.
    save('variation-' + label + '.json', report)
    coverage[label] = {q:{'records':v['instances'], 'semantic_instances':v['semantic_instances'],
                           'slots':v['slots'], 'bank_roles':v['bank_roles'],
                           'deterministic_surface_predictors':v['deterministic_surface_predictors'],
                           'distinct_correct_values':v['distinct_correct_values']}
                       for q,v in report['templates'].items() if q in ('e-728','q-107461')}

# Confirm the new family is reachable through the public unforced sampler,
# retaining a small five-question CLI batch for independent review.
samples = [g.generate('easy', seed=18+i) for i in range(5)]
save('samples.json', samples)
normal_templates = {r['generation']['template'] for r in samples}
unforced = None
if 'e-728' not in normal_templates:
    for seed in range(40):
        if __import__('random').Random(seed).choice([q for q,s in g.SPECS.items() if s['level']=='easy']) == 'e-728':
            unforced = g.generate('easy', seed=seed)
            assert unforced['generation']['template'] == 'e-728'
            break
    assert unforced is not None
save('unforced-canonical.json', unforced or next(r for r in samples if r['generation']['template']=='e-728'))
manifest = json.loads((P/'package.json').read_text())
assert manifest['dependencies'] == {'python':sys.version.split()[0], 'packages':{'sympy':sp.__version__}}
with tempfile.TemporaryDirectory(prefix='ca-repair-') as temp:
    temp = Path(temp)
    for name in manifest['files']:
        shutil.copyfile(P/name, temp/name)
    result = run([sys.executable,temp/manifest['entrypoint'],'--difficulty','easy','--count','5',
                  '--seed','18','--format','json'], 'relocation.log',
                 env={**os.environ,'PYTHONPATH':'','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(temp/'outputs')}, cwd=temp)
    assert json.loads(result.stdout) == samples
save('relocation.json', {'passed':True, 'count':5, 'seed':18, 'files':manifest['files'],
                         'dependencies':manifest['dependencies']})
run([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',E/'samples.json',
     '--source',P.parent/'source/source.json','--inventory',P.parent/'source/inventory.json',
     '--difficulty','easy','--output',E/'delivery-batch','--asset-root',E,
     '--math-root','/media/jake/SSD/EDB/math'], 'delivery-batch.log')

render_records = [canonical] + pairs[0]['records'] + pairs[1]['records'] + [defect]
save('render-records.json', render_records)
run(['python3', REPO/'generate/pipeline/render_preview.py', '--input', E/'render-records.json',
     '--output', E/'render','--asset-root', E, '--math-root','/media/jake/SSD/EDB/math'], 'render.log')

save('commands.json', {'reproduce':[sys.executable,'repair_checks.py'], 'commands':commands})
save('repair-summary.json', {
    'status':'unsupported',
    'fidelity':{'unchanged_practice_replays':len(old),'canonical_original_parameters_replayed':True},
    'mathematical_correctness':{'targeted_records':len(records),'independent_checks_passed':True},
    'grading':{'scaled_linear_and_regression_passed':True,'valid_logarithm_equivalents':'unresolved',
               'alternate_choices_ignored':True,'switching_canonical_reverses_failure':True,
               'blocking_acceptance_test':'required-acceptance-failure.log'},
    'variation':coverage,
    'filtering':{band:{k:v[k] for k in ('input_count','accepted_count','duplicate_count')}
                 for band,v in deliveries.items()},
    'rendering':{'records':len(render_records),'visual_inspection':'pending'},
    'generator_rejections':g.REJECTIONS,
    'limitations':['Native grade_field compares only one canonical blank value and cannot prove ln(4)=2ln(2). '
                   'The package cannot add accepted alternatives or alter native canonicalization. '
                   'Fixing the learner engine is outside this workspace-only job.',
                   'Delivery is read-only; actual personalized learner selection remains unavailable.'],
    'generator_sha256':hashlib.sha256((P/'generator.py').read_bytes()).hexdigest()})
print(json.dumps({'status':'unsupported','unchanged_source_replays':len(old),
                  'canonical_replayed':True,'targeted_records':len(records),
                  'delivery_counts':{k:v['accepted_count'] for k,v in deliveries.items()},
                  'blocker':'valid logarithm equivalents remain unresolved by native grader'}))
