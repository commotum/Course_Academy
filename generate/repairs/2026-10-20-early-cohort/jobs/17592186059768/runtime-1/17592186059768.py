#!/usr/bin/env python3
"""Source-profile augmented-matrix generator; easy and moderate only.

Exact source replay couples observed literal parameters and preserves complete banks.
Normal sampling independently assigns signed entries and equation/variable roles.
No equation solving, row operations, additional stages or generated plots.
"""
import argparse, hashlib, json, random, re, uuid, sys
from pathlib import Path
from math_format import normalize_prose, normalize_tex, checked_math_content

KP_ID=17592186059768
KP_UUID='3f9ccaa5-d69c-584d-946e-0c57b3050160'
TITLE='Finding the Augmented Matrix of a System of Linear Equations'
VERSION='2.0.0'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
PROFILES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
SUPPORTED=('easy','moderate')

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def slots(q):
    texts=[q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
    return sorted({int(n) for t in texts for n in re.findall(r'\d+',t) if int(n)>1})
def render(text,parameters):
    text=re.sub(r'\d+',lambda m:str(parameters.get(m[0],int(m[0]))),text)
    text=normalize_prose(text)
    def coefficient(match):
        paragraph=text[:match.start()].rstrip().split('\n\n')[-1]
        if 'coefficient matrix' not in paragraph.lower() or 'augment' in paragraph.lower():return match[0]
        return re.sub(r'\\left\[\\begin\{array\}\{c+\|c\}(.*?)\\end\{array\}\\right\]',lambda matrix:r'\begin{bmatrix}'+matrix[1]+r'\end{bmatrix}',match[0],flags=re.S)
    return re.sub(r'\$\$.*?\$\$',coefficient,text,flags=re.S)
def matrices(text):
    return [[[int(x.strip()) for x in row.split('&')] for row in body.split('\\\\') if row.strip()] for _,body in re.findall(r'\\begin\{(array|bmatrix)\}(?:\{[^}]*\})?(.*?)\\end\{\1\}',text,re.S)]
def equations(text):
    return [r.replace('&','').strip() for r in re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)[1].split('\\\\')]
def terms(text):
    return re.findall(r'[+-]?[^+-]+',re.sub(r'\s+','',text))
def parse_system(text,n):
    out=[]
    for row in equations(text):
        result=[0]*(n+1)
        for side,expr in enumerate(row.split('=')):
            for term in terms(expr):
                var=term[-1] if term[-1] in 'xyz' else None
                a=term[:-1] if var else term
                value=int(a) if a not in ('','+','-') else (-1 if a=='-' else 1)
                j='xyz'.index(var) if var else n
                result[j]+=value*((1 if side==0 else -1) if var else (-1 if side==0 else 1))
        out.append(result)
    return out

def matrix_tex(m,augmented=True):
    body=r' \\ '.join(' & '.join(map(str,row)) for row in m)
    return (r'\left[\begin{array}{'+'c'*(len(m[0])-1)+'|c}'+body+r'\end{array}\right]') if augmented else r'\begin{bmatrix}'+body+r'\end{bmatrix}'
def expression(parts):
    result=''
    for value,var in parts:
        if not value:continue
        magnitude=abs(value)
        t=('' if magnitude==1 and var else str(magnitude))+var
        result+=('-' if value<0 else '+' if result else '')+t
    return result or '0'
def system_tex(rows):return r'\left\{\begin{aligned}'+r' \\ '.join(a+' &='+b for a,b in rows)+r'\end{aligned}\right.'
def prompt_rows(src,m,row_order,var_order):
    n=len(m[0])-1;out=[]
    for k,oldrow in enumerate(row_order):
        sides=[]
        for side,expr in enumerate(equations(src[':question/problem'])[oldrow].split('=')):
            parts=[]
            for token in terms(expr):
                var=token[-1] if token[-1] in 'xyz' else None
                if var:
                    j=var_order.index('xyz'.index(var));value=m[k][j]*(1 if side==0 else -1);parts.append((value,'xyz'[j]))
                elif int(token):parts.append((m[k][-1]*(-1 if side==0 else 1),''))
            sides.append(expression(parts))
        out.append(sides)
    return out

def permute_values(m,rng,mask):
    out=[r[:] for r in m];groups={}
    for i,row in enumerate(m):
        for j,v in enumerate(row):
            if v:groups.setdefault((v>0) if mask else 'all',[]).append((i,j))
    for cells in groups.values():
        vals=[m[i][j] for i,j in cells];rng.shuffle(vals)
        for (i,j),v in zip(cells,vals):out[i][j]=v
    return out

def bank_for_matrix(m,rng):
    # Explicit controlled inputs: same-mask banks defeat corner/sign recognition.
    bank=[m];seen={digest(m)}
    for _ in range(2000):
        candidate=permute_values(m,rng,True)
        if digest(candidate) not in seen:bank.append(candidate);seen.add(digest(candidate))
        if len(bank)==5:return bank
    raise ValueError('Not enough distinct same-mask entry assignments')

