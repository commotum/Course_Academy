"""Independent printed-content, full-source fidelity, identity and native grading QA."""
import sys
sys.dont_write_bytecode=True
import copy,collections,hashlib,importlib.util,itertools,json,pathlib,re,subprocess,platform
import sympy as sp
D=pathlib.Path(__file__).parent;P=D.with_suffix('.py');ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('kp00913_private',P);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from math_format import cells,validate_generated_record,normalize_prose,normalize_tex
PAT=re.compile(r'\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}')
def matrices(text):return [cells(m[1])for m in PAT.finditer(text)]
def number(s):
 assert re.fullmatch(r'\(?-?\d+\)?',s),s
 return int(s.strip('()'))
def evaluated(rows):return [[number(c)for c in row]for row in rows]
def mathematical(value):
 raw=value.strip();raw=re.sub(r'^\$\$\s*|\s*\$\$$','',raw)
 mm=matrices(raw)
 if mm:
  assert len(mm)==1
  return tuple(map(tuple,evaluated(mm[0])))
 if re.fullmatch(r'\[-?\d+\]',raw):return ((int(raw[1:-1]),),)
 if re.fullmatch('-?\\d+',raw):return int(raw)
 assert raw=='Undefined',raw
 return raw
def read_prompt(record):
 q=record['question'];mm=matrices(q[':question/problem']);assert len(mm)==2
 aa,bb=map(evaluated,mm)
 # Derive conformability from actual printed rows and columns, not metadata.
 defined=len(aa[0])==len(bb)
 if defined:
  p=[[sum(aa[i][k]*bb[k][j]for k in range(len(bb)))for j in range(len(bb[0]))]for i in range(len(aa))]
 else:p=None
 return aa,bb,p

def check_printed(record):
 q=record['question'];assert not any(ord(c)<32 and c not in '\n\t\r'for key in [':question/problem',':question/worked-solution']for c in q.get(key,''))
 aa,bb,p=read_prompt(record);fields=q.get(':question/answer-fields',[])
 if p is not None:
  assert len(aa[0])==1 and len(bb)==1,'outer-product orientation'
 correct_value='Undefined'if p is None else tuple(map(tuple,p))
 for f in fields:
  assert '{{'+f[':answer-field/key']+'}}'in q[':question/problem']or f[':answer-field/type'].endswith('/radio')
  correct=f.get(':answer-field/correct')
  if correct:
   actual=next(a for a in f[':answer-field/choices']if a[':answer/id']==correct[1]);got=mathematical(actual[':answer/value'])
   if f[':answer-field/type'].endswith('/blank'):
    pos=int(f[':answer-field/key'].split('-')[1])-1;i,j=divmod(pos,len(p[0]));assert got==p[i][j],(got,p,i,j)
   else:assert got==correct_value,(got,correct_value)
  if not record['generation']['evidence_only']and f[':answer-field/type'].endswith('/radio'):
   bank=[mathematical(a[':answer/value'])for a in f[':answer-field/choices']];assert len(bank)==len(set(bank))==5
 sol=q.get(':question/worked-solution')
 if sol is None:return
 if p is None:
  assert 'undefined'in sol.lower();assert not matrices(sol);return
 n,k=len(aa),len(bb[0]);sm=matrices(sol)
 if n==2:
  # Four partial matrices, four independently read scalar multiplications,
  # then the full conclusion. No generic equality-only check.
  assert len(sm)==13,len(sm)
  for step in range(4):
   assert evaluated(sm[step*3])==aa and evaluated(sm[step*3+1])==bb
   part=sm[step*3+2]
   for i in range(n):
    for j in range(k):
     if i*k+j<=step:assert number(part[i][j])==p[i][j]
     else:assert part[i][j]=='∗'
  scalar=re.findall(r'\\,(-?\d+)=([^\n]*?)(?= \\\\|\\end\{aligned\})',sol);assert len(scalar)==4
  for idx,(value,rhs)in enumerate(scalar):
   i,j=divmod(idx,k);factors=rhs.split(r'\cdot');assert len(factors)==2
   x,y=map(lambda t:number(t.strip()),factors);assert x==aa[i][0]and y==bb[0][j]and int(value)==x*y
  assert evaluated(sm[-1])==p,'concluding matrix stale'
 else:
  # First substituted vector pair, explicit unevaluated full product matrix,
  # then collected result: require structure as well as mathematical equality.
  assert len(sm)==4,len(sm);assert evaluated(sm[0])==aa and evaluated(sm[1])==bb
  for i,row in enumerate(sm[2]):
   for j,cell in enumerate(row):
    ff=cell.split(r'\cdot');assert len(ff)==2,'required product operation missing'
    x,y=map(lambda t:number(t.strip()),ff);assert x==aa[i][0]and y==bb[0][j]and x*y==p[i][j]
  assert evaluated(sm[3])==p
 # Shared prose and dimension statement independently read for normal/source.
 assert (str(n)+r'\times 1')in sol and ('1'+r'\times '+str(k))in sol

