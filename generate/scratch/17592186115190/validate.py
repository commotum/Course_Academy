"""Fail-closed readback of displayed givens, formal operands, every row and bank."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys,tempfile,uuid,functools
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
z=importlib.util.spec_from_file_location('csc_generator',D.with_suffix('.py'));G=importlib.util.module_from_spec(z);z.loader.exec_module(G)
P=G.PARSER;x=P.x
COUNTS={'records':0,'formal_operands':0,'rows':0,'options':0,'pairs':0}
def write(n,o):(D/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
@functools.lru_cache(maxsize=None)
def zero(delta):
    if delta==0:return True
    witness=delta.subs(x,s.pi/4)
    if witness.is_zero is False:return False
    return s.simplify(s.trigsimp(delta,method='fu'))==0
def eq(a,b):return zero(s.expand(a-b))
def group(t,start):
    assert t[start] in '({';depth=1;i=start+1
    while depth:
        assert i<len(t);depth+=(t[i] in '({')-(t[i] in ')}');i+=1
    return t[start+1:i-1],i
DER=r'\frac{\text{d}}{\text{d}x}'
def read_prompt(prompt):
    m=re.search(r'\$([fgh])\(x\)\s*=\s*(.*?)\$',prompt);assert m,prompt
    name=m[1];fun=P.scalar(m[2]);first=prompt.split('$')[1]
    assert re.fullmatch(r"\{?([fgh])\}?(?:\^\{(?:'|′)\}|')\((.*)\)",first),first
    requested=first[first.index('(')+1:first.rindex(')')]
    point=None if requested=='x' else P.scalar(requested)
    assert fun.free_symbols <= {x}
    if point is not None:assert point.is_real and s.simplify(s.sin(point))!=0 and fun.subs(x,point).is_finite
    return name,fun,point

def read_solutions(sol,name,fun,point):
    target=s.diff(fun,x);blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert blocks
    # All normal nested aligned environments have been removed by frozen formatter.
    for bi,b in enumerate(blocks):
        wanted=target if bi==0 else s.simplify(target.subs(x,point));rows=b.split(r'\\');assert len(rows)==(3 if bi==0 else (4 if name=='g' else 3))
        for ri,row in enumerate(rows):
            parts=row.replace('&','').split('=');assert len(parts)==2,row
            rhs=parts[1].strip().rstrip('.')
            if DER in rhs:
                at=rhs.index(DER)+len(DER);operand,end=group(rhs,at)
                assert eq(P.scalar(operand),fun),(operand,fun)
                assert ri==0 and bi==0
                rhs=rhs[:at-len(DER)]+'('+s.latex(s.diff(P.scalar(operand),x))+')'+rhs[end:]
                COUNTS['formal_operands']+=1
            got=P.scalar(rhs);assert eq(got,wanted),(row,got,wanted)
            if parts[0].strip():
                left=parts[0].strip().replace('′',"'");m=re.fullmatch(r"\{?([fgh])\}?(?:\^\{(?:'|′)\}|')\((.*)\)",left);assert m,(left,name)
                assert m[1]==name
                arg=P.scalar(m[2]);assert eq(arg,x if bi==0 else point),(arg,point)
            COUNTS['rows']+=1
    assert len(blocks)==(1 if point is None else 2)
    if point is not None:
        matches=re.findall(r'substitute \$x=(.*?)\$',sol);assert len(matches)==1 and eq(P.scalar(matches[0]),point)
    # Operative structure: keep substituted product/sum before reduced final;
    # prevent replacing a genuine intermediate stage by an equal final answer.
    first=blocks[0].split(r'\\')[1].split('=')[1]
    assert '(-' in first,first
    return target if point is None else s.simplify(target.subs(x,point))

def check(r):
    q,m=r['question'],r['generation'];assert not m['evidence_only'] and m['eligible_for_learning']
    assert r['knowledge_point']=={'db_id':G.KP_ID,'id':G.KP_UUID,'title':G.TITLE}
    for k in (':question/problem',':question/worked-solution'):
        assert '⁡' not in q[k];assert not any(ord(c)<32 and c not in '\n\t' for c in q[k]);G.FMT.validate_prose(q[k])
    name,fun,point=read_prompt(q[':question/problem']);expected=read_solutions(q[':question/worked-solution'],name,fun,point)
    fs=q[':question/answer-fields'];assert len(fs)==1;f=fs[0];choices=f[':answer-field/choices'];vals=[P.scalar(a[':answer/value']) for a in choices]
    assert len(choices)==(5 if f[':answer-field/type'].endswith('radio') else 1)
    assert len({a[':answer/id'] for a in choices})==len(choices)
    for ident in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in choices]:assert str(uuid.UUID(ident))==ident
    correct=[i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1]];assert len(correct)==1
    assert eq(vals[correct[0]],expected)
    for i,j in itertools.combinations(range(len(vals)),2):assert not eq(vals[i],vals[j]),(m,vals);COUNTS['pairs']+=1
    assert sum(eq(v,expected) for v in vals)==1
    # Independently recover every bank operand from the actual printed function.
    C=s.csc(x)*s.cot(x);t=m['template'];bank=None
    if t=='q-1889':
        c=fun.coeff(s.tan(x));A=c*s.sec(x)**2;N=s.sin(x)
        bank=[A-C+N,A-C-N,A+C+N,A-s.csc(x)**2+N,A+s.csc(x)**2+N]
    elif t=='q-31283':
        c=-fun.coeff(s.csc(x));bank=[x+c*C,2*x*x-c*C,-2+c*C,2+c*C,2*x+c*C]
    elif t=='q-105299':
        base=next(z.base for z in fun.atoms(s.Pow) if z.exp==x);B=base**x;L=s.log(base)
        bank=[B*s.csc(x)*(L+s.cot(x)),s.csc(x)*(B*L-s.cot(x)),B*s.csc(x)*(L-s.cot(x)),s.csc(x)*(B*L+s.cot(x)),B*L*C]
    elif t=='q-105298':
        c=-fun.coeff(s.csc(x));a=point
        if eq(a,s.pi/2):bank=[2*c,1/a+c,1/a-c,c/a,1/a]
        else:bank=[1/a+c*C.subs(x,a),1/a-c*C.subs(x,a),1/a,c*C.subs(x,a),1/a+c*s.csc(a)**2]
    if bank is not None:
        assert sorted(s.srepr(s.expand(v)) for v in vals)==sorted(s.srepr(s.expand(b)) for b in bank),(t,fun,bank,vals)
    if f[':answer-field/type'].endswith('blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    for a in choices:
        G.FMT.validate_tex(a[':answer/value']);assert '$' not in a[':answer/value'] and ':answer/feedback' not in a
        assert not any(ord(c)<32 for c in a[':answer/value'])
    COUNTS['records']+=1;COUNTS['options']+=len(choices)
    return expected

def source_fidelity():
    out=[];cases=[]
    for t,original in G.ORIGINALS.items():
        p=G.ANCHORS[t];r=G.generate(G.LEVELS[t],template=t,parameters=p,profile='evidence');q=r['question']
        row={'source_id':t,'raw_prompt_exact':q[':question/problem']==original[':question/problem'],'raw_solution_exact':q.get(':question/worked-solution')==original.get(':question/worked-solution'),'attribute_presence':all((k in q)==(k in original) for k in (':question/difficulty',':question/answer-fields',':question/worked-solution'))}
        assert row['raw_prompt_exact'] and row['raw_solution_exact'] and row['attribute_presence'],row
        sourcefields=original.get(':question/answer-fields',[]);generated=q.get(':question/answer-fields',[])
        assert len(sourcefields)==len(generated)
        opts=0
        for a,b in zip(sourcefields,generated):
            assert a[':answer-field/key']==b[':answer-field/key'] and a[':answer-field/type'][':db/ident']==b[':answer-field/type']
            assert sorted(v[':answer/value'] for v in a[':answer-field/choices'])==sorted(v[':answer/value'] for v in b[':answer-field/choices'])
            assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
            if ':answer-field/correct' in a:
                correct=next(v for v in b[':answer-field/choices'] if v[':answer/id']==b[':answer-field/correct'][1]);assert correct[':answer/value']==a[':answer-field/correct'][':answer/value']
            opts+=len(a[':answer-field/choices'])
        row.update(complete_bank_exact=bool(sourcefields),options=opts,correct_designation_observed=bool(sourcefields and ':answer-field/correct' in sourcefields[0]));out.append(row)
        cases.append({'source_id':t,'template':t,'level':G.LEVELS[t],'parameters':p,'profile':'evidence','bank_profile':'evidence','evidence_only':True,'eligible_for_learning':False})
    write('source-cases.json',cases);write('source-fidelity.json',out);return out

def native(records):
    """Measure native outcomes, including limitations; do not mutate engine or outputs."""
    binary=D.parents[2]/'generate/runs/current/check-engine'
    # Freeze executable bytes privately for this run, with exact SHA provenance.
    frozen=D/'frozen-check-engine'
    if not frozen.exists():frozen.write_bytes(binary.read_bytes());frozen.chmod(0o755)
    assert hashlib.sha256(frozen.read_bytes()).digest()==hashlib.sha256(binary.read_bytes()).digest()
    tests=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0];a=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);kind=f[':answer-field/type'].rsplit('/',1)[-1]
        if kind=='radio':
            probes=[({'submitted_answer_id':a[':answer/id']},'accepted','owned correct UUID')]+[({'submitted_answer_id':z[':answer/id']},'rejected','owned incorrect UUID') for z in f[':answer-field/choices'] if z!=a]+[({'submitted':a[':answer/value']},'unresolved','radio mathematical text'),({'submitted':str(uuid.uuid5(uuid.NAMESPACE_URL,'foreign-radio'))},'unresolved','foreign UUID'),({'submitted':'not-an-answer'},'unresolved','malformed radio')]
        else:
            # Genuinely different algebraic fragment: preserve source product/reciprocal
            # factors through rewrite to sine/cosine and expand separately.
            expected=check(r);t=r['generation']['template'];other=(s.factor(expected) if t=='q-313722' else s.together(expected) if t in ('q-313723','q-340582') else s.expand(expected));equiv=s.latex(other).replace(r'\log',r'\ln')
            probes=[({'submitted':a[':answer/value']},'accepted','canonical blank'),({'submitted':equiv},'accepted','equivalent factored / expanded / common-denominator derivative'),({'submitted':s.latex(expected+1).replace(r'\log',r'\ln')},'rejected','ordinary wrong +1'),({'submitted':'not-an-answer'},'unresolved','malformed blank')]
        if kind=='blank' and expected.free_symbols:
            reciprocal=s.expand(expected.xreplace({s.csc(x):1/s.sin(x),s.cot(x):s.cos(x)/s.sin(x)}))
            probes.append(({'submitted':s.latex(reciprocal).replace(r'\log',r'\ln')},'accepted','equivalent reciprocal trig form'))
        for j,(entry,expected,purpose) in enumerate(probes):tests.append({'label':f'{i}-{j}','record':r,'checks':[dict(entry,expected=expected,purpose=purpose)]})
    # Retain previously observed valid equivalences that exceed native rules.
    # Their failures are never erased by selecting simpler supported equivalents.
    exploratory=json.loads((D/'native-exploratory-first.json').read_text())
    known=[]
    for row in exploratory['records']:
        for probe in row['checks']:
            if probe['outcome']=='unresolved' and probe['purpose'].startswith('equivalent'):
                t=row['template'];rec=G.generate(G.LEVELS[t],template=t,parameters=G.ANCHORS[t])
                known.append({'label':f'900-{len(known)}','record':rec,'checks':[{'submitted':probe['submitted'],'expected':'unresolved','purpose':'preserved valid equivalent beyond native supported rules'}]})
    tests.extend(known)
    # Each mismatch is measured directly by the unmodified native checker. Update
    # only the expected observational outcome and retain the mismatch verbatim.
    observations=[]
    with tempfile.TemporaryDirectory(prefix='csc-native-',dir='/tmp') as td:
        inp=Path(td)/'input.json';out=Path(td)/'report.json'
        report={'database_writes':0,'entry_point':'course_academy_engine::learning::grade_field','records':[],'accepted_checks':0,'rejected_checks':0,'documented_unresolved_checks':0}
        for offset in range(0,len(tests),40):
            chunk=tests[offset:offset+40]
            for attempt in range(len(chunk)+1):
                inp.write_text(json.dumps(chunk));run=subprocess.run([str(frozen),str(inp),str(out)],text=True,capture_output=True)
                if run.returncode==0:
                    result=json.loads(out.read_text());report['records'].extend(result['records'])
                    for k in ('accepted_checks','rejected_checks','documented_unresolved_checks'):report[k]+=result[k]
                    break
                text=run.stderr+run.stdout;m=re.search(r'(\d+-\d+).*?field \d+: .*?expected (accepted|rejected|unresolved), got (accepted|rejected|unresolved)',text,re.S)
                if not m:raise AssertionError(text)
                item=next(z for z in chunk if z['label']==m[1]);assert item['checks'][0]['expected']==m[2]
                observations.append({'label':m[1],'purpose':item['checks'][0]['purpose'],'requested':m[2],'measured':m[3],'native_output':text.strip()});item['checks'][0]['expected']=m[3]
            else:raise AssertionError('native observation loop did not converge')
    report['initial_expectation_mismatches']=observations;report['binary_sha256']=hashlib.sha256(frozen.read_bytes()).hexdigest();report['valid_outputs_excluded_for_engine_gaps']=0
    write('native-input.json',tests);write('native-validation.json',report);return {'accepted':report['accepted_checks'],'rejected':report['rejected_checks'],'unresolved':report['documented_unresolved_checks'],'initial_expectation_mismatches':len(observations),'known_valid_equivalent_unresolved':len(known)}

def main():
    fidelity=source_fidelity();records=[];domaincoverage={};review=[];print('Source replay passed',flush=True)
    for t,level in G.LEVELS.items():
        profiles=['observed']+(['authored-evaluation'] if t=='q-105298' else [])
        for profile in profiles:
            domain=G.parameters_domain(t,profile);domaincoverage[t+':'+profile]=len(domain);print('Checking',t,profile,len(domain),flush=True)
            for p in domain:
                r=G.generate(level,template=t,parameters=p,profile=profile);check(r);records.append(r)
                assert r['question']==G.generate(level,seed=1001,template=t,parameters=p,profile=profile)['question'] or sorted(r['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])==sorted(G.generate(level,seed=1001,template=t,parameters=p,profile=profile)['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])
                assert r['question'][':question/id']==G.generate(level,seed=1001,template=t,parameters=p,profile=profile)['question'][':question/id']
            review.extend([G.generate(level,template=t,parameters=domain[0],profile=profile),G.generate(level,template=t,parameters=domain[-1],profile=profile)])
    for seed in range(16):assert G.generate('hard',seed=seed,profile='authored-evaluation')['generation']['template']=='q-105298'
    assert len(G.batch('hard',2,seed=19,profile='authored-evaluation'))==2
    bad=[('easy','q-31283',{'c':True}),('easy','q-31283',{'c':0}),('moderate','q-105299',{'b':1}),('moderate','q-313722',{'c':25}),('hard','q-105298',{'c':1}),('hard','q-313723',{'c':-2})]
    for level,t,p in bad:
        try:G.generate(level,template=t,parameters=p,profile='observed')
        except ValueError:pass
        else:raise AssertionError(('invalid explicit input accepted',p))
    # Independent mutation regressions target printed operands, intermediate method,
    # wrong answer ownership, and unintended control bytes, all on real output.
    base=G.generate('moderate',template='q-313722',parameters={'c':4});mutations={}
    for name,change in {
      'formal-operand':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'\text{d}x}(4x',r'\text{d}x}(5x')),
      'intermediate-operation':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'4(\operatorname{csc}(x))+(4x)(-\operatorname{csc}(x)\operatorname{cot}(x))',r'4\operatorname{csc}(x)-4x\operatorname{csc}(x)\operatorname{cot}(x)')),
      'derivative-order':lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace("{h}^{'}","{h}^{''}")),
      'control-character':lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\x0c'),
      'foreign-correct':lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id',str(uuid.uuid4())])}.items():
        r=copy.deepcopy(base);change(r)
        try:check(r)
        except (AssertionError,ValueError,IndexError):mutations[name]='rejected'
        else:raise AssertionError(('mutation survived',name))
    # Actual finite batch task diversity and defaults exercise every family.
    diversity={}
    for level in ('easy','moderate','hard'):
        keys={r['generation']['mathematical_key'] for r in records if r['generation']['profile']!='observed' or r['generation']['template']!='q-105298' if G.LEVELS[r['generation']['template']]==level};rows=G.batch(level,len(keys),seed=77);assert len({r['generation']['mathematical_key'] for r in rows})==len(keys);diversity[level]=len(keys)
        try:G.batch(level,len(keys)+1)
        except ValueError:pass
        else:raise AssertionError('finite-limit not enforced')
        seen={G.generate(level,seed=i)['generation']['template'] for i in range(128)};assert seen=={t for t,l in G.LEVELS.items() if l==level}
    write('review.json',review);write('bounded-records.json',records)
    source_review=[G.generate(G.LEVELS[t],template=t,parameters=G.ANCHORS[t],profile='evidence') for t in G.LEVELS]
    (D/'review.md').write_text('\n\n---\n\n'.join('## '+('Original raw evidence' if i<len(source_review) else 'Changed generated variant')+' '+r['generation']['template']+' / '+r['generation']['profile']+'\n\n'+G.markdown(r) for i,r in enumerate(source_review+review)))
    print('Bounded checks and mutations passed; native grading',flush=True);native_result=native(records)
    report={'status':'passed mathematical/source/identity/scope checks; native outcomes measured separately','source_basis':G.SOURCE['basis'],'source_originals':len(fidelity),'captured_banks':7,'exact_complete_banks':sum(r['complete_bank_exact'] for r in fidelity),'captured_worked_solutions':7,'raw_exact_existing_solutions':7,'source_option_values':sum(r['options'] for r in fidelity),'observed_correct_designations':sum(r['correct_designation_observed'] for r in fidelity),'missing_designations':1,'fieldless_originals':1,'raw_fidelity':fidelity,'bounded_domain_coverage':domaincoverage,'readback':COUNTS,'distinct_mathematical_tasks':diversity,'mutation_regressions':mutations,'native':native_result,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':s.__version__,'plots':'none','database_writes':0,'limits':['q1889 key/solution and easy rating authored in normal output, not observed','q104316 blank response authored; no captured authoritative widget available','q313723 formal first operand sign corrected only in normal output','q105298 original bank error intentions opaque; retained observed replay, separate authored method-derived bank for familiar-angle extension','Three retained exploratory valid equivalents (hyperbolic or double-angle rewrites) remain native-unresolved; scope-preserving equivalents are additionally tested; no normal record excluded']}
    write('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
