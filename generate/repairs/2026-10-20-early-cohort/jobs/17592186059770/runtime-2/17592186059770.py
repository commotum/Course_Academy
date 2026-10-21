#!/usr/bin/env python3
"""Source-backed easy and moderate matrix questions; no database operations."""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186059770
KP_UUID='14d047c8-f032-5ff3-aced-65d40bfeeaad'
TITLE='Finding the Augmented Matrix of a Linear System With Variables Other Than x, y, z'
VERSION='other-variables-matrices-1.2'
SUPPORTED_LEVELS=('easy','moderate')
SOURCE=json.loads(Path(__file__).with_name('provenance.json').read_text())
SOURCE={k:SOURCE[k] for k in ('database','basis','lineage')}
TEMPLATES={'coefficient':'q-1070','augmented':'q-1073'}
SOURCE_PARAMETERS={'coefficient':{'a':4,'b':2,'c':3,'d':-11,'e':12},'augmented':{'k':4,'l':11,'m':3,'r':-1}}
EASY_SOURCES={
    'q-129137':([1,3,9,-4,2,1],['p','q']),
    'q-71731':([1,-1,1,1,-1,-1],[r'{x}_{1}',r'{x}_{2}']),
    'q-71733':([3,5,5,3,-5,-3],[r'{x}_{1}',r'{x}_{2}']),
    'q-71734':([1,-1,-1,-1,-1,1],['u','v']),
}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def tex(x):return sp.latex(sp.Rational(x))
def term(x,name,first=False,explicit=False):
    x=sp.Rational(x)
    sign='-' if x<0 else ('' if first else '+')
    return sign+('' if abs(x)==1 and not explicit else tex(abs(x)))+name

def linear(values,names):return ''.join(term(x,n,first=i==0,explicit=True) for i,(x,n) in enumerate(zip(values,names,strict=True)))
def matrix(rows,augmented=False):
    body=r' \\ '.join(' & '.join(tex(x) for x in row) for row in rows)
    if augmented:return r'\left[\begin{array}{'+'c'*(len(rows[0])-1)+'|c}'+body+r'\end{array}\right]'
    return r'\begin{bmatrix}'+body+r'\end{bmatrix}'
def system(equations):return r'\left\{\begin{aligned}'+r' \\ '.join(lhs+' &='+rhs for lhs,rhs in equations)+r'\end{aligned}\right.'
def normalize_parameters(template,p):
    assert set(p)==set(SOURCE_PARAMETERS[template]),'Parameter keys mismatch'
    p={k:int(v) for k,v in p.items() if not isinstance(v,bool) and sp.Rational(v).q==1}
    assert set(p)==set(SOURCE_PARAMETERS[template]),'Exact integers required'
    assert all(1<=abs(v)<=15 for v in p.values()),'Nonzero integer magnitudes 1..15 required'
    if template=='coefficient':
        assert p['a']!=p['b'],'Swapped-column distractor must differ'
    return p

