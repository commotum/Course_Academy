"""Current-source replay, displayed mathematics and actual application grading."""
import collections
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('legacy_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
LEVELS = ('easy', 'moderate', 'hard')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def plain_matrices(s):
    return re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', lambda m:r'[\begin{aligned}'+m[1]+r'\end{aligned}]', s, flags=re.S)

def plain_prompt(s):
    s = s.replace('Select all that apply.\n\n', '')
    return re.sub(r'- \*\*(I|II|III)\.\*\* ', lambda m:m[1]+'. ', s)

def fingerprint(q):
    m = v.system(q[':question/problem']) if '\\begin{aligned}' in q[':question/problem'] else v.matrices(plain_matrices(q[':question/worked-solution']))[0]
    rows = []
    for row in m.tolist():
        pivot = next((x for x in row if x != 0), 1)
        rows.append([str(x/pivot) for x in row])
    return g.digest({'variables':list('xyz'[:m.cols-1]), 'normalized_equations':sorted(rows)})

def native_checks(rec):
    q = rec['question']
    m = v.system(q[':question/problem'])
    kind = v.independent_class(m)
    categories = g.statements(plain_prompt(q[':question/problem']))
    checks = []
    for i, f in enumerate(q[':question/answer-fields']):
        if f[':answer-field/type'].endswith('/checkbox'):
            expected = 'true' if categories[g.ROMAN.index(f[':answer-field/key'])] == kind else 'false'
        else:
            expected = g.ROMAN[categories.index(kind)]+' only'
        for a in f[':answer-field/choices']:
            correct = a[':answer/value'] == expected
            assert correct == (a[':answer/id'] == f[':answer-field/correct'][1])
            checks.append({'field_index':i, 'submitted_answer_id':a[':answer/id'], 'expected':'accepted' if correct else 'rejected', 'purpose':'Independently classify displayed system and grade every owned option'})
    return checks

def validate(rec, replay=True):
    q = rec['question']
    assert rec['knowledge_point']['db_id'] == g.KP_ID
    assert fingerprint(q) == rec['generation']['mathematical_fingerprint']
    native_checks(rec)
    fields = q[':question/answer-fields']
    layout = rec['generation']['response_layout']
    if layout == 'checkbox':
        assert [f[':answer-field/key'] for f in fields] == g.ROMAN
        for f in fields:
            assert f[':answer-field/type'] == ':answer-field.type/checkbox'
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices']) == ['false', 'true']
    else:
        assert len(fields) == 1 and fields[0][':answer-field/type'] == ':answer-field.type/radio'
    ids = [q[':question/id']]+[f[':answer-field/id'] for f in fields]+[a[':answer/id'] for f in fields for a in f[':answer-field/choices']]
    assert len(ids) == len(set(ids))
    for x in ids: uuid.UUID(x)
    # Reuse the existing independent stage/substitution validator on an adapter
    # of the rendered response. Current field truth is checked independently above.
    adapted = copy.deepcopy(rec)
    aq = adapted['question']
    aq[':question/problem'] = plain_prompt(q[':question/problem'])
    aq[':question/worked-solution'] = plain_matrices(q[':question/worked-solution'])
    m = v.system(q[':question/problem'])
    answer = g.correct_for(aq[':question/problem'], m)
    values = ['I only', 'II only', 'III only', 'None', 'I and II only']
    aq[':question/answer-fields'] = [{':answer-field/type':':answer-field.type/radio', ':answer-field/correct':[':answer/id', answer], ':answer-field/choices':[{':answer/id':x, ':answer/value':x} for x in values]}]
    v.validate_record(adapted)
    if replay:
        meta = rec['generation']
        again = g.generate(q[':question/difficulty'].split('/')[-1], meta['seed'], template=meta['template'], parameters=meta['parameters'], profile=meta['bank_profile'])
        def ordered(record):
            record=copy.deepcopy(record)
            for f in record['question'][':question/answer-fields']:
                f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
            return record
        assert ordered(again) == ordered(rec), 'Stored output differs from deterministic current generator'
    return m

def compare_source(source, rec):
    sf = sorted(source[':question/answer-fields'], key=lambda f:f[':answer-field/key'])
    gf = sorted(rec['question'][':question/answer-fields'], key=lambda f:f[':answer-field/key'])
    assert len(sf) == len(gf)
    for a,b in zip(sf,gf):
        assert a[':answer-field/key'] == b[':answer-field/key']
        assert a[':answer-field/type'][':db/ident'] == b[':answer-field/type']
        assert sorted(x[':answer/value'] for x in a[':answer-field/choices']) == sorted(x[':answer/value'] for x in b[':answer-field/choices'])
        actual = next(x[':answer/value'] for x in b[':answer-field/choices'] if x[':answer/id'] == b[':answer-field/correct'][1])
        assert actual == a[':answer-field/correct'][':answer/value']
    # All current source mathematics/layout is retained, apart from recorded
    # TeX normalization and the q-32242 unstated first-row negation repair.
    clean = lambda s: re.sub(r'\s+', '', v.normalize(plain_matrices(s)))
    assert clean(plain_prompt(source[':question/problem'])) == clean(plain_prompt(rec['question'][':question/problem']))
    repaired = source[':question/math-academy-id'] == 'q-32242'
    if not repaired:
        assert clean(source[':question/worked-solution']) == clean(rec['question'][':question/worked-solution'])
    return {'source':source[':question/math-academy-id'], 'fields':len(sf), 'options':sum(len(f[':answer-field/choices']) for f in sf), 'banks_matched':len(sf), 'solution_repair':repaired}

def main():
    source = json.loads((HERE/'source-current.json').read_text())
    native, coverage, reviews = [], [], []
    for q in source['record'][':knowledge-point/questions']:
        name = q[':question/math-academy-id']
        n = v.system(q[':question/problem']).cols-1
        rec = g.generate('moderate', template=name, parameters={'scales':[1]*n,'translations':[0]*n})
        validate(rec)
        coverage.append(compare_source(q, rec))
        native.append(rec)
        variant = g.generate('moderate', 731+len(reviews), template=name)
        validate(variant); reviews.append(variant)
    stress = collections.Counter()
    kinds = collections.defaultdict(set)
    unique = collections.defaultdict(set)
    for level in LEVELS:
        for seed in range(120):
            rec = g.generate(level, seed)
            validate(rec)
            stress[level] += 1
            kinds[level].add(rec['generation']['classification'])
            unique[level].add(fingerprint(rec['question']))
            if seed < 6: reviews.append(rec)
        assert kinds[level] == set(g.WORDS)
    for name in g.TEMPLATES:
        for profile in g.BANKS:
            validate(g.generate('moderate', 981, template=name, profile=profile))
    # Hold each other coordinate slot fixed, change only one scale/translation.
    slots = []
    for name in g.TEMPLATES:
        n = g.parse_matrix(g.TEMPLATES[name]['math_components'][1]).cols-1
        base = {'scales':[1]*n,'translations':[0]*n}
        for slot in base:
            for i in range(n):
                for value in ([-2,-1,1,2] if slot == 'scales' else [-2,-1,0,1,2]):
                    p = copy.deepcopy(base);p[slot][i] = value
                    validate(g.generate('moderate', template=name, parameters=p))
                slots.append({'template':name,'slot':slot,'coordinate':i,'all_allowed_values_checked':True})
    # Actual native grading includes every source field, every current option,
    # every layout and the easy/hard examples; no learner state is touched.
    records = native+reviews
    fixtures = [{'label':str(i), 'record':r, 'checks':native_checks(r)} for i,r in enumerate(records)]
    (HERE/'reference/current-native-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
    subprocess.run([str(HERE/'reference/check-engine'), str(HERE/'reference/current-native-input.json'), str(HERE/'reference/current-native-report.json')],check=True)
    (HERE/'reference/current-replays.json').write_text(json.dumps(native,indent=2)+'\n')
    (HERE/'reference/current-review.json').write_text(json.dumps(reviews,indent=2)+'\n')
    report = {'passed':True, 'source_basis':source['basis'], 'lineage':source['lineage'], 'source_replays':coverage, 'banks_matched':sum(c['fields'] for c in coverage), 'options_matched':sum(c['options'] for c in coverage), 'stress_records':dict(stress), 'distinct_tasks':{l:len(x) for l,x in unique.items()}, 'classification_coverage':{l:sorted(x) for l,x in kinds.items()}, 'slot_checks':slots, 'plots':'none', 'native_report':'reference/current-native-report.json', 'unresolved_findings':[], 'hashes':{str(p.relative_to(ROOT)):sha(p) for p in (HERE.with_suffix('.py'), HERE/'templates.json', HERE/'current-layouts.json', HERE/'validate_current.py', HERE/'source-current.json', HERE/'reference/check-engine')}}
    (HERE/'validation-current.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['passed','banks_matched','options_matched','stress_records','distinct_tasks']}),flush=True)

if __name__ == '__main__': main()
