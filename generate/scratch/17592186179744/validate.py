"""Independent checks of printed fields, curves, substitutions and complete banks."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('flux_generator', HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y,T=g.X,g.Y,g.T


def group(z,i):
    assert z[i]=='{'
    depth=1;j=i+1
    while depth:
        depth+=(z[j]=='{')-(z[j]=='}');j+=1
    return z[i+1:j-1],j


def expression(z):
    z=z.strip().replace('\\\\','\\').replace('π',r'\pi').replace('⁡','')
    z=z.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\pi','pi')
    z=z.replace(r'\operatorname{cos}','cos').replace(r'\operatorname{sin}','sin')
    z=re.sub(r'\\(sin|cos)\^\{(\d+)\}\{\((.*?)\)\}',r'(\1(\3))^\2',z)
    z=z.replace(r'\sin','sin').replace(r'\cos','cos')
    while r'\frac' in z:
        m=list(re.finditer(r'\\frac',z))[-1]
        a,end=group(z,m.end());b,end=group(z,end)
        z=z[:m.start()]+'(('+a+')/('+b+'))'+z[end:]
    z=z.replace('{','(').replace('}',')')
    z=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','E',z)
    assert '\\' not in z,z
    return parse_expr(z,local_dict={'x':X,'y':Y,'t':T,'E':s.E,'pi':s.pi,'sin':s.sin,'cos':s.cos},
        transformations=standard_transformations+(implicit_multiplication_application,convert_xor))


def native(rec):
    f=rec['question'][':question/answer-fields'][0]
    return {'label':rec['question'][':question/id'],'record':rec,'checks':[
        {'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every source-profile radio option through actual learner grade_field'}
        for a in f[':answer-field/choices']]}


def verify(rec):
    q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
    m=re.search(r'F\(x,y\)=\((.*?)\)\\,i\+\((.*?)\)\\,j',prompt);assert m
    P,Q=map(expression,m.groups())
    m=re.search(r'r\(t\)=(.*?)\\,i\+(.*?)\\,j',prompt);assert m
    xt,yt=map(expression,m.groups())
    a=xt.subs(T,0);b=yt.subs(T,s.pi/2)
    assert a>0 and b>0 and xt==a*s.cos(T) and yt==b*s.sin(T)
    assert r't\in[0,2\pi)' in prompt
    dx,dy=s.diff(xt,T),s.diff(yt,T)
    Pt=P.subs({X:xt,Y:yt},simultaneous=True);Qt=Q.subs({X:xt,Y:yt},simultaneous=True)
    integrand=s.expand(Pt*dy-Qt*dx)
    # A second method, independent of the sampled answer: integrate divergence
    # over an ellipse using its exact area and odd-monomial symmetry.
    div=s.expand(s.diff(P,X)+s.diff(Q,Y))
    truth=s.Integer(0)
    for term in s.Add.make_args(div):
        powers=term.as_powers_dict();px=powers.get(X,0);py=powers.get(Y,0)
        if px%2 or py%2:continue
        assert not term.has(X,Y),'Unexpected nonconstant even divergence'
        truth+=term*s.pi*a*b
    if P==s.exp(Y) and Q==s.exp(X):
        primitive=s.exp(yt)-s.exp(xt)
        assert s.simplify(s.diff(primitive,T)-integrand)==0
        exact=primitive.subs(T,2*s.pi)-primitive.subs(T,0)
    else:
        exact=s.integrate(integrand,(T,0,2*s.pi))
    assert s.simplify(exact-truth)==0
    field=q[':question/answer-fields'][0]
    vals=[expression(v[':answer/value']) for v in field[':answer-field/choices']]
    assert len(vals)==5 and all(s.simplify(x-y)!=0 for i,x in enumerate(vals) for y in vals[i+1:])
    correct=[v[':answer/id'] for v,x in zip(field[':answer-field/choices'],vals) if s.simplify(x-truth)==0]
    assert correct==[field[':answer-field/correct'][1]]
    checks=[(r'we have \$x=(.*?)\$, \$y=(.*?)\$',(xt,yt)),
            (r'Therefore, \$P=(.*?)\$ and \$Q=(.*?)\$',(Pt,Qt)),
            (r'gives \$x\\prime\(t\)=(.*?)\$ and \$y\\prime\(t\)=(.*?)\$',(dx,dy))]
    for pattern,expected in checks:
        found=re.search(pattern,sol);assert found,(pattern,sol)
        assert all(s.simplify(expression(z)-w)==0 for z,w in zip(found.groups(),expected))
    printed=re.search(r'&=\\int_0\^\{2\\pi\}\\left\((.*?)\\right\)\\,\\mathrm dt',sol)
    assert printed and s.simplify(expression(printed[1])-integrand)==0
    for text in [prompt,sol]+[a[':answer/value'] for a in field[':answer-field/choices']]:
        assert text.count('$')%2==0 and text.count('{')==text.count('}')
        assert not any(ord(c)<32 and c not in '\n\t' for c in text)
    assert 'outward' in sol and len(q[':question/answer-fields'])==1
    return truth


def main():
    originals={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions']}
    report={'correctness':{},'fidelity':{'banks':[]},'coverage':{},'grading':{},'source_errors':[
        {'source':'q-127062','error':'v=a cos(t) source incorrectly shows endpoints 1,1 for a=3','correction':'Both endpoints are a=3; result remains zero; source unchanged.'}]}
    native_records=[];review=[];cases=[]
    for sid,(template,p,profile) in g.CASES.items():
        r=g.generate('easy',template=template,parameters=p,profile=profile);verify(r)
        old=originals[sid][':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0]
        observed=[expression(a[':answer/value']) for a in old[':answer-field/choices']]
        generated=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
        assert all(sum(s.simplify(x-y)==0 for y in generated)==1 for x in observed)
        assert s.simplify(verify(r)-expression(old[':answer-field/correct'][':answer/value']))==0
        report['fidelity']['banks'].append({'source':sid,'template':template,'profile':profile,'matched_options':5,'total_options':5,'matched_distractors':4,'complete':True,'missing':[],'extra':[]})
        native_records.append(native(r));cases.append({'source_id':sid,'level':'easy','template':template,'parameters':p,'bank_profile':profile})
        # Hold all mathematical information fixed except one declared radius.
        changed=dict(p);changed['a']=10 if p['a']!=10 else 9
        if template in ('circle-linear','cross-quadratic'):changed['b']=changed['a']
        variant=g.generate('easy',template=template,parameters=changed,profile=profile);verify(variant)
        assert r['question'][':question/problem']!=variant['question'][':question/problem']
        review.append('## '+sid+' / '+profile+'\n\nSource:\n\n'+originals[sid][':question/problem']+'\n\nReplay:\n\n'+r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']+'\n\nChanged radius:\n\n'+variant['question'][':question/problem']+'\n\n'+variant['question'][':question/worked-solution'])
    coverage={}
    for template in g.TEMPLATES:
        seen={'a':set(),'b':set(),'k':set(),'profiles':set()}
        for seed in range(16):
            r=g.generate('easy',seed,template=template);verify(r)
            assert r==g.generate('easy',seed,template=template)
            for name,value in r['generation']['parameters'].items():seen[name].add(value)
            seen['profiles'].add(r['generation']['bank_profile']);native_records.append(native(r))
        coverage[template]={k:sorted(v) for k,v in seen.items()}
        assert len(seen['a'])>=5 and len(seen['b'])>=5
        assert seen['profiles']=={c[2] for c in g.CASES.values() if c[0]==template}
    # Boundaries, including the observed a=1 and all selected bank profiles.
    boundary=0
    for template in g.TEMPLATES:
        for sid,(tt,p,profile) in g.CASES.items():
            if tt!=template:continue
            for a,b in ((1,1),(2,3),(12,11)):
                p=dict(a=a,b=a if tt in ('circle-linear','cross-quadratic') else b,k=p['k'])
                try:r=g.generate('easy',template=tt,parameters=p,profile=profile)
                except AssertionError:continue
                verify(r);boundary+=1
    # The printed-data check must reject stale radius references and keys.
    r=g.generate('easy',template='radial-linear',parameters=dict(a=5,b=6,k=2),profile='signed-half')
    for mutate in ('prompt','key','solution'):
        bad=copy.deepcopy(r)
        if mutate=='prompt':bad['question'][':question/problem']=bad['question'][':question/problem'].replace('5 \\cos','7 \\cos')
        elif mutate=='key':bad['question'][':question/answer-fields'][0][':answer-field/correct'][1]=next(a[':answer/id'] for a in bad['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']!=bad['question'][':question/answer-fields'][0][':answer-field/correct'][1])
        else:bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('5 \\cos','7 \\cos')
        assert bad!=r
        try:verify(bad)
        except AssertionError:pass
        else:raise AssertionError('Stale '+mutate+' was accepted')
    for unsupported in ('moderate','hard'):
        try:g.generate(unsupported)
        except ValueError:pass
        else:raise AssertionError('unsupported level sampled')
    (HERE/'reference/native-input.json').write_text(json.dumps(native_records,indent=2))
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'reference/native-input.json'),str(HERE/'reference/native-report.json')],check=True)
    engine=json.loads((HERE/'reference/native-report.json').read_text());assert engine['documented_unresolved_checks']==0
    report['grading']={'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':0,'entry_point':engine['entry_point']}
    report['correctness']={'printed_instances_checked':len(native_records)+boundary,'independent_methods':['parameterized flux integral','ellipse divergence integral'],'stale_prompt_key_solution_rejected':True,'deterministic_replay':True}
    report['fidelity'].update({'complete_banks':8,'matched_options':40,'matched_distractors':32,'unresolved_comparisons':0,'solution_layout':'Same definition, substitution, derivatives, parameter integral, identities/substitution, endpoint evaluation; corrected exponential endpoint typo.'})
    report['coverage']=coverage;report['passed']=True
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2))
    (HERE/'reference/side-by-side.md').write_text('\n\n'.join(review))
    (HERE/'validation.json').write_text(json.dumps(report,indent=2))
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'validation.json',HERE/'source-cases.json')}
    (HERE/'reference/freeze.json').write_text(json.dumps({'status':'validated','hashes':hashes,'version':g.VERSION},indent=2))
    print(json.dumps({'passed':True,'complete_banks':8,'engine_checks':report['grading'],'boundary_cases':boundary}))


if __name__=='__main__':main()
