"""Unit-vector normalization, bounded source-bank extensions; no seed-only variants.

Hard combines vectors as in rated q-125138, with the complete q-17709 bank.
Its missing source field is an explicit authored completion, not a source replay.
Moderate uses the complete rated q-125135 profile. Easy remains unsupported.
"""
import argparse, hashlib, json, math, os, random, sys, uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    python = Path(__file__).resolve().parents[2]/'.venv/bin/python'
    os.execv(str(python), [str(python), __file__, *sys.argv[1:]])
KP_ID=17592186059716
KP_UUID='9c45a70b-273c-5fec-a768-40a1cf218628'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
SUPPORTED_LEVELS=('moderate','hard')
VERSION='unit-vector-bounded-1'
HERE=Path(__file__).with_suffix('')
CATALOG=[(5,12,2),(8,-6,3),(3,8,1),(5,4,2),(7,24,3),(-8,15,2),(20,-21,-2),(9,40,1),(-12,-5,-1),(4,-7,-3),(11,6,2),(2,9,-2)]

def matrix(x,y):return r'\begin{bmatrix}'+sp.latex(x)+r' \\ '+sp.latex(y)+r'\end{bmatrix}'

def direction(x,y):
    d=math.gcd(int(x),int(y));return (int(x)//d,int(y)//d)

def fingerprint_xy(x,y):
    return hashlib.sha256(('oriented-unit-direction:'+str(direction(x,y))).encode()).hexdigest()

def bank(profile,x,y):
    x,y=sp.Integer(x),sp.Integer(y);s=x*x+y*y;n=sp.sqrt(s)
    if profile=='q-17709':return [(x/n,-y/n),(x,y),(x/n,y/(3*n)),(x/n,y/n),(x/(2*n),y/n)],3
    if profile=='q-125135':return [(x/(2*n),y/(2*n)),(x/sp.sqrt(n/2),y/sp.sqrt(n/2)),(x/n,y/n),(x/sp.sqrt(n),y/sp.sqrt(n)),(x/(4*n),y/(2*n))],2
    if profile=='q-18058':return [(sp.Integer(1)/n,x/n),(x/sp.sqrt(s+4),y/sp.sqrt(s+4)),(y/n,x/n),(x/n,y/n),(x/sp.sqrt(s+3),y/sp.sqrt(s+3))],3
    raise ValueError(profile)

def generate(level,x,y,t,seed=0):
    assert level in SUPPORTED_LEVELS and (x,y,t) in CATALOG
    assert level=='hard' or math.isqrt(x*x+y*y)**2==x*x+y*y, 'Moderate restricted to observed integer-length profile'
    profile='q-17709' if level=='hard' else 'q-125135'
    values,correct=bank(profile,x,y);n=sp.sqrt(x*x+y*y)
    a=(0,t);b=(x,y-2*t)
    target='2a+b' if level=='hard' else 'b'
    problem=(f'Let $a={matrix(*a)}$ and $b={matrix(*b)}$.' if level=='hard' else f'Let $b={matrix(x,y)}$.')+f' Find a unit vector that is parallel to ${target}$ and points the same direction.'
    solution='Remember that to find a unit vector that is parallel to a given vector and points the same direction, we need to divide the given vector by its length:\n\n'+f'$$\nu=\\frac{{{target}}}{{|{target}|}}\n$$'
    if level=='hard':
        solution+=f"\n\nFirst, let's compute the sum:\n\n$$\n\\begin{{aligned}}\n2a+b &= 2\\cdot {matrix(*a)}+{matrix(*b)} \\\\\n&= {matrix(0,2*t)}+{matrix(*b)} \\\\\n&= \\begin{{bmatrix}}0+({x}) \\\\ ({2*t})+({b[1]})\\end{{bmatrix}} \\\\\n&= {matrix(x,y)}\n\\end{{aligned}}\n$$"
    square_step=f'&= \\sqrt{{{x*x}+{y*y}}} \\\\\n' if level=='moderate' else ''
    solution+=f'\n\nUsing the formula for the magnitude of a vector, we get\n\n$$\n\\begin{{aligned}}\n|{target}| &= \\sqrt{{({x})^2+({y})^2}} \\\\\n'+square_step+f'&= \\sqrt{{{x*x+y*y}}} \\\\\n&= {sp.latex(n)}\n\\end{{aligned}}\n$$'
    solution+=f'\n\nFinally, we divide ${target}$ by its length and get the following unit vector:\n\n$$\n\\begin{{aligned}}\nu &= \\frac{{{target}}}{{|{target}|}} \\\\\n&= \\frac{{1}}{{{sp.latex(n)}}}\\cdot ({target}) \\\\\n&= \\frac{{1}}{{{sp.latex(n)}}}\\cdot {matrix(x,y)} \\\\\n&= {matrix(*values[correct])}\n\\end{{aligned}}\n$$'
    fp=fingerprint_xy(x,y)
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+':'+level+':'+fp));fid=str(uuid.uuid5(uuid.UUID(qid),'field:selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'recipe:'+str(i))),':answer/type':':answer.type/math',':answer/value':matrix(*v)} for i,v in enumerate(values)]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Calculating a Unit Vector Parallel to a Given Vector'},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/requires-calculator':False,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct][':answer/id']]}]},'generation':{'version':VERSION,'template':'combination' if level=='hard' else 'direct','bank_profile':profile,'parameters':{'x':x,'y':y,'t':t},'seed':seed,'parameter_fingerprint':fp,'source_ids':['q-125138','q-17709'] if level=='hard' else ['q-125135'],'authored_completion':'Hard source field absent; explicit five-choice completion using full observed combination bank. Source records unchanged.' if level=='hard' else 'Generalization of rated direct-vector bank.','domains':'Nonzero integer components; finite catalog; exact normalization; oriented primitive directions deduplicated','dependencies':{'sympy':sp.__version__},'assets':[]}}

def batch(difficulty,count,seed):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    params=[p for p in CATALOG if difficulty=='hard' or math.isqrt(p[0]**2+p[1]**2)**2==p[0]**2+p[1]**2];random.Random(seed).shuffle(params)
    return [generate(difficulty,*p,seed) for p in params[:min(count,len(params))]]

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='hard');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
    if a.count<1:p.error('count must be positive')
    records=batch(a.difficulty,a.count,a.seed)
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
