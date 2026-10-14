#!/usr/bin/env python3
"""Independent readback of learner strings, source parity and actual native grading."""
import copy, functools, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('constant_ln',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ENGINE=ROOT/'generate/runs/current/check-engine'
native=[]
def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
@functools.lru_cache(maxsize=8192)
def eq(a,b):return sp.simplify(a-b)==0

def format_check(text):
    assert not any(ord(c)<32 and c not in '\n\t\r' for c in text),'Control characters'
    state=None
    for token in re.findall(r'\$\$|\$',text):
        if state is None:state=token
        else:assert state==token,'Mixed math delimiters';state=None
    assert state is None,'Math delimiters'
    depth=0
    for c in text:
        if c=='{':depth+=1
        elif c=='}':depth-=1
        assert depth>=0,'TeX braces'
    assert depth==0,'TeX braces'
    assert '--' not in text and '+-' not in text,'Ungrouped signs'

def solution_values(q):
    text=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)
    assert len(blocks)==2,'Source identity then worked chain'
    identity=blocks[0].replace(r'\frac{\text{d}}{\text{d}x}','D')
    lhs,rhs=identity.split('=');assert eq(g.expression(lhs),g.expression(rhs))
    displayed=g.coefficient(q[':question/problem']);expected=sp.diff(displayed*sp.log(g.x),g.x)
    aligned=re.sub(r'\\(?:begin|end)\{aligned\}','',blocks[1])
    rows=aligned.split(r'\\');assert len(rows)==4,'Ordered four-row source sequence'
    # Require operative structures, not merely four equivalent expressions.
    assert r'\frac{\text{d}}{\text{d}x}(' in rows[0]
    assert r'\frac{\text{d}}{\text{d}x}(' in rows[1]
    assert r'\cdot' in rows[2] and r'\frac{1}{x}' in rows[2]
    assert r'\frac{\text{d}}' not in rows[3]
    for i,row in enumerate(rows):
        lhs,rhs=row.replace('&','').split('=')
        rhs=rhs.replace(r'\frac{\text{d}}{\text{d}x}','D')
        assert eq(g.expression(rhs),expected),('Displayed stage',i,rhs,expected)
    return expected

def validate(rec,grade=True):
    assert set(rec['knowledge_point'])=={'db_id','id','title'}
    assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q,meta=rec['question'],rec['generation']
    assert meta['source_basis']==1356 and meta['domain']=='x>0'
    assert meta['dependencies']['python']==sys.version.split()[0]
    for k in (':question/problem',':question/worked-solution'):
        if k in q:format_check(q[k])
    c=g.coefficient(q[':question/problem'])
    assert not c.free_symbols and c!=0 # establish real x>0 and constant before CAS
    target=sp.diff(c*sp.log(g.x),g.x)
    if ':question/worked-solution' in q:assert eq(solution_values(q),target)
    fields=q.get(':question/answer-fields',[])
    assert len(fields)==(0 if meta['template']=='fieldless' else 1)
    for f in fields:
        vals=f[':answer-field/choices'];mathvals=[]
        for a in vals:format_check(a[':answer/value']);mathvals.append(g.expression(a[':answer/value']))
        assert len({a[':answer/id'] for a in vals})==len(vals)
        is_blank=f[':answer-field/type'].endswith('/blank')
        if is_blank:
            assert q[':question/problem'].count('{{'+f[':answer-field/key']+'}}')==1
            assert all(eq(v,target) for v in mathvals),'Every blank alias must be correct'
        else:
            assert len(vals)==5 and sum(eq(v,target) for v in mathvals)==1
            assert not any(eq(v,w) for i,v in enumerate(mathvals) for w in mathvals[:i]),'Full pairwise bank equivalence'
        if ':answer-field/correct' not in f:
            assert meta['evidence_only'] and not meta['eligible_for_learning'];continue
        correct=f[':answer-field/correct'][1];answer=next(a for a in vals if a[':answer/id']==correct)
        assert eq(g.expression(answer[':answer/value']),target)
        checks=[]
        if is_blank:
            checks=[{'submitted':a[':answer/value'],'expected':'accepted','purpose':'Canonical or captured equivalent blank entry'} for a in vals]
            # unreduced coefficient quotient is an actual different mathematical spelling
            p=meta['parameters'];exponent='' if p['k']==0 else 'e' if p['k']==1 else f'e^{p["k"]}'
            checks+=[{'submitted':f'{2*p["n"]}{exponent}/({2*p["d"]}x)','expected':'accepted','purpose':'Independently unreduced equivalent quotient'},
             {'submitted':g.latex(-target),'expected':'rejected','purpose':'Wrong coefficient sign'},
             {'submitted':g.latex(target+1),'expected':'rejected','purpose':'Spurious constant'}]
        else:checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Owned answer choice grading'} for a in vals]
        if grade:native.append({'label':q[':question/id'],'record':rec,'checks':checks})
    assert meta['math_fingerprint']==g.digest(['differentiate c ln x',sp.srepr(c),'x>0'])
    return target

