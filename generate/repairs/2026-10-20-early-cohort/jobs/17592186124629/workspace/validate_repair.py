"""Visible-record witnesses, complete source banks, controlled changes and native grading."""
import collections
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = Path('/home/jake/Developer/Course_Academy')
JOB = REPO/'generate/repairs/2026-10-20-early-cohort/jobs/17592186124629'
E = ROOT/'evidence'
spec = importlib.util.spec_from_file_location('imt', ROOT/'17592186124629.py')
g = importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name, value):
    (E/name).write_text(json.dumps(value, indent=2)+'\n')

def plain(s):
    for _ in range(3): s = re.sub(r'\\(?:text|operatorname|textrm|mathrm|mathbb)\{([^{}]*)\}',r'\1',s)
    return re.sub(r'\s|\$|\*', '', s).replace(r'\det','det').replace(r'\,','').replace(r'\!','')

def evaluate(s, n, rank):
    """Evaluate printed assertions on diagonal matrices diag(1^rank,0^(n-rank))."""
    t = plain(s)
    if 'hasnobasis' in t: return False
    if 'hasabasis' in t: return True
    if 'notinvertible' in t or 'hasnoinverse' in t: return rank < n
    if 'isinvertible' in t: return rank == n
    if 'det(A)' in t: return rank == n if r'\ne' in t else rank < n
    if 'Ax=0' in t: return rank == n if ('onlythetrivial' in t or 'nonon-trivial' in t) else rank < n
    if 'pivotcolumns' in t:
        if 'allcolumns' in t.lower(): return rank == n
        if 'fewerthan' in t or 'lessthan' in t: return rank < n
        m = re.search(r'has(n|\d+)pivot', t);assert m,t
        return rank == (n if m[1]=='n' else int(m[1]))
    if 'Null(A)' in t and 'hasdimensionzero' in t: return n-rank == 0
    if t.startswith('nullity(A)') or t.startswith('dim(Null(A))'):
        return n-rank > 0 if (r'\ne0' in t or '>0' in t) else n-rank == 0
    if t.startswith('rank(A)') or t.startswith('dim(Col(A))'):
        m = re.search(r'(=|<)(n|\d+)',t);assert m,t
        target = n if m[2]=='n' else int(m[2])
        return rank == target if m[1]=='=' else rank < target
    if t.startswith('Col(A)'):
        m = re.search(r'\{?R\}?\^\{(n|\d+)\}',t);assert m,t
        target = n if m[1]=='n' else int(m[1])
        if r'\subsetneq' in t or '⊂' in t or r'\ne' in t: return rank < n
        return rank == n and target == n
    if t.startswith('Null(A)'):
        if re.search(r'\{?R\}?\^',t): return rank == 0
        return rank < n if r'\ne' in t else rank == n
    raise AssertionError('Unparsed visible proposition: '+s)

def decode(r):
    q = r['question'];prompt = q[':question/problem'];given = prompt.split('then')[0]
    m = re.search(r'\$(n|\d+)\\times (n|\d+)\$',given)
    assert m and m[1]==m[2], given
    dims = [int(m[1])] if m[1]!='n' else [1,2,5,9]
    # Read only the hypothesis, not generation metadata or stored keys.
    hyp = given.split(' matrix and ',1)[1].rstrip(' ,') if ' matrix and ' in given else '$A$ is invertible'
    fields = q[':question/answer-fields']
    statements = ([f[':answer-field/key'] for f in fields] if len(fields)==3 else
                  re.findall(r'^I{1,3}\. (.+)$',prompt,re.M))
    assert len(statements)==3
    witness_results=[]
    for n in dims:
        ranks=[rank for rank in range(n+1) if evaluate(hyp,n,rank)]
        assert ranks, hyp
        values=[tuple(evaluate(s,n,rank) for s in statements) for rank in ranks]
        witness_results.extend(values)
    # For an implication, a conclusion qualifies iff true for every compatible matrix.
    expected = tuple(all(v[i] for v in witness_results) for i in range(3))
    if len(fields)==3:
        actual=tuple(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])=='true' for f in fields)
    else:
        f=fields[0]
        value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        actual=tuple(bool(re.search(r'\b'+l+r'\b',value)) for l in ('I','II','III'))
    assert actual==expected,(r['generation'],statements,actual,expected)
    sol=q[':question/worked-solution']
    clauses=re.findall(r'- The following statement is (true|false):\s*\n\s*\*If ([^\n]+)\*',sol)
    assert len(clauses)==3,(r['generation']['template'],len(clauses))
    solution_map={}
    for printed, clause in clauses:
        assert 'then' in clause
        condition, conclusion=clause.split('then',1)
        shyp=condition.split(' matrix and ',1)[1].rstrip(' ,') if ' matrix and ' in condition else '$A$ is invertible'
        vals=[]
        for n in dims:
            ranks=[rank for rank in range(n+1) if evaluate(shyp,n,rank)]
            vals.extend(evaluate(conclusion,n,rank) for rank in ranks)
        assert (printed=='true')==all(vals),(printed,clause)
        solution_map[plain(conclusion).rstrip('.').lower()] = printed=='true'
    for s,b in zip(statements,expected):
        assert solution_map[plain(s).rstrip('.').lower()]==b,(s,solution_map)
    return expected

