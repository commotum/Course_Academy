"""Seeded four-dimensional volume practice. Runtime is database-free and relocatable."""
import argparse
import hashlib
import itertools
import json
import math
import random
import uuid
from math_format import normalize_prose, validate_generated_record

KP = 17592186119932
VERSION = '1.0.0'
SUPPORT = {
    'easy': ['302209ad-3d64-52f9-9fa9-99104ad6beb3','210e9083-358f-508e-9376-e356564e0e4d'],
    'moderate': ['c594e512-d19a-53c5-8f50-4caaf295111c','c3a8456a-5f67-54bf-8d0a-07a8bbe82bf5'],
    'hard': ['395a5b70-ac13-5278-8751-fd5d50d0bc64'],
}

def mat(a, env='bmatrix'):
    return r'\begin{' + env + '}' + r' \\ '.join(' & '.join(map(str,row)) for row in a) + r'\end{' + env + '}'

def display(tex):
    return '\n\n$$\n' + tex + '\n$$'

def scalar(x):
    return '(' + str(x) + ')' if x < 0 else str(x)

def minor(a,i,j):
    return [[v for c,v in enumerate(row) if c!=j] for r,row in enumerate(a) if r!=i]

def triangular(a):
    n=len(a)
    return all(not a[i][j] for i in range(n) for j in range(i)) or all(not a[i][j] for i in range(n) for j in range(i+1,n))

def derive(a):
    """Ordered lesson operations, preserving the learner's minors and cofactor signs."""
    n=len(a)
    if triangular(a):
        factors=[a[i][i] for i in range(n)]
        return {'a':a,'kind':'product','factors':factors,'value':math.prod(factors)}
    if n==2:
        p,q=a[0][0]*a[1][1],a[0][1]*a[1][0]
        return {'a':a,'kind':'cross','p':p,'q':q,'value':p-q}
    lines=[(sum(v!=0 for v in a[i]),'row',i) for i in range(n)]
    lines += [(sum(a[i][j]!=0 for i in range(n)),'column',j) for j in range(n)]
    # Among equally sparse lines, prefer the one with simpler surviving minors.
    # This retains the one-versus-two-contribution instructional progression
    # after row/column permutations instead of expanding needless extra branches.
    minimum=min(line[0] for line in lines)
    candidates=[]
    for count,axis,index in lines:
        if count!=minimum:continue
        entries=[(index,j) for j in range(n)] if axis=='row' else [(i,index) for i in range(n)]
        terms=[{'i':i,'j':j,'pivot':a[i][j],'factor':a[i][j]*(-1)**(i+j),'child':derive(minor(a,i,j))} for i,j in entries if a[i][j]]
        tree={'a':a,'kind':'expand','axis':axis,'index':index,'terms':terms,'value':sum(t['factor']*t['child']['value'] for t in terms)}
        candidates.append((sum(node['kind']=='expand' for t in terms for _,node in nodes(t['child'])),sum(operation_work(t['child']) for t in terms),axis!='row',index,tree))
    return min(candidates,key=lambda t:t[:4])[4]

def operation_work(t):
    if t['kind']=='product':return len(t['factors'])
    if t['kind']=='cross':return 3
    return len(t['terms'])+sum(operation_work(x['child']) for x in t['terms'])

def nodes(tree,path=()):
    yield path,tree
    for k,t in enumerate(tree.get('terms',[])):
        yield from nodes(t['child'],path+(k,))

def faults(tree):
    """Complete authored error operations; profile selection precedes collision checks."""
    out=[]
    for path,t in nodes(tree):
        if t['kind']=='product':
            for i in range(len(t['factors'])):
                out.extend([(path,'omit-factor',i),(path,'repeat-factor',i)])
            out.append((path,'add-factors',0))
            # Replace a multiplication joining two factor groups by addition.
            out.extend((path,'add-product-groups',mask) for mask in range(1,2**len(t['factors'])-1) if mask & 1)
        elif t['kind']=='cross':
            out.extend((path,k,0) for k in ['add-cross-products','first-cross-product','second-cross-product','multiply-cross-products','row-products-difference','column-products-difference'])
        else:
            for i in range(len(t['terms'])):
                out.extend([(path,'omit-pivot',i),(path,'repeat-pivot',i),(path,'omit-branch',i),(path,'add-pivot',i)])
            if len(t['terms'])>1:
                out.extend((path,k,0) for k in ['absolute-contributions','flip-first-sign'])
    return out

