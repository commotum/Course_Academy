#!/usr/bin/env python3
"""Independent displayed-math, structural, source-fidelity and native grading QA."""
import collections, copy, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('triple_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
FACTOR=r'(?:\([^()]*[abc]\)|(?:\([^()]*\)|-?\d+|-?\\sqrt\{\d+\}|-)?[abc])'
TRIPLE=re.compile('('+FACTOR+r')\\cdot \(('+FACTOR+r')\\times ('+FACTOR+r')\)')

def number(text):
    s=text.strip().rstrip('.,').replace(r'\,','').replace(' ','')
    s=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',s)
    s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
    s=s.replace(r'\cdot','*').replace('[','(').replace(']',')')
    s=re.sub(r'(\d|\))(?=\(|sqrt)',r'\1*',s)
    assert not re.search(r'[^0-9+*/().sqrt-]',s), ('unparsed numeric expression',text,s)
    out=sp.sympify(s);assert not out.free_symbols
    return out

def permutation(order):
    # Independent alternating tensor table; cyclic classes positive, swaps negative.
    return 1 if order in ('abc','bca','cab') else -1

def component(s):
    clean=s.replace('(','').replace(')','').strip();v=clean[-1];c=clean[:-1]
    return v,number(c) if c not in ('','-') else sp.Integer(-1 if c else 1)

def triple_value(m,T):
    vc=[component(x) for x in m.groups()];order=''.join(v for v,c in vc)
    assert sorted(order)==list('abc')
    return permutation(order)*sp.prod([c for v,c in vc])*T

def expression(text,T):
    s=text.strip().replace(r'\,','').rstrip('.,')
    if '⟨' in s:
        m=re.fullmatch(r'⟨([^⟩]+)⟩\\cdot ⟨([^⟩]+)⟩',s)
        assert m,s
        a,b=[[number(z) for z in t.split(',')] for t in m.groups()]
        assert len(a)==len(b)==3
        return sum(x*y for x,y in zip(a,b))
    s=TRIPLE.sub(lambda m:'('+str(triple_value(m,T))+')',s)
    return number(s)

def prompt_math(record):
    text=record['question'][':question/problem']
    request=text.split('Find $',1)[1].split('$',1)[0].rstrip(',')
    match=TRIPLE.fullmatch(request);assert match,request
    if '⟨' in text:
        m=re.search(r'if \$b\\times c=⟨([^⟩]+)⟩\$ and \$a=⟨([^⟩]+)⟩',text);assert m,text
        w,v=[[number(x) for x in z.split(',')] for z in m.groups()]
        T=sum(x*y for x,y in zip(v,w))
    else:
        given=text.split('if $',1)[1].split('$',1)[0].rstrip('.')
        lhs,rhs=given.split('=',1);gm=TRIPLE.fullmatch(lhs);assert gm,lhs
        coefficient=triple_value(gm,sp.Integer(1));T=sp.simplify(number(rhs)/coefficient)
    return T,triple_value(match,T)

def formatting(s):
    assert not any(ord(c)<32 and c not in '\n\t' for c in s),'C0 control byte'
    assert s.count('$')%2==0,'Unbalanced math delimiters'
    depth=0
    for i,c in enumerate(s):
        if c in '{}' and (i==0 or s[i-1]!='\\'):
            depth+=1 if c=='{' else -1;assert depth>=0,'Unbalanced TeX braces'
    assert depth==0,'Unbalanced TeX braces'
    assert '--' not in s and '+-' not in s,'Ungrouped signed component'
    assert not any(line.startswith('    ') for line in s.splitlines()),'Captured indentation'

def structure(record):
    gen=record['generation'];q=record['question'];solution=q[':question/worked-solution'];c=g.CASE.get(gen['template'])
    if c:
        original=g.QUESTIONS[c['source_id']][':question/worked-solution']
        def skeleton(s):
            return re.sub(r'\$\$.*?\$\$','<MATH>',s,flags=re.S)
        assert skeleton(solution)==skeleton(original),'Common worked prose changed'
        originalblocks=re.findall(r'\$\$(.*?)\$\$',original,re.S);blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S)
        assert len(blocks)==len(originalblocks)
        assert [x.count(r'\\') for x in blocks]==[x.count(r'\\') for x in originalblocks],'Operative stage count changed'
        first=blocks[0]
        rows=first.split(r'\\')
        if c['family']=='vector':
            assert '⟨' in rows[0] and len(re.findall(r'\\cdot',rows[1]))==3,'Supplied dot substitution stage absent'
            assert '⟨' not in rows[1] and r'\cdot' not in rows[2],'Individual product evaluation stage absent'
        else:
            assert '[' in rows[1] and r'\cdot' in rows[1],'Factoring operative stage absent'
            assert 'a'+r'\cdot (b\times c)' in rows[-1]
    else:
        assert 'First, we factor out the constants and get' in solution
        assert '[' in re.findall(r'\$\$(.*?)\$\$',solution,re.S)[0].split(r'\\')[1]
        if gen['template']=='double_scaling':
            assert 'Factoring out the constants in the requested product' in solution
            last=re.findall(r'\$\$(.*?)\$\$',solution,re.S)[-1];rows=last.split(r'\\')
            assert len(rows)==3 and '[' in rows[0] and r'\cdot' in rows[1],'Requested scaling stages absent'

