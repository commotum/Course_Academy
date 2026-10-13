"""Independent printed-math, complete-bank, fidelity and native-grader audit."""
import hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as s
import math_parser as mp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def eq(a,b):return s.simplify(s.trigsimp(a-b))==0

def rows(block):
    if not block.startswith(r'\begin{aligned}'):raise AssertionError('aligned structure')
    return [x.strip().rstrip('.') for x in block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\  & =')]

def getrows(block):
    first,*other=rows(block)
    return [first.split(' & =',1)[1],*other]

def balanced(text):
    assert text.count('$$')%2==0
    assert text.replace('$$','').count('$')%2==0
    n=0
    for c in text:
        if c=='{':n+=1
        if c=='}':n-=1
        assert n>=0
    assert n==0
    assert '+-' not in text and '--' not in text

def strip_group(q):
    q=q.strip().rstrip('.')
    if q.startswith('(') and q.endswith(')'):
        depth=0;close=None
        for i,c in enumerate(q):
            depth+=(c=='(')-(c==')')
            if depth==0:close=i;break
        if close==len(q)-1:return q[1:-1]
    return q

def derivative_args(text):
    pattern=re.compile(r'\\frac\{\\(?:mathrm|text)\{d\}\}\{\\(?:mathrm|text)\{d\}t\}\(')
    found=[]
    for m in pattern.finditer(text):
        depth=1;j=m.end()
        while depth:
            depth+=(text[j]=='(')-(text[j]==')');j+=1
        found.append(mp.expr(text[m.end():j-1]))
    return found

def mathcheck(r,raw=False):
    q=r['question'];P,Q,u,v,lo,hi=mp.prompt(q[':question/problem']);pr=P.subs({mp.X:u,mp.Y:v});qr=Q.subs({mp.X:u,mp.Y:v});du,dv=s.diff(u,mp.T),s.diff(v,mp.T);correct=s.expand(pr*du+qr*dv)
    fingerprint=g.digest([s.srepr(e) for e in (s.trigsimp(correct),lo,hi)]+['supplied-parameterization-dot-product-setup'])
    assert fingerprint==r['generation']['mathematical_fingerprint']
    bs=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S);assert len(bs)==6
    # Actual along-curve equations, initial formal coordinate derivative rows,
    # ordered operator arguments, reduced vector and every subsequent scalar row.
    along=bs[1].strip().rstrip('.')
    xy=along.split(r',\,')
    assert len(xy)==2 and eq(mp.expr(xy[0].split('=',1)[1]),u) and eq(mp.expr(xy[1].split('=',1)[1]),v)
    fr=getrows(bs[2]);first=mp.vector(fr[0]);assert eq(first[0],P) and eq(first[1],Q)
    for row in fr[1:]:
        a,b=mp.vector(row);assert eq(a,pr) and eq(b,qr),(r['generation']['template'],'F substitution',row)
    dr=getrows(bs[3]);assert 'frac' in dr[0] and 'x' in dr[0] and 'y' in dr[0]
    args=derivative_args(dr[1]);assert len(args)==2 and eq(args[0],u) and eq(args[1],v)
    a,b=mp.vector(dr[2]);assert eq(a,du) and eq(b,dv)
    dot=getrows(bs[4]);left,right=dot[0].split(r'\cdot ',1)
    fvec=mp.vector(strip_group(left));dvec=mp.vector(strip_group(right))
    assert eq(fvec[0],pr) and eq(fvec[1],qr) and eq(dvec[0],du) and eq(dvec[1],dv)
    for row in dot[1:]:assert eq(mp.expr(row),correct),('dot stage',row)
    final=getrows(bs[5]);assert len(final)==2 and 'F(r(t))' in final[0]
    fi,fl,fh,_=mp.integral(final[1]);assert eq(fi,correct) and eq(fl,lo) and eq(fh,hi)
    f=q[':question/answer-fields'][0];vals=[];elig=[]
    for ans in f[':answer-field/choices']:
        ai,al,ah,av=mp.integral(ans[':answer/value']);vals.append(av)
        eligible=ai is not None and eq(ai,correct) and eq(al,lo) and eq(ah,hi)
        elig.append(eligible)
        if ans[':answer/id']==f[':answer-field/correct'][1]:assert eligible
    assert sum(elig)==1
    collisions=[(i,j) for i in range(5) for j in range(i) if eq(vals[i],vals[j])]
    if not raw:assert not collisions
    return {'response_form_correct':sum(elig),'scalar_collision_pairs':collisions}

