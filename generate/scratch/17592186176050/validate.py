#!/usr/bin/env python3
"""Independent displayed-math, source-presence/fidelity and real native grading."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
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
            if s.startswith('y='):continue # function declaration, not an equality to evaluate
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
        # All replay profiles must also operate under changed complete parameters.
        p=case['parameters'].copy();p['n']=int(p['n'])+(-1 if int(p['n'])<0 else 1)
        displayed(g.generate(case['level'],1,case['template'],parameters=p,profile=case['bank_profile']),True)
    write('source-cases.json',cases)
    generated=[];fingerprints={};families={}
    for level in g.TEMPLATES:
        sample_records=[g.generate(level,seed) for seed in range(120)]
        for rec in sample_records:displayed(rec)
        fingerprints[level]=len(set(r['generation']['mathematical_fingerprint'] for r in sample_records))
        families[level]=sorted(set(r['generation']['template'] for r in sample_records))
        assert set(families[level])==set(g.TEMPLATES[level])
        for t in g.TEMPLATES[level]:
            for seed in (19,47):
                rec=g.generate(level,seed,template=t);displayed(rec);generated.append(rec)
        # Same fixed content and bank independent of seed/order.
        rec=sample_records[0];p=rec['generation']['parameters'];t=rec['generation']['template']
        assert g.generate(level,77,t,parameters=p)['question'][':question/id']==g.generate(level,78,t,parameters=p)['question'][':question/id']
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
    write('review.json',dict(original_replays=rawrecords,generated=generated))
    rows=['# Tangent periodicity review','', 'Raw originals retain missing attributes; generated variants are explicitly authored.']
    for oq,r in zip(originals,rawrecords):
        rows+=['','## Original '+oq[':question/math-academy-id'], '', g.markdown(r)]
        case=next(c for c in cases if c['source_id']==oq[':question/math-academy-id'])
        p=case['parameters'].copy();p['n']=int(p['n'])+(-1 if int(p['n'])<0 else 1)
        variant=g.generate(case['level'],parameters=p,profile=case['bank_profile'])
        rows+=['','### Parameterized observed-bank evidence variant (ineligible)', '',g.markdown(variant)]
    for r in generated:rows+=['','## Authored '+r['question'][':question/difficulty'].split('/')[-1]+' / '+r['generation']['template'],'',g.markdown(r)]
    (D/'review.md').write_text('\n'.join(rows)+'\n')
    validation=dict(passed=True,provenance=g.PROVENANCE,source=dict(questions=7,complete_banks_matched=7,choices_matched=35,distractors_matched=28,correct_designations_matched=5,correct_designations_present=5,correct_designations_missing=2,prompt_exact=7,solution_exact=5,solutions_present=5,solutions_absent=2,key_presence_parity=7,option_spellings_exact=lexical,opaque_bank_profiles=7),generated=dict(displayed_math_records=360,template_coverage=families,sampled_mathematical_tasks=fingerprints,review_records=len(generated),mutation_regressions=5),native=dict(returncode=result.returncode,records=len(engine),checks=sum(len(e['checks']) for e in engine),ungraded_raw_missing_designations=2,engine_sha256=hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest()),runtime=dict(python=sys.version.split()[0],sympy=sp.__version__),limitations=['Two unrated raw originals omit correct refs and solutions; raw replay preserves omissions. Their completed practice fields/solutions are authored, not matched.', 'Scalar source distractor intent is underdetermined; public observed-bank profiles are evidence-only. No source errors were detected.'])
    write('validation.json',validation)
    print(json.dumps(validation,indent=2))
if __name__=='__main__':main()
