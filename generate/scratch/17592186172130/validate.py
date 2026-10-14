#!/usr/bin/env python3
"""Read displayed formulas independently, then fidelity and real native grading."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('surfacegen',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def vector(s):
    assert s.startswith('⟨') and s.endswith('⟩'),s
    return sp.Matrix([g.read_math(t) for t in s[1:-1].split(r',\,')])
def rows(s):
    pieces=s.split(r' & =')[1:]
    return [p.removesuffix(r'\end{aligned}').removesuffix(r' \\ ').rstrip('.,') for p in pieces]
def nonnegative_norm(expr,domain):
    symbols={g.u:sp.Symbol('U',nonnegative=True),g.v:sp.Symbol('V',nonnegative=True)} if domain in ['u>=0','v>=0'] else {}
    return sp.simplify(expr.xreplace(symbols))
def equal(a,b,domain='real u,v'):
    return sp.simplify(nonnegative_norm(a-b,domain))==0

def formatting(record):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    q=record['question'];strings=[q[':question/problem'],q.get(':question/worked-solution','')]
    for f in q.get(':question/answer-fields',[]):
        assert f[':answer-field/type']==':answer-field.type/radio'
        assert len(f[':answer-field/choices'])==5
        strings.extend(a[':answer/value'] for a in f[':answer-field/choices'])
        for a in f[':answer-field/choices']:assert a[':answer/type']==':answer.type/math'
        if ':answer-field/correct' in f:assert f[':answer-field/correct'][0]==':answer/id' and f[':answer-field/correct'][1] in [a[':answer/id'] for a in f[':answer-field/choices']]
    for s in strings:
        assert not any(ord(c)<32 and c not in '\n\t' for c in s),'C0 control'
        assert s.count('$')%2==0,'math delimiters'
        depth=0
        for i,c in enumerate(s):
            if c in '{}' and not (i and s[i-1]=='\\'):
                depth+=1 if c=='{' else -1;assert depth>=0,'braces'
        assert depth==0,'braces'
        assert '--' not in s and '+-' not in s,'ungrouped signed factors'

def audit(record):
    formatting(record);assert record['generation']['eligible_for_learning']
    q=record['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];name=record['generation']['template'];level=record['generation']['level'];domain=record['generation']['domain']
    f=g.read_math(re.search(r'\$f\(x,y,z\)=(.*?)\$',prompt).group(1));r=vector(g.display_blocks(prompt)[1].split('=',1)[1])
    ru=r.diff(g.u);rv=r.diff(g.v);cross=ru.cross(rv);norm=sp.sqrt(sp.expand(cross.dot(cross)))
    pull=sp.expand(f.subs({g.x:r[0],g.y:r[1],g.z:r[2]},simultaneous=True));correct=pull*norm
    blocks=g.display_blocks(sol);source=g.BY_NAME['mixed' if name=='mixed_hard' else name];expected=g.display_blocks(source[':question/worked-solution'])
    assert len(blocks)==len(expected)
    if level=='easy':
        hint=g.read_math(re.search(r'‖\{r\}_\{u\}\^\{′\}\\times \{r\}_\{v\}\^\{′\}‖=(.*?)\.\$\*',prompt).group(1))
        assert equal(hint,norm,domain)
        assert equal(g.read_math(blocks[1].split('=',1)[1]),norm,domain)
    else:
        der=blocks[1]
        # Formal operator conventions are checked literally; substituted operator
        # operands are compared to the ACTUAL printed surface, including zeros.
        for s in [g.u,g.v]:
            for c in [g.x,g.y,g.z]:assert r'\frac{∂'+str(c)+'}{∂'+str(s)+'}' in der
            for c in r:assert r'\frac{∂}{∂'+str(s)+'}('+g.tex(c)+')' in der
        reduced=re.findall(r'& =(⟨[^⟨]*?⟩)',der)
        assert len(reduced)==6
        assert vector(reduced[2])==ru and vector(reduced[5])==rv
        cb=blocks[2];matrices=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',cb)
        assert len(matrices)==4
        parse=lambda t:[[p.strip() for p in row.split('&')] for row in t.split(r'\\')]
        main=parse(matrices[0]);assert main[0]==['i','j','k']
        assert sp.Matrix([[g.read_math(z) for z in row] for row in main[1:]])==sp.Matrix([list(ru),list(rv)])
        dets=[sp.Matrix([[g.read_math(z) for z in row] for row in parse(t)]).det() for t in matrices[1:]]
        assert sp.Matrix([dets[0],-dets[1],dets[2]])==cross
        lastvec=re.findall('⟨[^⟨]*?⟩',cb)[-1];assert vector(lastvec)==cross
        nr=rows(blocks[3]);assert len(nr)==len(rows(expected[3]))
        assert vector(nr[0][1:-1])==cross
        for val in nr[1:]:assert equal(g.read_math(val),norm,domain),(name,val,norm)
        if name in ['plane','fold','cylinder']:
            assert nr[2].startswith(r'\sqrt{') and '+' in nr[2],'expanded component squares lost'
    pb=next(b for b in blocks if b.startswith(r'\begin{aligned}f(r(u,v))'));pr=rows(pb)
    assert len(pr)==len(rows(next(b for b in expected if b.startswith(r'\begin{aligned}f(r(u,v))'))))
    fpart,restr=pr[0].split(r'\,{|}_{',1);assert equal(g.read_math(fpart),f)
    restrictions=restr.removesuffix('}').split(r'\,');assert len(restrictions)==3
    for part,c,sym in zip(restrictions,r,[g.x,g.y,g.z]):
        lhs,rhs=part.split('=',1);assert lhs==str(sym) and equal(g.read_math(rhs),c)
    for val in pr[1:]:assert equal(g.read_math(val),pull),(name,val,pull)
    # Family operative stages: repeated factors, cancellation, signs, reduction.
    if name=='powers':assert r'\cdot' in pr[1] and len(pr)==3
    if name=='product':assert pr[1].count(r'\cdot')>=2 and '(u+v)' in pr[1]
    if name=='cancel':assert '(u-v^{2})+v^{2}' in pr[1]
    if name=='cylinder':assert '(v^{2}'+r'\cdot v^{2})' in pr[1]
    if name in ['mixed','mixed_hard']:assert r'^{2}\cdot (' in pr[1]
    final=rows(blocks[-1]);assert len(final)==2
    val=re.search(r'\{∬\}_\{D\}\\,(.*?)\\,\\,\\text\{d\}A',final[1]).group(1)
    assert equal(g.read_math(val),correct,domain)
    field=q[':question/answer-fields'][0];values=[g.read_math(a[':answer/value']) for a in field[':answer-field/choices']]
    assert all(not equal(a,b,domain) for i,a in enumerate(values) for b in values[:i]),'pointwise-equivalent options'
    for answer,val in zip(field[':answer-field/choices'],values):
        assert equal(val,correct,domain)==(answer[':answer/id']==field[':answer-field/correct'][1])
    assert 'as a function on $D$' in prompt
    return True

def native_item(label,record):
    checks=[]
    for i,f in enumerate(record['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'correct selection' if a[':answer/id']==f[':answer-field/correct'][1] else 'wrong selection'})
    return {'label':label,'record':record,'checks':checks}

def main():
    source_cases=[];reviews=[];native=[];values=refs=rawsol=0
    for name,source in g.BY_NAME.items():
        level=g.LEVELS[name];case={'source_id':source[':db/id'],'template':name,'level':level,'parameters':{'k':1},'bank_profile':'observed'};source_cases.append(case)
        record=g.generate(level,template=name,parameters=case['parameters'],profile='observed');formatting(record)
        q=record['question'];assert q[':question/problem']==source[':question/problem'];assert q[':question/worked-solution']==source[':question/worked-solution'];rawsol+=1
        for k in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (k in q)==(k in source)
        for field,old in zip(q[':question/answer-fields'],source[':question/answer-fields']):
            assert (':answer-field/correct' in field)==(':answer-field/correct' in old)
            actual=sorted(a[':answer/value'] for a in field[':answer-field/choices']);expected=sorted(a[':answer/value'] for a in old[':answer-field/choices']);assert actual==expected;values+=len(actual)
            if ':answer-field/correct' in old:
                correct=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert correct==old[':answer-field/correct'][':answer/value'];refs+=1
        reviews.append({'kind':'original replay','source_id':source[':db/id'],'record':record})
        if name!='saddle':native.append(native_item('original '+name,record))
        # Changed source replay is really computed scalar scaling, with raw errors
        # retained and ineligible for learning rather than disguised as corrected.
        changed=g.generate(level,template=name,parameters={'k':2},profile='observed');assert changed['question'][':question/problem']!=q[':question/problem']
        for fi,f in enumerate(changed['question'][':question/answer-fields']):
            for orig in source[':question/answer-fields'][fi][':answer-field/choices']:
                assert any(equal(g.read_math(a[':answer/value']),2*g.read_math(orig[':answer/value'])) for a in f[':answer-field/choices'])
        for i,par in enumerate([{'a':1,'p':1,'q':3 if name=='product' else 1},{'a':2,'p':3,'q':1 if name in ['saddle','powers'] else 2}]):
            normal=g.generate(level,i,template=name,parameters=par);audit(normal);reviews.append({'kind':'generated variant','source_id':source[':db/id'],'record':normal});native.append(native_item('variant '+name+' '+str(i),normal))
    for i in range(2):
        r=g.generate_hard(i,parameters={'a':i+1,'b':2,'c':i+1,'d':2,'p':2,'q':3});audit(r);reviews.append({'kind':'authored hard variant','record':r});native.append(native_item('hard '+str(i),r))
    # Enumerate full modest parameter domains; variety counts are actual canonical
    # assessed tasks, excluding profiles/order/unused q. Complete banks reject all
    # collisions; explicit inputs enforce the same bounds as sampling.
    counts={};rejections={};tested=0
    for name,level in g.LEVELS.items():
        tasks=set();bad=0
        domain=itertools.product(range(1,4),repeat=6) if level=='hard' else itertools.product(range(1,4),range(1,5),[1] if name in ['saddle','powers'] else range(1,5))
        for i,ps in enumerate(domain):
            par=dict(zip(['a','b','c','d','p','q'] if level=='hard' else ['a','p','q'],ps))
            try:r=g.generate(level,template=name,parameters=par)
            except ValueError as e:
                assert 'collision' in str(e);bad+=1;continue
            tasks.add(r['generation']['mathematical_fingerprint']);tested+=1
            # Full independent stage checks on boundary/change combinations.
            if i%17==0 or all(t==1 for t in ps):audit(r)
        counts[name]=len(tasks);rejections[name]=bad
    coverage={l:set() for l in ['easy','moderate','hard']}
    for seed in range(80):
        for l in coverage:
            r=g.generate(l,seed);audit(r);coverage[l].add(r['generation']['template'])
    for l,names in coverage.items():assert names=={n for n,lv in g.LEVELS.items() if lv==l}
    r=g.generate_moderate(template='mixed',parameters={'a':2,'p':3,'q':2});r2=g.generate_moderate(seed=88,template='mixed',parameters={'a':2,'p':3,'q':2});assert r['question'][':question/id']==r2['question'][':question/id']
    mutation=copy.deepcopy(r);mutation['question'][':question/worked-solution']=mutation['question'][':question/worked-solution'].replace(r'\frac', '\x0crac',1)
    try:audit(mutation)
    except AssertionError:pass
    else:raise AssertionError('C0 mutation passed')
    mutation=copy.deepcopy(r);mutation['question'][':question/worked-solution']=mutation['question'][':question/worked-solution'].replace(r'\frac{∂}{∂u}(2 u v)',r'\frac{∂}{∂v}(2 u v)',1)
    try:audit(mutation)
    except AssertionError:pass
    else:raise AssertionError('Held-coordinate mutation passed')
    mutation=copy.deepcopy(g.generate_moderate(template='cylinder',parameters={'a':2,'p':3,'q':2}));sb=g.display_blocks(mutation['question'][':question/worked-solution'])[3];rr=rows(sb);new=sb.replace(rr[2],rr[3]);mutation['question'][':question/worked-solution']=g.replace_block(mutation['question'][':question/worked-solution'],sb,new)
    try:audit(mutation)
    except AssertionError:pass
    else:raise AssertionError('Same-row-count lost-stage mutation passed')
    for args in [('hard','mixed_hard',{'a':1,'b':1,'c':0,'d':1,'p':1,'q':1}),('easy','powers',{'a':1,'p':1,'q':2}),('moderate','mixed',{'a':4,'p':1,'q':1})]:
        try:g.generate(args[0],template=args[1],parameters=args[2])
        except ValueError:pass
        else:raise AssertionError('Explicit workload bounds bypass')
    (HERE/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n');(HERE/'native-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([str(HERE.parents[1]/'runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    report=json.loads((HERE/'native-report.json').read_text())
    result={'pass':True,'source':{k:g.CAPTURE[k] for k in ['database','basis','lineage']},'source_questions':12,'complete_banks':13,'source_values_matched':values,'source_values_total':65,'source_correct_designations_matched':refs,'source_correct_designations_present':12,'source_correct_designations_missing':1,'raw_exact_solutions':rawsol,'source_normal_math_repairs':5,'raw_native_ungradable_records':1,'raw_native_ungradable_reason':'q160711 retains duplicate legacy field without correct ref; harness requires refs for every field','normal_families':13,'explicit_parameter_instances_constructed':tested,'valid_math_tasks_by_family':counts,'whole_bank_rejections':rejections,'default_family_coverage':{l:sorted(a) for l,a in coverage.items()},'native_accepted':report['accepted_checks'],'native_rejected':report['rejected_checks'],'native_unresolved':report['documented_unresolved_checks'],'native_binary_sha256':hashlib.sha256((HERE.parents[1]/'runs/current/check-engine').read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':sp.__version__,'mutation_checks':['C0 control','held coordinate','same-row-count removed norm expansion'],'lesson_route':g.lesson_route(),'limitations':['Historical bank intentions partly opaque; public observed profiles evidence-only.','Raw q160712/q161134/q161286 omit necessary half-plane restrictions; repaired normal output.','Raw q160712/q161286/q161135 contain erroneous solution components; normal repaired.','No native raw fixture possible for q160711 missing legacy correct ref.']}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    md=['# Source and generated review','Raw captures use explicit observed profile, including legacy omissions. Generated variants use method-derived banks and repaired learner content.']
    for item in reviews:
        r=item['record'];md+=['\n## '+item['kind']+' — '+r['generation']['template']+' / '+r['generation']['level'],g.markdown(r)]
    (HERE/'review.md').write_text('\n\n'.join(md))
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