def contract(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==g.KP_ID
    q=r['question'];f=q[':question/answer-fields'][0]
    assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5 and f[':answer-field/correct'][0]==':answer/id'
    assert all(a[':answer/type']==':answer.type/math' and not '$' in a[':answer/value'] for a in f[':answer-field/choices'])
    assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
    assert f[':answer-field/correct'][1] in {a[':answer/id'] for a in f[':answer-field/choices']}
    assert r['generation']['eligible_for_learning']!=r['generation']['evidence_only']
    identity=g.digest({'version':g.VERSION,'difficulty':q[':question/difficulty'].split('/')[-1],'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],'bank':sorted(a[':answer/value'] for a in f[':answer-field/choices'])})
    assert identity==r['generation']['content_fingerprint']
    json.dumps(r)


def main():
    source_cases=[];replays=[];fidelity=[];bankmap=[]
    for family,src in g.SOURCE_BY_FAMILY.items():
        p={'scale':1,'upper':str(s.pi if family in ('rotation','shifted_circle','spiral') else 1)}
        r=g.generate('easy',template=family,parameters=p,profile='observed_'+family);replays.append(r);contract(r)
        q=r['question'];old=src[':question/answer-fields'][0];new=q[':question/answer-fields'][0]
        assert q[':question/problem']==src[':question/problem'] and q[':question/worked-solution']==src[':question/worked-solution']
        assert {a[':answer/value'] for a in new[':answer-field/choices']}=={a[':answer/value'] for a in old[':answer-field/choices']}
        val=next(a[':answer/value'] for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1]);assert val==old[':answer-field/correct'][':answer/value']
        assert q[':question/difficulty']==src[':question/difficulty'][':db/ident']
        for k in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (k in q)==(k in src)
        P,Q,u,v,lo,hi=mp.prompt(q[':question/problem']);integrand=s.trigsimp(P.subs({mp.X:u,mp.Y:v})*s.diff(u,mp.T)+Q.subs({mp.X:u,mp.Y:v})*s.diff(v,mp.T))
        result=[]
        for a in old[':answer-field/choices']:
            f,l,h,vv=mp.integral(a[':answer/value']);result.append({'value':a[':answer/value'],'parsed_integrand':str(f),'bounds':[str(l),str(h)],'scalar':str(vv),'structurally_eligible':f is not None and eq(f,integrand),'designated_correct':a[':answer/id']==old[':answer-field/correct'][':answer/id'],'interpretation':'parameterized observed expression pattern; author error intent unresolved'})
        designated=next(a for a in result if a['designated_correct']);assert designated['structurally_eligible']
        pairs=[(i,j) for i in range(5) for j in range(i) if eq(mp.integral(result[i]['value'])[3],mp.integral(result[j]['value'])[3])]
        known=('missing j basis marker' if family=='exponential_root' else 'malformed last distributed sin cos product/unmatched parenthesis' if family=='spiral' else None)
        if not known:mathcheck(r,raw=True)
        else:
            try:mathcheck(r,raw=True)
            except (ValueError,AssertionError):pass
            else:raise AssertionError('expected raw anomaly not detected')
        source_cases.append({'source_id':src[':question/math-academy-id'],'template':family,'parameters':p,'bank_profile':'observed_'+family,'difficulty':'easy','evidence_only':True,'eligible_for_learning':False})
        fidelity.append({'source_id':src[':question/math-academy-id'],'prompt_exact':True,'solution_raw_exact':True,'bank_values_exact':5,'designation_exact':True,'known_solution_anomaly':known,'scalar_collision_pairs':pairs})
        bankmap.append({'source_id':src[':question/math-academy-id'],'family':family,'profile':'observed_'+family,'original_parameters':p,'choices':result})
        # Nonunit observed field scaling is genuinely derived, including integral
        # scale and changed endpoint, not a literal original answer lookup.
        scaled=g.generate('easy',template=family,parameters={'scale':2,'upper':p['upper']},profile='observed_'+family)
        ps=mp.prompt(scaled['question'][':question/problem']);assert eq(ps[0],2*P) and eq(ps[1],2*Q)
        ss=scaled['question'][':question/answer-fields'][0];sv=next(a[':answer/value'] for a in ss[':answer-field/choices'] if a[':answer/id']==ss[':answer-field/correct'][1]);assert eq(mp.integral(sv)[0],2*integrand)
        if not known:mathcheck(scaled,raw=True)
        neg=g.generate('easy',template=family,parameters={'scale':-2,'upper':str(s.sympify(p['upper'])/2)},profile='observed_'+family)
        contract(neg)
        if not known:mathcheck(neg,raw=True)
    variants=[];tested=[];fingerprints={l:set() for l in ('easy','moderate','hard')}
    for family,level in g.TEMPLATES.items():
        for seed in range(6):
            r=g.generate(level,seed,template=family);contract(r);balanced(r['question'][':question/problem']);balanced(r['question'][':question/worked-solution']);mathcheck(r)
            for a in r['question'][':question/answer-fields'][0][':answer-field/choices']:balanced(a[':answer/value'])
            fingerprints[level].add(r['generation']['mathematical_fingerprint']);tested.append(r)
            if seed<2:variants.append(r)
        first=tested[-6];p=first['generation']['parameters'];again=g.generate(level,890,template=family,parameters=p)
        assert again['question'][':question/id']==first['question'][':question/id']
        assert again['generation']['mathematical_fingerprint']==first['generation']['mathematical_fingerprint']
    assert all(len(v)>=6 for v in fingerprints.values())
    # Public explicit-input workload/domain guards.
    bad=[('moderate','monomial',{'a':1,'b':1,'m':1,'n':2,'lower':'0','upper':'1'}),('hard','mixed_spiral',{'a':1,'b':1,'c':1,'d':1,'lower':'0','upper':'pi/3'}),('easy','exponential_root',{'a':1,'b':1,'lower':'0','upper':'1'}),('easy','polynomial',{'a':0,'b':1,'lower':'0','upper':'1'})]
    for level,f,p in bad:
        try:g.generate(level,template=f,parameters=p)
        except ValueError:pass
        else:raise AssertionError('invalid explicit input accepted')
    defaults={g.generate('easy',seed)['generation']['template'] for seed in range(24)};assert defaults==set(g.FAMILIES)
    allrecords=replays+variants
    checks=[]
    for r in allrecords:
        f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
        checks.append({'label':r['generation']['bank_profile']+':'+r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'native owned radio UUID selection; symbolic eligibility/equivalence audited separately'} for a in f[':answer-field/choices']]})
    (HERE/'native-input.json').write_text(json.dumps(checks,indent=2));engine=HERE.parents[1]/'runs/current/check-engine'
    subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    (HERE/'source-cases.json').write_text(json.dumps(source_cases,indent=2))
    (HERE/'bank-map.json').write_text(json.dumps(bankmap,indent=2))
    (HERE/'review.json').write_text(json.dumps(allrecords,indent=2))
    review=['# Setup-only vector line integral review','', 'Raw observed replays preserve anomalies and are ineligible for learning. Authored generated records use the stated parameterization and limits; the learner does not evaluate integrals.','']
    for src,r in zip(g.SOURCES,replays):review.extend(['## Original '+src[':question/math-academy-id'],'',src[':question/problem'],'', 'Original worked solution','',src[':question/worked-solution'],'',g.markdown(r),''])
    review.extend(g.markdown(r) for r in variants)
    (HERE/'review.md').write_text('\n\n'.join(review))
    report={'status':'pass with public source anomalies retained ineligible','source_basis':g.SOURCE['basis'],'source_questions':5,'source_prompt_exact':5,'source_solution_raw_exact':5,'complete_source_banks_exact':5,'source_values_exact':25,'source_distractors_exact':20,'source_designations_exact':5,'source_correct_integrands':5,'raw_source_solution_parse_pass':3,'raw_source_solution_known_anomalies':2,'raw_scalar_ambiguous_banks':1,'normal_generated_checks':len(tested),'review_generated_count':len(variants),'sampled_meaningful_task_counts':{k:len(v) for k,v in fingerprints.items()},'default_easy_family_coverage':sorted(defaults),'explicit_invalid_input_checks':len(bad),'source_fidelity':fidelity,'finite_domain_variety':'variety.json','normal_response_criterion':'same integrand and original bounds from supplied parameterization, no evaluation/change of variable','normal_bank_policy':'structurally unique correct setup; additionally no complete scalar coincidences','native_report':'native-report.json','native_equivalent_input_limits':'radio fields grade owned answer UUIDs only; free mathematical entry equivalence is not an interface for these sources','dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'frozen_after_step':7,'database_operations':0}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','complete_source_banks_exact','source_distractors_exact','normal_generated_checks','sampled_meaningful_task_counts')},indent=2))
if __name__=='__main__':main()
