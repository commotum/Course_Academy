"""Validate current four-source banks and every bounded easy mathematical task."""
import copy,hashlib,importlib.util,json,re,subprocess,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('open_intervals',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ENGINE=HERE.parents[1]/'runs/current/check-engine'
def clean(t):
    t=re.sub(r'\{\\color\{(?:red|blue)\}\{([^{}]*)\}\}',r'\1',t)
    return t.replace(r'\,','').replace('$','').strip().rstrip('.?')
def num(t):
    t=t.strip().replace('−','-').replace(' ','')
    if t in ('-∞',r'-\infty'):return -s.oo
    t=re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',t)
    t=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1/\2)',t)
    assert re.fullmatch(r'[-+\d/().sqrt]+',t),t
    out=s.sympify(t);assert out.is_real and out.is_finite,t
    return out

def math_object(t):
    t=clean(t)
    if '∈' in t:t=t.split('∈')[1].strip()
    if re.match(r'[xyzt]\s*\\in\s',t):t=t.split(r'\in',1)[1].strip()
    if t[0] in '([' and ',' in t:
        a,b=map(num,t[1:-1].split(','));assert a<b
        return s.Interval(a,b,left_open=t[0]=='(',right_open=t[-1]==')')
    if ' or ' in t:
        m=re.fullmatch(r'([xyzt])\s*<\s*(.*?)\s+or\s+\1\s*>\s*(.*)',t);assert m,t
        return s.Union(s.Interval.open(-s.oo,num(m[2])),s.Interval.open(num(m[3]),s.oo))
    m=re.fullmatch(r'(.*?)\s*(\\le|<)\s*([xyzt])\s*(\\le|<)\s*(.*)',t);assert m,t
    a,b=num(m[1]),num(m[5]);assert a<b
    return s.Interval(a,b,left_open=m[2]=='<',right_open=m[4]=='<')

def fingerprint(q):
    obj=math_object(re.findall(r'\$(.*?)\$',q[':question/problem'])[0]);template='inequality_to_interval' if q[':question/problem'].startswith('The inequality') else 'interval_to_inequality'
    return g.digest({'template':template,'a':str(obj.start),'b':str(obj.end)})

