#!/usr/bin/env python3
"""Independent displayed-content, fidelity, scope, identity and native grading QA."""
import sys
sys.dont_write_bytecode = True
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
SCRIPT = D.with_suffix('.py')
sys.path.insert(0, str(ROOT))
from scripts.question_capture.math_format import validate_generated_record, normalize_prose
spec = importlib.util.spec_from_file_location('zero_matrix_private_draft', SCRIPT)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def write(name, value):
    (D/name).write_text(json.dumps(value, indent=2)+'\n')


def displayed_arrays(text):
    found = re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}', text)
    assert len(found) == 3 and len({x[0] for x in found}) == 3
    values = {}
    for name, body in found:
        rows = [[Fraction(v.strip()) for v in row.split('&')] for row in body.split(r'\\')]
        assert 1 <= len(rows) <= 4 and 1 <= len(rows[0]) <= 6 and len({len(z) for z in rows}) == 1
        assert all(v in [Fraction(0), Fraction(1), Fraction(1,10), Fraction(3), Fraction(10)] for row in rows for v in row)
        values[name] = rows
    assert sum(len(z)*len(z[0]) for z in values.values()) <= 46
    return values


def validate_record(record):
    validate_generated_record(record)
    assert set(record) == {'knowledge_point', 'question', 'generation'}
    assert record['knowledge_point'] == {'db_id': g.KP_ID, 'id': g.KP_UUID, 'title': g.TITLE}
    q = record['question']; text = q[':question/problem']; worked = q[':question/worked-solution']
    for s in [text, worked]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
        assert not re.search(r'[\x00-\x08\x0b-\x1f\x7f]', s), 'Control character in learner content'
    matrices = displayed_arrays(text)
    truths = {name: all(v == 0 for row in rows for v in row) for name, rows in matrices.items()}
    bullets = worked.split('\n\n')
    assert len(bullets) == 4, 'Exactly three independent classifications then conclusion'
    for (name, rows), bullet in zip(matrices.items(), bullets[:3]):
        assert bullet.startswith('- $'+name+'$ is ')
        nz = [(r+1,c+1,v) for r,row in enumerate(rows) for c,v in enumerate(row) if v]
        if not nz:
            assert bullet == '- $'+name+'$ is a zero matrix since *all* its entries are zeros.'
        else:
            assert re.search(r'is (?:\*not\*|not) a zero matrix since ', bullet)
            one = 'one of its entries is not zero' in bullet
            assert one == (record['generation']['template'] == 'q-68729')
            assert ('some of its entries are not zeros (for instance, ' in bullet) == (not one)
            # Source uses either {a}_{rc} or a_{rc}. Evaluate the printed witness
            # at the displayed coordinate, not the generation parameters.
            m = re.search(r'\$(?:\{([a-z])\}|([a-z]))_\{([1-4])([1-6])\}=([0-9.]+)\\(?:ne |neq)0\$', bullet)
            assert m, 'Required operative witness equality missing'
            assert (m[1] or m[2]) == name.lower()
            r,c = int(m[3]),int(m[4]);v = Fraction(m[5])
            assert r <= len(rows) and c <= len(rows[0]) and rows[r-1][c-1] == v != 0, 'Printed witness is false'
    names = re.findall(r'\$([A-Z])\$', bullets[-1])
    assert names == [n for n,z in truths.items() if z], 'Conclusion must match actual matrices in displayed order'
    assert bullets[-1].startswith('Therefore, ')
    fields = q[':question/answer-fields']; types = {f[':answer-field/type'] for f in fields}
    assert len(types) == 1
    t = g.TEMPLATES[record['generation']['template']]
    assert [sum(v!=0 for row in rows for v in row) for rows in matrices.values()] == t['nonzero_counts']
    assert types == {':answer-field.type/'+t['field_type']}
    ids = set()
    for f in fields:
        assert f[':answer-field/id'] not in ids; ids.add(f[':answer-field/id'])
        choices = f[':answer-field/choices']; values = [a[':answer/value'] for a in choices]
        assert len(set(values)) == len(values), 'Complete displayed bank must have no collisions'
        assert all(a[':answer/type'] == ':answer.type/text' for a in choices)
        for a in choices:
            assert a[':answer/id'] not in ids;ids.add(a[':answer/id'])
        selected = [a for a in choices if a[':answer/id'] == f[':answer-field/correct'][1]]
        assert len(selected) == 1
        if f[':answer-field/type'].endswith('/checkbox'):
            assert len(fields) == 3 and set(values) == {'false','true'}
            assert f[':answer-field/key'] in truths
            assert selected[0][':answer/value'] == str(truths[f[':answer-field/key']]).lower()
        else:
            assert len(fields) == 1 and len(choices) == 5 and f[':answer-field/key'] == 'selection'
            subsets = [frozenset(re.findall(r'\$([A-Z])\$', s)) for s in values]
            assert len(set(subsets)) == 5, 'Response-equivalent subset collision'
            assert all(z <= set(matrices) for z in subsets)
            correct_set = frozenset(n for n,z in truths.items() if z)
            assert frozenset(re.findall(r'\$([A-Z])\$', selected[0][':answer/value'])) == correct_set
            expected_masks = {frozenset(list(matrices)[i] for i in mask) for mask in t['subset_masks']}
            assert set(subsets) == expected_masks, 'All five complete source subset patterns required'
    assert set(f[':answer-field/key'] for f in fields) == (set(matrices) if t['field_type']=='checkbox' else {'selection'})
    return True


