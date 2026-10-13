"""Normal-line two-blank generators; exact arithmetic, no plots.

Moderate only. Complete source blank banks are preserved. Radio profiles and
context-dependent fragments are explicitly excluded from this bounded version.
"""
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as s
H=Path(__file__).with_suffix('');C=json.loads((H/'contract.json').read_text())
NAMESPACE=uuid.UUID(C['kp_uuid']);GENERATOR_ID=C['generator_id'];VERSION='1.0.0'
x=s.Symbol('x',positive=True)
CONFIG=C['profiles']
def latex(v):return s.latex(s.simplify(v))
def semantic_key(expr,point):return 'normal:'+str(s.expand(expr))+':at:'+str(s.Rational(point))
def generate(level,seed=0,profile=None,parameters=None):
 if level!='moderate':raise ValueError('Only moderate has verified source evidence')
 rng=random.Random(seed);profile=profile or rng.choice(list(CONFIG));c=CONFIG[profile]
 p=parameters or {'scale':rng.randint(1,30),'point':rng.choice(c['points'])}
 scale=s.Rational(p['scale']);point=s.Rational(p['point']);assert 1<=scale<=30 and str(point) in c['points']
 expr=scale*s.sympify(c['expression'],locals={'x':x});y=s.simplify(expr.subs(x,point));m=s.simplify(s.diff(expr,x).subs(x,point));assert m and s.sign(m)==c['sign']
 L=s.Integer(c['x_coefficient']);A=abs(L*m);B=s.simplify(L*(point+m*y));normal=-1/m
 key=semantic_key(expr,point);qid=str(uuid.uuid5(NAMESPACE,key));fields=[]
 for i,v in enumerate([A,B],1):
  fid=str(uuid.uuid5(uuid.UUID(qid),'field-'+str(i)));aid=str(uuid.uuid5(uuid.UUID(fid),latex(v)))
  fields.append({':answer-field/id':fid,':answer-field/key':'field-'+str(i),':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':latex(v)}],':answer-field/correct':[':answer/id',aid]})
 original=scale==1 and point==s.Rational(c['point'])
 expr_text=c['expression_latex'] if original else latex(expr);point_text=c['point_latex'] if original else latex(point);y_text=c['y_latex'] if original else latex(y)
 problem=c['prompt'].replace(c['expression_latex'],expr_text).replace(c['point_pair'],f'({point_text},{y_text})')
 sign='+' if m>0 else '-';lx='x' if L==1 else str(L)+'x'
 solution=(rf'Let $f(x)={expr_text}.$ First, we compute the derivative:'+'\n\n$$\n'+rf"f'(x)=\frac{{\text{{d}}}}{{\text{{d}}x}}\left({expr_text}\right)={latex(s.diff(expr,x))}"+'\n$$\n\n'+
 rf'Then, we compute the slope of the tangent at the point $({point_text},{y_text}):$'+'\n\n$$\n'+rf"m=f'({point_text})={latex(m)}"+'\n$$\n\nTherefore, the slope of the normal line is\n\n$$\n'+rf"m'=-\frac{{1}}{{m}}={latex(normal)}."+'\n$$\n\nFinally, the equation of the normal line is\n\n$$\n'+rf'\begin{{aligned}}y-\left({y_text}\right)&={latex(normal)}\left(x-\left({point_text}\right)\right) \\ {lx}{sign}{latex(A)}\cdot y&={latex(B)}.\end{{aligned}}'+'\n$$')
 return {'knowledge_point':{'id':C['kp_uuid'],'db_id':C['kp'],'title':C['title']},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':fields},'generation':{'generator_id':GENERATOR_ID,'version':VERSION,'template':c['template'],'profile':profile,'seed':seed,'parameters':{'scale':str(scale),'point':str(point)},'expression':str(expr),'point':str(point),'mathematical_key':key,'domain':'x>0 for reciprocal and radical families; sampled polynomial points positive, plus observed zero','source_references':[profile],'dependencies':{'sympy':s.__version__},'plots':[]}}
def candidates(level):
 if level!='moderate':raise ValueError('Unsupported difficulty: '+level)
 return [(sid,{'scale':str(k),'point':pt}) for sid,c in CONFIG.items() for k in range(1,31) for pt in c['points']]
def main():
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');z=a.parse_args();cs=candidates(z.difficulty);random.Random(z.seed).shuffle(cs);out=[];seen=set()
 for sid,p in cs:
  r=generate(z.difficulty,z.seed,profile=sid,parameters=p);key=r['generation']['mathematical_key']
  if key in seen:continue
  seen.add(key);out.append(r)
  if len(out)==z.count:break
 if z.count<1 or len(out)<z.count:raise ValueError('Bounded finite distinct capacity exceeded')
 print(json.dumps(out,indent=2) if z.format=='json' else '\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in out))
if __name__=='__main__':main()
