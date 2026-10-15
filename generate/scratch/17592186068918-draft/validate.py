"""Independent printed-stage, fidelity, identity, domain and native checks."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from functools import lru_cache
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('quotient_draft_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
p=g.printed;x=p.x;u=p.u

def save(n,v):(HERE/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
@lru_cache(maxsize=30000)
def zero_core(e):return sp.trigsimp(e)==0
def zero(e):
    reduced=sp.cancel(e)
    if reduced==0:return True
    _,primitive=reduced.as_content_primitive()
    return zero_core(primitive)
@lru_cache(maxsize=30000)
def eq(a,b,indef=False):
    difference=sp.diff(a-b,x) if indef else a-b
    if difference==0:return True
    # A single exact rational evaluation distinguishes unequal functions; expensive
    # symbolic reduction is reserved for candidate equivalences.
    value=difference.subs(x,sp.Rational(1,5)) if indef else difference
    try:
        if abs(complex(value.evalf(30)))>1e-16:return False
    except (ValueError,TypeError):pass
    return zero(difference) if indef else (sp.simplify(difference)==0 or sp.simplify(sp.expand_log(difference,force=True))==0)

def tex(t):return p.scalar(t.strip().rstrip('.,')).subs(p.C,0)
def as_scalar(t):
    # Source primitive endpoint operators bind exactly their printed bounds.
    t=p.clean(t).replace(r'\big|','|').replace(r'{|}','|')
    matches=list(re.finditer(r'\|_',t))
    if matches:
        m=matches[0];a,end=p.group(t,m.end());assert t[end]=='^';b,end=p.group(t,end+1)
        pre=t[:m.start()];post=t[end:]
        # A multiplier wrapping the complete evaluation has a closing parenthesis.
        opening=pre.count('(')-pre.count(')');closing=')'*opening
        expr=tex(pre+closing);value=expr.subs(u,tex(b))-expr.subs(u,tex(a))
        assert post==closing,(post,closing,t)
        return value
    return tex(t)

@lru_cache(maxsize=30000)
def finite_real(e):
    if e.is_real is False:return False
    try:v=complex(e.evalf());return abs(v.imag)<1e-10 and abs(v.real)<1e100
    except (TypeError,ValueError):return False

def check_domains(r):
    q=r['question'];f,lo,hi=p.integral(q[':question/problem']);indef=lo is None
    bank=[tex(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
    # Source q10046 contains ln(1-sqrt2): retained explicitly in raw evidence.
    nonreal=[i for i,a in enumerate(bank) if not a.has(x) and not finite_real(a)]
    if nonreal:assert r['generation']['evidence_only'] and r['generation']['template']=='q-10046'
    if not indef:
        assert lo<hi
        for j in range(41):assert finite_real(f.subs(x,lo+(hi-lo)*sp.Rational(j,40)))
    else:
        # Every choice is interpreted on its connected real domain. This samples a
        # points in real components; analytic poles/zero predicates are documented.
        for a in bank:
            for point in [sp.Rational(1,5),sp.Rational(2,5),sp.Rational(3,5)]:assert finite_real(a.subs(x,point)),(a,point)

def stages(r):
    q=r['question'];sol=q.get(':question/worked-solution');f,lo,hi=p.integral(q[':question/problem']);indef=lo is None
    if sol is None:return
    # Read u from actual prose, protect complete arguments before proxy normalization.
    match=re.search(r'\$u\s*=\s*(.*?)\.?,\$|\$u\s*=\s*(.*?)\.\$',sol)
    assert match,sol
    inner=tex(next(z for z in match.groups() if z is not None))
    blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
    for b in blocks:
        if r'\begin{aligned}' in b:continue
        if '=' not in b:continue
        left,right=b.strip().split('=',1);right=right.split('⟹')[0].strip().rstrip(r'\,').strip()
        # Formal derivative of the denominator and du/dx are separate source rows.
        if r'\frac{\text{d}}' in left:
            arg=re.search(r'\}\((.*)\)$',left.strip());assert arg,left
            assert zero(tex(right)-sp.diff(tex(arg[1]),x))
        else:
            assert r'\frac{\text{d}u}' in left,left
            assert zero(tex(right)-sp.diff(inner,x)),(right,inner)
        if '⟹' in b:
            differential=b.split('⟹',1)[1].strip().rstrip('.')
            lhs,rhs=differential.split('=',1)
            def dcoef(z):
                z=p.clean(z).replace('D','d');z=re.sub(r'd\s*[xyu]','',z);z=z.replace('(', '').replace(')','') if z.strip() in ('(-du)','(du)') else z
                return -sp.Integer(1) if z.strip()=='-' else (tex(z) if z.strip() else sp.Integer(1))
            assert zero(dcoef(lhs)*sp.diff(inner,x)-dcoef(rhs)),differential
    chain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert chain
    rows=chain[1].split('\\\\');assert len(rows)>=4
    # Actual ordered chain, not just equality/row counts. Whole source rows retain
    # integral decomposition, grouped u factors, factor extraction and endpoints.
    first=rows[0].split('&',1)[0];ff,ll,hh,v=p.read_integral(first);assert zero(ff-f) and (ll,hh)==(lo,hi)
    last_primitive=None;need_endpoints=False
    for row in rows:
        body=row.split('&',1)[1].strip();assert body.startswith('=');body=body[1:].strip()
        if r'\int' in body:
            e,a,b,var=p.read_integral(body)
            if var=='u':
                assert zero(e.subs(u,inner)*sp.diff(inner,x)-f),(body,e,f)
                if not indef:assert eq(a,inner.subs(x,lo)) and eq(b,inner.subs(x,hi))
            else:assert zero(e-f) and (a,b)==(lo,hi),(body,e,f)
        elif indef:
            value=tex(body)
            if value.has(u):assert zero(sp.diff(value,u).subs(u,inner)*sp.diff(inner,x)-f)
            else:assert zero(sp.diff(value,x)-f),(body,value,f)
        else:
            if '|_' in p.clean(body).replace(r'{|}','|').replace(r'\big|','|'):
                # Independently differentiate displayed primitive and verify both
                # individually substituted endpoint values before their subtraction.
                z=p.clean(body).replace(r'{|}','|').replace(r'\big|','|');m=z.index('|_');pre=z[:m];op=pre.count('(')-pre.count(')');primitive=tex(pre+')'*op)
                assert zero(sp.diff(primitive,u).subs(u,inner)*sp.diff(inner,x)-f)
                last_primitive=primitive;need_endpoints=True
            logs=[];zt=p.clean(body);zt=re.sub(r'\\operatorname\{ln\}',r'\\ln',zt)
            for matchlog in re.finditer(r'\\ln',zt):
                j=matchlog.end()
                while j<len(zt) and zt[j].isspace():j+=1
                if zt[j:j+1] in ('(', '{'):
                    arg,_=p.group(zt,j);logs.append(tex(arg))
                elif zt[j:j+1].isdigit():logs.append(tex(re.match(r'\d+',zt[j:])[0]))
            if len(logs)==2 and need_endpoints:
                need_endpoints=False
                assert eq(logs[0],inner.subs(x,hi)) and eq(logs[1],inner.subs(x,lo)),('individual endpoints',logs,body)
            value=as_scalar(body);expected=None
            # Exact displayed primitive supplies each endpoint independently.
            if last_primitive is not None:
                expected=last_primitive.subs(u,inner.subs(x,hi))-last_primitive.subs(u,inner.subs(x,lo))
                assert eq(value,expected),(body,value,expected)
    if not indef:
        table=re.search(r'\| \$[xy]\$ \| \$(.*?)\$ \| \$(.*?)\$ \|\n\| --- \| --- \| --- \|\n\| \$u\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol);assert table
        a,b,c,d=map(tex,table.groups());assert (a,b)==(lo,hi) and eq(c,inner.subs(x,a)) and eq(d,inner.subs(x,b))
    # Structural source masks: each operative row is an independently required
    # stage. An algebraically equal but collapsed integral row must fail.
    t=r['generation']['template'];m=r['generation']['parameters'].get('m')
    if t=='q-113997':assert '$K=C+'+str(m)+'.$' in sol
    if t in g.DATA and g.QUESTIONS[t].get(':question/worked-solution'):
        anchor=g.QUESTIONS[t][':question/worked-solution'];original_rows=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',anchor,re.S)[1].split('\\\\')
        assert len(rows)==len(original_rows)
        for actual,old in zip(rows,original_rows):
            for token in [r'\int',r'\frac{1}{u}',r'\cdot',r'\text{d}u']:
                assert actual.replace(str(m)+r'\cdot ','').count(token)==old.count(token),(token,actual,old)
            # u-1 rewrite and expanded integrand remain two separate stages.
            if '(u-1)' in old:assert '(u-1)' in actual
            if r'(1-\frac{1}{u})' in old:assert r'(1-\frac{1}{u})' in actual

def check(r):
    q=r['question'];meta=r['generation'];raw=meta['evidence_only'];t=meta['template']
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert meta['eligible_for_learning']==(not raw)
    for name in (':question/problem',':question/worked-solution'):
        if name in q:
            assert not any(ord(c)<32 and c not in '\n\t' for c in q[name]);g.fmt.validate_prose(q[name])
    f,lo,hi=p.integral(q[':question/problem']);indef=lo is None
    expected,F,a,c,inner,h,H,var,elo,ehi=g.math_data(t,meta['parameters']);assert zero(f-expected) and (lo,hi)==(elo,ehi)
    assert zero(sp.diff(F,x)-f)
    assert meta['mathematical_fingerprint']==g.math_fingerprint(f,lo,hi)
    field=q[':question/answer-fields'][0];vals=[tex(z[':answer/value']) for z in field[':answer-field/choices']]
    for choice in field[':answer-field/choices']:
        g.fmt.validate_tex(choice[':answer/value']);assert not any(ord(c)<32 for c in choice[':answer/value'])
    matches=[eq(v,F if indef else a,indef) for v in vals]
    if not raw:
        if field[':answer-field/type'].endswith('radio'):
            assert sum(matches)==1,(t,matches)
            for i,v in enumerate(vals):
                for w in vals[:i]:assert not eq(v,w,indef),(t,v,w)
        else:assert all(matches)
        ref=field[':answer-field/correct'][1];assert next(matches[i] for i,z in enumerate(field[':answer-field/choices']) if z[':answer/id']==ref)
    if raw and ':answer-field/correct' in field:
        ref=field[':answer-field/correct'][1]
        assert next(matches[i] for i,z in enumerate(field[':answer-field/choices']) if z[':answer/id']==ref)
        assert all(matches) if field[':answer-field/type'].endswith('blank') else sum(matches)==1
    assert ('{{field-1}}' in q[':question/problem'])==field[':answer-field/type'].endswith('blank')
    check_domains(r);stages(r)
    return r

def main():
    source_cases=[];replay=[];review=[];native=[];normal=[];counts={};fps=set()
    for t,old in g.QUESTIONS.items():
        print('replay',t,flush=True)
        level=g.DATA[t][0];r=check(g.generate(level,template=t,parameters={'m':1},profile='observed'));q=r['question'];of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
        for k in [':question/problem',':question/worked-solution']:
            assert (k in q)==(k in old);assert q.get(k)==old.get(k)
        assert (':question/difficulty' in q)==(':question/difficulty' in old)
        assert (':answer-field/correct' in nf)==(':answer-field/correct' in of)
        assert sorted(z[':answer/value'] for z in nf[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices'])
        if ':answer-field/correct' in of:
            assert next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
        source_cases.append({'source_id':t,'template':t,'difficulty':level,'parameters':{'m':1},'bank_profile':'observed','observed_difficulty':old.get(':question/difficulty'),'evidence_only':True,'eligible_for_learning':False})
        replay.append({'source_id':t,'exact_prompt':True,'exact_solution_or_omission':True,'key_presence_parity':True,'values':len(of[':answer-field/choices']),'designation_matched':':answer-field/correct' in of})
        review.extend([{'label':'Original evidence '+t,'record':r},{'label':'Changed evidence '+t,'record':check(g.generate(level,template=t,parameters={'m':2},profile='observed'))},{'label':'Normal authored bank '+t,'record':check(g.generate(level,template=t,parameters={'m':2}))}])
    for level in g.LEVELS:
        n=0;local=set()
        for t,pr,params in g.domains(level):
            if params.get('m')==1 or params.get('k')==1:print('domain',level,t,pr,params,flush=True)
            r=check(g.generate(level,seed=73,template=t,profile=pr,parameters=params))
            if pr=='method':
                normal.append(r);n+=1;local.add(r['generation']['mathematical_fingerprint'])
                again=g.generate(level,seed=101,template=t,profile=pr,parameters=params)
                assert r['question'][':question/id']==again['question'][':question/id']
        counts[level]={'normal_records':n,'distinct_mathematical_tasks':len(local)}
        defaults=g.batch(level,2,seed=41);review.extend({'label':'Generated '+level+' '+str(i+1),'record':r} for i,r in enumerate(defaults))
    # Strict type/boundary checks use the same public domains as seeded sampling.
    bad=[('easy','q-49557',{'m':True}),('easy','q-49557',{'m':1.0}),('easy','q-49557',{'m':13}),('moderate','shifted-sine',{'k':1,'a':1}),('moderate','shifted-sine',{'k':13,'a':2}),('hard','q-73674',{'m':0})]
    for level,t,params in bad:
        try:g.generate(level,template=t,parameters=params)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit parameters accepted')
    # Canonical task deduplication across observed/raw aliases, including the two
    # distinct definite source families yielding ln(4/3) but different integrands.
    for level in g.LEVELS:
        pool=list(g.domains(level));expect=len({g.generate(level,template=t,profile=pr,parameters=d)['generation']['mathematical_fingerprint'] for t,pr,d in pool})
        assert len(g.batch(level,expect,profile=None))==expect
        try:g.batch(level,expect+1)
        except ValueError:pass
        else:raise AssertionError('Finite task exhaustion not enforced')
    # Mutation regressions must fail the actual rendered checks.
    mutants=[]
    r=g.generate_hard(template='q-73674',parameters={'m':2});z=copy.deepcopy(r);z['question'][':question/worked-solution']=z['question'][':question/worked-solution'].replace(r'\frac{1}{2}\,\text{d}u',r'\frac{1}{3}\,\text{d}u');mutants.append(z)
    z=copy.deepcopy(r);z['question'][':question/worked-solution']=z['question'][':question/worked-solution'].replace(r'\frac{1}{u}\cdot \frac{1}{2}',r'\frac{1}{2u}');mutants.append(z)
    z=copy.deepcopy(r);z['question'][':question/problem']+='\x0c';mutants.append(z)
    z=copy.deepcopy(g.generate_hard(template='q-350887',parameters={'m':2}));z['question'][':question/worked-solution']=z['question'][':question/worked-solution'].replace(r'\operatorname{ln}⁡4-\operatorname{ln}⁡3',r'\operatorname{ln}⁡8-\operatorname{ln}⁡6');mutants.append(z)
    for z in mutants:
        try:check(z)
        except (AssertionError,ValueError):pass
        else:raise AssertionError('Mutation escaped independent checks')
    # Preserve protected live generator and every evidence/cache path byte-for-byte.
    baseline=json.loads((HERE/'registered-baseline.json').read_text());active=HERE.parent/'17592186068918'
    current={str(z) for z in [active.with_suffix('.py'),*active.rglob('*')] if z.is_file()}
    assert current=={str(Path(z['path']).resolve()) for z in baseline}
    for z in baseline:assert hashlib.sha256(Path(z['path']).read_bytes()).hexdigest()==z['sha256'],z['path']
    original=json.loads((HERE/'source.json').read_text());inventory=json.loads((HERE/'independent-inventory.json').read_text())
    assert {k:inventory[k] for k in ('database','basis','lineage')}=={k:original[k] for k in ('database','basis','lineage')}
    assert [z['record'] for z in inventory['questions']]==[z for z in original['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in z]
    # Actual curriculum order is a linked traversal rather than Pull-array order.
    activity=json.loads((HERE/'lesson.json').read_text())['record'][0];steps={z[':db/id']:z for z in activity[':activity/steps']};order=[];step=activity[':activity/first-step'][':db/id']
    while step is not None:
        node=steps[step];order.append(node[':step/content'][':db/id']);step=node.get(':step/next',{}).get(':db/id')
    assert steps[17592186069902][':step/content'][':tutorial/title']=='Integrating Products Containing Trigonometric Functions Using Substitution'
    assert order[-2:]==[17592186068917,17592186068918]
    subprocess.run([sys.executable,str(HERE/'native.py')],check=True)
    native=json.loads((HERE/'native-grading.json').read_text())
    save('source-cases.json',source_cases);save('source-replay.json',replay);save('review.json',review);save('previews.json',normal)
    (HERE/'review.md').write_text('\n\n'.join('## '+z['label']+'\n\n'+g.markdown(z['record']) for z in review))
    save('validation.json',{'passed':True,'basis':2275,'source_prompts':len(replay),'source_solutions':7,'source_omitted_solutions':2,'source_bank_values':sum(z['values'] for z in replay),'source_key_designations':7,'source_key_omissions':2,'counts':counts,'mutation_regressions':len(mutants),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'native':{k:native[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks','database_writes','entry_point']},'native_limitations':['foreign/malformed/mathtext radio input is unresolved rather than an owned ID judgment','normal endpoint-log-difference equivalents remain unresolved','original round wording rejects equivalent values and the q350904 legacy alias'], 'registered_baseline':{'passed':True,'unchanged_files':len(baseline)},'independent_inventory_records':len(inventory['questions']),'lesson_order':order,'hashes':{str(z):hashlib.sha256(z.read_bytes()).hexdigest() for z in [HERE.with_suffix('.py'),HERE/'printed.py',HERE/'math_format.py',HERE/'validate.py',HERE/'native.py',HERE/'check-engine',HERE/'check-engine.rs',HERE/'source.json']} })
    print(json.dumps(counts),flush=True)
if __name__=='__main__':main()