def native_checks(r):
    return [{'field_index':i,'submitted_answer_id':a[':answer/id'],
      'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
      'purpose':'Visible assertion independently evaluated on every compatible rank'}
      for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def cues(rows):
    groups=collections.defaultdict(list)
    for r in rows:
        p=r['question'][':question/problem']
        fs=r['question'][':question/answer-fields']
        # Recognizable profile includes dimension, response contract and conclusion concepts.
        sid=r['generation']['template'];key=(tuple(g.SLOTS[sid]),g.DIMENSIONS.get(sid,'n'),len(fs))
        expected=decode(r)
        correct_positions=tuple(i for i,f in enumerate(fs) if len(fs)==3 and expected[i]) if len(fs)==3 else tuple(i for i,a in enumerate(fs[0][':answer-field/choices']) if a[':answer/id']==fs[0][':answer-field/correct'][1])
        groups[key].append((expected,correct_positions,r['generation']['parameters'].get('invertible')))
    report=[]
    for key,rows2 in groups.items():
        answers=collections.Counter(b for b,_,_ in rows2);positions=collections.Counter(p for _,p,_ in rows2)
        counts=collections.Counter(sum(b) for b,_,_ in rows2)
        assert len(answers)>1,('Fixed profile response',key)
        assert len(positions)>1,('Fixed correct position',key)
        assert len(counts)>1,('Fixed correct count',key)
        by_state={str(state):len(set(b for b,_,s in rows2 if s==state)) for state in (False,True)}
        assert min(by_state.values())>1,('State predicts response',key,by_state)
        report.append({'recognizable_profile':str(key),'records':len(rows2),'answer_vectors':len(answers),
          'correct_counts':dict(counts),'best_constant_answer_successes':max(answers.values()),
          'best_constant_position_successes':max(positions.values()),'attempts':len(rows2),
          'uniform_response_baseline':1/(7 if key[-1]==3 else 5),'answers_by_matrix_status':by_state})
    return report

def main():
    replays=[]; rows=[]; controls=[]
    for sid,old in g.CASES.items():
        r=g.generate(template=sid,parameters={'premise':'replay'});decode(r)
        q=r['question']
        assert q[':question/problem']==g.normalize_prose(old[':question/problem'])
        expected=old[':question/worked-solution']
        if sid=='q-141342':expected=expected.replace(g.ORIGINAL+',$ then',r'\text{nullity}(A)\ne 0,$ then')
        assert q[':question/worked-solution']==g.normalize_prose(expected)
        assert len(q[':question/answer-fields'])==len(old[':question/answer-fields'])
        for f,of in zip(q[':question/answer-fields'],old[':question/answer-fields']):
            assert f[':answer-field/key']==of[':answer-field/key']
            assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
            assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
        replays.append(r)
        hyps=g.hypothesis_concepts(sid)
        # Cover each outcome in both rule cases; cycle all noncopying hypotheses.
        for index,bits in enumerate(g.masks(sid)):
            for state in (False,True):
                p={'premise':'decision','invertible':state,'hypothesis':hyps[index%len(hyps)],'truths':bits}
                rows.append(g.generate(seed=index,template=sid,parameters=p))
        bits=g.masks(sid)[0]
        # Controlled status change, same proposition polarity: complements keys.
        # Radio source banks may not contain the complement; use legal polarity changes there.
        base={'premise':'decision','invertible':True,'hypothesis':hyps[0],'truths':bits}
        other={**base,'truths':g.masks(sid)[1]}
        a,b=g.generate(seed=77,template=sid,parameters=base),g.generate(seed=77,template=sid,parameters=other)
        assert decode(a)!=decode(b)
        controls.append({'type':'conclusion_polarity','before':a,'after':b})
        for hyp in hyps[1:]:
            b=g.generate(seed=77,template=sid,parameters={**base,'hypothesis':hyp})
            assert decode(a)==decode(b)
            assert [f[':answer-field/key'] for f in a['question'][':question/answer-fields']]==[f[':answer-field/key'] for f in b['question'][':question/answer-fields']]
            controls.append({'type':'equivalent_hypothesis','before':a,'after':b})
            rows.append(b)
        if g.checkbox(sid):
            nonuniform=[True,False,False]
            p={**base,'truths':nonuniform}
            a=g.generate(seed=77,template=sid,parameters=p)
            b=g.generate(seed=77,template=sid,parameters={**p,'invertible':False,'truths':[not v for v in nonuniform]})
            assert [f[':answer-field/key'] for f in a['question'][':question/answer-fields']]==[f[':answer-field/key'] for f in b['question'][':question/answer-fields']]
            assert decode(a)==tuple(not x for x in decode(b))
            controls.append({'type':'hypothesis_status_same_conclusions','before':a,'after':b})
    # Prior changed-premise coverage is retained and independently checked.
    legacy=[]
    old=json.loads((ROOT/'17592186124629/source.json').read_text())
    for sid in ('q-142475','q-79334','q-141341'):
        original=next(q for q in old[':knowledge-point/questions'] if q[':question/math-academy-id']==sid)
        tail=original[':question/problem'].split('Which of the following')[1]
        tokens={'nonzero-determinant':'det(A)','full-rank':r'\text{rank}(A)','trivial-null-space':r'\text{Null}(A)','full-column-space':r'\text{Col}(A)','full-column-dimension':r'\text{dim(Col}(A))'}
        for name in g.PREMISES:
            if name not in tokens or tokens[name] not in tail:
                legacy.append(g.generate(template=sid,parameters={'premise':name}))
    for r in rows+legacy:decode(r)
    for control in controls:
        rows.extend([control['before'],control['after']])
    # Semantic evidence is deduplicated by visible prompt and field labels, never seeds or UUIDs.
    unique={}
    for r in rows:
        q=r['question'];key=(q[':question/problem'],tuple(f[':answer-field/key'] for f in q[':question/answer-fields']))
        unique.setdefault(key,r)
    rows=list(unique.values())
    before=cues(rows)
    save('source-replays.json',replays);save('test-records.json',rows);save('legacy-premise-records.json',legacy);save('counterfactuals.json',controls)
    save('source-replay-report.json',{'status':'pass','complete_banks':len(replays),'source_total':16,
      'choices_matched':sum(len(f[':answer-field/choices']) for r in replays for f in r['question'][':question/answer-fields']),
      'corrected_solution':'q-141342 three premise quotations','excluded':g.EXCLUDED})
    checks=[{'label':r['generation']['template']+' '+str(i),'record':r,'checks':native_checks(r)} for i,r in enumerate(replays+rows+legacy)]
    save('native-input.json',checks)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'native-input.json'),str(E/'native-report.json')],check=True,stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/'test-records.json'),
      '--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),
      '--difficulty','moderate','--output',str(E/'delivery'),'--math-root','/media/jake/SSD/EDB/math'],check=True,stdout=subprocess.DEVNULL)
    accepted=json.loads((E/'delivery/accepted.json').read_text())
    after=cues(accepted)
    save('pedagogical-variation.json',{'status':'pass','before_filter':before,'after_filter':after,
      'counterfactuals':dict(collections.Counter(c['type'] for c in controls)),
      'semantic_records_before':len(rows),'semantic_records_accepted':len(accepted),
      'generator_rejection':'Explicit invalid parameters and unsupported difficulty raise ValueError; empty checkbox mask is excluded before shared policy.',
      'learner_selection':'Read question_selection.rs: difficulty-first hashed draw from candidate bands; seen tasks removed upstream. No profile/key filtering in select. Live learner state and policy weights not exercised.'})
    for level in ('easy','hard'):
        try:g.batch(level)
        except ValueError:pass
        else:raise AssertionError('unsupported band')
    sid='q-142475';p={**g.domain(sid)[0],'truths':[False,False,False]}
    try:g.generate(template=sid,parameters=p)
    except ValueError:pass
    else:raise AssertionError('empty checkbox accepted')
    assert g.batch(count=5,seed=24629)==g.batch(count=5,seed=24629)
    save('samples.json',g.batch(count=5,seed=24629))
    render=[replays[0],replays[-1],controls[0]['before'],controls[0]['after'],next(r for r in rows if len(r['question'][':question/answer-fields'])==1)]
    save('render-records.json',render)
    save('validation.json',{'status':'pass','source_banks':len(replays),'legacy_variants':len(legacy),'independent_decision_records':len(rows),
      'native_cases':len(checks),'native_responses':sum(len(c['checks']) for c in checks),'accepted':len(accepted),
      'witnesses':'All diagonal ranks for numeric dimensions and n=1,2,5,9 for symbolic n; visible hypotheses and statements only.',
      'limitations':['Not a test of learner-specific live selection.','Symbolic dimensions tested at representative positive boundaries; universal equivalences justified in instructional account.']})
    print(json.dumps(json.loads((E/'validation.json').read_text())))

if __name__=='__main__':main()
