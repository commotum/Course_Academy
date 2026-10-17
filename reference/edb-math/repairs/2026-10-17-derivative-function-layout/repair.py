"""Repair presentation only, with native preview and exact historical readback."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))
from inspect_questions import QUESTION_PULL
from scripts.generator_publish import Publisher
from scripts.question_capture.math_format import _legacy_commands
from capture.scripts.database.edn import dumps, loads, kw

HERE = Path(__file__).resolve().parent
SOURCE = ':agent/gpt-6.1-sol-high'
PARENTS = [17592186235313, 17592186514356, 17592186235296]
EXAMPLE = 17592186096417
DB = Publisher.from_environment(source=SOURCE).client
NATIVE = ROOT / 'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'
PARENT_PULL = '[* {[:multistep/steps :limit nil] [* {:step/content [:db/id :question/id]}]}]'
ITEM_PULL = '[* {[:task-item/responses :limit nil] [*]} {[:learner-task/_items :limit nil] [*]}]'

def save(path, value): path.write_text(json.dumps(value, indent=2, default=str) + '\n')
def canonical(value):
    if isinstance(value, dict): return {str(k): canonical(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)): return sorted((canonical(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    return value if isinstance(value, (int, float, str, bool)) or value is None else str(value)

def prepare(directory):
    identity = DB.status(); basis = identity['basis']
    def read(name, query, inputs): return DB.query(query, inputs, directory / 'evidence', name, basis)
    parents = read('parents', '[:find (pull ?m ' + PARENT_PULL + ') :in $ [?m ...] :where [?m :multistep/id _]]', [PARENTS])
    ids = sorted({EXAMPLE} | {step[':step/content'][':db/id'] for [m] in parents for step in m[':multistep/steps']})
    queries = {
        'questions': ('[:find (pull ?q ' + QUESTION_PULL + ') :in $ [?q ...] :where [?q :question/id _]]', [ids]),
        'items': ('[:find (pull ?i ' + ITEM_PULL + ') :in $ [?q ...] :where [?i :task-item/content ?q]]', [ids]),
        'source': ('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]', [kw(SOURCE)]),
        'attributes': ('[:find ?a ?ident :where [?a :db/ident ?ident] [?a :db/valueType _]]', []),
    }
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {name: pool.submit(read, name, *args) for name, args in queries.items()}
        data = {name: future.result() for name, future in futures.items()}
    assert len(data['source']) == 1 and len(parents) == 3 and len(data['questions']) == len(ids)
    changes = []
    def change(e, attr, new):
        old = e[attr]
        if old != new:
            previous = next((c for c in changes if c['entity'] == e[':db/id'] and c['attribute'] == attr), None)
            if previous: previous['after'] = new
            else: changes.append({'entity': e[':db/id'], 'attribute': attr, 'before': old, 'after': new})
    for [q] in data['questions']:
        old = q[':question/problem']
        # These captured prompts contain browser-layout whitespace, not authored code.
        if re.search(r'(?m)^[ \t]{4,}\{\{field-', old):
            assert '```' not in old and '`' not in old
            new = '\n'.join(line.strip() for line in old.splitlines())
            new = re.sub(r'\n{3,}', '\n\n', new).strip()
            # Put the response beside its equation and keep suffixes with the field.
            new = re.sub(r'\s*(\{\{field-\d+\}\})\s*', r'\1', new)
            new = re.sub(r'(?<=[A-Za-z])(?=\{\{field-)', ' ', new)
            new = re.sub(r'(\}\})(?=[A-Za-z])', r'\1 ', new)
            assert re.sub(r'\s+', '', new) == re.sub(r'\s+', '', old)
            change(q, ':question/problem', new)
        if q[':db/id'] == EXAMPLE:
            old_solution = q[':question/worked-solution']
            if '\\eqalign{' in old_solution: assert old_solution.count('\\\n') == 3
            change(q, ':question/worked-solution', _legacy_commands(old_solution))
        if q[':db/id'] == 17592186235481 and '| --- |' in old:
            # The imported HTML fraction became a Markdown table with the
            # denominator under the equation label. Factor the same numerator
            # so its existing answer field can sit beside a complete fraction.
            assert q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'] == r'\operatorname{cos}(x)-\operatorname{sin}(x)'
            change(q, ':question/problem', r'Calculate $\frac{\text{d}}{\text{d}x}(\frac{f}{h}).$' + '\n\n' + r'$\frac{\text{d}}{\text{d}x}(\frac{f}{h})=\frac{e^x}{8\sin^2(x)}\bigl(${{field-1}}$\bigr)$')
    for [parent] in parents:
        old = parent[':multistep/context']
        if r'\begin{aligned}' in old: continue
        intro, math, tail = old.split('$$')
        assert not tail.strip()
        functions = math.strip().split(r',\,')
        assert len(functions) == 3
        new = intro.strip() + '\n\n$$\n\\begin{aligned}\n' + ' \\\\\n'.join(f.replace('=', '&=', 1) for f in functions) + '\n\\end{aligned}\n$$'
        change(parent, ':multistep/context', new)
    forms = [[kw('db/cas'), c['entity'], kw(c['attribute']), c['before'], c['after']] for c in changes]
    forms += [[kw('db/ensure'), e, kw('question/validate')] for e in sorted({c['entity'] for c in changes if c['attribute'].startswith(':question/')})]
    (directory / 'transaction.edn').write_text(dumps(forms) + '\n')
    groups = [['questions', QUESTION_PULL, ids], ['parents', PARENT_PULL, PARENTS], ['items', ITEM_PULL, sorted({i[':db/id'] for [i] in data['items']})]]
    (directory / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    (directory / 'snapshot.edn').write_text(dumps({**identity, **data, 'parents': parents}) + '\n')
    save(directory / 'snapshot.json', {**identity, **data, 'parents': parents})
    sha = hashlib.sha256((directory / 'transaction.edn').read_bytes()).hexdigest()
    plan = {**identity, 'source': SOURCE, 'source_eid': data['source'][0][0], 'attributes': dict(data['attributes']), 'changes': changes, 'questions_audited': len(ids), 'items_preserved': len(data['items']), 'sha256': sha, 'request_key': f'derivative-layout-b{basis}-{sha}', 'endpoint': DB.config.endpoint, 'transaction_file': str(directory / 'transaction.edn')}
    save(directory / 'plan.json', plan)
    return json.loads((directory / 'plan.json').read_text())

def verify_report(report, plan, committed):
    assert report[':edb/committed'] is committed and report[':edb/db-before-t'] == plan['basis']
    expected = {(c['entity'], c['attribute'], c[k], added) for c in plan['changes'] for k, added in [('before', False), ('after', True)]}
    actual = set()
    for e, a, v, tx, source, added in report[':edb/tx-data']:
        assert source == plan['source_eid']
        attr = str(plan['attributes'][str(a)])
        if attr != ':db/txInstant': actual.add((e, attr, v, added))
    assert actual == expected

def execute(directory, commit):
    directory.mkdir(exist_ok=True)
    intent = directory / 'commit-intent.json'
    if not (directory / 'preview-verification.json').exists():
        assert not intent.exists()
        plan = prepare(directory)
        run = subprocess.run([str(NATIVE), str(directory), SOURCE, str(plan['basis'])], env=DB.environment, capture_output=True, text=True, timeout=150)
        (directory / 'preview.stderr').write_text(run.stderr); run.check_returncode()
        (directory / 'preview.edn').write_text(run.stdout); verify_report(loads(run.stdout), plan, False)
        for name, pattern, ids in loads((directory / 'native-pulls.edn').read_text()):
            before = loads((directory / f'preview-{name}-before.edn').read_text())
            after = loads((directory / f'preview-{name}-after.edn').read_text())
            expected = copy.deepcopy(before)
            for e in expected:
                for c in plan['changes']:
                    if e[':db/id'] == c['entity']: e[c['attribute']] = c['after']
            assert canonical(expected) == canonical(after), name
        save(directory / 'preview-verification.json', {'passed': True, 'only_planned_presentation_changes': True, 'answers_difficulty_memberships_and_learner_items_preserved': True})
    plan = json.loads((intent if intent.exists() else directory / 'plan.json').read_text())
    if not commit:
        print(json.dumps({'prepared': True, 'basis': plan['basis'], 'changes': len(plan['changes']), 'questions_audited': plan['questions_audited']})); return
    assert hashlib.sha256((directory / 'transaction.edn').read_bytes()).hexdigest() == plan['sha256']
    assert DB.status()['lineage'] == plan['lineage']
    save(intent, plan)
    receipt = directory / 'receipt.edn'
    if not receipt.exists():
        receipt.write_text(DB.command('transact', '--source', SOURCE, '--file', plan['transaction_file'], '--basis', plan['basis'], '--endpoint', plan['endpoint'], '--request-key', plan['request_key'], '--timeout-ms', '120000', timeout=150))
    report = loads(receipt.read_text()); verify_report(report, plan, True)
    after_basis = report[':edb/db-after-t']
    def verify_group(group):
        name, pattern, ids = group
        for basis, stage in [(plan['basis'], 'before'), (after_basis, 'after')]:
            rows = DB.query('[:find (pull ?e ' + pattern + ') :in $ [?e ...] :where [?e _ _]]', [ids], directory / 'readback', name + '-' + stage, basis) if ids else []
            assert canonical([e for [e] in rows]) == canonical(loads((directory / f'preview-{name}-{stage}.edn').read_text())), name
    with ThreadPoolExecutor(max_workers=3) as pool: list(pool.map(verify_group, loads((directory / 'native-pulls.edn').read_text())))
    result = {'committed': True, 'basis_before': plan['basis'], 'basis_after': after_basis, 'questions_audited': plan['questions_audited'], 'prompt_fixes': [c['entity'] for c in plan['changes'] if c['attribute'] == ':question/problem'], 'solution_fixes': [c['entity'] for c in plan['changes'] if c['attribute'] == ':question/worked-solution'], 'context_fixes': [c['entity'] for c in plan['changes'] if c['attribute'] == ':multistep/context'], 'learner_items_preserved': plan['items_preserved'], 'only_presentation_changed': True, 'exact_committed_and_historical_readback': True, 'request_key': plan['request_key']}
    save(directory / 'verification.json', result); save(HERE / 'content-verification.json', result); print(json.dumps(result))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--attempt', required=True); parser.add_argument('--commit', action='store_true')
    args = parser.parse_args(); execute(HERE / args.attempt, args.commit)
