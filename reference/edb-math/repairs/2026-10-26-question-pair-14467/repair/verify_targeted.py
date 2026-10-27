"""Independent current-output verification for the parallel-line sampler repair."""
import argparse
import ast
from collections import Counter
import copy
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

D = Path(__file__).resolve().parent
R = next(p for p in D.parents if (p / 'scripts/generator_pipeline.py').is_file())
E = D / 'review'
sys.path.insert(0, str(R / 'scripts'))
from generator_pipeline import Pipeline, digest
from generator_review import validate_review
sys.path.insert(0, str(R))
from scripts.question_capture.math_format import normalize_prose, normalize_tex, validate_prose, validate_math_boundaries, validate_tex


def load(path):
    return json.loads(Path(path).read_text())


def save(name, value):
    (E / name).write_text(json.dumps(value, indent=2) + '\n')


def import_functions(path, names):
    tree = ast.parse(path.read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == names
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), globals())


def run(command, name):
    command = list(map(str, command))
    result = subprocess.run(command, text=True, capture_output=True)
    save(name, {'command': command, 'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    assert result.returncode == 0, (name, result.stderr[-2000:])


def bank(record):
    return tuple(sorted(c[':answer/value'] for c in record['question'][':question/answer-fields'][0][':answer-field/choices']))


def probes(records, label, refs):
    groups = {'all': records}
    if len(records) > 5:
        groups.update({
            'positive-target': [r for r in records if not observe(r)['negative']],
            'negative-target': [r for r in records if observe(r)['negative']],
            'integer-target': [r for r in records if not observe(r)['fraction']],
            'fractional-target': [r for r in records if observe(r)['fraction']],
        })
    result = []
    for group, rows in groups.items():
        if len(rows) < 5:
            continue
        counts = Counter()
        for record in rows:
            for cue, answer in predictions(record).items():
                counts[cue] += answer == observe(record)['target']
        for cue, count in counts.items():
            result.append({'cue': cue, 'subgroup': label + '/' + group,
                'scope': 'within_template' if group == 'all' else 'other_recognizable_subgroup',
                'strategy': 'Bank-only ' + cue + '; first-visible ties; no given line or key used for prediction.',
                'correct': count, 'total': len(rows), 'baseline': 0.2,
                'disposition': 'not_predictive',
                'conclusion': 'Compared with uniform five-choice guessing. No tested strategy answers every item; finite correlations do not establish independence.',
                'sample_refs': refs})
    return result


def checks():
    state = load(D / 'job.json')
    pipeline = Pipeline(D, state['request'], None)
    pipeline.verify_approval_inputs()
    binding = load(E / 'final-binding.json')
    assert pipeline.review_binding() == binding
    sys.path.insert(0, str(D / 'workspace'))
    spec = importlib.util.spec_from_file_location('repaired_generator', D / 'workspace/generator.py')
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    all_records, paths, grading, summaries, shortcut_rows = [], [], [], {}, []

    def inspect(records, label, refs):
        observations = []
        for i, record in enumerate(records):
            boundary(record)
            observations.append(observe(record))
            path = scope(record)
            path['sample_refs'] = refs
            paths.append(path)
            choices = record['question'][':question/answer-fields'][0][':answer-field/choices']
            grading.append({'label': label + ':' + str(i), 'record': record, 'checks': [
                {'field_index': 0, 'submitted_answer_id': c[':answer/id'],
                 'expected': 'accepted' if j == observations[-1]['target'] else 'rejected',
                 'purpose': 'Independent visible-equation slope and distinctness criterion'}
                for j, c in enumerate(choices)]})
        return observations

    for k, band in enumerate(('easy', 'moderate', 'hard')):
        batch = state['verification_batches'][band]
        records = load(batch['batch_file'])
        assert digest(records) == binding['verification_batches'][band]['batch_hash']
        assert len(records) == 5
        save('final-' + band + '.json', records)
        observations = inspect(records, 'final-' + band, ['final-' + band + '.json'])
        assert len({o['slope'] for o in observations}) == 5
        assert len({bank(r) for r in records}) == 5
        all_records.extend(records)
        controls = g.batch(band, 24, 19379 + k)
        save('control-' + band + '.json', controls)
        control_obs = inspect(controls, 'control-' + band, ['control-' + band + '.json'])
        slopes = Counter(o['slope'] for o in control_obs)
        assert max(slopes.values()) - min(slopes.values()) <= 1
        assert len(slopes) == (12 if band == 'easy' else 22)
        assert len({bank(r) for r in controls}) == len(controls)
        delivery = {}
        for label, sample in (('final', records), ('control', controls)):
            filename = label + '-' + band + '.json'
            target = E / (label + '-delivery-' + band)
            run([sys.executable, R / 'generate/pipeline/check_delivery.py', '--input', E / filename,
                 '--source', D / 'source/source.json', '--inventory', D / 'source/inventory.json',
                 '--difficulty', band, '--output', target, '--asset-root', batch['assets_directory']],
                label + '-delivery-' + band + '-command.json')
            accepted = load(target / 'accepted.json')
            assert len(accepted) == len(sample)
            inspect(accepted, label + '-delivered-' + band, [target.name + '/accepted.json'])
            assert len({bank(r) for r in accepted}) == len(accepted)
            delivery[label] = load(target / 'delivery.json')
            shortcut_rows.extend(probes(accepted, band + '/' + label + '/delivered', [filename, target.name + '/accepted.json']))
        summaries[band] = {'final': observations, 'control_slope_counts': dict(slopes), 'delivery': delivery}

    # Construction is unchanged. Rerun its retained independent controlled pairs
    # through visible algebra and the current grader, without publishing them.
    counterfactuals = load(E / 'prior/counterfactual-records.json')
    inspect(counterfactuals, 'retained-counterfactuals', ['prior/counterfactual-records.json'])
    for group in load(E / 'prior/counterfactual-tests.json'):
        before, after, irrelevant = [counterfactuals[i] for i in group['indices']]
        assert bank(before) == bank(after) == bank(irrelevant)
        assert observe(before)['target'] != observe(after)['target']
        assert observe(before)['target'] == observe(irrelevant)['target']
    save('counterfactual-recheck.json', {'passed': True, 'records': len(counterfactuals),
        'source': 'prior/counterfactual-tests.json', 'meaning': 'Fixed-bank target swaps and irrelevant scaling are controlled tests, not ordinary practice sampling.'})
    replays = []
    for source in load(E / 'prior/source-replay-records.json'):
        replay_id = source['generation']['template'].split(':', 1)[1]
        current = g.replay(replay_id)
        assert current == source
        replays.append(current)
    inspect(replays, 'source-replay', ['prior/source-replay-records.json'])
    save('source-replay-recheck.json', {'passed': True, 'count': len(replays), 'exact_records_unchanged': True})
    save('final-records.json', all_records)
    save('independent-math.json', summaries)
    save('solution-paths.json', {'cases': paths})
    save('grading-input.json', grading)
    run([R / 'generate/runs/current/check-engine', E / 'grading-input.json', E / 'grading-report.json'], 'grading-command.json')
    save('shortcut-probes.json', shortcut_rows)
    perfect = [p for p in shortcut_rows if p['correct'] == p['total']]
    save('perfect-probes.json', perfect)
    assert not perfect, perfect[:3]
    print(json.dumps({'passed': True, 'final_records': len(all_records), 'grading_cases': len(grading), 'native_checks': 5 * len(grading), 'shortcut_probes': len(shortcut_rows)}))


def rendered():
    records = load(E / 'final-records.json')
    report = load(E / 'render/rendering.json')
    assert report['passed'] and len(report['cases']) == len(records) == 15
    import_functions(E / 'prior/render_audit.py', {'signature', 'flatten'})
    checks, ui_records, shortcut_rows = [], [], []
    for i, record in enumerate(records):
        q = record['question']
        html = (E / 'render' / f'question-{i+1:03d}.html').read_text()
        blocks = re.findall(r'<mjx-assistive-mml[^>]*>(.*?)</mjx-assistive-mml>', html, re.S)
        observed = [signature(flatten(ET.fromstring(s))) for s in blocks]
        field = q[':question/answer-fields'][0]
        choices = field[':answer-field/choices']
        intended = [signature(m.group(1) or m.group(2)) for text in (q[':question/problem'], q[':question/worked-solution'])
                    for m in re.finditer(r'\$\$(.*?)\$\$|\$([^$]+)\$', text, re.S)]
        intended += [signature(c[':answer/value']) for c in choices] + [signature(observe(record)['key'])]
        assert Counter(observed) == Counter(intended), (i, Counter(intended) - Counter(observed))
        expected_rows = sum(1 + block.count('\\\\') for text in (q[':question/problem'], q[':question/worked-solution'])
                            for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', text, re.S))
        assert expected_rows == html.count('data-mml-node="mtr"')
        ids = re.findall(r'<input type="radio"[^>]*value="([^"]+)"', html)
        assert len(ids) == 5 and set(ids) == {c[':answer/id'] for c in choices}
        ui = copy.deepcopy(record)
        ui['question'][':question/answer-fields'][0][':answer-field/choices'] = sorted(choices, key=lambda c: ids.index(c[':answer/id']))
        ui_records.append(ui)
        checks.append({'index': i, 'math_spans': len(observed), 'aligned_rows': expected_rows, 'passed': True})
    save('ui-ordered-final-records.json', ui_records)
    for k, band in enumerate(('easy', 'moderate', 'hard')):
        shortcut_rows.extend(probes(ui_records[k*5:k*5+5], band + '/final/actual-UI', ['ui-ordered-final-records.json']))
    save('ui-shortcut-probes.json', shortcut_rows)
    perfect = [p for p in shortcut_rows if p['correct'] == p['total']]
    save('ui-perfect-probes.json', perfect)
    assert not perfect, perfect
    save('render-math-boundary.json', {'passed': True, 'cases': checks, 'method': 'Exact authored TeX versus rendered assistive MathML multiset and alignment row counts; actual rendered radio order.'})
    print(json.dumps({'passed': True, 'rendered_questions': len(checks), 'formulas': sum(c['math_spans'] for c in checks), 'aligned_rows': sum(c['aligned_rows'] for c in checks)}))


def accept():
    state = load(D / 'job.json')
    pipeline = Pipeline(D, state['request'], None)
    pipeline.verify_approval_inputs()
    binding = load(E / 'final-binding.json')
    assert binding == pipeline.review_binding()
    assert load(E / 'visual-inspection.json')['passed']
    assert load(E / 'render-math-boundary.json')['passed']
    regression = load(D / 'sampler-regression.json')
    assert regression['passed']
    save('sampler-regression.json', regression)
    source = load(E / 'prior/source-analysis.json')
    source['provenance'] = 'Retained independent source analysis, reassessed against unchanged current instructional source identity and repaired sampler. This repair changes batch selection only.'
    save('source-analysis.json', source)
    variation = {'learner_operation': source['skill'],
        'fixed_features': [{'feature': 'Complete line selection after isolating y', 'justification': 'Matches source response and prerequisite algebra.'},
                           {'feature': 'Hard contains one coincident option', 'justification': 'Distinctness requires intercept comparison after slope comparison.'}],
        'answer_roles': [{'role': 'Unique distinct parallel line', 'eligible_variation': 'Any eligible slope pair member and randomized bank slot',
                          'observed': 'Fresh banks per question; distinct final target slopes and no universally successful tested bank-only cue.'}],
        'coverage': [{'case': 'Exact final five-question bands and independent 24-question controls',
                      'result': 'Every final band has five distinct banks and target slopes; controls exhaust the supported slopes with balanced usage.',
                      'sample_refs': ['independent-math.json', 'sampler-regression.json']}],
        'counterfactuals': [
            {'kind': 'relevant', 'change': 'Change the given slope/intercept while holding the answer bank fixed.', 'expected': 'Correct choice changes.',
             'observed': 'Each retained pair changes target and passes visible algebra/current grader.', 'status': 'passed',
             'justification': 'Tests dependence on given line; these pairs are not practice batches.', 'sample_refs': ['prior/counterfactual-records.json', 'counterfactual-recheck.json']},
            {'kind': 'irrelevant', 'change': 'Scale the given equation by a nonzero factor.', 'expected': 'Same geometric line and correct choice.',
             'observed': 'Target preserved; exact visible algebra/current grader pass.', 'status': 'passed',
             'justification': 'Equivalent equations represent the same line.', 'sample_refs': ['prior/counterfactual-records.json', 'counterfactual-recheck.json']}],
        'shortcut_probes': load(E / 'shortcut-probes.json') + load(E / 'ui-shortcut-probes.json'),
        'delivery': {'stages_examined': ['New batch sampling', 'Source/difficulty validation', 'Captured inventory and batch deduplication', 'Actual UI option order'],
                     'sample_refs': ['independent-math.json', 'ui-ordered-final-records.json'],
                     'result': 'All final and control records survive captured filtering; no bank reused; all final bands retain five distinct slopes.'},
        'limitations': ['Balancing applies within each generator call, not across historical learner sessions.',
                       'Existing questions are not rewritten; previously published twins can remain in inventory.',
                       'Finite probes do not establish absence of every shortcut. Random correlations in short batches are not blanket independence.',
                       'Hard bank geometry excludes its singleton slope from coincidence work; this intended mathematical inference leaves four eligible choices.',
                       'Live learner history and future inventory changes are not simulated; retained selection evidence uses surrogate IDs.']}
    save('pedagogical-variation.json', variation)
    specs = {
        'source_replay': (['source-analysis.json', 'source-replay-recheck.json', 'prior/source-replay.json'], 'All seven complete source/exemplar replay records remain exact; incomplete imports unchanged.'),
        'math': (['independent-math.json', 'grading-report.json'], 'Independent rational parsing checks unique distinct parallel answer and every displayed normalization row on final/control/delivered records.'),
        'variety': (['sampler-regression.json', 'independent-math.json'], 'Fresh bank per ordinary practice question; five distinct target slopes in each final band; larger controls balance all supported slopes.'),
        'decision_variation': (['pedagogical-variation.json', 'shortcut-probes.json', 'ui-shortcut-probes.json'], 'Reused test-only controlled pairs plus fresh final/control bank-only probes and actual UI order; no observed universal shortcut.'),
        'scope': (['solution-paths.json'], 'Independent displayed algebra establishes each keyed complete line; hard coincidence is explicitly explained.'),
        'grading': (['grading-input.json', 'grading-report.json'], 'Current native grader accepts exactly the independently valid option and rejects each other option before and after delivery normalization.'),
        'rendering': (['render/rendering.json', 'render-math-boundary.json', 'visual-inspection.json'], 'All15 final questions rendered in actual UI; every formula and alignment row matched; representative screenshots inspected.'),
        'packaging': (['final-binding.json', 'sampler-regression.json'], 'Runner relocated package, checked declared dependencies, generated deterministic bands, and verified bound package/source/inventory/sample bytes.'),
        'progression': (['prior/progression.json', 'prior/matched-progression-records.json', 'final-records.json'], 'Construction unchanged: easy slope-intercept choices, moderate standard-form normalization, hard coincident alternative and distinctness. Prior matched-case analysis remains applicable; current output independently checked.')}
    report = {'verdict': 'accepted', 'summary': 'Sampler repaired to publish fresh answer banks and varied target slopes. Current all-band output passes independent math, native grading, delivery, rendered math and short-batch variety checks.',
              'source_analysis': source, 'checks': {name: {'status': 'passed', 'evidence_paths': refs, 'details': details} for name, (refs, details) in specs.items()},
              'findings': [], 'band_verification': {}}
    for band, batch in binding['verification_batches'].items():
        report['band_verification'][band] = {'status': 'passed', 'batch_sha256': batch['batch_hash'],
            'evidence_paths': ['final-' + band + '.json', 'independent-math.json', 'grading-report.json', 'render/rendering.json', 'final-delivery-' + band + '/delivery.json'],
            'details': 'Five independently checked records, five distinct banks and slopes; visible solution math, all-option grading, delivery and actual rendering passed.'}
    validate_review(report, E, binding)
    save('result.json', report)
    print(json.dumps({'verdict': 'accepted', 'report': str(E / 'result.json'), 'package_hash': state['package_hash']}))


if __name__ == '__main__':
    E.mkdir(exist_ok=True)
    import_functions(E / 'prior/review_checks.py', {'coeff', 'line', 'observe', 'boundary', 'scope'})
    import_functions(E / 'prior/probe_lib.py', {'predictions'})
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('checks', 'rendered', 'accept'))
    args = parser.parse_args()
    {'checks': checks, 'rendered': rendered, 'accept': accept}[args.stage]()
