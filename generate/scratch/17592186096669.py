#!/usr/bin/env python3
"""Back substitution: exact homothetic variants of complete observed Easy banks.

Narrow policy: keep each source's coefficients, variable names, field shape and
complete choice-bank profile; multiply every RHS and choice coordinate by one
positive integer k in 1..9. This preserves all substitution stages and exact
error-vector relationships without inferring unsupported misconception recipes.
The package supports Easy only. Identity is based on the mathematical system
and bank, never seed or order. Inventory distinctness ignores the bank.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
import os
import sys
try:
    import sympy as sp
except ModuleNotFoundError:
    # InventoryJobs invokes scripts with its own interpreter. Use the existing
    # project's dependency environment, without installing or changing it.
    project_python=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__=='__main__' and project_python.is_file() and str(project_python)!=sys.executable:
        os.execv(str(project_python),[str(project_python),str(Path(__file__).resolve()),*sys.argv[1:]])
    raise

KP = 17592186096669
HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE/'source.json').read_text())
KPID = SOURCE['record'][':knowledge-point/id']
VERSION = '1.0.0'
SCALES = tuple(range(1,10))

# Source parameters: x+a*y+b*z=c, y+d*z=e, z=f.
PARAMETERS = {
 'q-20418':(1,-1,-1,'3','1/2','2'),
 'q-10195':(1,1,1,'1/2','1','2'),
 'q-10196':(-1,1,-1,'1','-1','3'),
 'q-10197':(-1,-1,2,'4','2','1/2'),
 'q-10198':(-1,3,-3,'9','2','1/3'),
 'q-10199':(-1,-1,-1,'3','2','1'),
 'q-129447':(-2,1,1,'2','-1/2','-1'),
 'q-129452':(1,-1,-1,'2','1/2','3'),
 'q-129453':(-1,-1,1,'4','2','-2'),
 'q-129455':(1,-1,-6,'2','3','-1/3'),
 'q-20421':(-1,-1,1,'4','2','3'),
}
QUESTIONS = {q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}

def canonical_tex(value):
    # Historical choice values contain an extra transport escaping layer.
    if value.startswith('⟨'):
        return value.replace('\\\\','\\')
    if value.startswith('\\\\begin'):
        return value.replace('\\\\','\\')
    return value

def number(tex):
    tex=tex.strip().replace(' ', '')
    m=re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(\d+)\}',tex)
    if m:return (-1 if m[1] else 1)*sp.Rational(int(m[2]),int(m[3]))
    if re.fullmatch(r'-?\d+',tex):return sp.Integer(tex)
    raise ValueError('Not an exact source coordinate: '+repr(tex))

def read_vector(tex):
    tex=canonical_tex(tex).strip()
    if tex.startswith('⟨') and tex.endswith('⟩'):parts=tex[1:-1].split(',')
    elif tex.startswith(r'\begin{bmatrix}') and tex.endswith(r'\end{bmatrix}'):
        parts=tex[len(r'\begin{bmatrix}'):-len(r'\end{bmatrix}')].split(r'\\')
    else:raise ValueError('Unknown vector notation: '+repr(tex))
    assert len(parts)==3
    return tuple(number(v) for v in parts)

def tex(n):return sp.latex(sp.Rational(n))

def vector(values,shape):
    return ('⟨'+','.join(tex(v) for v in values)+'⟩') if shape=='angle' else r'\begin{bmatrix}'+r' \\ '.join(tex(v) for v in values)+r'\end{bmatrix}'

def data(profile,k):
    if profile not in PARAMETERS:raise ValueError('Unsupported bank profile')
    if type(k) is not int or k not in SCALES:raise ValueError('Scale outside validated domain 1..9')
    a,b,d,c,e,f=PARAMETERS[profile]
    c,e,f=(sp.Rational(v)*k for v in (c,e,f))
    z=f;y=e-d*z;x=c-a*y-b*z
    return a,b,d,c,e,f,x,y,z

def system_fingerprint(profile,k):
    a,b,d,c,e,f,*_=data(profile,k)
    return hashlib.sha256(json.dumps([a,b,d,str(c),str(e),str(f)]).encode()).hexdigest()

def terms(first,coefficient,second):
    return first+('+' if coefficient>0 else '-')+(tex(abs(coefficient)) if abs(coefficient)!=1 else '')+second

def generate(difficulty='easy',seed=0,profile=None,scale=None,template=None):
    if difficulty!='easy':raise ValueError('Unsupported difficulty; only source-anchored Easy is validated')
    rng=random.Random(seed)
    eligible=list(PARAMETERS)
    if template:eligible=[p for p in eligible if ('column' if canonical_tex(QUESTIONS[p][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']).startswith('\\begin') else 'angle')==template]
    profile=profile or rng.choice(eligible)
    k=scale if scale is not None else rng.choice(SCALES)
    a,b,d,c,e,f,x,y,z=data(profile,k)
    q0=QUESTIONS[profile];f0=q0[':question/answer-fields'][0]
    shape='angle' if canonical_tex(f0[':answer-field/choices'][0][':answer/value']).startswith('⟨') else 'column'
    names=('x','y','z') if 'x_{1}' not in q0[':question/problem'] and '{x}_{1}' not in q0[':question/problem'] else ('{x}_{1}','{x}_{2}','{x}_{3}')
    nx,ny,nz=names
    prompt=q0[':question/problem']
    # The only prompt slots are the RHS constants, substituted in source order.
    rhs=iter((c,e,f))
    prompt=re.sub(r'&=\s*(-?\\frac\{\d+\}\{\d+\}|-?\d+)',lambda m:'&='+tex(next(rhs)),prompt)
    bank=[tuple(k*v for v in read_vector(ans[':answer/value'])) for ans in f0[':answer-field/choices']]
    correct=(x,y,z)
    assert len(bank)==5 and len(set(bank))==5 and bank.count(correct)==1
    identity=json.dumps([system_fingerprint(profile,k),shape,sorted([list(map(str,v)) for v in bank])],sort_keys=True)
    qid=uuid.uuid5(uuid.UUID(KPID),identity);fid=uuid.uuid5(qid,'selection')
    choices=[{':answer/id':str(uuid.uuid5(fid,','.join(map(str,v)))),':answer/type':':answer.type/math',':answer/value':vector(v,shape)} for v in bank]
    correct_id=choices[bank.index(correct)][':answer/id']
    second=terms(ny,d,'('+tex(z)+')')
    first=terms(terms(nx,a,'('+tex(y)+')'),b,'('+tex(z)+')')
    solution=(f'The third equation states that ${nz}={tex(z)}.$ Substituting this into the second equation, we get\n\n'
      +f'$$\n{second}={tex(e)}\\,⟹\\,{ny}={tex(e)}-({tex(d*z)})={tex(y)}.\n$$\n\n'
      +f'Now, we substitute ${ny}={tex(y)}$ and ${nz}={tex(z)}$ into the first equation to get\n\n'
      +f'$$\n{first}={tex(c)}\\,⟹\\,{nx}={tex(c)}-({tex(a*y)})-({tex(b*z)})={tex(x)}.\n$$\n\n'
      +f'Therefore, the solution is ${nx}={tex(x)}$, ${ny}={tex(y)}$, and ${nz}={tex(z)}.$ '
      +f'In vector form, the solution can be written as ${vector(correct,shape)}.$')
    return {'knowledge_point':{'db_id':KP,'id':KPID,'title':SOURCE['record'][':knowledge-point/title']},
      'question':{':question/id':str(qid),':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[
        {':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]},
      'generation':{'version':VERSION,'seed':seed,'parameters':{'scale':k},'domain':{'scale':list(SCALES)},'template':shape,'profile':profile,'source_question_ids':[q0[':db/id']],
        'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'sympy_version':sp.__version__,'mathematical_fingerprint':system_fingerprint(profile,k),
        'recipe':'Every complete observed choice vector multiplied by the same positive integer scale as every RHS; no pooled or inferred error bank'}}

def native_checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete radio bank selection'} for a in f[':answer-field/choices']]

def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--template',choices=['angle','column']);p.add_argument('--profile',choices=list(PARAMETERS));p.add_argument('--scale',type=int)
    args=p.parse_args()
    if args.difficulty!='easy':p.error('Unsupported difficulty: this validated package supports Easy only')
    if args.count<1:p.error('Count must be positive')
    domain=[(profile,k) for profile in PARAMETERS for k in SCALES if (not args.profile or profile==args.profile) and (args.scale is None or k==args.scale)]
    random.Random(args.seed).shuffle(domain)
    records=[];seen=set()
    for profile,k in domain:
        rec=generate(args.difficulty,args.seed,profile,k,template=args.template)
        if args.template and rec['generation']['template']!=args.template:continue
        fp=rec['generation']['mathematical_fingerprint']
        if fp not in seen:records.append(rec);seen.add(fp)
        if len(records)==args.count:break
    if len(records)<args.count:p.error(f'Finite domain: only {len(records)} genuinely distinct tasks match these constraints')
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
