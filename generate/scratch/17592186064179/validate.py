"""Validate frozen bank replay, rendered mathematics, solution steps and native grading."""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import uuid
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, default=str) + '\n')

def expr(text):
    return g.expression(text)

def parse(problem):
    return g.fingerprint_text(problem)

def primitive(e, variable):
    table = {sp.sin(variable): -sp.cos(variable), sp.cos(variable): sp.sin(variable),
             sp.sec(variable)*sp.tan(variable): sp.sec(variable),
             sp.csc(variable)*sp.cot(variable): -sp.csc(variable)}
    result = 0
    for term in sp.Add.make_args(sp.expand(e)):
        coefficient, function = term.as_coeff_Mul()
        assert function in table, ('unsupported integral term', function)
        result += coefficient * table[function]
    assert g.reduced(sp.diff(result, variable) - e) == 0
    return result

def evaluated(text, variable):
    def replace(m):
        return '(' + str(primitive(expr(m[1]), variable)) + ')'
    text = re.sub(r'\\int\s+(.*?)\\text\{d\}\s*(?:\\theta|[xy])', replace, text)
    return expr(text.strip().rstrip('.,'))

def bank_check(question):
    fields = question.get(':question/answer-fields', [])
    assert len(fields) == 1
    f = fields[0]
    assert f[':answer-field/key'] == 'selection'
    ftype = f[':answer-field/type']
    assert (ftype.get(':db/ident') if isinstance(ftype, dict) else ftype) == ':answer-field.type/radio'
    choices = f[':answer-field/choices']
    assert len(choices) == 5
    correct = f[':answer-field/correct']
    cid = str(correct[':answer/id']) if isinstance(correct, dict) else correct[1]
    assert sum(str(a[':answer/id']) == cid for a in choices) == 1
    problem = question[':question/problem']
    integrand = g.integrand(problem)
    variables = integrand.free_symbols
    assert len(variables) == 1
    variable = next(iter(variables))
    values = [expr(a[':answer/value']) for a in choices]
    valid = [g.reduced(sp.diff(e, variable) - integrand) == 0 for e in values]
    assert sum(valid) == 1, ('ambiguous/incorrect source bank', valid)
    assert choices[valid.index(True)][':answer/id'] == cid or str(choices[valid.index(True)][':answer/id']) == cid
    assert not any(g.reduced(e-v) == 0 for i,e in enumerate(values) for v in values[:i])
    return variable, integrand

def solution_check(question):
    variable, integrand = bank_check(question)
    text = question[':question/worked-solution']
    displays = re.findall(r'\$\$\n(.*?)\n\$\$', text, re.S)
    assert len(displays) == 2
    count = 0
    for i, display in enumerate(displays):
        display = re.sub(r'\\(?:begin|end)\{aligned\}', '', display)
        previous = None
        for line in display.split(r'\\'):
            left, right = line.replace('&', '').split('=')
            if left.strip():
                lhs = evaluated(left, variable)
                previous = lhs
            else:
                assert previous is not None
                lhs = previous
            rhs = evaluated(right, variable)
            delta = g.reduced(lhs-rhs)
            assert not delta.free_symbols - {sp.Symbol('C', real=True)}, ('bad solution step', line, delta)
            if i == 1:
                assert g.reduced(sp.diff(rhs, variable)-integrand) == 0, line
            previous = rhs
            count += 1
    return count

def independent(record):
    q, m = record['question'], record['generation']
    assert record['knowledge_point']['db_id'] == g.KP_ID and record['knowledge_point']['id'] == g.KP_UUID
    level = q[':question/difficulty'].split('/')[-1]
    assert level in g.SUPPORTED_LEVELS
    assert record == g.generate(level, m['seed'], m['template'], m['parameters'], m['bank_profile'])
    assert parse(q[':question/problem']) == m['parameter_fingerprint']
    steps = solution_check(q)
    f = q[':question/answer-fields'][0]
    ids = [q[':question/id'], f[':answer-field/id']] + [a[':answer/id'] for a in f[':answer-field/choices']]
    assert len(set(ids)) == len(ids)
    for x in ids:
        uuid.UUID(x)
    for text in (q[':question/problem'], q[':question/worked-solution']):
        assert text.count('$') % 2 == 0 and text.count('{') == text.count('}')
        assert '{a}' not in text and '{b}' not in text and '{sum}' not in text
    assert '{{' not in q[':question/problem']
    return steps

def checks(record):
    f = record['question'][':question/answer-fields'][0]
    return [{'field_index': 0, 'submitted_answer_id': a[':answer/id'],
             'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected',
             'purpose': 'Select every owned option through actual learner radio grading'} for a in f[':answer-field/choices']]

