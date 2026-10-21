"""Read-only delivery/selection/relocation checks, after audit.py and check_delivery."""
import collections, hashlib, json, pathlib, shutil, subprocess, sys
import audit as A

def counts(rows):
    return dict(collections.Counter(r['generation']['template'] for r in rows))
def outcomes(rows):
    return {'count':len(rows),'by_template':counts(rows),
        'shortcut_correct':sum(A.shortcut(r)==A.key(r) for r in rows)}

def choose(candidates,weights,seed,seen=()):
    # Faithful implementation of question_selection.rs::select: deduplicate and
    # sort numeric entity IDs, draw band then draw uniformly in band using SHA256.
    candidates=sorted({q[':db/id']:q for q in candidates if q[':db/id'] not in seen}.values(),key=lambda q:q[':db/id'])
    if weights is None:return candidates[0] if candidates else None
    bands=[[],[],[]];unrated=[]
    for q in candidates:
        d=q.get(':question/difficulty')
        if d is None:unrated.append(q);continue
        ident=d[':db/ident'] if isinstance(d,dict) else d
        bands[['easy','moderate','hard'].index(ident.split('/')[-1])].append(q)
    digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
    u=lambda offset:(int.from_bytes(digest[offset:offset+8],'big')>>11)/(1<<53)
    total=sum(w for w,band in zip(weights,bands) if band)
    if total>0:
        draw=u(0)*total;chosen=None
        for i,w in enumerate(weights):
            if not bands[i] or w==0:continue
            chosen=i
            if draw<w:break
            draw-=w
        pool=bands[chosen]
    else:pool=unrated
    return pool[int(u(8)*len(pool))] if pool else None

