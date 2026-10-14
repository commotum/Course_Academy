"""Rendered-task duplicate detection and validation, independent of seed/profile IDs."""
import copy, importlib.util, json, re
from pathlib import Path
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('tangent_validation',HERE/'legacy_validation.py')
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
z=importlib.util.spec_from_file_location('current_tangent',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)

def claim(st):
    bits=v.mathbits(st)
    if 'domain' in st:
        if 'except' in st:return ['domain-excluded',lattice(bits)]
        if st=='The domain is all real numbers.':return ['domain','R']
        return ['domain',interval(bits[-1])]
    if 'range' in st:return ['range',interval(bits[-1].split('\\in ',1)[-1].replace('y∈',''))]
    if 'zeros' in st:return ['zeros',lattice(bits)]
    if 'asymptote' in st:return ['asymptotes',lattice(bits)]
    if 'positive' in st or 'negative' in st:
        if 'period' in st:
            return ['least-period',str(v.expr(bits[-1])) if bits else 'none']
        return ['sign','positive' if 'positive' in st else 'negative',interval(next(b for b in bits if ',' in b))]
    if 'passes through' in st:return ['point',interval(bits[-1])]
    args=v.tangent_arguments(st)
    assert len(args)==2,st
    # The two supplied angle roles matter; strip algebraic spelling, not shifts.
    return ['identity',sorted(str(z) for z in args)]

def lattice(bits):
    e=v.expr(next(b.split('=',1)[1] for b in bits if '=' in b))
    step=v.sp.simplify(v.sp.diff(e,v.n)/v.sp.pi)
    offset=v.sp.simplify(e.subs(v.n,0)/v.sp.pi)
    assert step!=0 and v.sp.diff(e,v.n,2)==0
    return [str(abs(step)),str(v.sp.Mod(offset,abs(step)))]

def interval(raw):
    raw=raw.replace(r'\,','').strip().rstrip('., ')
    raw=raw[min(i for i in (raw.find('('),raw.find('[')) if i>=0):]
    assert raw[0] in '([' and raw[-1] in ')]',raw
    a,b=raw[1:-1].split(',')
    return [raw[0],str(v.expr(a)),str(v.expr(b)),raw[-1]]

def fingerprint(q):
    # A statement permutation does not establish another mathematical task.
    return g.digest(sorted((claim(s) for s in statements(q[':question/problem'])),key=lambda c:json.dumps(c,sort_keys=True)))

def statements(prompt):
    prompt=re.sub(r'- \*\*I{1,3}\.\*\* ', '- ',prompt)
    return v.statements(prompt)

def check(rec):
    fields=rec['question'][':question/answer-fields']
    if fields[0][':answer-field/type']==':answer-field.type/radio':return v.check(rec)
    assert len(fields)==3
    actual=[bool(v.truth(st)) for st in statements(rec['question'][':question/problem'])]
    for i,f in enumerate(fields):
        assert f[':answer-field/key']==g.ROMAN[i] and f[':answer-field/type']==':answer-field.type/checkbox'
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==str(actual[i]).lower()
    # Validate the printed solution with the independent legacy mathematics parser.
    # This projection is only a correctness check: grading uses the actual fields.
    projected=copy.deepcopy(rec);q=projected['question']
    q[':question/problem']=re.sub(r'- \*\*I{1,3}\.\*\* ', '- ',q[':question/problem'])
    labels=g.SUBSETS.copy();correct=g.label(actual)
    if correct not in labels:labels.append(correct)
    labels=[correct]+[s for s in labels if s!=correct][:4]
    q[':question/answer-fields']=[{':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/id':str(i),':answer/value':label} for i,label in enumerate(labels)],':answer-field/correct':[':answer/id','0']}]
    if not projected['generation'].get('evidence_only'):
        v.check(projected)
    return rec

def native(rec,label):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Printed Boolean claim truth'})
    return {'label':label,'record':rec,'checks':checks}

def record(q):
    # Validate database content from its actual printed claims/key, not a replay key.
    normalized=copy.deepcopy(q)
    normalized[':question/id']=str(q[':question/id'])
    normalized[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
    normalized[':question/answer-fields'].sort(key=lambda f:g.ROMAN.index(f[':answer-field/key']))
    for f in normalized[':question/answer-fields']:
        f[':answer-field/id']=str(f[':answer-field/id'])
        f[':answer-field/type']=str(f[':answer-field/type'][':db/ident'])
        f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
        for a in f[':answer-field/choices']:
            a[':answer/id']=str(a[':answer/id']);a[':answer/type']=str(a[':answer/type'][':db/ident'])
    level=normalized[':question/difficulty'].rsplit('/',1)[1]
    rec={'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':normalized,'generation':{'evidence_only':False,'level':level,'template':'database-current'}}
    check(rec);return rec