def evaluate(t,fault=None,path=()):
    selected=fault is not None and tuple(fault[0])==path
    mode,idx=(fault[1],fault[2]) if selected else ('correct',0)
    if t['kind']=='product':
        f=t['factors']
        if mode=='omit-factor': return math.prod(f[:idx]+f[idx+1:])
        if mode=='repeat-factor':return math.prod(f)*f[idx]
        if mode=='add-factors':return sum(f)
        if mode=='add-product-groups':return math.prod(x for i,x in enumerate(f) if idx & (1<<i))+math.prod(x for i,x in enumerate(f) if not idx & (1<<i))
        return t['value']
    if t['kind']=='cross':
        p,q=t['p'],t['q']
        return {'correct':p-q,'add-cross-products':p+q,'first-cross-product':p,'second-cross-product':q,'multiply-cross-products':p*q,'row-products-difference':t['a'][0][0]*t['a'][1][0]-t['a'][0][1]*t['a'][1][1],'column-products-difference':t['a'][0][0]*t['a'][0][1]-t['a'][1][0]*t['a'][1][1]}[mode]
    values=[x['factor']*evaluate(x['child'],fault,path+(i,)) for i,x in enumerate(t['terms'])]
    if mode=='omit-pivot':
        x=t['terms'][idx];values[idx]=(-1)**(x['i']+x['j'])*evaluate(x['child'],fault,path+(idx,))
    elif mode=='add-pivot':
        x=t['terms'][idx];values[idx]=(-1)**(x['i']+x['j'])*(x['pivot']+evaluate(x['child'],fault,path+(idx,)))
    elif mode=='repeat-pivot':values[idx]*=t['terms'][idx]['pivot']
    elif mode=='omit-branch':values[idx]=0
    elif mode=='absolute-contributions':return sum(map(abs,values))
    elif mode=='flip-first-sign':values[0]*=-1
    return sum(values)

def solution(a,tree):
    text='Construct the matrix whose columns are the four vectors:' + display('M='+mat(a)+'.')
    text+='\n\nThe volume is the absolute value of its determinant:' + display(r'V=|\det(M)|.')
    labels={path:(r'\det(M)' if not path else 'D_{'+str(i)+'}') for i,(path,_) in enumerate(nodes(tree))}
    for path,t in nodes(tree):
        label=labels[path]
        if path:text+='\n\nEvaluate the minor' + display(label+'='+mat(t['a'],'vmatrix')+'.')
        if t['kind']=='product':
            text+='\n\nThis matrix is triangular, so multiply its diagonal entries.'
            text+=display(label+'='+r'\cdot '.join(scalar(x) for x in t['factors'])+'='+str(t['value'])+'.')
        elif t['kind']=='cross':
            b=t['a']
            text+='\n\nUse the difference of the cross products.'
            text+=display(r'\begin{aligned}'+label+'&='+scalar(b[0][0])+r'\cdot '+scalar(b[1][1])+'-'+scalar(b[0][1])+r'\cdot '+scalar(b[1][0])+r'\\&='+scalar(t['p'])+'-'+scalar(t['q'])+'='+str(t['value'])+r'.\end{aligned}')
        else:
            text+='\n\nExpand along '+t['axis']+' $'+str(t['index']+1)+'$, retaining the cofactor signs.'
            expr='+'.join(scalar(x['pivot'])+'(-1)^{'+str(x['i']+1)+'+'+str(x['j']+1)+'}'+labels[path+(k,)] for k,x in enumerate(t['terms'])) or '0'
            text+=display(label+'='+expr+'.')
    # Combining bottom-up makes all intermediate evaluations available before use.
    for path,t in reversed(list(nodes(tree))):
        if t['kind']=='expand':
            expr='+'.join(scalar(x['factor'])+r'\cdot '+scalar(x['child']['value']) for x in t['terms']) or '0'
            text+='\n\nCombine the signed contributions:' + display(labels[path]+'='+expr+'='+str(t['value'])+'.')
    text+='\n\nTherefore,' + display('V=|'+str(tree['value'])+'|='+str(abs(tree['value']))+'.')
    return normalize_prose(text)

def uid(body):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy-volume-v1:'+body))

