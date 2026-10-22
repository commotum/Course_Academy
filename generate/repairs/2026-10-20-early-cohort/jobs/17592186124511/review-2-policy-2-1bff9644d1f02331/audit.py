"""Read-only independent generator review. Run with the job's Python executable."""
import collections, copy, hashlib, importlib.util, json, os, pathlib, re, shutil, subprocess, sys
sys.dont_write_bytecode = True
E = pathlib.Path(__file__).resolve().parent
B = E.parent
P = B/'workspace'
REPO = pathlib.Path('/home/jake/Developer/Course_Academy')
def save(name, obj):
    (E/name).write_text(json.dumps(obj, indent=2, default=str)+'\n')
def hashes(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def load_generator(root=P):
    sys.path.insert(0,str(root))
    spec=importlib.util.spec_from_file_location('reviewed',root/'17592186124511.py')
    g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    return g
import sympy as sp
MAT = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def norm(s):
    for a,b in [(r'\operatorname',''),(r'\textrm',''),(r'\text',''),(r'\mathbb',''),(r'\ne','!='),(r'\neq','!='),('**','')]: s=s.replace(a,b)
    return re.sub(r'[\s${}\\]','',s)
def correct(f):
    ref=f[':answer-field/correct']
    if isinstance(ref,dict):return ref[':answer/value']
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==ref[1])
def visible(record):
    """Infer all possible ranks from visible givens; evaluate displayed claims at every rank."""
    q=record['question'];prompt=q[':question/problem']
    n=int(re.search(r'(\d+)\s*\\(?:times|cdot)\s*(\d+)',prompt)[1])
    numbered=re.findall(r'(?:^|\n)(?:III|II|I|[123])\. ([^\n]+)',prompt)
    head=re.split(r'\n(?:I|1)\.',prompt)[0]
    matrices=MAT.findall(head)
    if matrices:
        expr=[sp.sympify(re.sub(r'(\d)(x)',r'\1*\2',re.sub(r'\{x\}_\{([12])\}',r'x\1',r.strip()))) for r in matrices[0].split(r'\\')]
        assert len(expr)==n
        xs=sorted(set().union(*(v.free_symbols for v in expr)),key=str)
        if xs:
            basis=sp.Matrix([[v.coeff(x) for x in xs] for v in expr])
            assert all(v==sum(basis[i,j]*x for j,x in enumerate(xs)) for i,v in enumerate(expr))
            ranks=[n-basis.rank()];kind='nullspace'
        else:
            assert any(expr);ranks=list(range(n));kind='nonzero-vector'
    elif (d:=re.search(r'det\(A\)=(-?\d+)',head)):
        ranks=[n] if int(d[1]) else list(range(n));kind='det-nonzero' if int(d[1]) else 'det-zero'
    elif 'rank' in head:ranks=[n];kind='full-rank'
    elif 'Col' in head:ranks=[n];kind='full-column-space'
    else:raise AssertionError(('unknown given',head))
    fs=q[':question/answer-fields'];radio=fs[0][':answer-field/type'].endswith('/radio') if isinstance(fs[0][':answer-field/type'],str) else fs[0][':answer-field/type'][':db/ident'].endswith('/radio')
    claims=numbered if radio else [f[':answer-field/key'] for f in fs if f[':answer-field/key']!='None of the above']
    assert len(claims)==3
    def evaluate(text,r):
        s=norm(text);k=n-r
        if s=='Aisinvertible':return r==n
        if s=='Aisnotinvertible':return r<n
        if 'pivotcolumns' in s:
            v=int(re.search(r'(\d+)pivotcolumns',s)[1]);return r!=v if 'doesnothave' in s else r==v
        if (m:=re.fullmatch(r'(Null|Col)\(A\)(=|!=)(.*)',s)):
            obj,op,rhs=m.groups()
            if rhs=='0':eq=k==0 if obj=='Null' else r==0
            else:assert obj=='Col' and rhs=='R^'+str(n),s;eq=r==n
            return eq if op=='=' else not eq
        m=re.fullmatch(r'(rank|dim\(Null|dim\(Col|nullity)\(A\)\)?(=|!=|<)(\d+)',s)
        assert m,s
        obj,op,value=m.groups();actual=r if obj in ('rank','dim(Col') else k;v=int(value)
        return {'=':actual==v,'!=':actual!=v,'<':actual<v}[op]
    mask=[]
    for c in claims:
        values={evaluate(c,r) for r in ranks};assert len(values)==1,('underdetermined claim',c,ranks)
        mask.append(values.pop())
    if radio:
        target=' and '.join(label for label,b in zip(('I','II','III'),mask) if b)+' only'
        assert correct(fs[0])==target,(correct(fs[0]),target)
    else:
        expected=dict(zip(claims,mask))
        for f in fs:
            truth=not any(mask) if f[':answer-field/key']=='None of the above' else expected[f[':answer-field/key']]
            assert correct(f)==str(truth).lower()
    sol=q.get(':question/worked-solution','')
    if not record.get('generation',{}).get('replay'):
        for c,b in zip(claims,mask):
            # Radio labels and shuffled checkbox fields have different presentation.
            assert ('$'+c.strip('$')+'$') in sol
            match=(re.search(r'Statement '+('III' if claims.index(c)==2 else 'II' if claims.index(c)==1 else 'I')+r' is (true|false)',sol) if radio else re.search(r'Statement \$'+re.escape(c.strip('$'))+r'\$ is (true|false)',sol))
            assert match and match[1]==str(b).lower(),(c,b)
    return {'kind':kind,'n':n,'mask':''.join(str(int(x)) for x in mask),'radio':radio,'response':str(next(i for i,a in enumerate(fs[0][':answer-field/choices']) if a[':answer/id']==fs[0][':answer-field/correct'][1])) if radio else ''.join('1' if correct(f)=='true' else '0' for f in fs)}
