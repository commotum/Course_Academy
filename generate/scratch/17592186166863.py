#!/usr/bin/env python3
"""Moderate conservative-field triples; faithful source structures, exact pullbacks.
Each field independently substitutes X=u*x,Y=v*y and uses (u*P(X,Y),v*Q(X,Y)).
Signed coordinate scalings preserve smoothness, conservativity, function nesting
and the two-partial-derivative comparison. No plots or new reasoning stages.
"""
import argparse,hashlib,json,random,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186166863
KP_UUID='65adbd80-9647-59d8-bd4a-42f431587c85'
TITLE='Identifying Conservative Vector Fields'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'conservative-vector-fields-generator-v1'))
VERSION='1.0.0'
HERE=Path(__file__).with_suffix('')
SOURCES=json.loads((HERE/'source-components.json').read_text())
PROFILES=tuple(SOURCES)
SUPPORTED_LEVELS=('moderate',)
SCALES=(-2,-1,1,2)
KEYS=('I','II','III')
x,y=sp.symbols('x y',real=True)
def expr(s):return sp.sympify(s,locals={'x':x,'y':y})
def base(profile):return [(expr(p),expr(q)) for p,q in SOURCES[profile]['pairs']]
def pairs(profile,scales):
 assert len(scales)==3 and all(len(p)==2 and all(k in SCALES for k in p) for p in scales)
 return [(sp.expand_mul(u*p.subs({x:u*x,y:v*y},simultaneous=True)),sp.expand_mul(v*q.subs({x:u*x,y:v*y},simultaneous=True))) for (p,q),(u,v) in zip(base(profile),scales)]
def canonical_pair(p,q):
 # Uniform field multiples and choice/field order do not make a new task.
 terms=sp.Add.make_args(sp.expand(p))+sp.Add.make_args(sp.expand(q))
 coeff=[t.as_coeff_Mul()[0] for t in terms if t!=0]
 scale=sp.gcd_list(coeff)
 if scale==0:scale=1
 p,q=sp.simplify(p/scale),sp.simplify(q/scale)
 a=(sp.srepr(p),sp.srepr(q));b=(sp.srepr(-p),sp.srepr(-q))
 return min(a,b)
def fingerprint_pairs(fields):
 normalized=sorted(canonical_pair(p,q) for p,q in fields)
 return hashlib.sha256(json.dumps(normalized).encode()).hexdigest()
def generate(difficulty='moderate',seed=0,template=None,parameters=None,bank_profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty '+difficulty+'; no source evidence')
 rng=random.Random(seed);profile=bank_profile or template or rng.choice(PROFILES)
 if profile not in SOURCES:raise ValueError('Unknown source structure')
 parameters=parameters or {'scales':[[rng.choice(SCALES),rng.choice(SCALES)] for _ in range(3)]}
 parameters=json.loads(json.dumps(parameters));fields=pairs(profile,parameters['scales'])
 truth=[sp.simplify(sp.diff(p,y)-sp.diff(q,x))==0 for p,q in fields]
 assert truth==SOURCES[profile]['truth']
 heading='Which of the following vector fields are conservative '+('in their respective domains?' if profile=='q-104582' else r'on $\mathbb R^{2}?$')
 prompt=heading+'\n\nSelect all that apply.\n\n'
 for key,name,(p,q) in zip(KEYS,'FGH',fields):
  prompt+='- **'+key+'.** $'+name+('(x,y)' if profile=='q-81460' else '')+'=('+sp.latex(p)+r')\,i+('+sp.latex(q)+r')\,j$'+'\n'
 prompt=prompt.rstrip()
 solution=r'Let $F(x,y)=P(x,y)\,i+Q(x,y)\,j$ be a vector field with domain $D=\mathbb R^{2},$ where $P$ and $Q$ have continuous first-order partial derivatives everywhere on $D.$ Then, we have the following theorem:'+'\n\n'+r'$F$ *is conservative if and only if $\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}$ everywhere on $D.$*'+'\n\n'+r"Note that for each of our functions, $D=\mathbb R^{2}.$ With this in mind, let's check each of the vector fields."
 for name,(p,q),yes in zip('FGH',fields,truth):
  a,b=sp.diff(p,y),sp.diff(q,x)
  solution+='\n\n- For the vector field $'+name+',$ we have $P='+sp.latex(p)+'$ and $Q='+sp.latex(q)+'$. Computing the partial derivatives, we get\n\n$$\n'+r'\frac{\partial P}{\partial y}='+sp.latex(a)+r',\qquad \frac{\partial Q}{\partial x}='+sp.latex(b)+'.\n$$\n\n'
  solution+=(r'Since the partial derivatives are continuous and equal everywhere on $\mathbb R^{2},$ we conclude that $'+name+r'$ is conservative on $\mathbb R^{2}.$' if yes else r'Since the partial derivatives are not equal everywhere, we conclude that $'+name+r'$ is not conservative on $\mathbb R^{2}.$')
 selected=[key for key,yes in zip(KEYS,truth) if yes]
 conclusion=(', '.join(selected[:-1])+', and '+selected[-1] if len(selected)==3 else ' and '.join(selected))+(' only' if len(selected)<3 else '')
 solution+='\n\nTherefore, the correct answer is "'+conclusion+'."'
 fp=fingerprint_pairs(fields);qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),fp));banks=[]
 for key,yes in zip(KEYS,truth):
  fid=str(uuid.uuid5(uuid.UUID(qid),key));answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
  banks.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[int(yes)][':answer/id']]})
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':banks}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':profile,'bank_profile':'three-field-owned-booleans','source':profile,'source_db_id':SOURCES[profile]['source_db_id'],'parameters':parameters,'domain':'R^2; C1 globally','parameter_fingerprint':fp,'generator_id':GENERATOR_UUID,'sympy_version':sp.__version__}}
def batch(difficulty,count,seed):return [generate(difficulty,seed+i,template=PROFILES[i%len(PROFILES)]) for i in range(count)]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+q[':question/worked-solution']

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='moderate');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args();rows=batch(a.difficulty,a.count,a.seed);print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
