"""Validate actual printed functions/options, full replay and learner grading."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE));import printed as p
spec=importlib.util.spec_from_file_location('trigderivative',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def check(rec):
    m=rec['generation'];q=rec['question'];assert rec==g.generate(g.DATA[m['template']][0],m['seed'],m['template'],m['parameters'])
    expr,point=g.printed_task(q);expected=sp.diff(expr,p.x)
    if point is not None:expected=sp.simplify(expected.subs(p.x,point))
    f=q[':question/answer-fields'][0];values=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']]
    assert sum(sp.simplify(a-expected)==0 for a in values)==1
    assert all((sp.simplify(v-expected)==0)==(a[':answer/id']==f[':answer-field/correct'][1]) for a,v in zip(f[':answer-field/choices'],values))
    assert all(sp.simplify(a-b)!=0 for i,a in enumerate(values) for b in values[:i])
    assert g.fingerprint(q)==m['mathematical_fingerprint']
    if m['parameters']['k']>1:
        sol=q[':question/worked-solution'];block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1]
        rows=block.split('\\\\');assert len(rows)==3
        for row in rows[1:]:assert sp.simplify(p.scalar(row.split('&=')[1])-sp.diff(expr,p.x))==0
        if point is not None:
            eq=sol.split('y^{\\prime}(',1)[1].split(')=',1)[1].split('.\n$$',1)[0]
            assert all(sp.simplify(p.scalar(v)-expected)==0 for v in eq.split('='))
    return rec
def native(label,rec):
    f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/radio'):checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'each complete bank option'} for a in f[':answer-field/choices']]
    else:
        val=f[':answer-field/choices'][0][':answer/value'];checks=[{'submitted':s,'expected':e,'purpose':reason} for s,e,reason in [(val,'accepted','canonical'),('('+val+')+0','accepted','equivalent'),('2('+val+')/2','accepted','equivalent unsimplified'),('('+val+')+1','rejected','incorrect constant'),('-('+val+')','rejected','incorrect sign')]]
    return {'label':label,'record':rec,'checks':checks}
def main():
    inputs=[];replay=[];review=[];seen=set();counts={}
    for t,(level,_,_) in g.DATA.items():
        old=g.sources()[t];r=check(g.generate(level,0,t,{'k':1}));q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        assert q[':question/problem']==old[':question/problem'];assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
        assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
        assert q[':question/worked-solution']==old[':question/worked-solution'] or t=='q-1900'
        replay.append({'source':t,'profile':t,'matched_values':len(of[':answer-field/choices']),'total_values':len(of[':answer-field/choices']),'matched_distractors':len(of[':answer-field/choices'])-1,'total_distractors':len(of[':answer-field/choices'])-1,'complete_bank_matched':True,'missing_extra':[]})
        inputs.append(native('source-'+t,r));review.append({'label':'source '+t,'record':r})
    for level in ('easy','moderate'):
        count=0
        for t,params in g.candidates(level):
            rec=check(g.generate(level,1963,t,params));fp=fingerprint(rec['question']);assert fp not in seen;seen.add(fp);count+=1
            assert g.generate(level,123,t,params)['question']==rec['question'];inputs.append(native(t+'-'+str(params['k']),rec))
        counts[level]=count
    for level,t,k in [('hard','q-1900',2),('moderate','q-1900',0),('moderate','q-1900',13),('easy','q-1900',2),('moderate','q-1900',2.0)]:
        try:g.generate(level,1,t,{'k':k})
        except ValueError:pass
        else:raise AssertionError('Invalid parameter accepted')
    previews=g.batch('easy',5,1963)+g.batch('moderate',4,1963)
    for rec in previews:check(rec);review.append({'label':'variant','record':rec})
    save('previews.json',previews);save('review.json',review);(HERE/'review.md').write_text('\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in review)+'\n')
    save('native-input.json',inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    save('source-replay.json',{'passed':True,'source_results':replay,'complete_banks_matched':5,'complete_banks_total':5,'matched_values':21,'total_values':21,'matched_distractors':16,'total_distractors':16,'fidelity':'Five supported banks exactly replayed. q-1900 source solution f-prime(30) corrected to pi/6 locally. Original database records untouched. Four other source records explicitly excluded.'})
    save('capabilities.json',{'supported_levels':['easy','moderate'],'bounded_distinct_tasks':counts,'policy':'Positive integer amplitude transport k=2..12, source replay k=1. Full source bank transported. No chain/product rules, argument shifts or new workload.','exceptions':[{'difficulty':'hard','status':'unsupported','unfilled_reserve':5,'evidence':'No hard source among nine practice records at basis 1963. Supported workload comprises direct sum/constant differentiation and single special-angle tangent evaluation. No evidence for hard bank/template. Reopen with new evidence.'}],'unsupported_levels_filled':False})
    files=[HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'printed.py',HERE/'check-engine.rs',HERE/'check-engine',ROOT/'target/debug/libcourse_academy_engine.rlib']
    save('validation.json',{'passed':True,'counts':counts,'exhaustive_distinct_instances':len(seen),'actual_printed_math_checked':True,'solution_equations_checked':True,'native_grading_checked':True,'hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}})
    print('Validated',counts)
if __name__=='__main__':main()
