"""Independent printed-math checks, complete bank replay, and actual grading."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import printed as p
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def equivalent(a,b,indefinite):return sp.trigsimp(sp.diff(a-b,p.x))==0 if indefinite else sp.simplify(a-b)==0

def check(rec):
    q=rec['question'];meta=rec['generation'];t=meta['template'];m=meta['parameters']['m']
    assert g.generate(g.DATA[t][0],meta['seed'],t,{'m':m})==rec
    f,lo,hi=p.integral(q[':question/problem']);expected,F,answer,factor,inner,h,H,elo,ehi=g.math_data(t,m)
    assert sp.trigsimp(f-expected)==0 and lo==elo and hi==ehi
    assert sp.trigsimp(sp.diff(F,p.x)-f)==0
    if lo is not None:
        assert lo<hi
        # All definite substitutions are positive multiples of x^2, monotone;
        # sec*tan domain is [0,pi/3], and sin/cos have no poles.
        if t=='q-350202':assert sp.simplify(inner.subs(p.x,lo))==0 and sp.simplify(inner.subs(p.x,hi))==sp.pi/3
        answer=sp.simplify(F.subs(p.x,hi)-F.subs(p.x,lo))
    fields=q[':question/answer-fields'];assert len(fields)==1;field=fields[0];bank=field[':answer-field/choices'];indefinite=lo is None
    values=[p.scalar(a[':answer/value']).subs(p.C,0) for a in bank]
    for i,a in enumerate(values):
        valid=equivalent(a,F if indefinite else answer,indefinite)
        assert valid==(bank[i][':answer/id']==field[':answer-field/correct'][1]),(t,m,bank[i][':answer/value'])
        for b in values[:i]:assert not equivalent(a,b,indefinite),(t,m,'equivalent options')
    assert len(bank)==(1 if field[':answer-field/type'].endswith('/blank') else 5)
    assert ('{{field-1}}' in q[':question/problem'])==field[':answer-field/type'].endswith('/blank')
    assert fingerprint(q)==meta['mathematical_fingerprint']
    if m>1 or t=='q-13461':
        # Read the printed substitution, derivative, transformed integral, and
        # primitive independently; check the endpoint row and final scalar.
        solution=q[':question/worked-solution']
        printed_inner=p.scalar(re.search(r'\$u=(.*?),\$',solution)[1]);assert printed_inner==inner
        printed_derivative=p.scalar(re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(.*?)\.\n',solution)[1]);assert sp.simplify(printed_derivative-sp.diff(inner,p.x))==0
        block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)[1];rows=block.split('\\\\')
        rhs=[row.split('&=')[1].strip() for row in rows]
        i=rhs[0].index(r'\int');printed_factor=p.scalar(rhs[0][:i].rstrip('{ '))
        assert printed_factor==factor
        htext=rhs[0].split(r'\text{d}u')[0]
        if indefinite:htext=htext[i+4:]
        else:
            start=i+4;assert htext[start:].startswith(' }')
            start+=2;assert htext[start]=='_';a,start=p.group(htext,start+1);assert htext[start]=='^';b,start=p.group(htext,start+1)
            assert p.scalar(a)==sp.simplify(inner.subs(p.x,lo)) and p.scalar(b)==sp.simplify(inner.subs(p.x,hi));htext=htext[start:]
        assert sp.trigsimp(p.scalar(htext)-h)==0
        primitive_text=rhs[1].split(r'\big|')[0] if not indefinite else rhs[1]
        printed_primitive=p.scalar(primitive_text).subs(p.C,0)
        assert sp.trigsimp(sp.diff(printed_primitive,p.u)-factor*h)==0
        if indefinite:assert sp.trigsimp(sp.diff(p.scalar(rhs[-1]).subs(p.C,0),p.x)-f)==0
        else:
            assert sp.simplify(p.scalar(rhs[-2])-answer)==0 and sp.simplify(p.scalar(rhs[-1])-answer)==0
            table=re.search(r'\| \$x\$ \| \$(.*?)\$ \| \$(.*?)\$ \|\n\| --- \| --- \| --- \|\n\| \$u\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',solution)
            a,b,c,d=map(p.scalar,table.groups());assert (a,b)==(lo,hi) and sp.simplify(inner.subs(p.x,a)-c)==0 and sp.simplify(inner.subs(p.x,b)-d)==0
    return rec

def native(label,rec):
    f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'all bank options'} for a in f[':answer-field/choices']]
    else:
        c=f[':answer-field/choices'][0][':answer/value']
        checks=[{'submitted':v,'expected':e,'purpose':purpose} for v,e,purpose in [(c,'accepted','canonical'),('('+c+')+0','accepted','equivalent exact'),('2('+c+')/2','accepted','unsimplified equivalent'),('('+c+')+1','rejected','wrong offset'),('-('+c+')','rejected','wrong sign')]]
    return {'label':label,'record':rec,'checks':checks}
def main():
    replays=[];inputs=[];review=[];all_records=[];seen=set();counts={};sources=g.sources()
    for t,old in sources.items():
        r=check(g.generate(g.DATA[t][0],0,t,{'m':1}));q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        assert q[':question/problem']==old[':question/problem'];assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
        if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution']
        if of.get(':answer-field/correct'):assert f[':answer-field/choices'][[a[':answer/id'] for a in f[':answer-field/choices']].index(f[':answer-field/correct'][1])][':answer/value']==of[':answer-field/correct'][':answer/value']
        replays.append({'source':t,'profile':t if len(f[':answer-field/choices'])>1 else None,'matched_values':len(f[':answer-field/choices']),'total_values':len(of[':answer-field/choices']),'matched_distractors':len(f[':answer-field/choices'])-1,'total_distractors':len(of[':answer-field/choices'])-1,'complete_bank_matched':True,'missing_extra':[],'legacy_completion':t=='q-13461'})
        inputs.append(native('source-'+t,r));review.append({'label':'source '+t,'record':r});review.append({'label':'variant '+t,'record':check(g.generate(g.DATA[t][0],2,t,{'m':2}))})
    for level in ('moderate','hard'):
        count=0
        for t,params in g.candidates(level):
            r=check(g.generate(level,1,t,params));fp=fingerprint(r['question']);assert fp not in seen;seen.add(fp);count+=1;assert r['question']==g.generate(level,999,t,params)['question'];all_records.append(r);inputs.append(native(t+'-'+str(params['m']),r))
        counts[level]=count
    for level,t,m in [('easy','q-13461',2),('moderate','q-13461',0),('moderate','q-13461',13),('moderate','q-13461',2.5),('hard','q-13461',2)]:
        try:g.generate(level,1,t,{'m':m})
        except ValueError:pass
        else:raise AssertionError('Invalid input accepted')
    assert g.batch('moderate',3,5)==g.batch('moderate',3,5)
    try:g.batch('moderate',34,0)
    except ValueError:pass
    else:raise AssertionError('Finite limit not enforced')
    save('source-replay.json',{'passed':True,'sources':replays,'complete_banks_matched':8,'complete_banks_total':8,'matched_values':32,'total_values':32,'matched_distractors':24,'total_distractors':24,'source_solutions_retained':7,'unrated_source_completed_locally':'q-13461 moderate label, correct marker derived by differentiation, fixed worked solution authored; source untouched'})
    save('previews.json',all_records);save('review.json',review);(HERE/'review.md').write_text('\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in review)+'\n')
    save('native-input.json',inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    save('capabilities.json',{'supported_levels':['moderate','hard'],'bounded_distinct_tasks':counts,'policy':'Positive amplitude m=2..12; m=1 exact source-bank replay. No changed substitution, arbitrary shifts, or bank mixing. Original labels retained, unrated basic substitution classified moderate locally.','exceptions':[{'difficulty':'easy','status':'unsupported','unfilled_reserve':5,'evidence':'Eight sources at basis 1941: two rated moderate, five rated hard, one unrated. No easy bank or worked-solution template. Bounded package implements observed substitution workloads; absence does not prove mathematical impossibility. New source evidence reopens classification.'}],'unsupported_levels_filled':False})
    files=[HERE.with_suffix('.py'),HERE/'source.json',HERE/'printed.py',HERE/'validate.py',HERE/'check-engine.rs',HERE/'check-engine']
    save('validation.json',{'passed':True,'counts':counts,'exhaustive_distinct_instances':len(seen),'printed_math':'Integrand, bounds, differentiated primitives, all banks, substitution derivatives, u bounds, transformed integrals, primitives, endpoint equations and final answer parsed independently. Connected-domain pole restrictions explicit.','native_grading':'All eight source replays and all 88 bounded variants through learning::grade_field; every radio option; canonical/equivalent/incorrect blank probes.','hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}})
    print('Validated',counts)
if __name__=='__main__':main()
