"""Executable retained findings; inspect visible equations, not recipe labels.

Run from any directory: <job-python> -B checks/repair.py
Optionally audit an actual filtered JSON array with --records FILE.
All writes are evidence; runtime package files are never modified.
"""
import argparse, collections, importlib.util, json, re, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent.parent / 'workspace'
E = Path(__file__).resolve().parent / 'author-check-rerun'
E.mkdir(exist_ok=True)
s = importlib.util.spec_from_file_location('generator', W/'17592186124674.py')
g = importlib.util.module_from_spec(s)
s.loader.exec_module(g)
trans = standard_transformations + (implicit_multiplication_application,)

def save(name, data):
    (E/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')

def field(r): return r['question'][':question/answer-fields'][0]
def choices(r): return field(r)[':answer-field/choices']
def key(r): return field(r)[':answer-field/correct'][1]
def answer(r): return next(c[':answer/value'] for c in choices(r) if c[':answer/id']==key(r))
def clean(t): return re.sub(r'\s+', '', t.replace('\\\\', '\\'))
def rhs(value):
    t=value.replace('\\\\','\\').split('=',1)[1]
    t=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
    t=t.replace('{','(').replace('}',')').replace('^','**')
    return sp.expand(parse_expr(t, local_dict={c:sp.Symbol(c) for c in 'kNMTBCPVRSFH'}, transformations=trans))

def witness(r):
    q=r['question']; prompt=q[':question/problem']
    symbol=re.search(r'\$([A-Z])\(t\)\$',prompt)[1]
    cap=int(re.search(r'(?:maximum.+?is|maximum capacity is) \$(\d+)\$',prompt)[1])
    X=sp.Symbol(symbol); k=sp.Symbol('k'); target=k*(cap-X)
    expr=[rhs(c[':answer/value']) for c in choices(r)]
    matches=[c[':answer/id'] for c,e in zip(choices(r),expr) if sp.expand(e-target)==0]
    assert matches==[key(r)], (q[':question/id'],matches,cap)
    assert len(set(expr))==5
    assert str(cap)+'-'+symbol in clean(q[':question/worked-solution'])
    # The shared derivative is part of each whole-equation answer.
    assert all(symbol in c[':answer/value'].split('=')[0] for c in choices(r))
    return {'question_id':q[':question/id'],'capacity':cap,'symbol':symbol,'correct':answer(r)}

def probes(records):
    groups=collections.defaultdict(list)
    for r in records:
        vals=[c[':answer/value'] for c in choices(r)]
        lengths=[len(clean(v)) for v in vals]
        eq=[rhs(v) for v in vals]
        # Identify eligible positive linear gaps from the visible bank.
        X=sp.Symbol(re.search(r'\$([A-Z])\(t\)\$',r['question'][':question/problem'])[1]);k=sp.Symbol('k')
        linear=[i for i,e in enumerate(eq) if sp.expand(e).coeff(X)==-k and sp.degree(e,X)==1 and e.subs(X,0)/k>0]
        caps=[int(sp.expand(eq[i]).subs(X,0)/k) for i in linear]
        rank=sorted(caps).index(caps[linear.index(next(i for i,c in enumerate(choices(r)) if c[':answer/id']==key(r)))])
        correct_i=next(i for i,c in enumerate(choices(r)) if c[':answer/id']==key(r))
        group=(r['generation']['template'],'capacities' if len(linear)==5 else 'mixed')
        groups[group].append({'lengths':lengths,'position':correct_i,'rank':rank,
            'unique_shortest':lengths.count(min(lengths))==1 and lengths[correct_i]==min(lengths),
            'unique_longest':lengths.count(max(lengths))==1 and lengths[correct_i]==max(lengths),
            'shortest_first':correct_i==min(range(5),key=lambda i:lengths[i]),
            'longest_first':correct_i==max(range(5),key=lambda i:lengths[i])})
    out=[]
    for (template,kind),rows in groups.items():
        n=len(rows)
        result={'template':template,'bank_kind':kind,'count':n,'chance':0.2,
          'chance_after_identifying_linear_form':1/(5 if kind=='capacities' else 3),
          'positions':dict(collections.Counter(x['position'] for x in rows)),
          'eligible_capacity_ranks':dict(collections.Counter(x['rank'] for x in rows)),
          **{name:sum(x[name] for x in rows) for name in ('unique_shortest','unique_longest','shortest_first','longest_first')}}
        # Strict original shortcut: never a uniquely shortest correct normal item.
        assert result['unique_shortest']==0, result
        if n>=3:
            assert max(result['positions'].values())<n, result
            assert max(result['eligible_capacity_ranks'].values())<n, result
        out.append(result)
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--records');p.add_argument('--output',default='filtered-variation.json');a=p.parse_args()
    if a.records:
        records=json.loads(Path(a.records).read_text())
        assert records
        maths=[witness(r) for r in records]
        report={'input':a.records,'count':len(records),'groups':probes(records),'math':maths}
        save(a.output,report)
        print(json.dumps({'filtered_count':len(records),'groups':len(report['groups']),'passed':True}))
        return
    # Both exact retained counterexamples are tested against current code.
    minimal=g.generate_easy(seed=88,parameters={'context':'deer','capacity':20})
    fixed60=g.generate_easy(seed=624,template='source_17592186308739',parameters={'capacity':60,'initial':10})
    witness(minimal);witness(fixed60)
    assert not fixed60['generation']['evidence_only']
    controlled=[];pairs=[]
    # Every normal source context, plus both direct-model profiles. Each fixed bank
    # is reassigned across EVERY eligible answer-bearing capacity.
    templates=['direct_model',*g.LEARNING_SOURCES]
    for template in templates:
        seeds=[88,3] if template=='direct_model' else [624]
        for seed in seeds:
            base=g.generate_easy(seed=seed,template=template)
            X=sp.Symbol(base['generation']['symbol']);k=sp.Symbol('k')
            linear_count=sum(bool(sp.degree(rhs(c[':answer/value']),X)==1 and sp.expand(rhs(c[':answer/value'])).coeff(X)==-k and rhs(c[':answer/value']).subs(X,0)/k>0) for c in choices(base))
            eligible=[0,2,4] if linear_count==3 else list(range(5))
            bank=[30,45,60,75,95]
            group=[]
            for i in eligible:
                params={'capacity':bank[i],'candidates':bank,'target_rank':i,'linear_indices':eligible}
                if template=='direct_model':params['context']='deer'
                elif g.LEARNING_SOURCES[template]['initial'] is not None:params['initial']=10
                r=g.generate_easy(seed=seed,template=template,parameters=params)
                group.append(r);controlled.append(r)
            assert len({answer(r) for r in group})==linear_count
            assert len({tuple(sorted(c[':answer/value'] for c in choices(r))) for r in group})==1
            assert len({r['question'][':question/problem'] for r in group})==linear_count
            assert len({r['question'][':question/worked-solution'] for r in group})==linear_count
    # Exact reviewer fixed-bank pair: hold all source capacities fixed, 95 -> 60.
    for A in (95,60):
        pairs.append(g.generate_easy(seed=624,template='source_17592186308739',parameters={'capacity':A,'initial':10,'candidates':[95,30,60,100,950]}))
    assert answer(pairs[0])!=answer(pairs[1])
    assert sorted(c[':answer/value'] for c in choices(pairs[0]))==sorted(c[':answer/value'] for c in choices(pairs[1]))
    irrelevant=g.generate_easy(seed=624,template='source_17592186308739',parameters={**pairs[1]['generation']['parameters'],'initial':20})
    assert answer(irrelevant)==answer(pairs[1])
    assert irrelevant['question'][':question/worked-solution']==pairs[1]['question'][':question/worked-solution']
    assert sorted(c[':answer/value'] for c in choices(irrelevant))==sorted(c[':answer/value'] for c in choices(pairs[1]))
    # Small fresh default sample; normal branch must deliver competing capacities.
    fresh=[g.generate_easy(seed=i) for i in range(48371,48411)]
    for r in fresh:
        meta=r['generation']
        assert g.generate_easy(seed=meta['seed'],template=meta['template'],parameters=meta['parameters'])==r
    assert any(len({str(rhs(c[':answer/value'])).split('-')[0] for c in choices(r)})>1 for r in fresh)
    assert any(r['generation']['template'] in g.LEARNING_SOURCES and g.LEARNING_SOURCES[r['generation']['template']]['initial'] is not None for r in fresh)
    assert {r['generation']['bank_kind'] for r in fresh}=={'mixed','capacities'}
    # Context catalog and capacity boundaries; no extra source methods.
    boundaries=[g.generate_easy(seed=88,parameters={'context':context,'capacity':A}) for context,A in zip(g.CONTEXTS,(20,99,100,499,500))]
    invalid=[]
    for cap in (19,501,True):
        try:g.generate_easy(seed=88,parameters={'context':'deer','capacity':cap})
        except ValueError:invalid.append(cap)
        else:raise AssertionError(('unexpected acceptance',cap))
    for A in (10,99,100,5000):
        witness(g.generate_easy(seed=624,template='source_17592186308739',parameters={'capacity':A,'initial':1}))
    records=[minimal,fixed60]+controlled+pairs+[irrelevant]+fresh+boundaries
    maths=[witness(r) for r in records]
    save('regression-records.json',records)
    save('fresh-records.json',fresh)
    save('counterfactual-records.json',pairs+[irrelevant])
    save('render-records.json',[next(r for r in fresh if r['generation']['bank_kind']=='mixed'),pairs[0],pairs[1]])
    # Separate controlled groups remove stochastic small-group ambiguity.
    variation=probes(controlled)
    save('pedagogical-variation.json',{'controlled':variation,'fresh':probes(fresh),'exact_minimal':probes([minimal]),'pairs':'counterfactual-records.json','semantic_models':len({x['capacity'] for x in maths}),'normal_sampler_rejection':'Constructive sampling: no rejection loop; explicit invalid calls raise ValueError.','limitations':'Cue probes are finite, not a proof against every strategy. Structure elimination in mixed banks exercises the lesson but leaves three competing equilibrium capacities.'})
    save('math-results.json',{'passed':True,'count':len(maths),'cases':maths,'invalid_parameters_rejected':invalid})
    # Native checks are selected using independent visible-equation witnesses.
    grader=[]
    for index,r in enumerate([minimal,fixed60]+controlled+pairs+[irrelevant]+fresh[:5]):
        w=witness(r)
        grader.append({'label':f'easy {index} capacity {w["capacity"]}','record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/value']==w['correct'] else 'rejected','purpose':'visible equilibrium and complete equation independently checked'} for c in choices(r)]})
    save('grader-input.json',grader)
    save('regression-results.json',{'passed':True,'finding_ids':['4063419ca27213935be7','8eb8b8ca4774f2a7305b'],'tested_records':len(records),'controlled_records':len(controlled),'fresh_records':len(fresh),'command':'<job-python> -B checks/repair.py'})
    print(json.dumps({'passed':True,'records':len(records),'controlled':len(controlled),'fresh':len(fresh)}))

if __name__=='__main__':main()
