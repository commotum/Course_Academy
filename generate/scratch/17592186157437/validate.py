#!/usr/bin/env python3
"""Independent displayed-expression, full fidelity, identity, and native grading checks."""
import hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;script=D.with_suffix('.py');REPO=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',script);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=g.X

def parse(s):
    s=s.strip().rstrip('.,?').replace(r'\cdot','*').replace(r'\,','').replace('&','')
    s=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
    s=s.replace('{','(').replace('}',')').replace('^','**')
    return parse_expr(s,local_dict={'x':X,'e':sp.E},transformations=standard_transformations+(implicit_multiplication_application,))
def maths(s):return [m.group()[2:-2].strip() if m.group().startswith('$$') else m.group()[1:-1] for m in re.finditer(r'\$\$[\s\S]*?\$\$|\$[^$]*?\$',s)]
def lhs(s):
    parts=s.strip().rstrip('.,?').split('=');assert len(parts)==2 and parse(parts[1])==0,s
    return parse(parts[0])
def aligned(s):
    s=s.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
    return [lhs(row) for row in s.split(r'\\')]
def same(a,b):assert sp.simplify(sp.expand(a-b))==0,(a,b)
def roots_text(s):
    assert s.startswith('x=')
    return [parse(v) for v in s[2:].rstrip('.,').split(',')]
def braces(s):
    depth=0
    for c in re.sub(r'\{\{field-[12]\}\}','',s):
        depth+=c=='{';depth-=c=='}';assert depth>=0,s
    assert depth==0,s

def mathematics(r):
    q=r['question']; p=r['generation']['parameters'];t=r['generation']['template'];s=g.DISPLAYS[r['generation']['display_profile']]
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    for text in [q[':question/problem'],q[':question/worked-solution']]:
        assert text.count('$')%2==0; braces(text)
        assert not re.search(r'\{\{(?!field-[12]\}\})',text),text
        assert 'sinh' not in text and 'cosh' not in text
    prompt=maths(q[':question/problem']); actual=lhs(prompt[0])
    # Read exponential base/input from the displayed formula, not generator metadata.
    found=re.findall(r'\{(e|[2-9])\}\^\{([^{}]+)\}|(?<![A-Za-z])([e2-9])\^\{([^{}]+)\}',prompt[0])
    assert len(found)>=2,prompt[0]
    base,exponent=(found[0][0] or found[0][2],found[0][1] or found[0][3]);base=parse(base);exponent=parse(exponent)
    assert base>0 and base!=1
    E=base**exponent
    for b1,k1,b2,k2 in found:same(parse(b1 or b2)**parse(k1 or k2),E)
    P=sp.Poly(sp.expand(actual/E),X);assert P.degree()==2
    real_roots=sorted(sp.solve(P.as_expr(),X));assert len(real_roots)==2 and all(v.is_real and v!=0 for v in real_roots)
    sol=maths(q[':question/worked-solution']); rows=aligned(sol[0]);assert len(rows)==2
    for row in rows:same(row,actual)
    assert sol[1:4]==['ab=0','a=0','b=0.']
    split=sol[4].split(r'\,\text{and}\,');assert len(split)==2
    same(lhs(split[0]),P.as_expr());same(lhs(split[1]),E)
    same(lhs(sol[5]),P.as_expr())
    factor_rows=aligned(sol[6]) if r'\begin{aligned}' in sol[6] else [lhs(sol[6])]
    assert len(factor_rows)==(2 if s['two_rows'] else 1)
    for row in factor_rows:same(row,P.as_expr())
    for v in roots_text(sol[7]):assert v in real_roots
    assert roots_text(sol[7])==real_roots
    pos=8
    if s['two_rows']:
        # This false scalar equation has no root; retain the distinct teaching stage.
        assert lhs(sol[pos])!=0;pos+=1
    same(lhs(sol[pos]),E);same(parse(sol[pos+1]),E);assert sol[pos+2]=='x.';pos+=3
    fields=q[':question/answer-fields'];uids=[]
    if t.endswith('_blank'):
        assert len(sol)==pos+1
        final=sol[pos].split(r'\,\text{and}\,');assert len(final)==2
        assert [parse(v.split('=')[1]) for v in final]==real_roots
    else:
        assert len(sol)==pos+2 and roots_text(sol[pos])==real_roots
        mul,answer=sol[pos+1].rstrip('.').split('=');same(parse(mul),real_roots[0]*real_roots[1]);same(parse(answer),parse(mul))
    for f in fields:
        key=f[':answer-field/key'];arr=f[':answer-field/choices'];correct=f[':answer-field/correct'];assert correct[0]==':answer/id'
        assert len(arr)==(1 if t.endswith('_blank') else 5)
        vals=[parse(a[':answer/value']) for a in arr];assert len(set(vals))==len(vals)
        chosen=next(a for a in arr if a[':answer/id']==correct[1]);target=real_roots[int(key[-1])-1] if key.startswith('field-') else sp.prod(real_roots)
        same(parse(chosen[':answer/value']),target)
        if key.startswith('field-'):assert '{{'+key+'}}' in q[':question/problem']
        for a in arr:
            assert '$' not in a[':answer/value'];assert a[':answer/type']==':answer.type/math';uids.append(a[':answer/id'])
    assert len(uids)==len(set(uids))
    return real_roots

