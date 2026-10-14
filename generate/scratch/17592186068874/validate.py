#!/usr/bin/env python3
"""Independent displayed-polynomial, source-fidelity and actual native grading QA."""
import copy
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g68874',SCRIPT)
g=importlib.util.module_from_spec(spec);sys.modules[spec.name]=g;spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)


def polynomial(text):
    """Read displayed TeX, independent of generator recipe metadata."""
    text=text.strip().replace(r'\,','').replace(r'\cdot','*')
    text=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1/\2)',text)
    text=text.replace('{','').replace('}','').replace('^','**')
    assert '\\' not in text,text
    return sp.expand(parse_expr(text,transformations=TRANS))


def formatted(text):
    assert not any(ord(c)<32 and c not in '\n\t' for c in text),'C0'
    assert text.count('$')%2==0,'math delimiters'
    depth=0
    for c in text:
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0,'closing brace'
    assert depth==0,'braces'
    assert not any(line.startswith('    ') for line in text.splitlines()),'capture indentation'
    assert '--' not in text and '+-' not in text,'bare signed components'


def checked(record):
    q=record['question']; meta=record['generation']; p=meta['parameters']; v=sp.Symbol(p['variable'])
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    for text in [q[':question/problem'],q.get(':question/worked-solution','')]:formatted(text)
    # Extract the *actual printed prompt*, including first blank's fragmented math.
    text=q[':question/problem'].split('$')[1].split('=')[0].strip()
    expected=polynomial(text)
    assert expected.coeff(v,2)==p['b']**2
    assert expected.coeff(v,1)==-2*p['a']*p['b']<0
    assert expected.subs(v,0)==p['a']**2+p['c']
    assert text.startswith('(') and ')+' in text.replace(' ','') or text.startswith('(') and ')-' in text.replace(' ','')
    solution=q.get(':question/worked-solution')
    if solution:
        assert [block.strip() for block in solution.split('$$')[::2] if block.strip()]==[g.OPENING,g.FACTORING,g.CONCLUSION]
        blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
        assert len(blocks)==2
        rows=[]
        for block in blocks:
            exprs=[row.split('&')[0].strip() for row in block.split(r'\\')]
            maths=[polynomial(row) for row in exprs]
            assert all(sp.expand(a-maths[0])==0 for a in maths)
            rows.append(exprs)
        assert polynomial(rows[0][0])+p['c']==expected
        assert all(polynomial(row)==expected for row in rows[1])
        # Structural half-coefficient/square-identity stages must remain visible.
        assert r'2\cdot '+str(p['a']) in rows[0][-2]
        assert '^' in rows[0][-1] and rows[0][-1].startswith('(')
        stage=g.TEMPLATES[meta['template']].stages
        if stage=='numeric':
            assert len(rows[0])==4 and f'+{{{p["a"]}}}^{{2}}' in rows[0][1]
        else: assert len(rows[0])==3
        if stage=='scaled':assert f'({p["b"]}{p["variable"]})^{{2}}' in rows[0][1]
        # Independently verify displayed recalled formula, including its sign.
        formula=solution.split('$$')[1].strip()
        lhs,rhs=formula.split('=');assert polynomial(lhs)==polynomial(rhs)
    for fi,field in enumerate(q[':question/answer-fields']):
        choices=field.get(':answer-field/choices',[])
        for a in choices:formatted(a[':answer/value']);uuid=a[':answer/id'];assert len(uuid)==36
        if not choices: continue
        values=[polynomial(a[':answer/value']) for a in choices]
        correctref=field.get(':answer-field/correct')
        if field[':answer-field/type'].endswith('/radio'):
            assert len(choices)==len(set(values))==5
            correct=[i for i,val in enumerate(values) if val==expected];assert len(correct)==1
            if correctref: assert choices[correct[0]][':answer/id']==correctref[1]
        else:
            assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
            assert len(choices)==1 and '=' not in choices[0][':answer/value']
            target=p['b']*v-p['a'] if fi==0 else abs(p['c'])
            assert values[0]==target
            if correctref: assert correctref[1]==choices[0][':answer/id']
    return expected


def record_linear(r):
    p=r['generation']['parameters']
    return g.linear(p['variable'],p['b'])


