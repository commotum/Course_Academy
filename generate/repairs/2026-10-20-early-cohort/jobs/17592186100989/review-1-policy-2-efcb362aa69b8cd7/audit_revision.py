"""Independent targeted checks; all evidence output resides beside this script."""
import sys,json,re,pathlib,importlib.util,copy,collections,subprocess
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent;JOB=ROOT.parent;REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,x):(ROOT/n).write_text(json.dumps(x,indent=2)+'\n')
def load(n):return json.loads((ROOT/n).read_text())
spec=importlib.util.spec_from_file_location('candidate',JOB/'workspace/17592186100989.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def q(r):return r.get('question',r)
def field(r):return q(r)[':question/answer-fields'][0]
def enum(x):return x.get(':db/ident') if isinstance(x,dict) else x
def parsed(r):
 s=q(r)[':question/problem'];m=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',s,re.S)
 a=[[v.strip() for v in row.split('&')] for row in m[1].split('\\\\')];i,j=map(int,re.search(r'_\{(\d)(\d)\}',s).groups());return a,i,j

def expected(r):
 a,i,j=parsed(r);return a[i-1][j-1] if i<=len(a) and j<=len(a) else 'No such entry'
def bank(r):return [v[':answer/value'] for v in field(r)[':answer-field/choices']]
def key(r):
 f=field(r);c=f[':answer-field/correct'];cid=c[':answer/id'] if isinstance(c,dict) else c[1];return next(v[':answer/value'] for v in f[':answer-field/choices'] if v[':answer/id']==cid)
def summary(rs):
 groups=collections.defaultdict(list)
 for r in rs:
  a,i,j=parsed(r);s=q(r)[':question/problem'];f=field(r);group=f"{enum(f[':answer-field/type']).split('/')[-1]}/{len(a)}/"+('display' if '$$' in s else 'inline');groups[group].append({'id':q(r)[':question/id'],'i':i,'j':j,'answer':expected(r),'position':bank(r).index(key(r))})
 return {k:{'count':len(v),'missing':sum(x['answer']=='No such entry' for x in v),'coordinates':sorted(set((x['i'],x['j']) for x in v)),'records':v} for k,v in groups.items()}
if __name__=='__main__':
 controlled=[];relationships=[]
 for profile,n,i,j in [('all_four',2,2,2),('transpose_neighbors',3,3,2),('right_up_left',3,2,2),('local_neighbors',4,2,3),('inline_diagonal',4,1,1)]:
  p={'name':'B','matrix':[[str(r*n+c-6) for c in range(n)] for r in range(n)],'i':i,'j':j}
  base=g.generate_easy(seed=37,profile=profile,parameters=p);start=len(controlled);controlled.append(base)
  for label,axis in [('missing_row','i'),('missing_column','j')]:
   pp=copy.deepcopy(p);pp[axis]=n+1
   if profile!='all_four':pp['bank_anchor']=[i,j]
   after=g.generate_easy(seed=37,profile=profile,parameters=pp);controlled.append(after)
   relationships.append({'profile':profile,'change':label,'before':start,'after':len(controlled)-1,'expected':'No such entry','old':expected(base),'same_bank':bank(base)==bank(after),'passed':key(after)=='No such entry' and bank(base)==bank(after)})
  for label,pp in [('rename',p|{'name':'G'}),('non_target',copy.deepcopy(p)),('target_value',copy.deepcopy(p))]:
   if label=='non_target':pp['matrix'][0][0]=r'\sqrt{3}' if (i,j)!=(1,1) else pp['matrix'][0][0];pp['matrix'][-1][-1]=r'\sqrt{3}' if (i,j)==(1,1) else pp['matrix'][-1][-1]
   if label=='target_value':pp['matrix'][i-1][j-1]=r'\sqrt{2}'
   after=g.generate_easy(seed=37,profile=profile,parameters=pp);controlled.append(after);want=r'\sqrt{2}' if label=='target_value' else expected(base)
   relationships.append({'profile':profile,'change':label,'before':start,'after':len(controlled)-1,'expected':want,'old':expected(base),'passed':key(after)==want})
 # Fully controlled target movement, same 2x2 matrix, same answer bank and option order.
 p={'name':'B','matrix':[['1','-3'],['0','5']],'i':3,'j':2}
 for i,j in [(3,2),(2,2),(1,2),(2,1),(1,1)]:controlled.append(g.generate_easy(seed=11,profile='all_four',parameters=p|{'i':i,'j':j}))
 save('controlled-records.json',controlled);save('controlled-relationships.json',relationships)
 pairs=g.generate_batch('easy',430123,32);save('cli-samples.json',pairs)
 assert all(x['passed'] for x in relationships)
 # Record actual rejected proposals without changing acceptance behavior.
 original=g.sample;attempts=[];current=[]
 def trace(*args,**kwargs):
  p=original(*args,**kwargs);current.append(p);return p
 g.sample=trace
 for seed in range(918201,918249):
  current=[];r=g.generate_easy(seed=seed);attempts.append({'seed':seed,'profile':r['generation']['bank_profile'],'proposals':current,'accepted':r,'attempt_count':len(current)})
 save('resampling.json',{'runs':attempts,'rule':'Existence decision and bank chosen before whole-bank rejection; both missing/existing now supported; invalid coordinates and duplicate scalar choices resampled.','attempts':sum(x['attempt_count'] for x in attempts)})
 # Add checks to the inherited independent grader inputs, including stale values.
 cases=load('grader-input.json')
 for idx,r in enumerate(controlled):
  f=field(r);e=expected(r);checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==e else 'rejected','purpose':'Independent displayed indices, including stale counterpart answers'} for a in f[':answer-field/choices']]
  cases.append({'label':f'controlled-{idx}','record':r,'checks':checks})
 save('grader-input.json',cases)
 render=load('batch-records.json')+controlled[:6]+[controlled[18],controlled[20],controlled[24],controlled[26]]+[cases[-len(controlled)-1]['record']]
 save('render-revision.json',render)
 save('scope-results.json',{'requested_difficulty':'easy','sample_files':['samples.json','cli-samples.json','batch-records.json','controlled-records.json'],'passed':all(len(parsed(r)[0]) in (2,3,4) and q(r)[':question/difficulty']==':question.difficulty/easy' for r in load('samples.json')+pairs+controlled),'reasoning':'One square-matrix lookup or dimension check; symbols and integers copied without arithmetic. Missing column cases use the same lesson bounds rule as missing row. No added prerequisites.'})
 save('revision-summary.json',{'controlled':len(controlled),'relationships':len(relationships),'failures':[x for x in relationships if not x['passed']],'random_sample_count':48,'paired_cli_count':32,'exact_batch_count':5,'profiles':dict(collections.Counter(r['generation']['bank_profile'] for r in load('samples.json'))),'resampling_attempts':sum(x['attempt_count'] for x in attempts)})
 (ROOT/'session-state.md').write_text('Source verified; old counterexample fails on preserved old package and passes current. Independent source replay, fresh 48 API/32 CLI samples, 35 controlled radios, exact 5-item batch, rejection, deterministic replay and relocation saved. Native grading, delivery and visual inspection pending.\n')
 print(json.dumps(load('revision-summary.json')))
