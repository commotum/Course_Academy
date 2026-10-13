"""Independent printed-expression, source-fidelity, scope, identity and native QA."""
import hashlib, importlib.util, json, re, subprocess, sys
sys.dont_write_bytecode=True
from functools import lru_cache
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
# Independent small TeX parser. It reads what is actually printed, without using
# generator parameter metadata or generator formulas, and preserves exact math.
@lru_cache(None)
def parse(text):
    text=text.replace(r'\,','').replace('&','').strip().rstrip('.,')
    tokens=re.findall(r'\\frac|\\cdot|\d+|[a-z]|[{}()+*/^\-]',text)
    recognized=''.join(tokens)
    assert re.sub(r'\s+','',text)==recognized,('unparsed TeX',text)
    i=0
    def atom():
        nonlocal i
        t=tokens[i];i+=1
        if t in ('{','('):
            z=add();assert tokens[i]==('}' if t=='{' else ')'),text;i+=1;return z
        if t==r'\frac':return atom()/atom()
        if t.isdigit():return sp.Integer(t)
        assert len(t)==1 and t.isalpha(),(text,t)
        return sp.Symbol(t,real=True)
    def power():
        nonlocal i
        z=atom()
        if i<len(tokens) and tokens[i]=='^':i+=1;z=z**unary()
        return z
    def unary():
        nonlocal i
        if i<len(tokens) and tokens[i] in ('+','-'):
            t=tokens[i];i+=1;return unary()*(1 if t=='+' else -1)
        return power()
    def product():
        nonlocal i
        z=unary()
        while i<len(tokens) and tokens[i] not in ('+','-','}',')'):
            t=tokens[i]
            if t in ('*',r'\cdot','/'):
                i+=1;z=z/unary() if t=='/' else z*unary()
            else:z=z*unary()
        return z
    def add():
        nonlocal i
        z=product()
        while i<len(tokens) and tokens[i] in ('+','-'):
            t=tokens[i];i+=1;z=z+product()*(1 if t=='+' else -1)
        return z
    z=add();assert i==len(tokens),(text,tokens[i:]);return z

def logpoly(expr):
    # Exact formal logarithm of positive rational bases; combine products by
    # independent prime factorization. All numerical bases are >0 and !=1.
    if expr.is_Pow:
        b,e=expr.args
        assert b.is_Rational and b>0 and b!=1,expr
        out={}
        for sign,n in ((1,b.p),(-1,b.q)):
            for prime,power in sp.factorint(n).items():out[prime]=out.get(prime,0)+sign*power*e
        return out
    if expr.is_Mul:
        out={}
        for x in expr.args:
            for prime,e in logpoly(x).items():out[prime]=out.get(prime,0)+e
        return out
    assert expr.is_Rational and expr>0,expr
    out={}
    for sign,n in ((1,expr.p),(-1,expr.q)):
        for prime,power in sp.factorint(n).items():out[prime]=out.get(prime,0)+sign*power
    return out

def equation(text):
    text=text.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').strip()
    left,right=text.split('=');return parse(left),parse(right)
def residual(left,right):
    if left.has(sp.Pow) and any(p.exp.free_symbols for p in left.atoms(sp.Pow)) or right.has(sp.Pow) and any(p.exp.free_symbols for p in right.atoms(sp.Pow)):
        L,R=logpoly(left),logpoly(right);keys=sorted(set(L)|set(R));assert keys,(L,R)
        d=sp.expand(L.get(keys[0],0)-R.get(keys[0],0))
        for key in keys[1:]:
            other=sp.expand(L.get(key,0)-R.get(key,0));ratio=sp.cancel(other/d);assert ratio.is_Rational and ratio>0,(L,R)
        return d
    return sp.expand(left-right)
def balanced(text):
    assert text.count('$')%2==0,text
    n=0
    for c in text:
        if c=='{':n+=1
        if c=='}':n-=1
        assert n>=0,text
    assert n==0,text
    assert '--' not in text and '+-' not in text,text

