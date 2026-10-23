import sys,os,json,re,pathlib,hashlib,subprocess,shutil,collections,argparse
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PYTHON=str(REPO/'.venv/bin/python')
p=argparse.ArgumentParser();p.add_argument('--package',default=str(JOB/'workspace'));p.add_argument('--candidate-records',default=str(JOB/'samples.json'));args=p.parse_args()
sys.path.insert(0,args.package)
import generator as g

def save(n,x): (ROOT/n).write_text(json.dumps(x,indent=2))
def load(p): return json.load(open(p))
def enum(v):return v.get(':db/ident') if isinstance(v,dict) else v
def matrix(q):
 s=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1]
 return [[c.strip() for c in r.split('&')] for r in s.split('\\\\')]
def answer(f):
 x=f[':answer-field/correct'];return x[':answer/value'] if isinstance(x,dict) else next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==x[1])
def compact(s):return re.sub(r'\s+|[${}]','',s)
def shape(rec):
 m=matrix(rec['question']);return len(m),len(m[0])
def mathcheck(rec):
 q=rec['question'];m=matrix(q);r,c=len(m),len(m[0]);fs=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']);errs=[]
 if any(len(row)!=c for row in m):errs.append('ragged')
 vals=[answer(f) for f in fs];expect=[f'{r}\\times{c}'] if len(fs)==1 else [str(r),str(c)]
 if list(map(compact,vals))!=expect:errs.append('key')
 if not re.search(r'\$'+str(r)+r'\$ rows and \$'+str(c)+r'\$ columns',q[':question/worked-solution']):errs.append('solution counts')
 if len(fs)==1 and len(set(compact(a[':answer/value']) for a in fs[0][':answer-field/choices']))!=5:errs.append('bank')
 return errs
source=load(JOB/'source/source.json')['material']['kp'];src=source[':knowledge-point/questions'];replays=[];replay_results=[]
for q in src:
 sid=q[':question/math-academy-id']
 try:
  rec=g.generate(seed=20261022,profile='observed-'+sid);replays.append(rec)
  fs=q[':question/answer-fields'];gs=rec['question'][':question/answer-fields']
  checks={'matrix':matrix(q)==matrix(rec['question']),'field_types':[enum(f[':answer-field/type']) for f in fs]==[enum(f[':answer-field/type']) for f in gs], 'complete_banks':[[*sorted(compact(c[':answer/value']) for c in f[':answer-field/choices'])] for f in fs]==[[*sorted(compact(c[':answer/value']) for c in f[':answer-field/choices'])] for f in gs], 'keys':[compact(answer(f)) for f in fs]==[compact(answer(f)) for f in gs], 'solution':compact(q[':question/worked-solution'])==compact(rec['question'][':question/worked-solution'])}
  replay_results.append({'source_id':q[':question/id'],'profile':'observed-'+sid,'checks':checks})
 except Exception as e:replay_results.append({'source_id':q[':question/id'],'profile':'observed-'+sid,'error':str(e),'source_record':q})
can=source[':knowledge-point/canonical-example'];cr=g.generate(seed=20261022,template='radio',parameters={'entries':matrix(can),'name':'A'});replays.append(cr)
replay_results.append({'source_id':can[':question/id'],'canonical_parameters':cr['generation']['parameters'],'matrix_equal':matrix(can)==matrix(cr['question']),'counts_correct':not mathcheck(cr),'answer_contract':'Absent in canonical source; generated radio contract inferred from other source cases.'})
save('source-replays.json',replays);save('source-replay-results.json',replay_results)
normal=[g.generate(seed=2026102200+i,template=t) for t in g.TEMPLATES for i in range(30)]
boundaries=[g.generate(seed=76543,template=t,parameters={'entries':[[str((i+j)%9-4) for j in range(c)] for i in range(r)],'name':'A'}) for t in g.TEMPLATES for r in range(2,7) for c in range(2,7)]
batch=load(args.candidate_records);save('batch-records.json',batch);save('normal-records.json',normal);save('boundary-records.json',boundaries)
cf=[]
for t in g.TEMPLATES:
 b={'entries':[['1','2','3'],['4','5','6']],'name':'A'};rel={'entries':b['entries']+[['7','8','9']],'name':'A'};irr={'entries':[['0','2','3'],['4','5','6']],'name':'Z'}
 for label,par in [('base',b),('relevant',rel),('irrelevant',irr)]:
  kw={'bank':[(2,3),(3,3),(3,2),(2,2),(4,4)]} if t=='radio' else {}
  cf.append(g.generate(seed=908172,template=t,parameters=par,**kw))
