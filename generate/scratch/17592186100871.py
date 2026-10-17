#!/usr/bin/env python3
"""Source-backed bounded matrix-product dimensions; no database operations.

Entries and labels are incidental. Only ordered operand dimensions create new
mathematical tasks. Moderate uses forward products; hard uses reversed products.
Easy has no supported source template. See capabilities and extraction in package.
"""
import argparse,hashlib,json,os,random,sys,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts/question_capture'))
from math_format import matrix_operands
try:
    import sympy as sp
except ModuleNotFoundError:
    if __name__ != '__main__':raise
    executable=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if not executable.is_file():raise
    os.execv(str(executable),[str(executable),str(Path(__file__).resolve()),*sys.argv[1:]])
sys.dont_write_bytecode=True
HERE=Path(__file__).with_suffix('');sys.path.insert(0,str(HERE))
from math_reader import displayed,fingerprint,dimension
KP_ID=17592186100871
CAPTURE=json.loads((HERE/'source.json').read_text());SOURCE=CAPTURE['record']
SOURCE_BY_ID={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
EXCLUDED={'q-22065':'Unrated; correct-answer link and worked solution absent. Original preserved.'}
VERSION='matrix-product-dimensions-v1'
TEMPLATES={mid:{'level':q[':question/difficulty'][':db/ident'].split('/')[-1],'field_type':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1],'profile':'source-bank:'+mid} for mid,q in SOURCE_BY_ID.items() if mid not in EXCLUDED}
SUPPORTED=('moderate','hard')

def domain(mid):
    if mid=='q-129492':return [(r,r,c) for r in range(2,5) for c in range(2,5) if r!=c]
    if mid=='q-77475':return [(1,k,1) for k in range(2,5)]
    if mid=='q-77476':return [(r,1,r) for r in range(2,5)]
    if mid=='q-320351':return [(r,1,c) for r in range(2,5) for c in range(2,5) if r!=c]
    if mid=='q-320389':return [(r,k,1) for r in range(2,5) for k in range(2,5)]
    if mid in ('q-22067','q-275395','q-320371'):return [(r,k,r) for r in range(2,5) for k in range(2,5) if r!=k]
    if mid=='q-129489':return [(r,k,c) for r in range(2,5) for k in range(2,5) for c in range(2,5) if len({r,k,c})==3]
    raise ValueError(mid)

def recipes(mid,r,k,c):
    if mid=='q-129489':return [('inner×outer-right',(k,c)),('transpose',(c,r)),('outer-right-square',(c,c)),('correct',(r,c)),('undefined',None)]
    if mid=='q-129492':return [('correct',(r,c)),('transpose',(c,r)),('undefined',None),('outer-right-square',(c,c)),('outer-left-square',(r,r))]
    return [('undefined',None),('outer-left×inner',(r,k)),('inner×outer-left',(k,r)),('inner-square',(k,k)),('correct',(r,c))]

def matrix(rows,cols):
    # Fixed deterministic values; counting rows/columns is the entire task.
    return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(str((i*cols+j)%9-4) for j in range(cols)) for i in range(rows))+r'\end{bmatrix}'

