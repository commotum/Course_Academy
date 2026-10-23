import os,sys,json,re,hashlib,platform,importlib.metadata,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PKG=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT.parent/'workspace'
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(ROOT/'assets')
sys.path[:0]=[str(ROOT/'review-deps'),str(PKG)]
import generator as g
import sympy as s
from sympy.parsing.latex import parse_latex

def save(name,data): (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False))
def parse(v):
 v=v.replace('\u2061','').replace('′',"'")
 v=re.sub(r'\\operatorname\{(sin|cos|tan|cot|sec|csc|ln)\}',r'\\\1',v)
 v=re.sub(r'\{(sin|cos|tan|cot|sec|csc)\}',r'\\\1',v)
 v=v.replace('\\,','').strip().rstrip('.,')
 v=re.sub(r'(?<![A-Za-z])t\s*(?=\\left\()', r't\\cdot ',v)
 v=v.replace(r'}\left(',r'}\cdot \left(')
 v=re.sub(r'(\\(?:sin|cos|tan|cot|sec|csc)(?:\^\{[0-9]+\})?)\s*\{t\}', r'\1(t)',v)
 z=parse_latex(v)
 return z.xreplace({a:(s.E if a.name=='e' else s.pi) for a in z.free_symbols if a.name in ('e','pi')})
def eq(x,y):return s.simplify(s.trigsimp(x-y))==0

def key(r):
 f=r['question'][':question/answer-fields'][0]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def mathcheck(r):
 q=r['question'];prompt=q[':question/problem'];fields=q[':question/answer-fields'];f=fields[0]
 block=re.findall(r'\$\$(.*?)\$\$',prompt,re.S)[0].strip()
 xs,ys=block[2:].split(r',\,y=');ys=ys.split(r',\,')[0]
 x,y=parse(xs),parse(ys);t=next(v for v in x.free_symbols|y.free_symbols if v.name=='t')
 target=re.search(r'where \$t=(.*?)\.\$',prompt).group(1);u=parse(target)
 dx,dy=s.diff(x,t),s.diff(y,t);m=s.simplify((dy/dx).subs(t,u));vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert dx.subs(t,u)!=0,(xs,ys,target)
 assert eq(parse(key(r)),m),('wrong key',key(r),str(m))
 assert sum(eq(v,m) for v in vals)==1
 assert all(not eq(a,b) for i,a in enumerate(vals) for b in vals[i+1:])
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
 last=blocks[-1].split('& =')[-1].replace(r'\end{aligned}','').strip().rstrip('.')
 assert eq(parse(last),m),('wrong solution',last,str(m))
 # Every displayed ratio and evaluated equality RHS, independently interpreted.
 checks=0
 for bi in [2,3]:
  for row in re.split(r'\\\\\s*&\s*=',blocks[bi].split('& =',1)[1]):
   row=row.replace(r'\end{aligned}','').strip().rstrip('.')
   z=parse(row);target_value=dy/dx if bi==2 else m
   assert eq(z,target_value),('bad displayed equality',bi,row,str(target_value))
   checks+=1
 return {'id':q[':question/id'],'template':r['generation']['template'],'answer':str(m),'displayed_rows':checks,'result':'passed'}

