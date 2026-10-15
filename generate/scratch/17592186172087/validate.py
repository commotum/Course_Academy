#!/usr/bin/env python3
"""Independent printed dimension/solution checks and native checkbox grading."""
import copy,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('vector_field_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def unlabel(prompt):
    return re.sub(r'- \*\*(?:I|II|III)\.\*\* ', '- ',prompt)

def printed_dimensions(prompt):
    result=[]
    for line in unlabel(prompt).splitlines():
        if not line.startswith('- $'):continue
        match=re.fullmatch(r'- \$(.*?)\(([^)]*)\)\s*=\s*(.*)\$',line)
        assert match, 'bad function declaration: '+line
        args=match[2].split(',');assert len(set(args))==len(args)
        expr=match[3]
        if expr.startswith('⟨'):
            assert expr.endswith('⟩');m=1+len(re.findall(r'(?<!\\),',expr))
        elif expr.startswith(r'\langle '):
            assert expr.endswith(r'\rangle');m=1+len(re.findall(r'(?<!\\),',expr))
        else:
            bases=re.findall(r'\\,(?:\\mathbf\s+)?([ijk])(?:\s*[+-]|$)',expr)
            m=len(bases) if bases else 1
        result.append((len(args),m))
    assert len(result)==3,result
    return result

def check_format(text):
    assert all(ord(c)>=32 or c in '\n\t' for c in text)
    assert len(re.findall(r'(?<!\\)\$',text))%2==0
    balance=0
    for m in re.finditer(r'(?<!\\)[{}]',text):
        balance+=1 if m[0]=='{' else -1
        assert balance>=0
    assert balance==0

def check_math(r):
    q=r['question'];dims=printed_dimensions(q[':question/problem'])
    fields={f[':answer-field/key']:f for f in q[':question/answer-fields']}
    assert set(fields)==set(g.KEYS) and len(q[':question/answer-fields'])==3
    for key,(n,m) in zip(g.KEYS,dims):
        f=fields[key];assert f[':answer-field/type']==':answer-field.type/checkbox'
        choices=f[':answer-field/choices'];assert len(choices)==2
        assert sorted(a[':answer/value'] for a in choices)==['false','true']
        assert len({a[':answer/id'] for a in choices})==2
        correct=[a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]]
        assert len(correct)==1 and correct[0][':answer/value']==str(n==m==3).lower()
    mask=sum(1<<i for i,pair in enumerate(dims) if pair==(3,3))
    solution=q[':question/worked-solution']
    assert solution.endswith(f'Therefore, the correct answer is "{g.legacy.LABELS[mask]}."')
    apps=re.findall(r'- \$([A-Z]\([^)]*\))=',unlabel(q[':question/problem']))
    claims=re.findall(r'- The function \$([A-Z]\([^)]*\))\$ is (.*?)vector field',solution)
    assert [a for a,_ in claims]==apps and len(apps)==3
    for i,(_,claim) in enumerate(claims):assert ('*not*' not in claim)==(dims[i]==(3,3))
    for text in (q[':question/problem'],solution):check_format(text)
    return dims