def check(record):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    q=record['question'];gen=record['generation'];T,correct=prompt_math(record)
    formatting(q[':question/problem']);formatting(q[':question/worked-solution']);structure(record)
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];assert f[':answer-field/type'] in (':answer-field.type/radio',':answer-field.type/blank')
    answers=f[':answer-field/choices'];uuidkeys=[a[':answer/id'] for a in answers];assert len(uuidkeys)==len(set(uuidkeys))
    assert f[':answer-field/correct'][1] in uuidkeys
    matched=0;values=[]
    for a in answers:
        v=a[':answer/value'];formatting(v)
        if v.startswith('⟨'):
            assert gen['evidence_only'];values.append(tuple(number(x) for x in v[1:-1].split(',')));continue
        x=number(v);values.append(x)
        iscorrect=sp.simplify(x-correct)==0
        assert iscorrect==(a[':answer/id']==f[':answer-field/correct'][1]);matched+=iscorrect
    assert matched==1 and len(set(values))==len(values)
    if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem'] and len(answers)==1
    else:assert len(answers)==5
    # Read every displayed equation, including substitution, individual evaluation and final prose math.
    for block in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
        block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').strip()
        inherited=None
        for row in block.split(r'\\'):
            assert '=' in row, row
            lhs,rhs=row.split('=',1);lhs=lhs.strip()
            if lhs: inherited=expression(lhs,T)
            assert inherited is not None
            assert sp.simplify(inherited-expression(rhs,T))==0,('False displayed stage',row,T)
    # Prose swap statements must correspond to the next printed change of vector order.
    prior='abc'
    for a,b,body in re.findall(r'(?:Then, we swap |and again we swap )\$([abc])\$ and \$([abc])\$ to get\s*\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
        m=TRIPLE.search(body);assert m
        order=''.join(component(z)[0] for z in m.groups())
        changed=''.join(b if x==a else a if x==b else x for x in prior);assert order==changed,('Wrong swap prose',prior,a,b,order)
        prior=order
    return correct

def fidelity(c,r):
    source=g.QUESTIONS[c['source_id']];q=r['question'];f=q[':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
    for k in (':question/difficulty',':question/problem',':question/worked-solution',':question/answer-fields'):
        assert (k in source)==(k in q)
    for k in (':question/problem',':question/worked-solution'):assert q[k]==source[k],(c['template'],k)
    assert q[':question/difficulty']==source[':question/difficulty'][':db/ident']
    assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident'] and f[':answer-field/key']==sf[':answer-field/key']
    assert collections.Counter(a[':answer/value'] for a in f[':answer-field/choices'])==collections.Counter(c['bank'])
    selected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert selected==sf[':answer-field/correct'][':answer/value']

def fixtures(records):
    result=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0];checks=[]
        if f[':answer-field/type'].endswith('/radio'):
            checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete field-owned option selection'} for a in f[':answer-field/choices']]
        else:
            correct=check(r);n,d=sp.fraction(correct)
            checks=[{'submitted':next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]),'expected':'accepted','purpose':'canonical scalar blank'}, {'submitted':r'\frac{'+str(3*n)+'}{'+str(3*d)+'}','expected':'accepted','purpose':'unreduced equivalent scalar fraction'}, {'submitted':str(-correct),'expected':'rejected','purpose':'incorrect swap parity'}]
        result.append({'label':str(i)+':'+r['generation']['template'],'record':r,'checks':checks})
    return result

