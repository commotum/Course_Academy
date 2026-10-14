#!/usr/bin/env python3
"""Isolated basis-2275 draft: exact special-square recognition and public source replay.

Backbone: three labeled matrices; test square shape, then off-diagonal zeros,
then diagonal ones (identity only). Source banks are complete checkbox booleans
or the observed five subset answers. See private evidence for authored grades.
No EDB access, registration, assets, or dependency installation.
"""
import argparse, hashlib, itertools, json, math, random, re, sys, uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import matrix_tex, normalize_prose, validate_prose, validate_generated_record
HERE=Path(__file__).with_suffix('')
KP_ID=17592186087697
KP_UUID='09fa0899-a3d2-584f-8cdd-a471f8cfd16b'
TITLE='Identifying a Special Square Matrix'
VERSION='2.0.0-draft'
SUPPORTED_LEVELS=('easy','moderate','hard')
# These specify layouts and logical roles, never captured prompt/answer payloads.
TEMPLATES={
'q-11562':dict(kind='diagonal',labels=['H','J','L'],roles=['offdiagonal','diagonal','offdiagonal'],counts=[1,0,2],field_order=[0,1,2]),
'q-68741':dict(kind='identity',labels=['M','N','P'],roles=['identity','rectangular','diagonal'],counts=[0,0,0],field_order=[0,1,2],rectangular_patterns={1:'column_wrap'}),
'q-68744':dict(kind='diagonal',labels=['F','H','M'],roles=['offdiagonal','diagonal','diagonal'],counts=[2,0,0],field_order=[0,1,2],double_space=1),
'q-126222':dict(kind='diagonal',labels=['P','Q','R'],roles=['rectangular','rectangular','offdiagonal'],counts=[0,0,2],field_order=[0,1,2],dense=1,nbsp=0,rectangular_patterns={0:'truncated'}),
'q-68745':dict(kind='diagonal',labels=['S','R','Y'],roles=['diagonal','rectangular','offdiagonal'],counts=[0,0,2],field_order=[1,0,2],rectangular_patterns={1:'row_wrap'}),
'q-7829':dict(kind='identity',labels=['B','C','D'],roles=['diagonal','rectangular','identity'],counts=[0,0,0],field_order=[0],radio=True,rectangular_patterns={1:'truncated'}),
}
BANK_PROFILES={**{'raw-'+k:{'template':k,'origin':'observed raw evidence','eligible_for_learning':k!='q-7829'} for k in TEMPLATES},
**{'method-'+k:{'template':k,'origin':'authored method-derived complete bank','eligible_for_learning':True} for k in TEMPLATES}}
MATRIX_RE=re.compile(r'([A-Z])\s*=\s*\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}')

def arrays(text):
    out={}
    for m in MATRIX_RE.finditer(text):
        body=re.sub(r'\\text\{[^}]*\}','',m[2])
        out[m[1]]=[[str(sp.Rational(v.strip())) for v in row.split('&')] for row in body.split(r'\\')]
    return out

def properties(rows):
    m=sp.Matrix([[sp.Rational(x) for x in row] for row in rows])
    square=m.rows==m.cols
    diagonal=square and all(m[i,j]==0 for i in range(m.rows) for j in range(m.cols) if i!=j)
    return {'zero':all(x==0 for x in m),'square':square,'diagonal':diagonal,'identity':square and m==sp.eye(m.rows)}

def fingerprint_text(text):
    """Canonical actual predicate operands; ignore labels and irrelevant entries.

    Rectangular rejection depends only on shape. A square diagonal question
    inspects only offdiagonal zero/nonzero positions. An identity question also
    inspects diagonal one/nonone positions. Bank/profile/seed are excluded.
    """
    kind='identity' if 'identity matrices?' in text else 'diagonal'
    items=[]
    for m in arrays(text).values():
        r,c=len(m),len(m[0])
        if r!=c:items.append((r,c,()));continue
        values=tuple(tuple((int(sp.Rational(v)==1) if kind=='identity' else -1) if i==j else int(sp.Rational(v)!=0) for j,v in enumerate(row)) for i,row in enumerate(m))
        items.append((r,c,values))
    return json.dumps([kind,sorted(items)],separators=(',',':'))

