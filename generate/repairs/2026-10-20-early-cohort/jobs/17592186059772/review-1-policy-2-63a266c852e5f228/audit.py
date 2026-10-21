import sys
sys.dont_write_bytecode=True
import json,re,random,copy,pathlib,hashlib,subprocess,os,itertools
from fractions import Fraction as F
ROOT=pathlib.Path('/home/jake/Developer/Course_Academy')
JOB=ROOT/'generate/repairs/2026-10-20-early-cohort/jobs/17592186059772'
PKG=pathlib.Path(os.environ.get('AUDIT_PACKAGE_ROOT',str(JOB/'workspace'))); OUT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(PKG));import generator as g

def save(n,x): (OUT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def digest():return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()}
def numeric(s):
 s=s.strip().replace(' ','')
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 # Exact rational expression; reject all unrecognized syntax before eval.
 if not re.fullmatch(r'[\d+*/()\-]+',s):raise ValueError(s)
 s=re.sub(r'(?<=\d)\(', '*(',s);s=re.sub(r'\)(?=\d|\()',')*',s)
 s=s.replace('\\cdot','*')
 import ast
 def ev(n):
  if isinstance(n,ast.Constant):return F(n.value)
  if isinstance(n,ast.UnaryOp):return -ev(n.operand) if isinstance(n.op,ast.USub) else ev(n.operand)
  if isinstance(n,ast.BinOp):
   a,b=ev(n.left),ev(n.right)
   if isinstance(n.op,ast.Add):return a+b
   if isinstance(n.op,ast.Sub):return a-b
   if isinstance(n.op,ast.Mult):return a*b
   if isinstance(n.op,ast.Div):return a/b
  raise ValueError(n)
 return ev(ast.parse(s,mode='eval').body)
def matrices(s,expression=False):
 while '\\\\begin' in s:s=s.replace('\\\\','\\')
 matches=re.findall(r'\\begin\{(?:array|bmatrix)\}(?:\{[c|]+\})?(.*?)\\end\{(?:array|bmatrix)\}',s,re.S)
 result=[]
 for body in matches:
  # body row separators are \\ in normalized content, single slash in double-escaped source after above decoding.
  rows=re.split(r'\\\\|\\(?![a-zA-Z])',body.strip())
  try:result.append([[numeric(x.replace('\\cdot','*')) for x in row.split('&')] for row in rows if row.strip()])
  except Exception:
   if not expression:raise
 return result

def operations(prompt):
 p=prompt.split('What matrix results')[1]
 p=p.replace('{R}', 'R').replace('↔',r'\leftrightarrow').replace('&','').replace(' ','')
 p=re.sub(r'R_(\d)',r'R_{\1}',p)
 p=p.replace('\\\\','\n')
 token=r'R_\{(\d)\}'
 ops=[]
 for m in re.finditer(token+r'(?:\\leftrightarrow'+token+r'|:=([^$\n]*))',p):
  t=int(m[1])-1
  if m[2]:ops.append(('swap',t,int(m[2])-1));continue
  rhs=m[3].split('\\\\')[0].split('\\end')[0]
  rs=list(re.finditer(token,rhs))
  if len(rs)==2:
   coeff=rhs[rs[0].end():rs[1].start()].replace('\\cdot','').lstrip('+')
   ops.append(('add',t,int(rs[1][1])-1,numeric(coeff or '1')))
  elif len(rs)==1:
   coeff=rhs[:rs[0].start()].replace('\\cdot','')
   ops.append(('scale',t,numeric(coeff or '1')))
  else:raise ValueError(rhs)
 return ops

def expected(q):
 m=matrices(q[':question/problem'])[0]
 for op in operations(q[':question/problem']):
  if op[0]=='swap':_,a,b=op;m[a],m[b]=m[b],m[a]
  elif op[0]=='scale':_,t,k=op;m[t]=[k*x for x in m[t]]
  else:_,t,d,k=op;m[t]=[x+k*y for x,y in zip(m[t],m[d])]
 return m

def key(q):
 f=q[':question/answer-fields'][0];k=f[':answer-field/correct'];return k[':answer/id'] if isinstance(k,dict) else k[1]
def check(record):
 q=record['question'];want=expected(q);f=q[':question/answer-fields'][0]
 matches=[c[':answer/id'] for c in f[':answer-field/choices'] if matrices(c[':answer/value'])[0]==want]
 sol=matrices(q[':question/worked-solution'],True)
 return {'id':q[':question/id'],'ops':str(operations(q[':question/problem'])),'unique_correct':matches==[key(q)],'final_solution_correct':sol[-1]==want,'choices':len(f[':answer-field/choices'])}

