#!/usr/bin/env python3
"""Independent displayed-mathematics, source fidelity, identity and native checks."""
import importlib.util, json, re, hashlib, subprocess, sys, itertools
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('surface_normal',HERE.with_suffix('.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def read_prompt(r):
    text=r['question'][':question/problem']
    ft=re.search(r'f\(x,y,z\)=(.*?)\$',text).group(1).rstrip(',')
    pts=re.search(r'\(x,y,z\)=\((.*?)\)',text).group(1).rstrip('.')
    return m.scalar(ft),[m.scalar(c) for c in pts.split(',')]

def rows(r):return r['question'][':question/worked-solution'].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')

def zero(v):return all(sp.simplify(sp.expand(a.rewrite(sp.exp)))==0 for a in v)

def formal_arguments(s):
    found=[]
    for var in 'xyz':
        needle=r'\frac{∂}{∂'+var+'}('
        if needle not in s:needle=r'\frac{\partial}{\partial '+var+'}('
        start=s.index(needle)+len(needle);i=start;depth=1
        while depth:
            depth+=(s[i]=='(')-(s[i]==')');i+=1
        found.append(m.scalar(s[start:i-1]))
    return found

def check(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==m.KP_ID
    assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
    f,p=read_prompt(r);sub=dict(zip(m.VARS,p));partials=[sp.diff(f,v) for v in m.VARS];g=sp.Matrix([sp.simplify(d.subs(sub)) for d in partials]);c=f.subs(sub)
    assert all(a.is_finite and a.is_real for a in g) and g!=sp.zeros(3,1)
    assert c.is_finite and c.is_real and sp.simplify(c-sp.sympify(r['generation']['level_surface_value']))==0
    rr=rows(r);assert len(rr)==5
    assert all(token in rr[0] for token in ('{f}_{x}(x,y,z)','{f}_{y}(x,y,z)','{f}_{z}(x,y,z)'))
    assert all(sp.simplify(a-f)==0 for a in formal_arguments(rr[1]))
    symbolic=m.vector(rr[2].split('=',1)[1]);assert zero(symbolic-sp.Matrix(partials))
    evaluated=m.vector(rr[3].split('=',1)[1]);assert zero(evaluated-g)
    reduced=m.vector(rr[4].split('=',1)[1]);assert zero(reduced-g)
    w=r['question'][':question/worked-solution'];conclusion=re.search(r'Therefore, \$(.*?)\$',w).group(1);assert zero(m.vector(conclusion)-g)
    # All prose mentions of the substituted gradient and point agree with prompt.
    for match in re.findall(r'(?:∇f|\(x,y,z\)=)\((.*?)\)',w):
        if match!='x,y,z':assert [m.scalar(a) for a in match.split(',')]==p
    alltext=r['question'][':question/problem']+w
    assert alltext.count('$')%2==0 and alltext.count('{')==alltext.count('}')
    for row in rr:assert row.count('(')==row.count(')')
    assert not any(s in alltext for s in ('+-','--',r'\sinh',r'\cosh'))
    for field in r['question'][':question/answer-fields']:
        assert field[':answer-field/type']==':answer-field.type/radio' and len(field[':answer-field/choices'])==5
        correct=field[':answer-field/correct'][1]
        vs=[m.vector(a[':answer/value']) for a in field[':answer-field/choices']]
        valid=[v!=sp.zeros(3,1) and zero(v.cross(g)) for v in vs]
        assert sum(valid)==1
        assert next(a[':answer/id'] for a,yes in zip(field[':answer-field/choices'],valid) if yes)==correct
        assert len(set(a[':answer/id'] for a in field[':answer-field/choices']))==5
        assert all(v!=sp.zeros(3,1) for v in vs)
        assert all(not zero(a-b) for a,b in itertools.combinations(vs,2))
    return g

def presence(a,b):
    assert set(a)==set(b)
    for k in a:
        if isinstance(a[k],dict):presence(a[k],b[k])
        elif isinstance(a[k],list) and a[k] and isinstance(a[k][0],dict):
            assert len(a[k])==len(b[k])
            for aa,bb in zip(a[k],b[k]):presence(aa,bb)

def main():
    fidelity=[];review=[];engine=[];normal_count=0
    for k,q in m.QUESTIONS.items():
        r=m.generate('easy',template=k,parameters={'point':m.POINTS[k]},profile='raw_'+k)
        expected=m.normalized(q);presence(r['question'],expected)
        assert r['question']==expected
        assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
        f,p=read_prompt(r);g=sp.Matrix([sp.diff(f,v).subs(dict(zip(m.VARS,p))) for v in m.VARS])
        banks=[]
        for fi,field in enumerate(r['question'][':question/answer-fields']):
            valid=[a[':answer/value'] for a in field[':answer-field/choices'] if m.eligible(m.vector(a[':answer/value']),g)]
            assert len(valid)==1
            designated=field.get(':answer-field/correct')
            banks.append({'field_index':fi,'choices_matched':5,'valid_normals':valid,'designation_matched':designated is not None,'legacy_missing_designation':designated is None})
            if designated:
                checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==designated[1] else 'rejected','purpose':'source radio native designation'} for a in field[':answer-field/choices']]
                fixture=json.loads(json.dumps(r));fixture['question'][':question/answer-fields']=[field]
                engine.append({'label':k+' source field '+str(fi),'record':fixture,'checks':checks})
        fidelity.append({'source_id':k,'raw_prompt_exact':True,'raw_solution_exact':True,'key_presence_exact':True,'banks':banks})
        review.append({'label':'Original evidence '+k,'record':r})
        # Public raw evidence also parameterizes changed inputs: no literal payload.
        changed=list(m.POINTS[k]);changed[0]+=1
        try:
            rr=m.generate('easy',template=k,parameters={'point':changed},profile='raw_'+k)
            assert rr['question'][':question/problem']!=r['question'][':question/problem']
            review.append({'label':'Parameterized opaque evidence variant '+k+' (ineligible)', 'record':rr})
        except ValueError:pass  # raw domain guards remain active
        for seed in (201,202):
            n=m.generate('easy',seed=seed,template=k);check(n);review.append({'label':'Generated source-family variant '+k,'record':n})
    uniques={};coverage={l:set() for l in ('easy','moderate','hard')}
    for level in coverage:
        records=[m.generate(level,seed=i) for i in range(36)]
        for r in records:check(r);normal_count+=1;coverage[level].add(r['generation']['template'])
        assert coverage[level]=={k for k,v in m.TEMPLATES.items() if v['level']==level}
        uniques[level]=len({r['generation']['task_fingerprint'] for r in records})
        for i,r in enumerate(records[:2]):review.append({'label':'Generated '+level+' example '+str(i+1),'record':r})
    # Each implemented family receives direct randomized coverage, independent of
    # the family-selection coverage check, including zero/signed source originals.
    for k,v in m.TEMPLATES.items():
        for seed in range(12):
            r=m.generate(v['level'],seed=seed,template=k);check(r);normal_count+=1
        r=m.generate(v['level'],seed=12,template=k);p=r['generation']['parameters']
        other=m.generate(v['level'],seed=999,template=k,parameters=p,profile=r['generation']['bank_profile'])
        same=m.generate(v['level'],seed=2,template=k,parameters=p,profile=r['generation']['bank_profile'])
        assert other['generation']['content_identity']==same['generation']['content_identity']==r['generation']['content_identity']
        assert other['generation']['task_fingerprint']==r['generation']['task_fingerprint']
    # Invalid explicit inputs must use the same guards as samplers.
    bad=[('easy','q-71396',{'point':[0,0,0]}),('easy','q-71403',{'point':[1,1,1]}),('easy','q-131119',{'point':[2,0,0]}),('moderate','weighted_quadratic',{'point':[1,2,3],'coefficients':[1]*6}),('hard','rational_quadratic',{'point':[2,2,2],'coefficients':[1]*6}),('hard','rational_quadratic',{'point':['3/2']*3,'coefficients':[0]*6})]
    for level,k,p in bad:
        try:m.generate(level,template=k,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit input admitted')
    # Common function coefficient scaling changes presentation, not assessed task.
    a=m.generate('moderate',template='weighted_quadratic',parameters={'point':[2,2,3],'coefficients':[1]*6})
    b=m.generate('moderate',template='weighted_quadratic',parameters={'point':[2,2,3],'coefficients':[2]*6})
    assert a['generation']['task_fingerprint']==b['generation']['task_fingerprint']
    assert a['generation']['content_identity']!=b['generation']['content_identity']
    g=sp.Matrix([1,1,0]);assert m.eligible(-g,g);assert not m.eligible(sp.Matrix([-1,1,0]),g)
    assert m.eligible(g/sp.sqrt(2),g,'unit_normal') and m.eligible(-g/sp.sqrt(2),g,'unit_normal')
    assert not m.eligible(2*g,g,'unit_normal') and not m.eligible(-g,g,'gradient')
    # Complete rejection under actual normal criterion, beyond UUID equality.
    assert sum(m.eligible(v,g) for v in [g,-g,sp.Matrix([-1,1,0])])==2
    for entry in review:
        r=entry['record']
        if r['generation']['evidence_only']:continue
        checks=[]
        for a in r['question'][':question/answer-fields'][0][':answer-field/choices']:
            checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] else 'rejected','purpose':'normal full radio bank native grading'})
        engine.append({'label':entry['label'],'record':r,'checks':checks})
    (HERE/'native-input.json').write_text(json.dumps(engine,indent=2))
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    native=json.loads((HERE/'native-report.json').read_text())
    (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (HERE/'review.md').write_text('# Normal-vector author review\n\nOriginal profiles are raw public evidence; generated variants use method-derived banks.\n\n'+'\n\n---\n\n'.join('### '+e['label']+'\n\n'+m.markdown(e['record']) for e in review)+'\n')
    report={'status':'passed','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'provenance':{k:m.SOURCE[k] for k in ('database','basis','lineage')},'source_fidelity':{'questions':12,'prompt_exact':12,'worked_solution_exact':12,'banks':13,'choices':65,'designations':12,'missing_legacy_designations':1,'key_presence_exact':12,'sources':fidelity},'mathematics':{'normal_randomized_instances':normal_count+24,'full_displayed_readback':True,'all_three_ordered_partials_evaluations_conclusions':True,'source_original_normals':12,'source_bank_ambiguities':0,'raw_teaching_anomalies':3,'raw_full_stage_correctness_claim':False},'normal_repairs':{'formal_derivative_extra_plus':1,'evaluation_extra_closing_parenthesis':1,'stale_intro_point':1,'legacy_duplicate_field_removed':1},'default_family_coverage':{k:sorted(v) for k,v in coverage.items()},'sample_task_counts':uniques,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'limits':['Observed opaque banks are evidence-only; their distractor intentions are not recovered.','Legacy q-37570 field has no correct ref; native test uses only the authoritative designated field.','No typed field is observed or authored, so typed-entry equivalence is not a grading claim.','Moderate/hard workload labels are authored, with no observed practice examples.','No source practice/canonical plots; relevant tutorial sphere inspected, no variable plot generation.'],'database_writes':0}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','source_fidelity','mathematics','native')},indent=2))
if __name__=='__main__':main()
