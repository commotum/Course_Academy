"""Validate current source replay and exact-domain checkbox practice; no DB writes."""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sympy as sp
import numpy as np
from PIL import Image

D = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('graph_generator', D.with_suffix('.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
X = sp.Symbol('x', real=True)

def check(condition, message):
    if not condition:
        raise AssertionError(message)

# Reuse the independently authored preimage and PNG readers without running the
# legacy validator's module-level fixture writes or replacing its frozen evidence.
tree = ast.parse((D/'validate.py').read_text())
helpers = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef)
                          and n.name in ('exp','independent','plot_math')], type_ignores=[])
exec(compile(helpers, str(D/'validate.py'), 'exec'), globals())

def normalize(q):
    q = json.loads(json.dumps(q, default=str))
    result = {k:q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    if ':question/difficulty' in q:
        result[':question/difficulty'] = m.enum(q[':question/difficulty'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f:f[':answer-field/key']):
        correct = f[':answer-field/correct']
        result[':question/answer-fields'].append({
            ':answer-field/id':f[':answer-field/id'], ':answer-field/key':f[':answer-field/key'],
            ':answer-field/type':m.enum(f[':answer-field/type']),
            ':answer-field/correct':[':answer/id',correct[':answer/id']] if isinstance(correct,dict) else correct,
            ':answer-field/choices':sorted([{':answer/id':a[':answer/id'],
                ':answer/type':m.enum(a[':answer/type']), ':answer/value':a[':answer/value']}
                for a in f[':answer-field/choices']],key=lambda a:a[':answer/value'])})
    return result

def native(r):
    r = copy.deepcopy(r)
    r['question'] = normalize(r['question'])
    checks = []
    for i,f in enumerate(r['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i, 'submitted_answer_id':a[':answer/id'],
                'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
                'purpose':'field-owned boolean choice on graph '+f[':answer-field/key']})
    return {'label':r['question'][':question/id'], 'record':r,'checks':checks}

def validate(r, plots=True):
    q,meta = r['question'],r['generation']
    check(r['knowledge_point']['db_id']==m.KP and r['knowledge_point']['id']==m.UUID,'requested KP')
    check(not meta['evidence_only'] and meta['eligible_for_learning'],'practice eligibility')
    level = q[':question/difficulty'].split('/')[-1]
    computed = sum(1<<i for i,g in enumerate(meta['graphs']) if independent(g))
    check(computed==meta['correct_mask'],'independent exact preimage answer')
    fields = q[':question/answer-fields']
    check([f[':answer-field/key'] for f in fields]==list(m.ROMANS),'four panel fields')
    identities = [q[':question/id']]
    for i,f in enumerate(fields):
        check(f[':answer-field/type']==':answer-field.type/checkbox','checkbox type')
        choices = f[':answer-field/choices']
        check(sorted(a[':answer/value'] for a in choices)==['false','true'],'complete boolean bank')
        expected = 'true' if computed>>i&1 else 'false'
        correct = next(a for a in choices if a[':answer/id']==f[':answer-field/correct'][1])
        check(correct[':answer/value']==expected,'checkbox key matches graph')
        identities += [f[':answer-field/id'],*[a[':answer/id'] for a in choices]]
    check(len(identities)==len(set(identities)),'field-owned UUIDs')
    for ident in identities:
        check(str(__import__('uuid').UUID(ident))==ident,'UUID format')
    check(':question/math-academy-id' not in q,'generated content has no captured identity')
    check('Select all that apply.' in q[':question/problem'],'subset response prompt')
    for line in q[':question/worked-solution'].splitlines():
        if line.startswith('- For graph'):
            labels = re.findall(r'\b(?:IV|III|II|I)\b',line.split(', any horizontal')[0].split(', some horizontal')[0])
            passing = 'at most once' in line
            expected = [m.ROMANS[i] for i in range(4) if bool(computed>>i&1)==passing]
            check(labels==expected,'worked solution target references')
    if plots:
        for path in meta['assets'].values():
            check(plot_math(path)==computed,'PNG geometry and endpoints agree with answer')
    return computed

def replay(r):
    meta = r['generation']
    level = r['question'][':question/difficulty'].split('/')[-1]
    return m.generate(level,seed=meta.get('seed',0),parameters=meta['parameters'],
                      profile=meta['legacy_sampling_profile'])

def main():
    records=[]
    source_masks={}
    for name,q in m.CURRENT_SOURCES.items():
        raw=m.generate('easy',profile='current:'+name)
        check(raw['question']==q,'complete current source replay')
        fields=normalize(q)[':question/answer-fields']
        check({f[':answer-field/key'] for f in fields}==set(m.ROMANS),'current source field layout')
        source_masks[name]=sum(1<<m.ROMANS.index(f[':answer-field/key']) for f in fields
            if next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']=='true')
        old=m.SOURCES[name][':question/answer-fields'][0]
        expected=m.mask(old[':answer-field/correct'][':answer/value']) if ':answer-field/correct' in old else {'q-36000':3,'q-36897':1}[name]
        check(source_masks[name]==expected,'current checkbox subset retains verified graph answer')
        records.append(raw)
    normal=[]
    for level in ('easy','moderate','hard'):
        for seed in (9,10):
            r=m.generate(level,seed)
            validate(r)
            check(normalize(replay(r)['question'])==normalize(r['question']),'deterministic parameter replay')
            normal.append(r)
    # Hold all graphs fixed, permute panel roles, update mask, and read the result.
    r=normal[-1];p=copy.deepcopy(r['generation']['parameters'])
    p['graphs']=p['graphs'][1:]+p['graphs'][:1]
    p['correct_mask']=(p['correct_mask']>>1)|((p['correct_mask']&1)<<3)
    profile=next(k for k,bank in m.BANKS.items() if p['correct_mask'] in [m.mask(v) for v in bank])
    changed=m.generate('hard',parameters=p,profile=profile)
    validate(changed)
    check(changed['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint'],'label permutation does not create another task')
    bad=copy.deepcopy(r)
    bad['question'][':question/answer-fields'][0][':answer-field/correct'][1]=bad['question'][':question/answer-fields'][0][':answer-field/choices'][0 if r['generation']['correct_mask']&1 else 1][':answer/id']
    try:validate(bad,plots=False)
    except AssertionError:pass
    else:raise AssertionError('stale checkbox key accepted')
    records += normal+[changed]
    inputs=D/'checkbox-engine-input.json';report=D/'checkbox-engine-report.json'
    inputs.write_text(json.dumps([native(r) for r in records],indent=2))
    subprocess.run([str(m.REPO/'generate/runs/current/check-engine'),str(inputs),str(report)],check=True)
    engine=json.loads(report.read_text());check(engine['documented_unresolved_checks']==0,'native grader')
    summary={'passed':True,'version':m.CHECKBOX_VERSION,'source_basis':2221,
        'current_source_complete_replays':10,'current_source_fields':40,'current_source_boolean_choices':80,
        'current_source_verified_subset_masks':source_masks,'normal_records':len(normal),
        'supported_levels':['easy','moderate','hard'],'hard_is_authored_extension':True,
        'label_permutation_deduplicated':True,'changed_target_and_stale_key_checks':True,
        'native_grading':engine,'legacy_evidence':'history/radio-v1/freeze.json',
        'dependencies':{'sympy':sp.__version__,'numpy':np.__version__},
        'exceptions':['Opaque captured graph equations cannot be recovered exactly; source replay is evidence only.',
                      'Two source questions remain unrated and excluded from available practice inventory.'],
        'hashes':{str(p.relative_to(m.REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
            (D.with_suffix('.py'),D/'render.py',D/'current-source.json',Path(__file__))}}
    (D/'checkbox-validation.json').write_text(json.dumps(summary,indent=2)+'\n')
    (D/'checkbox-review.json').write_text(json.dumps(normal+[changed],indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ('passed','current_source_complete_replays','normal_records','supported_levels')}))

if __name__=='__main__':main()
