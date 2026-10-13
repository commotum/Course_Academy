#!/usr/bin/env python3
"""Source fidelity, displayed-component independent math, scope and real grading.
Runs fail closed; source evidence equality× limitations remain explicit separately.
"""
from pathlib import Path
import hashlib,importlib.util,json,re,subprocess,sys
import sympy as s
from functools import lru_cache
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from mathparse import parse,X,Y
ROOT=HERE.parents[2]

@lru_cache(maxsize=20000)
def equivalent(a,b):return s.simplify(s.trigsimp(s.expand_log(a-b,force=True)))==0

def clean(value):
    value=re.sub(r'\\text\{ for all \}','',value)
    return value.replace(r'\,✓','').replace(r'\,\times','').strip().rstrip('.')

def split_relation(row):
    lhs,rhs=row.split('&',1)
    m=re.match(r'\s*(\\overset\{\?\}\{=\}|\\not\\equiv|\\ne|=)(.*)',rhs,re.S)
    assert m,row
    return clean(lhs),m[1],clean(m[2])

def displayed(r):
    q=r['question'];text=q[':question/problem'];solution=q[':question/worked-solution']
    # Parse independent/dependent components FROM printed prompt.
    eq=re.search(r'\$\$\n(.*?)\n\$\$',text,re.S)[1]
    rhs=eq.split('=',1)[1].split(r'\,x')[0].split(r',\,\sin')[0].split(r',\,\cos')[0].rstrip('.')
    rhs=parse(rhs);ft=re.findall(r'- \$y=(.*?)\$',text);fs=[parse(f) for f in ft]
    assert len(fs)==3
    flags=[equivalent(s.diff(f,X),rhs.subs(Y,f)) for f in fs]
    correct=g.LABELS[sum(2**i for i,v in enumerate(flags) if v)]
    field=q[':question/answer-fields'][0];choices=field[':answer-field/choices']
    assert len(choices)==5 and len({a[':answer/value'] for a in choices})==5
    assert all(a[':answer/value'] in g.LABELS.values() for a in choices)
    a=next(a for a in choices if a[':answer/id']==field[':answer-field/correct'][1]);assert a[':answer/value']==correct
    # Every stated derivative and substituted function is checked independently.
    stated=re.findall(r'- Differentiating \$y=(.*?),\$ we get \$.*?=(.*?)\.\$',solution)
    assert len(stated)==3,(r['generation']['template'],stated)
    for i,(f,d) in enumerate(stated):assert equivalent(parse(f),fs[i]) and equivalent(parse(d),s.diff(fs[i],X))
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
    assert len(blocks)==3
    rows_total=0;opaque_false_equalities=0
    for i,body in enumerate(blocks):
        derivative=s.diff(fs[i],X);target=rhs.subs(Y,fs[i]);res=s.simplify(s.trigsimp(s.expand_log(derivative-target,force=True)))
        rows=body.split(r'\\');rows_total+=len(rows)
        assert len(rows)>=2
        for n,row in enumerate(rows):
            lhs,rel,right=split_relation(row)
            if n==0:
                assert 'd}y' in lhs;assert equivalent(parse(right),rhs);continue
            a,b=parse(lhs),parse(right)
            residual=s.simplify(s.trigsimp(s.expand_log(a-b,force=True)))
            if n==1:
                assert equivalent(a,derivative)
                assert equivalent(b,target),(g.tex(b),g.tex(target),row)
            elif rel in ('=',r'\overset{?}{=}') and equivalent(a,derivative):
                # Every substituted/simplified RHS is equal, even on false tests.
                assert equivalent(b,target),(row,g.tex(target))
            else:
                # Final reduced statements preserve the complete zero set;
                # reductions divide/multiply only nonzero factors on the domain.
                if flags[i]:assert equivalent(a,b)
                else:
                    assert not equivalent(a,b)
                    ratio=s.simplify(residual/res)
                    if r['generation']['domain']=='x > 0':
                        positive=s.Symbol('positive_x',positive=True)
                        ratio=s.cancel(s.powdenest(ratio.subs(X,positive**2),force=True)).subs(positive,s.sqrt(X))
                    assert ratio!=0 and ratio.is_zero is not True
                    # These families' ratios are nonzero monomials/exponentials.
                    # No free y or altered nonlinear factor can slip through.
                    assert not ratio.has(Y)
                    for factor in s.Mul.make_args(ratio):
                        valid=factor.is_number or factor==X or (factor.is_Pow and factor.base==X and factor.exp.is_number) or factor.func==s.exp
                        assert valid,(row,ratio)
                    if ratio.has(X) and any(factor==X or (factor.is_Pow and factor.base==X) for factor in s.Mul.make_args(ratio)):
                        assert r['generation']['domain']!='all real x'
                    num,den=s.fraction(ratio)
                    for term in (num,den):
                        assert not (term.has(s.sin,s.cos,s.tan,s.cot) and not equivalent(ratio,1)),(row,ratio)
            if rel=='=' and not flags[i] and not equivalent(a,b):opaque_false_equalities+=1
    assert solution.endswith('Therefore, the correct answer is "'+correct+'."')
    # Fixed solution is independent of answer selection; no fabricated diagnosis.
    assert 'initial condition' not in text.lower() and 'solve the differential' not in text.lower()
    for value in (text,solution):
        assert value.count('$')%2==0
        assert '+-' not in value and '--' not in value
        depth=0
        for j,c in enumerate(value):
            if c=='{' and (j==0 or value[j-1]!='\\'):depth+=1
            if c=='}' and (j==0 or value[j-1]!='\\'):depth-=1
            assert depth>=0
        assert depth==0
    assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==g.KP
    assert field[':answer-field/type']==':answer-field.type/radio'
    return {'stages':rows_total,'raw_false_equality_rows':opaque_false_equalities}

