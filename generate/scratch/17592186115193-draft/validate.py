"""Independent readback, exact interval non-equivalence and frozen native grading."""
import sys
sys.dont_write_bytecode=True
import copy,functools,hashlib,importlib.util,itertools,json,re,stat,subprocess,tempfile,uuid
from pathlib import Path
import sympy as s
from mpmath import iv
iv.dps=50
D=Path(__file__).resolve().parent
z=importlib.util.spec_from_file_location('slope_draft',D.with_suffix('.py'));G=importlib.util.module_from_spec(z);z.loader.exec_module(G)
P=G.P;x=P.x
COUNTS=dict(records=0,formal_operands=0,equalities=0,bank_values=0,bank_pairs=0)
ROWS={'q-1886':(4,2),'q-1905':(2,4),'q-104437':(3,3),'q-340642':(3,3),'q-104442':(2,4),'q-1904':(3,3),'q-340630':(2,3),'q-340660':(5,3),'q-70874':(3,4),'canonical-quotient':(4,4)}
def write(n,v):(D/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def interval(e):
    if e==s.pi:return iv.pi
    if e==s.E:return iv.e
    if e.is_Integer:return iv.mpf(int(e))
    if e.is_Rational:return iv.mpf(int(e.p))/int(e.q)
    if e.is_Add:return sum((interval(a) for a in e.args),iv.mpf(0))
    if e.is_Mul:
        out=iv.mpf(1)
        for a in e.args:out*=interval(a)
        return out
    if e.is_Pow:return interval(e.base)**interval(e.exp)
    if e.func in (s.sin,s.cos,s.tan,s.exp,s.log):return {s.sin:iv.sin,s.cos:iv.cos,s.tan:iv.tan,s.exp:iv.exp,s.log:iv.ln}[e.func](interval(e.args[0]))
    if e.func in (s.sec,s.csc,s.cot):return 1/{s.sec:iv.cos,s.csc:iv.sin,s.cot:iv.tan}[e.func](interval(e.args[0]))
    raise AssertionError(('unsupported interval expression',e))
@functools.lru_cache(maxsize=None)
def zero(delta):
    if delta==0:return True
    if not delta.free_symbols:
        v=interval(delta)
        if bool(v.a>0) or bool(v.b<0):return False
    reduced=s.simplify(s.trigsimp(delta,method='fu'))
    return reduced==0

def eq(a,b):return zero(s.expand(a-b))
def scalar(t):return P.scalar(t.strip().rstrip('.').replace('[','(').replace(']',')'))
def group(t,start):
    assert t[start] in '({';depth=1;i=start+1
    while depth:
        assert i<len(t);depth+=(t[i] in '({')-(t[i] in ')}');i+=1
    return t[start+1:i-1],i
DERS=(r'\frac{\text{d}}{\text{d}x}',r'\frac{d}{dx}')
LABEL=re.compile(r"\{?([fgh])\}?(?:\^\{['′]\}|')\((.*?)\)")
def value(t,fun,name,at,formal):
    t=t.strip().rstrip('.')
    for der in DERS:
        while der in t:
            i=t.index(der);arg,end=group(t,i+len(der));operand=scalar(arg);formal.append(operand)
            t=t[:i]+'('+s.latex(s.diff(operand,x))+')'+t[end:]
    derivative=s.diff(fun,x)
    dy=r'\frac{\text{d}y}{\text{d}x}'
    if dy in t:
        # Source dy/dx|_{pi/3} notation owns its actual evaluation argument.
        m=re.search(re.escape(dy)+r'\{\|\}_\{(.*?)\}',t)
        if m:
            point=scalar(m[1]);assert eq(point,at);t=t[:m.start()]+'('+s.latex(derivative.subs(x,point))+')'+t[m.end():]
        t=t.replace(dy,'('+s.latex(derivative)+')')
    def label(m):
        assert m[1]==name,(m[0],name)
        p=scalar(m[2]);return '('+s.latex(derivative.subs(x,p))+')'
    t=LABEL.sub(label,t)
    assert '′' not in t and "'" not in t,('wrong/unparsed derivative order',t)
    if t.strip()=='m':return s.simplify(derivative.subs(x,at))
    return scalar(t)

def structure(t,blocks):
    rows=[b.split(r'\\') for b in blocks];rhs=lambda bi,ri:rows[bi][ri].split('=')[-1]
    if t=='q-1886':assert '{x}^{-1}' in rhs(0,1) and '(-' in rhs(0,2)
    if t=='q-1905':assert re.search(r'=\s*\d+-2',rows[1][2])
    if t=='q-104437':assert '(-' in rhs(0,1) and '+' in rhs(0,1)
    if t=='q-340642':assert ')(-' in rhs(0,1) and ')(' in rhs(0,1) and '+' in rhs(0,1) and '+' in rhs(0,2) and '{0}^{2}+{1}^{2}' in rhs(1,1)
    if t=='q-104442':assert '+' in rhs(1,2)
    if t=='q-1904':assert r'2\cdot (-x)' in rhs(0,1) and '(-' in rhs(0,1)
    if t=='q-340630':assert r'\cdot (-1)\cdot 0' in rhs(1,1)
    if t=='q-340660':
        assert sum(rhs(0,1).count(d) for d in DERS)==2
        assert re.search(r'\\sec\s*x\(1-x\\tan',rhs(0,3)),rhs(0,3)
        assert re.search(r'\}\{\\sec\s*x\}',rhs(0,4)),rhs(0,4)
        assert not any(d in rhs(0,2) for d in DERS)
    if t=='q-70874':assert r'(\frac{2}{3})' in rhs(1,2)
    if t=='canonical-quotient':
        assert sum(rhs(0,1).count(d) for d in DERS)==2
        assert r'\csc^2 x' in rhs(0,2) and r'\cdot \sin x' in rhs(0,2)
        assert r'\csc x' in rhs(0,3) and r'\cot x\cos x' in rhs(0,3) and r'\csc^2 x' not in rhs(0,3)
        assert r'\frac{' in rhs(1,2)

def expected_bank(t,pr,fun,at):
    C=s.csc(at)*s.cot(at);S=s.sec(at)*s.tan(at)
    if t=='q-1886':
        a=fun.coeff(s.cos(x));return [-s.sin(at)-C-1/at**2,-a*s.sin(at)-S-1/at**2,-a*s.sin(at)+S+1/at**2,a*s.sin(at)-S-1/at**2,-a*s.sin(at)-C-1]
    if t=='q-1905':
        a=fun.coeff(x)
        return [a-2,a+2,a-s.sqrt(2),a-2*s.sqrt(2),a*s.pi/4-2] if pr=='authored-bank' else [a+2,a-6*s.sqrt(2),a+3*s.sqrt(2),a-2,a-3*s.sqrt(2)]
    if t=='q-104442':
        a=s.expand(fun).coeff(x,2)*s.pi;u=s.sec(at)*s.tan(at)/s.sqrt(3);v=2*a*at/s.pi
        return [u-v,-u-v,u,u+v,-v]
    if t=='q-1904':
        a=fun.coeff(s.csc(x));return [-2*at-a*s.sqrt(3),2*at-2*a*s.sqrt(3),-at-2*a*s.sqrt(3),2*at+2*a*s.sqrt(3),-2*at-2*a*s.sqrt(3)]
    if t=='q-70874':
        a=fun.coeff(s.csc(x));return [a*C-1/at,1/at-a*C,s.pi-a*C,1/at,1/at+a*C]
    return [s.simplify(s.diff(fun,x).subs(x,at))]

def printed_given(prompt):
    definition=re.search(r'\$([fgh])\(x\)\s*=\s*(.*?)\$',prompt)
    point=re.search(r'\$x\s*=\s*(.*?)\$',prompt)
    assert definition and point,prompt
    assert re.search(r'\$y='+definition[1]+r'\(x\)\$',prompt),prompt
    return definition[1],scalar(definition[2]),scalar(point[1])

def check(r):
    q,m=r['question'],r['generation'];t=m['template'];assert not m['raw_evidence']
    assert r['knowledge_point']=={'db_id':G.KP_ID,'id':G.KP_UUID,'title':G.TITLE}
    for k in (':question/problem',':question/worked-solution'):
        assert '⁡' not in q[k] and not any(ord(c)<32 and c not in '\n\t' for c in q[k]);G.F.validate_prose(q[k])
    name,fun,at=printed_given(q[':question/problem']);assert at.is_real and fun.subs(x,at).is_finite
    if t in ('q-1886','q-1905','q-104442','q-340630','q-340660'):assert not eq(s.cos(at),0) and 'cos(x) != 0' in m['domain']
    else:assert not eq(s.sin(at),0) and 'sin(x) != 0' in m['domain']
    if t=='q-70874':assert at>0 and 'x > 0' in m['domain']
    a=m['parameters']['a'];role={'q-1886':fun.coeff(s.cos(x)),'q-1905':fun.coeff(x),'q-104437':fun/(x*s.cot(x)),'q-340642':fun/(s.csc(x)*s.cot(x)),'q-104442':s.expand(fun).coeff(x,2)*s.pi,'q-1904':fun.coeff(s.csc(x)),'q-340630':fun.coeff(s.exp(x)),'q-340660':fun*s.sec(x)/x,'q-70874':fun.coeff(s.csc(x)),'canonical-quotient':-fun*s.sin(x)/s.cot(x)}[t];assert eq(role,a)
    if t=='canonical-quotient':assert eq(at,s.sympify(m['parameters']['angle']))
    der=s.diff(fun,x);answer=s.simplify(der.subs(x,at));formal=[]
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S);assert len(blocks)==2
    assert tuple(len(b.split(r'\\')) for b in blocks)==ROWS[t]
    structure(t,blocks)
    for bi,block in enumerate(blocks):
        expected=der if bi==0 else answer
        for row in block.split(r'\\'):
            parts=row.replace('&','').split('=');assert len(parts)>=2
            for side in parts:
                if side.strip():assert eq(value(side,fun,name,at,formal),expected),(t,row,side,expected)
            COUNTS['equalities']+=len(parts)-1
    expected_formal=[fun,fun] if t=='q-1886' else [fun,*s.fraction(fun)] if t in ('q-340660','canonical-quotient') else [fun]
    assert len(formal)==len(expected_formal) and all(eq(a,b) for a,b in zip(formal,expected_formal)),(t,formal,expected_formal)
    COUNTS['formal_operands']+=len(formal)
    # Read prose's actual substitution separately, and reject stale times/angles.
    points=re.findall(r'substitute \$x=(.*?)\$',q[':question/worked-solution']);assert len(points)==1 and eq(scalar(points[0]),at)
    fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];choices=f[':answer-field/choices'];vals=[scalar(a[':answer/value']) for a in choices]
    assert len(choices)==(5 if G.KINDS[t]=='radio' else 1);assert all(not v.free_symbols for v in vals)
    assert len({a[':answer/id'] for a in choices})==len(choices)
    for ident in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in choices]:assert str(uuid.UUID(ident))==ident
    selected=[v for v,a in zip(vals,choices) if a[':answer/id']==f[':answer-field/correct'][1]];assert len(selected)==1 and eq(selected[0],answer)
    for v,w in itertools.combinations(vals,2):assert not eq(v,w),(t,m['parameters'],vals);COUNTS['bank_pairs']+=1
    bank=expected_bank(t,m['profile'],fun,at);assert len(vals)==len(bank) and all(any(eq(v,b) for v in vals) for b in bank)
    if G.KINDS[t]=='blank':
        placeholder='{{'+f[':answer-field/key']+'}}';assert placeholder in q[':question/problem']
        context=q[':question/problem'].split('\n\n',1)[1];assert context.startswith('$m=$\n'),context
        completed=context.replace(placeholder,'$'+choices[0][':answer/value']+'$');assert eq(scalar(completed.split('$')[-2]),answer)
    for a in choices:
        assert ':answer/feedback' not in a and a[':answer/type']==':answer.type/math';G.F.validate_tex(a[':answer/value']);assert not any(ord(c)<32 for c in a[':answer/value'])
    assert r['generation']['evidence_only']==(t=='q-1905' and m['profile']=='observed')
    COUNTS['records']+=1;COUNTS['bank_values']+=len(vals);return answer