def main():
 save('package-hashes-before.json',digest())
 src=json.load(open(JOB/'source/source.json'))['material']['kp'];sources=[src[':knowledge-point/canonical-example']]+src[':knowledge-point/questions']
 replays=[g.build(i) for i in g.source_instances()+g.moderate_ops.sources()+g.hard_ops.sources()]
 canonical=dict(template='swap',pair=[0,1],matrix=[[-1,5,4,1],[1,0,5,2],[3,7,1,9]],letter='A')
 replays.append(g.build(canonical))
 missing=dict(template='scale',matrix=[[1,2,3],[3,4,5],[4,6,7]],target=0,factor='2',columns=[0,1,2],extra_row=1,letter='A')
 replays.append(g.build(missing))
 save('source-replays.json',replays)
 replay_results=[]
 for q in sources:
  want=expected(q); candidates=[r for r in replays if matrices(r['question'][':question/problem'])[0]==matrices(q[':question/problem'])[0] and expected(r['question'])==want]
  rr={'source_id':q[':question/id'],'matched_parameters':len(candidates)}
  if candidates:
   r=candidates[0];bank=[matrices(c[':answer/value'])[0] for c in r['question'][':question/answer-fields'][0][':answer-field/choices']]
   sb=[matrices(c[':answer/value'])[0] for c in q.get(':question/answer-fields',[{}])[0].get(':answer-field/choices',[])]
   rr.update(bank_complete=not sb or sorted(map(str,bank))==sorted(map(str,sb)),source_bank_size=len(sb),generated_id=r['question'][':question/id'])
   if sb and not rr['bank_complete']:rr.update(source_bank=str(sb),generated_bank=str(bank))
  replay_results.append(rr)
 save('source-replay-results.json',replay_results)
 records=[]
 for difficulty,n in [('easy',240),('moderate',30),('hard',50)]:
  for j in range(n):records.append(g.generate(random.Random(846217+j),difficulty=difficulty,seed=846217+j))
 save('samples.json',records);save('easy-samples.json',records[:240])
 batch=json.load(open(JOB/'samples.json'));save('runner-batch.json',batch)
 save('math-results.json',[check(r) for r in records+replays+batch])
 # Counterfactuals share a fixed bank and change which operation is requested.
 bases={t:next(r for r in records if r['generation']['template']==t) for t in ['swap','scale','add','swap-add','scale-add']}
 cf=[];cf_results=[]
 for t,r in bases.items():
  i=copy.deepcopy(r['generation']['instance']);a=g.build(i)
  j=copy.deepcopy(i)
  if t=='swap':j['pair']=next(p for p in [[0,1],[0,2],[1,2]] if p!=j['pair'])
  elif t=='scale':old=j['factor'];j['factor']=j['wrong_factors'][0];j['wrong_factors'][0]=old
  elif t=='add':old=j['coefficient'];j['coefficient']=j['wrong_coefficients'][0];j['wrong_coefficients'][0]=old
  else:
   c=next(c for c in j['candidates'] if c['coefficient']!=j['coefficient'] and c.get('pair',c.get('scale'))==j.get('pair',j.get('scale')))
   j['coefficient']=c['coefficient']
  b=g.build(j);z=copy.deepcopy(i);z['letter']='B' if i['letter']!='B' else 'C';c=g.build(z)
  # Also change scale target while keeping entry data/factors fixed.
  cf.extend([a,b,c]);cf_results.append({'template':t,'indices':[len(cf)-3,len(cf)-2,len(cf)-1], 'relevant_expected_changed':expected(a['question'])!=expected(b['question']),'irrelevant_expected_preserved':expected(a['question'])==expected(c['question']),'fixed_bank':sorted(x[':answer/value'] for x in a['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(x[':answer/value'] for x in b['question'][':question/answer-fields'][0][':answer-field/choices']),'checks':[check(x) for x in [a,b,c]]})
 i=copy.deepcopy(bases['scale']['generation']['instance']);a=g.build(i);i['target']=(i['target']+1)%3;b=g.build(i);cf.extend([a,b]);cf_results.append({'template':'scale-target','indices':[len(cf)-2,len(cf)-1],'relevant_expected_changed':expected(a['question'])!=expected(b['question']),'checks':[check(a),check(b)]})
 save('counterfactual-records.json',cf);save('counterfactual-results.json',cf_results)
 render=batch+cf+[next(r for r in records if r['generation']['template']==t) for t in ['add','swap-add','scale-add']]
 save('render-records.json',render)
 cases=[]
 for i,r in enumerate(batch+replays+cf+records[:10]):
  q=r['question'];want=expected(q);checks=[]
  for c in q[':question/answer-fields'][0][':answer-field/choices']:
   checks.append({'submitted_answer_id':c[':answer/id'],'expected':'accepted' if matrices(c[':answer/value'])[0]==want else 'rejected','purpose':'independent entrywise result comparison'})
  cases.append({'label':f'independent-{i}','record':r,'checks':checks})
 save('grader-input.json',cases)
 # Degenerate full banks must be rejected, and entry filling must retry rather than return zero-row questions.
 rejects=[]
 for i in [dict(template='swap',matrix=[[0]*3]*3,pair=[0,1],letter='A'),dict(template='scale',matrix=[[0]*4]*3,target=0,factor='2',profile='scale-factor-comparison',wrong_factors=['3','4','5','6'],letter='A')]:
  try:g.build(i);rejects.append({'instance':i,'rejected':False})
  except ValueError as e:rejects.append({'instance':i,'rejected':True,'error':str(e)})
 class ZeroFirst(random.Random):
  def __init__(self,seed,zeros):super().__init__(seed);self.zeros=zeros
  def randint(self,a,b):
   if self.zeros:self.zeros-=1;return 0
   return super().randint(a,b)
 retries=[g.sample(ZeroFirst(317,9),'swap'),g.sample(ZeroFirst(317,16),'scale')]
 save('rejection-results.json',{'degenerates':rejects,'forced_zero_first_instances':retries})
 print('source replay failures',[r for r in replay_results if not r.get('bank_complete')])
 print('math failures',[r for r in json.load(open(OUT/'math-results.json')) if not r['unique_correct'] or not r['final_solution_correct']])
 print('records',len(records),'cf',len(cf),'grader cases',len(cases))
if __name__=='__main__':main()
