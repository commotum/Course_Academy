"""Post-delivery probes, conditional selection, and relocatable CLI checks."""
from validate_repair import *
import platform
import shutil
import tempfile


def select(candidates, seed):
    # question_selection.rs with positive easy-only weights and a fresh pool.
    pool = sorted(set(candidates))
    h = hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
    draw = (int.from_bytes(h[8:16], 'big') >> 11) / 2**53
    return pool[int(draw*len(pool))] if pool else None


def main():
    before = json.load(open(OUT/'delivery-input.json'))
    after = json.load(open(OUT/'delivery/accepted.json'))
    before_report, after_report = probes(before), probes(after)
    save('shortcut-after.json', after_report)
    def coverage(rs):
        groups = {}
        for r in rs:
            q = r['question']; t = r['generation']['template']
            c = groups.setdefault(t, dict(count=0, operations=Counter(), semantic_results=set()))
            c['count'] += 1
            c['operations'][str(operations(q[':question/problem']))] += 1
            c['semantic_results'].add(str((matrices(q[':question/problem'])[0], operations(q[':question/problem']))))
        for c in groups.values():
            c['semantic_instances'] = len(c.pop('semantic_results'))
        return groups
    save('stage-coverage.json', dict(before=coverage(before), after=coverage(after),
         before_shortcuts=before_report, after_shortcuts=after_report,
         limits='Finite probes; small conditional groups do not establish absence of all shortcuts. Original-only replay profiles are not normal sampled templates.'))
    # Check control decisions survive actual publisher filtering, allowing dedup.
    def witness(r):
        q=r['question'];f=q[':question/answer-fields'][0]
        return (q[':question/problem'],
                tuple(sorted(str(matrices(c[':answer/value'])[0]) for c in f[':answer-field/choices'])),
                str(expected(q)))
    # The publisher assigns canonical IDs; compare visible mathematical records.
    delivered = {witness(r): r for r in after}
    controls = [r for r in json.load(open(OUT/'counterfactual-records.json')) if r['generation']['difficulty']=='easy']
    assert all(witness(r) in delivered for r in controls)
    delivered_cases=[]
    for n, raw in enumerate(controls):
        r=delivered[witness(raw)];q=r['question'];want=expected(q)
        delivered_cases.append(dict(label=f'delivered-counterfactual-{n}',record=r,checks=[
            dict(submitted_answer_id=c[':answer/id'],
                 expected='accepted' if matrices(c[':answer/value'])[0]==want else 'rejected',
                 purpose='counterfactual survives delivery canonicalization')
            for c in q[':question/answer-fields'][0][':answer-field/choices']]))
    save('delivered-grader-input.json',delivered_cases)
    assert all(check(r)['unique_correct'] and check(r)['final_solution_correct'] for r in after)
    batch = json.load(open(OUT/'delivery-batch/accepted.json'))
    assert len(batch) == 5
    assert all(check(r)['unique_correct'] and check(r)['final_solution_correct'] for r in batch)
    inventory = json.load(open(JOB/'source/inventory.json'))
    old_easy = [q[':db/id'] for q in inventory['questions']
                if q.get(':question/difficulty',{}).get(':db/ident','').endswith('/easy')]
    new_ids = list(range(1,len(batch)+1))
    model_results=[]
    for seen in (False, True):
        pool = new_ids + ([] if seen else old_easy)
        selected = Counter(select(pool, f'repair-{n}') for n in range(256))
        assert all(selected[n] for n in new_ids)
        model_results.append(dict(inventory_excluded_as_seen=seen, modeled_pool=pool, counts=selected))
    save('selection-results.json', dict(conditional_tests=model_results,
         rule='Positive easy weight; sorted unique fresh IDs; digest offset 8 uniformly selects within easy band.',
         limits='No learner history or policy snapshot supplied, and publication has not allocated new database IDs. Synthetic IDs test conditional reachability, not the actual next learner draw. Zero easy weight excludes this batch; no-policy mode takes the first ID.'))
    manifest=json.load(open(PKG/'package.json'))
    assert manifest['dependencies']==dict(python=platform.python_version(),packages={})
    assert 'package.json' not in manifest['files']
    hashes={name:hashlib.sha256((PKG/name).read_bytes()).hexdigest() for name in manifest['files']}
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    checks=[]
    with tempfile.TemporaryDirectory(prefix='row-operation-relocation-') as temp:
        reloc=pathlib.Path(temp)
        for name in manifest['files']:
            target=reloc/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(PKG/name,target)
        env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(reloc/'assets')
        for difficulty in ('easy','moderate','hard'):
            outputs=[]
            for directory in (PKG,PKG,reloc):
                command=[sys.executable,str(directory/manifest['entrypoint']),'--difficulty',difficulty,
                         '--count','2','--seed','20261021','--format','json']
                p=subprocess.run(command,cwd=reloc,env=env,capture_output=True,text=True,check=True)
                outputs.append(json.loads(p.stdout))
            assert outputs[0]==outputs[1]==outputs[2]
            checks.append(dict(difficulty=difficulty, deterministic=True, relocatable=True, count=2))
        # Exercise added local data after relocation as well as normal sampling.
        command=[sys.executable,'-c','import generator as g,json; print(json.dumps([g.build(i) for i in g.source_instances()+g.moderate_ops.sources()]))']
        replay=json.loads(subprocess.run(command,cwd=reloc,env=env,capture_output=True,text=True,check=True).stdout)
        assert len(replay)==9
    assert hashes=={name:hashlib.sha256((PKG/name).read_bytes()).hexdigest() for name in manifest['files']}
    save('packaging-results.json', dict(python=platform.python_version(), dependencies=manifest['dependencies'],
         checks=checks, relocated_source_profiles=len(replay), runtime_hashes=hashes,
         runtime_files_unchanged_by_validation=True))
    print(json.dumps(dict(delivered=len(after), controls_retained=len(controls), batch=len(batch),
                          relocation_bands=3, relocated_source_profiles=len(replay))))


if __name__=='__main__':
    main()