def baseline():
    b=json.loads((D/'registered-baseline.json').read_text());old=D.with_name('17592186115193');current=[old.with_suffix('.py')]+list(old.rglob('*'))
    assert {str(p.resolve()) for p in current}=={str(Path(v['path']).resolve()) for v in b['files']}
    for item in b['files']:
        p=Path(item['path']);assert stat.S_IMODE(p.stat().st_mode)==item['mode']
        if item['kind']=='file':assert p.stat().st_size==item['size'] and hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],p
    return len(current)
def fidelity():
    out=[];cases=[]
    for t,original in G.ORIGINALS.items():
        r=G.generate(G.LEVELS[t],template=t,parameters=G.ANCHORS[t],profile='evidence');q=r['question']
        for k in (':question/problem',':question/worked-solution'):assert q.get(k)==original.get(k),(t,k)
        assert all((k in q)==(k in original) for k in (':question/difficulty',':question/worked-solution',':question/answer-fields'))
        sf=original.get(':question/answer-fields',[]);gf=q.get(':question/answer-fields',[]);assert len(sf)==len(gf);values=0
        for a,b in zip(sf,gf):
            assert a[':answer-field/key']==b[':answer-field/key'] and a[':answer-field/type'][':db/ident']==b[':answer-field/type']
            assert sorted(z[':answer/value'] for z in a[':answer-field/choices'])==sorted(z[':answer/value'] for z in b[':answer-field/choices'])
            selected=next(z for z in b[':answer-field/choices'] if z[':answer/id']==b[':answer-field/correct'][1]);assert selected[':answer/value']==a[':answer-field/correct'][':answer/value'];values+=len(a[':answer-field/choices'])
        out.append({'source_id':t,'raw_prompt_exact':True,'raw_solution_exact':True,'attribute_presence_exact':True,'complete_bank_exact':bool(sf),'option_values':values,'observed_correct_designations':len(sf)})
        cases.append({'source_id':t,'difficulty':G.LEVELS[t],'level':G.LEVELS[t],'template':t,'parameters':G.ANCHORS[t],'bank_profile':'evidence','profile':'evidence','evidence_only':True,'eligible_for_learning':False})
    inventory=json.loads((D/'independent-inventory.json').read_text());expected=[q for q in G.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q];assert [r['record'] for r in inventory['questions']]==expected and all(r['role']=='independently authored inventory' for r in inventory['questions'])
    write('source-cases.json',cases);write('source-fidelity.json',out);return out