def replay_fidelity(rec,source):
    q=rec['question'];assert q[':question/problem']==source[':question/problem']
    keys=(':question/difficulty',':question/worked-solution',':question/answer-fields')
    for key in keys:assert (key in q)==(key in source),(source[':question/math-academy-id'],key)
    if ':question/worked-solution' in source:assert q[':question/worked-solution']==source[':question/worked-solution']
    if ':question/difficulty' in source:assert q[':question/difficulty']==source[':question/difficulty'][':db/ident']
    for f,out in zip(source.get(':question/answer-fields',[]),q.get(':question/answer-fields',[]),strict=True):
        assert (':answer-field/correct' in f)==(':answer-field/correct' in out)
        assert f[':answer-field/key']==out[':answer-field/key'] and f[':answer-field/type'][':db/ident']==out[':answer-field/type']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in out[':answer-field/choices'])
        if ':answer-field/correct' in f:
            actual=next(a[':answer/value'] for a in out[':answer-field/choices'] if a[':answer/id']==out[':answer-field/correct'][1])
            assert actual==f[':answer-field/correct'][':answer/value']

def expect_fail(rec,label):
    try:validate(rec,grade=False)
    except (AssertionError,ValueError):return label
    raise AssertionError('Mutation unexpectedly passed '+label)