def validate_parameters(level,t,p,raw=False):
    if set(p)!={'matrices','witnesses'}:raise ValueError('Exactly matrices and witnesses are required')
    if len(p['matrices'])!=3 or len(p['witnesses'])!=3:raise ValueError('Exactly three matrix/witness slots')
    cells=0
    for i,(m,w,role,count) in enumerate(zip(p['matrices'],p['witnesses'],t['roles'],t['counts'],strict=True)):
        if not m or not m[0] or len({len(row) for row in m})!=1:raise ValueError('Ragged or empty matrix')
        r,c=len(m),len(m[0]);cells+=r*c
        if not 1<=r<=5 or not 1<=c<=5:raise ValueError('Shape outside 1..5')
        if any(sp.Rational(v).q!=1 or not -3<=sp.Rational(v)<=7 for row in m for v in row):raise ValueError('Entries are bounded integers -3..7')
        props=properties(m)
        if role=='identity' and not props['identity']:raise ValueError('Identity role lost')
        if role=='diagonal' and (not props['diagonal'] or (props['identity'] and (raw or t['kind']=='identity'))):raise ValueError('Diagonal role or required identity obstruction lost')
        if role=='rectangular' and props['square']:raise ValueError('Rectangular role lost')
        if role=='rectangular':
            if t.get('dense')==i:
                if not all(sp.Rational(v)!=0 for row in m for v in row):raise ValueError('Dense rectangular role lost')
            elif m!=rectangular_matrix(r,c,t.get('rectangular_patterns',{}).get(i,'truncated')):raise ValueError('Sparse rectangular shape pattern lost')
        if role=='offdiagonal':
            actual=[(k+1,j+1) for k,row in enumerate(m) for j,v in enumerate(row) if k!=j and sp.Rational(v)!=0]
            if not props['square'] or len(actual)!=count:raise ValueError('Offdiagonal obstruction count lost')
            if not isinstance(w,list) or len(w)!=2 or tuple(w) not in actual:raise ValueError('Witness must name an actual nonzero offdiagonal cell')
        elif w is not None:raise ValueError('Unexpected witness')
    if raw:
        if level!='easy' or cells>36:raise ValueError('Source replay keeps its original easy/unrated workload')
    else:
        lo,hi={'easy':(3,36),'moderate':(37,45),'hard':(46,60)}[level]
        if not lo<=cells<=hi:raise ValueError('Outside authored level inspection workload')
    return cells

def rectangular_matrix(r,c,mode):
    return [['1' if (j==k if mode=='truncated' else j==k%c if mode=='row_wrap' else k==j%r) else '0' for j in range(c)] for k in range(r)]

def sample(level,t,rng,raw=False):
    for _ in range(2000):
        matrices=[];witnesses=[]
        for i,(role,count) in enumerate(zip(t['roles'],t['counts'],strict=True)):
            n=rng.randint(2 if role=='offdiagonal' else 1,5)
            r,c=(n,n) if role!='rectangular' else rng.choice([(a,b) for a in range(1,6) for b in range(1,6) if a!=b])
            m=[['0']*c for _ in range(r)]
            if role in ('identity','diagonal','offdiagonal'):
                for k in range(n):m[k][k]='1' if role=='identity' else rng.choice(['0','1','2','3','-2'])
                if role=='diagonal' and properties(m)['identity'] and (raw or t['kind']=='identity'):m[0][0]='0'
                if role=='offdiagonal':
                    for k,j in rng.sample([(a,b) for a in range(n) for b in range(n) if a!=b],count):m[k][j]=rng.choice(['1','2','-1','5','7'])
            elif t.get('dense')==i:
                m=[[rng.choice(['1','2']) for _ in range(c)] for _ in range(r)]
            else:
                m=rectangular_matrix(r,c,t.get('rectangular_patterns',{}).get(i,'truncated'))
            actual=[(k+1,j+1) for k,row in enumerate(m) for j,v in enumerate(row) if k!=j and sp.Rational(v)!=0]
            matrices.append(m);witnesses.append(list(rng.choice(actual)) if role=='offdiagonal' else None)
        p={'matrices':matrices,'witnesses':witnesses}
        try:validate_parameters(level,t,p,raw);return p
        except ValueError:pass
    raise ValueError('Bounded sampling found no eligible complete instance')