source=json.load(open(D/'source.json'));orig=source['record'][':knowledge-point/questions'];cases=json.load(open(D/'source-cases.json'))
fidelity={'questions':0,'prompts_exact':0,'solutions_exact':0,'solutions_present':0,'all_field_banks':0,'all_choices':0,'correct_designations':0,'questions_missing_correct':0,'attribute_presence':0,'source_rows':[],'exact_typed_choice_strings':0};reviews=[];fixtures=[]
def native_checks(record,label):
 checks=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  if ':answer-field/correct'not in f:continue
  correct=f[':answer-field/correct'][1];answer=next(a for a in f[':answer-field/choices']if a[':answer/id']==correct)
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else 'rejected','purpose':'complete source/native radio bank'if record['generation']['evidence_only']else 'method-derived radio bank'})
  else:
   v=answer[':answer/value'];iv=int(v)
   for value,expect,purpose in [(v,'accepted','canonical blank'),(str(iv*3)+'/3','accepted','legitimate unreduced rational equivalent'),(str(iv+1),'rejected','wrong entry')]:checks.append({'field_index':i,'submitted':value,'expected':expect,'purpose':purpose})
 if checks:fixtures.append({'label':label,'record':record,'checks':checks})
for q,c in zip(orig,cases):
 r=g.generate(c['level'],parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);nq=r['question'];check_printed(r);native_checks(r,c['source_id']);reviews.append(r)
 assert nq[':question/problem']==q[':question/problem'];fidelity['prompts_exact']+=1
 for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert(key in q)==(key in nq)
 fidelity['attribute_presence']+=1
 if ':question/worked-solution'in q:
  fidelity['solutions_present']+=1;assert nq[':question/worked-solution']==q[':question/worked-solution'];fidelity['solutions_exact']+=1
 for of,nf in zip(q[':question/answer-fields'],nq[':question/answer-fields']):
  assert of[':answer-field/key']==nf[':answer-field/key'];assert of[':answer-field/type'][':db/ident']==nf[':answer-field/type']
  assert sorted((a[':answer/type'][':db/ident'],a[':answer/value'])for a in of[':answer-field/choices'])==sorted((a[':answer/type'],a[':answer/value'])for a in nf[':answer-field/choices']);fidelity['exact_typed_choice_strings']+=len(of[':answer-field/choices'])
  ov=collections.Counter((a[':answer/type'][':db/ident'],mathematical(a[':answer/value']))for a in of[':answer-field/choices']);nv=collections.Counter((a[':answer/type'],mathematical(a[':answer/value']))for a in nf[':answer-field/choices']);assert ov==nv,(c['source_id'],ov,nv)
  fidelity['all_field_banks']+=1;fidelity['all_choices']+=sum(ov.values());assert(':answer-field/correct'in of)==(':answer-field/correct'in nf)
  if ':answer-field/correct'in of:
   assert mathematical(of[':answer-field/correct'][':answer/value'])==mathematical(next(a[':answer/value']for a in nf[':answer-field/choices']if a[':answer/id']==nf[':answer-field/correct'][1]));fidelity['correct_designations']+=1
 if any(':answer-field/correct'not in f for f in q[':question/answer-fields']):fidelity['questions_missing_correct']+=1
 fidelity['questions']+=1
 fidelity['source_rows'].append({'source_id':c['source_id'],'question_id':nq[':question/id'],'content_sha256':r['generation']['content_sha256'],'full_bank':True,'present_solution_exact':True if ':question/worked-solution'in q else None,'correct_designation':'missing preserved'if any(':answer-field/correct'not in f for f in q[':question/answer-fields'])else 'matched'})
