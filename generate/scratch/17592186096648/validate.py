#!/usr/bin/env python3
"""Independent displayed-prompt math, full raw bank fidelity, actual native grader."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def rat(s):
    s=s.strip()
    s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1)/(\2)',s)
    return sp.Rational(sp.sympify(s))

def lin(s):
    # Parse displayed mathematical object, never generation metadata.
    a,b=sp.symbols('a b')
    s=s.strip();s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1)/(\2)',s)
    s=re.sub(r'(?<=[\d)])(?=[ab])','*',s)
    x=sp.sympify(s,locals={'a':a,'b':b},rational=True)
    assert sp.expand(x)==x.coeff(a)*a+x.coeff(b)*b
    return x.coeff(a),x.coeff(b)

def displayed(r):
    prompt=r['question'][':question/problem']
    chunks=re.findall(r'\$(.*?)\$',prompt)
    assert len(chunks)==3 and chunks[2]=='λ'
    scaled=[s for s in chunks[:2] if s.startswith('λ(')]
    assert len(scaled)==1
    base=lin(scaled[0][2:-1]);target=lin(next(s for s in chunks[:2] if not s.startswith('λ(')))
    assert all(base) and all(target)
    k=sp.cancel(target[0]/base[0]);assert sp.cancel(target[1]/base[1])==k
    assert 'equal (non-zero) vectors, find the scale factor' in prompt
    return base,target,k

def formatting(s):
    assert s.count('$')%2==0
    depth=0
    for i,c in enumerate(s):
      if c=='{' and (i==0 or s[i-1]!='\\'):depth+=1
      if c=='}' and (i==0 or s[i-1]!='\\'):depth-=1
      assert depth>=0
    assert depth==0
    assert '--' not in s and '+-' not in s

def check(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];f=q[':question/answer-fields'][0];base,target,k=displayed(r)
    assert f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5
    values=[];correct=[]
    for a in f[':answer-field/choices']:
      assert re.fullmatch('[0-9a-f-]{36}',a[':answer/id'])
      formatting(a[':answer/value'])
      if a[':answer/type']==':answer.type/math':
        value=rat(a[':answer/value']);values.append(value)
        if value==k:correct.append(a[':answer/id'])
      else:assert a[':answer/value']=='No such $λ$'
    assert len(set(values))==4 and len(correct)==1
    formatting(q[':question/problem'])
    if r['generation']['evidence_only']:
      assert ':question/worked-solution' not in q and ':question/difficulty' not in q and ':answer-field/correct' not in f
      return
    assert f[':answer-field/correct']==[':answer/id',correct[0]]
    sol=q[':question/worked-solution'];formatting(sol)
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
    assert len(blocks)==4
    # Formal operator and independently parsed complete components.
    m=re.fullmatch(r'λ\((.*?)\)=λ\((.*?)\)a\+λ\((.*?)\)b\.',blocks[0])
    assert m and lin(m[1])==base and (rat(m[2]),rat(m[3]))==base
    rows=[x.strip().removesuffix(r'\\').strip() for x in blocks[1].splitlines()[1:-1]]
    assert len(rows)==2
    for row,n,d in zip(rows,target,base):
      m=re.fullmatch(r'λ &= \\frac\{(.*?)\}\{(.*?)\} = (.*)',row)
      assert m and rat(m[1])==n and rat(m[2])==d and rat(m[3])==n/d==k
    m=re.fullmatch(r'(.*?)=(.*?)\((.*?)\)\.',blocks[2])
    assert m and lin(m[1])==target and rat(m[2])==k and lin(m[3])==base
    assert rat(blocks[3].split('=')[1])==k
    assert 'non-zero vectors are parallel.' in sol
    assert ('same because the factor is positive.' if k>0 else 'opposite because the factor is negative.') in sol
    assert sol.startswith('Notice that') and '\n\nTherefore,\n\n' in sol

def main():
    sources=json.load(open(P/'source.json'))['record'][':knowledge-point/questions']
    cases=json.load(open(P/'source-cases.json'))
    fidelity=[];reviews=[]
    for case,s in zip(cases,sources):
        assert case['source_id']==s[':question/math-academy-id']
        r=g.generate(case['authored_level'],17,case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(r)
        q=r['question'];f=q[':question/answer-fields'][0];sf=s[':question/answer-fields'][0]
        assert q[':question/problem']==s[':question/problem']
        for key in (':question/difficulty',':question/worked-solution'):assert (key in q)==(key in s)
        assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
        pairs=lambda xs:sorted((a[':answer/type'] if isinstance(a[':answer/type'],str) else a[':answer/type'][':db/ident'],a[':answer/value']) for a in xs)
        assert pairs(f[':answer-field/choices'])==pairs(sf[':answer-field/choices'])
        fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'complete_bank_exact':True,'attribute_presence':True,'correct_designation':'absent in source; inferred scalar independently checked'})
        reviews.append(r)
    checks=[];counts={};family_coverage={};tested=0
    for level in ('easy','moderate','hard'):
        dom=g.domain(level);counts[level]=len(dom)
        assert len(dom)>100
        seen=set()
        for seed in range(36):
            r=g.generate(level,seed);check(r);tested+=1;seen.add(r['generation']['template'])
            if seed<2:reviews.append(r)
            # Actual native grading of every displayed choice.
            f=r['question'][':question/answer-fields'][0]
            checks.append({'label':level+'-'+str(seed),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete source-shaped radio bank selection'} for a in f[':answer-field/choices']]})
            p=r['generation']['parameters']
            other=g.generate(level,999,r['generation']['template'],parameters=p)
            assert other['question'][':question/id']==r['question'][':question/id']
            # Coincident task under common base scaling: independent math key.
            assert g.math_key({n:sp.Rational(x) for n,x in p.items()})==g.math_key({'u':sp.Rational(p['u'])*2,'v':sp.Rational(p['v'])*2,'k':sp.Rational(p['k'])})
        assert seen==set(g.TEMPLATES);family_coverage[level]=sorted(seen)
        # Enumerate whole domain bounds and complete bank uniqueness.
        for p in dom:
            g.eligible(level,p);assert len(set(g.bank(p,'method_ratio')))==5
        for template in g.TEMPLATES:
            for p in (dom[0],dom[-1]):check(g.generate(level,1,template,parameters={n:str(v) for n,v in p.items()}))
        for p in ({'u':0,'v':2,'k':3},{'u':2,'v':0,'k':3},{'u':1,'v':2,'k':0},{'u':100,'v':1,'k':3}):
            try:g.generate(level,parameters=p)
            except ValueError:pass
            else:raise AssertionError('invalid explicit parameters accepted')
    # More bank-family variants in the review, including raw profiles.
    for case in cases:
        p={n:sp.Rational(v) for n,v in case['parameters'].items()};p['v']*=2
        reviews.append(g.generate(case['authored_level'],44,case['template'],parameters={n:str(v) for n,v in p.items()},profile=case['bank_profile']))
        p={n:sp.Rational(v) for n,v in case['parameters'].items()};p['k']*=2
        reviews.append(g.generate(case['authored_level'],45,case['template'],parameters={n:str(v) for n,v in p.items()},profile=case['bank_profile']))
    for level in ('easy','moderate','hard'):
      for template in g.TEMPLATES:
        reviews.append(g.generate(level,100,template))
    for r in reviews:check(r)
    (P/'engine-input.json').write_text(json.dumps(checks,indent=2))
    engine=P.parents[1]/'runs/current/check-engine'
    subprocess.run([str(engine),str(P/'engine-input.json'),str(P/'engine-report.json')],check=True)
    er=json.load(open(P/'engine-report.json'))
    validation={'passed':True,'source_database':g.SOURCE,'source_coverage':fidelity,'source_prompts':{'matched':2,'total':2},'source_banks':{'matched':2,'total':2},'source_values':{'matched':10,'total':10},'source_correct_designations':{'matched':0,'total':0,'missing':2},'source_solutions':{'matched':0,'total':0,'missing':2},'source_difficulty':{'rated':0,'unrated':2},'authored_levels':['easy','moderate','hard'],'meaningful_domains':counts,'default_family_coverage':family_coverage,'generated_mathematical_checks':tested,'native_grading':{k:v for k,v in er.items() if k!='records'},'raw_grading':'not attempted: absent correct refs; separate inferred supported defaults grade normally','formatting':'all displayed prompts, choices and solutions checked','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'unresolved':['Original correct designations and worked solutions absent; no matching claims possible.','Historical q-12135 wrong values 3 and 2 have underdetermined intended operations; evidence-only profile.','Canonical example nonzero a,b alone do not guarantee nonzero combination; normal output uses practice nonzero equality premise.']}
    (P/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    (P/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n')
    (P/'review.md').write_text('# Source and generated review\n\nFirst two records are original raw replay; next six are two authored examples per level. Later records cover changed historical banks and both prompt families at each level. Raw evidence is ineligible for learners.\n\n'+'\n\n---\n\n'.join(map(g.markdown,reviews))+'\n')
    (P/'freeze.json').write_text(json.dumps({'version':g.VERSION,'basis':1356,'generator_sha256':hashlib.sha256(P.with_suffix('.py').read_bytes()).hexdigest(),'validation_sha256':hashlib.sha256((P/'validate.py').read_bytes()).hexdigest(),'runtime':validation['runtime'],'stop_after_step':7},indent=2)+'\n')
    print(json.dumps({k:validation[k] for k in ('passed','source_banks','meaningful_domains','generated_mathematical_checks','native_grading')},indent=2))
if __name__=='__main__':main()