def make_record(a,band,values,profile=None,family=None):
    tree=derive(a);v=abs(tree['value'])
    assert len(values)==len(set(values))==5 and values.count(v)==1
    vectors=[mat([[a[i][j]] for i in range(4)]) for j in range(4)]
    problem=normalize_prose('Calculate the volume of the $4$-dimensional parallelepiped spanned by the vectors'+display(',\\quad '.join('\\mathbf{'+name+'}='+vec for name,vec in zip('abcd',vectors))+'.'))
    worked=solution(a,tree)
    # All prose is normalized before identities are calculated.
    identity=json.dumps([band,problem,worked,values],separators=(',',':'))
    qid=uid(identity)
    answers=[{':answer/id':uid(qid+':answer:'+str(x)),':answer/type':{':db/ident':':answer.type/math'},':answer/value':str(x)} for x in values]
    field={':answer-field/id':uid(qid+':field'),':answer-field/key':'selection',':answer-field/type':{':db/ident':':answer-field.type/radio'},':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(c[':answer/id'] for c in answers if c[':answer/value']==str(v))]}
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':worked,':question/difficulty':{':db/ident':':question.difficulty/'+band},':question/answer-fields':[field]}
    record={'knowledge_point':KP,'question':q,'generation':{'version':VERSION,'family':family,'matrix':a,'profile':profile,'support':SUPPORT[band]}}
    validate_generated_record(record)
    return record

def nz(r):return r.choice([-4,-3,-2,-1,1,2,3,4])

def insert_singleton(a,axis,i,j,pivot,r):
    n=len(a)+1;b=[[0]*n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if x!=i and y!=j:b[x][y]=a[x-(x>i)][y-(y>j)]
    b[i][j]=pivot
    # Singleton column: other entries in its row do not affect the surviving minor.
    for y in range(n):
        if y!=j:b[i][y]=nz(r)
    if axis=='row':b=[list(row) for row in zip(*b)]
    return b

def sample_matrix(r,band,family):
    if band=='easy':
        a=[[r.randint(-3,3) if j>=i else 0 for j in range(4)] for i in range(4)]
        for i in range(4):a[i][i]=nz(r)
        if family=='lower':a=[list(row) for row in zip(*a)]
        return a
    if band=='moderate':
        if family=='triangular-minor':
            a=[[nz(r) if j>=i else 0 for j in range(3)] for i in range(3)]
            if r.randrange(2):a=[list(row) for row in zip(*a)]
        else:
            a=[[nz(r),nz(r)],[nz(r),nz(r)]]
            a=insert_singleton(a,r.choice(['row','column']),r.randrange(3),r.randrange(3),nz(r),r)
        return insert_singleton(a,r.choice(['row','column']),r.randrange(4),r.randrange(4),nz(r),r)
    pattern=[[1,1,0,0],[0,1,1,1],[1,0,1,1],[0,0,1,1]]
    a=[[nz(r) if x else 0 for x in row] for row in pattern]
    rows=list(range(4));cols=list(range(4));r.shuffle(rows);r.shuffle(cols)
    return [[a[i][j] for j in cols] for i in rows]

EASY_PROFILES={'omission':{'omit-factor':2,'add-product-groups':2},'repetition':{'repeat-factor':2,'add-product-groups':2},'addition':{'add-product-groups':3,'add-factors':1},'mixed':{'omit-factor':1,'repeat-factor':1,'add-product-groups':1,'add-factors':1}}
ARITHMETIC={'add-product-groups','add-factors','add-pivot','add-cross-products','row-products-difference','column-products-difference'}

def admissible_profile(band,kinds,style=None):
    if band=='easy':
        profiles=[EASY_PROFILES[style]] if style else EASY_PROFILES.values()
        return any(all(kinds.count(k)==n for k,n in profile.items()) for profile in profiles)
    if band=='moderate':
        return sum(k in ARITHMETIC for k in kinds) in ([style] if style else [2,3])
    return True

def repair_batch_banks(records,band,r):
    # Guard repeated visible families against a universal bank-only rank/position cue.
    # Change only the authored error bank: preserve all mathematical instances.
    by_family={}
    for index,rec in enumerate(records):by_family.setdefault(rec['generation']['family'],[]).append(index)
    for family,indices in by_family.items():
        if len(indices)<2:continue
        def bank(rec):
            field=rec['question'][':question/answer-fields'][0]
            vs=[int(c[':answer/value']) for c in field[':answer-field/choices']]
            v=abs(derive(rec['generation']['matrix'])['value'])
            return vs,v,sorted(vs).index(v),vs.index(v)
        ranks={bank(records[i])[2] for i in indices}
        if len(ranks)==1:
            fixed=next(iter(ranks))
            # Prefer a nonzero witness. Zero is necessarily the smallest valid volume.
            for index in reversed(indices):
                rec=records[index];a=rec['generation']['matrix'];t=derive(a);key=abs(t['value'])
                if key==0:continue
                fs=faults(t);ev=[abs(evaluate(t,f)) for f in fs]
                eligible=[i for i,v in enumerate(ev) if v!=key]
                chosen=None;total=0
                for ix in itertools.combinations(eligible,4):
                    vs=[key]+[ev[i] for i in ix]
                    if len(set(vs))!=5 or sorted(vs).index(key)==fixed:continue
                    if not admissible_profile(band,[fs[i][1] for i in ix]):continue
                    total+=1
                    if r.randrange(total)==0:chosen=ix
                if chosen is None:continue
                vs=[key]+[ev[i] for i in chosen];r.shuffle(vs)
                replacement=make_record(a,band,vs,[fs[i] for i in chosen],family)
                replacement['generation'].update({k:v for k,v in rec['generation'].items() if k in ['seed','index','attempts_so_far']})
                replacement['generation']['batch_bank_guard']='alternate complete error profile; same matrix'
                records[index]=replacement
                break
        positions={bank(records[i])[3] for i in indices}
        if len(positions)==1:
            index=indices[-1];rec=records[index];vs,key,_,position=bank(rec)
            target=r.choice([i for i in range(5) if i!=position])
            vs[position],vs[target]=vs[target],vs[position]
            replacement=make_record(rec['generation']['matrix'],band,vs,rec['generation']['profile'],family)
            replacement['generation'].update(rec['generation'])
            replacement['generation']['batch_position_guard']='distinct position within repeated family'
            records[index]=replacement
    return records

def generate(band,count,seed):
    if band=='unclassified':band='moderate'
    r=random.Random(seed)
    families={'easy':['upper','lower'],'moderate':['triangular-minor','two-singletons'],'hard':['two-contributions']}[band]
    output=[];seen=set();attempts=0
    styles=[];style=None
    # A shuffled structural cycle avoids a finite batch dropping a supported family.
    schedule=[]
    while len(output)<count:
        if not schedule:schedule=r.sample(families,len(families))
        family=schedule[-1]
        if band=='moderate' and style is None:
            style=r.choice([2,3])
        if band=='easy' and style is None:
            if not styles:styles=r.sample(['omission','repetition','addition','mixed'],4)
            style=styles[-1]
        attempts+=1
        if attempts>max(10000,count*5000):raise RuntimeError('Could not construct distinct five-choice banks')
        a=sample_matrix(r,band,family)
        if band=='moderate' and triangular(a):continue
        t=derive(a);fs=faults(t)
        if len(fs)<4:continue
        # Hold the mathematical instance while selecting a complete compatible bank.
        # Reservoir sampling chooses uniformly among whole four-fault profiles,
        # rather than greedily taking the first distinct errors or rejecting zeros.
        error_values=[abs(evaluate(t,f)) for f in fs]
        eligible=[i for i,v in enumerate(error_values) if v!=abs(t['value'])]
        selected=None;compatible=0
        for indices in itertools.combinations(eligible,4):
            if band=='moderate':
                if not admissible_profile(band,[fs[i][1] for i in indices],style):continue
            if band=='easy':
                kinds=[fs[i][1] for i in indices]
                if not admissible_profile(band,kinds,style):continue
            if len({error_values[i] for i in indices})!=4:continue
            compatible+=1
            if r.randrange(compatible)==0:selected=indices
        if selected is None:continue
        profile=[fs[i] for i in selected]
        values=[abs(t['value'])]+[error_values[i] for i in selected]
        semantic=json.dumps(a)
        if semantic in seen:continue
        r.shuffle(values)
        rec=make_record(a,band,values,profile,family)
        rec['generation'].update({'seed':seed,'index':len(output),'attempts_so_far':attempts})
        if band=='easy':
            rec['generation']['bank_style']=style
            styles.pop();style=None
        if band=='moderate':
            rec['generation']['bank_style']={'arithmetic_errors':style}
            style=None
        output.append(rec);seen.add(semantic);schedule.pop()
    return repair_batch_banks(output,band,r)

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],required=True);p.add_argument('--count',type=int,required=True);p.add_argument('--seed',type=int,required=True);p.add_argument('--format',choices=['json'],default='json')
    a=p.parse_args()
    if a.count<0:p.error('--count must be nonnegative')
    print(json.dumps(generate(a.difficulty,a.count,a.seed),ensure_ascii=False))

if __name__=='__main__':main()