def checks(r):
    out=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        correct=f[':answer-field/correct'][1]
        for a in f[':answer-field/choices']:
            value=a[':answer/value']
            if f[':answer-field/type'].endswith('/radio'):
                out.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'each owned choice'})
            else:
                v=parse(value);out.extend([{'field_index':i,'submitted':value,'expected':'accepted','purpose':'exact fragment'},
                 {'field_index':i,'submitted':f'({sp.numer(v)*3})/({sp.denom(v)*3})','expected':'accepted','purpose':'independently unreduced fraction'},
                 {'field_index':i,'submitted':g.tex(v+1),'expected':'rejected','purpose':'incorrect neighboring root'}])
    return out

def main():
    (D/'validation.json').unlink(missing_ok=True)
    raw=json.loads((D/'source.json').read_text());assert raw==json.loads((REPO/'generate/runs/current/sources/17592186157437.json').read_text())
    sources={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']};cases=json.loads((D/'source-cases.json').read_text())
    fidelity=[];records=[];options=0;designations=0;solutions=0
    for c in cases:
        r=g.generate(c['level'],seed=17,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];original=sources[c['source_id']];mathematics(r)
        assert q[':question/problem']==original[':question/problem'];assert [f[':answer-field/key'] for f in q[':question/answer-fields']]==[f[':answer-field/key'] for f in original[':question/answer-fields']]
        if ':question/worked-solution' in original:assert q[':question/worked-solution']==original[':question/worked-solution'];solutions+=1
        for f,of in zip(q[':question/answer-fields'],original[':question/answer-fields']):
            assert f[':answer-field/type']==of[':answer-field/type'][':db/ident']
            vals=sorted(a[':answer/value'] for a in f[':answer-field/choices']);old=sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert vals==old;options+=len(old)
            if ':answer-field/correct' in of:
                chosen=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert chosen[':answer/value']==of[':answer-field/correct'][':answer/value'];designations+=1
        fidelity.append({'source_id':c['source_id'],'prompt':'exact','complete_bank':'exact','solution':'exact' if ':question/worked-solution' in original else 'authored; absent original','designation':'matched' if ':question/difficulty' in original else 'unavailable; independently derived -9','level':c['assignment_origin']})
        records.append({'label':'source '+c['source_id'],'record':r,'checks':checks(r)})
    diversity={};generated=[]
    for t,level in g.TEMPLATES.items():
        fingerprints=set()
        for seed in range(60):
            r=g.generate(level,seed=seed,template=t);mathematics(r);fingerprints.add(r['generation']['mathematical_fingerprint'])
            replay=g.generate(level,seed=1000+seed,template=t,parameters=r['generation']['parameters'],profile='authored')
            assert replay['question'][':question/id']==r['question'][':question/id']
            if seed<2:
                generated.append(r);records.append({'label':'generated '+t+' '+str(seed),'record':r,'checks':checks(r)})
        assert len(fingerprints)>=(10 if level=='easy' else 40),(t,len(fingerprints));diversity[t]=len(fingerprints)
    # Exercise every source display/bank under changed mathematical parameters.
    for c in cases:
        good=0
        for seed in range(20):
            r=g.generate(c['level'],seed=seed,profile=c['bank_profile']);mathematics(r);good+=1
        assert good==20
    for level,t,p in [('easy','difference_radio',{'g':1,'a':1,'b':13,'c':1,'d':-13,'base':2,'k':1,'h':0}),('hard','hard_leading_radio',{'g':1,'a':2,'b':2,'c':3,'d':1,'base':2,'k':1,'h':0}),('moderate','leading_blank',{'g':1,'a':4,'b':1,'c':1,'d':2,'base':2,'k':1,'h':0})]:
        try:g.generate(level,template=t,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Out-of-scope explicit inputs accepted')
    # Whole-bank collision: monic roots 2,4 have product 8, sum6, unique; roots2,2 invalid outright.
    bad={'g':1,'a':1,'b':-2,'c':1,'d':-2,'base':3,'k':1,'h':0}
    try:g.generate('moderate',template='quadratic_radio',parameters=bad)
    except ValueError:pass
    else:raise AssertionError('Repeated roots accepted')
    # Enumerate mathematical task domains without incidental base/exponent/scalar values.
    domain_tasks={}; by_level={l:set() for l in ['easy','moderate','hard']}
    for t,level in g.TEMPLATES.items():
        seen=set(); gs=[2,3] if 'gcf' in t or 'scaled' in t else [1]
        aa=[1] if level=='easy' or 'quadratic' in t else [2,3,4] if level=='hard' else [2,3]
        cc=[2,3,4] if level=='hard' else [1]
        tuples=itertools.product(gs,aa,range(1,13),cc,[0]) if level=='easy' else itertools.product(gs,aa,[i for i in range(-9,10) if i],cc,[i for i in range(-9,10) if i])
        for scalar,a,b,c,d in tuples:
            p={'g':scalar,'a':a,'b':b,'c':c,'d':-b if level=='easy' else d,'base':2,'k':1,'h':0}
            try:
                g.bounds(p,level,t)
                roots=sorted([sp.Rational(-b,a),sp.Rational(-p['d'],c)])
                if not t.endswith('_blank'):
                    sample_bank=g.bank('authored',p,roots)
                    if len({v for _,v in sample_bank})!=5:continue
            except ValueError:continue
            key=(tuple(roots),'roots' if t.endswith('_blank') else 'product',scalar!=1)
            seen.add(key);by_level[level].add(key)
        domain_tasks[t]=len(seen)
    assert by_level['easy'] and len(by_level['easy'])==36
    # Incidental exponential changes cannot create a mathematical task; banks can change content identity.
    p={'g':1,'a':1,'b':3,'c':1,'d':-3,'base':3,'k':1,'h':0}
    r1=g.generate('easy',template='difference_radio',parameters=p,profile='q-88454')
    r2=g.generate('easy',template='difference_radio',parameters=dict(p,base=7,k=2,h=3),profile='q-88454')
    assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
    assert r1['question'][':question/id']!=r2['question'][':question/id']
    r3=g.generate('easy',template='difference_radio',parameters=p,profile='q-110801')
    assert r1['generation']['mathematical_fingerprint']==r3['generation']['mathematical_fingerprint']
    assert r1['question'][':question/id']!=r3['question'][':question/id']
    (D/'engine-input.json').write_text(json.dumps(records,indent=2)+'\n')
    engine=REPO/'generate/runs/current/check-engine';subprocess.run([str(engine),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
    report=json.loads((D/'engine-report.json').read_text())
    source_variants=[]
    review=['# Source and generated review','All original evidence is retained verbatim; generated entries are labeled.']
    for c in cases:
        original=sources[c['source_id']];review+=['\n## Original '+c['source_id'],original[':question/problem']]
        for f in original[':question/answer-fields']:review+=['Bank '+f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices'])]
        review+=[original.get(':question/worked-solution','No original solution, difficulty, or correct reference. Independent product derivation: (x+3)(x-3)e^(2x)=0; roots -3,3; product -9.')]
        variant=g.generate(c['level'],seed=97,profile=c['bank_profile']);source_variants.append(variant);review+=['\n### Generated changed-parameter variant of '+c['bank_profile'],variant['question'][':question/problem']]
        for f in variant['question'][':question/answer-fields']:review+=['Generated bank '+f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices'])]
        review+=[variant['question'][':question/worked-solution']]
    for r in generated:
        review+=['\n## Generated '+r['question'][':question/difficulty'].split('/')[-1]+' / '+r['generation']['template'],r['question'][':question/problem']]
        for f in r['question'][':question/answer-fields']:review+=['Generated bank '+f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices'])]
        review+=[r['question'][':question/worked-solution']]
    (D/'review.json').write_text(json.dumps(generated+source_variants,indent=2)+'\n')
    (D/'review.md').write_text('\n\n'.join(review)+'\n')
    result={'status':'pass','script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'display_profiles_sha256':hashlib.sha256((D/'display-profiles.json').read_bytes()).hexdigest(),'source_questions':14,'rated_easy':5,'rated_moderate':8,'unrated':1,'prompt_exact':14,'original_solutions_exact':solutions,'original_solutions_available':13,'complete_banks_exact':14,'displayed_options_matched':options,'original_designations_matched':designations,'original_designations_available':19,'independently_derived_missing_designations':1,'source_fidelity':fidelity,'observed_templates':9,'authored_hard_templates':2,'random_instances_checked':660,'changed_source_profile_instances_checked':280,'diversity_60_samples_per_template':diversity,'enumerated_authored_task_domains':domain_tasks,'deduplicated_level_task_counts':{l:len(v) for l,v in by_level.items()},'generated_review_records':len(generated)+len(source_variants),'native_grading':{k:report[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'plots':'none','database_writes':0,'limitations':['q-88412 lacks source designation/difficulty/solution; easy assignment and solution are authored','q-110801/q-88458/q-88459/q-88460 scalar bank intent underidentified; explicit replay formulas only','Hard difficulty scope is authored, not an observed label']}
    (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