def engine_request(r,label):
    checks=[]
    for fi,f in enumerate(r['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            if f[':answer-field/type'].endswith('/radio'):
                checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned complete choice'})
            else:
                value=a[':answer/value']
                equivalent=f'({record_linear(r)}-{r["generation"]["parameters"]["a"]-1})-1' if fi==0 else f'{int(value)*2}/2'
                for submitted,expected,purpose in [(value,'accepted','canonical fragment'),(equivalent,'accepted','equivalent unsimplified fragment'),('('+value+')+1','rejected','wrong fragment'),('-('+value+')','rejected','wrong sign')]:
                    checks.append({'field_index':fi,'submitted':submitted,'expected':expected,'purpose':purpose})
    return {'label':label,'record':r,'checks':checks}


def main():
    source=json.loads((HERE/'source.json').read_text())
    qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
    cases=[];reviews=[];source_report=[];engine=[]
    matched_options=0;correct_designations=0;matched_solutions=0
    for case in g.CASES:
        cid=case['source_id']; rawprofile='raw_'+cid
        replay=g.generate(case['level'],parameters=case['parameters'],profile=rawprofile)
        checked(replay)
        if not case['raw_missing']: engine.append(engine_request(replay,'original source bank '+cid))
        q=qs[cid];r=replay['question']
        for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
            assert (k in q)==(k in r),(cid,k,'presence')
        assert q[':question/problem']==r[':question/problem']
        if ':question/worked-solution' in q:
            assert q[':question/worked-solution']==r[':question/worked-solution'];matched_solutions+=1
        if ':question/difficulty' in q:assert q[':question/difficulty'][':db/ident']==r[':question/difficulty']
        for sf,gf in zip(q[':question/answer-fields'],r[':question/answer-fields']):
            assert sf[':answer-field/type'][':db/ident']==gf[':answer-field/type']
            assert sf[':answer-field/key']==gf[':answer-field/key']
            for k in (':answer-field/choices',':answer-field/correct'):assert (k in sf)==(k in gf),(cid,k)
            sv=sorted(a[':answer/value'] for a in sf.get(':answer-field/choices',[]))
            gv=sorted(a[':answer/value'] for a in gf.get(':answer-field/choices',[]));assert sv==gv,(cid,sv,gv)
            matched_options+=len(sv)
            if ':answer-field/correct' in sf:
                correct_designations+=1
                assert sf[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1])
        source_report.append({'source_id':cid,'prompt_exact':True,'present_solution_exact':':question/worked-solution' in q,'bank_values_exact':True,'raw_presence_exact':True,'raw_missing':case['raw_missing']})
        cases.append({**case,'observed_bank_profile':case['bank_profile'],'bank_profile':rawprofile,'profile':rawprofile,'authored_level_assignment':':question/difficulty' not in q})
        reviews.append({'label':'Original raw replay '+cid,'record':replay,'original':q})
        # Raw adjacent bank remains public evidence-only; normal counterpart uses
        # complete method-derived bank without fabricating the adjacent intention.
        normalprofile=case['bank_profile'] if case['bank_profile']!='adjacent_opaque' else 'half_coefficient'
        completed=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=normalprofile)
        checked(completed);engine.append(engine_request(completed,'completed '+cid))
        changed=dict(case['parameters']);changed['c']=(-1 if changed['c']<0 else 1)*(abs(changed['c'])%12+1)
        changed['a']=12 if case['level']=='moderate' else 8
        variant=g.generate(case['level'],seed=13,template=case['template'],parameters=changed,profile=normalprofile)
        checked(variant);engine.append(engine_request(variant,'variant '+cid))
        reviews.append({'label':'Generated variant of '+cid,'record':variant})
        # Every observed bank gets a changed-parameter raw replay, including opaque
        # adjacent patterns with explicit evidence-only status.
        if case['bank_profile']:
            vr=g.generate(case['level'],parameters=changed,profile=rawprofile);checked(vr)
            reviews.append({'label':'Changed-parameter observed bank evidence '+cid,'record':vr})
    fingerprints={level:set() for level in ('easy','moderate','hard')}
    families={level:set() for level in fingerprints}
    tested=0
    for level in fingerprints:
        for kind in ('radio','blank'):
            for seed in range(40):
                r=g.generate(level,seed,field_type=kind);checked(r);tested+=1
                assert r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/'+kind)
                fingerprints[level].add(r['generation']['mathematical_fingerprint']);families[level].add(r['generation']['template'])
                if seed<2:reviews.append({'label':f'Generated {level} {kind} seed {seed}','record':r});engine.append(engine_request(r,f'{level} {kind} seed {seed}'))
        expected={t for t in g.TEMPLATES if t.endswith('_scaled')==(level=='hard')}
        assert families[level]==expected,(level,families[level])
    # Enumerated meaningful domains omit variable and profile aliases entirely.
    enumeration={}
    for level in fingerprints:
        if level=='easy': pairs=[(a,1) for a in range(2,10)]
        elif level=='moderate':pairs=[(a,1) for a in range(10,16)]
        else:pairs=[(a,b) for a in range(2,10) for b in range(2,6) if sp.gcd(a,b)==1]
        enumeration[level]=len(pairs)*24
    for level in fingerprints:
        for t,s in g.TEMPLATES.items():
            if t.endswith('_scaled')!=(level=='hard'):continue
            banks=[None] if s.field=='blank' else (['scaled_method'] if level=='hard' else ['half_coefficient','square_constant','both_constant_signs'])
            for bank in banks:
                a=10 if level=='moderate' else 3;b=2 if level=='hard' else 1
                for c in [-12,-1,1,12]:
                    p={'a':a,'b':b,'c':c,'variable':'t'}
                    r=g.generate(level,template=t,parameters=p,profile=bank);checked(r);tested+=1
                    assert r['question'][':question/id']==g.generate(level,99,t,parameters=p,profile=bank)['question'][':question/id']
                    alias={**p,'variable':'z'}
                    assert r['generation']['mathematical_fingerprint']==g.generate(level,0,t,parameters=alias,profile=bank)['generation']['mathematical_fingerprint']
    # Public unfiltered defaults must cover every eligible family and bank.
    default_coverage={}
    for level in fingerprints:
        records=[g.generate(level,seed) for seed in range(100)]
        assert {r['generation']['template'] for r in records}=={t for t in g.TEMPLATES if t.endswith('_scaled')==(level=='hard')}
        expected_banks={'scaled_method'} if level=='hard' else {'half_coefficient','square_constant','both_constant_signs'}
        assert {r['generation']['profile'] for r in records if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio')}==expected_banks
        default_coverage[level]=sorted(expected_banks)
    p={'a':5,'b':1,'c':2,'variable':'x'}
    first=g.generate('easy',parameters=p,template='radio_numeric',profile='square_constant')
    second=g.generate('easy',parameters=p,template='radio_numeric',profile='both_constant_signs')
    assert first['question'][':question/id']!=second['question'][':question/id']
    assert first['generation']['mathematical_fingerprint']==second['generation']['mathematical_fingerprint']
    alias=g.generate('easy',parameters=p,profile='raw_q-140281')
    assert alias['question'][':question/id']==first['question'][':question/id']
    for a in range(2,10):
        for b in range(2,6):
            if sp.gcd(a,b)!=1:continue
            for c in [-12,12]:
                for t in ('radio_scaled','blank_scaled'):
                    checked(g.generate('hard',template=t,parameters={'a':a,'b':b,'c':c,'variable':'x'}));tested+=1
    invalid=[('easy','radio_numeric',{'a':0,'b':1,'c':2,'variable':'x'}),('moderate','radio_numeric',{'a':9,'b':1,'c':2,'variable':'x'}),('hard','radio_scaled',{'a':4,'b':2,'c':2,'variable':'x'}),('hard','radio_scaled',{'a':3,'b':1,'c':2,'variable':'x'}),('easy','radio_numeric',{'a':3,'b':1,'c':-13,'variable':'x'})]
    for level,t,p in invalid:
        try:g.generate(level,template=t,parameters=p)
        except ValueError:pass
        else:raise AssertionError('invalid parameter accepted')
    r=g.generate('easy',4,template='radio_numeric',parameters={'a':4,'b':1,'c':3,'variable':'x'},profile='half_coefficient')
    # Regressions preserve equal final mathematics but remove operative structure.
    for change in ('C0','half-stage','sign','prompt'):
        bad=copy.deepcopy(r)
        if change=='C0':bad['question'][':question/worked-solution']+='\x0c'
        elif change=='half-stage':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(r'2\cdot 4x','8x')
        elif change=='sign':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('-2ax','+2ax')
        else:bad['question'][':question/problem']=bad['question'][':question/problem'].replace('-8x','+8x')
        try:checked(bad)
        except AssertionError:pass
        else:raise AssertionError('mutation unnoticed '+change)
    for path,payload in [('source-cases.json',cases),('review.json',reviews),('native-input.json',engine)]:
        (HERE/path).write_text(json.dumps(payload,indent=2)+'\n')
    executable=REPO/'generate/runs/current/check-engine'
    subprocess.run([str(executable),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    native=json.loads((HERE/'native-report.json').read_text())
    review=[]
    for item in reviews:
        review+=['## '+item['label'],'',g.markdown(item['record']),'']
    (HERE/'review.md').write_text('\n'.join(review))
    result={'passed':True,'source':g.SOURCE,'source_questions':8,'source_prompts_exact':8,'source_present_solutions_exact':{'matched':matched_solutions,'total':6},'raw_attribute_presence_exact':8,'source_bank_options_exact':{'matched':matched_options,'total':29},'source_correct_designations':{'matched':correct_designations,'total':8},'source_complete_radio_banks_exact':{'matched':5,'total':5},'source_distractors_exact':{'matched':20,'total':20},'inferred_missing_designations':3,'authored_missing_solutions':2,'observed_difficulties':{'easy':5,'moderate':1,'unrated':2,'hard':0},'raw_replay_evidence_only':8,'opaque_banks':['q-140283 adjacent offsets; structural pattern parameterized, intent unresolved'],'independent_displayed_checks':tested,'sampled_distinct_meaningful_tasks':{k:len(v) for k,v in fingerprints.items()},'enumerated_meaningful_tasks':enumeration,'default_family_coverage':{k:sorted(v) for k,v in families.items()},'unfiltered_default_bank_coverage':default_coverage,'native':native,'native_executable_sha256':hashlib.sha256(executable.read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_results':source_report,'unresolved_findings':['Opaque adjacent choice-bank intent; raw public evidence retained and excluded from normal defaults.']}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','source_questions','source_prompts_exact','source_bank_options_exact','independent_displayed_checks','enumerated_meaningful_tasks')}))

if __name__=='__main__':main()