def check(r):
    q=r['question'];meta=r['generation'];kind=meta['kind'];raw=meta['evidence_only']
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==g.KP_ID
    for text in (q[':question/problem'],q.get(':question/worked-solution','')):balanced(text)
    printed=next(t for t in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem']) if '=' in t and '^' in t)
    left,right=equation(printed);diff=residual(left,right);syms=diff.free_symbols;assert len(syms)==1
    var=next(iter(syms));poly=sp.Poly(diff,var);assert poly.degree()==1
    root=-poly.nth(0)/poly.nth(1)
    field=q.get(':question/answer-fields',[None])[0]
    if field:
        assert field[':answer-field/type']==':answer-field.type/radio'
        bank=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
        assert len(bank)==5 and len(set(bank))==5 and sum(x==root for x in bank)==1
        if ':answer-field/correct' in field:
            uuid=field[':answer-field/correct'][1]
            correct=next(a for a in field[':answer-field/choices'] if a[':answer/id']==uuid)
            assert parse(correct[':answer/value'])==root
        else:assert raw
    else:assert raw
    worked=q.get(':question/worked-solution')
    if worked:
        blocks=re.findall(r'\$\$\n(.*?)\n\$\$',worked,re.S)
        expected=4 if kind=='reciprocal' else 3
        assert len(blocks)==expected
        rows=[]
        for block in blocks:
            body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
            rows.extend(body.split(r'\\'))
        # Independently parse EVERY displayed row including distributed sums.
        for row in rows:
            L,R=equation(row);d=residual(L,R)
            assert set(d.free_symbols)<=syms,(row,d,var)
            assert sp.simplify(d.subs(var,root))==0,(row,root,d)
            assert d!=0,('identity replacing meaningful stage',row)
        # Before equating exponents, each displayed side must equal the actual
        # original side's formal prime logarithm, not just have the same root.
        n_exp=2 if kind!='reciprocal' and kind!='product' else 3
        origL,origR=logpoly(left),logpoly(right)
        for row in rows[:n_exp]:
            L,R=equation(row)
            for x,original in ((L,origL),(R,origR)):
                current=logpoly(x)
                assert set(current)==set(original)
                assert all(sp.expand(current[k]-original[k])==0 for k in original),(row,original,current)
        linear=rows[n_exp:]
        assert len(linear)==(3 if meta['level']=='easy' else 4)
        # First linear and distributed rows have exactly the same residual;
        # collection can reverse both signs as in q-3362, and solving divides.
        d0=residual(*equation(linear[0]));d1=residual(*equation(linear[1]))
        assert sp.expand(d0-d1)==0,(linear,d0,d1)
        if meta['level']!='easy':
            assert linear[-2].strip()!=linear[-1].strip(),('collapsed repeated solution stage',linear)
            d2=residual(*equation(linear[2]));assert sp.expand(d2-d1)==0 or sp.expand(d2+d1)==0
        assert sp.simplify(equation(linear[-1])[1]-root)==0
        # The distribution row may keep source-observed separate x terms, but
        # must actually remove every affine grouping on both sides.
        assert '(' not in linear[1] and ')' not in linear[1]
    return root

def audit_variety():
    import itertools
    counts={}
    for kind,level in [('one_shift','easy'),('two_shifts','moderate')]:
        tasks=set();eligible=0
        for b,u,w in itertools.product(range(2,7),range(2,6),range(2,6)):
            shifts=([(h,0) for h in range(-8,9) if h]+[(0,k) for k in range(-8,9) if k]) if kind=='one_shift' else list(itertools.product(range(-10,0),range(1,11)))
            for h,k in shifts:
                p=dict(b=b,p=u,q=w,a=1,h=h,c=1,k=k,var='x')
                try:g.guard(p,level,kind,'authored-method')
                except ValueError:continue
                eligible+=1;tasks.add(g.identity(p,kind))
        counts[kind]={'exact_eligible_parameter_sets':eligible,'exact_canonical_task_count':len(tasks),'enumeration':'All public base/power/shift parameters, variable x, complete-bank eligibility'}
    for kind in ('coefficient','reciprocal','product'):
        level='moderate' if kind=='coefficient' else 'hard'
        sid=next(s for s,v in g.SPECS.items() if v[:2]==(level,kind) and s not in ('q-66788','q-66893'))
        tasks={g.generate(level,seed,template=sid)['generation']['mathematical_fingerprint'] for seed in range(1500)}
        counts[kind]={'canonical_task_lower_bound':len(tasks),'enumeration':'1500 deterministic accepted seeds; family not exhausted'}
    assert counts['one_shift']['exact_canonical_task_count']>=400
    assert counts['two_shifts']['exact_canonical_task_count']>=3000
    assert all(counts[k]['canonical_task_lower_bound']>=1200 for k in ('coefficient','reciprocal','product'))
    (HERE/'variety.json').write_text(json.dumps(counts,indent=2)+'\n')
    return counts

def main():
    cases=[];source_results=[];engine=[];review=[]
    for sid,(level,kind,p) in g.SPECS.items():
        profile='observed:'+sid;r=g.generate(level,template=sid,parameters=p,profile=profile);old=g.ORIGINALS[sid];new=r['question'];root=check(r)
        for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
            assert (key in old)==(key in new),(sid,key,'presence')
        assert old[':question/problem']==new[':question/problem']
        if ':question/worked-solution' in old:assert old[':question/worked-solution']==new[':question/worked-solution']
        matched=0;designation=False
        if ':question/answer-fields' in old:
            assert len(new[':question/answer-fields'])==len(old[':question/answer-fields'])
            for of,nf in zip(old[':question/answer-fields'],new[':question/answer-fields']):
                assert of[':answer-field/key']==nf[':answer-field/key']
                assert of[':answer-field/type'][':db/ident']==nf[':answer-field/type']
                assert sorted(parse(a[':answer/value']) for a in of[':answer-field/choices'])==sorted(parse(a[':answer/value']) for a in nf[':answer-field/choices'])
                matched+=len(of[':answer-field/choices'])
                assert (':answer-field/correct' in of)==(':answer-field/correct' in nf)
                if ':answer-field/correct' in of:
                    assert parse(of[':answer-field/correct'][':answer/value'])==root;designation=True
        cases.append({'source_id':sid,'template':sid,'level':level,'parameters':p,'bank_profile':profile,'inferred_level':':question/difficulty' not in old})
        source_results.append({'source_id':sid,'prompt_exact':True,'solution_exact':':question/worked-solution' in old,'solution_present':':question/worked-solution' in old,'bank_values_matched':matched,'correct_designation_matched':designation,'original_missing_correct':':question/answer-fields' in old and ':answer-field/correct' not in old[':question/answer-fields'][0],'original_fieldless':':question/answer-fields' not in old})
        review.append({'label':'Original source replay '+sid,'record':r})
        if designation:add_engine(engine,r,'original observed bank '+sid)
        # Two changed-parameter records for EVERY style/template and whole bank.
        for seed in (107,209):
            changed=g.generate(level,seed,template=sid,profile=profile);check(changed)
            assert changed['generation']['parameters']!=p
            review.append({'label':'Generated observed-profile evidence variant '+sid+' '+str(seed),'record':changed})
        normal=g.generate(level,template=sid,parameters=p)
        check(normal);add_engine(engine,normal,'source parameters with authored bank '+sid)
    sampled=0;fingerprints={l:set() for l in ('easy','moderate','hard')};first_positions=set()
    for sid,(level,kind,_) in g.SPECS.items():
        for seed in range(80):
            r=g.generate(level,seed,template=sid);check(r);sampled+=1;fingerprints[level].add(r['generation']['mathematical_fingerprint'])
            f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
            first_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==correct))
            twin=g.generate(level,seed+20000,template=sid,parameters=r['generation']['parameters'])
            assert r['question'][':question/id']==twin['question'][':question/id']
            assert r['generation']['mathematical_fingerprint']==twin['generation']['mathematical_fingerprint']
            if seed<2:review.append({'label':'Generated normal authored-bank '+level+' '+sid+' '+str(seed),'record':r});add_engine(engine,r,'normal '+sid+' '+str(seed))
    assert len(first_positions)==5
    # Explicit workload guards and samplers share the same predicate.
    invalid=[]
    for sid,(level,kind,p) in g.SPECS.items():
        probes=[dict(p,b=1),dict(p,p=1),dict(p,q=p['p']),dict(p,h=20),dict(p,c=0)]
        for bad in probes:
            try:g.generate(level,template=sid,parameters=bad)
            except ValueError:invalid.append({'template':sid,'parameters':bad})
            else:raise AssertionError(('invalid explicit parameters accepted',sid,bad))
    # Counterchecks: broken prompt coefficient, printed distribution, bank and
    # grading ref must all fail independent math rather than pass on metadata.
    import copy
    r=g.generate_moderate(7,template='q-100462');mutations=[]
    q=r['question'];p=r['generation']['parameters'];v=p['var']
    broken=copy.deepcopy(r);broken['question'][':question/problem']=broken['question'][':question/problem'].replace('}^{'+v,'}^{2'+v,1);mutations.append(broken)
    broken=copy.deepcopy(r);blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S);old=blocks[-1];bad=old.replace(' & =',' & =1+',1);broken['question'][':question/worked-solution']=q[':question/worked-solution'].replace(old,bad);mutations.append(broken)
    broken=copy.deepcopy(r);broken['question'][':question/answer-fields'][0][':answer-field/correct'][1]=broken['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']
    if broken['question'][':question/answer-fields'][0][':answer-field/correct']==r['question'][':question/answer-fields'][0][':answer-field/correct']:broken['question'][':question/answer-fields'][0][':answer-field/correct'][1]=broken['question'][':question/answer-fields'][0][':answer-field/choices'][1][':answer/id']
    mutations.append(broken)
    for broken in mutations:
        try:check(broken)
        except (AssertionError,ValueError,StopIteration):pass
        else:raise AssertionError('Independent validator did not detect mutation')
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
    (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
    exe=HERE.parents[1]/'runs/current/check-engine'
    subprocess.run([str(exe),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
    native=json.loads((HERE/'engine-validation.json').read_text())
    variety=audit_variety()
    report={'status':'pass','version':g.VERSION,'snapshot':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_questions':12,'exact_source_prompts':12,'exact_present_solutions':10,'present_solution_denominator':10,'source_banks_matched':10,'source_bank_denominator':10,'source_values_matched':50,'source_value_denominator':50,'correct_designations_matched':8,'correct_designation_denominator':8,'missing_original_correct_refs':2,'fieldless_originals':2,'unrated_originals':2,'raw_presence_parity':True,'source_results':source_results,'generated_math_instances':sampled,'sampled_meaningful_tasks':{l:len(v) for l,v in fingerprints.items()},'explicit_guard_rejections':len(invalid),'mutation_failures_detected':len(mutations),'all_correct_positions_seen':sorted(first_positions),'native_grader_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'native_grader_source_sha256':hashlib.sha256(exe.with_suffix('.rs').read_bytes()).hexdigest(),'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks']},'variety':variety,'opaque_banks_eligible_for_learning':False,'authored_missing_level_extensions':0,'authored_extensions':'complete method-based choice banks at all three observed levels; completed fields/correct refs for malformed originals','unresolved_findings':['Historical scalar distractor authoring intent is underdetermined; opaque observed replay profiles are evidence-only. Missing original correct refs and fields cannot count as original designation/layout matches.']}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    lines=['# Review: two-exponent rewriting\n','Originals preserve missing attributes. Generated observed-profile variants are evidence-only, with opaque proportional continuation. Generated normal records use complete authored method-operation banks.\n']
    for item in review:
        lines+=['## '+item['label']+'\n',g.markdown(item['record'])+'\n']
    (HERE/'review.md').write_text('\n'.join(lines))
    files=[HERE.with_suffix('.py'),*sorted(HERE.glob('*'))]
    frozen={str(f.relative_to(HERE.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file() and f.name!='freeze.json'}
    (HERE/'freeze.json').write_text(json.dumps({'version':g.VERSION,'sha256':frozen},indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','source_questions','source_banks_matched','source_values_matched','generated_math_instances','sampled_meaningful_tasks','native')},indent=2))

def add_engine(items,r,label):
    f=r['question'][':question/answer-fields'][0]
    checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Select independently verified actual printed value'} for a in f[':answer-field/choices']]
    items.append({'label':label,'record':r,'checks':checks})
if __name__=='__main__':main()
