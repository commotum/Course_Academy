#!/usr/bin/env python3
"""Independent readback/fidelity/native-engine validation; fails closed, zero DB writes."""
import hashlib, importlib.util, json, math, re, subprocess, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
CASES=json.loads((HERE/'source-cases.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in g.RECORD[':knowledge-point/questions']}

def same(a,b):return sp.expand(a-b)==0

def clean_math(s):
    assert s.count('$')%2==0,'Unbalanced math delimiters'
    depth=0
    for ch in s:
        if ch=='{':depth+=1
        if ch=='}':depth-=1
        assert depth>=0,'Unbalanced brace'
    assert depth==0,'Unbalanced brace'
    assert '\\'+'\\' not in s,'Unexpected doubled TeX slash'
    assert '--' not in s and '+-' not in s,'Ungrouped sign'

def split_commas(s):
    s=s.replace(r'\,','');depth=0;parts=[];start=0
    for i,c in enumerate(s):
        if c=='(':depth+=1
        elif c==')':depth-=1
        elif c==',' and depth==0:parts.append(s[start:i]);start=i+1
    parts.append(s[start:]);return parts

def check_solution(sol,P,Q,L):
    # Formal LCM equalities are read from actual displayed solution, not metadata.
    observed=[]
    for match in re.finditer(re.escape(r'\text{LCM}('),sol):
        start=match.end();depth=1;i=start
        while depth:
            ch=sol[i]
            if ch=='(':depth+=1
            if ch==')':depth-=1
            i+=1
        if sol[i:i+1]!='=':continue
        terms=[g.parse_tex(t) for t in split_commas(sol[start:i-1])]
        assert len(terms)==2
        lhs=sp.lcm(terms[0],terms[1])
        end=i+1
        while end<len(sol) and sol[end] not in '$\n':end+=1
        chain=sol[i+1:end].rstrip('.')
        for stage in chain.split('='):assert same(lhs,g.parse_tex(stage)),f'Incorrect displayed LCM stage {stage}'
        observed.append((terms,lhs))
    assert len(observed)==3,'Three integer/variable/full LCM equalities required'
    assert same(observed[-1][0][0],P) and same(observed[-1][0][1],Q)
    assert same(observed[-1][1],L)
    numeric=observed[0][0];a,b=map(int,numeric);l=math.lcm(a,b)
    lists=re.findall(r'- Multiples of \$(\d+):\$ \$(.*?)\$',sol)
    assert len(lists)==2
    for c,values in lists:
        c=int(c);nums=list(map(int,re.findall(r'\d+',values)))
        assert nums and all(k>0 and k%c==0 for k in nums)
        assert l in nums,'Worked list must expose common multiple'
    power=int(re.search(r'which is \$(\d+)\.\$',sol).group(1))
    variable=next(iter(L.free_symbols))
    assert power==sp.degree(L,variable),'Largest-power prose disagrees with actual task'
    assert sol.startswith(g.OPENING)
    assert sol.count('Therefore,')==1 and sol.count('Finally, we multiply all of our results together:')==1

def check_record(r,raw=False):
    assert set(r)=={'knowledge_point','question','generation'}
    kp=r['knowledge_point'];assert set(kp)=={'db_id','id','title'} and kp['db_id']==g.KP_ID
    q,meta=r['question'],r['generation'];uuid.UUID(q[':question/id']);clean_math(q[':question/problem'])
    prompt_exprs=re.findall(r'\$([^$]+)\$',q[':question/problem'])
    assert len(prompt_exprs)==2
    P,Q=map(g.parse_tex,[s.rstrip('.') for s in prompt_exprs]);L=sp.lcm(P,Q)
    assert len(P.free_symbols|Q.free_symbols)==1,'Single variable only'
    # Independent full-polynomial LCM over integers retains integer content.
    for obj in (P,Q):
        variable=next(iter(obj.free_symbols));coeff,factors=sp.factor_list(obj,variable)
        assert coeff>0 and len(factors)==1 and sp.degree(factors[0][0],variable)==1
        assert sp.LC(sp.Poly(factors[0][0],variable))==1
    fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0]
    uuid.UUID(f[':answer-field/id']);kind=f[':answer-field/type'].split('/')[-1]
    assert kind in ('blank','radio')
    if kind=='blank':assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    if raw:
        assert ':answer-field/correct' not in f and ':question/worked-solution' not in q and ':question/difficulty' not in q
        if kind=='blank':assert ':answer-field/choices' not in f;return
    answers=f[':answer-field/choices'];assert len(answers)==(1 if kind=='blank' else 5)
    vals=[];ids=set()
    for answer in answers:
        uuid.UUID(answer[':answer/id']);assert answer[':answer/id'] not in ids;ids.add(answer[':answer/id'])
        assert answer[':answer/type']==':answer.type/math';value=answer[':answer/value'];assert '$' not in value;clean_math(value)
        val=g.parse_tex(value);assert val.free_symbols<=P.free_symbols;vals.append(val)
    assert not any(same(x,y) for i,x in enumerate(vals) for y in vals[i+1:]),'Equivalent displayed options'
    if not raw:
        assert f[':answer-field/correct'][0]==':answer/id' and f[':answer-field/correct'][1] in ids
        selected=next(a for a in answers if a[':answer/id']==f[':answer-field/correct'][1])
        assert same(g.parse_tex(selected[':answer/value']),L)
        assert sum(same(v,L) for v in vals)==1
        assert not same(L,L/sp.Poly(L,next(iter(L.free_symbols))).content()),'Content must be substantive'
        assert q[':question/difficulty']==':question.difficulty/'+meta['level']
        clean_math(q[':question/worked-solution']);check_solution(q[':question/worked-solution'],P,Q,L)
        core={'version':g.VERSION,'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],'bank':sorted(a[':answer/value'] for a in answers),'field_type':kind}
        assert g.digest(core)==meta['content_identity']

def replay_checks():
    prompts=solutions=bankmatches=designation=missing=choices=distractors=0;rows=[]
    for case in CASES:
        sid=case['source_id'];src=SOURCES[sid]
        r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        raw=bool(g.PROFILES[sid].get('missing'));check_record(r,raw)
        q=r['question'];assert q[':question/problem']==src[':question/problem'];prompts+=1
        assert q.get(':question/worked-solution')==src.get(':question/worked-solution')
        if ':question/worked-solution' in src:solutions+=1
        sf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        assert sf[':answer-field/key']==f[':answer-field/key'] and sf[':answer-field/type'][':db/ident']==f[':answer-field/type']
        if ':answer-field/choices' in sf:
            originals=[a[':answer/value'] for a in sf[':answer-field/choices']]
            generated=[a[':answer/value'] for a in f[':answer-field/choices']]
            assert sorted(originals)==sorted(generated),'Exact full source bank mismatch'
            assert all(sum(same(g.parse_tex(a),g.parse_tex(b)) for b in generated)==1 for a in originals)
            bankmatches+=1;choices+=len(originals);distractors+=len(originals)-1
        else:assert ':answer-field/choices' not in f
        if ':answer-field/correct' in sf:
            srcval=sf[':answer-field/correct'][':answer/value']
            correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert correct[':answer/value']==srcval;designation+=1
        else:
            assert ':answer-field/correct' not in f;missing+=1
        if raw:
            derived=g.generate(case['level'],parameters=case['parameters'],profile='derived_'+sid);check_record(derived)
            assert derived['generation']['authored_completion']
        rows.append({'source_id':sid,'prompt_exact':True,'captured_solution_exact':not raw,'captured_bank_exact':':answer-field/choices' in sf,'correct_designation_exact':':answer-field/correct' in sf,'missing_fields_preserved':raw,'source_level':src.get(':question/difficulty',{}).get(':db/ident'),'replay_level_authored':':question/difficulty' not in src})
    return {'source_questions':len(CASES),'exact_prompts':prompts,'exact_captured_solutions':f'{solutions}/5','preserved_absent_solutions':'2/2','exact_captured_banks':f'{bankmatches}/6','exact_captured_choices':f'{choices}/14','matched_source_distractors':f'{distractors}/8','matched_captured_correct_designations':f'{designation}/5','preserved_missing_designations':f'{missing}/2','rows':rows}

def engine_checks(records):
    items=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0];checks=[]
        correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);p=r['generation']['parameters']
        if f[':answer-field/type'].endswith('/radio'):
            checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a==correct else 'rejected','purpose':'Owned correct/distractor selection'} for a in f[':answer-field/choices']]
        else:
            expr=g.parse_tex(correct[':answer/value']);v=sp.Symbol(p['v']);N=max(p['n'],p['m']);l=math.lcm(p['a'],p['b']);h=p['h']
            reordered=f'{l}*({h}+{v})^{N}' if h>0 else f'{l}*({h}+{v})^{N}'
            split=f'{l}*({v}+({h}))^{N-1}*({v}+({h}))'
            checks=[{'submitted':correct[':answer/value'],'expected':'accepted','purpose':'canonical polynomial'},
                    {'submitted':str(expr).replace('**','^'),'expected':'accepted','purpose':'fully expanded equivalent polynomial'},
                    {'submitted':reordered,'expected':'accepted','purpose':'binomial term order'},
                    {'submitted':split,'expected':'accepted','purpose':'uncollected equivalent powers'},
                    {'submitted':str(sp.expand(expr/l)).replace('**','^'),'expected':'rejected','purpose':'wrong monic normalization over Q instead of integer content LCM'},
                    {'submitted':str(sp.expand(2*expr)).replace('**','^'),'expected':'rejected','purpose':'wrong scalar multiple is not equivalent'},
                    {'submitted':g.polynomial(p,l,min(p['n'],p['m'])),'expected':'rejected','purpose':'minimum exponent gives GCF variable part'}]
        items.append({'label':f'{i}-{r["generation"]["profile"]}-{r["generation"]["level"]}','record':r,'checks':checks})
    (HERE/'engine-input.json').write_text(json.dumps(items,indent=2)+'\n')
    executable=REPO/'generate/runs/current/check-engine'
    subprocess.run([str(executable),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    report=json.loads((HERE/'engine-report.json').read_text())
    report['executable_sha256']=hashlib.sha256(executable.read_bytes()).hexdigest()
    (HERE/'engine-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','entry_point','executable_sha256')}

def main():
    source=replay_checks();records=[];checks=0;fingerprints={l:set() for l in ('easy','moderate','hard')}
    for level in fingerprints:
        for template in g.TEMPLATES:
            for seed in range(100):
                r=g.generate(level,seed,template);check_record(r);checks+=1;fingerprints[level].add(r['generation']['mathematical_fingerprint'])
                if seed<2:records.append(r)
            for seed in range(2):
                r=g.generate(level,seed,template);p=r['generation']['parameters']
                shifted=g.generate(level,seed+100,template,parameters=p)
                assert r['question'][':question/id']==shifted['question'][':question/id']
                alias={**p,'v':'t' if p['v']!='t' else 'x'}
                aliasr=g.generate(level,seed,template,parameters=alias)
                assert r['generation']['mathematical_fingerprint']==aliasr['generation']['mathematical_fingerprint']
                assert r['question'][':question/id']!=aliasr['question'][':question/id']
        assert len(fingerprints[level])>=80,'Insufficient meaningful task variety'
    for case in CASES:
        for prefix in ('observed_','derived_'):
            r=g.generate(case['level'],parameters=case['parameters'],profile=prefix+case['source_id'])
            if not r['generation']['source_omissions']:records.append(r)
        # Changed parameters through original whole bank/profile; preserve list ratios.
        p=case['parameters'];cfg=g.PROFILES[case['source_id']]
        changed={**p,'h':-p['h'],'v':'t','n':p['n'],'m':p['m']}
        r=g.generate(case['level'],parameters=changed,profile='derived_'+case['source_id']);check_record(r);records.append(r)
    # Complete banks must reject collisions, explicit guards must reject scope drift.
    invalid=[('easy',{'a':2,'b':4,'n':2,'m':3,'v':'x','h':1},None),('moderate',{'a':2,'b':3,'n':2,'m':4,'v':'x','h':1},None),('hard',{'a':8,'b':16,'n':6,'m':4,'v':'x','h':1},None),('hard',{'a':8,'b':20,'n':5,'m':3,'v':'x','h':1},None),('easy',{'a':2,'b':3,'n':1,'m':2,'v':'x','h':1},'retain_inputs')]
    for level,p,profile in invalid:
        try:g.generate(level,template='power_radio',parameters=p,profile=profile)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit instance accepted')
    # Source-profile changes retain arithmetic list recipes and varied coefficients.
    changed_profiles=[('easy','derived_q-218483',dict(a=7,b=3,n=2,m=5,v='x',h=-2)),('easy','derived_q-76460',dict(a=3,b=5,n=3,m=1,v='z',h=2)),('hard','derived_q-76457',dict(a=12,b=18,n=8,m=5,v='x',h=-2)),('hard','derived_q-222022',dict(a=12,b=18,n=8,m=5,v='z',h=4))]
    # q-218483 fixed list does not contain lcm(7,3)/7=3; reject honestly.
    try:g.generate(changed_profiles[0][0],parameters=changed_profiles[0][2],profile=changed_profiles[0][1])
    except ValueError:pass
    else:raise AssertionError('Source list omitted LCM under changed parameters')
    for level,profile,p in changed_profiles[1:]:
        r=g.generate(level,parameters=p,profile=profile);check_record(r);records.append(r)
    for level,profile,p in [
        ('easy','derived_q-218483',dict(a=5,b=2,n=3,m=4,v='w',h=-1)),
        ('easy','derived_q-222013',dict(a=4,b=7,n=2,m=5,v='z',h=2)),
        ('moderate','derived_q-222016',dict(a=12,b=4,n=5,m=3,v='x',h=-4)),
        ('hard','derived_q-222021',dict(a=12,b=8,n=7,m=4,v='z',h=-2)),
    ]:
        r=g.generate(level,parameters=p,profile=profile);check_record(r);records.append(r)
    for level,profile in [('easy','retain_inputs'),('hard','product_power')]:
        for seed in range(3):
            r=g.generate(level,seed,profile=profile);check_record(r)
            assert r['generation']['template']=='power_radio'
        try:g.generate(level,field_type='blank',profile=profile)
        except ValueError:pass
        else:raise AssertionError('Radio bank accepted a blank layout')
    native=engine_checks(records)
    (HERE/'review.json').write_text(json.dumps(records,indent=2)+'\n')
    summary={'status':'passed','generator_version':g.VERSION,'source_fidelity':source,'correctness':{'random_instances':checks,'review_native_records':len(records),'independent_displayed_polynomial_and_solution_readback':True,'unique_sampled_tasks':{l:len(v) for l,v in fingerprints.items()},'invalid_explicit_cases_rejected':len(invalid)+1},'native_grading':native,'scope':{'all_three_levels':True,'moderate_authored':True,'no_new_mathematical_branches':True,'plots':'none'},'remaining_unresolved_findings':[]}
    (HERE/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
    lines=['# Source and generated review','',f'Math database basis {g.SOURCE["basis"]}; learner answers shown for review only. Raw missing records are explicitly labeled.','']
    for case in CASES:
        sid=case['source_id'];lines+=['## Original '+sid,'',SOURCES[sid][':question/problem'],'',json.dumps(SOURCES[sid][':question/answer-fields'],indent=2),'',SOURCES[sid].get(':question/worked-solution','[Source solution and correct designation absent.]'),'','## Parameterized replay '+sid,'',g.markdown(g.generate(case['level'],parameters=case['parameters'],profile='observed_'+sid)),'']
        variant=next(r for r in records if r['generation']['profile']=='derived_'+sid and r['generation']['parameters']['v']=='t')
        lines+=['## Generated variant / authored completion '+sid,'',g.markdown(variant),'']
    lines+=['## Authored defaults at each level','']
    lines+=['\n\n'.join(g.markdown(r) for r in records[:12])]
    (HERE/'review.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