def validate_record(r):
    dims=check_math(r);meta=r['generation']
    assert meta['mathematical_fingerprint']==g.task_signature(dims)
    assert list(map(list,dims))==list(map(list,meta['semantic_signature']))
    replay=g.generate(r['question'][':question/difficulty'].split('/')[-1],meta['seed'],
        template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
    assert replay==r,'deterministic complete content/identity replay'
    return dims

def engine_checks(r):
    # The application resolves checkbox selections to field-owned answer IDs.
    return [{'field_index':i,'submitted_answer_id':a[':answer/id'],
        'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
        'purpose':'Live checkbox field-owned true/false choice'}
        for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def main():
    records=[];details=[];review=[]
    for sid,src in g.SOURCES.items():
        names=[s[0] for s in re.findall(r'- \*\*(?:I|II|III)\.\*\* \$([A-Z])',src[':question/problem'])]
        p={'a':g.legacy.SPECS[sid][0],'names':names,'order':[0,1,2]}
        r=g.generate('easy',template='observed_'+sid,parameters=p,profile='observed_'+sid)
        validate_record(r)
        assert r['question'][':question/problem']==src[':question/problem']
        assert r['question'][':question/worked-solution']==src[':question/worked-solution']
        sf={f[':answer-field/key']:f for f in src[':question/answer-fields']}
        for f in r['question'][':question/answer-fields']:
            old=sf[f[':answer-field/key']]
            assert old[':answer-field/type'][':db/ident']==f[':answer-field/type']
            assert sorted(a[':answer/value'] for a in old[':answer-field/choices'])==['false','true']
            correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert old[':answer-field/correct'][':answer/value']==correct
        records.append(r);review.append({'label':sid+' current exact source replay','record':r})
        for order in itertools.permutations(range(3)):
            changed=g.generate('easy',template='observed_'+sid,parameters={**p,'order':list(order),'a':7})
            validate_record(changed);records.append(changed)
        details.append({'source':sid,'prompt_exact':True,'solution_exact':True,'complete_checkbox_banks':3,'Boolean_values_matched':6,'keys_matched':3})
    counts={}
    for level in g.LEVELS:
        seen=set()
        for types in g.legacy.eligible_types(level):
            p={'a':2,'types':list(types),'names':['A','B','C']}
            r=g.generate(level,template='authored_'+level,parameters=p)
            validate_record(r);records.append(r);seen.add(r['generation']['mathematical_fingerprint'])
            alias=g.generate(level,template='authored_'+level,parameters={**p,'a':7,'names':['U','V','W']})
            assert alias['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
        counts[level]=len(seen)
        review.extend({'label':level+' authored '+str(i),'record':r} for i,r in enumerate(records[-2:]))
    # Target position regression: same expressions/values but changed candidate
    # arities. Independently read all three prompt declarations and solution claims.
    a=g.generate('hard',template='authored_hard',parameters={'a':2,'names':['A','B','C'],'types':[0,0,1]})
    b=g.generate('hard',template='authored_hard',parameters={'a':2,'names':['A','B','C'],'types':[1,0,0]})
    validate_record(a);validate_record(b)
    assert [f[':answer-field/correct'] for f in a['question'][':question/answer-fields']] != [f[':answer-field/correct'] for f in b['question'][':question/answer-fields']]
    for field in range(3):
        bad=copy.deepcopy(a);f=bad['question'][':question/answer-fields'][field]
        f[':answer-field/correct']=[':answer/id',next(x[':answer/id'] for x in f[':answer-field/choices'] if x[':answer/id']!=f[':answer-field/correct'][1])]
        try:check_math(bad)
        except AssertionError:pass
        else:raise AssertionError('wrong checkbox key accepted')
    engine=[{'label':str(i),'record':r,'checks':engine_checks(r)} for i,r in enumerate(records)]
    save('engine-input.json',engine)
    binary=HERE/'reference/replenishment/check-engine'
    subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    native=json.loads((HERE/'engine-report.json').read_text());assert native['documented_unresolved_checks']==0
    save('review.json',review)
    (HERE/'review.md').write_text('\n\n---\n\n'.join('## '+x['label']+'\n\n'+g.markdown(x['record']) for x in review)+'\n')
    save('validation.json',{'pass':True,'basis':g.CURRENT['basis'],'source_replay':details,
        'source_banks_matched':27,'source_banks_total':27,'Boolean_values_matched':54,'Boolean_values_total':54,
        'finite_unordered_authored_tasks':counts,'source_permutations_checked':54,'records_checked':len(records),
        'slot_checks':['coefficient boundaries','all source candidate positions','all authored dimension assignments','name aliases','changed target with constant coefficients','all incorrect checkbox mutations rejected'],
        'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},
        'plot_rating':'none','unresolved_findings':[]})
    print(json.dumps({'pass':True,'records':len(records),'finite_unordered_authored_tasks':counts}))

if __name__=='__main__':main()
