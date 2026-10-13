"""Bounded source-bank-preserving frequency transports for trig integration.

r=1 is source replay; stock uses r=2..6. Difficulty/field/layout profiles stay
separate. Domain exclusions come from the original quotient, before cancellation.
"""
import functools,argparse,hashlib,json,random,sys,uuid,os,re
from pathlib import Path
try:import sympy as sp
except ImportError:
 if __name__=='__main__':
  runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python';os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
HERE=Path(__file__).with_suffix('');sys.path.insert(0,str(HERE));import printed as p
SOURCE=json.loads((HERE/'source.json').read_text());KP_ID=17592186064226;KP_UUID=SOURCE['kp'][':knowledge-point/id'];TITLE=SOURCE['kp'][':knowledge-point/title']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'));VERSION='trig-quotient-frequency-1';SUPPORTED_LEVELS=('easy','moderate');x=p.x
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['kp'][':knowledge-point/questions']}
PRIMITIVES={'q-49273':sp.sin(x)-sp.cot(x),'q-49275':sp.tan(x)/8,'q-114306':3*sp.sec(x),'q-114313':sp.sin(x)+sp.csc(x),'q-114318':-sp.csc(x),'q-352848':sp.tan(x),'q-352853':sp.sin(x)-sp.cos(x),'q-352858':sp.sin(4*x)/4,'q-352867':sp.sin(5*x)/5,'q-352868':-sp.cos(4*x)/4,'q-49284':sp.sec(x),'q-73361':sp.sin(x)-sp.cos(x),'q-74279':-sp.csc(4*x)/4,'q-74281':sp.cot(x),'q-114308':sp.tan(x)+sp.cos(x),'q-73365':sp.tan(x),'q-352711':sp.sec(x),'q-114319':-sp.cos(x)}
def level(t):return SOURCES[t][':question/difficulty'][':db/ident'].split('/')[-1]
def fingerprint(q):return task_fingerprint(q[':question/problem'])
@functools.lru_cache(maxsize=2000)
def task_fingerprint(problem):
 expr,lo,hi=p.integral(problem)
 # Exact reduced integrand and bounds ignore bank, field type, identity and order.
 expr=sp.trigsimp(expr.rewrite(sp.sin))
 return hashlib.sha256(json.dumps([sp.srepr(expr),None if lo is None else sp.srepr(lo),None if hi is None else sp.srepr(hi)]).encode()).hexdigest()
def generate(difficulty,seed=0,template=None,parameters=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported level '+difficulty)
 rng=random.Random(seed);template=template or rng.choice([t for t in SOURCES if level(t)==difficulty]);parameters=parameters or {'r':rng.randint(2,6)};r=parameters['r']
 if template not in SOURCES or level(template)!=difficulty or type(r)is not int or not 1<=r<=6:raise ValueError('Unsupported template/parameters')
 old=SOURCES[template];of=old[':question/answer-fields'][0];expr,lo,hi=p.integral(old[':question/problem']);primitive=PRIMITIVES[template]
 integral=expr.subs(x,r*x);a=None if lo is None else lo/r;b=None if hi is None else hi/r
 anti=primitive.subs(x,r*x)/r
 correct=anti+p.C if a is None else sp.simplify(anti.subs(x,b)-sp.limit(anti,x,a,dir='+'))
 original=[p.scalar(z[':answer/value'])for z in of[':answer-field/choices']]
 bank=[z.subs(p.C,0).subs(x,r*x)/r+(p.C if a is None else 0)for z in original]
 chosen=[i for i,z in enumerate(bank)if p.same(z,correct)];assert len(chosen)==1
 assert all(not p.same(z,w)for i,z in enumerate(bank)for w in bank[i+1:])
 if r==1:prompt=old[':question/problem'];solution=old[':question/worked-solution'];values=[z[':answer/value']for z in of[':answer-field/choices']]
 else:
  sign=r'\int' if a is None else r'\int_{'+sp.latex(a)+'}^{'+sp.latex(b)+'}'
  body=sign+' '+sp.latex(integral)+r'\,\text{d}x'
  if of[':answer-field/type'][':db/ident'].endswith('/blank'):prompt='Evaluate the following integral. Do not round the answer.\n\n$'+body+'=$\n{{'+of[':answer-field/key']+'}}'
  elif old[':question/problem'].startswith('$'):prompt='$'+body+'=$'
  else:prompt=('Evaluate 'if old[':question/problem'].startswith('Evaluate')else'Calculate ')+'$'+body+'.$'
  # Source steps, transformed to u, provide the entire identity reduction.
  base=re.sub(r'(?<![A-Za-z])x(?![A-Za-z])','t',old[':question/worked-solution'])
  solution='Let $t='+str(r)+r'x$, so $\text{d}x=\frac{1}{'+str(r)+r'}\text{d}t$.'
  if a is not None:solution+=' The limits become $t='+sp.latex(lo)+'$ and $t='+sp.latex(hi)+'$.'
  solution+=' Apply the constant multiple rule to take $1/'+str(r)+'$ outside the integral. For the remaining integral, we have:\n\n'+base
  solution+='\n\nMultiplying this result by $1/'+str(r)+'$'+(' and substituting back $t='+str(r)+'x$'if a is None else'')+', we obtain\n\n$$\n'+body+'='+sp.latex(correct)+'.\n$$'
  if template in ('q-352858','q-352867'):solution+='\n\nAt the lower endpoint the quotient is interpreted by its continuous limit.'
  values=[sp.latex(z)for z in bank]
 fp=fingerprint({':question/problem':prompt});uid=lambda s:str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),s));qid=uid('question:'+fp+':profile:'+template);fid=uid(qid+':field:'+of[':answer-field/key'])
 answers=[{':answer/id':uid(fid+':answer:'+str(i)),':answer/type':':answer.type/math',':answer/value':v}for i,v in enumerate(values)]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[chosen[0]][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':template,'profile':template,'parameters':{'r':r},'mathematical_fingerprint':fp,'source_question':template,'source_basis':SOURCE['basis'],'domain':'Real x on each connected interval where the original quotient at r*x is defined; removable lower endpoint for cot/csc definite templates uses its continuous limit.','dependencies':{'sympy':sp.__version__},'recipe_policy':'Complete original bank transported by v(x)->v(r*x)/r; C remains arbitrary. No pooled or invented distractors.'}}
def batch(difficulty,count,seed):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported level '+difficulty)
 if type(count)is not int or count<1:raise ValueError('Count must be a positive integer')
 pool=[(t,r)for t in SOURCES if level(t)==difficulty for r in range(2,7)];random.Random(seed).shuffle(pool);out=[];seen=set()
 for t,r in pool:
  rec=generate(difficulty,seed,t,{'r':r});fp=rec['generation']['mathematical_fingerprint']
  if fp not in seen:seen.add(fp);out.append(rec)
  if len(out)==count:break
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args();rows=batch(args.difficulty,args.count,args.seed)
 if len(rows)<args.count:raise SystemExit('Finite variant limit: '+str(len(rows)))
 print(json.dumps({'instances':rows,'generator_id':GENERATOR_UUID},indent=2)if args.format=='json'else'\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']for r in rows))