def sampled_instance(src,rng):
    correct=matrices(normalize_tex(src[':question/answer-fields'][0][':answer-field/correct'][':answer/value']))[0]
    n=len(correct[0])-1;nr=len(correct)
    # Assignment decisions precede magnitudes; candidates have equal status.
    mask=rng.choice([True,False]);chosen=rng.randrange(5)
    row_order=rng.sample(range(nr),nr);var_order=rng.sample(range(n),n)
    signs=[[rng.choice([-1,1]) for _ in row] for row in correct]
    values=iter(rng.sample(range(2,25),sum(abs(v)>1 for row in correct for v in row)))
    base=[[0 if v==0 else signs[i][j]*(1 if abs(v)==1 else next(values)) for j,v in enumerate(row)] for i,row in enumerate(correct)]
    bank=[];layouts=[];seen=set()
    for _ in range(3000):
        rows=row_order if mask else rng.sample(range(nr),nr)
        cols=var_order if mask else rng.sample(range(n),n)
        candidate=[[base[i][j] for j in cols]+[base[i][-1]] for i in rows]
        candidate=permute_values(candidate,rng,mask)
        if digest(candidate) in seen:continue
        seen.add(digest(candidate));bank.append(candidate);layouts.append((rows,cols))
        if len(bank)==5:break
    if len(bank)!=5:raise ValueError('Insufficient candidate assignments')
    return bank[chosen],bank,*layouts[chosen],('same-sign-mask' if mask else 'entry-roles')

def make_record(src,name,difficulty,seed,problem,solution,values,correct,parameters,extra=None):
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),digest([problem,sorted(values)])))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    question={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in choices if a[':answer/value']==correct)]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':name,'bank_profile':name,'parameters':parameters,'source_question_id':src[':question/id'],'source_basis':SOURCE['basis'],'eligible_for_learning':True,'evidence_only':False,**(extra or {})}}

@checked_math_content
def generate(difficulty,seed,template=None,parameters=None,profile=None,instance=None):
    if difficulty not in SUPPORTED:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed)
    names=[n for n,q in PROFILES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+difficulty)]
    name=profile or template or rng.choice(names)
    if name not in names:raise ValueError('Profile does not belong to requested difficulty')
    src=PROFILES[name];original={str(n):n for n in slots(src)}
    if parameters is not None:
        parameters={str(k):int(v) for k,v in parameters.items()}
        if set(parameters)!=set(original) or not all(1<=abs(v)<=24 for v in parameters.values()):raise ValueError('Invalid literal parameters')
        # The literal source point is a finite evidence replay, never a sampler mode.
        if parameters==original:
            values=[normalize_tex(render(a[':answer/value'],parameters)) for a in src[':question/answer-fields'][0][':answer-field/choices']]
            correct=normalize_tex(render(src[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],parameters))
            return make_record(src,name,difficulty,seed,render(src[':question/problem'],parameters),render(src[':question/worked-solution'],parameters),values,correct,parameters,{'mode':'source-replay'})
        problem=render(src[':question/problem'],parameters)
        # Signed literal substitutions must be parsed as ordinary sums, not -- tokens.
        problem=problem.replace('--','+').replace('+-','-').replace('-+','-').replace('++','+')
        n=3 if 'z' in problem else 2;m=parse_system(problem,n);bank=bank_for_matrix(m,rng)
        row_order=list(range(len(m)));var_order=list(range(n));mode='controlled-literals'
    else:
        m,bank,row_order,var_order,mode=sampled_instance(src,rng)
        if instance is not None:
            m=instance['matrix'];row_order=instance.get('row_order',row_order);var_order=instance.get('variable_order',var_order)
            bank=bank_for_matrix(m,rng);mode='controlled-instance'
        problem='What is the augmented matrix for the following system of linear equations?\n\n$$\n'+system_tex(prompt_rows(src,m,row_order,var_order))+'\n$$'
    n=len(m[0])-1
    organized=[]
    for row in m:
        lhs=''
        for j,v in enumerate(row[:-1]):
            term=(str(abs(v)) if abs(v)!=1 else '')+'xyz'[j]
            lhs+=('-' if v<0 else '+' if j else '')+term
        organized.append((lhs,str(row[-1])))
    solution='First, we organize the system so that the variables are ordered $'+','.join('xyz'[:n])+'$ on the left-hand side, the constants are on the right-hand side, and every variable has a coefficient:\n\n$$\n'+system_tex(organized)+'\n$$\n\nThe coefficient matrix consists of the coefficients of the variables:\n\n$$\n'+matrix_tex([row[:-1] for row in m],False)+'\n$$\n\nThe augmented matrix is the coefficient matrix augmented with the column that represents the right-hand sides of the equations:\n\n$$\n'+matrix_tex(m)+'\n$$'
    rng.shuffle(bank);values=[matrix_tex(x) for x in bank]
    return make_record(src,name,difficulty,seed,problem,solution,values,matrix_tex(m),parameters,{'mode':mode,'matrix':m,'row_order':row_order,'variable_order':var_order})
def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n\n'.join('$'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=SUPPORTED,required=True);p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--template');p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
    records=[generate(a.difficulty,a.seed+i,a.template) for i in range(a.count)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