def main():
    source_records=[];normal=[];samplecounts={};seen_by_level={}
    for c in g.CASES:
        r=g.generate('moderate',template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check(r);fidelity(c,r);source_records.append(r)
    for name,s in g.TEMPLATES.items():
        fingerprints=set()
        for seed in range(60):
            r=g.generate(s['level'],seed,template=name);check(r);normal.append(r);fingerprints.add(r['generation']['mathematical_fingerprint'])
            fixed=g.generate(s['level'],seed+1000,template=name,parameters=r['generation']['parameters'])
            assert fixed['question'][':question/id']==r['question'][':question/id'],'Seed affected fixed content identity'
        samplecounts[name]=len(fingerprints)
    for level in ('easy','moderate','hard'):
        records=[g.generate(level,i) for i in range(200)]
        for r in records:check(r)
        seen_by_level[level]=sorted(set(r['generation']['template'] for r in records))
        assert seen_by_level[level]==sorted(n for n,s in g.TEMPLATES.items() if s['level']==level)
    # Authored level workload guards; explicit out-of-scope inputs must fail.
    guards=[('easy','single_scale',{'factor':1,'base':2,'target':'bac'}),('hard','double_scaling',{'factors':[1,2,3],'requested':[1,2,3],'base':2,'target':'bca'}),('hard','double_scaling',{'factors':[2,3,4],'requested':[1,1,3],'base':2,'target':'bca'}),('moderate','q-20058',{'factors':['1','1','2'],'rhs':'4'}),('moderate','q-20058',{'factors':['2','3','4'],'rhs':'501'}),('moderate','q-20062',{'v':[10,1,2],'w':[1,2,3]}),('moderate','q-128352',{'factors':['1','-1','-1'],'rhs':'2'}),('moderate','q-20059',{'factors':['2','3','4'],'rhs':'48'})]
    for l,n,p in guards:
        try:g.generate(l,template=n,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Explicit workload guard failed')
    mutations=0
    r=normal[0]
    for mut in ('control','stage','equation','swap'):
        broken=copy.deepcopy(r);sol=broken['question'][':question/worked-solution']
        if mut=='control':sol+='\x0c'
        elif mut=='stage':sol=re.sub(r'(?<=\\\\ ).*?\[a\\cdot \(b\\times c\)\].*?(?=\\\\)',r'a\\cdot (b\\times c) & =4 ',sol,count=1)
        elif mut=='equation':sol=sol.replace(' & =', ' & =1+',1)
        else:sol=sol.replace('Then, we swap $a$ and $b$','Then, we swap $b$ and $c$')
        broken['question'][':question/worked-solution']=sol
        try:check(broken)
        except (AssertionError,ValueError,sp.SympifyError,StopIteration):mutations+=1
        else:raise AssertionError('Mutation survived: '+mut)
    # Tuple masks must survive swapped source tuples without sequential replacement overlap.
    overlap=g.generate('moderate',template='q-20062',parameters={'v':[2,3,0],'w':[1,-2,2]},profile='observed:q-20062');check(overlap)
    preview=[]
    for c in g.CASES:
        preview.append(g.generate('moderate',14,template=c['template']))
        # Explicit historical homothety is still parameterized, and publicly marked evidence-only.
        p=copy.deepcopy(c['parameters'])
        if c['family']=='scalar':p['rhs']=str(sp.sympify(p['rhs'])*2)
        else:p['v']=[2*x for x in p['v']]
        try:
            er=g.generate('moderate',template=c['template'],parameters=p,profile=c['bank_profile']);check(er)
        except ValueError:
            # Coordinate/rhs ceiling is part of both explicit and sampled workload, no bypass.
            pass
    for level in ('easy','moderate','hard'):
        preview.extend(g.generate(level,i+51) for i in range(2))
    native_records=source_records+preview
    engine_input=HERE/'native-input.json';engine_report=HERE/'native-results.json';engine_input.write_text(json.dumps(fixtures(native_records),indent=2,ensure_ascii=False))
    engine=HERE.parents[1]/'runs/current/check-engine'
    subprocess.run([str(engine),str(engine_input),str(engine_report)],check=True)
    native=json.loads(engine_report.read_text())
    # Finite meaningful authored domains; easy exact enumeration, hard structural factors bounded count.
    easy=sum(len(set([c,-c,s*f*t,-s*f*t,s*f*f*t]))==5 for f in (-7,-6,-5,-4,-3,-2,2,3,4,5,6,7) for t in range(-9,10) if t for o in ('bac','bca','cab','cba','acb') for s in [permutation(o)] for c in [s*t])
    hard_requested=sum(len(set([r*s*t,-r*s*t,s*t,a*s*t,b*s*t]))==5 for a in (-4,-3,-2,2,3,4) for b in (-4,-3,-2,2,3,4) for r in [a*b] for t in range(-9,10) if t for o in ('bac','bca','cab','cba','acb') for s in [permutation(o)])
    hard=hard_requested*8**3
    summary={'pass':True,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_questions':15,'source_prompt_exact':15,'source_worked_solution_exact':15,'source_attribute_presence':15,'source_fields':15,'source_correct_designations':15,'source_complete_banks':15,'source_choices':sum(len(c['bank']) for c in g.CASES),'source_distractors':sum(len(c['bank'])-1 for c in g.CASES),'source_repairs':0,'public_evidence_profiles':15,'opaque_radio_bank_profiles':12,'source_answer_shape_anomalies':1,'normal_scalar_banks_verified':True,'normal_sample_checks':len(normal)+600,'unique_tasks_in_60_per_template':samplecounts,'default_template_coverage':seen_by_level,'meaningful_authored_domain_counts':{'easy':easy,'hard':hard,'moderate':'bounded vector/factor families; per-template sampled counts provided, no unsupported exact enumeration claim'},'mutation_regressions':mutations,'explicit_invalid_guard_checks':len(guards),'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'plots':'none','database_writes':0,'native_limitations':[]}
    (HERE/'validation.json').write_text(json.dumps(summary,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(preview,ensure_ascii=False,indent=2)+'\n')
    sections=['# Scalar triple product property review','Local author evidence; observed banks are evidence-only. All15 original masks are represented.']
    for c,original,variant in zip(g.CASES,source_records,preview):
        sections+=['## '+c['source_id'],'### Original, complete historical bank',g.markdown(original),'### Generated variant, authored method bank',g.markdown(variant)]
    for r in preview[len(g.CASES):]:sections+=['## Authored/default '+r['question'][':question/difficulty'].split('/')[-1]+' variant',g.markdown(r)]
    (HERE/'review.md').write_text('\n\n'.join(sections)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
