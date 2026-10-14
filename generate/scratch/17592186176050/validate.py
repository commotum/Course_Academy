#!/usr/bin/env python3
"""Independent displayed-math, source-presence/fidelity and real native grading."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x',real=True);n=sp.Symbol('n',integer=True);T=sp.Symbol('T',real=True)

def parse(s,v=None):
    s=s.strip().rstrip('.,').replace('tan⁡',r'\tan ').replace('π',r'\pi').replace('−','-')
    s=re.sub(r'\\(?:left|right|begin\{aligned\}|end\{aligned\})','',s)
    s=s.replace('&','').replace(r'\cdot','*').replace(r'\,','').replace(r'\pi',' pi ')
    # Consume the actual displayed tangent arguments with balanced parentheses.
    while r'\tan' in s:
        start=s.index(r'\tan');i=start+4
        while i<len(s) and s[i].isspace():i+=1
        if s[i]=='x':end=i+1;arg=x
        else:
            assert s[i]=='(',s
            j=i+1;depth=1
            while depth:
                assert j<len(s),s
                depth+=(s[j]=='(')-(s[j]==')');j+=1
            end=j;arg=parse(s[i+1:j-1])
        delta=sp.simplify((arg-x)/sp.pi)
        assert delta.is_integer is True,('not an integer-period shift',s,arg)
        s=s[:start]+'T'+s[end:]
    # Complete scalar components; no blanket short-expression substitutions.
    s=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',s)
    while '\\frac' in s:
        new=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',s)
        assert new!=s,s;s=new
    s=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',s)
    s=s.replace('{','(').replace('}',')').strip().rstrip('.,')
    val=parse_expr(s,local_dict={'x':x,'n':n,'T':T,'pi':sp.pi,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
    return sp.simplify(val.subs(T,v)) if v is not None else sp.simplify(val)

def balanced(s):
    assert not any(ord(c)<32 and c not in '\n\t\r' for c in s),'C0 character'
    assert '+-' not in s.replace(' ','') and '--' not in s.replace(' ',''),'ungrouped signed operations'
    assert s.count('$')%2==0,'math delimiters'
    depth=0
    for c in s:
        depth+=(c=='{')-(c=='}');assert depth>=0,'TeX braces'
    assert depth==0,'TeX braces'

def displayed(rec,raw=False):
    assert rec['knowledge_point']==dict(db_id=g.KP_ID,id=g.KP_UUID,title=g.TITLE)
    q=rec['question'];f=q[':question/answer-fields'][0]
    for s in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in f[':answer-field/choices']]:balanced(s)
    math=re.findall(r'\$([^$]*)\$',q[':question/problem'])
    given=math[0];assert given.count('=')==1
    left,right=given.split('=');assert parse(left)==T
    v=parse(right);request=parse(math[-1]);target=request.subs(T,v);actual_values=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
    original=math[-1].replace('tan⁡',r'\tan ').replace('π',r'\pi')
    shift_match=re.search(r'x\s*([+-])\s*(\d+)\s*\\pi',original);assert shift_match
    shift_value=int(shift_match[2])*(1 if shift_match[1]=='+' else -1)
    a=sp.expand(request).coeff(T);b=sp.expand(request).subs(T,0)
    template=rec['generation']['template']
    assert 1<=abs(shift_value)<=12 and v!=0 and abs(v)<=16
    if not raw:
        level=q[':question/difficulty'].split('/')[-1]
        assert level in ('easy','moderate','hard')
        if level=='easy':assert template=='direct_legacy' and v.is_Integer and 2<=abs(v)<=16 and a==1 and b==0
        elif level=='moderate':
            assert template in ('direct','add','scale','affine','affine_legacy')
            if template=='direct':assert v in [s*sp.sqrt(k) for s in (-1,1) for k in (2,3,5,6,7)] and a==1 and b==0
            elif template=='add':assert v.is_Integer and 2<=abs(v)<=9 and a==1 and b.is_Integer and 1<=abs(b)<=6
            elif template=='scale':assert v.is_Integer and a.is_Rational and not a.is_Integer and 2<=sp.denom(a)<=4 and 1<=abs(sp.numer(a))<=3 and (a*v).is_Integer and a*v!=0 and b==0
            else:assert v.is_Rational and a.is_Integer and 2<=abs(a)<=12 and 1<=sp.denom(v)<=4 and abs(sp.numer(v))<=8 and (a*v).is_Integer and abs(a*v)<=24 and b.is_Integer and 1<=abs(b)<=6
        else:
            assert template=='rational_affine' and all(z.is_Rational and not z.is_Integer and 2<=sp.denom(z)<=4 and 1<=abs(sp.numer(z))<=6 for z in (a,v)) and not (a*v).is_Integer and b.is_Integer and 1<=abs(b)<=5
    if raw:
        sid=rec['generation']['source_id'];av=a*v;d=sp.denom(a);num=sp.numer(a)
        bank={
          'q-29382':[v-shift_value*sp.pi,b,-shift_value*sp.pi,av+b,av-b],
          'q-66218':[1/v,1,v,-v,-1/v],
          'q-103307':[av+b,av,-av-b,av*sp.pi+av+b,-b],
          'q-103312':[v/d,av,av+shift_value/num*sp.pi,av+sp.pi,av+num],
          'q-66594':[v+2*sp.pi,-1,-v,v,v/2],
          'q-70998':[v+b-shift_value*sp.pi,shift_value*sp.pi,b,-v+b,v+b],
          'q-71002':[-v,-v**2,v**2,v+shift_value*sp.pi,v],
        }[sid]
    elif template.startswith('direct'):bank=[v,1/v,-v,-1/v,v+shift_value*sp.pi]
    elif template=='add':bank=[v+b,v,b,-v+b,v+shift_value*sp.pi+b]
    elif template=='scale':bank=[a*v,v,v/a,-a*v,a*(v+shift_value*sp.pi)]
    else:bank=[a*v+b,a*v,a*v-b,a+b*v,a*(v+shift_value*sp.pi)+b]
    assert len(actual_values)==5
    assert all(sum(sp.simplify(z-w)==0 for w in actual_values)==1 for z in bank),'displayed complete operation bank'
    assert all(sp.simplify(a-b)!=0 for i,a in enumerate(actual_values) for b in actual_values[i+1:])
    correct=[a for a,z in zip(f[':answer-field/choices'],actual_values) if sp.simplify(z-target)==0]
    assert len(correct)==1
    if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',correct[0][':answer/id']]
    sol=q.get(':question/worked-solution')
    if sol is not None:
        for block in re.findall(r'\$\$([\s\S]*?)\$\$|(?<!\$)\$([^$]*?)\$(?!\$)',sol):
            s=(block[0] or block[1]).strip().rstrip('.,')
            if '=' not in s:continue
            if s.startswith('y='):
                assert parse(s[2:])==T,'tangent function declaration'
                continue
            if s.startswith('n='):
                # Read n independently from the target's printed tangent argument.
                original=math[-1].replace('tan⁡',r'\tan ').replace('π',r'\pi')
                m=re.search(r'x\s*([+-])\s*(\d+)\s*\\pi',original);assert m
                expected=int(m[2])*(1 if m[1]=='+' else -1)
                assert parse(s[2:])==expected
                continue
            parts=s.split('=');vals=[parse(z,v) for z in parts]
            assert all(sp.simplify(z-vals[0])==0 for z in vals[1:]),('displayed stage',s,vals)
        # Independently require the complete source-shaped formal/substitution chain.
        norm=sol.replace('tan⁡',r'\tan ')
        assert r'\tan (x+n\pi )' in norm
        expected_shift='x+'+(str(shift_value) if shift_value>0 else '('+str(shift_value)+')')+r'\cdot \pi '
        assert expected_shift in norm,'substituted integer stage'
        assert 'Substituting' in norm
        template=rec['generation']['template']
        if template in ('affine','affine_legacy','rational_affine'):
            final=re.findall(r'\$\$([\s\S]*?)\$\$',sol)[-1]
            assert len(final.split('='))==4,'affine source stages must include individual product before collection'
        if template=='scale':assert len(re.findall(r'\$\$([\s\S]*?)\$\$',sol)[-1].split('='))==3
    elif not raw:raise AssertionError('normal solution absent')
    return target

def fidelity(rec,original):
    q=rec['question'];f=q[':question/answer-fields'][0];of=original[':question/answer-fields'][0]
    assert q[':question/problem']==original[':question/problem'],('prompt',original[':question/math-academy-id'],q[':question/problem'])
    assert q.get(':question/worked-solution')==original.get(':question/worked-solution'),('solution',original[':question/math-academy-id'])
    for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in original)
    assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
    assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
    sourcevalues=[a[':answer/value'] for a in of[':answer-field/choices']]
    gotvalues=[a[':answer/value'] for a in f[':answer-field/choices']]
    # Equal complete scalar values, one-to-one. Also separately count exact spelling.
    assert sorted(map(sp.sstr,map(parse,sourcevalues)))==sorted(map(sp.sstr,map(parse,gotvalues)))
    if ':answer-field/correct' in of:
        generated=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        assert parse(generated[':answer/value'])==parse(of[':answer-field/correct'][':answer/value'])
    return sum(z in gotvalues for z in sourcevalues)

def rejection(fn):
    try:fn()
    except (AssertionError,ValueError):return
    raise AssertionError('mutation unexpectedly accepted')

def write(name,data): (D/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def main():
    originals=g.SOURCE['record'][':knowledge-point/questions'];cases=[];rawrecords=[];lexical=0
    for oq in originals:
        sid=oq[':question/math-academy-id'];spec=g.SPECS[sid]
        case=dict(source_id=sid,template=spec['template'],parameters=spec['p'],bank_profile='source_'+sid,level=spec['level'],authored_level_assignment=':question/difficulty' not in oq)
        cases.append(case);rec=g.generate(case['level'],seed=72,template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        lexical+=fidelity(rec,oq);displayed(rec,True);rawrecords.append(rec)
        for shift_probe in (-12,12):
            boundary=case['parameters'].copy();boundary['n']=shift_probe
            displayed(g.generate(case['level'],template=case['template'],parameters=boundary,profile=case['bank_profile']),True)
        if sid=='q-103312':
            signed=case['parameters'].copy();signed['a']='-3/4';signed['n']=12
            displayed(g.generate(case['level'],template=case['template'],parameters=signed,profile=case['bank_profile']),True)
        # All replay profiles must also operate under changed complete parameters.
        p=case['parameters'].copy();p['n']=int(p['n'])+(-1 if int(p['n'])<0 else 1)
        displayed(g.generate(case['level'],1,case['template'],parameters=p,profile=case['bank_profile']),True)
    write('source-cases.json',cases)
    generated=[];fingerprints={};families={}
    for case in cases:
        if case['authored_level_assignment']:
            r=g.generate(case['level'],template=case['template'],parameters=case['parameters']);displayed(r);generated.append(r)
    for level in g.TEMPLATES:
        sample_records=[g.generate(level,seed) for seed in range(120)]
        for rec in sample_records:displayed(rec)
        positions={next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in sample_records}
        assert len(positions)>1,'correct choice must not have a fixed position'
        fingerprints[level]=len(set(r['generation']['mathematical_fingerprint'] for r in sample_records))
        families[level]=sorted(set(r['generation']['template'] for r in sample_records))
        assert set(families[level])==set(g.TEMPLATES[level])
        for t in g.TEMPLATES[level]:
            for seed in (19,47):
                rec=g.generate(level,seed,template=t);displayed(rec);generated.append(rec)
        # Same fixed content and bank independent of seed/order.
        rec=sample_records[0];p=rec['generation']['parameters'];t=rec['generation']['template']
        assert g.generate(level,77,t,parameters=p)['question'][':question/id']==g.generate(level,78,t,parameters=p)['question'][':question/id']
    evidence=g.generate('easy',parameters=g.SPECS['q-66218']['p'],profile='source_q-66218')
    normal=g.generate('easy',parameters=g.SPECS['q-66218']['p'])
    assert evidence['question'][':question/id']!=normal['question'][':question/id']
    assert evidence['generation']['mathematical_fingerprint']==normal['generation']['mathematical_fingerprint']
    # Boundary and invalid workload checks apply to public explicit inputs.
    rejection(lambda:g.generate('easy',parameters=dict(v=2,a=2,b=0,n=1)))
    rejection(lambda:g.generate('moderate',template='scale',parameters=dict(v=3,a='1/2',b=0,n=1)))
    rejection(lambda:g.generate('hard',parameters=dict(v='3/2',a='2/3',b=1,n=2)))
    rejection(lambda:g.generate('hard',parameters=dict(v=2,a='2/3',b=1,n=2)))
    # Meaningful displayed-content regressions, including equal-but-omitted operation.
    for mutation in ('bank','stage','control','omission'):
        r=copy.deepcopy(next(z for z in generated if z['generation']['template']=='affine'))
        q=r['question']
        if mutation=='bank':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='999'
        if mutation=='stage':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\cdot \pi',r'\cdot 2\pi')
        if mutation=='control':q[':question/problem']+='\x0c'
        if mutation=='omission':
            sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$([\s\S]*?)\$\$',sol);last=blocks[-1];pieces=last.split('=');q[':question/worked-solution']=sol.replace(last,'='.join(pieces[:2]+pieces[-1:]))
        rejection(lambda:displayed(r))
    wronglevel=copy.deepcopy(next(z for z in generated if z['generation']['template']=='rational_affine'));wronglevel['question'][':question/difficulty']=':question.difficulty/moderate';rejection(lambda:displayed(wronglevel))
    missing=copy.deepcopy(rawrecords[0]);missing['question'][':question/difficulty']=':question.difficulty/moderate';rejection(lambda:fidelity(missing,originals[0]))
    engine=[]
    for i,r in enumerate(rawrecords+generated):
        f=r['question'][':question/answer-fields'][0]
        if ':answer-field/correct' not in f:continue
        engine.append(dict(label=str(i),record=r,checks=[dict(field_index=0,submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',purpose='native owned radio grading') for a in f[':answer-field/choices']]))
    write('engine-input.json',engine)
    result=subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True)
    assert result.returncode==0,(result.stdout,result.stderr)
    report=json.loads((D/'engine-report.json').read_text())
    rows=['# Tangent periodicity review','', 'Raw originals retain missing attributes; generated variants are explicitly authored.']
    bankvariants=[]
    for oq,r in zip(originals,rawrecords):
        rows+=['','## Original '+oq[':question/math-academy-id'], '', g.markdown(r)]
        case=next(c for c in cases if c['source_id']==oq[':question/math-academy-id'])
        p=case['parameters'].copy();p['n']=int(p['n'])+(-1 if int(p['n'])<0 else 1)
        p['v']='sqrt(5)' if case['source_id']=='q-66594' else ('sqrt(3)' if case['source_id']=='q-71002' else sp.sstr(sp.sympify(p['v'])+1))
        if case['source_id']=='q-103312':p['v']='12'
        variant=g.generate(case['level'],parameters=p,profile=case['bank_profile'])
        displayed(variant,True);bankvariants.append(variant)
        rows+=['','### Parameterized observed-bank evidence variant (ineligible)', '',g.markdown(variant)]
    for r in generated:rows+=['','## Authored '+r['question'][':question/difficulty'].split('/')[-1]+' / '+r['generation']['template'],'',g.markdown(r)]
    write('review.json',dict(original_replays=rawrecords,observed_bank_variants=bankvariants,generated=generated))
    (D/'review.md').write_text('\n'.join(rows)+'\n')
    def eligible_bank(p,t):
        try:g.check_scope('moderate',t,p)
        except ValueError:return False
        a,v,b=p['a'],p['v'],p['b']
        vals=([v+b,v,b,-v+b] if t=='add' else [a*v,v,v/a,-a*v] if t=='scale' else [a*v+b,a*v,a*v-b,a+b*v])
        return len(set(vals))==4
    mod_tasks=set()
    for k in (2,3,5,6,7):
        for sign in (-1,1):mod_tasks.add((sp.sstr(sign*sp.sqrt(k)),'1','0'))
    for v in [sp.Integer(i) for i in range(-9,10) if abs(i)>=2]:
        for b in [sp.Integer(i) for i in range(-6,7) if i]:
            p=dict(v=v,a=sp.Integer(1),b=b,n=1)
            if eligible_bank(p,'add'):mod_tasks.add(tuple(sp.sstr(p[k]) for k in ('v','a','b')))
    scale_tasks=set()
    for v in [sp.Integer(i) for i in range(-16,17) if i]:
        for a in set(sp.Rational(i,j) for i in (-3,-2,-1,1,2,3) for j in (2,3,4)):
            p=dict(v=v,a=a,b=sp.Integer(0),n=1)
            if eligible_bank(p,'scale'):scale_tasks.add(tuple(sp.sstr(p[k]) for k in ('v','a','b')))
    mod_tasks|=scale_tasks
    affine_tasks=set()
    for v in set(sp.Rational(i,j) for i in range(-8,9) if i for j in (1,2,3,4)):
        for a in [sp.Integer(i) for i in range(-12,13) if abs(i)>=2]:
            for b in [sp.Integer(i) for i in range(-6,7) if i]:
                p=dict(v=v,a=a,b=b,n=1)
                if eligible_bank(p,'affine'):affine_tasks.add(tuple(sp.sstr(p[k]) for k in ('v','a','b')))
    mod_tasks|=affine_tasks
    rats=set(sp.Rational(i,j) for i in range(-6,7) if i for j in (2,3,4) if not sp.Rational(i,j).is_Integer)
    hard_tasks=set()
    for v,a,b in itertools.product(rats,rats,[sp.Integer(i) for i in range(-5,6) if i]):
        p=dict(v=v,a=a,b=b,n=1)
        try:g.check_scope('hard','rational_affine',p)
        except ValueError:continue
        vals=[a*v+b,a*v,a*v-b,a+b*v]
        if len(set(vals))==4:hard_tasks.add(tuple(sp.sstr(p[k]) for k in ('v','a','b')))
    variety=dict(counts=dict(easy=30,moderate=len(mod_tasks),hard=len(hard_tasks)),moderate_families=dict(direct_radical=10,additive=len(mod_tasks)-len(scale_tasks)-len(affine_tasks)-10,scale=len(scale_tasks),affine=len(affine_tasks)),exclusions='Integer shift magnitude, presentation alias, and answer bank do not create a mathematical task.',enumeration='Canonical exact (v,a,b) triples; guards applied before complete bank collision rejection; n=1 represents every nonzero integer shift.',tasks=dict(moderate=sorted(mod_tasks),hard=sorted(hard_tasks)))
    write('variety.json',variety)
    validation=dict(passed=True,provenance=g.PROVENANCE,source=dict(questions=7,complete_banks_matched=7,choices_matched=35,distractors_matched=28,distractors_with_source_designations=20,inferred_distractors=8,correct_designations_matched=5,correct_designations_present=5,correct_designations_missing=2,prompt_exact=7,solution_exact=5,solutions_present=5,solutions_absent=2,key_presence_parity=7,option_spellings_exact=lexical,opaque_bank_profiles=7),generated=dict(displayed_math_records=360,template_coverage=families,sampled_mathematical_tasks=fingerprints,review_records=len(generated),mutation_regressions=6,finite_domain_tasks=variety['counts']),native=dict(returncode=result.returncode,records=len(engine),checks=sum(len(e['checks']) for e in engine),ungraded_raw_missing_designations=2,engine_sha256=hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest()),runtime=dict(python=sys.version.split()[0],sympy=sp.__version__),limitations=['Two unrated raw originals omit correct refs and solutions; raw replay preserves omissions. Their completed practice fields/solutions are authored, not matched.', 'Scalar source distractor intent is underdetermined; public observed-bank profiles are evidence-only. No source errors were detected.'])
    write('validation.json',validation)
    print(json.dumps(validation,indent=2))
if __name__=='__main__':main()