counts={};samples={};coverage={};all_records=[]
for level in ['easy','moderate','hard']:
 seen=set();roles=collections.defaultdict(set);families=set();forms=set();representatives=[]
 for seed in range(500):
  rec=g.generate(level,seed);check_printed(rec);validate_generated_record(rec);seen.add(rec['generation']['mathematical_fingerprint']);families.add(rec['generation']['family']);forms.add(rec['question'][':question/answer-fields'][0][':answer-field/type']);all_records.append(rec)
  a,b,p=read_prompt(rec)
  for i,row in enumerate(a):roles['a'+str(i)].add(row[0])
  for j,x in enumerate(b[0]):roles['b'+str(j)].add(x)
  if len(representatives)<2 or rec['generation']['family']not in {x['generation']['family']for x in representatives}:representatives.append(rec)
  # Fixed params/family/profile/layout: seed and choice order never change IDs.
  replay=g.generate(level,seed+10000,template=rec['generation']['template'],profile=rec['generation']['profile'],field_type=rec['question'][':question/answer-fields'][0][':answer-field/type'],parameters=rec['generation']['parameters']);assert replay['question'][':question/id']==rec['question'][':question/id']
  assert set(rec['knowledge_point'])=={'db_id','id','title'}
  if seed<8:native_checks(rec,level+'-'+str(seed))
 counts[level]=len(seen);assert len(seen)>=450,(level,len(seen));coverage[level]={'families':sorted(families),'field_types':sorted(forms),'slot_values':{k:sorted(v)for k,v in roles.items()}}
 samples[level]=representatives;reviews.extend(representatives)
# Every mask and field contract changed-parameter validation.
for family in sum(g.SOURCES.values(),[]):
 for ft in ['radio','blank']:
  for seed in range(20):check_printed(g.generate('easy',seed,profile='authored-method/'+family,field_type=ft))
# Change one complete entry slot while holding every other operand fixed.
left={'a':[2,-3,4],'b':[2,-3]};right={'a':[3,-3,4],'b':[2,-3]}
x=g.generate('moderate',parameters=left,profile='authored-method/q-275548',field_type='blank');y=g.generate('moderate',parameters=right,profile='authored-method/q-275548',field_type='blank');check_printed(x);check_printed(y);assert read_prompt(x)[2][1:]==read_prompt(y)[2][1:]and read_prompt(x)[2][0]!=read_prompt(y)[2][0]
assert x['question'][':question/id']!=y['question'][':question/id']
# Explicit boundary guards same as sampler; change printed factors at unchanged keys.
mutants=[]
def must_fail(fn,label):
 try:fn()
 except (AssertionError,ValueError,KeyError):mutants.append(label);return
 raise AssertionError('mutation survived '+label)