def native(records):
    frozen=D/'frozen-check-engine';shared=D.parents[2]/'generate/runs/current/check-engine'
    if not frozen.exists():frozen.write_bytes(shared.read_bytes());frozen.chmod(0o755)
    sha=hashlib.sha256(frozen.read_bytes()).hexdigest();assert sha=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
    fixtures=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0];chosen=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);radio=f[':answer-field/type'].endswith('radio')
        if radio:probes=[({'submitted_answer_id':a[':answer/id']},'accepted' if a==chosen else 'rejected','owned correct ID' if a==chosen else 'owned wrong ID') for a in f[':answer-field/choices']]+[({'submitted':chosen[':answer/value']},'unresolved','radio mathematical text'),({'submitted':str(uuid.uuid5(uuid.NAMESPACE_URL,'foreign-slope-answer'))},'unresolved','foreign UUID'),({'submitted':'not-an-answer'},'unresolved','malformed radio')]
        else:
            answer=scalar(chosen[':answer/value']);other=s.together(answer);equiv=tex(other)
            if equiv==chosen[':answer/value'] or answer.is_Integer or r['generation']['template'] in ('q-340630','canonical-quotient'):
                numerator,denominator=s.fraction(s.together(answer));equiv=r'\frac{'+tex(3*numerator)+'}{'+tex(3*denominator)+'}'
            assert eq(scalar(equiv),answer) and equiv!=chosen[':answer/value'],(r['generation'],equiv,chosen)
            probes=[({'submitted':chosen[':answer/value']},'accepted','canonical blank'),({'submitted':equiv},'accepted','unreduced common-denominator equivalent'),({'submitted':tex(answer+1)},'rejected','ordinary wrong +1'),({'submitted':'not-an-answer'},'unresolved','malformed blank')]
        for j,(entry,expected,purpose) in enumerate(probes):fixtures.append({'label':f'{i}-{j}','record':r,'checks':[dict(entry,expected=expected,purpose=purpose)]})
    report={'database_writes':0,'entry_point':'course_academy_engine::learning::grade_field','records':[],'accepted_checks':0,'rejected_checks':0,'documented_unresolved_checks':0};mismatches=[]
    with tempfile.TemporaryDirectory(prefix='slope-draft-native-',dir='/tmp') as td:
        inp=Path(td)/'input.json';out=Path(td)/'output.json'
        for off in range(0,len(fixtures),40):
            chunk=fixtures[off:off+40]
            for _ in range(len(chunk)+1):
                inp.write_text(json.dumps(chunk));run=subprocess.run([str(frozen),str(inp),str(out)],capture_output=True,text=True)
                if run.returncode==0:
                    part=json.loads(out.read_text());report['records'].extend(part['records'])
                    for k in ('accepted_checks','rejected_checks','documented_unresolved_checks'):report[k]+=part[k]
                    break
                text=run.stderr+run.stdout;m=re.search(r'(\d+-\d+).*?field \d+: .*?expected (accepted|rejected|unresolved), got (accepted|rejected|unresolved)',text,re.S);assert m,text
                item=next(v for v in chunk if v['label']==m[1]);probe=item['checks'][0]
                assert probe['purpose'] not in ('canonical blank','ordinary wrong +1','owned correct ID','owned wrong ID'),text
                mismatches.append({'label':m[1],'purpose':probe['purpose'],'requested':m[2],'measured':m[3],'native_output':text});probe['expected']=m[3]
            else:raise AssertionError('native probes failed to converge')
    report.update(binary_sha256=sha,initial_expectation_mismatches=mismatches,valid_outputs_excluded=0)
    write('native-input.json',fixtures);write('native-validation.json',report);return {k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')}|{'valid_equivalent_limitations':len(mismatches)}
def tex(e):return s.latex(e).replace(r'\log',r'\ln')

def main():
    baseline_paths=baseline();sources=fidelity();print('Baseline and 9 original replays passed',flush=True);records=[];review=[];coverage={}
    for t,l in G.LEVELS.items():
        prs=[p for p in G.profiles(t) if p!='evidence']
        for pr in prs:
            domain=G.parameters_domain(t,pr);coverage[t+':'+pr]=len(domain);print('Checking',t,pr,len(domain),flush=True)
            for p in domain:
                r=G.generate(l,template=t,profile=pr,parameters=p);check(r);records.append(r)
            for p in (domain[0],domain[-1]):
                r=G.generate(l,template=t,profile=pr,parameters=p);other=G.generate(l,seed=1001,template=t,profile=pr,parameters=p);assert r['question'][':question/id']==other['question'][':question/id'];assert sorted(r['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])==sorted(other['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id']);review.append(r)
    bad=[('easy','q-1905',{'a':True}),('easy','q-1904',{'a':0}),('moderate','q-1886',{'a':1}),('moderate','q-340660',{'a':25}),('hard','canonical-quotient',{'a':0,'angle':'pi/4'}),('hard','canonical-quotient',{'a':2,'angle':'pi/2'})]
    for l,t,p in bad:
        try:G.generate(l,template=t,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('invalid explicit parameters accepted',t,p))
    base=G.generate('moderate',template='q-340660',parameters={'a':4});mutations={}
    def replace_row(r,index,with_index):
        sol=r['question'][':question/worked-solution'];m=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);rows=m[1].split(r'\\');rows[index]=rows[with_index];r['question'][':question/worked-solution']=sol[:m.start(1)]+r'\\'.join(rows)+sol[m.end(1):]
    for name,change in {
      'stale-given-coefficient':lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace(r'\frac{4x}',r'\frac{5x}')),
      'inner-formal-operand':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'\text{d}x}(4x)',r'\text{d}x}(5x)')),
      'factoring-operation-removed':lambda r:replace_row(r,3,2),
      'derivative-order':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('{f}^{′}','{f}^{′′}')),
      'control-character':lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\x0c'),
      'foreign-key':lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id',str(uuid.uuid4())])}.items():
        r=copy.deepcopy(base);change(r)
        try:check(r)
        except (AssertionError,ValueError,IndexError):mutations[name]='rejected'
        else:raise AssertionError(('mutation survived',name))
    diversity={}
    for level in ('easy','moderate','hard'):
        selected=[r for r in records if G.LEVELS[r['generation']['template']]==level and r['generation']['profile']==G.default_profile(r['generation']['template'])];keys={r['generation']['mathematical_key'] for r in selected};rows=G.batch(level,len(keys),seed=71);assert len({r['generation']['mathematical_key'] for r in rows})==len(keys);diversity[level]=len(keys)
        try:G.batch(level,len(keys)+1)
        except ValueError:pass
        else:raise AssertionError('finite-domain overflow accepted')
        assert {G.generate(level,seed=i)['generation']['template'] for i in range(96)}=={t for t,l in G.LEVELS.items() if l==level}
    originals=[G.generate(G.LEVELS[t],template=t,parameters=G.ANCHORS[t],profile='evidence') for t in G.ORIGINALS]
    (D/'review.md').write_text('\n\n---\n\n'.join('## '+('Original raw evidence' if i<len(originals) else 'Generated variant')+' '+r['generation']['template']+' / '+r['generation']['profile']+'\n\n'+G.markdown(r) for i,r in enumerate(originals+review)))
    write('review.json',review);write('bounded-records.json',records);print('Bounded mathematics, banks, identities and mutations passed; native grading',flush=True);native_result=native(records);assert baseline()==baseline_paths
    report={'status':'mathematics/source/identity/domain/format/baseline passed; native outcomes separately reported','source_basis':2275,'originals':len(sources),'exact_captured_banks':sum(q['complete_bank_exact'] for q in sources),'exact_option_values':sum(q['option_values'] for q in sources),'observed_correct_designations':sum(q['observed_correct_designations'] for q in sources),'fieldless_originals':1,'independent_inventory_records':2,'bounded_domain':coverage,'distinct_default_tasks':diversity,'readback':COUNTS,'mutation_regressions':mutations,'native':native_result,'immutable_registered_paths':baseline_paths,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':s.__version__,'plots':'none','database_writes':0,'limits':['q104437 fieldless raw evidence preserved; normal scalar blank authored from original solution and sibling response contract','q1905 historical wrong-value intentions opaque; full bank retained as ineligible observed/evidence replay; separate method-derived default bank','Hard level authored from canonical e3648; not an observed source difficulty label']}
    write('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
