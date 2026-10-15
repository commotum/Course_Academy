#!/usr/bin/env python3
"""Independent printed-math, source-fidelity and actual native-grading checks.

This parser reads displayed TeX, including vector/reversed-endpoint objects and
every solution equality. It never takes the magnitude, answer or solution from
generation metadata. Exhaustive finite parameter domains are checked for both
layouts and both authored banks. Source keys absent in raw evidence remain absent.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import copy
import sys
from functools import lru_cache
from pathlib import Path

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCRIPT = HERE.with_suffix('.py')
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('unit_vectors_draft', SCRIPT)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
V = sp.Symbol('V', real=True)


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def group(text, i):
    assert text[i] == '{', (text, i)
    depth, start = 1, i + 1
    i += 1
    while depth:
        assert i < len(text), text
        depth += (text[i] == '{') - (text[i] == '}')
        i += 1
    return text[start:i - 1], i


@lru_cache(maxsize=None)
def scalar(text):
    """Translate the small actually emitted exact-number grammar independently."""
    text = text.replace(r'\,', '').replace(r'\left', '').replace(r'\right', '')
    out, i = '', 0
    while i < len(text):
        command = next((c for c in (r'\dfrac', r'\frac', r'\sqrt') if text.startswith(c, i)), None)
        if command:
            i += len(command)
            a, i = group(text, i)
            aa = str(scalar(a))
            if command == r'\sqrt':
                out += '*sqrt(' + aa + ')' if out and out[-1].isdigit() else 'sqrt(' + aa + ')'
            else:
                b, i = group(text, i)
                out += '((' + aa + ')/(' + str(scalar(b)) + '))'
        else:
            out += text[i]
            i += 1
    assert '\\' not in out, out
    out = out.replace('{', '(').replace('}', ')').replace('^', '**')
    return parse_expr(out, local_dict={'V': V, 'sqrt': sp.sqrt},
                      transformations=standard_transformations + (implicit_multiplication_application,))


def context(record):
    prompt = record['question'][':question/problem']
    match = re.fullmatch(r'The vector \$(.*?)\$ has magnitude \$(.*?)\$\. (.*)', prompt)
    assert match, prompt
    vector, mtext, remainder = match.groups()
    m = scalar(mtext)
    assert m > 1 and m.is_real
    assert remainder in (f'Find a unit vector that is parallel to ${vector}$.',
                         f'Which of the following is a unit vector that is parallel to ${vector}$?')
    if '^(→)' in vector:
        label = vector.split('^')[0]
        reverse = label[::-1] + '^(→)'
    elif 'overrightarrow' in vector:
        label = re.fullmatch(r'\\overrightarrow\{([A-Z]{2})\}', vector)[1]
        reverse = r'\overrightarrow{' + label[::-1] + '}'
    else:
        reverse = None
    return vector, reverse, m


@lru_cache(maxsize=None)
def expression(text, vector, reverse, m):
    # Norm replacement happens before replacing its mathematical argument.
    text = text.replace(r'\mid \,' + vector + r'\, \mid', sp.sstr(m))
    if reverse:
        text = text.replace(reverse, '(-V)')
    if len(vector) == 1:
        # Raw named vectors occur only as a complete final vector component;
        # replacing the letter globally would corrupt the command \\frac.
        if text.endswith(vector):
            text = text[:-1] + 'V'
    else:
        text = text.replace(vector, 'V')
    return sp.simplify(scalar(text))


def formatted(text, raw=False):
    assert text.count('$') % 2 == 0
    depth = 0
    for c in text:
        depth += (c == '{') - (c == '}')
        assert depth >= 0
    assert depth == 0
    assert not any(token in text for token in ('+-', '--', 'NaN', 'nan', 'zoo', 'undefined'))
    # Decoded text: adjacent backslashes are NOT inferred from serialized output.
    assert '\\\\' not in text
    if not raw:
        assert '^(→)' not in text


@lru_cache(maxsize=None)
def expected_bank_signatures(m, directed, raw):
    expected_banks = ([[m*V, 1/m, V/(2*m), V/(4*m), V/m]] if not directed else
                      [[V, -m*V, -V, V/m, m*V]]) if raw else [
                          [m*V, 1/m, V/m**2, V, V/m],
                          [V, -V, m*V, -m*V, V/m]]
    return tuple(tuple(sorted(sp.srepr(sp.simplify(value)) for value in bank))
                 for bank in expected_banks)


def verify(record):
    assert record['knowledge_point'] == {'db_id': g.KP_ID, 'id': g.KP_UUID, 'title': g.TITLE}
    q, generation = record['question'], record['generation']
    vector, reverse, m = context(record)
    raw = generation['evidence_only']
    f, = q[':question/answer-fields']
    assert f[':answer-field/type'] == ':answer-field.type/radio'
    assert f[':answer-field/key'] == 'selection'
    assert len(f[':answer-field/choices']) == 5
    ids = [a[':answer/id'] for a in f[':answer-field/choices']]
    assert len(set(ids)) == 5
    formatted(q[':question/problem'], raw)
    values = []
    for a in f[':answer-field/choices']:
        assert a[':answer/type'] == ':answer.type/math'
        assert '$' not in a[':answer/value']
        formatted(a[':answer/value'], raw)
        value = expression(a[':answer/value'], vector, reverse, m)
        assert not value.has(sp.zoo, sp.oo, sp.nan)
        assert all(sp.simplify(value - other) != 0 for other in values)
        values.append(value)
    # Both orientations meet the actual source criterion "unit and parallel".
    eligible = [i for i, value in enumerate(values)
                if sp.simplify(value - V / m) == 0 or sp.simplify(value + V / m) == 0]
    assert len(eligible) == 1, (record, eligible)
    # Independent complete-bank specifications read only the actual prompt.
    # Correctness of one key cannot excuse arbitrary or stale wrong options.
    assert tuple(sorted(sp.srepr(value) for value in values)) in expected_bank_signatures(m,reverse is not None,raw), values
    if raw:
        assert generation['eligible_for_learning'] is False
        assert ':answer-field/correct' not in f
        assert ':question/worked-solution' not in q
        assert ':question/difficulty' not in q
    else:
        assert generation['eligible_for_learning'] is True
        assert f[':answer-field/correct'] == [':answer/id', ids[eligible[0]]]
        solution = q[':question/worked-solution']
        formatted(solution)
        opening = f'To obtain the unit vector that is parallel to ${vector}$, we divide ${vector}$ by its length:'
        assert solution.startswith(opening + '\n\n$$\n')
        math_block = re.fullmatch(re.escape(opening) + r'\n\n\$\$\n(.*?)\n\$\$', solution, re.S)[1]
        lhs, *stages = math_block.split('=')
        assert lhs == r'\mathbf{u}'
        expected_count = 2 if q[':question/difficulty'].endswith('/easy') else 3
        assert len(stages) == expected_count
        assert stages[0] == r'\dfrac{' + vector + r'}{\mid \,' + vector + r'\, \mid}'
        assert stages[1] == r'\dfrac{1}{' + re.search(r'has magnitude \$(.*?)\$', q[':question/problem'])[1] + '}' + vector
        for stage in stages:
            assert sp.simplify(expression(stage, vector, reverse, m) - V / m) == 0, stage
    return m, values



def served_record(source):
    """Adapt pulled enums/references only; preserve all displayed content and UUIDs."""
    q = copy.deepcopy(source)
    for f in q[':question/answer-fields']:
        f[':answer-field/type'] = f[':answer-field/type'][':db/ident']
        for a in f[':answer-field/choices']:
            a[':answer/type'] = a[':answer/type'][':db/ident']
        if ':answer-field/correct' in f:
            f[':answer-field/correct'] = [':answer/id', f[':answer-field/correct'][':answer/id']]
    raw = ':question/math-academy-id' in q
    if ':question/difficulty' in q:
        q[':question/difficulty'] = q[':question/difficulty'][':db/ident']
    return {'knowledge_point': {'db_id': g.KP_ID, 'id': g.KP_UUID, 'title': g.TITLE},
            'question': q, 'generation': {'evidence_only': raw, 'eligible_for_learning': not raw}}


def comparable(q):
    """Exact learner content, ordering aside; ignore only persistence IDs/enum wrappers."""
    q = copy.deepcopy(q)
    q.pop(':db/id', None)
    for f in q[':question/answer-fields']:
        f.pop(':db/id', None)
        for a in f[':answer-field/choices']:
            a.pop(':db/id', None)
        f[':answer-field/choices'].sort(key=lambda a: a[':answer/id'])
    return q


def actual_task(record):
    # Read actual rendered magnitude; no metadata/seed/profile can inflate this set.
    return sp.srepr(context(record)[2])


def expected_engine(record, label):
    f, = record['question'][':question/answer-fields']
    correct = f[':answer-field/correct'][1]
    checks = [{'submitted_answer_id': a[':answer/id'],
               'expected': 'accepted' if a[':answer/id'] == correct else 'rejected',
               'purpose': 'normal radio own-choice canonical selection / valid wrong selection'}
              for a in f[':answer-field/choices']]
    index = next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id'] == correct)
    checks.append({'submitted': '000' + str(100 + index), 'expected': 'accepted',
                   'purpose': 'genuine equivalent decimal entity-ID entry for same canonical choice'})
    return {'label': label, 'record': record, 'checks': checks}


def run():
    capture = json.loads((HERE/'source.json').read_text())
    assert {k:capture[k] for k in ('database','basis','lineage')} == g.SOURCE
    assert (HERE/'source.json').read_bytes() == (ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186096813.json').read_bytes()
    all_sources = capture['record'][':knowledge-point/questions']
    originals = [q for q in all_sources if q.get(':question/math-academy-id')]
    inventory = [q for q in all_sources if not q.get(':question/math-academy-id')]
    assert len(originals) == 2 and len(inventory) == 15
    write('source-cases.json', [{'source_id':q[':question/math-academy-id'],'record':q} for q in originals])
    generated_prior = json.loads((HERE/'reference/replenishment-generated.json').read_text())
    prior_by_id = {r['question'][':question/id']:r for r in generated_prior}
    assert set(prior_by_id) == {q[':question/id'] for q in inventory}
    inventory_rows = []
    engine_input, reviews, source_audit = [], [], []
    for q in all_sources:
        source_record = served_record(q)
        verify(source_record)
        sid = q.get(':question/math-academy-id',q[':question/id'])
        if q in inventory:
            prior = prior_by_id[q[':question/id']]
            assert comparable(source_record['question']) == comparable(prior['question'])
            generation = prior['generation']
            replay = g.generate(generation['authored_level'], generation['seed'],
                                generation['template'], parameters=generation['parameters'],profile=generation['profile'])
            verify(replay)
            assert comparable(replay['question']) == comparable(prior['question'])
            inventory_rows.append({'record':q, 'role':'independently authored inventory',
              'relationship_to_source_templates':
              'Generated by the previously registered known-magnitude-unit-vector-1 normalization bank; '
              'replenishment basis 2077→2078 supplies independent provenance. Same named/directed '
              'supplied-magnitude method as the MA originals; authored rating, solution and five-choice '
              'normalization bank are not additional MA source evidence.'})
            engine_input.append(expected_engine(replay,'Existing generated inventory '+sid))
            reviews.append({'label':'existing generated inventory replay '+sid,'record':replay})
        else:
            template = 'named' if sid == 'q-11376' else 'directed'
            p = {'m':5 if template == 'named' else 7}
            replay = g.generate_easy(template=template,parameters=p,profile='raw_'+template)
            verify(replay)
            qraw = replay['question']
            assert qraw[':question/problem'] == q[':question/problem']
            assert sorted(a[':answer/value'] for a in qraw[':question/answer-fields'][0][':answer-field/choices']) == sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])
            for attr in (':question/worked-solution',':question/difficulty'):
                assert (attr in qraw) == (attr in q)
            assert ':answer-field/correct' not in qraw[':question/answer-fields'][0]
            source_audit.append({'source_id':sid,'exact_prompt':True,'exact_full_bank_values':5,
                'correct_designation_present':False,'solution_present':False,'rating_present':False,
                'eligible_for_learning':False,'normalization':'raw evidence not normalized; normal arrow notation repaired'})
            reviews.append({'label':sid+' immutable evidence replay','record':replay})
            # Unkeyed originals cannot be graded. This separate named memory fixture adds
            # an independent key only for radio harness QA; the raw replay stays unkeyed.
            fixture = copy.deepcopy(replay)
            f = fixture['question'][':question/answer-fields'][0]
            vector,reverse,m = context(fixture)
            key = next(a[':answer/id'] for a in f[':answer-field/choices'] if expression(a[':answer/value'],vector,reverse,m)==V/m)
            f[':answer-field/correct'] = [':answer/id',key]
            fixture['generation']['native_fixture_added_key'] = 'independent mathematics; absent original key remains absent in source/replay'
            engine_input.append(expected_engine(fixture,sid+' independent-key memory-only source-bank fixture'))
    write('independent-inventory.json', {'database':capture['database'],'basis':capture['basis'],'lineage':capture['lineage'],'questions':inventory_rows})

    canonical = capture['record'][':knowledge-point/canonical-example']
    canonical_replay = g.generate_easy(template='named',parameters={'m':3})
    assert canonical_replay['question'][':question/problem'] == canonical[':question/problem']
    assert canonical_replay['question'][':question/worked-solution'] == canonical[':question/worked-solution']
    verify(canonical_replay)
    engine_input.append(expected_engine(canonical_replay,'canonical-example method replay with authored complete bank'))

    # Execute only the owned reconstructed prior-approved text, never the registered
    # .py path or registered cache. It exactly hashes to the former parent-QA SHA.
    legacy_text = (HERE/'reference/previous-approved.py.txt').read_text()
    assert hashlib.sha256(legacy_text.encode()).hexdigest() == '8fcca39b2e30ae777d225b78bd5aa99ed107d0ee1ef05b0e4ecc99852df27a49'
    legacy = {'__name__':'owned_prior_approved_reference'}
    exec(compile(legacy_text,'owned_prior_approved_reference','exec'),legacy)
    tested = raw_count = preserved = stages = 0
    task_counts, variety = {}, {}
    for level,domain in g.PARAMETER_DOMAINS.items():
        task_ids = set()
        for template in g.TEMPLATES:
            for profile in ('normalization','direction_errors'):
                for p in domain:
                    r = g.generate(level,29,template,parameters=p,profile=profile)
                    verify(r)
                    previous = legacy['generate'](level,29,template,parameters=p,profile=profile)
                    assert r['question'] == previous['question'], (level,template,profile,p)
                    assert r['generation']['content_fingerprint'] == previous['generation']['content_fingerprint']
                    preserved += 1
                    shuffled = g.generate(level,91,template,parameters=p,profile=profile)
                    assert r['question'][':question/id'] == shuffled['question'][':question/id']
                    assert r['generation']['mathematical_fingerprint'] == shuffled['generation']['mathematical_fingerprint']
                    assert r == g.generate(level,29,template,parameters=p,profile=profile)
                    task_ids.add(actual_task(r))
                    stages += 2 if level=='easy' else 3
                    tested += 1
                    if p in (domain[0],domain[-1]):
                        label=f'{level} / {template} / {profile} / {p}'
                        reviews.append({'label':label,'record':r})
                        engine_input.append(expected_engine(r,label))
        assert len(task_ids)==len(domain)
        task_counts[level] = len(task_ids)
        # Independent numeric variety only, one per magnitude; neither banks nor
        # repeated source prompts or labels create additional mathematical tasks.
        batch = g.generate_many(level,seed=572,count=len(domain))
        assert len({actual_task(r) for r in batch}) == len(domain)
        assert len({r['generation']['mathematical_fingerprint'] for r in batch}) == len(domain)
        assert batch == g.generate_many(level,seed=572,count=len(domain))
        variety[level]={'capacity':len(domain),'exhaustive_unique_rendered_tasks':len(task_ids),
                        'full_capacity_batch_unique_tasks':len(batch),'target_roles':'one supplied magnitude; one normalized parallel vector'}
    for template in g.TEMPLATES:
        for p in g.PARAMETER_DOMAINS['easy']:
            verify(g.generate_easy(template=template,parameters=p,profile='raw_'+template))
            raw_count += 1
    # Full label domain changes notation only, never a mathematical task.
    labels_checked = 0
    for level,domain in g.PARAMETER_DOMAINS.items():
        for template,labels in [('named',('a','b','c','v','w')),('directed',('AB','CD','PQ','RS'))]:
            for label in labels:
                r=g.generate(level,template=template,parameters={**domain[-1],'label':label})
                verify(r); labels_checked += 1
    a=g.generate_easy(template='named',parameters={'m':5,'label':'a'})
    b=g.generate_easy(template='named',parameters={'m':5,'label':'b'})
    c=g.generate_easy(template='directed',parameters={'m':5,'label':'PQ'})
    assert len({actual_task(r) for r in (a,b,c)})==1
    assert len({r['generation']['mathematical_fingerprint'] for r in (a,b,c)})==1
    assert len({r['question'][':question/id'] for r in (a,b,c)})==3
    alt=g.generate_easy(template='named',parameters={'m':5},profile='direction_errors')
    assert a['question'][':question/id']!=alt['question'][':question/id']
    assert actual_task(a)==actual_task(alt)

    # Mutation controls leave final correct answer intact; each operative stage
    # and full bank must be audited, rather than merely checking the last line.
    negatives=[]
    base=g.generate_hard(template='directed',parameters={'k':2,'d':3})
    def reject(label, mutated):
        try: verify(mutated)
        except (AssertionError,ValueError,TypeError): negatives.append(label)
        else: raise AssertionError('Negative control escaped: '+label)
    r=copy.deepcopy(base);q=r['question'];q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\dfrac{1}{2 \sqrt{3}}',r'\dfrac{1}{3 \sqrt{3}}');reject('wrong intermediate reciprocal with correct final value',r)
    r=copy.deepcopy(base);q=r['question'];q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\mid \,\overrightarrow{AB}\, \mid',r'\mid \,\overrightarrow{BA}\, \mid');reject('stale reverse norm argument with correct final answer',r)
    r=copy.deepcopy(base);q=r['question'];q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\mathbf{u}',r'\mathbf{v}');reject('wrong declared solution vector',r)
    r=copy.deepcopy(base);f=r['question'][':question/answer-fields'][0];right=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);wrong=next(a for a in f[':answer-field/choices'] if a[':answer/id']!=right[':answer/id']);wrong[':answer/value']='-'+right[':answer/value'];reject('opposite parallel unit distractor creates second eligible choice',r)
    r=copy.deepcopy(base);f=r['question'][':question/answer-fields'][0];f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])];reject('wrong key',r)
    r=copy.deepcopy(base);f=r['question'][':question/answer-fields'][0];f[':answer-field/choices'][0][':answer/value']=f[':answer-field/choices'][1][':answer/value'];reject('duplicate complete displayed vector',r)
    r=copy.deepcopy(base);f=r['question'][':question/answer-fields'][0];wrong=next(a for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1]);wrong[':answer/value']=r'27\overrightarrow{AB}';reject('arbitrary non-equivalent wrong distractor outside complete bank',r)
    # A negative-orientation unit vector is a valid answer to "parallel", not a
    # wrong distractor. A separate mathematical witness checks the full criterion.
    vector,reverse,m=context(base)
    assert expression('-'+g.product(1/m,vector),vector,reverse,m)==-V/m
    assert expression(g.product(1/m,reverse),vector,reverse,m)==-V/m
    assert sp.simplify(abs(-1/m)*m)==1

    bad_calls=[lambda:g.generate_easy(seed=True),lambda:g.generate_easy(seed=1.0),lambda:g.generate_easy(seed='1'),
       lambda:g.generate_many('easy',seed=True),lambda:g.generate_many('easy',count=True),lambda:g.generate_many('easy',count=1.0),
       lambda:g.generate_many('easy',count=0),lambda:g.generate_many('easy',count=30),lambda:g.generate_many('moderate',count=73),lambda:g.generate_many('hard',count=61),
       lambda:g.generate_easy(parameters={'m':True}),lambda:g.generate_easy(parameters={'m':1}),lambda:g.generate_easy(parameters={'m':31}),
       lambda:g.generate_moderate(parameters={'p':4,'q':2}),lambda:g.generate_moderate(parameters={'p':2,'q':3}),
       lambda:g.generate_hard(parameters={'k':1,'d':4}),lambda:g.generate_hard(parameters={'k':6,'d':2}),
       lambda:g.generate_easy(template='bad'),lambda:g.generate_easy(profile='bad'),lambda:g.generate_hard(profile='raw_named'),lambda:g.generate_easy(field_type='blank')]
    for call in bad_calls:
        try:call()
        except ValueError:pass
        else:raise AssertionError('invalid API input accepted')
    cli=[]
    for fmt in ('json','markdown'):
        result=subprocess.run([sys.executable,str(SCRIPT),'--difficulty','all','--count','1','--seed','17','--format',fmt],capture_output=True,text=True,check=True)
        if fmt=='json':assert isinstance(json.loads(result.stdout),list) and len(json.loads(result.stdout))==3
        else:assert result.stdout.count('### ')==3
        cli.append({'format':fmt,'all_count_1_records':3})
    capacity_cli=subprocess.run([sys.executable,str(SCRIPT),'--difficulty','all','--count','30','--format','json'],capture_output=True,text=True)
    assert capacity_cli.returncode==2 and 'between 1 and 29' in capacity_cli.stderr
    boundary_cli=subprocess.run([sys.executable,str(SCRIPT),'--difficulty','easy','--count','29','--format','json'],capture_output=True,text=True,check=True)
    boundary_records=json.loads(boundary_cli.stdout)
    assert len({actual_task(r) for r in boundary_records})==29

    write('variants.json',reviews)
    (HERE/'review.md').write_text('# Original evidence, existing inventory, and variants\n\n'+ '\n\n'.join('## '+x['label']+'\n\n'+g.markdown(x['record']) for x in reviews)+'\n')
    write('negative-controls.json',{'caught':negatives,'bad_api_inputs_rejected':len(bad_calls),'actual_rendered_math_only':True})
    write('engine-input.json',engine_input)
    subprocess.run([str(HERE/'reference/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    native=json.loads((HERE/'engine-report.json').read_text())
    assert native['documented_unresolved_checks']==0
    for item in native['records']:
        for check in item['checks']:
            if check['outcome']=='rejected':assert check['reason'] is None
    baseline=json.loads((HERE/'registered-baseline.json').read_text())
    current_paths={str(p.relative_to(ROOT)) for p in (ROOT/'generate/scratch/17592186096813').rglob('*') if p.is_file()}|{'generate/scratch/17592186096813.py'}
    assert current_paths=={row['path'] for row in baseline['files']}
    for row in baseline['files']:
        assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
    cache_baseline=json.loads((HERE/'registered-cache-baseline.json').read_text())
    for row in cache_baseline['files']:
        cache=ROOT/row['path']
        assert hashlib.sha256(cache.read_bytes()).hexdigest()==row['sha256']
        assert cache.stat().st_mtime_ns==row['mtime_ns']
    validation={'status':'passed','source':g.SOURCE,'database_writes':0,'registered_baseline_unchanged':True,
      'registered_baseline_files':len(baseline['files']),'prior_approved_math_preserved':preserved,
      'sibling_numeric_cache_baseline':{'files':len(cache_baseline['files']),'unchanged':True,'timing':cache_baseline['capture_timing']},
      'registered_change_identified':'Only stable GENERATOR_ID comment/constant; removal hashes to prior parent-approved 8fcca39b…',
      'raw_exact_prompts':2,'raw_complete_banks':2,'raw_exact_values':10,'original_present_keys':0,'original_present_solutions':0,'original_present_ratings':0,
      'source_audit':source_audit,'non_MA_inventory_records':15,'non_MA_inventory_exact_replays':15,'canonical_prompt_solution_exact':True,
      'exhaustive_normal_instances':tested,'exhaustive_raw_evidence_instances':raw_count,'all_printed_normal_equalities':stages,
      'unique_actual_math_tasks':task_counts,'variety':variety,'notation_variants_checked':labels_checked,'negative_controls':len(negatives),
      'invalid_API_inputs_rejected':len(bad_calls),'CLI':cli,'capacity_boundary_CLI':29,'capacity_guard_CLI':True,
      'parallel_criterion':'both ±v/m qualify; exactly one eligible option in every full bank; reverse endpoints negate vector; scalar is not vector',
      'native_grading':{'accepted':native['accepted_checks'],'valid_false_rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks'],
         'rejection_qualification':'All rejected own-choice IDs yield Ok(false), reason=null; no error relabeled as rejected.',
         'equivalent_entry_contract':'Radio selected decimal entity ID, including leading zero equivalent ID; expression literals are not this response type.',
         'engine_sha256':hashlib.sha256((HERE/'reference/check-engine').read_bytes()).hexdigest()},
      'generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'remaining_limitations':['Both MA original keys/solutions/ratings absent and remain ineligible raw evidence.','MA scalar-bank 2m/4m intended errors unresolved; no claim of original-key fidelity.','All normal E/M/H levels remain authored; existing generated inventory does not establish independent MA levels.']}
    write('validation.json',validation)
    print(json.dumps(validation,indent=2))

if __name__=='__main__':run()
