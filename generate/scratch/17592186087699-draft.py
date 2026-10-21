#!/usr/bin/env python3
"""Direct verification of inverse 2x2 matrices, steps 3–7 review draft.

The supplied objects are matrices, never augmented matrices. Learners verify
products; no determinant/adjugate or row-reduction method is introduced.
Source masks hold complete prose and ordered product stages, with whole-matrix
and nonidentity-witness slots. Original incomplete records have public, explicitly
ineligible raw-source profiles. No numeric generator import or database access.
"""
import sys
sys.dont_write_bytecode=True
import argparse,copy,functools,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_tex,normalize_prose,checked_math_content
HERE=Path(__file__).with_suffix('')
KP_ID=17592186087699
KP_UUID='9b9ef325-2358-5041-8a8d-b459e8ed9f09'
TITLE='Determining the Inverse of a 2x2 Matrix'
VERSION='1.0.0-draft'
SUPPORTED_LEVELS=('easy','moderate','hard')
TEMPLATES=json.loads((HERE/'templates.json').read_text())
DEFAULT_TEMPLATES=tuple(k for k,v in TEMPLATES.items() if not v['canonical'])
PROFILES=('observed','raw-source')
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)

def scalar(s):
    if not isinstance(s,str):raise ValueError('Exact entries must be strings')
    s=s.strip().replace('−','-')
    s=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(-?\d+)\}',r'(\1)/(\2)',s)
    if not re.fullmatch(r'[-+\d()/ ]+',s):raise ValueError('Only rational entries are permitted')
    v=sp.sympify(s)
    if not v.is_Rational:raise ValueError('Rational entry required')
    return v

def read_matrix(body,stars=False):
    rows=[[x.strip() for x in row.split('&')] for row in body.split('\\\\')]
    if len(rows)!=2 or any(len(r)!=2 for r in rows):raise ValueError('Exactly 2x2')
    return [[None if stars and x=='∗' else scalar(x) for x in row] for row in rows]