def normalize(q):
    q=copy.deepcopy(q)
    for key in list(q):
        if key not in (':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):del q[key]
    q[':question/id']=str(q[':question/id'])
    if isinstance(q.get(':question/difficulty'),dict):q[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
    fields=[]
    for f in q[':question/answer-fields']:
        typ=f[':answer-field/type'];correct=f.get(':answer-field/correct')
        nf={':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(typ[':db/ident']) if isinstance(typ,dict) else typ,':answer-field/choices':[]}
        if correct:nf[':answer-field/correct']=[':answer/id',str(correct[':answer/id']) if isinstance(correct,dict) else str(correct[1])]
        for a in f[':answer-field/choices']:
            typ=a[':answer/type'];nf[':answer-field/choices'].append({':answer/id':str(a[':answer/id']),':answer/type':str(typ[':db/ident']) if isinstance(typ,dict) else typ,':answer/value':a[':answer/value']})
        nf[':answer-field/choices'].sort(key=lambda a:a[':answer/id']);fields.append(nf)
    q[':question/answer-fields']=sorted(fields,key=lambda f:f[':answer-field/key']);return q

def inspect(rec,raw=False):
    assert rec['knowledge_point']['db_id']==g.KP_ID
    q=normalize(rec['question']);assert len(q[':question/answer-fields'])==1
    f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    bank=f[':answer-field/choices'];assert len(bank)==5 and len({a[':answer/id'] for a in bank})==5
    for identity in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in bank]:uuid.UUID(identity)
    expected=math_object(re.findall(r'\$(.*?)\$',q[':question/problem'])[0]);assert expected.left_open and expected.right_open and expected.start!=-s.oo and expected.end!=s.oo
    values=[math_object(a[':answer/value']) for a in bank];assert len(set(values))==5 and values.count(expected)==1
    if raw:return
    assert q[':question/difficulty']==':question.difficulty/easy'
    correct=f[':answer-field/correct'];assert correct[0]==':answer/id'
    assert next(values[i] for i,a in enumerate(bank) if a[':answer/id']==correct[1])==expected
    solution=q[':question/worked-solution'];assert '*not* included' in solution
    rows=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);assert len(rows)==(3 if q[':question/problem'].startswith('The inequality') else 2)
    assert all(math_object(row)==expected for row in rows)
    for t in [q[':question/problem'],solution]+[a[':answer/value'] for a in bank]:
        assert t.count('$')%2==0 and t.count('{')==t.count('}') and '\\\\' not in t
    if 'mathematical_fingerprint' in rec.get('generation',{}):assert fingerprint(q)==rec['generation']['mathematical_fingerprint']
    if 'content_fingerprint' in rec.get('generation',{}):
        actual=g.digest({'version':g.VERSION,'prompt':q[':question/problem'],'solution':solution,'bank':sorted((a[':answer/value'],a[':answer/type'].split('/')[-1]) for a in bank),'correct':next(a[':answer/value'] for a in bank if a[':answer/id']==correct[1])})
        assert actual==rec['generation']['content_fingerprint'] and q[':question/id']==g.uid('question',actual)

def native(records,path):
    path.mkdir(parents=True,exist_ok=True)
    items=[]
    for r in records:
        inspect(r);f=r['question'][':question/answer-fields'][0]
        items.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently parsed complete-set semantics'} for a in f[':answer-field/choices']]})
    (path/'native-input.json').write_text(json.dumps(items,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    return json.loads((path/'native-report.json').read_text())

def validate():
    source=json.loads((HERE/'current-source.json').read_text());questions=source['record'][':knowledge-point/questions'];assert len(questions)==4
    cases=[('q-102204','inequality_to_interval','source_raw',{'a':3,'b':7}),('q-59294','interval_to_inequality','source_raw',{'a':3,'b':4}),('q-1256','inequality_to_interval','signed_source',{'a':-3,'b':-1}),('q-154704','inequality_to_interval','surd_source',{'a':'-sqrt(2)','b':'sqrt(2)'})]
    canonical=source['record'][':knowledge-point/canonical-example']
    assert all(math_object(row)==s.Interval.open(1,5) for row in re.findall(r'\$\$\n(.*?)\n\$\$',canonical[':question/worked-solution'],re.S))
    records=[];evidence=[]
    for sid,t,p,params in cases:
        original=next(q for q in questions if q[':question/math-academy-id']==sid);r=g.generate('easy',17,t,parameters=params,profile=p);inspect(r,p=='source_raw');q=r['question']
        assert q[':question/problem']==original[':question/problem']
        f=normalize(original)[':question/answer-fields'][0];rf=q[':question/answer-fields'][0]
        assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'],a[':answer/value']) for a in rf[':answer-field/choices'])
        if p!='source_raw':
            assert q[':question/worked-solution']==original[':question/worked-solution']
            records.append(r);records.append({'knowledge_point':r['knowledge_point'],'question':normalize(original),'generation':{'template':t}})
        else:records.append(g.generate('easy',17,t,parameters=params))
        evidence.append({'source_id':sid,'profile':p,'prompt_exact':True,'complete_bank_exact':True,'choices_matched':5,'correct_ref': 'matched value' if p!='source_raw' else 'absent; derived independently','worked_solution': 'byte exact' if p!='source_raw' else 'absent; authored'})
    fps=set()
    for a,b in g.catalog('easy'):
        for t in g.TEMPLATES:
            r=g.generate('easy',7,t,parameters={'a':a,'b':b});inspect(r);fps.add(fingerprint(r['question']));records.append(r)
    profile_counts={}
    for p in ('signed_source','surd_source'):
        eligible=[(a,b) for a,b in g.catalog('easy') if ('sqrt' not in a and int(b)<0) if p=='signed_source'] if p=='signed_source' else [(a,b) for a,b in g.catalog('easy') if 'sqrt' in a]
        for a,b in eligible:
            r=g.generate('easy',7,'inequality_to_interval',parameters={'a':a,'b':b},profile=p);inspect(r);records.append(r)
        profile_counts[p]=len(eligible)
        for seed in range(20):inspect(g.generate('easy',seed,profile=p))
    for t in g.TEMPLATES:
        for a,b in [('1','12'),('-12','0'),('-sqrt(30)','sqrt(30)')]:
            for var in ('x','y','t','z'):
                r=g.generate('easy',1,t,parameters={'a':a,'b':b,'variable':var});inspect(r)
                alt=g.generate('easy',2,t,parameters=r['generation']['parameters']);assert normalize(r['question'])==normalize(alt['question'])
    for level,p in [('moderate',{'a':1,'b':3}),('hard',{'a':1,'b':3}),('easy',{'a':5,'b':4}),('easy',{'a':'1/2','b':3}),('easy',{'a':'-sqrt(4)','b':'sqrt(4)'})]:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError((level,p))
    report=native(records,HERE/'reference/current-validation')
    result={'passed':True,'source_basis':source['basis'],'source_lineage':source['lineage'],'source_banks':evidence,'source_banks_matched':4,'source_banks_total':4,'source_options_matched':20,'source_options_total':20,'source_worked_solutions_matched':2,'source_worked_solutions_available':2,'unrated_incomplete_sources_preserved':2,'canonical_formatting':'Current canonical has original whitespace; normalized legacy canonical wording retained in generic authored solutions, separately from byte-exact practice replay. Both stages checked by set semantics.','supported_levels':list(g.LEVELS),'finite_mathematical_tasks':{'easy':len(fps)},'source_profile_cases':profile_counts,'independently_checked_records':len(records),'native_grading':{k:v for k,v in report.items() if k!='records'},'hashes':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ['../17592186059826.py','validate-current.py','current-source.json']},'unresolved_failures':[]}
    (HERE/'current-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':validate()
