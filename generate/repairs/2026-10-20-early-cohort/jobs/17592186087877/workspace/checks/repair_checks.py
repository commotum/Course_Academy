"""Executable current-generator regressions and independent printed-record checks."""
import collections,json,pathlib,sys
import audit as A
import source_validator as V
E=A.PKG/'evidence';E.mkdir(exist_ok=True)
def save(n,v):(E/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def correct_value(r):return next(a[':answer/value'] for a in A.field(r)[':answer-field/choices'] if a[':answer/id']==A.key(r))
def bank(r):return sorted(a[':answer/value'] for a in A.field(r)[':answer-field/choices'])
def exponent(r,a):
    left=A.clean(a[':answer/value']).split('=')[0]
    return A.S.simplify(A.scalar(left[len('\\frac{d}{dx}'):])/A.Y).args[0]/A.X

def probes(rows):
    report=[]
    for t in sorted({r['generation']['template'] for r in rows}):
        rs=[r for r in rows if r['generation']['template']==t]
        counts=collections.Counter(next(i for i,a in enumerate(A.field(r)[':answer-field/choices']) if a[':answer/id']==A.key(r)) for r in rs)
        strategies={'double_exponent':0,'smallest_abs':0,'largest_abs':0,'smallest_signed':0,'largest_signed':0}
        for r in rs:
            choices=A.field(r)[':answer-field/choices']; cs=[(a[':answer/id'],exponent(r,a)) for a in choices]
            strategies['double_exponent']+=A.shortcut(r)==A.key(r)
            for n,fn,which in [('smallest_abs',abs,min),('largest_abs',abs,max),('smallest_signed',lambda x:x,min),('largest_signed',lambda x:x,max)]:
                extreme=which(fn(c) for _,c in cs);ids=[aid for aid,c in cs if fn(c)==extreme]
                strategies[n]+=len(ids)==1 and ids[0]==A.key(r)
        report.append({'template':t,'n':len(rs),'position_counts':dict(counts),'bank_only_successes':strategies})
    return report

def main():
    rows=[];orbits=[]
    # Each of five factors becomes correct with the entire visible bank held fixed.
    coeffs=['-2','-1','1/2','1','2']
    for t in ['constant_cos','scaled_constant_power','signed_constant_power','constant_exp']:
        orbit=[]
        for a in coeffs:
            p={'a':a,**({'b':2,'c':-2} if t=='constant_exp' else {'b':2} if t=='constant_cos' else {'n':2})}
            r=A.G.generate('easy',8173,template=t,parameters=p,bank_coefficients=coeffs)
            A.math_check(r);V.verify_record(r)
            orbit.append(r)
        assert len({tuple(bank(r)) for r in orbit})==1
        assert len({correct_value(r) for r in orbit})==5
        # Thus every bank-only selection fails on at least four members.
        assert sum(A.shortcut(r)==A.key(r) for r in orbit)<=1
        assert len({r['question'][':question/worked-solution'] for r in orbit})==5
        orbits.append({'template':t,'same_bank':True,'distinct_correct_equations':5,'distinct_solutions':5})
        rows+=orbit
    # Exact original +/-1 failure, without the optional controlled bank argument.
    exact=[A.G.generate('easy',8173,template='signed_constant_power',parameters={'a':a,'n':2}) for a in ['1','-1']]
    assert not all(A.shortcut(r)==A.key(r) for r in exact)
    for r in exact:A.math_check(r)
    save('exact-counterexamples-repaired.json',exact)
    for t in ['constant_cos','scaled_constant_power','signed_constant_power','constant_exp']:
        for seed in [310,311,312]:
            r=A.G.generate('easy',seed,template=t);A.math_check(r);V.verify_record(r);rows.append(r)
            assert r==A.G.generate('easy',seed,template=t)
    base=rows[0]
    other=A.G.generate('easy',8193,template='constant_cos',parameters=base['generation']['parameters'],bank_coefficients=coeffs)
    assert bank(other)==bank(base) and correct_value(other)==correct_value(base)
    assert other['question'][':question/id']==base['question'][':question/id']
    rows.append(other)
    canonical=A.G.generate('easy',19073,template='constant_exp',parameters={'a':'2','b':2,'c':-2})
    assert A.S.simplify(A.normalized(A.prompt_equation(canonical)[1])-(A.V+2*A.Y-2*A.S.exp(-2*A.X)))==0
    A.math_check(canonical);V.verify_record(canonical);rows.append(canonical)
    # Only affected easy boundaries, plus one sample of each preserved family.
    for a in ['-4','4','-11/3','11/3']:
        r=A.G.generate('easy',914,template='constant_exp',parameters={'a':a,'b':-4,'c':4});A.math_check(r);rows.append(r)
    preserved=[]
    for t,(level,_) in A.G.TEMPLATES.items():
        if level!='easy':
            r=A.G.generate(level,31,template=t);A.math_check(r);preserved.append(r)
    raw=[];source_results=[]
    for source_id,t,p in A.G.CASES:
        r=A.G.generate(A.G.TEMPLATES[t][0],11,t,parameters=p,profile='observed_raw');V.verify_record(r,True)
        original=A.G.QUESTIONS[source_id]; f=original[':question/answer-fields'][0]
        available=list(A.field(r)[':answer-field/choices'])
        for a in f[':answer-field/choices']:
            if 'dx^{2}' in A.clean(a[':answer/value']):match=next(b for b in available if 'dx^{2}' in b[':answer/value'])
            else:match=next(b for b in available if V.same_equation(V.relation(a[':answer/value']),V.relation(b[':answer/value'])))
            available.remove(match)
        assert not available
        if ':answer-field/correct' in f:assert V.same_equation(V.relation(f[':answer-field/correct'][':answer/value']),V.relation(correct_value(r)))
        if ':question/worked-solution' in original:assert V.prose(original[':question/worked-solution'])==V.prose(r['question'][':question/worked-solution'])
        source_results.append({'source':original[':question/id'],'bank_choices_matched':5,'source_level':original.get(':question/difficulty'),'passed':True});raw.append(r)
    save('source-replay-records.json',raw);save('source-replay-results.json',source_results)
    save('records.json',rows);save('preserved-records.json',preserved)
    save('pedagogical-variation.json',{'orbits':orbits,'probes':probes(rows),'semantic_instances':len({r['generation']['mathematical_fingerprint'] for r in rows}),'irrelevant_shuffle_preserves_answer':True,'source_banks':len(raw),'math_checked':len(rows)+len(preserved)+len(raw),'same_bank_argument':'For each template all five different coefficients P share exactly the same complete bank and Q, with five different correct equations. No bank-only property can distinguish those keys.'})
    cases=[]
    for r in rows+preserved:
        cases.append({'label':r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==A.key(r) else 'rejected','purpose':'Independent normalized printed-equation equivalence'} for a in A.field(r)[':answer-field/choices']]})
    save('grader-input.json',cases)
    save('render-input.json',[rows[0],rows[4],rows[7],rows[12],canonical])
    print(json.dumps({'source_banks':len(raw),'source_choices':len(raw)*5,'easy_records':len(rows),'preserved_samples':len(preserved),'five_target_orbits':len(orbits),'native_cases_prepared':len(cases)*5}))
if __name__=='__main__':main()