def generate(level,seed=0,template=None,parameters=None,profile=None,replay=False):
    if level not in SUPPORTED:raise ValueError('Unsupported difficulty: '+level)
    rng=random.Random(seed);mids=sorted(mid for mid,t in TEMPLATES.items() if t['level']==level)
    mid=template or rng.choice(mids)
    if mid not in mids:raise ValueError('Template does not support level')
    assert profile in (None,TEMPLATES[mid]['profile'])
    src=SOURCE_BY_ID[mid];_,labels,observed=displayed(src)
    p=parameters or dict(zip(('r','k','c'),observed if replay else rng.choice(domain(mid))))
    assert set(p)=={'r','k','c'} and all(type(v) is int for v in p.values())
    r,k,c=(p[a] for a in ('r','k','c'))
    assert (r,k,c) in domain(mid)
    if replay:assert (r,k,c)==observed
    # Exact independent matrix multiplication verifies dimensions before rendering.
    result=sp.zeros(r,k)*sp.zeros(k,c);assert result.shape==(r,c)
    a,b=labels;reverse=level=='hard';first,second=(b,a) if reverse else (a,b)
    shapes={a:(r,k),b:(k,c)};kind=TEMPLATES[mid]['field_type']
    tail='What are the dimensions of $'+a+b+'?$' if kind=='radio' else 'Then, the dimensions of $'+a+b+r'$ are{{field-1}}$\times $'+'\n{{field-2}}.'
    problem='Let\n$'+first+'='+matrix(*shapes[first])+'$\nand\n$'+second+'='+matrix(*shapes[second])+'.$\n'+tail
    colword='is $1$ column' if k==1 else 'are $'+str(k)+'$ columns';rowword='row' if k==1 else 'rows'
    solution='We notice that $'+first+'$ is a $'+str(shapes[first][0])+r'\times '+str(shapes[first][1])+'$ matrix and $'+second+'$ is a $'+str(shapes[second][0])+r'\times '+str(shapes[second][1])+'$ matrix. \n\nThere '+colword+' in $'+a+'$ and $'+str(k)+'$ '+rowword+' in $'+b+'.$ Since the number of columns in $'+a+'$ equals the number of rows in $'+b+',$ the matrices $'+a+'$ and $'+b+'$ are conformable for multiplication. \n\nThe product $'+a+b+'$ has dimensions $'+str(r)+r'\times '+str(c)+':$\n\n$$\n{'+a+'}_{'+str(r)+r'\times \boxed{\text{'+str(k)+r'}}}{\times }_{✓}{'+b+r'}_{\boxed{\text{'+str(k)+r'}}\times '+str(c)+'}={'+a+b+'}_{'+str(r)+r'\times '+str(c)+'}\n$$'
    if replay:
        problem=src[':question/problem'];solution=src[':question/worked-solution']
        if mid=='q-22067':solution=solution.replace('$3\\times 2$ matrix','$4\\times 2$ matrix')
    identity=json.dumps([VERSION,level,kind,mid,r,k,c],separators=(',',':'))
    qid=str(uuid.uuid5(uuid.UUID(SOURCE[':knowledge-point/id']),identity));fields=[]
    for sf in sorted(src[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
        key=sf[':answer-field/key'];fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+key));bank=recipes(mid,r,k,c) if kind=='radio' else [('correct',(r if key=='field-1' else c))]
        choices=[];correct=None
        for recipe,value in bank:
            aid=str(uuid.uuid5(uuid.UUID(fid),'recipe:'+recipe));val='The product is undefined' if value is None else str(value[0])+r'\times '+str(value[1]) if isinstance(value,tuple) else str(value)
            choices.append({':answer/id':aid,':answer/type':':answer.type/text' if value is None else ':answer.type/math',':answer/value':val})
            if recipe=='correct':correct=aid
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/correct':[':answer/id',correct],':answer-field/choices':choices})
    # Preserve raw replay and every stable identity while improving only the
    # learner-facing operand layout and dimension-control spacing.
    if not replay:
        problem='Let\n\n'+matrix_operands([first+'='+matrix(*shapes[first]),second+'='+matrix(*shapes[second])])+'\n\n'+tail
        problem=problem.replace('are{{field-1}}$\\times $\n{{field-2}}',
            'are <span style="display: inline-flex; align-items: center; gap: .35em; white-space: nowrap;">{{field-1}} $\\times$ {{field-2}}</span>')
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
    return {'question':q,'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'generation':{'version':VERSION,'seed':seed,'template':mid,'parameters':p,'bank_profile':TEMPLATES[mid]['profile'],'source_question':src[':question/id'],'source_db_id':src[':db/id'],'source_basis':CAPTURE['basis'],'source_lineage':CAPTURE['lineage'],'eligible_for_learning':not replay,'evidence_only':replay,'sympy_version':sp.__version__,'python_version':sys.version.split()[0],'domains':'positive integer dimensions, shared inner dimension; profile conditions enforced','entry_policy':'deterministic incidental integers; entries never create distinct tasks'}}

def candidates(level,seed=0):
    out=[];used=set()
    for mid in sorted(TEMPLATES):
        if TEMPLATES[mid]['level']!=level:continue
        for p in domain(mid):
            if p in used:continue
            used.add(p);out.append(generate(level,seed,mid,dict(zip(('r','k','c'),p))))
    random.Random(seed).shuffle(out);return out

def markdown(rec):
    q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join(f[':answer-field/key']+': '+', '.join(a[':answer/value']+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']) for f in q[':question/answer-fields'])+'\n\n'+q[':question/worked-solution']

def generate_moderate(**kwargs):return generate('moderate',**kwargs)
def generate_hard(**kwargs):return generate('hard',**kwargs)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard'],required=True);p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
    if a.difficulty not in SUPPORTED:p.error('unsupported level; see capabilities.json')
    out=candidates(a.difficulty,a.seed)
    if not 0<=a.count<=len(out):p.error('finite limit: '+str(len(out)))
    print(json.dumps(out[:a.count],indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,out[:a.count])))