def matrix_text(label,m,nbsp=False,spaces=False):
    text=matrix_tex(m)
    if nbsp:text=text.replace(r'\end{bmatrix}',r'\text{'+chr(160)+r'}\end{bmatrix}')
    return label+(' = ' if spaces else '=')+text

def prompt(t,p,raw):
    kind=t['kind']
    if t.get('radio') and raw:
        return 'Which of the following are '+kind+' matrices?\n$'+', '.join(matrix_text(l,m,spaces=True) for l,m in zip(t['labels'],p['matrices'],strict=True))+'$'
    body=r',\,'.join(matrix_text(l,m,raw and t.get('nbsp')==i) for i,(l,m) in enumerate(zip(t['labels'],p['matrices'],strict=True)))
    ending='' if t.get('radio') else '\n\nSelect all that apply.'
    return 'Which of the following are '+kind+' matrices?\n\n$$\n'+body+'\n$$'+ending

def conclusion(labels,kind):
    if not labels:return 'Therefore, none of the given are '+kind+' matrices.'
    chosen=' and '.join('$'+l+'$' for l in labels)
    return 'Therefore, only '+chosen+((' is an' if kind=='identity' else ' is a') if len(labels)==1 else ' are')+' '+kind+(' matrix.' if len(labels)==1 else ' matrices.')

def solution(t,p):
    parts=[];selected=[]
    for i,(label,m,w) in enumerate(zip(t['labels'],p['matrices'],p['witnesses'],strict=True)):
        pr=properties(m);kind=t['kind'];is_correct=pr[kind]
        if is_correct:selected.append(label)
        article='an' if kind=='identity' else 'a'
        start='- $'+label+'$ is '+('' if is_correct else '*not* ')+article+' '+kind+' matrix'
        if not pr['square']:text=start+" since it's not a square matrix."
        elif kind=='identity':
            if is_correct:text=start+". First, it's a square matrix since it has the same number of rows and columns. Also, its entries on the main diagonal are all ones, and the rest of the entries are zeros."
            elif pr['diagonal']:text=start+'. Although it\'s a diagonal matrix, its diagonal entries are not all ones.'
            else:text=start+'. Some entries off the main diagonal are not zeros.'
        else:
            text=start+('.  ' if t.get('double_space')==i else '. ')+"It's a square matrix since it has the same number of rows and columns. "
            if pr['diagonal']:
                text+='Also, all the entries that do not lie on the main diagonal are zeros.'
                if not pr['identity']:text+='\n\nNotice that $'+label+'$ is not an identity matrix since the diagonal entries are not all ones.'
                else:text+='\n\nNotice that $'+label+'$ is also an identity matrix since the diagonal entries are all ones.'
            else:
                a,b=w;value=m[a-1][b-1]
                text+='But some of the entries that do not lie on the main diagonal are not zeros (for instance, ${'+label.lower()+'}_{'+str(a)+str(b)+'}='+value+r'\ne 0$).'
        parts.append(text)
    return '\n\n'.join(parts+[conclusion(selected,t['kind'])])

def subset_value(indices,labels):
    names=['$'+labels[i]+'$' for i in indices]
    if len(names)==1:return names[0]+' only'
    if len(names)==2:return ' and '.join(names)+' only'
    return names[0]+', '+names[1]+', and '+names[2]

