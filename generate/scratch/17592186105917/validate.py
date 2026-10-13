#!/usr/bin/env python3
"""Fail on displayed mathematics, source mask/value/key fidelity, scope or native grading."""
import hashlib,importlib.util,json,os,re,subprocess,sys,random
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('gen',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def mathparse(t):
    t=t.replace('−','-').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').strip().removesuffix('.')
    def group(text,i):
        assert text[i]=='{',(text,i)
        depth=1;j=i+1
        while depth:
            if text[j]=='{':depth+=1
            if text[j]=='}':depth-=1
            j+=1
        return text[i+1:j-1],j
    def convert(text):
        out='';i=0
        while i<len(text):
            if text.startswith(r'\frac',i):
                a,j=group(text,i+5);b,i=group(text,j);out+='(('+convert(a)+')/('+convert(b)+'))'
            elif text.startswith(r'\sqrt',i):
                a,i=group(text,i+5);out+='sqrt('+convert(a)+')'
            elif text[i]=='{':
                a,i=group(text,i);out+='('+convert(a)+')'
            elif text[i]=='^':out+='**';i+=1
            else:out+=text[i];i+=1
        return out
    return parse_expr(convert(t),local_dict={'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def equal(a,b):return s.simplify(a-b)==0

def formatting(t):
    assert '--' not in t and '+-' not in t,t
    assert t.count('$')%2==0,'Unbalanced math delimiter'
    depth=0
    for i,c in enumerate(t):
        if c=='{' and (i==0 or t[i-1]!='\\'):depth+=1
        if c=='}' and (i==0 or t[i-1]!='\\'):depth-=1;assert depth>=0
    assert depth==0,'Unbalanced TeX group'

def check(record):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']==g.KP
    q=record['question'];f=q[':question/answer-fields'][0];p=record['generation']['parameters']
    prompt=q[':question/problem'];vector_strings=re.findall('⟨([^⟩]+)⟩',prompt)
    assert len(vector_strings)==2
    a,b=[[mathparse(x) for x in v.split(',')] for v in vector_strings]
    assert all(equal(x,g.expr(y)) for x,y in zip(a+b,p['a']+p['b']))
    D=s.expand(sum(x*y for x,y in zip(a,b)));A2=s.expand(sum(x*x for x in a));B2=s.expand(sum(x*x for x in b));A=s.sqrt(A2);B=s.sqrt(B2)
    P=D/B;Q=D/A;R=P if p['operation']=='single' else P+Q if p['operation']=='sum' else P-Q
    names=re.findall(r'\$([a-z])\s*=',prompt)
    assert len(names)==2,names
    ua,ub=names
    if p['operation']=='single':assert 'scalar projection' in prompt
    else:assert ('+' if p['operation']=='sum' else '-') in prompt.split('Find',1)[1]
    values=[mathparse(c[':answer/value']) for c in f[':answer-field/choices']]
    assert len(set(c[':answer/id'] for c in f[':answer-field/choices']))==len(values)
    for c in f[':answer-field/choices']:
        assert '$' not in c[':answer/value'];formatting(c[':answer/value'])
    for v in values:assert not v.free_symbols and v.is_real is True and v.is_finite is True
    assert all(not equal(x,y) for i,x in enumerate(values) for y in values[i+1:]),'Ambiguous whole bank'
    correct=f.get(':answer-field/correct')
    if correct:
        assert correct[0]==':answer/id'
        expected=next(mathparse(c[':answer/value']) for c in f[':answer-field/choices'] if c[':answer/id']==correct[1]);assert equal(expected,R)
    else:assert record['generation']['evidence_only'] and sum(equal(v,R) for v in values)==1
    if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt
    for t in [prompt,q.get(':question/worked-solution','')]:formatting(t)
    # Every displayed formal, substitution, component-evaluation and reduction row.
    sol=q.get(':question/worked-solution','')
    blocks=list(re.finditer(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S))
    if sol:assert len(blocks)==(1 if p['operation']=='single' else 3)
    for ib,block in enumerate(blocks):
        expected=[P,Q,R][ib]
        rhss=re.findall(r' & =(.*?)(?= \\\\  & =|$)',block.group(1),re.S)
        assert len(rhss)>=2
        for ir,rhs in enumerate(rhss):
            rhs=rhs.removesuffix('.')
            for name,vec in [(ua,a),(ub,b)]:
                for coord,x in zip('xyz',vec):rhs=rhs.replace('{'+name+'}_{'+coord+'}', '('+g.tex(x)+')')
            rhs=rhs.replace(ua+r'\cdot '+ub,g.tex(D)).replace(ub+r'\cdot '+ua,g.tex(D))
            rhs=rhs.replace('|\\,'+ua+'\\,|',g.tex(A)).replace('|\\,'+ub+'\\,|',g.tex(B))
            val=mathparse(rhs)
            assert equal(val,expected),(record['generation']['template'],ib,ir,rhs,val,expected)
        if ib==0:
            assert rhss[1].count('^{2}')==3
            assert rhss[2].count('^{2}')==3
            assert (rhss[2].count(r'\cdot ')==3 or len(re.findall(r'\)\(',rhss[2]))==3),rhss[2]
    return dict(D=D,A2=A2,B2=B2,P=P,Q=Q,R=R)

def engine_entry(record,label):
    f=record['question'][':question/answer-fields'][0];c=f.get(':answer-field/correct')
    if not c:return None
    checks=[]
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==c[1] else 'rejected','purpose':'Owned complete-bank choice'} for a in f[':answer-field/choices']]
    else:
        p=record['generation']['parameters'];a,b=[list(map(g.expr,p[k])) for k in ('a','b')];D=sum(x*y for x,y in zip(a,b));A2=sum(x*x for x in a);B2=sum(x*x for x in b)
        equivalent=f'({D})/sqrt({B2})'
        if p['operation']!='single':equivalent+=('+' if p['operation']=='sum' else '-')+f'(({D})/sqrt({A2}))'
        checks=[{'submitted':f[':answer-field/choices'][0][':answer/value'],'expected':'accepted','purpose':'Canonical scalar entry'}, {'submitted':equivalent,'expected':'accepted','purpose':'Unreduced independently derived quotient(s)'},{'submitted':'10000','expected':'rejected','purpose':'Incorrect scalar'}]
    return {'label':label,'record':record,'checks':checks}

def main():
    source=json.loads((ROOT/'source.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/'source-cases.json').read_text());raw={q[':question/math-academy-id']:q for q in source}
    reports=[];review=[];engine=[];counts={'banks':0,'values':0,'correct_designations':0,'prompts':0,'solutions':0,'key_presence':0}
    original_reviews=[]
    for case in cases:
        sid=case['source_id'];original=raw[sid];r=g.generate(case['level'],17,case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(r)
        q=r['question'];f=q[':question/answer-fields'][0];sf=original[':question/answer-fields'][0]
        assert q[':question/problem']==original[':question/problem'],sid;counts['prompts']+=1
        assert q.get(':question/worked-solution')==original.get(':question/worked-solution'),sid
        if ':question/worked-solution' in original:counts['solutions']+=1
        assert set(q)-{':question/id'}==set(original)-{':db/id',':question/id'},(sid,set(q),set(original))
        assert set(f)-{':answer-field/id'}==set(sf)-{':db/id',':answer-field/id'}
        for choice in f[':answer-field/choices']:assert set(choice)=={':answer/id',':answer/type',':answer/value'}
        counts['key_presence']+=1
        assert f[':answer-field/key']==sf[':answer-field/key'];assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        sv=[mathparse(a[':answer/value']) for a in sf[':answer-field/choices']];gv=[mathparse(a[':answer/value']) for a in f[':answer-field/choices']]
        assert len(sv)==len(gv) and all(sum(equal(x,y) for y in gv)==1 for x in sv)
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
        counts['banks']+=1;counts['values']+=len(sv)
        if ':answer-field/correct' in sf:
            generated=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(mathparse(generated[':answer/value']),mathparse(sf[':answer-field/correct'][':answer/value']));counts['correct_designations']+=1
        entry=engine_entry(r,'Original '+sid)
        if entry:engine.append(entry)
        original_reviews.append(g.markdown(r,'Original replay'))
        # Changed substantive component, not magnitude-only scaling; preserve source bank.
        rng=random.Random(sid)
        for attempt in range(32):
            changed=dict(case['parameters']);changed['a']=list(changed['a']);rng.shuffle(changed['a']);changed['a']=[str(g.expr(x)*rng.choice((-1,1))) for x in changed['a']]
            try:variant=g.generate(case['level'],21,case['template'],parameters=changed,profile=case['bank_profile'])
            except ValueError:continue
            if variant['generation']['mathematical_fingerprint']!=r['generation']['mathematical_fingerprint']:break
        else:raise AssertionError('No substantive changed source variant')
        check(variant)
        variant_entry=engine_entry(variant,'Generated observed-bank variant '+sid)
        if variant_entry:engine.append(variant_entry)
        review.append(variant);reports.append({'source_id':sid,'bank_values':len(sv),'exact_prompt':True,'exact_solution':True if ':question/worked-solution' in original else 'absent preserved','correct_designation':'matched' if ':answer-field/correct' in sf else 'absent preserved; inferred 8/3 independently','variant_checked':True})
    stats={};positions=set();normal=[]
    for level in ['easy','moderate','hard']:
        prints=[];fingerprints=set();families=set();fields=set();number_forms=set()
        for seed in range(60):
            r=g.generate(level,seed);check(r);normal.append(r);fingerprints.add(r['generation']['mathematical_fingerprint']);families.add(r['generation']['template']);fields.add(r['question'][':question/answer-fields'][0][':answer-field/type']);number_forms.add('radical' if any(g.expr(x).is_Integer is not True for key in ('a','b') for x in r['generation']['parameters'][key]) else 'integer')
            if seed<2:review.append(r)
            entry=engine_entry(r,f'Generated {level} seed {seed}')
            if seed<12:engine.append(entry)
            f=r['question'][':question/answer-fields'][0]
            if len(f[':answer-field/choices'])==5:positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
        assert len(fingerprints)>=45,(level,len(fingerprints));assert len(families)==2;assert len(fields)==2
        if level!='hard':assert number_forms=={'integer','radical'}
        stats[level]={'checked':60,'distinct_meaningful_tasks':len(fingerprints),'families':sorted(families),'fields':sorted(fields),'number_forms':sorted(number_forms)}
    assert len(positions)>1
    # Fixed displayed content survives shuffle/seed, including owned answer IDs.
    for level in ['easy','moderate','hard']:
        r=g.generate(level,5);args=dict(template=r['generation']['template'],parameters=r['generation']['parameters'],field_type=r['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1],profile=r['generation']['bank_profile']);r2=g.generate(level,200,**args)
        assert r['question'][':question/id']==r2['question'][':question/id'];assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
    # Permitted coordinate/norm ceilings and mixed-root boundaries use public calls.
    boundaries=[('easy',{'a':[8,8,4],'b':[1,2,3],'operation':'single'}),('moderate',{'a':[9,12,0],'b':[0,3,4],'operation':'difference'}),('hard',{'a':[4,4,'sqrt(8)'],'b':[1,'sqrt(2)',3],'operation':'sum'})]
    for level,p in boundaries:
        r=g.generate(level,parameters=p);check(r);engine.append(engine_entry(r,'Authored permitted boundary '+level))
    # Explicit guard checks: differing levels and degenerate complete banks fail.
    bad=[('easy',{'a':[1,2,3],'b':[1,0,0],'operation':'sum'}),('moderate',{'a':[1,2,3],'b':[1,3,4],'operation':'difference'}),('hard',{'a':[1,2,2],'b':[1,4,1],'operation':'difference'}),('hard',{'a':[0,2,1],'b':[1,3,4],'operation':'sum'}),('easy',{'a':[0,0,0],'b':[1,2,3],'operation':'single'})]
    for level,p in bad:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('Guard failed',level,p))
    (ROOT/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
    executable=ROOT.parents[1]/'runs/current/check-engine'
    subprocess.run([str(executable),str(ROOT/'engine-input.json'),str(ROOT/'engine.json')],check=True)
    native=json.loads((ROOT/'engine.json').read_text())
    report={'status':'passed','source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','questions':24,'counts':counts,'reports':reports,'designation_missing':1,'native_original_records':23},'generated':stats,'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks']},'formatting':'all displayed source and changed/default math checked','plots':'none','runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'frozen_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT.with_suffix('.py'),ROOT/'recipes.json',ROOT/'source.json',ROOT/'source-cases.json',ROOT/'extract.py',ROOT/'domain_audit.py',ROOT/'domain-audit.json',Path(__file__),executable]}}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'review.md').write_text('# Scalar projection review\n\nOriginal banks are evidence-only; the unrated original intentionally has no designation/solution. Changed source-bank variants retain opaque ratio profiles. Normal authored banks derive specific component-method errors. Hard examples are authored.\n\n'+'\n\n---\n\n'.join(original_reviews+[g.markdown(r,'Generated changed source-mask variant' if r['generation']['evidence_only'] else 'Generated authored default') for r in review])+'\n')
    print(json.dumps({'source_fidelity':counts,'generated':stats,'native':report['native']},indent=2))
if __name__=='__main__':main()