def native(record,label):
    visible(record)
    return {'label':label,'record':record,'checks':[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==correct(f) else 'rejected','purpose':'visible theorem independently determines this choice'} for i,f in enumerate(record['question'][':question/answer-fields']) for a in f[':answer-field/choices']]}
def summary(records):
    groups=collections.defaultdict(list)
    for r in records:
        v=visible(r);t=r['generation']['template'];groups[t].append(v)
        groups[t+'/'+v['kind']].append(v)
    return {t:{'count':len(rows),'masks':dict(collections.Counter(x['mask'] for x in rows)),'responses':dict(collections.Counter(x['response'] for x in rows)),'dimensions':sorted({x['n'] for x in rows})} for t,rows in groups.items()}
def main():
    save('package-before.json',hashes(P));g=load_generator()
    original=json.load(open(B/'source/source.json'))
    supplied={q[':question/math-academy-id']:q for q in original['material']['kp'][':knowledge-point/questions']}
    replay=[];replay_result=[]
    for t,src in supplied.items():
        try:r=g.generate(template=t,replay=True)
        except Exception as ex:
            replay_result.append({'source':t,'id':src[':question/id'],'status':'excluded','error':str(ex),'captured_solution':bool(src.get(':question/worked-solution')),'captured_correct':all(':answer-field/correct' in f for f in src[':question/answer-fields'])});continue
        visible(r);q=r['question'];assert q[':question/problem']==src[':question/problem'] and q[':question/worked-solution']==src[':question/worked-solution']
        for a,b in zip(q[':question/answer-fields'],src[':question/answer-fields']):
            assert a[':answer-field/key']==b[':answer-field/key']
            assert [c[':answer/value'] for c in a[':answer-field/choices']]==['II only' if t=='q-142367' and c[':answer/value']=='lI only' else c[':answer/value'] for c in b[':answer-field/choices']]
            assert correct(a)==correct(b)
        replay.append(r);replay_result.append({'source':t,'status':'passed','complete_fields':len(q[':question/answer-fields'])})
    save('source-replay-records.json',replay);save('source-replay-results.json',replay_result)
    # Fixed fresh seeds, selected independently of author results.
    records=[g.generate(template=t,seed=seed) for t in g.TEMPLATES for seed in range(613401,613441 if t=='q-142367' else 613413)]
    batch=json.load(open(B/'samples.json'))
    public=[g.batch('moderate',5,s) for s in (91631,91632,91633)]
    save('samples.json',records);save('runner-batch.json',batch);save('public-batches.json',public)
    stats=summary(records);batchstats=summary(batch)
    for pub in public:summary(pub)
    assert g.batch('moderate',5,91631)==public[0]
    # Controlled changes: evidence relevant to invertibility; irrelevant sign/magnitude.
    p={'n':4,'det':1,'claims':[r'A\text{ is invertible}',r'\text{Null}(A)=\{0\}',r'\text{dim(Null}(A))\ne 0']}
    a=g.generate(template='q-141200',parameters=p,seed=901)
    p['det']=0;b=g.generate(template='q-141200',parameters=p,seed=901)
    p['det']=-3;c=g.generate(template='q-141200',parameters=p,seed=901)
    p['claims'][0]=r'A\text{ is not invertible}';d=g.generate(template='q-141200',parameters=p,seed=901)
    # Hold target statements fixed while ambient dimension changes in a rank/col profile.
    e=g.generate(template='q-141201',seed=902);pp=copy.deepcopy(e['generation']['parameters'])
    # Sign reversal of a nonzero homogeneous witness is irrelevant.
    f=g.generate(template='q-34929',seed=903);pp=copy.deepcopy(f['generation']['parameters']);pp['matrix']=[[-x for x in row] for row in pp['matrix']]
    h=g.generate(template='q-34929',parameters=pp,seed=903)
    counter=[a,b,c,d,f,h];m=[visible(r)['mask'] for r in counter]
    assert all(x!=y for x,y in zip(m[0],m[1])) and m[0]==m[2] and sum(x!=y for x,y in zip(m[2],m[3]))==1 and m[4]==m[5],m
    save('counterfactual-records.json',counter)
    save('counterfactual-results.json',{'masks':m,'pairs':[{'indices':[0,1],'change':'det 1 to 0','expected':'all three truth values reverse'},{'indices':[0,2],'change':'det 1 to -3','expected':'all truths preserved'},{'indices':[2,3],'change':'invertible to not invertible claim','expected':'only first claim reverses'},{'indices':[4,5],'change':'v to -v','expected':'all truths preserved'}]})
    # Invalid inputs must be refused, not silently repaired.
    invalid=[]
    for label,t,par in [('zero vector','q-141199',{'n':4,'matrix':[[0],[0],[0],[0]],'claims':[]}),('dependent nullspace','q-142358',{'n':5,'matrix':[[1,1]]*5,'claims':[]}),('out-of-range determinant','q-141200',{'n':4,'det':5,'claims':a['generation']['parameters']['claims']}),('out-of-range dimension','q-141200',{'n':2,'det':1,'claims':a['generation']['parameters']['claims']})]:
        try:g.generate(template=t,parameters=par)
        except Exception as ex:invalid.append({'case':label,'rejected':True,'exception':type(ex).__name__,'message':str(ex)})
        else:invalid.append({'case':label,'rejected':False})
    assert all(x['rejected'] for x in invalid)
    for level in ('easy','hard'):
        try:g.batch(level,5,1)
        except ValueError:invalid.append({'case':level,'rejected':True})
        else:raise AssertionError(level)
    save('boundary-results.json',invalid)
    save('math-results.json',{'independent_oracle':'audit.py visible(): infer possible ranks from rendered prompt, evaluate claims at every possible rank, compare stored key and solution judgments','sample_count':len(records),'runner_batch_count':len(batch),'public_batch_count':len(public),'results':'all checked records passed','coverage':stats,'runner_batch_coverage':batchstats})
    save('native-input.json',[native(r,'sample-'+str(i)) for i,r in enumerate(records+batch+counter+replay)])
    save('render-records.json',batch+counter+[replay[0]])
    # The exact submitted batch admits a repeated positional cue in its 3-option checkbox subgroup.
    sub=[r for r in batch if len(r['question'][':question/answer-fields'])==3 and not visible(r)['radio']]
    save('batch-shortcut.json',{'command':'python audit.py','scope':'runner batch, three-field checkbox subgroup','strategy':'leave first two unchecked; check only third','correct':sum(visible(r)['response']=='001' for r in sub),'total':len(sub),'baseline':1/7,'baseline_explanation':'uniform among seven nonempty subsets of three ordinary options','records':sub,'control':{'correct':sum(visible(r)['response']=='001' for r in records if not visible(r)['radio'] and len(r['question'][':question/answer-fields'])==3),'total':sum(not visible(r)['radio'] and len(r['question'][':question/answer-fields'])==3 for r in records)}})
    inv=json.load(open(B/'source/inventory.json'));generated=[q for q in inv['questions'] if q.get(':question/generation') or not q.get(':question/math-academy-id')]
    save('inventory-assessment.json',{'basis':inv['basis'],'questions':len(inv['questions']),'generated_count':len(generated),'source_count':len(inv['questions'])-len(generated),'status':'verified absence of generated instances in captured inventory' if not generated else 'requires reproduction','publication_preparation_exists':(B/'publication/preparation.json').exists()})
    save('affected-inventory.json',{'affected_questions':[]})
    save('audit-milestone.json',{'sample_count':len(records),'replayed':len(replay),'excluded':[x for x in replay_result if x['status']=='excluded'],'package_unchanged':hashes(P)==json.load(open(E/'package-before.json'))})
    (E/'session-state.md').write_text('Source analysis verified before package access. Current oracle completed: 220 fresh samples, exact runner batch, three public batches, 16 complete source replays, six controlled records; q-34936 evidence gap retained. Native grader, delivery, rendering and relocated runtime still to run. See audit.py and audit-milestone.json.\n')
    print(json.dumps({'samples':len(records),'replay':len(replay),'excluded':g.EXCLUDED,'batch_shortcut':{'correct':sum(visible(r)['response']=='001' for r in sub),'total':len(sub)},'package_unchanged':hashes(P)==json.load(open(E/'package-before.json'))}))
if __name__=='__main__':main()