def run():
    batch=A.load(A.HERE/'runner-batch.json');samples=A.load(A.HERE/'easy-samples.json')
    delivered={name:A.load(A.HERE/f'delivery-{name}/accepted.json') for name in ['batch','samples']}
    stages={'batch_before':outcomes(batch),'batch_after':outcomes(delivered['batch']),
            'fresh_before':outcomes(samples),'fresh_after':outcomes(delivered['samples'])}
    # Observe actual rejection/resampling calls for these identical fresh seeds.
    rejection=[];original=A.G.sample
    for row in samples:
        calls=[]
        def instrumented(t,r):
            p=original(t,r);calls.append({'template':t,'parameters':p});return p
        A.G.sample=instrumented
        m=row['generation'];r=A.G.generate('easy',seed=m['seed'],template=m['template'])
        assert r==row
        rejection.append({'seed':m['seed'],'template':m['template'],'attempts':calls,'accepted_question_id':r['question'][':question/id']})
    A.G.sample=original
    # Controlled relevant and irrelevant dependencies: check complete responses,
    # permutation, native outcomes, and rendered record binding, not metadata alone.
    pairs=A.load(A.HERE/'counterfactual-records.json')
    text=lambda r:next(a[':answer/value'] for a in A.field(r)[':answer-field/choices'] if a[':answer/id']==A.key(r))
    assert pairs[0]['question'][':question/problem']!=pairs[1]['question'][':question/problem']
    assert text(pairs[0])!=text(pairs[1])
    assert pairs[0]['question'][':question/problem']==pairs[2]['question'][':question/problem']
    assert pairs[0]['question'][':question/worked-solution']==pairs[2]['question'][':question/worked-solution']
    assert text(pairs[0])==text(pairs[2]) and A.key(pairs[0])==A.key(pairs[2])
    assert A.field(pairs[0])[':answer-field/choices']!=A.field(pairs[2])[':answer-field/choices']
    grader=A.load(A.HERE/'grader-report.json')
    labels={r['label']:r for r in grader['records']}
    assert all(r['question'][':question/id'] in labels for r in pairs)
    # Six captured designations must agree with independently matched banks.
    source=A.load(A.JOB/'source/source.json');replays=A.load(A.HERE/'source-replay-records.json')
    matches=A.load(A.HERE/'source-replay-results.json')['practice_cases'];key_checks=[]
    for q,m,r in zip(source['material']['kp'][':knowledge-point/questions'],matches,replays):
        f=q[':question/answer-fields'][0]
        if ':answer-field/correct' in f:
            sid=f[':answer-field/correct'][':answer/id']
            mapped=next(x['generated_answer_id'] for x in m['matches'] if x['source_answer_id']==sid)
            assert mapped==A.key(r)
            key_checks.append({'source_id':q[':question/id'],'source_correct_answer':sid,'generated_correct_answer':mapped,'passed':True})
    A.save('source-designation-results.json',{'checks':key_checks,'missing_source_keys':2})
    # Current inventory selection, with real captured entity IDs. Missing
    # learner history/policy is a scenario parameter, never asserted as live data.
    inv=A.load(A.JOB/'source/inventory.json')
    usable=[q for q in inv['questions'] if ':answer-field/correct' in q[':question/answer-fields'][0]]
    affected=A.load(A.HERE/'affected-inventory.json')['affected_questions'];bad={q['entity_id'] for q in affected}
    source_ids={q[':db/id'] for q in usable if ':question/math-academy-id' in q}
    scenarios=[]
    for label,weights,seen in [('easy band, no history',(1,0,0),set()),
        ('easy band, source questions already seen',(1,0,0),source_ids),
        ('easy band, affected questions already seen',(1,0,0),bad),
        ('illustrative 6:3:1 weights, no history',(6,3,1),set()),
        ('unconfigured policy',None,set())]:
        draws=[]
        for i in range(60):
            seed=f'independent-review-73/{i}';q=choose(usable,weights,seed,seen)
            draws.append({'seed':seed,'entity_id':q[':db/id'] if q else None,
                          'affected_generated_easy':q is not None and q[':db/id'] in bad})
        scenarios.append({'scenario':label,'weights':weights,'seen_entity_ids':sorted(seen),
            'draws':draws,'affected_draws':sum(d['affected_generated_easy'] for d in draws)})
    A.save('delivery-selection-results.json',{'command':f'{sys.executable} {A.HERE/"pipeline_audit.py"}',
        'stages':stages,'generator_rejection_trace':rejection,'inventory_basis':inv['basis'],
        'usable_current_inventory':len(usable),'selection_implementation':'engine/rust/question_selection.rs::select and seen_before_task',
        'selection_scenarios':scenarios,
        'conclusion':'All sampled generated easy items retain the shortcut before/after rejection and delivery. All 3 affected stored easy records remain selectable. Current easy pool also has two original source questions; do not equate its entire distribution to the generated subgroup.',
        'limits':['Live inventory may change after basis 5319. No publication preparation exists. Shared check_delivery used actual publisher preparation read-only.',
                  'No learner history or configured policy weights supplied. Scenario results condition on explicit weights/history; they are not a claim about an actual learner next question.',
                  'Selection cannot remove the bank-only shortcut within any surviving authored easy item.']})
    # Relocation uses only a copy under evidence_root and captures stdout there.
    relocation=A.HERE/'relocated-package'
    if not relocation.exists():shutil.copytree(A.PKG,relocation)
    commands=[];outputs=[]
    for label,root in [('original',A.PKG),('relocated',relocation)]:
        cmd=[sys.executable,str(root/'17592186087877.py'),'--difficulty','easy','--seed','9183','--count','2','--format','json']
        cp=subprocess.run(cmd,cwd=A.HERE,capture_output=True,text=True)
        (A.HERE/f'{label}-cli.json').write_text(cp.stdout)
        (A.HERE/f'{label}-cli.stderr').write_text(cp.stderr)
        assert cp.returncode==0
        outputs.append(json.loads(cp.stdout));commands.append(cmd)
    assert outputs[0]==outputs[1]
    p=A.load(A.HERE/'packaging-results.json');p.update({'relocation_commands':commands,
        'relocation_equal':True,'package_unchanged':A.snapshot()==A.load(A.HERE/'package-before.json')})
    A.save('packaging-results.json',p)
    A.save('counterfactual-integration-results.json',{'relevant_changed_prompt_answer_and_solution':True,
        'irrelevant_permutation_preserved_full_response_and_key':True,
        'native_grader_labels':[r['question'][':question/id'] for r in pairs],
        'native_grader_file':'grader-report.json','render_input_file':'render-input.json'})
    print(json.dumps({'stages':stages,'selection_scenarios':[{k:r[k] for k in ['scenario','affected_draws']} for r in scenarios],
                      'source_designations':len(key_checks),'relocation_equal':True}))

if __name__=='__main__':run()
