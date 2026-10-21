"""Repair the labelled-line alignment in the reported question and its family."""
import copy
import importlib.util
import json
import shutil
from pathlib import Path
from read import DB, HERE, ROOT, save
from capture.scripts.database.client import QUESTION_PULL
from capture.scripts.database.edn import dumps, loads
from scripts.generator_packages import materialize_package
import subprocess

def repair(text):
    if ' &{}={}& ' not in text or 'l_{1}:\\quad &' not in text:
        return text
    return text.replace(r'\begin{alignedat}{2}', r'\begin{aligned}').replace(
        r'\end{alignedat}', r'\end{aligned}').replace(' &{}={}& ', ' = ')

if __name__ == '__main__':
    identity = json.loads((HERE / 'identity.json').read_text())
    out = HERE / 'formatting'
    out.mkdir(exist_ok=True)
    kp = 17592186073777
    rows = DB.query('[:find ?q :in $ ?kp :where [?kp :knowledge-point/questions ?q]]',
                    [kp], out, 'questions', identity['basis'])
    ids = sorted(row[0] for row in rows)
    groups = [['questions', QUESTION_PULL, ids]]
    (out / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    reader = ROOT / 'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'
    result = subprocess.run([str(reader), str(out), str(identity['basis'])], env=DB.environment,
                            capture_output=True, text=True, timeout=120)
    result.check_returncode()
    questions = loads((out / 'questions.edn').read_text())
    (out / 'questions.json').write_text(json.dumps(questions, indent=2, default=str) + '\n')
    changes, records = [], []
    for q in questions:
        updated = copy.deepcopy(q)
        for attr in (':question/problem', ':question/worked-solution'):
            if attr not in q: continue
            value = repair(q[attr])
            if value != q[attr]:
                changes.append({'entity': q[':db/id'], 'attribute': attr, 'before': q[attr], 'after': value})
                updated[attr] = value
        if q[':db/id'] == 17592186561248:
            records = [{'question': q}, {'question': updated}]
    (out / 'changes.json').write_text(json.dumps(changes, indent=2) + '\n')
    (out / 'render-records.json').write_text(json.dumps(records, indent=2, default=str) + '\n')
    registry = json.loads((HERE / 'registry.json').read_text())
    registration = next(row for row in registry if row[0] == kp)
    if not (out / 'original').exists(): materialize_package(registration[2], Path(DB.config.math_root), out / 'original')
    manifest = json.loads((out / 'original/generator-package.json').read_text())
    directory = out / 'package'
    for name in manifest['files']:
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out / 'original' / name, target)
    path = directory / 'generator.py'
    text = path.read_text()
    old = r'rows.append(f"l_{{{i}}}:\\quad & " + left.strip() + r" &{}={}& " + right.strip())'
    new = r'rows.append(f"l_{{{i}}}:\\quad & " + left.strip() + " = " + right.strip())'
    assert text.count(old) == 1
    text = text.replace(old, new).replace('VERSION = "line-intersection-count-3"', 'VERSION = "line-intersection-count-4"')
    text = text.replace(r'r"\begin{alignedat}{2}"', r'r"\begin{aligned}"').replace(r'r"\end{alignedat}"', r'r"\end{aligned}"')
    path.write_text(text)
    print(json.dumps({'questions': len(questions), 'formatting_changes': len(changes), 'registration': registration}))