save('counterfactual-records.json',cf)
allrecs=replays+normal+boundaries+batch+cf
fail=[{'id':r['question'][':question/id'],'errors':mathcheck(r)} for r in allrecs if mathcheck(r)]
save('math-results.json',{'command':f'{PYTHON} audit.py --package {args.package} --candidate-records {args.candidate_records}','checked':len(allrecs),'independent_method':'Parse matrix TeX rows and cells from prompts; compare ordered dimensions to keys, uniqueness of choices and prose counts. No generator metadata used.','failures':fail})
# Real learner grader: every bank option and free numeric equivalents and mistakes.
cases=[]
for ix,rec in enumerate(replays+normal[:6]+boundaries[25:30]+batch+cf):
 checks=[];r,c=shape(rec)
 for fi,f in enumerate(rec['question'][':question/answer-fields']):
  if enum(f[':answer-field/type']).endswith('/radio'):
   for a in f[':answer-field/choices']:
    checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if compact(a[':answer/value'])==f'{r}\\times{c}' else 'rejected','purpose':'independent dimensions vs each offered choice'})
  else:
   n=(r,c)[fi]
   for value,expected in [(str(n),'accepted'),(f'{n}.0','accepted'),(f'{2*n}/2','accepted'),(f'\\frac{{{2*n}}}{{2}}','accepted'),(str(n+1),'rejected'),('0','rejected'),('-'+str(n),'rejected')]:
    checks.append({'field_index':fi,'submitted':value,'expected':expected,'purpose':'numeric equivalence or plausible incorrect count'})
   if r!=c:checks.append({'field_index':fi,'submitted':str((c,r)[fi]),'expected':'rejected','purpose':'row/column reversal'})
 cases.append({'label':f'independent-{ix}','record':rec,'checks':checks})
for case in cases[-9:]:
 rec=case['record']; gen=rec['generation']
 if gen['template']!='radio' and len(gen['parameters']['entries'])==3:
  case['checks'].append({'field_index':0,'submitted':'2','expected':'rejected','purpose':'Controlled added-row pair: formerly correct row count must now fail'})
save('grader-input.json',cases)
# Rejections and contracts.
reject=[]
invalid=[{'parameters':{'entries':[],'name':'A'}},{'parameters':{'entries':[['1','2'],['3']],'name':'A'}},{'parameters':{'entries':[['x','2'],['3','4']],'name':'A'}},{'level':'hard'},{'template':'unsupported'},{'template':'radio','parameters':{'entries':[['1','2'],['3','4']],'name':'A'},'bank':[(2,2)]*5}]
for kw in invalid:
 try:g.generate(**kw);reject.append({'input':kw,'rejected':False})
 except Exception as e:reject.append({'input':kw,'rejected':True,'message':str(e)})
vec=[]
for par in [{'entries':[['1','2','3']],'name':'A'},{'entries':[['1'],['2']],'name':'A'}]:
 try:g.generate(parameters=par);vec.append({'input':par,'accepted':True})
 except Exception as e:vec.append({'input':par,'accepted':False,'message':str(e)})
finite=g.batch('easy',25,611329)
save('finite-batch-records.json',finite)
save('construction-results.json',{'invalid_inputs':reject,'lesson_vector_probes':vec,'finite_batch_unique_shapes':len(set(shape(r) for r in finite)),'finite_batch_rejections':finite[0]['generation']['batch_rejected_repeated_shapes'],'deterministic':normal==[g.generate(seed=2026102200+i,template=t) for t in g.TEMPLATES for i in range(30)],'runner_batch_replay':batch==json.loads(json.dumps(g.batch('easy',5,928264887))),'source_basis_supplied':5665,'embedded_source_basis':g.SOURCE['basis']})
# Captured inventory: original source and non-source records are distinguished; no generation metadata invented.
inv=load(JOB/'source/inventory.json');stored=[]
for q in inv['questions']:
 rec={'question':q};stored.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':':question/math-academy-id' in q,'retired':q.get(':question/retired',False),'difficulty':enum(q.get(':question/difficulty')),'shape':shape(rec),'errors':mathcheck(rec)})
save('inventory-results.json',{'basis':inv['basis'],'records':stored,'limits':'Captured inventory has no generation metadata on the five non-source records; no defect demonstrated. Original q-139628 is source, not generated. Actual learner histories and policy weights are not in snapshot.'})
save('affected-inventory.json',{'affected_questions':[]})
# Shortcut counts, grouped by recognizable prompt template. Keep empirical counts, do not extrapolate tiny groups.
def summary(records):
 out={}
 for t in g.TEMPLATES:
  rs=[r for r in records if r['generation']['template']==t]
  if not rs:continue
  sh=[shape(r) for r in rs];d={'total':len(rs),'shape_counts':dict(collections.Counter(f'{r}x{c}' for r,c in sh)),'square':sum(r==c for r,c in sh),'always_3x3':sum((r,c)==(3,3) for r,c in sh)}
  if t=='radio':
   idx=[next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if compact(a[':answer/value'])==f'{shape(r)[0]}\\times{shape(r)[1]}') for r in rs];d['correct_positions']=dict(collections.Counter(idx));d['first_choice_successes']=idx.count(0)
  out[t]=d
 return out
save('coverage-results.json',{'normal':summary(normal),'boundary':summary(boundaries),'runner_batch':summary(batch),'finite_batch':summary(finite)})
save('render-records.json',cf+[boundaries[24],replays[3]]+batch)
print(json.dumps({'math_failures':fail,'source_replay_failures':[r for r in replay_results if 'error' in r],'normal_count':len(normal),'grader_cases':len(cases),'runner_batch':summary(batch)},indent=2))
