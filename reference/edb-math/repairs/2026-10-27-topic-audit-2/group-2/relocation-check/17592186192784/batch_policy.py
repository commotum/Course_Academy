"""Deterministic bank-cue checks at the CLI batch boundary.

Math construction remains unrestricted: valid signs, cancellations and target roles
are retained. Rejection changes error profiles/instances, never the mathematical
rule or key. A singleton is not evidence of a shared subgroup strategy.
"""
from collections import Counter, defaultdict
from itertools import combinations
import sympy as s


def shortcuts(records):
    groups = defaultdict(list)
    for r in records:
        m = r['generation']; xs = s.symbols('x y z', real=True)
        local = dict(zip(('x','y','z'), xs))
        bank = [s.sympify(v, locals=local) for v in m['bank_expressions']]
        f = r['question'][':question/answer-fields'][0]
        cs = f[':answer-field/choices']; correct = f[':answer-field/correct'][1]
        key = next(i for i,c in enumerate(cs) if c[':answer/id'] == correct)
        vals = [float(v.subs(dict(zip(xs,[s.Rational(2,3),s.Rational(3,4),s.Rational(4,5)]))).evalf()) for v in bank]
        ranks = sorted(range(5), key=lambda i:(vals[i],i))
        texts = [c[':answer/value'] for c in cs]
        cues = {**{'rank_'+str(j):ranks[j] for j in range(5)},
                'shortest':min(range(5),key=lambda i:len(texts[i])),
                'longest':max(range(5),key=lambda i:len(texts[i]))}
        for sign in [-1,1]:
            ids=[i for i,v in enumerate(vals) if sign*v>0]
            cues['unique_sign_'+str(sign)] = ids[0] if len(ids)==1 else -1
        pairs=[(i,j) for i,j in combinations(range(5),2) if bank[i]!=0 and s.expand(bank[i]+bank[j])==0]
        for sign in [-1,1]:
            cues['unique_opposite_pair_'+str(sign)] = next((i for i in pairs[0] if vals[i]*sign>0),-1) if len(pairs)==1 else -1
        feats=[(tuple(sorted(str(t.as_coeff_Mul()[0]) for t in s.Add.make_args(s.expand(b)))),tuple(sorted(str(t.args[0]) for t in b.atoms(s.sin,s.cos)))) for b in bank]
        coeff=Counter(f[0] for f in feats);args=Counter(f[1] for f in feats)
        ids=[i for i,f in enumerate(feats) if coeff[f[0]]==max(coeff.values()) and args[f[1]]==max(args.values())]
        cues['modal_coeff_arg_intersection']=ids[0] if len(ids)==1 else -1
        correct_cues={cue for cue,i in cues.items() if i==key}
        family=m['template']; names=[family, family+'/target='+m['target']]
        if family in ('power','trig_sum'): names.append(family+'/role='+str(m['role']))
        else:
            F=s.sympify(m['expression'],locals=local)
            radical=next(p.base for p in F.atoms(s.Pow) if p.exp==s.Rational(1,2))
            coefficient=s.expand(radical).coeff(local[m['target']],2)
            names.append(family+'/coefficient='+str(coefficient))
        for name in names:groups[name].append(correct_cues)
    return [{'group':name,'count':len(items),'cues':sorted(set.intersection(*items))}
            for name,items in groups.items() if len(items)>=2 and set.intersection(*items)]