for level,params,template in [('easy',{'a':[5,5,5,5],'b':[5,5,5]},'outer-4x3'),('moderate',{'a':[2,2,1],'b':[2,2]},'outer-3x2'),('moderate',{'a':[5,5,5],'b':[5,5]},'outer-3x2'),('hard',{'a':[1,1,1,1],'b':[2,3,4]},'outer-4x3'),('hard',{'a':[10,10,10,10],'b':[5,5,5]},'outer-4x3')]:must_fail(lambda:g.generate(level,parameters=params,template=template),'level guard '+level+str(params))
ref=g.generate('moderate',8,field_type='radio');
m=copy.deepcopy(ref);text=m['question'][':question/problem'];m['question'][':question/problem']=PAT.sub(lambda z:z[0].replace(' & ',r' \\ ')if '&'in z[1]else z[0],text);must_fail(lambda:check_printed(m),'orientation changed unchanged key')
m=copy.deepcopy(ref);m['question'][':question/problem']=PAT.sub(lambda z:z[0].replace(re.findall('-?\\d+',z[1])[0],'9',1),m['question'][':question/problem'],count=1);must_fail(lambda:check_printed(m),'factor changed unchanged key')
m=copy.deepcopy(ref);m['question'][':question/worked-solution']=m['question'][':question/worked-solution'].replace(r'\cdot',r'+',2);must_fail(lambda:check_printed(m),'ordered product operation removed')
m=copy.deepcopy(ref);m['question'][':question/worked-solution']=m['question'][':question/worked-solution'].replace(r'\cdot', '\x0c'+'rac',1);must_fail(lambda:check_printed(m),'control character product mutation')
ref2=g.generate('easy',profile='authored-method/q-318484',field_type='blank');m=copy.deepcopy(ref2);sol=m['question'][':question/worked-solution'];mm=list(PAT.finditer(sol));last=mm[-1];m['question'][':question/worked-solution']=sol[:last.start()]+g.matrix([[99,99],[99,99]])+sol[last.end():];must_fail(lambda:check_printed(m),'stale conclusion unchanged key')
extras=json.load(open(D/'render-extra-records.json'))
for i,r in enumerate(extras):check_printed(r);validate_generated_record(r);native_checks(r,'supplementary-'+str(i))
# Finite bounded coverage claim:500 sampled tasks/level, not unlimited or exhaustive.
(D/'review.json').write_text(json.dumps(reviews,indent=2)+'\n');(D/'review.md').write_text('# Source evidence and generated variants\n\n'+ '\n\n'.join(('Original replay (evidence-only)\n\n'if r['generation']['evidence_only']else 'Authored generated variant\n\n')+g.markdown(r)for r in reviews)+'\n')
(D/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
base=ROOT/'generate/scratch/17592186059716-draft/check-engine';subprocess.run([str(base),str(D/'engine-input.json'),str(D/'engine-results.json')],check=True)
build=json.load(open(D/'reference/grader-build.json'));hashes={**build['engine_sources'],**build['dependencies'],build['source']:build['source_sha256'],build['library']:build['library_sha256'],build['binary']:build['binary_sha256']}
assert len(hashes)==42
for path,h in hashes.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,path
(D/'reference/grader-recheck-after.json').write_text(json.dumps({'checked_files':42,'sha256':hashes},indent=2)+'\n')
# Recheck complete protected numeric path set; never import or mutate numeric files.
protected={}
for p in (ROOT/'generate/scratch').rglob('*'):
 if p.is_file()and(p==ROOT/'generate/scratch/17592186100913.py'or ROOT/'generate/scratch/17592186100913'in p.parents or p.parent.name=='__pycache__'and p.name.startswith('17592186100913.')and p.suffix=='.pyc'):protected[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
assert protected==json.load(open(D/'reference/registered-baseline.json'))['path_sha256']
(D/'reference/registered-after.json').write_text(json.dumps({'path_sha256':protected,'unchanged':True},indent=2)+'\n')
report={'status':'passed','script_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'source_basis':2275,'fidelity':fidelity,'sampled_meaningful_tasks':counts,'coverage':coverage,'mutant_regressions':mutants,'normal_records_checked':len(all_records),'independent_inventory_records':0,'native':json.load(open(D/'engine-results.json')),'native_current_files_rechecked':42,'protected_numeric_unchanged':True,'runtime':{'python':platform.python_version(),'sympy':sp.__version__},'plots':'none','limits':['Opaque historical bank intention unresolved; evidence-only public replay.','Two source questions lack keys and solutions; omissions preserved, not counted as matched designations.','Moderate column-by-column and unrated row-by-column undefined sources retained as out-of-scope evidence; normal defaults outer products only.','500 tasks per level checked; bounded sampler coverage rather than exhaustive full numerical domain.']}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['native','coverage']},indent=2))