def main():
    source = json.loads((HERE / 'source.json').read_text())
    cases, records, excluded, reviews = [], [], [], []
    all_banks, all_values, matched, steps = 0, 0, 0, 0
    for q in source['record'][':knowledge-point/questions']:
        mid = q[':question/math-academy-id']
        if mid not in g.TEMPLATES:
            excluded.append({'source': mid, 'reason': 'Incomplete or unrated source; missing correct designation, worked solution, or answer fields. Preserved unchanged.'})
            continue
        t = g.TEMPLATES[mid]
        p = t['parameters']
        assert g.render(t['problem'], p) == q[':question/problem']
        assert g.render(t['solution'], p) == q[':question/worked-solution']
        original = q[':question/answer-fields'][0]
        values = [g.render(a,p) for a in t['choices']]
        assert sorted(values) == sorted(a[':answer/value'] for a in original[':answer-field/choices'])
        assert values[t['correct_index']] == original[':answer-field/correct'][':answer/value']
        all_banks += 1; all_values += len(values)
        case = {'source': mid, 'difficulty': t['difficulty'], 'template': mid, 'bank_profile': mid,
                'parameters': p, 'exact_prompt': True, 'exact_solution': True, 'complete_bank_match': True,
                'matched_values': len(values), 'total_values': 5, 'missing_options': [], 'extra_options': []}
        if mid not in g.SUPPORTED_PROFILES:
            # Independent proof of the duplicated source answer, never silently repair its bank.
            assert g.reduced(expr(values[0])-expr(values[t['correct_index']])) == 0
            case['excluded_mathematical_error'] = '3 sec(x) cot(x) = 3 csc(x); two correct choices. Entire profile excluded.'
            excluded.append({'source': mid, 'reason': case['excluded_mathematical_error']})
        else:
            r = g.generate(t['difficulty'], template=mid, parameters=p)
            steps += independent(r)
            records.append(r); matched += 1
            reviews.append('## ' + mid + ': exact source replay\n\n' + g.markdown(r))
        cases.append(case)
    # Exercise the complete finite parameter domains for every supported profile.
    import itertools
    for mid in g.SUPPORTED_PROFILES:
        t = g.TEMPLATES[mid]
        bounds = range(2,10) if mid in ('q-71656','q-71659') else range(1,10)
        keys = list(t['parameters'])
        for values in itertools.product(bounds, repeat=len(keys)):
            p = dict(zip(keys, values))
            r = g.generate(t['difficulty'], 971, mid, p)
            steps += independent(r)
            assert r['question'] == g.generate(t['difficulty'], 11, mid, p)['question']
            records.append(r)
    negatives = 0
    for level, mid, p in [('hard',None,None), ('easy','q-113920',{'a':3}), ('easy','q-71656',{'a':1}), ('moderate','q-113926',{'a':0,'b':2}), ('moderate','q-113930',{'a':10,'b':1})]:
        try:
            g.generate(level, template=mid, parameters=p)
        except ValueError:
            negatives += 1
        else:
            raise AssertionError('unsupported parameters accepted')
    for which in ('answer','solution'):
        bad = copy.deepcopy(records[0])
        if which == 'answer':
            f = bad['question'][':question/answer-fields'][0]
            a = next(a for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1])
            a[':answer/value'] = '0'
        else:
            bad['question'][':question/worked-solution'] = bad['question'][':question/worked-solution'].replace('=3csc', '=4csc')
            # First supported replay is moderate; force a bad final antiderivative.
            bad['question'][':question/worked-solution'] = bad['question'][':question/worked-solution'].replace('=-4cos', '=-9cos')
        try:
            solution_check(bad['question'])
        except (AssertionError, ValueError):
            negatives += 1
        else:
            raise AssertionError('corruption accepted')
    sizes = {}
    for level in g.SUPPORTED_LEVELS:
        rows = g.batch(level,1000,781)
        fps = [r['generation']['parameter_fingerprint'] for r in rows]
        assert len(fps) == len(set(fps))
        sizes[level] = len(rows)
        reviews.append('## ' + level + ' variant\n\n' + g.markdown(rows[0]))
    save('source-cases.json',cases); save('excluded-source.json',excluded)
    save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)])
    binary = ROOT / 'generate/runs/current/check-engine'
    result = subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True,check=True)
    (HERE/'engine.log').write_text(result.stdout+result.stderr)
    engine = json.loads((HERE/'engine-report.json').read_text())
    assert engine['documented_unresolved_checks'] == 0
    (HERE/'review.md').write_text('\n\n---\n\n'.join(reviews)+'\n')
    save('validation.json',{'status':'pass','source_basis':source['basis'],'lineage':source['lineage'],
        'supported_levels':list(g.SUPPORTED_LEVELS),'source_coverage':{'complete_source_banks':all_banks,'exact_banks_replayed':all_banks,
        'matched_values':all_values,'total_values':all_values,'supported_banks_matched':matched,'supported_bank_total':6,
        'missing_options':[],'extra_options':[],'exclusions':excluded},
        'fidelity':'Exact original prompts, fixed solutions, field layout, correct designation and complete banks. Ambiguous q-113920 is explicitly excluded; q-2038 wrong-variable distractor preserved for singleton replay only.',
        'mathematics':{'records_checked':len(records),'rendered_solution_steps':steps,'negative_controls':negatives,'finite_distinct_parameter_tasks':sizes},
        'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},
        'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',HERE/'templates.json',binary)}})
    print(result.stdout)

if __name__ == '__main__':
    main()