def components(template,p,role_assignment=None):
    roles=role_assignment or {'columns':[0,1,2],'rows':[0,1]}
    columns=roles['columns'];order=roles['rows']
    if template=='coefficient':
        a,b,c,d,e=(p[k] for k in ('a','b','c','d','e'));names=[r'{x}_{1}',r'{x}_{2}',r'{x}_{3}']
        slots=[names[j] for j in columns]
        equations=[(term(b,slots[1],True)+term(a,slots[0]),term(c,slots[2],True)),(term(d,slots[2],True),tex(e))]
        A=[[a,b,-c],[0,0,d]];rhs=[0,e]
        banks=[('correct',A,False),('append_constants',[[a,b,-c,0],[0,0,d,e]],False),('appearance_order_and_keep_rhs_sign_with_constants',[[b,a,c,0],[0,0,d,e]],False),('keep_rhs_sign',[[a,b,c],[0,0,d]],False),('appearance_order_and_keep_rhs_sign',[[b,a,c],[0,0,d]],False)]
        kind='coefficient'
    else:
        k,l,m,r=(p[x] for x in ('k','l','m','r'));names=['a','b','c']
        slots=[names[j] for j in columns]
        equations=[(slots[0]+'-'+slots[2],term(k,slots[1],True)),(term(m,slots[2],True)+term(-l,slots[0]),tex(r))]
        A=[[1,-k,-1],[-l,0,m]];rhs=[0,r];C=[row+[v] for row,v in zip(A,rhs,strict=True)]
        banks=[('correct',C,True),('treat_b_coefficient_as_constant',[[1,0,-1,k],[-l,0,m,r]],True),('omit_b_column_and_use_second_row_appearance_order',[[1,-1,k],[m,-l,r]],True),('reverse_second_constant',[[1,-k,-1,0],[-l,0,m,-r]],True),('appearance_order_and_negate_c_second_row',[[1,-1,0,k],[-m,-l,0,r]],True)]
        kind='augmented'
    def reorder(rows,short=False):
        if short:
            selected=sorted(range(2),key=lambda i:columns[[0,2][i]])
            return [[rows[i][j] for j in selected]+[rows[i][2]] for i in order]
        return [[rows[i][columns.index(j)] for j in range(3)]+rows[i][3:] for i in order]
    A=reorder(A);rhs=[rhs[i] for i in order];equations=[equations[i] for i in order]
    banks=[(recipe,reorder(rows,template=='augmented' and len(rows[0])==3),aug) for recipe,rows,aug in banks]
    organized=[(linear(row,names),tex(v)) for row,v in zip(A,rhs,strict=True)]
    prompt='What is the '+kind+' matrix for the following system of linear equations?\n\n$$\n'+system(equations)+'\n$$'
    solution='First, we organize the system so that the variables are ordered $'+','.join(names)+'$ on the left-hand side, the constants are on the right-hand side, and every variable has a coefficient:\n\n$$\n'+system(organized)+'\n$$\n\nThe coefficient matrix consists of the coefficients of the variables:\n\n$$\n'+matrix(A)+'\n$$'
    if kind=='augmented':solution+='\n\nThe augmented matrix is the coefficient matrix augmented with the column that represents the right-hand sides of the equations:\n\n$$\n'+matrix([row+[v] for row,v in zip(A,rhs,strict=True)],True)+'\n$$'
    return prompt,solution,banks,A,rhs

def mathematical_fingerprint(template,A,rhs):
    # Exclude common scaling aliases, variable naming, bank/order and UUID changes.
    rows=[]
    for row,v in zip(A,rhs,strict=True):
        augmented=[sp.Rational(x) for x in (row if template=='coefficient' else row+[v])]
        pivot=next(x for x in augmented if x)
        rows.append([str(x/pivot) for x in augmented])
    return digest({'requested_matrix':template,'equations':rows})

