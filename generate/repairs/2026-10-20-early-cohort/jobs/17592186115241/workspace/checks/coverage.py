"""Count semantic solution sets and pivot/zero/constant roles from visible math."""
import collections,json,sys
sys.dont_write_bytecode=True
from validate_repair import E,dump
from witness import system,vec,field,correct,sp,v
fresh=json.load(open(E/'fresh.json'));out={}
for name in sorted({r['generation']['template'] for r in fresh}):
    group=[r for r in fresh if r['generation']['template']==name]
    profiles=collections.Counter();signs=collections.Counter();semantic=set()
    for r in group:
        M=system(r['question'][':question/problem']);R,piv=M.rref()
        fc=next(j for j in range(M.cols-1) if j not in piv)
        vv=next(vec(c[':answer/value']) for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r))
        semantic.add(str(R.tolist()))
        const=tuple(j for j in piv if sp.diff(vv[j],v[fc])==0)
        zero=tuple(j for j in piv if vv[j].subs(v[fc],0)==0)
        profiles[str({'pivots':piv,'free':fc,'constant_basic':const,'zero_intercept':zero})]+=1
        signs[str(tuple(int(sp.sign(sp.diff(vv[j],v[fc]))) for j in piv))]+=1
    out[name]={'records':len(group),'distinct_solution_sets':len(semantic),'assignment_profiles':dict(profiles),'slope_sign_profiles':dict(signs)}
dump('coverage.json',{'by_template':out,'semantic_total':sum(x['distinct_solution_sets'] for x in out.values()),'limits':['Semantic counts ignore row mixing and UUIDs.','Easy integer entries are bounded by 42 under the existing 48 limit; distinct coordinate pools prevent bank collisions. No easy decision case is removed by the bank-validity rule.','Original banks are retained for explicit source replay; ordinary source-profile and default sampling use repaired banks.','Normal rank-one cases have a nonconstant basic coordinate so solving in the parameter remains necessary; explicit zero slopes are legal.','Live learner history, policy weights, and future entity IDs are unavailable.']})
print(json.dumps({'records':len(fresh),'semantic_solution_sets':sum(x['distinct_solution_sets'] for x in out.values()),'templates':len(out)}))
