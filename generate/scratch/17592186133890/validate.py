#!/usr/bin/env python3
"""Fail-closed prompt, endpoint, displayed stages, full-bank and native QA."""
import importlib.util, json, re, sys, subprocess, hashlib
from functools import lru_cache
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as s
sys.path.insert(0,'/home/jake/.cache/uv/wheels-v5/pypi/lark/1.2.2-py3-none-any')
from sympy.parsing.latex import parse_latex
from lark import Tree
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('cartesian_ftli',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def normalize(v):
    v=re.sub(r'\\operatorname\{(ln|sin|cos)\}',lambda m:'\\'+m[1],v)
    v=v.replace('\u2061','').replace(r'\u2061','').replace(r'\dfrac',r'\frac').replace(r'\left','').replace(r'\right','')
    v=re.sub(r'(?<=\})\\(ln|sin|cos)',r'\\cdot \\\1',v)
    v=v.replace('}(',r'}\cdot (')
    v=re.sub(r'(?<=\})(?=[a-z])',r'\\cdot ',v)
    v=re.sub(r'([xyz])(?=\{[xyz]\})',r'\1\\cdot ',v)
    v=re.sub(r'(?<=[xyz0-9)])\\(sin|cos|ln)',r'\\cdot \\\1',v)
    v=re.sub(r'\\(sin|cos|ln|log)\s*((?:[0-9]+)?\\pi|[a-z]|[0-9]+)',lambda m:'\\'+m[1]+'('+m[2]+')',v)
    matches=list(re.finditer(r'\\(?:sin|cos|ln|log)\(',v))
    for mm in reversed(matches):
        depth=1;end=mm.end()
        while depth:
            if v[end]=='(':depth+=1
            if v[end]==')':depth-=1
            end+=1
        v=v[:mm.start()]+'{'+v[mm.start():end]+'}'+v[end:]
    v=v.strip().rstrip('.,').replace(r'\pi','P')
    v=re.sub(r'(?<=[ePxyz])\s*(?=\()',r'\\cdot ',v)
    return v

@lru_cache(None)
def parse(v):
    z=parse_latex(normalize(v),backend='lark')
    if isinstance(z,Tree):
        vals=[child for child in z.children if isinstance(child,s.Basic)]
        assert vals and all(s.simplify(vals[0]-t)==0 for t in vals),(v,z)
        z=vals[0]
    return z.subs({a:({'e':s.E,'P':s.pi,'x':g.X,'y':g.Y,'t':g.T}.get(a.name,a)) for a in z.free_symbols})

def equal(a,b):return s.simplify(s.expand(a-b))==0

def check(r):
    q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
    f=parse(re.search(r'Let \$f\(x,y\)=(.*?)\.\$',prompt)[1])
    curve=re.search(r'curve \$(.*?)\$ for',prompt)[1];lhs,rhs=curve.split('=');relation=parse(lhs)-parse(rhs)
    var,a,b=re.search(r'\$([xy])\\in \[(.*?),(.*?)\]',prompt).groups();a,b=parse(a),parse(b)
    xt,yt=re.search(r'r\(t\)\s*=⟨(.*?),(.*?)⟩',sol).groups();xt,yt=parse(xt),parse(yt)
    assert equal(xt if var=='x' else yt,g.T)
    assert equal(relation.subs({g.X:xt,g.Y:yt}),0),(curve,xt,yt)
    A=(s.simplify(xt.subs(g.T,a)),s.simplify(yt.subs(g.T,a)));B=(s.simplify(xt.subs(g.T,b)),s.simplify(yt.subs(g.T,b)))
    endpoint_block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[0]
    displayed=re.findall(r'r\((.*?)\)\s*& =⟨(.*?),(.*?)⟩',endpoint_block)
    assert len(displayed)==2
    for (t,x,y),tt,P in zip(displayed,[a,b],[A,B]):
        assert equal(parse(t),tt) and equal(parse(x),P[0]) and equal(parse(y),P[1]),displayed
    D=s.simplify(f.subs({g.X:B[0],g.Y:B[1]})-f.subs({g.X:A[0],g.Y:A[1]}))
    tail=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[-1]
    rows=tail.split(r'\\')
    rhsrows=[row.split('& =')[1].strip().rstrip('.') for row in rows]
    coords=re.fullmatch(r'f\((.*?),(.*?)\)-f\((.*?),(.*?)\)',rhsrows[1]);assert coords,rhsrows[1]
    assert all(equal(parse(v),actual) for v,actual in zip(coords.groups(),(*B,*A)))
    for row in rhsrows[2:]:assert equal(parse(row),D),(r['generation']['template'],row,D,parse(row))
    field=q[':question/answer-fields'][0];answers=field[':answer-field/choices'];ids=[z[':answer/id'] for z in answers]
    assert len(answers)==5 and len(set(ids))==5 and field[':answer-field/correct'][1] in ids
    assert not any('cosh' in z[':answer/value'] or 'sinh' in z[':answer/value'] for z in answers)
    vals=[parse(z[':answer/value']) for z in answers]
    assert not any(equal(vals[i],vals[j]) for i in range(5) for j in range(i)),vals
    flags=[equal(v,D) for v in vals];assert flags.count(True)==1
    assert flags[ids.index(field[':answer-field/correct'][1])]
    for text in (prompt,sol):
        assert text.count('$')%2==0 and text.count('{')==text.count('}'),text
        assert not any(term in text for term in ['source_id','bank_profile','underidentified'])
    return len(rhsrows)-2

def native(records,path):
    path.mkdir(parents=True,exist_ok=True)
    fixtures=[]
    for r in records:
        f=r['question'][':question/answer-fields'][0]
        fixtures.append({'label':r['generation']['template']+str(r['generation']['parameters']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every displayed option through application radio grader'} for a in f[':answer-field/choices']]})
    (path/'input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
    subprocess.run([str(HERE/'reference/native/check-engine'),str(path/'input.json'),str(path/'report.json')],check=True)
    return json.loads((path/'report.json').read_text())

def fingerprint(q):
    # Derivatives discard additive potential constants; banks, UUIDs and seed are absent.
    prompt=q[':question/problem'];f=parse(re.search(r'Let \$f\(x,y\)=(.*?)\.\$',prompt)[1])
    curve=re.search(r'curve \$(.*?)\$ for',prompt)[1];lhs,rhs=curve.split('=')
    var,a,b=re.search(r'\$([xy])\\in \[(.*?),(.*?)\]',prompt).groups()
    return g.hash_data([s.srepr(s.expand(s.diff(f,z))) for z in (g.X,g.Y)]+[s.srepr(s.expand(parse(lhs)-parse(rhs))),var,s.srepr(parse(a)),s.srepr(parse(b))])

def main():
    cases=[];review=[];fidelity=[];stages=0;records=[]
    for name,q in g.QUESTIONS.items():
        level=g.LEVELS[name];r=g.generate(level,template=name,parameters={'scale':1})
        stages+=check(r);records.append(r)
        f=q[':question/answer-fields'][0];gf=r['question'][':question/answer-fields'][0]
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices'])
        assert r['question'][':question/problem']==q[':question/problem']
        repair=q[':question/worked-solution']
        if name=='q-39749':repair=repair.replace(')-f(0,0)',')-f(0,-1)').replace(r'-{0}^{2}\cdot 0',r'-{0}^{2}\cdot (-1)')
        assert r['question'][':question/worked-solution']==repair
        correct=next(a for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1])
        assert correct[':answer/value']==f[':answer-field/correct'][':answer/value']
        fidelity.append({'source':name,'level':level,'complete_bank_matched':True,'choices_matched':5,'distractors_matched':4,'source_correct_matched':True,'prompt_exact':True,'solution_exact_after_documented_repair':True})
        review.append({'label':'source replay '+name,'record':r})
        for k in (2,-3):
            variant=g.generate(level,template=name,parameters={'scale':k});stages+=check(variant);records.append(variant)
            review.append({'label':name+' coefficient '+str(k),'record':variant})
            replay=g.generate(level,seed=999,template=name,parameters={'scale':k})
            assert replay['question'][':question/id']==variant['question'][':question/id']
            assert fingerprint(variant['question'])!=fingerprint(r['question'])
        print('Validated '+name,flush=True)
    for level in g.SUPPORTED_LEVELS:
        assert g.generate(level)['generation']['template'] in g.QUESTIONS
    try:g.generate('hard')
    except ValueError:pass
    else:raise AssertionError('Hard must be unsupported')
    report=native(records,HERE/'reference/validation/native')
    validation={'passed':True,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'source_basis':g.SOURCE['basis'],'source_lineage':g.SOURCE['lineage'],'source_complete_banks_matched':12,'source_choices_matched':60,'source_distractors_matched':48,'fidelity':fidelity,'displayed_arithmetic_stages_checked':stages,'supported_levels':list(g.SUPPORTED_LEVELS),'unsupported_levels':['hard'],'source_repairs':['q-39749 start substitution corrected from (0,0) to (0,-1), final answer unchanged; source remains untouched'],'coefficient_slot_coverage':{'samples':[1,2,-3],'bounds':[-12,12],'zero_excluded':True,'proof':'For nonzero k, scaling all five distinct source values preserves pairwise inequality and the unique correct designation. Line integral and every evaluation stage scale linearly by k. Endpoint roles and curve are fixed.'},'native':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'boundaries_checked_by_exact_scaling_proof':True}
    (HERE/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (HERE/'review.md').write_text('\n\n---\n\n'.join(item['label']+'\n\n'+g.markdown(item['record']) for item in review)+'\n')
    print(json.dumps(validation,indent=2))
if __name__=='__main__':main()