def same_bank(raw, generated):
    rf = {f[':answer-field/key']: f for f in raw[':question/answer-fields']}
    gf = {f[':answer-field/key']: f for f in generated['question'][':question/answer-fields']}
    assert set(rf) == set(gf)
    choices = designations = 0
    for key, f in rf.items():
        target = gf[key]
        assert f[':answer-field/type'][':db/ident'] == target[':answer-field/type']
        assert sorted((a[':answer/type'][':db/ident'], a[':answer/value']) for a in f[':answer-field/choices']) == sorted((a[':answer/type'], a[':answer/value']) for a in target[':answer-field/choices'])
        choices += len(f[':answer-field/choices'])
        if ':answer-field/correct' in f:
            correct = next(a[':answer/value'] for a in target[':answer-field/choices'] if a[':answer/id']==target[':answer-field/correct'][1])
            assert correct == f[':answer-field/correct'][':answer/value'];designations += 1
    return choices, designations


def rejected_mutation(record, mutate):
    changed = copy.deepcopy(record); original_keys = [f[':answer-field/correct'] for f in record['question'][':question/answer-fields']]
    mutate(changed)
    assert original_keys == [f[':answer-field/correct'] for f in changed['question'][':question/answer-fields']]
    try:
        validate_record(changed)
    except (AssertionError, ValueError, IndexError):
        return True
    raise AssertionError('Negative control escaped independent validation')


