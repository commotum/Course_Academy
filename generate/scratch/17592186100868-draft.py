"""KP17592186100868: exact, private matrix–column-vector generators.

Extracted source recipes live in the same-basename evidence directory. They are
structural prompt/solution masks and complete expression banks, never returned as
literal source-question payloads. Every public call rebuilds inputs, ordered dot
products, evaluated terms, collected answers, field-owned banks and identities.
Observed bank expressions encode patterns, not diagnoses of learner intent.
"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, importlib.util, json, random, re, uuid
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
ROOT=Path(__file__).with_suffix(''); ASSETS=ROOT/'assets'
_spec=importlib.util.spec_from_file_location('kp100868_math_format',ROOT/'math_format.py')
mf=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(mf)
TEMPLATES=json.loads((ROOT/'templates.json').read_text())
VERSION='100868-v1.0'; KP={'db_id':17592186100868,'id':'8451e22a-247e-51dd-8fb1-9ce9b212dc65','title':'Multiplying a Matrix With Variable Entries by a Column Vector'}
NS=uuid.UUID('c8ec906d-40ec-515b-a67d-87bc2daf608b')
TRANS=standard_transformations+(implicit_multiplication_application,)
def scalar(tex):
    t=re.sub(r'\\[,!; ]','',tex).replace(r'\cdot','*').replace('{','(').replace('}',')').replace('^','**')
    if not re.fullmatch(r'[a-z0-9+*() .\-]+',t):raise ValueError('Unsupported scalar '+tex)
    t=re.sub(r'(?<=[0-9a-z])(?=[a-z])','*',t)
    return parse_expr(t,local_dict={c:S.Symbol(c) for c in 'abcdefghijklmnopqrstuvwxyz'},transformations=TRANS)
def tex(expr):
    # Native parser reserves `ln`; explicitly separate a product of scalar l,n.
    raw=S.latex(expr,order='lex').replace(' ','').replace(r'\left','').replace(r'\right','')
    return mf.normalize_tex(raw.replace('ln',r'l\cdot n'))
def guarded(obj):
    if isinstance(obj,str) and any(ord(c)<32 and c not in '\n\t\r' for c in obj):raise ValueError('C0 control character')
    if isinstance(obj,dict):
        for k,v in obj.items():guarded(k);guarded(v)
    if isinstance(obj,list):
        for v in obj:guarded(v)
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(tag,obj):return str(uuid.uuid5(NS,tag+digest(obj)))
def matrix(rows):return mf.matrix_tex(rows,augmented=False)
def group(expr):
    t=tex(expr);return '('+t+')' if expr.could_extract_minus_sign() or isinstance(expr,S.Add) else t
def summed(terms):
    out=tex(terms[0])
    for x in terms[1:]:
        t=tex(x);out+=t if t.startswith('-') else '+'+t
    return out

def _parameters(t,rng,given):
    variables=t['variables'];explicit=given is not None;given={} if given is None else dict(given)
    if explicit and not {'scales','names'}<=set(given):raise ValueError('Explicit parameters require complete scales and names maps')
    if set(given)-{'scales','names','vector','matrix_coefficients','matrix_gain'}:raise ValueError('Unknown parameter key')
    scales=given.get('scales',{v:(1 if t['source_id']=='q-318595' else rng.randint(1,3 if t['level']=='easy' else 2)) for v in variables})
    # Names are complete symbol slots, never replacements across prose or labels.
    names=given.get('names',{v:v for v in variables})
    if set(scales)!=set(variables) or set(names)!=set(variables):raise ValueError('Every symbol slot is required')
    if any(type(v)!=int or not 1<=v<=5 for v in scales.values()):raise ValueError('Scale bounds 1..5')
    if len(set(names.values()))!=len(variables) or any(not re.fullmatch('[a-z]',v) for v in names.values()):raise ValueError('Distinct single-letter variable names required')
    # Protect matrix/vector object names; source scalar x is permitted when vector is u.
    label=re.search(r'Find \$([A-Z])([a-z])\$',t['prompt_mask']) or re.search(r'find \$([A-Z])([a-z])',t['prompt_mask'])
    if label and label[2] in names.values():raise ValueError('Scalar variable collides with column-vector name')
    p={'scales':dict(scales),'names':dict(names)}
    if t['source_id']=='q-13554':
        uv=given.get('vector',[1,2] if explicit else [rng.randint(1,3),rng.randint(2,3)])
        if not isinstance(uv,list) or len(uv)!=2 or any(type(x)!=int for x in uv) or not(1<=uv[0]<=4 and 2<=uv[1]<=5) or uv[0]==uv[1]:raise ValueError('Easy vector: u1..4,v2..5,u != v')
        p['vector']=uv
    elif 'vector' in given:raise ValueError('Vector coefficients are fixed for this family')
    if t['source_id']=='q-318595':
        coeff=given.get('matrix_coefficients',[6,-4,-5,2] if explicit else [rng.randint(1,6),-rng.randint(1,6),-rng.randint(1,6),rng.randint(1,6)])
        if not isinstance(coeff,list) or len(coeff)!=4 or any(type(x)!=int or not 1<=abs(x)<=6 for x in coeff) or [x>0 for x in coeff]!=[True,False,False,True]:raise ValueError('Matrix coefficient signs and magnitudes must match +,-,-,+ and1..6')
        p['matrix_coefficients']=coeff
    elif 'matrix_coefficients' in given:raise ValueError('Independent matrix coefficients are fixed outside q-318595')
    if t['source_id'] in {'q-275597','q-318589','q-70226'}:
        gain=given.get('matrix_gain',1 if given else rng.randint(1,2))
        if type(gain)!=int or gain not in [1,2]:raise ValueError('Matrix gain1..2')
        p['matrix_gain']=gain
    elif 'matrix_gain' in given:raise ValueError('Matrix gain fixed for this family')
    return p

def _substitute(t,p):return {S.Symbol(v):p['scales'][v]*S.Symbol(p['names'][v]) for v in t['variables']}
def _bank_value(value,subs):
    if value.startswith(r'\begin{bmatrix}'):
        e=mf.environment(value,0);return matrix([[tex(scalar(c).xreplace(subs)) for c in row] for row in mf.cells(value[e[0]:e[1]])])
    return tex(scalar(value).xreplace(subs))
def _value_expr(value):
    if value.startswith(r'\begin{bmatrix}'):
        e=mf.environment(value,0);return tuple(scalar(c) for row in mf.cells(value[e[0]:e[1]]) for c in row)
    return (scalar(value),)
def _equal(a,b):return len(a)==len(b) and all(S.expand(x-y)==0 for x,y in zip(a,b))
def _easy_bank(M,V):
    a,c=M[0];b,d=M[1];u,v=V
    return [[u*a+c,u*b+v*d],[u*a+v*c,v*b+v*d],[v*a+v*c,u*b+v*d],[u*a+v*c,u*b+v*d],[u*a+v*c,u*b+d]]

# Source-grounded workload ceilings: numeric polynomial coefficients, not values
# assigned to free scalars. Caps inspect actual operands, individual products and
# collected row components before a bank or content identity is constructed.
WORKLOAD={'easy':{'factor':3,'product':6,'collected':6},'moderate':{'factor':6,'product':6,'collected':7},'hard':{'factor':2,'product':4,'collected':4}}
def _max_coefficient(expressions):
    out=0
    for e in expressions:
        if e==0:continue
        syms=sorted(e.free_symbols,key=str)
        coeffs=S.Poly(S.expand(e),*syms).coeffs() if syms else [e]
        out=max(out,max(abs(c) for c in coeffs))
    return out
def _workload(level,M,V,products,answer):
    cap=WORKLOAD[level]
    if _max_coefficient([x for row in M for x in row]+list(V))>cap['factor'] or _max_coefficient([x for row in products for x in row])>cap['product'] or _max_coefficient(answer)>cap['collected']:raise ValueError('Actual displayed arithmetic exceeds '+level+' workload caps')

# Easy: canonical two-row variable matrix, two positive numeric vector entries.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: observed two-row collection and symbolic products; no new operators.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed three-row signed symbolic row products and cancellations.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

@mf.checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in {'easy','moderate','hard'}:raise ValueError('Invalid level')
    rng=random.Random(seed);eligible=[k for k,t in TEMPLATES.items() if t['level']==level]
    if template is not None and template not in eligible:raise ValueError('Template is outside level')
    template=template or rng.choice(eligible);t=TEMPLATES[template]
    expected_type=t['fields'][0]['type']
    if field_type and field_type.split('/')[-1]!=expected_type:raise ValueError('Field type is fixed by template')
    profile=profile or ('authored-operations' if expected_type=='radio' and template!='q-13554' else 'observed')
    if profile not in ({'observed','authored-operations'} if expected_type=='radio' and template!='q-13554' else {'observed'}):raise ValueError('Unsupported complete profile')
    # Reject a whole sampled instance; explicit parameters fail without alteration.
    for attempt in range(100):
        try:p=_parameters(t,rng,parameters)
        except ValueError:
            if parameters is not None:raise
            continue
        subs=_substitute(t,p);M=[[scalar(c).xreplace(subs) for c in row] for row in t['inputs'][0]]
        V=[scalar(row[0]).xreplace(subs) for row in t['inputs'][1]]
        if template=='q-13554':V=list(map(S.Integer,p['vector']))
        if template=='q-318595':
            a,b,c,d=p['matrix_coefficients'];pp,qq=[S.Symbol(p['names'][v]) for v in ['p','q']]
            M=[[a*p['scales']['p']*pp,b*p['scales']['q']*qq],[c*p['scales']['p']*pp,d*p['scales']['q']*qq]]
        M=[[p.get('matrix_gain',1)*x for x in row] for row in M]
        products=[[S.expand(a*b) for a,b in zip(row,V)] for row in M];answer=[S.expand(sum(row)) for row in products]
        try:_workload(level,M,V,products,answer)
        except ValueError:
            if parameters is not None:raise
            continue
        if expected_type=='radio':
            if template=='q-13554':values=[matrix([[tex(x)] for x in row]) for row in _easy_bank(M,V)]
            elif profile=='observed':
                values=[_bank_value(x,subs) for x in t['fields'][0]['choices']]
                if p.get('matrix_gain',1)!=1:values=[matrix([[tex(p['matrix_gain']*x)] for x in _value_expr(v)]) for v in values]
            else:
                # One complete authored operation profile; every wrong option is tied
                # to a row operation, with no learner-facing error diagnosis.
                choices=[answer,[-x for x in answer], [S.expand(sum(row[1:])) for row in products], [S.expand(sum(row[:-1])) for row in products]]
                # Change every vector-entry sign used by the original, preserving zero.
                if template=='q-127276':alternate=[S.expand(sum(a*b for a,b in zip(row,V[::-1]))) for row in M]
                elif template=='q-13556':alternate=answer[::-1]
                elif template=='q-127277':alternate=[S.expand(sum(row)) for row in M]
                else:alternate=[S.expand(sum(a*(-b if b.could_extract_minus_sign() else b) for a,b in zip(row,V))) for row in M]
                choices.append(alternate)
                values=[matrix([[tex(x)] for x in row]) for row in choices]
            exprs=[_value_expr(x) for x in values]
            if _max_coefficient([x for row in exprs for x in row])>WORKLOAD[level]['collected']:
                if parameters is not None:raise ValueError('Displayed bank exceeds '+level+' workload caps')
                continue
            invalid=any(_equal(a,b) for i,a in enumerate(exprs) for b in exprs[:i]) or sum(_equal(a,tuple(answer)) for a in exprs)!=1
            if invalid:
                if parameters is not None:raise ValueError('Complete bank is ambiguous')
                continue
        break
    else:raise ValueError('No eligible instance')
    inputs=[matrix([[tex(c) for c in row] for row in M]),matrix([[tex(x)] for x in V])]
    prompt=t['prompt_mask']
    for i,x in enumerate(inputs):prompt=prompt.replace('@@M'+str(i)+'@@',x)
    dot=matrix([[ '+'.join(group(a)+r'\cdot '+group(b) for a,b in zip(row,V))] for row in M])
    evaluated=matrix([[summed(row)] for row in products]);final=matrix([[tex(x)] for x in answer])
    stages=inputs+[dot]+([evaluated] if len(t['solution_matrices'])==5 else [])+[final]
    if t['missing_solution']:
        stages=inputs+[dot,final]
        solution='We multiply each row in the matrix by the column vector using the dot product:\n\n$$\n'+r'\begin{aligned}Ax & ='+inputs[0]+inputs[1]+r' \\ & ='+dot+r' \\ & ='+final+r'\end{aligned}'+'\n$$'
    else:
        solution=t['solution_mask']
        for i,x in enumerate(stages):solution=solution.replace('@@M'+str(i)+'@@',x)
    prompt=mf.normalize_prose(prompt);solution=mf.normalize_prose(solution)
    guarded({'prompt':prompt,'solution':solution})
    # Full banks are normalized before identity; display order is excluded.
    fields=[]
    for f in t['fields']:
        if f['type']=='radio':bank=values;correct=next(i for i,v in enumerate(values) if _equal(_value_expr(v),tuple(answer)))
        else:
            idx=int(f['key'].split('-')[-1])-1;bank=[tex(answer[idx])];correct=0
        guarded(bank)
        identity={'key':f['key'],'type':f['type'],'values':sorted(bank),'correct':bank[correct]}
        fid=uid('field',identity)
        choices=[{':answer/id':uid('answer',{'field':fid,'value':v}),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
        correct_ref=[':answer/id',choices[correct][':answer/id']]
        if f['type']=='radio':rng.shuffle(choices)
        fields.append({':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':':answer-field.type/'+f['type'],':answer-field/choices':choices,':answer-field/correct':correct_ref})
    content={'version':VERSION,'prompt':prompt,'solution':solution,'fields':[{k:(sorted(v,key=lambda z:z[':answer/value']) if k==':answer-field/choices' else v) for k,v in f.items()} for f in fields]}
    # Mathematical fingerprint excludes labels, bank, seed and variable spelling.
    canon={S.Symbol(p['names'][v]):S.Symbol('v'+str(i)) for i,v in enumerate(t['variables'])}
    mathkey={'matrix':[[S.srepr(S.expand((x if V[j]!=0 else S.Integer(0)).xreplace(canon))) for j,x in enumerate(row)] for row in M],'vector':[S.srepr(S.expand(x.xreplace(canon))) for x in V]}
    question={':question/id':uid('question',content),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields}
    result={'knowledge_point':dict(KP),'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'mathematical_fingerprint':digest(mathkey),'source_ids':[template],'source_basis':2275,'authored_level':t['source_level'] is None,'repairs':(['missing correct designation inferred by matrix multiplication','missing worked solution authored from canonical example'] if t['missing_correct'] else []),'workload_caps':WORKLOAD[level],'scope':'same row-dot-product method; fixed matrix/vector roles and stage workload','bank_interpretation':('observed expression patterns; learner intent unverified' if profile=='observed' else 'authored complete row-operation bank')}}
    guarded(result)
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    out=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
    if a.format=='json':print(json.dumps(out,indent=2))
    else:
        for r in out:
            q=r['question'];print(q[':question/problem'])
            for f in q[':question/answer-fields']:
                print('\n'+f[':answer-field/key']+': '+', '.join('$'+x[':answer/value']+'$' for x in f[':answer-field/choices']))
            print('\n'+q[':question/worked-solution']+'\n')
if __name__=='__main__':main()
