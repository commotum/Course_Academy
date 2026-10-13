"""Printed-math checks, exhaustive bounded bank replay, and actual grading."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE));import printed as p
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def check(rec):
    q=rec['question'];meta=rec['generation'];t=meta['template'];m=meta['parameters']['m']
    assert g.generate(g.DATA[t][0],meta['seed'],t,{'m':m})==rec
    f,lo,hi=p.integral(q[':question/problem']);N,g1,g2,elo,ehi,A,B,a,b,F,answer=g.math_data(t,m)
    assert sp.cancel(f-N/(g1*g2))==0 and (lo,hi)==(elo,ehi)
    assert lo<hi
    roots=sp.solve(sp.denom(sp.cancel(f)),p.x)
    assert len(roots)==2 and all(not lo<=r<=hi for r in roots),(t,'pole crossing')
    # Residues derived independently from printed rational function.
    independent=sp.apart(f,p.x);primitive=sp.integrate(independent,p.x)
    assert sp.cancel(sp.diff(primitive,p.x)-f)==0
    expected=0
    for r in roots:
        residue=sp.simplify(sp.limit((p.x-r)*f,p.x,r))
        expected+=residue*sp.log(abs((hi-r)/(lo-r)))
    assert p.equivalent(answer,expected),(t,m,answer,expected)
    fields=q[':question/answer-fields'];assert len(fields)==1;field=fields[0];bank=field[':answer-field/choices']
    assert len(bank)==(1 if field[':answer-field/type'].endswith('/blank') else 5)
    assert ('{{field-1}}' in q[':question/problem'])==field[':answer-field/type'].endswith('/blank')
    values=[p.scalar(v[':answer/value']) for v in bank]
    for i,v in enumerate(values):
        assert p.equivalent(v,expected)==(bank[i][':answer/id']==field[':answer-field/correct'][1]),(t,m,bank[i])
        assert all(not p.equivalent(v,w) for w in values[:i]),'Equivalent options'
    assert fingerprint(q)==meta['mathematical_fingerprint']
    if m!=1 or t=='q-49766':
        # Independently read the printed factorization, identities, coefficients,
        # primitive, endpoint evaluation and final answer. Original source
        # replay solutions have a separate fidelity audit, including one typo.
        blocks=q[':question/worked-solution'].split('$$')[1::2]
        pos=0
        if g.DATA[t][-1]:
            left,right=blocks[pos].split('=');assert sp.cancel(p.scalar(left)-p.scalar(right))==0;pos+=1
        if t!='q-128238':
            initial=blocks[pos].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').strip();pos+=1
            parts=initial.split('=');assert sp.cancel(p.scalar(parts[0])-f)==0;assert sp.cancel(p.scalar(parts[1])-f)==0
            rhs=p.scalar(parts[2]);assert sp.cancel(rhs.subs({p.A:A,p.B:B})-f)==0
            left,right=blocks[pos].split('=');pos+=1
            assert sp.expand(p.scalar(left)-p.scalar(right).subs({p.A:A,p.B:B}))==0
            for _ in range(2):
                block=blocks[pos].replace(r'\begin{aligned}','').replace(r'\end{aligned}','');pos+=1
                for row in block.split(r'\\'):
                    left,right=row.replace('&','').split('=');assert sp.simplify(p.scalar(left).subs({p.A:A,p.B:B})-p.scalar(right).subs({p.A:A,p.B:B}))==0
        left,right=blocks[pos].split('=');pos+=1;assert sp.cancel(p.scalar(left)-f)==0 and sp.cancel(p.scalar(right)-f)==0
        integration=blocks[pos];pos+=1
        printed_F=p.scalar(integration.split('&=')[-1].replace(r'\end{aligned}','')).subs(p.C,0)
        # Abs logarithms differentiated piecewise off the poles.
        for point in (lo,(lo+hi)/2,hi):
            assert sp.simplify((sp.diff(printed_F,p.x)-f).subs(p.x,point))==0
        logs=blocks[pos].replace(r'\begin{aligned}','').replace(r'\end{aligned}','');pos+=1
        left,right=logs.split('&=');left=p.scalar(left).subs(p.C,0);right=p.scalar(right).subs(p.C,0)
        for point in (lo,(lo+hi)/2,hi):assert p.equivalent(left.subs(p.x,point),right.subs(p.x,point))
        endpoint=blocks[pos].replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rows=endpoint.split(r'\\')
        assert p.integral(rows[0])[1:]==(lo,hi)
        assert p.equivalent(p.scalar(rows[1].split('&=')[1]),expected)
        assert p.equivalent(p.scalar(rows[2].split('&=')[1]),expected)
    return rec

def native(label,rec):
    f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'every complete bank option'} for a in f[':answer-field/choices']]
    else:
        c=f[':answer-field/choices'][0][':answer/value']
        checks=[{'submitted':v,'expected':e,'purpose':purpose} for v,e,purpose in [(c,'accepted','canonical'),('('+c+')+0','accepted','equivalent exact'),('2('+c+')/2','accepted','unsimplified equivalent'),('('+c+')+1','rejected','wrong offset'),('('+c+')-1','rejected','wrong offset below')]]
    if f[':answer-field/type'].endswith('/blank') and rec['generation']['parameters']['m']>1:
        final=rec['question'][':question/worked-solution'].split('$$')[-2].split('&=')[-1].replace(r'\end{aligned}','').strip()
        checks.append({'submitted':final,'expected':'accepted','purpose':'printed worked-solution final value'})
    return {'label':label,'record':rec,'checks':checks}
def main():
    replays=[];inputs=[];review=[];records=[];seen=set();counts={};sources=g.sources()
    for t,old in sources.items():
        r=check(g.generate(g.DATA[t][0],0,t,{'m':1}));q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        assert q[':question/problem']==p.clean(old[':question/problem'])
        assert len(f[':answer-field/choices'])==len(of[':answer-field/choices'])
        for generated,original in zip(f[':answer-field/choices'],of[':answer-field/choices']):assert p.equivalent(p.scalar(generated[':answer/value']),p.scalar(original[':answer/value']))
        correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        if of.get(':answer-field/correct'):assert p.equivalent(p.scalar(correct[':answer/value']),p.scalar(of[':answer-field/correct'][':answer/value']))
        if old.get(':question/worked-solution') and t!='q-49761':assert q[':question/worked-solution']==old[':question/worked-solution']
        replays.append({'source':t,'profile':t if len(f[':answer-field/choices'])>1 else None,'matched_values':len(f[':answer-field/choices']),'total_values':len(of[':answer-field/choices']),'matched_distractors':len(f[':answer-field/choices'])-1,'total_distractors':len(of[':answer-field/choices'])-1,'complete_bank_matched':True,'missing_extra':[],'legacy_completion':t=='q-49766','solution_correction':t=='q-49761'})
        inputs.append(native('source-'+t,r));review.append({'label':'source '+t,'record':r});review.append({'label':'variant '+t,'record':check(g.generate(g.DATA[t][0],2,t,{'m':2}))})
    for level in ('moderate','hard'):
        count=0
        for t,params in g.candidates(level):
            r=check(g.generate(level,1,t,params));fp=fingerprint(r['question']);assert fp not in seen;seen.add(fp);count+=1;assert r['question']==g.generate(level,999,t,params)['question'];records.append(r);inputs.append(native(t+'-'+str(params['m']),r))
        counts[level]=count
    for level,t,m in [('easy','q-49764',2),('moderate','q-49764',0),('moderate','q-49764',7),('moderate','q-49764',2.5),('hard','q-49764',2)]:
        try:g.generate(level,1,t,{'m':m})
        except ValueError:pass
        else:raise AssertionError('Invalid input accepted')
    assert g.batch('moderate',3,5)==g.batch('moderate',3,5)
    for level in counts:
        try:g.batch(level,counts[level]+1,0)
        except ValueError:pass
        else:raise AssertionError('Finite limit not enforced')
    save('source-replay.json',{'passed':True,'sources':replays,'complete_banks_matched':14,'complete_banks_total':14,'matched_values':sum(r['matched_values'] for r in replays),'total_values':sum(r['total_values'] for r in replays),'matched_distractors':sum(r['matched_distractors'] for r in replays),'total_distractors':sum(r['total_distractors'] for r in replays),'missing_extra':[],'solution_fidelity':'12 solutions exact; q-49761 mixed indefinite/definite bounds corrected locally; q-49766 completed locally. Variants preserve all source instructional sentences and ordered math stages, using compact equation rows; equation-row layout is an explicit extension. Double-escaped historical prompts/banks normalized for actual rendering.'})
    save('previews.json',records);save('review.json',review);(HERE/'review.md').write_text('\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in review)+'\n')
    save('native-input.json',inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    save('capabilities.json',{'supported_levels':['moderate','hard'],'bounded_distinct_tasks':counts,'policy':'Positive amplitude m=2..6; m=1 exact source-bank replay. Poles, endpoints, denominator form and complete bank preserved. Local unrated q-49766 completion conservatively moderate; no source modifications.','exceptions':[{'difficulty':'easy','status':'unsupported','unfilled_reserve':5,'evidence':'14 sources at basis 1978: five moderate, eight hard and one unrated. No easy bank or worked solution. This bounded generator implements only observed workloads; absence is not proof of impossibility. New source evidence reopens classification.'}],'unsupported_levels_filled':False})
    files=[HERE.with_suffix('.py'),HERE/'source.json',HERE/'printed.py',HERE/'validate.py',HERE/'check-engine.rs',HERE/'check-engine',ROOT/'target/debug/libcourse_academy_engine.rlib']
    save('validation.json',{'passed':True,'counts':counts,'exhaustive_distinct_instances':len(seen),'printed_math':'Printed integrands/bounds parsed independently; independent residues, derivative, pole checks, all options, factorization, identities, coefficient equations, primitive, logarithm combination, endpoint values and final answer checked.','native_grading':'All 14 source replays and all 70 bounded variants through learning::grade_field; every radio option; canonical, two equivalent and two incorrect blank probes (offset above and below).','hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}})
    print('Validated',counts)
if __name__=='__main__':main()
