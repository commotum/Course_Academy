"""Independent printed mathematics, full source banks, real learner grading."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
import printed as p
spec=importlib.util.spec_from_file_location('linear_trig',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def expression(text):
    t=text.strip().replace(r'{\int }',r'\int')
    if r'\big|' in t:
        body,limits=t.split(r'\big|');assert limits[0]=='_';lo,j=p.group(limits,1);assert limits[j]=='^';hi,j=p.group(limits,j+1);assert j==len(limits)
        value=p.scalar(body);return sp.simplify(value.subs(p.u,p.scalar(hi))-value.subs(p.u,p.scalar(lo)))
    if r'\int' in t:
        i=t.index(r'\int');factor=p.scalar(t[:i]) if t[:i].strip() else sp.Integer(1)
        start=i+4;lo=hi=None
        if t[start:start+1]=='_':
            lo,start=p.group(t,start+1);assert t[start]=='^';hi,start=p.group(t,start+1);lo=p.scalar(lo);hi=p.scalar(hi)
        match=re.search(r'\\text\{d\}([xuz])',t[start:]);assert match,t
        variable=p.u if match[1]=='u' else p.x;body=p.scalar(t[start:start+match.start()]);tail=t[start+match.end():];assert not tail.strip(),tail
        return sp.simplify(factor*sp.integrate(body,variable if lo is None else (variable,lo,hi)))
    return p.scalar(t)
def check(rec):
    q=rec['question'];meta=rec['generation'];t=meta['template'];k=meta['parameters']['k']
    assert g.generate(g.DATA[t][0],meta['seed'],t,{'k':k})==rec
    assert rec['knowledge_point']['db_id']==g.KP_ID and meta['version']==g.VERSION
    integrand,lo,hi=p.integral(q[':question/problem']);fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];bank=f[':answer-field/choices'];indefinite=lo is None
    correct=[];values=[]
    for a in bank:
        value=p.scalar(a[':answer/value']);values.append(value)
        valid=sp.trigsimp(sp.diff(value,p.x)-integrand)==0 if indefinite else sp.simplify(value-sp.integrate(integrand,(p.x,lo,hi)))==0
        assert valid==(a[':answer/id']==f[':answer-field/correct'][1]);correct.append(valid)
    assert sum(correct)==1
    for i,a in enumerate(values):
        for b in values[:i]:assert sp.trigsimp(sp.diff(a-b,p.x))!=0 if indefinite else sp.simplify(a-b)!=0
    assert len(bank)==(1 if f[':answer-field/type'].endswith('/blank') else 5)
    assert ('{{field-1}}' in q[':question/problem'])==f[':answer-field/type'].endswith('/blank')
    if k>1 or t=='q-2204':
        # Read numerical equations from generated solution, including each
        # transformed integral, antiderivative, bound evaluation and final result.
        block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)[1]
        previous=None
        for row in block.split('\\\\'):
            l,r=row.split('&=');left=expression(l) if l.strip() else previous;right=expression(r)
            if indefinite:
                b,c=g.math_data(t,k)[3:5]
                difference=(left-right).subs(p.u,b*p.x+c)
                assert sp.trigsimp(sp.diff(difference,p.x))==0,(t,k,row)
            else:assert sp.simplify(left-right)==0,(t,k,row,left,right)
            previous=right
        # Substitution derivative and bound table are independently checked.
        assert f'$u={sp.latex((g.math_data(t,k)[3]*g.x+g.math_data(t,k)[4]).subs(g.x,sp.Symbol("z") if t=="q-2204" else g.x))},$' in q[':question/worked-solution']
    assert g.fingerprint(q)==meta['mathematical_fingerprint']
    return rec
def native(label,rec):
    f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete source-bank option grading'} for a in f[':answer-field/choices']]
    else:
        value=p.scalar(f[':answer-field/choices'][0][':answer/value'])
        canonical=f[':answer-field/choices'][0][':answer/value']
        checks=[{'submitted':v,'expected':e,'purpose':purpose} for v,e,purpose in [(canonical,'accepted','canonical LaTeX'),('('+canonical+')+0','accepted','equivalent exact scalar'),('2('+canonical+')/2','accepted','unsimplified equivalent'),('('+canonical+')+1','rejected','incorrect offset'),('-('+canonical+')','rejected','incorrect sign')]]
    return {'label':label,'record':rec,'checks':checks}
def main():
    source=g.sources();replays=[];inputs=[];review=[]
    for t,old in source.items():
        r=check(g.generate(g.DATA[t][0],0,t,{'k':1}));q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        assert q[':question/problem']==old[':question/problem']
        assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
        assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
        if of.get(':answer-field/correct'):
            chosen=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert chosen[':answer/value']==of[':answer-field/correct'][':answer/value']
        if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution']
        replays.append({'source':t,'profile':t,'matched_values':len(f[':answer-field/choices']),'total_values':len(of[':answer-field/choices']),'matched_distractors':len(f[':answer-field/choices'])-1,'total_distractors':len(of[':answer-field/choices'])-1,'complete_bank_matched':True,'missing_extra':[],'missing_marker_derived':not bool(of.get(':answer-field/correct')),'missing_solution_authored':not bool(old.get(':question/worked-solution'))})
        inputs.append(native('source-'+t,r));review.append({'label':'source '+t,'record':r})
    counts={};seen=set()
    for level in ('easy','moderate'):
        count=0
        for t,params in g.candidates(level):
            r=check(g.generate(level,1915,t,params));assert r['generation']['mathematical_fingerprint'] not in seen;seen.add(r['generation']['mathematical_fingerprint']);count+=1
            assert g.generate(level,999,t,params)['question']==r['question'];inputs.append(native(t+'-'+str(params['k']),r))
        counts[level]=count
    for level,t,k in [('hard','q-10061',2),('easy','q-10061',0),('easy','q-10061',13),('easy','q-10061',2.5),('moderate','q-10061',2)]:
        try:g.generate(level,0,t,{'k':k})
        except ValueError:pass
        else:raise AssertionError('Invalid boundary accepted')
    previews=g.batch('easy',8,1915)+g.batch('moderate',8,1915)
    for rec in previews:check(rec);review.append({'label':'variant','record':rec})
    for t in g.DATA:review.append({'label':'template variant '+t,'record':check(g.generate(g.DATA[t][0],1915,t,{'k':2}))})
    save('previews.json',previews);save('review.json',review);(HERE/'review.md').write_text('\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in review)+'\n')
    save('native-input.json',inputs)
    subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    save('source-replay.json',{'passed':True,'source_results':replays,'complete_banks_matched':7,'complete_banks_total':7,'matched_values':27,'total_values':27,'matched_distractors':20,'total_distractors':20,'fidelity':'All seven exact prompts, fields, all 27 exact source values, six supplied solutions retained. Missing q-2204 marker and solution authored locally. Variants retain solution sequence with simplified aligned structure.'})
    save('validation.json',{'passed':True,'exhaustive_distinct_instances':len(seen),'counts':counts,'printed_math':'Independent integrand/bounds, exact integration and differentiation, unique options modulo integration constants, numerical solution rows, source replay','native_grading':'Every source and bounded variant through actual learning::grade_field; canonical/equivalent/wrong blank entries and every radio option','hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'printed.py',HERE/'check-engine.rs',HERE/'check-engine',ROOT/'target/debug/libcourse_academy_engine.rlib']}})
    save('capabilities.json',{'supported_levels':['easy','moderate'],'bounded_distinct_tasks':counts,'policy':'Positive integer coordinate dilation k=2..12, exact source replay at k=1. Complete banks transported together. No arbitrary shifts/amplitudes or unobserved workload extensions. Equivalent integrands and bounds deduplicated; seed/identity/order ignored.','exceptions':[{'difficulty':'hard','status':'unsupported','unfilled_reserve':5,'evidence':'Seven sources at basis 1915: three rated easy, three rated moderate, one incomplete unrated. No hard template, bank or solution evidence. Bounded implementation supports observed workload only; new evidence reopens classification.'}],'unsupported_levels_filled':False})
    print('Validated',counts)
if __name__=='__main__':main()
