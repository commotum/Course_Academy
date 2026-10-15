"""Finite same-method domain counts, independently read from printed functions.

Letter/target swaps, seeds, option order and bank aliases are excluded. Enumerates
complete banks with exact rational arithmetic or exact symbolic zero tests.
"""
import sys
sys.dont_write_bytecode=True
import hashlib,importlib.util,itertools,json
from pathlib import Path
import sympy as S
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import texmath as tm
sp=importlib.util.spec_from_file_location('partial_enum',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
counts={}
for key,f in g.FAMILIES.items():
    total=eligible=rejected=0;objects=set();ratio_tests=0
    for N,M in itertools.product(f['ns'],f['ms']):
        base=None
        for U,V in itertools.product(*f['coords']):
            try:base=g.generate(f['level'],template=key,parameters={'a':1,'b':1,'n':N,'m':M,'U':str(U),'V':str(V),'target':f['target']});break
            except ValueError as exc:assert 'collision' in str(exc)
        assert base is not None
        fun,target,unused=tm.prompt(base['question'][':question/problem']);terms=fun.as_ordered_terms();assert len(terms)==2
        dt=[S.diff(z,target) for z in terms];held=tm.SYMBOLS['y' if str(target)=='x' else 'x']
        # Source order is irrelevant to this symmetric complete method bank.
        for U,V in itertools.product(*f['coords']):
            point={target:U,held:V};Q1,Q2=[S.simplify(z.subs(point)) for z in dt]
            ratio=S.simplify(Q1/Q2) if Q2!=0 else None
            for A,B in itertools.product(range(1,5),repeat=2):
                total+=1
                if Q1==0 or Q2==0:rejected+=1;continue
                eligible_pair=True
                for k in (S.Integer(1),S.Integer(2),S.Rational(1,2)):
                    difference=S.simplify(ratio*A/B-k);ratio_tests+=1
                    if difference==0:eligible_pair=False;break
                    assert difference.is_zero is False,('Unresolved exact domain inequality',key,difference)
                if not eligible_pair:rejected+=1;continue
                eligible+=1
                # A/B multiply whichever two displayed terms the parser reads.
                # Both cover the same full 1..4 coefficient domain, preserving
                # candidate counts without assuming source term ordering.
                obj=S.srepr(A*terms[0]+B*terms[1])+'@'+S.srepr(U)+','+S.srepr(V)
                objects.add(hashlib.sha256(obj.encode()).hexdigest())
    assert eligible==len(objects)
    counts[key]={'candidate_role_tasks':total,'eligible_meaningful_tasks':eligible,'whole_bank_collision_or_zero_rejections':rejected,'exact_ratio_inequalities':ratio_tests,'target_aliases_counted':False,'source_bank_aliases_counted':False}
    print(key,eligible,'/',total,flush=True)
(D/'finite-domain-counts.json').write_text(json.dumps({'method':'Independently parse each displayed function at each exponent structure; differentiate its two terms; enumerate coefficients and role-coordinate inputs. Exact zero tests reject complete banks when t1=0, t2=0, t1=t2, t1=2t2 or t2=2t1. Source/target/profile/order aliases excluded.','families':counts,'total_eligible_tasks':sum(z['eligible_meaningful_tasks'] for z in counts.values())},indent=2)+'\n')