def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None,bank_orientation=None,role_assignment=None,target_recipe=None):
    if level=='easy':return generate_easy(seed,template,parameters,profile,field_type,bank_orientation,target_recipe)
    if bank_orientation is not None:raise ValueError('Bank orientation applies to easy only')
    if level not in SUPPORTED_LEVELS:raise ValueError('Supported difficulties are easy and moderate; hard remains unimplemented')
    if field_type not in (None,'radio'):raise ValueError('Only source radio fields supported')
    rng=random.Random(seed);template=template or rng.choice(tuple(TEMPLATES))
    if template not in TEMPLATES:raise ValueError('Unknown template')
    profile=profile or TEMPLATES[template]
    if profile!=TEMPLATES[template]:raise ValueError('Template/profile mismatch')
    eligible=('correct','keep_rhs_sign','appearance_order_and_keep_rhs_sign') if template=='coefficient' else ('correct','reverse_second_constant')
    target=target_recipe or ('correct' if parameters is not None else rng.choice(eligible))
    if target not in eligible:raise ValueError('Target must preserve the supplied system template')
    roles=role_assignment or ({'columns':[0,1,2],'rows':[0,1]} if parameters is not None else {'columns':rng.sample(range(3),3),'rows':rng.sample(range(2),2)})
    if sorted(roles.get('columns',[]))!=[0,1,2] or sorted(roles.get('rows',[]))!=[0,1]:raise ValueError('Roles must permute three variable columns and two equations')
    if parameters is None:
        if template=='coefficient':
            a,b=rng.sample([i for i in range(-15,16) if i],2);p={'a':a,'b':b,'c':signed(rng,15),'d':signed(rng,15),'e':signed(rng,15)}
        else:p={key:signed(rng,15) for key in ('k','l','m','r')}
    else:p=parameters
    p=normalize_parameters(template,p)
    actual=dict(p)
    if template=='coefficient' and target!='correct':
        actual['c']=-p['c']
        if target=='appearance_order_and_keep_rhs_sign':actual['a'],actual['b']=p['b'],p['a']
    elif template=='augmented' and target!='correct':actual['r']=-p['r']
    prompt,solution,_,A,rhs=components(template,actual,roles)
    banks=components(template,p,roles)[2]
    target_index=next(i for i,(recipe,_,_) in enumerate(banks) if recipe==target)
    banks.insert(0,banks.pop(target_index))
    values=[matrix(rows,aug) for recipe,rows,aug in banks]
    assert len(set(values))==5
    content=digest({'template':template,'prompt':prompt,'bank':sorted(values),'correct':values[0]})
    qid=uid('question:'+content);fid=uid(qid+':selection')
    answers=[{':answer/id':uid(fid+':'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct=answers[0][':answer/id'];rng.shuffle(answers)
    q={':question/id':qid,':question/problem':prompt,':question/difficulty':':question.difficulty/'+level,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'role_assignment':roles,'target_recipe':target,'parameters':p,'system_parameters':actual,'source':SOURCE,'source_references':[profile],'eligible_for_learning':True,'evidence_only':False,'mathematical_fingerprint':mathematical_fingerprint(template,A,rhs),'content_identity':content,'recipes':[{'recipe':recipe,'is_correct':i==0,'matrix':rows,'augmented_notation':aug} for i,(recipe,rows,aug) in enumerate(banks)],'plot_rating':'none','domains':'signed nonzero integer magnitude 1..15; eligible source-template answer roles, permuted variable roles and equation rows','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def signed(rng,bound):return rng.choice((-1,1))*rng.randint(1,bound)

def easy_banks(profile,p,orientation='identity'):
    row_swap=orientation in ('row_swap','both');col_swap=orientation in ('column_swap','both')
    rp=[1,0] if row_swap else [0,1];cp=[1,0] if col_swap else [0,1]
    actual=[[p['a'],p['b'],p['e']],[p['c'],p['d'],p['f']]]
    base=[[actual[rp[i]][cp[j]] for j in range(2)]+[actual[rp[i]][2]] for i in range(2)]
    p=dict(zip('abcdef',[*base[0][:2],*base[1][:2],base[0][2],base[1][2]]))
    a,b,c,d,e,f=(p[k] for k in 'abcdef');C=[[a,b,e],[c,d,f]]
    transpose=lambda rows:[list(col) for col in zip(*rows)]
    if profile=='q-129137':
        wrong=[('swap_constants_and_reverse_d',[[a,b,f],[c,-d,e]]),('extra_zero_row',C+[[0,0,0]]),('swap_second_column_and_constants',[[a,e,b],[c,f,d]]),('transpose',transpose(C))]
    elif profile=='q-71731':
        wrong=[('reverse_off_diagonal_signs_transpose',transpose([[a,-b,e],[-c,d,f]])),('zero_constants',[[a,b,0],[c,d,0]]),('negate_first_row_coefficients_and_d',[[-a,-b,e],[c,-d,f]]),('negate_first_row_coefficients_c_and_f',[[-a,-b,e],[-c,d,-f]])]
    elif profile=='q-71733':
        wrong=[('zero_constants',[[a,b,0],[c,d,0]]),('swap_variable_columns',[[b,a,e],[d,c,f]]),('swap_variable_columns_reverse_constants',[[b,a,-e],[d,c,-f]]),('reverse_constants',[[a,b,-e],[c,d,-f]])]
    else:
        wrong=[('negate_first_row_coefficients',[[-a,-b,e],[c,d,f]]),('negate_all_coefficients',[[-a,-b,e],[-c,-d,f]]),('negate_first_row_coefficients_reverse_constants',[[-a,-b,-e],[c,d,-f]]),('negate_first_column_transpose',transpose([[-a,b,e],[-c,d,f]]))]
    def orient(rows):
        if len(rows)==3 and len(rows[0])==2:
            # Transposed choices have variable/constant rows and equation columns.
            return [[rows[i][j] for j in rp] for i in cp+[2]]
        order=rp+([2] if len(rows)==3 else [])
        return [[rows[i][j] for j in cp+[2]] for i in order]
    return [(recipe,orient(rows)) for recipe,rows in [('correct',C)]+wrong]

def generate_easy(seed=0,template=None,parameters=None,profile=None,field_type=None,bank_orientation=None,target_recipe=None):
    if template not in (None,'organized'):raise ValueError('Easy supports the organized augmented-matrix template')
    if field_type not in (None,'radio'):raise ValueError('Only source radio fields supported')
    rng=random.Random(seed);profile=profile or rng.choice(tuple(EASY_SOURCES))
    if profile not in EASY_SOURCES:raise ValueError('Unknown easy profile')
    orientation=bank_orientation or ('identity' if parameters is not None else rng.choice(('identity','row_swap','column_swap','both')))
    if orientation not in ('identity','row_swap','column_swap','both'):raise ValueError('Unknown bank orientation')
    # Every 2x3 candidate is itself a legitimate already-organized easy system.
    # Choose the answer-bearing role before numbers, preventing bank-only cues.
    eligible=[recipe for recipe,rows in easy_banks(profile,dict(zip('abcdef',[1,2,3,4,5,6])),orientation) if len(rows)==2 and len(rows[0])==3]
    target=target_recipe or ('correct' if parameters is not None else rng.choice(eligible))
    if target not in eligible:raise ValueError('Target must be a two-equation/two-variable augmented matrix')
    if parameters is not None:
        if set(parameters)!=set('abcdef') or any(type(v) is not int or not 1<=abs(v)<=9 for v in parameters.values()):
            raise ValueError('Easy parameters require six signed nonzero integers a..f of magnitude 1..9')
        p=dict(parameters)
    else:
        while True:
            p={k:signed(rng,9) for k in 'abcdef'}
            if len({matrix(rows,True) for _,rows in easy_banks(profile,p,orientation)})==5:break
    banks=easy_banks(profile,p,orientation);values=[matrix(rows,True) for _,rows in banks]
    if len(set(values))!=5:raise ValueError('Parameters merge choices in this source bank')
    target_index=next(i for i,(recipe,_) in enumerate(banks) if recipe==target)
    banks.insert(0,banks.pop(target_index));values=[matrix(rows,True) for _,rows in banks]
    C=banks[0][1];A=[row[:2] for row in C];rhs=[row[2] for row in C];names=EASY_SOURCES[profile][1]
    equations=[(term(row[0],names[0],True)+term(row[1],names[1]),tex(v)) for row,v in zip(A,rhs)]
    prompt='What is the augmented matrix for the following system of linear equations?\n\n$$\n'+system(equations)+'\n$$'
    solution='Notice that the system is already organized so that the variables are in the order $'+','.join(names)+'$ on the left-hand side, the constants are on the right-hand side, and every variable has a coefficient.\n\nThe coefficient matrix consists of the coefficients of the variables:\n\n$$\n'+matrix(A)+'\n$$\n\nThe augmented matrix is the coefficient matrix augmented with the column that represents the right-hand sides of the equations:\n\n$$\n'+values[0]+'\n$$'
    content=digest({'template':'organized','prompt':prompt,'bank':sorted(values),'correct':values[0]})
    qid=uid('question:'+content);fid=uid(qid+':selection')
    answers=[{':answer/id':uid(fid+':'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct=answers[0][':answer/id'];rng.shuffle(answers)
    q={':question/id':qid,':question/problem':prompt,':question/difficulty':':question.difficulty/easy',':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':'organized','bank_profile':profile,'bank_orientation':orientation,'target_recipe':target,'parameters':p,'source':SOURCE,'source_references':[profile],'eligible_for_learning':True,'evidence_only':False,'mathematical_fingerprint':mathematical_fingerprint('augmented',A,rhs),'content_identity':content,'recipes':[{'recipe':recipe,'is_correct':i==0,'matrix':rows,'augmented_notation':True} for i,(recipe,rows) in enumerate(banks)],'plot_rating':'none','domains':'six latent nonzero signed integers, magnitudes 1..9; eligible 2x3 answer roles and error-role assignments vary; reject duplicate banks','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)

def generate_batch(level,count,seed=0,template=None,parameters=None,profile=None):
    """Retain contrasting correct roles in small batches, not just in the pool.

    Source-parameter replay and single-record calls keep their existing contract.
    Shared banks have a shared option order but different displayed systems, so
    a bank-only rule cannot solve every member of any complete group.
    """
    if count<1:raise ValueError('Count must be positive')
    if parameters is not None or count==1:
        return [generate(level,seed+i,template,parameters,profile) for i in range(count)]
    rng=random.Random(seed);records=[];group=0;orientations={}
    while len(records)<count:
        remaining=count-len(records)
        size=3 if remaining%2 and remaining>=3 else min(2,remaining)
        chosen_template=template
        # The augmented moderate bank has only two compatible target roles.
        if level=='moderate' and size==3 and template is None and profile is None:
            chosen_template='coefficient'
        if level=='easy':
            chosen_profile=profile or rng.choice(tuple(EASY_SOURCES))
            previous=orientations.get(chosen_profile)
            opposite={'identity':'both','both':'identity','row_swap':'column_swap','column_swap':'row_swap'}
            orientation=opposite[previous] if previous is not None else rng.choice(tuple(opposite))
            shared_constants=chosen_profile=='q-129137' and previous is None
            orientations[chosen_profile]=orientation
            targets=[recipe for recipe,rows in easy_banks(chosen_profile,dict(zip('abcdef',[1,2,3,4,5,6])),orientation) if len(rows)==2 and len(rows[0])==3]
        else:
            if chosen_template is None and profile is not None:
                chosen_template=next((t for t,p in TEMPLATES.items() if p==profile),None)
            chosen_template=chosen_template or rng.choice(tuple(TEMPLATES))
            chosen_profile=profile or TEMPLATES.get(chosen_template)
            orientation=None
        if level!='easy' and chosen_template=='coefficient':
            targets=['correct','keep_rhs_sign','appearance_order_and_keep_rhs_sign']
        elif level!='easy':
            targets=['correct','reverse_second_constant']
        size=min(size,len(targets))
        targets=rng.sample(targets,size)
        base_seed=rng.getrandbits(64)
        base=generate(level,base_seed,chosen_template,profile=chosen_profile,bank_orientation=orientation,target_recipe=targets[0])
        if level=='easy' and shared_constants:
            # Exercise ambiguous RHS evidence, not only cases in which one
            # constant alone identifies the answer. All target roles remain.
            while True:
                p={**base['generation']['parameters']}
                p['f']=p['e']
                try:
                    base=generate(level,base_seed,chosen_template,p,chosen_profile,bank_orientation=orientation,target_recipe=targets[0])
                    break
                except ValueError:
                    base_seed=rng.getrandbits(64)
                    base=generate(level,base_seed,chosen_template,profile=chosen_profile,bank_orientation=orientation,target_recipe=targets[0])
        meta=base['generation']
        extra={'bank_orientation':orientation} if level=='easy' else {'role_assignment':meta['role_assignment']}
        order=sorted(a[':answer/value'] for a in base['question'][':question/answer-fields'][0][':answer-field/choices'])
        rng.shuffle(order)
        for target in targets:
            r=generate(level,base_seed,meta['template'],meta['parameters'],meta['bank_profile'],target_recipe=target,**extra)
            field=r['question'][':question/answer-fields'][0]
            by_value={a[':answer/value']:a for a in field[':answer-field/choices']}
            field[':answer-field/choices']=[by_value[value] for value in order]
            r['generation']['batch']={'seed':seed,'group':group,'size':size,'construction':'shared-bank-distinct-targets','decision_case':'shared_constants' if level=='easy' and shared_constants else 'independent_values'}
            records.append(r)
        group+=1
    rng.shuffle(records)
    return records

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='easy');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='json');parser.add_argument('--template',choices=[*TEMPLATES,'organized']);parser.add_argument('--parameters');parser.add_argument('--profile',choices=[*TEMPLATES.values(),*EASY_SOURCES])
    args=parser.parse_args()
    if args.count<1:parser.error('Count must be positive')
    level='moderate' if args.difficulty=='all' else args.difficulty
    try:records=generate_batch(level,args.count,args.seed,args.template,json.loads(args.parameters) if args.parameters else None,args.profile)
    except ValueError as e:parser.error(str(e))
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