def matrices_from_prompt(prompt):
    return {m[1]:sp.Matrix(read_matrix(m[2])) for m in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',prompt,re.S)}

def tex_matrix(m):return matrix_tex([[sp.latex(m[i,j]).replace('- '+chr(92),'-'+chr(92)) for j in range(2)] for i in range(2)],augmented=False)
def serial_matrix(m):return [[str(m[i,j]) for j in range(2)] for i in range(2)]
def uid(scope,text):return str(uuid.uuid5(uuid.UUID(scope),text))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def original_parameters(template):
    t=TEMPLATES[template]
    return {'matrices':[[[str(scalar(v)) for v in row] for row in m] for m in t['original_matrices']], 'witnesses':[b['witness'] for b in t['blocks']]}

def relations(t):
    # Mathematical role graph; q11637's second pair shares the middle matrix.
    if t['canonical']:return [(0,1)]
    return [(0,1),(1,2) if t['source_id']=='q-11637' else (0,2)]

def truth(mats,t):
    labels=t['labels'];out=[mats[a]*mats[b]==sp.eye(2) and mats[b]*mats[a]==sp.eye(2) for a,b in relations(t)]
    if t['canonical']:return out
    third=re.findall(r'(?<!\$)\$(?!\$)([^$]+)(?<!\$)\$(?!\$)',t['prompt_mask'])[-1]
    left=re.search(r'([A-Z])\s*(?:=|\\ne)',third)[1]
    right=re.search(r'\{?([A-Z])\}?\^',third)[1]
    a,b=mats[labels.index(left)],mats[labels.index(right)]
    eq=a*b==sp.eye(2) and b*a==sp.eye(2)
    out.append(not eq if r'\ne' in third else eq)
    return out

def expected_truth(t):
    return truth([sp.Matrix([[scalar(v) for v in r] for r in m]) for m in t['original_matrices']],t)

def selected_words(values):
    names=[v for v,yes in zip(('I','II','III'),values) if yes]
    return (' and '.join(names)+' only') if names else 'None'

def validate_parameters(p,t,level,profile):
    if not isinstance(p,dict) or set(p)!={'matrices','witnesses'}:raise ValueError('Exactly matrices and witnesses required')
    if len(p['matrices'])!=len(t['labels']):raise ValueError('Wrong matrix-slot count')
    mats=[]
    for rows in p['matrices']:
        if len(rows)!=2 or any(len(r)!=2 for r in rows):raise ValueError('All supplied objects must be 2x2 matrices')
        m=sp.Matrix([[scalar(x) for x in r] for r in rows]);mats.append(m)
        if any(abs(x)>4 or x.q>12 for x in m):raise ValueError('Source-shaped arithmetic ceiling: absolute value <=4, denominator <=12')
    if truth(mats,t)!=expected_truth(t):raise ValueError('Source profile requires its complete truth-role pattern')
    if len(p['witnesses'])!=len(t['blocks']):raise ValueError('One witness slot per product stage')
    for b,w in zip(t['blocks'],p['witnesses']):
        product=mats[b['pair'][0]]*mats[b['pair'][1]]
        if b['identity']:
            if w is not None or product!=sp.eye(2):raise ValueError('Identity stage must retain identity result')
        elif type(w) is not int or not 0<=w<4 or product[w//2,w%2]==sp.eye(2)[w//2,w%2]:raise ValueError('A witness must differ from the corresponding identity entry')
    if profile!='raw-source':
        if level=='easy':
            if any(x.q>3 for m in mats for x in m) or any(x.q!=1 for x in mats[0]):raise ValueError('Easy: integral first matrix; denominator <=3')
        elif level=='moderate':
            if any(x==0 for x in mats[0]) or any(x.q!=1 for x in mats[0]) or sum(x.q==4 for m in mats for x in m)<2 or any(x.q>4 for m in mats for x in m):raise ValueError('Moderate: dense integer first matrix and at least two reduced quarter entries; denominators <=4')
        else:
            if any(x==0 for m in mats for x in m) or sum(x.q>1 for x in mats[0])<2 or sum(x.q>1 for m in mats for x in m)<5 or any(x.q>6 for m in mats for x in m):raise ValueError('Hard: dense rational matrices, >=2 fractional first-matrix entries and >=5 total; denominators <=6')
    return mats

def sample_parameters(t,level,rng):
    # Pick the complete supplied-candidate construction before coefficients.
    # This is object generation, not a learner inversion procedure/distractor bank.
    recipe=rng.choice(('flip-entry','omit-scale','transpose'))
    target=expected_truth(t)
    for _ in range(5000):
        vals=[sp.Rational(rng.randint(-3,3),rng.choice((2,3))) if level=='hard' else sp.Integer(rng.randint(-3,3)) for _ in range(4)]
        a=sp.Matrix(2,2,vals)
        if not a.det():continue
        good=a.inv();bad=good.copy()
        if recipe=='flip-entry':
            i=rng.randrange(4);bad[i]=-bad[i]
        elif recipe=='omit-scale':bad=good*a.det()
        else:bad=good.T
        if bad==good:continue
        if t['canonical']:mats=[a,good]
        elif t['source_id']=='q-11637':mats=[a,good,bad]
        else:mats=[a,good if target[0] else bad,good if target[1] else bad]
        witnesses=[]
        for b in t['blocks']:
            prod=mats[b['pair'][0]]*mats[b['pair'][1]]
            candidates=[i for i in range(4) if prod[i]!=sp.eye(2)[i]]
            witnesses.append(None if b['identity'] else (rng.choice(candidates) if candidates else 0))
        p={'matrices':[serial_matrix(m) for m in mats],'witnesses':witnesses}
        try:validate_parameters(p,t,level,'observed')
        except ValueError:continue
        return p
    raise ValueError('Complete source role profile has no sampled eligible instance')

def render_masks(t,mats,witnesses,raw=False):
    replacements={f'@@M{i}@@':tex_matrix(m) for i,m in enumerate(mats)}
    for i,(b,w) in enumerate(zip(t['blocks'],witnesses)):
        prod=mats[b['pair'][0]]*mats[b['pair'][1]]
        replacements[f'@@P{i}@@']=tex_matrix(prod) if w is None else matrix_tex([[sp.latex(prod[r,c]).replace('- '+chr(92),'-'+chr(92)) if r*2+c==w else '∗' for c in range(2)] for r in range(2)],augmented=False)
    def fill(mask):
        if mask is None:return None
        for key,value in replacements.items():mask=mask.replace(key,value)
        return normalize_prose(mask)
    prompt,solution=fill(t['prompt_mask']),fill(t['solution_mask'])
    if t['canonical'] and not raw:
        prompt=normalize_prose('Using the method of direct verification, determine whether the matrix $B$ is the inverse of $A,$ where\n\n$$\nA='+tex_matrix(mats[0])+r',\,B='+tex_matrix(mats[1])+'.\n$$')
    if solution is None and not raw:
        # Missing historical explanation: independently authored completion using
        # the same verification stages as the other original practice records.
        a,b,c=t['labels'];blocks=[]
        for x,y in ((a,b),(a,c),(c,a)):
            prod=mats[t['labels'].index(x)]*mats[t['labels'].index(y)]
            blocks.append('Computing $'+x+y+'$, we get\n\n$$\n'+r'\begin{aligned}'+x+y+' & ='+tex_matrix(mats[t['labels'].index(x)])+tex_matrix(mats[t['labels'].index(y)])+r' \\ & ='+tex_matrix(prod)+r'\end{aligned}'+'\n$$')
        solution=normalize_prose('We must check whether each pair multiplies to $I_2$.\n\n'+'\n\n'.join(blocks)+'\n\nTherefore, the correct answer is "'+selected_words(truth(mats,t))+'".')
    return prompt,solution

def fingerprint(prompt,t,mats):
    # Labels/TeX spellings, witness choices, bank profiles and presentation are
    # incidental. Complete rational matrices and ordered relation roles matter.
    return digest({'objects':[serial_matrix(m) for m in mats],'pairs':relations(t),'third':None if t['canonical'] else [re.findall(r'(?<!\$)\$(?!\$)([^$]+)(?<!\$)\$(?!\$)',t['prompt_mask'])[-1].replace(' ','').replace('{','').replace('}','').translate(str.maketrans(dict(zip(t['labels'],'XYZ'))))]})

def preserve_raw_attribute_absence(fn):
    """Shared formatting validation predates optional source explanations.

    Validate an empty placeholder, then remove it from raw public evidence so
    the captured key-presence contract remains exact. Normal output is complete.
    """
    @functools.wraps(fn)
    def call(*args,**kwargs):
        record=fn(*args,**kwargs)
        g=record['generation']
        if g['profile']=='raw-source' and not TEMPLATES[g['template']]['has_solution']:
            record['question'].pop(':question/worked-solution')
        return record
    return call

@preserve_raw_attribute_absence
@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
    if type(seed) is not int:raise ValueError('seed must be an integer')
    if template is not None and template not in TEMPLATES:raise ValueError('Unknown template')
    if profile is not None and profile not in PROFILES:raise ValueError('Unknown profile')
    rng=random.Random(seed)
    allowed_fields=('radio','checkbox',':answer-field.type/radio',':answer-field.type/checkbox')
    if field_type is not None and field_type not in allowed_fields:raise ValueError('Unsupported field type')
    eligible=DEFAULT_TEMPLATES if field_type is None else tuple(k for k in DEFAULT_TEMPLATES if any(f['type'].split('/')[-1]==field_type.split('/')[-1] for f in TEMPLATES[k]['fields']))
    template=template or rng.choice(eligible);t=TEMPLATES[template];profile=profile or 'observed';raw=profile=='raw-source'
    types={f['type'].split('/')[-1] for f in t['fields']}
    if field_type is not None and (len(types)!=1 or field_type.lstrip(':').split('/')[-1] not in types):raise ValueError('Unsupported field type')
    if raw and parameters is None:parameters=original_parameters(template)
    p=copy.deepcopy(parameters) if parameters is not None else sample_parameters(t,level,rng)
    mats=validate_parameters(p,t,level,profile);values=truth(mats,t)
    prompt,solution=render_masks(t,mats,p['witnesses'],raw)
    bank=[]
    for i,f in enumerate(t['fields']):
        correct=f['correct'] if raw else (selected_words(values) if f['type'].endswith('/radio') else str(values[i]).lower())
        bank.append({'key':f['key'],'type':f['type'],'choices':f['choices'],'correct':correct})
    # Identities use normalized displayed content before ordering; no seed,
    # template alias or raw parameter spelling can affect content identity.
    identity={'version':VERSION,'prompt':prompt,'solution':solution,'banks':bank,'difficulty':level if (not raw or t['has_difficulty']) else None}
    qid=uid(KP_UUID,digest(identity));q={':question/id':qid,':question/problem':prompt}
    if not raw or t['has_difficulty']:q[':question/difficulty']=':question.difficulty/'+level
    q[':question/worked-solution']=solution or ''
    if t['has_fields']:
        fields=[]
        for f in bank:
            fid=uid(qid,'field:'+f['key']);answers=[];correctid=None
            for a in f['choices']:
                aid=uid(fid,a['type']+':'+a['value']);answers.append({':answer/id':aid,':answer/type':a['type'],':answer/value':a['value']})
                if a['value']==f['correct']:correctid=aid
            rng.shuffle(answers)
            field={':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':f['type'],':answer-field/choices':answers}
            if correctid is not None:field[':answer-field/correct']=[':answer/id',correctid]
            fields.append(field)
        q[':question/answer-fields']=fields
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'difficulty':level,'seed':seed,'template':template,'profile':profile,'parameters':p,'mathematical_fingerprint':fingerprint(prompt,t,mats),'evidence_only':raw or t['canonical'],'eligible_for_learning':not raw and not t['canonical'],'source_id':template,'basis':2275,'python':sys.version.split()[0],'sympy':sp.__version__,'plots':'none'}}

# Easy: observed labels, integer first matrix, small familiar rational candidates.
def generate_easy(seed=0,**kwargs):return generate('easy',seed=seed,**kwargs)
# Moderate: authored uncalibrated arithmetic placement, same direct checks.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed=seed,**kwargs)
# Hard: authored uncalibrated rational bookkeeping, same direct checks.
def generate_hard(seed=0,**kwargs):return generate('hard',seed=seed,**kwargs)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('json','markdown'),default='json');parser.add_argument('--template',choices=tuple(TEMPLATES));parser.add_argument('--profile',choices=PROFILES)
    args=parser.parse_args()
    if args.count<1:parser.error('--count must be positive')
    levels=SUPPORTED_LEVELS if args.difficulty=='all' else (args.difficulty,)
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    if args.format=='json':print(json.dumps(records if args.difficulty=='all' or args.count!=1 else records[0],indent=2))
    else:
        for r in records:
            q=r['question'];print(q[':question/problem']);print('\n'+q.get(':question/worked-solution','[Absent in captured source]'))
            for f in q.get(':question/answer-fields',[]):print('\n'+f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':main()