def bank_specs(t,p,raw):
    if t.get('radio'):
        # Complete source bank represents the two temptations separately and jointly,
        # their conjunction with the genuine identity, and the identity alone.
        # Role slots preserve this eligibility, so no option repair is necessary.
        subsets=[(0,1),(0,2),(1,2),(0,1,2),(2,)]
        true=tuple(i for i,m in enumerate(p['matrices']) if properties(m)[t['kind']])
        if true not in subsets:raise ValueError('Complete radio bank lacks the correct subset')
        return [('selection','radio',[subset_value(x,t['labels']) for x in subsets],None if raw else subset_value(true,t['labels']))]
    return [(t['labels'][i],'checkbox',['false','true'],str(properties(p['matrices'][i])[t['kind']]).lower()) for i in t['field_order']]

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unknown level')
    if profile is not None:
        if profile not in BANK_PROFILES:raise ValueError('Unknown profile')
        if template is not None and BANK_PROFILES[profile]['template']!=template:raise ValueError('Profile/template mismatch')
        template=BANK_PROFILES[profile]['template']
    eligible=[k for k,t in TEMPLATES.items() if field_type is None or field_type==('radio' if t.get('radio') else 'checkbox')]
    if not eligible or template is not None and template not in eligible:raise ValueError('Unsupported template/field combination')
    rng=random.Random(seed);template=template or rng.choice(eligible);t=TEMPLATES[template]
    profile=profile or 'method-'+template;raw=profile.startswith('raw-')
    if raw and level!='easy':raise ValueError('Raw source level cannot be relabeled')
    p=json.loads(json.dumps(parameters)) if parameters is not None else sample(level,t,rng,raw)
    if set(p)!={'matrices','witnesses'}:raise ValueError('Exactly matrices and witnesses are required')
    p['matrices']=[[list(map(lambda x:str(sp.Rational(x)),row)) for row in m] for m in p['matrices']]
    cells=validate_parameters(level,t,p,raw)
    problem=normalize_prose(prompt(t,p,raw));worked=None if raw and t.get('radio') else normalize_prose(solution(t,p))
    specs=bank_specs(t,p,raw)
    display={'version':VERSION,'level':None if raw and t.get('radio') else level,'problem':problem,'worked_solution':worked,
             'fields':[(key,kind,sorted(values),correct) for key,kind,values,correct in specs]}
    content=json.dumps(display,sort_keys=True,separators=(',',':'))
    digest=hashlib.sha256(content.encode()).hexdigest();qid=str(uuid.uuid5(uuid.UUID(KP_UUID),content));fields=[]
    for key,kind,values,correct in specs:
        fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+key));answers=[]
        for v in values:answers.append({':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/text',':answer/value':v})
        rng.shuffle(answers)
        f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
        if correct is not None:f[':answer-field/correct']=[':answer/id',str(uuid.uuid5(uuid.UUID(fid),correct))]
        fields.append(f)
    q={':question/id':qid,':question/problem':problem,':question/answer-fields':fields}
    if worked is not None:q[':question/worked-solution']=worked
    if not(raw and t.get('radio')):q[':question/difficulty']=':question.difficulty/'+level
    rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
         'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,
                       'bank_origin':BANK_PROFILES[profile]['origin'],'source_basis':2275,'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','source_ids':[template],
                       'parameter_fingerprint':fingerprint_text(problem),'content_fingerprint':digest,'eligible_for_learning':BANK_PROFILES[profile]['eligible_for_learning'],
                       'authored_extension':not raw,'authored_difficulty':not raw and level!='easy','inspection_cells':cells,'domains':{'shape':[1,5],'integer_entries':[-3,7],'inspection_cells':{'easy':[3,36],'moderate':[37,45],'hard':[46,60]}},'plot_rating':'none'}}
    if worked is not None:validate_generated_record(rec)
    else:validate_prose(problem)
    return rec

# EASY: observed easy workload plus the explicitly completed unrated radio family.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: authored wider inspection workload; unchanged shape/entry predicates.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored wider inspection workload; unchanged shape/entry predicates.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(rec):
    q=rec['question'];lines=[q[':question/problem'],'']
    for f in q.get(':question/answer-fields',[]):
        vals={a[':answer/id']:a[':answer/value'] for a in f[':answer-field/choices']}
        lines+=['Field '+f[':answer-field/key']+' ('+f[':answer-field/type'].split('/')[-1]+'): '+', '.join(vals.values()),'Correct: '+vals[f[':answer-field/correct'][1]] if ':answer-field/correct' in f else 'Correct: absent in raw evidence']
    lines+=['',q.get(':question/worked-solution','Worked solution: absent in raw evidence')]
    return '\n'.join(lines)

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--difficulty',choices=['all',*SUPPORTED_LEVELS],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template',choices=TEMPLATES);a.add_argument('--profile',choices=BANK_PROFILES);a.add_argument('--field-type',choices=['checkbox','radio']);args=a.parse_args()
    if args.count<1:a.error('count must be positive')
    levels=list(SUPPORTED_LEVELS) if args.difficulty=='all' else [args.difficulty]
    try:records=[generate(l,args.seed+i,args.template,args.field_type,None,args.profile) for l in levels for i in range(args.count)]
    except ValueError as e:a.error(str(e))
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