def main():
    wrapper = json.loads((D/'source.json').read_text()); cases=json.loads((D/'source-cases.json').read_text())
    captured = wrapper['record'][':knowledge-point/questions']
    assert {z['source_id']:z['record'] for z in cases} == {q[':question/math-academy-id']:q for q in captured if ':question/math-academy-id' in q}
    inventory = json.loads((D/'independent-inventory.json').read_text())
    assert {x:inventory[x] for x in ('database','basis','lineage')} == {x:wrapper[x] for x in ('database','basis','lineage')}
    assert [x['record'] for x in inventory['questions']] == [q for q in captured if ':question/math-academy-id' not in q]
    assert all(x['role']=='independently authored inventory' and x['relationship_to_source_templates'] for x in inventory['questions'])
    review=[];fidelity=[];choice_count=designation_count=exact_solutions=0
    for case in cases:
        r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        validate_record(r);raw=case['record']
        assert raw[':question/problem'] == r['question'][':question/problem']
        choices,designations=same_bank(raw,r);choice_count+=choices;designation_count+=designations
        sol=raw.get(':question/worked-solution');target=r['question'][':question/worked-solution']
        if case['source_id']=='q-126201':
            assert target == sol.replace('${i}_{12}', '${i}_{21}')
        elif sol:
            assert sol == target;exact_solutions+=1
        fidelity.append({'source_id':case['source_id'],'prompt_raw_exact':True,'bank_values_exact':choices,'original_designations_matched':designations,'solution_raw_exact':sol==target if sol else None,'repair':case['repair']})
        review.append({'role':'original MA replay; documented repair when present','source_id':case['source_id'],'record':r})
    canonical=json.loads((D/'canonical.json').read_text())
    cr=g.generate('easy',template='canonical',parameters=canonical['restored_parameters'])
    validate_record(cr);assert cr['question'][':question/worked-solution']==canonical['record'][':question/worked-solution']
    review.append({'role':'canonical restored from original screenshot; authored fields','source_id':'e-4390','record':cr})
    for level in g.SUPPORTED_LEVELS:
        for i,template in enumerate(g.DEFAULT_TEMPLATES):
            for seed in [1000+i,2000+i]:
                r=g.generate(level,seed=seed,template=template);validate_record(r)
                review.append({'role':'authored same-method variant; '+('source-observed easy family or unrated placement' if level=='easy' else 'uncalibrated '+level),'source_id':template,'record':r})
    # Broad content verification and collision-free mathematical bank per level.
    samples=g.batch('all',500,seed=31000)
    assert len(samples)==1500 and len({x['generation']['parameter_fingerprint'] for x in samples})==1500
    source_fps={g.fingerprint_text(q[':question/problem']) for q in captured}
    source_fps.add(cr['generation']['parameter_fingerprint'])
    assert not source_fps & {x['generation']['parameter_fingerprint'] for x in samples}
    family_coverage={}
    for level in g.SUPPORTED_LEVELS:
        family_coverage[level]=sorted({r['generation']['template'] for r in samples if r['question'][':question/difficulty'].endswith('/'+level)})
        assert set(family_coverage[level]) == set(g.DEFAULT_TEMPLATES)
    for r in samples:validate_record(r)
    # Explicit target-position coverage: every feasible cell of each nonzero role,
    # for every source family, all levels. Other matrices shrink without changing
    # source nonzero counts, keeping total workload within the observed ceiling.
    slot_coverage={};slot_records=[]
    for level in g.SUPPORTED_LEVELS:
        for template,t in g.TEMPLATES.items():
            for slot,count in enumerate(t['nonzero_counts']):
                if not count:continue
                covered=[]
                for row in range(1,5):
                    for col in range(1,7):
                        p={'labels':['A','B','C'],'matrices':[],'witnesses':[]}
                        for j,cnt in enumerate(t['nonzero_counts']):
                            nr,nc=(4,6) if j==slot else (1,max(1,cnt))
                            rows=[['0']*nc for _ in range(nr)]
                            cells=[(row-1,col-1)] if j==slot else []
                            cells += [(rr,cc) for rr in range(nr) for cc in range(nc) if (rr,cc) not in cells][:max(0,cnt-len(cells))]
                            for rr,cc in cells:rows[rr][cc]='1'
                            p['matrices'].append(rows);p['witnesses'].append([cells[0][0]+1,cells[0][1]+1] if cells else None)
                        r=g.generate(level,template=template,parameters=p);validate_record(r);slot_records.append(r);covered.append([row,col])
                assert len(covered)==24
                slot_coverage[level+'/'+template+'/'+str(slot)]=covered
    # Seed/order and cosmetic naming cannot change task identity.
    c=cases[2];r=g.generate('easy',template=c['template'],parameters=c['parameters'],seed=1)
    same=g.generate('easy',template=c['template'],parameters=c['parameters'],seed=11,profile='observed')
    assert r['question'][':question/id']==same['question'][':question/id']
    p=copy.deepcopy(c['parameters']);p['labels']=['A','B','C']
    alias=g.generate('easy',template=c['template'],parameters=p)
    assert alias['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
    assert alias['question'][':question/id']!=r['question'][':question/id']
    assert g.fingerprint_text(r['question'][':question/problem'])==g.fingerprint_text(same['question'][':question/problem'])
    actual=list(displayed_arrays(r['question'][':question/problem']).items())
    reordered=','.join(n+'='+g.matrix_tex([[str(v) for v in row] for row in rows]) for n,rows in reversed(actual))
    assert g.fingerprint_text(reordered)==r['generation']['parameter_fingerprint']
    magnitude_p=copy.deepcopy(c['parameters'])
    magnitude_p['matrices']=[[[('10' if v!='0' else v) for v in row] for row in rows] for rows in magnitude_p['matrices']]
    mag=g.generate('easy',template=c['template'],parameters=magnitude_p)
    assert mag['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
    assert mag['question'][':question/id']!=r['question'][':question/id']
    orderings={tuple(tuple(a[':answer/id'] for a in f[':answer-field/choices']) for f in g.generate('easy',template=c['template'],parameters=c['parameters'],seed=seed)['question'][':question/answer-fields']) for seed in range(20)}
    assert len(orderings)>1
    # Scope and strict public interface, including explicit parameters.
    invalid=0
    for kwargs in [{'level':'unrated'},{'level':'easy','template':'bogus'},{'level':'easy','field_type':'blank'},{'level':'easy','template':'q-11553','field_type':'checkbox'},{'level':'hard','profile':'bogus'}]:
        try:g.generate(**kwargs)
        except ValueError:invalid+=1
        else:raise AssertionError('Invalid API call accepted')
    for level in g.SUPPORTED_LEVELS:
        for change in ['shape','entry','witness','count','extra']:
            p=copy.deepcopy(c['parameters'])
            if change=='shape':p['matrices'][0].append(['0']*7)
            if change=='entry':p['matrices'][0][0][0]='x'
            if change=='witness':p['witnesses'][1]=[0,0]
            if change=='count':p['matrices'][0][0][0]='1'
            if change=='extra':p['junk']=1
            try:g.generate(level,template=c['template'],parameters=p)
            except ValueError:invalid+=1
            else:raise AssertionError('Invalid explicit parameter accepted')
    negative=[]
    fixed=next(z['record'] for z in review if z['source_id']=='q-68729')
    def alter_solution(r,a,b):r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(a,b,1)
    negative.append(rejected_mutation(fixed,lambda r:alter_solution(r,'=1\\ne 0','=3\\ne 0')))
    negative.append(rejected_mutation(fixed,lambda r:alter_solution(r,'${t}_{12}=1\\ne 0$','a nonzero entry')))
    negative.append(rejected_mutation(fixed,lambda r:alter_solution(r,'${t}_{12}','${t}_{11}')))
    negative.append(rejected_mutation(fixed,lambda r:alter_solution(r,'Therefore, only $V$','Therefore, only $T$')))
    negative.append(rejected_mutation(fixed,lambda r:alter_solution(r,'- $V$ is a zero matrix since *all* its entries are zeros.\n\n','')))
    negative.append(rejected_mutation(fixed,lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\x0c')))
    native_records=[z['record'] for z in review]+samples+slot_records
    native=[]
    for i,r in enumerate(native_records):
        checks=[]
        for fi,f in enumerate(r['question'][':question/answer-fields']):
            for a in f[':answer-field/choices']:
                checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every complete displayed option; original and varied bank'})
        native.append({'label':str(i)+'-'+r['generation']['template'],'record':r,'checks':checks})
    write('engine-input.json',native)
    build=json.loads((D/'reference/grader-build.json').read_text())
    hashes={build['source']:build['source_sha256'],build['library']:build['library_sha256'],build['binary']:build['binary_sha256'],**build['engine_sources'],**build['dependencies']}
    assert len(hashes)==42
    for p,h in hashes.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
    subprocess.run([str(ROOT/build['binary']),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True,cwd=ROOT)
    write('source-fidelity.json',fidelity);write('slot-coverage.json',slot_coverage);write('review.json',review);write('samples.json',samples[:3]);write('render-records.json',[x['record'] for x in review])
    cli=json.loads(subprocess.check_output([str(ROOT/'.venv/bin/python'),str(SCRIPT),'--difficulty','all','--count','1','--format','json'],cwd=ROOT))
    assert len(cli)==3 and [r['question'][':question/difficulty'] for r in cli]==[':question.difficulty/'+x for x in g.SUPPORTED_LEVELS]
    for r in cli:validate_record(r)
    baseline=json.loads((D/'registered-baseline.json').read_text())
    paths=[D.parent/'17592186087695.py',*sorted((D.parent/'17592186087695').rglob('*')),*sorted((D.parent/'__pycache__').glob('17592186087695.*.pyc'))]
    actual={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}
    assert actual==baseline,'Registered numeric script/tree/pycs changed'
    report={'status':'passed','database_writes':0,'registered_pathset_and_hashes_unchanged':len(actual),'source_basis':wrapper['basis'],'source_lineage':wrapper['lineage'],'original_MA_practice':len(cases),'independent_inventory':len(inventory['questions']),'canonical_separate':1,'raw_exact_prompts':7,'complete_source_banks':7,'exact_source_choices':choice_count,'exact_existing_correct_designations':designation_count,'missing_original_correct_designations_inferred':2,'raw_exact_existing_solutions':exact_solutions,'existing_solution_denominator':5,'minimal_mathematical_solution_repairs':1,'missing_original_solutions_authored':2,'canonical_solution_exact':True,'generated_default_records_checked':len(samples),'generated_default_task_fingerprints':len({r['generation']['parameter_fingerprint'] for r in samples}),'default_family_coverage':family_coverage,'explicit_witness_slot_records':len(slot_records),'slot_groups':len(slot_coverage),'rejected_invalid_API_and_parameter_calls':invalid,'negative_controls_unchanged_final_keys':len(negative),'native_hashes_verified':len(hashes),'native_report':json.loads((D/'engine-report.json').read_text())|{'records':'See engine-report.json'},'difficulty_limit':'Moderate and hard are same-method authored/uncalibrated; no observed calibration or additional matrix skill claimed.','native_equivalent_entry_limit':'Fields are discrete checkbox/radio selections. No scalar-equivalent-entry parser applies; all displayed choices tested by their actual answer IDs.','python_version':sys.version.split()[0]}
    write('validation.json',report)
    lines=['# Zero-matrix review','', 'All originals retain raw evidence in source-cases.json. q-126201 uses the one documented witness correction; two unrated radio originals receive authored solutions and inferred keys. Moderate/hard variants are uncalibrated same-method placements.','']
    for row in review:
        r=row['record'];q=r['question'];lines += ['## '+row['source_id']+' — '+row['role']+' — '+q[':question/difficulty'].split('/')[-1],'',q[':question/problem'],'',q[':question/worked-solution'],'']
        for f in q[':question/answer-fields']:
            correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            lines += ['Field '+f[':answer-field/key']+' ('+f[':answer-field/type']+'): '+json.dumps([a[':answer/value'] for a in f[':answer-field/choices']])+'; correct: '+correct,'']
    (D/'review.md').write_text('\n'.join(lines))
    print(json.dumps({k:v for k,v in report.items() if k!='native_report'},indent=2))


if __name__=='__main__':main()