def main():
    assert equivalent(parse(r'2x\sqrt{x}'),2*X*s.sqrt(X))
    assert equivalent(parse(r'2y\operatorname{cot}⁡2x'),2*Y*s.cot(2*X))
    captured=json.loads((ROOT/'generate/runs/current/sources/17592186100959.json').read_text());assert captured==g.RAW
    cases=[];review=[];engine=[];metrics=[];source_counts={'questions':0,'prompts_exact':0,'solutions_exact':0,'choices_exact':0,'correct_designations_exact':0,'complete_banks':0,'wrong_choices_matched':0,'wrong_choices_total':0}
    def add(r,label):
        metrics.append(displayed(r));review.append({'label':label,'record':r});f=r['question'][':question/answer-fields'][0]
        engine.append({'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Complete semantic subset criterion; owned radio ID','field_index':0} for a in f[':answer-field/choices']]})
    for sid,q in g.SOURCES.items():
        case={'source_id':sid,'source_db_id':q[':db/id'],'level':'moderate','template':'source_'+sid,'bank_profile':sid,'parameters':{'scale':1}};cases.append(case)
        r=g.generate('moderate',seed=13,profile=sid,parameters=case['parameters']);new=r['question'];sf=q[':question/answer-fields'][0];nf=new[':question/answer-fields'][0]
        source_counts['questions']+=1
        assert set(new)-{':question/id'}==set(q)-{':db/id',':question/math-academy-id',':question/id'}
        assert new[':question/problem']==q[':question/problem'];source_counts['prompts_exact']+=1
        assert new[':question/worked-solution']==q[':question/worked-solution'];source_counts['solutions_exact']+=1
        assert sf[':answer-field/key']==nf[':answer-field/key'] and sf[':answer-field/type'][':db/ident']==nf[':answer-field/type']
        old=sorted(a[':answer/value'] for a in sf[':answer-field/choices']);newbank=sorted(a[':answer/value'] for a in nf[':answer-field/choices']);assert old==newbank
        source_counts['choices_exact']+=len(old);source_counts['complete_banks']+=1
        actual=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert actual==sf[':answer-field/correct'][':answer/value'];source_counts['correct_designations_exact']+=1
        source_counts['wrong_choices_matched']+=4;source_counts['wrong_choices_total']+=4
        add(r,'original '+sid)
        for c in [2,-3]:add(g.generate('moderate',seed=17,profile=sid,parameters={'scale':c}),'generated source-mask '+sid+' scale='+str(c))
    variety={};patterns={};orders=set();sampler_records=[]
    for level,templates in g.FAMILIES.items():
        fps=set();patterns[level]=set()
        for template in templates:
            for seed in range(40):
                r=g.generate(level,seed,template=template);displayed(r);sampler_records.append(r)
                fps.add(r['generation']['mathematical_fingerprint']);patterns[level].add(next(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]))
                repeat=g.generate(level,seed+91,template=template,parameters=r['generation']['parameters'])
                assert r['question'][':question/id']==repeat['question'][':question/id']
                assert r['generation']['mathematical_fingerprint']==repeat['generation']['mathematical_fingerprint']
                f=r['question'][':question/answer-fields'][0];orders.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
                if seed<2:add(r,'authored '+level+' '+template+' seed='+str(seed))
        assert len(fps)>=30;variety[level]={'sampled_instances':40*len(templates),'distinct_mathematical_tasks':len(fps),'common_scaling_excluded':True,'variable_aliases_excluded':True,'observed_truth_patterns_in_sample':sorted(patterns[level])}
    assert orders==set(range(5))
    for index,r in enumerate(sampler_records):
        if r['generation']['seed']<2:continue
        f=r['question'][':question/answer-fields'][0]
        engine.append({'label':'sampled authored '+str(index),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Native complete subset criterion on independent sampled task','field_index':0} for a in f[':answer-field/choices']]})
    # Explicit boundaries and invalid inputs must fail instead of silently changing.
    bad=[('easy','exp',{'k':2,'candidates':[[1,1,0],[2,-1,0],[3,1,1]]}),('hard','affine',{'n':2,'a':1,'candidates':[[0,1,0],[1,1,0],[2,2,0]]}),('moderate','sin',{'k':1,'candidates':[[1,1,0],[2,1,0],[3,1,1]]}),('hard','log',{'a':1,'b':'1','candidates':[[1,0,0],[2,0,0],[3,0,0]]}),('moderate','exp',{'k':2,'candidates':[[1,2,0],[1,2,0],[2,2,0]]})]
    for level,template,p in bad:
        try:g.generate(level,template=template,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit parameter accepted')
    for sid in g.SOURCES:
        a=g.generate('moderate',profile=sid,parameters={'scale':1});b=g.generate('moderate',profile=sid,parameters={'scale':2})
        assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
        assert a['question'][':question/id']!=b['question'][':question/id']
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True,capture_output=True,text=True)
    report=json.loads((HERE/'engine-report.json').read_text())
    result={'pass':True,'source_fidelity':source_counts,'source_repairs':{'presentation_repairs':0,'mathematical_bank_repairs':0,'raw_false_equalities_with_cross':sum(m['raw_false_equality_rows'] for m in metrics[:3*len(cases):3]),'normal_authored_solution_relation_repair':'False comparisons are queries followed by residual not identically zero; raw replay retains equality× notation as evidence-only.'},'generated_review_records':len(review),'sampled_authored_math_checks':len(sampler_records),'independently_checked_review_stages':sum(m['stages'] for m in metrics),'variety':variety,'native_engine':report,'native_engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'guard_rejections':len(bad),'limitations':['No observed easy or hard labels; their workload scope is explicitly authored.','Observed scale parameterization is excluded from meaningful task variety.','Raw observed profiles retain equality followed by cross on invalid comparisons and are evidence-only.','A finite bounded sampler is implemented; random sample diversity is reported, not an unbounded total.']}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    md=[]
    for row in review:
        md.append('## '+row['label']+' | '+g.preview_label(row['record'])+'\n\n'+g.markdown(row['record']))
    (HERE/'review.md').write_text('# Originals and labeled generated variants\n\n'+'\n\n'.join(md)+'\n')
    print(json.dumps({k:result[k] for k in ('pass','source_fidelity','generated_review_records','sampled_authored_math_checks','variety')},indent=2))
if __name__=='__main__':main()