if __name__=='__main__':
 before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.iterdir() if p.is_file()}
 save('package-before.json',before)
 source=json.load(open(ROOT.parent/'source/source.json'))['material']['kp'][':knowledge-point/questions']
 replays=[]; replay_results=[]
 for q in source:
  ma=q[':question/math-academy-id'];template=g.SOURCE_TEMPLATE[ma];level,kind,*_=g.TEMPLATES[template]
  r=g.generate(level,4021,template,parameters=g.PARAMETERS[ma],profile='observed_'+ma if kind=='radio' else 'observed');replays.append(r)
  sf=q[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0]
  src=[parse(a[':answer/value']) for a in sf[':answer-field/choices']]; dst=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
  replay_results.append({'source_id':q[':question/id'],'ma_id':ma,'complete_bank_match':len(src)==len(dst) and all(any(eq(a,b) for b in dst) for a in src),'correct_match':eq(parse(sf[':answer-field/correct'][':answer/value']),parse(key(r))),'generated_id':r['question'][':question/id']})
 save('source-replays.json',replays);save('source-replay-results.json',replay_results)
 print('source replay',len(replays),flush=True)
 samples=[]
 for i,(template,(level,*_)) in enumerate(g.TEMPLATES.items()):
  for j in range(2):samples.append(g.generate(level,71003+i*13+j,template))
 save('samples-independent.json',samples)
 pairs=[]
 def add(label,template,p,change,kind):
  level=g.TEMPLATES[template][0];a=g.generate(level,8201,template,parameters=p);b=g.generate(level,8201,template,parameters=dict(p,**change));pairs.append({'label':label,'kind':kind,'before':a,'after':b,'change':change})
 add('target reverses trig slope','double_cos_radio',dict(a=2,b=3,u='pi/6'),{'u':'pi/3'},'relevant')
 add('horizontal target becomes positive','linear_trig_radio',dict(a=2,b=1,u='pi/2'),{'u':'3*pi/2'},'relevant')
 add('translation preserves slope','poly5_radio',dict(a=2,b=3,c=3,u=1),{'c':-4},'irrelevant')
 add('illustrated cubic target changes slope','cubic_blank',dict(a=2,b=1,u=2),{'u':3},'relevant')
 add('hard horizontal target','exp_root_radio',dict(a=2,b=2,u=1),{'u':2},'relevant')
 save('counterfactuals.json',pairs);save('counterfactual-records.json',[r for p in pairs for r in (p['before'],p['after'])])
 batch=json.load(open(ROOT.parent/'samples.json'));save('batch.json',batch)
 allrecords=replays+samples+batch+[r for p in pairs for r in (p['before'],p['after'])]
 results=[]
 for r in allrecords:
  try:results.append(mathcheck(r))
  except Exception as e:results.append({'id':r['question'][':question/id'],'template':r['generation']['template'],'error':repr(e)})
 save('math-results.json',results);print('math',len(results),'errors',sum('error'in v for v in results),flush=True)
 cases=[]
 for i,r in enumerate(allrecords):
  f=r['question'][':question/answer-fields'][0];checks=[]
  if f[':answer-field/type'].endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independent exact derivative and unique distractor check'} for a in f[':answer-field/choices']]
  else:
   m=parse(key(r));equiv=str(m).replace('**','^').replace('exp(','exp(')
   checks=[{'submitted':z,'expected':e,'purpose':purpose} for z,e,purpose in [(key(r),'accepted','exact TeX'),(equiv,'accepted','equivalent plain mathematical notation'),('('+equiv+')+1','rejected','plausible additive error'),('-('+equiv+')','rejected','sign error')] if not (purpose=='sign error' and m==0)]
  cases.append({'label':str(i)+' '+r['generation']['template'],'record':r,'checks':checks})
 # Counterfactual grader must reject the obsolete relevant response, preserve irrelevant.
 for p in pairs:
  for side in ['before','after']:
   r=p[side];other=p['after' if side=='before' else 'before'];f=r['question'][':question/answer-fields'][0]
   if f[':answer-field/type'].endswith('/blank'):
    cases.append({'label':p['label']+' stale response '+side,'record':r,'checks':[{'submitted':key(other),'expected':'accepted' if p['kind']=='irrelevant' else 'rejected','purpose':'counterfactual response dependency'}]})
 save('grader-input.json',cases)
 rejects=[]
 for template,p in [('cubic_blank',dict(a=3,b=1,u=-2)),('poly5_radio',dict(a=2,b=3,c=0,u=0)),('exp_root_blank',dict(a=2,b=2,u=0)),('exp_log_blank',dict(a=2,b=2,u=-2)),('double_cos_radio',dict(a=1,b=1,u='pi/4'))]:
  try:g.generate(g.TEMPLATES[template][0],4,template,parameters=p);error=None
  except ValueError as e:error=str(e)
  rejects.append({'template':template,'parameters':p,'rejected':error is not None,'message':error})
 save('rejection-tests.json',rejects)
 replay=g.generate('easy',3175644379)
 save('determinism.json',{'same_call_equal':replay==g.generate('easy',3175644379),'batch_nonplot_record_equal':replay==batch[1]})
 save('runtime.json',{'python':platform.python_version(),'packages':{p:importlib.metadata.version(p) for p in ['sympy','matplotlib','numpy']},'package_hashes_unchanged':before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.iterdir() if p.is_file()},'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python review.py '+str(PKG)})
 save('render-records.json',batch+[r for p in pairs for r in (p['before'],p['after'])]+[r for r in replays if r['generation']['template'] in ['harmonic_blank','nested_trig_radio','sec_csc_radio','exp_log_blank']])
 print('saved all checks',flush=True)