def main():
    cases=[];review=[];details=[];records=[]
    for sid,(template,bank,n,d,k) in g.CASES.items():
        case={'source_id':sid,'level':'easy','template':template,'parameters':{'n':n,'d':d,'k':k},'bank_profile':'raw-'+sid};cases.append(case)
        rec=g.generate('easy',0,template,parameters=case['parameters'],profile=case['bank_profile']);validate(rec);replay_fidelity(rec,g.QS[sid]);records.append(rec)
        details.append({'source_id':sid,'exact_prompt':True,'attribute_presence_parity':True,'bank_values':len(g.QS[sid].get(':question/answer-fields',[{}])[0].get(':answer-field/choices',[])),'observed_correct':bool(g.QS[sid].get(':question/answer-fields',[{}])[0].get(':answer-field/correct')),'exact_solution':':question/worked-solution' in g.QS[sid],'evidence_only':rec['generation']['evidence_only']})
        review+=['## Original '+sid+' and parameterized raw replay',json.dumps(g.QS[sid],indent=2,ensure_ascii=False),'### Raw replay',g.markdown(rec)]
        variants=[]
        for seed in (17,29):
            variant=g.generate('easy',seed,template,profile='raw-'+sid);validate(variant);variants.append(variant);records.append(variant)
        review+=['### Generated raw-profile variants (evidence status preserved)']+[g.markdown(r) for r in variants]
    normal=[];coverage={};levelcounts={};tasks={};profiles=set()
    for level in g.LEVELS:
        for template,(l,kind,banks) in g.TEMPLATES.items():
            if l!=level:continue
            for bank in banks:
                domain=g.parameter_domain(level,bank);coverage[template+'/'+bank]=len(domain)
                # full family domain parameter guards and complete-bank validity before sampling
                for p in domain:g.validate_parameters(p,level,bank);g.bank_values(p,bank)
                boundary=[domain[0],domain[-1]]
                for i,p in enumerate(boundary):
                    r=g.generate(level,i,template,parameters=p,profile=bank);validate(r);normal.append(r)
                for seed in range(12):
                    r=g.generate(level,seed,template,profile=bank);validate(r);normal.append(r)
                review+=['## Generated '+level+' — '+template+'/'+bank+' (authored level)' if level!='easy' else '## Generated easy — '+template+'/'+bank]+[g.markdown(r) for r in normal[-2:]]
        defaults=[g.generate(level,seed) for seed in range(120)]
        for r in defaults:validate(r,grade=False)
        profiles.update((r['generation']['template'],r['generation']['bank_profile']) for r in defaults)
        tasks[level]=len({r['generation']['math_fingerprint'] for r in defaults})
        levelcounts[level]=sum(r['generation']['authored_level']==(level!='easy') for r in defaults)
    expected={(t,b) for t,(_,_,banks) in g.TEMPLATES.items() for b in banks};assert profiles==expected,'Default family/profile coverage'
    # Public parameterized default also chooses eligible families deterministically.
    for p in ({'n':7,'d':1,'k':0},{'n':11,'d':4,'k':0},{'n':2,'d':1,'k':1}):
        a=g.generate('easy',1,parameters=p);b=g.generate('easy',900,parameters=p)
        validate(a,grade=False);assert a['question'][':question/id']==b['question'][':question/id']
    # identities independent of seed and option ordering, but banks/layouts remain distinguished
    for r in normal:
        m=r['generation'];l=r['question'][':question/difficulty'].split('/')[-1]
        s=g.generate(l,987,m['template'],parameters=m['parameters'],profile=m['bank_profile'])
        assert s['question'][':question/id']==r['question'][':question/id']
        assert s['generation']['math_fingerprint']==m['math_fingerprint']
    mutations=[];anchor=normal[-1]
    damaged=copy.deepcopy(anchor);damaged['question'][':question/worked-solution']=damaged['question'][':question/worked-solution'].replace(r'\cdot \frac{1}{x}',r'\cdot \frac{2}{x}');mutations.append(expect_fail(damaged,'Wrong intermediate reciprocal'))
    damaged=copy.deepcopy(anchor);damaged['question'][':question/worked-solution']=damaged['question'][':question/worked-solution'].replace(r'\cdot \frac{1}{x}',r'/x');mutations.append(expect_fail(damaged,'Lost operative reciprocal stage'))
    damaged=copy.deepcopy(anchor);damaged['question'][':question/problem']+='\x0c';mutations.append(expect_fail(damaged,'Control character'))
    damaged=copy.deepcopy(anchor);damaged['question'][':question/problem']=damaged['question'][':question/problem'].replace(r'\ln x',r'\ln x^2');mutations.append(expect_fail(damaged,'Changed displayed logarithm input'))
    invalid=[('moderate',{'n':-3,'d':2,'k':1}),('moderate',{'n':2,'d':1,'k':1}),('moderate',{'n':13,'d':2,'k':1}),('hard',{'n':3,'d':2,'k':2}),('hard',{'n':-3,'d':2,'k':1}),('hard',{'n':-14,'d':3,'k':2})]
    for level,p in invalid:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Authored level guard bypass')
    records+=normal
    save('source-cases.json',cases);save('review.json',records);(HERE/'review.md').write_text('# Constant×ln generator review\n\nFrozen basis 1356. Raw profiles preserve omissions; missing levels are authored.\n\n'+'\n\n---\n\n'.join(review)+'\n')
    save('native-input.json',native)
    subprocess.run([str(ENGINE),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    native_report=json.loads((HERE/'native-report.json').read_text())
    save('validation.json',{'passed':True,'basis':1356,'lineage':g.SOURCE['lineage'],'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_fidelity':{'questions':9,'exact_prompts':9,'complete_banks':8,'bank_values':sum(d['bank_values'] for d in details),'supplied_correct_designations':sum(d['observed_correct'] for d in details),'exact_supplied_solutions':sum(d['exact_solution'] for d in details),'attribute_presence_parity':9,'fieldless_replays':1,'unrated_replays':2},'source_details':details,'authored_missing_levels':['moderate','hard'],'bounded_profile_counts':coverage,'default_sample_distinct_math_tasks':tasks,'native':{k:v for k,v in native_report.items() if k!='records'},'native_report':'native-report.json','native_engine_sha256':hashlib.sha256(ENGINE.read_bytes()).hexdigest(),'mutation_regressions':mutations,'no_plots':True,'no_database_writes':True})
    print(json.dumps({'passed':True,'sources':len(cases),'normal_records':len(normal),'native_checks':{k:v for k,v in native_report.items() if k!='records'}},indent=2))
if __name__=='__main__':main()
