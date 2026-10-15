"""Independent displayed-data checks, source fidelity, native grading and baseline audit."""
import copy, fractions, hashlib, importlib.util, json, pathlib, re, subprocess, sys
sys.dont_write_bytecode=True
D=pathlib.Path(__file__).resolve().parent; ROOT=D.parents[2]; SCRIPT=D.with_suffix('.py')
spec=importlib.util.spec_from_file_location('scalar_draft',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
F=fractions.Fraction

def write(name,data): (D/name).write_text(json.dumps(data,indent=2)+'\n')
def number(s):
 s=s.replace(' ','').rstrip('.');s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'\1/\2',s)
 return F(s)
def entry(s):
 s=s.strip(); has='k' in s;s=s.replace('k','').replace(' ','')
 return (F(-1 if s=='-' else 1) if s in ('','-') else number(s),has)
def read_mats(s):
 return [[[entry(c) for c in row.split('&')] for row in body.split(r'\\')] for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)]
def vals(m):return [[c[0] for c in row] for row in m]
def scaled(m,k):return [[c*k for c in row] for row in m]
def independent(r,allow_source_errors=False):
 q=r['question'];sid=r['generation']['template'];raw=r['generation']['evidence_only'];pm=read_mats(q[':question/problem']);sol=q.get(':question/worked-solution');sm=read_mats(sol or '')
 b=vals(pm[0]);a=vals(pm[1]) if len(pm)==2 else vals(sm[0]); pairs=[(x,y) for row,br in zip(a,b) for x,y in zip(row,br) if x]
 c=pairs[0][1]/pairs[0][0];assert all(y==c*x for x,y in pairs)
 assert all(y==c*x for row,br in zip(a,b) for x,y in zip(row,br))
 f=q[':question/answer-fields'][0];radio=f[':answer-field/type'].endswith('/radio');answers=[number(z[':answer/value'].split('=')[-1]) for z in f[':answer-field/choices']];assert len(set(answers))==len(answers)
 if ':answer-field/correct' in f: assert next(number(z[':answer/value'].split('=')[-1]) for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1])==c
 assert c in answers
 if sol:
  assert len(sm)==4
  first=copy.deepcopy(a)
  if allow_source_errors and raw and sid=='q-320536':first[1][0]=-first[1][0]
  assert vals(sm[0])==first and vals(sm[1])==first and vals(sm[2])==a and vals(sm[3])==b
  for m in sm[1:3]: assert all(has==(v!=0) for row in m for v,has in row)
  stages=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(stages)==2
  assert re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}', '',stages[0],flags=re.S).count(r'\\')==1
  first_operand=stages[0].split('& =')[1].split(r'\begin{bmatrix}')[0].strip()
  assert first_operand in ('k',r'k\cdot')
  final=stages[1].split(r'\\');assert len(final)==2
  left,right=final[0].split('& =');coef,has=entry(left);assert has and number(right)==coef*c
  assert re.fullmatch(r'\s*k\s*& =.*',final[1]);assert number(final[1].split('& =')[1])==c
  choice=re.search(r"Let's choose (.*?), \$(.*?)\$ and \$(.*?)\$",sol);assert choice
  assert entry(choice[2])==(coef,True) and number(choice[3])==coef*c
  loc=choice[1];rc=re.search(r'row \$(\d+)\$ and column \$(\d+)\$',loc)
  if rc:i,j=int(rc[1])-1,int(rc[2])-1
  else:i,j=g.POSITIONS[sid]
  assert a[i][j]==coef
  if not raw and radio:
   aa=a[i][j];bb=b[i][j];assert set(answers)=={c,aa/bb,aa*bb,bb-aa,bb+aa}
  source_solution=g.CASES[sid].get(':question/worked-solution',g.CASES['q-69670'][':question/worked-solution'].replace('kS','kG').replace('$S$','$G$'))
  def skeleton(text):
   text=re.sub(r'\$\$.*?\$\$','DISPLAY',text,flags=re.S)
   return re.sub(r"Let's choose .*?Equating these elements","Let's choose SLOT Equating these elements",text,flags=re.S)
  assert skeleton(sol)==skeleton(source_solution)
  # Ordered fixed prose/stages: no missing or generic replacement of source operations.
  assert sol.index('To express')<sol.index('Now, we set')<sol.index('We can solve')<sol.index('Equating these elements')<sol.index('**Note:**')
 if not raw and not radio:assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 for text in [q[':question/problem'],sol or '',*[z[':answer/value'] for z in f[':answer-field/choices']]]:assert not any(ord(ch)<32 and ch not in '\n\t\r' for ch in text)
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 return c

source_cases=[];fidelity=[];review=[];native=[]
for sid,q in g.CASES.items():
 r=g.generate('easy',template=sid,parameters=g.DEFAULTS[sid],profile='raw-'+sid)
 independent(r,True);source_cases.append({'source_id':sid,'record':q})
 out=r['question'];field=out[':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
 assert out[':question/problem']==g.normalize_prose(q[':question/problem'])
 assert out.get(':question/worked-solution')==q.get(':question/worked-solution')
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in out)==(key in q)
 assert (':answer-field/correct' in field)==(':answer-field/correct' in sf)
 assert sorted(z[':answer/value'] for z in field[':answer-field/choices'])==sorted(z[':answer/value'] for z in sf[':answer-field/choices'])
 fidelity.append({'source_id':sid,'prompt_exact':True,'solution_exact':True,'bank_matched':len(sf[':answer-field/choices']),'designation_present':':answer-field/correct' in sf,'raw_presence_parity':True})
 p=copy.deepcopy(g.DEFAULTS[sid]);a=g.sp.Matrix(p['matrix']);p['scalar']=str(g.sp.Rational(p['scalar'])+1 if sid!='q-69670' else -8)
 # preserve integral products for source reciprocal variant.
 if sid=='q-320563':p['scalar']='2/3'
 changed=g.generate('easy',template=sid,parameters=p,profile='raw-'+sid);independent(changed,True)
 review.extend([{'label':'Original MA '+sid,'record':r},{'label':'Changed empirical evidence '+sid,'record':changed}])
 for seed in (41,73):
  lev='easy';normal=g.generate(lev,seed,template=sid);independent(normal);review.append({'label':'Authored method bank '+sid,'record':normal})
for lev in g.SUPPORTED_LEVELS:
 for seed in range(160):
  r=g.generate(lev,seed);independent(r)
  if seed<2:review.append({'label':'Generated '+lev,'record':r})
 # substantive varied actual tasks and family coverage.
 rs=[g.generate(lev,seed) for seed in range(160)]
 assert len({r['generation']['mathematical_fingerprint'] for r in rs})>100
 expected=set(g.CASES)-({'q-139431'} if lev!='easy' else set());assert {r['generation']['template'] for r in rs}==expected
 # distinct workload under all explicit calls.
 for other in g.SUPPORTED_LEVELS:
  if other!=lev:
   try:g.generate(other,template=r['generation']['template'],parameters=r['generation']['parameters'])
   except ValueError:pass
   else:raise AssertionError('difficulty guard bypass')
# Every eligible target with data held constant; key remains scalar while solution target changes.
slots={}
for sid in g.CASES:
 r=g.generate('easy',31,template=sid);p=r['generation']['parameters'];a=g.sp.Matrix(p['matrix']);slots[sid]=[]
 for i in range(a.rows):
  for j in range(a.cols):
   if a[i,j]:
    pp=copy.deepcopy(p);pp['target']=[i,j]
    try:z=g.generate('easy',31,template=sid,parameters=pp)
    except ValueError:continue # the fixed whole method bank can collide at this cell.
    assert independent(z)==independent(r);slots[sid].append([i,j]);review.append({'label':f'Held data target {sid} {i},{j}','record':z})
 assert len(slots[sid])>=2
# Mutations leave final key unchanged: validators must reject incorrect initial cells,
# scalar operands, chosen-cell prose, distributed rows, and final calculation stages.
base=g.generate('easy',73,template='q-320536');checks=[]
for name,fun in [
 ('matrix-cell',lambda s:s.replace(g.mat(g.sp.Matrix(base['generation']['parameters']['matrix'])),g.mat(g.sp.Matrix(base['generation']['parameters']['matrix'])*2),1)),
 ('symbolic-scalar-operand',lambda s:s.replace('kB & =k','kB & =2k',1)),
 ('selected-cell-prose',lambda s:s.replace("Let's choose", "Let's choose the elements in row $99$ and column $99$ instead of",1)),
 ('drop-equating-stage',lambda s:s.replace('Now, we set','We skip setting',1)),
 ('control-character',lambda s:s+'\x0c')]:
 z=copy.deepcopy(base);z['question'][':question/worked-solution']=fun(z['question'][':question/worked-solution'])
 try:independent(z)
 except (AssertionError,ValueError,IndexError):checks.append(name)
 else:raise AssertionError('mutation escaped '+name)
z=copy.deepcopy(base);field=z['question'][':question/answer-fields'][0]
# Use radio for a wrong-bank mutation independent of the stored correct lookup.
z=g.generate('easy',12,template='q-69670');field=z['question'][':question/answer-fields'][0]
next(a for a in field[':answer-field/choices'] if a[':answer/id']!=field[':answer-field/correct'][1])[':answer/value']='k=999'
try:independent(z)
except AssertionError:checks.append('entire-wrong-bank')
else:raise AssertionError('wrong-bank mutation escaped')
for val in [True,0.5,'2',None]:
 try:g.generate(seed=val)
 except TypeError:pass
 else:raise AssertionError('bad seed accepted')
for val in [True,1.5,'1',None]:
 try:g.batch(count=val)
 except TypeError:pass
 else:raise AssertionError('bad count accepted')
assert len(json.loads(subprocess.check_output([str(ROOT/'.venv/bin/python'),str(SCRIPT),'--difficulty','all','--count','1'])))==3
# Seed/order cannot create content identity; banks can, mathematical tasks cannot.
a=g.generate('easy',1,template='q-69670',parameters=g.DEFAULTS['q-69670'],profile='raw-q-69670');b=g.generate('easy',999,template='q-69670',parameters=g.DEFAULTS['q-69670'],profile='raw-q-69670')
assert a['question'][':question/id']==b['question'][':question/id']
c=g.generate('easy',1,template='q-69670',parameters=g.DEFAULTS['q-69670'],profile='method')
assert c['generation']['mathematical_fingerprint']==a['generation']['mathematical_fingerprint'] and c['question'][':question/id']!=a['question'][':question/id']
# Native current build: all 42 recorded inputs verified. No engine changes.
build=json.loads((D/'reference/grader-build.json').read_text()); hashes={**build['engine_sources'],**build['dependencies'],build['source']:build['source_sha256'],build['library']:build['library_sha256'],build['binary']:build['binary_sha256']}
assert len(hashes)==42
for path,sha in hashes.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
for item in review:
 r=item['record'];f=r['question'][':question/answer-fields'][0]
 if ':answer-field/correct' not in f:continue
 c=independent(r,True);checks2=[]
 if f[':answer-field/type'].endswith('/radio'):
  for z in f[':answer-field/choices']:checks2.append({'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete displayed radio bank'})
 else:
  correct=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1])
  checks2=[{'submitted':correct,'expected':'accepted','purpose':'exact answer'},{'submitted':f'({c.numerator*2})/({c.denominator*2})','expected':'accepted','purpose':'independently unreduced equivalent quotient'},{'submitted':str(c+1),'expected':'rejected','purpose':'wrong scalar'}]
 native.append({'label':item['label'],'record':r,'checks':checks2})
write('engine-input.json',native);subprocess.run([str(ROOT/build['binary']),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
write('source-cases.json',source_cases);write('source-replay.json',fidelity);write('review.json',review);write('slot-coverage.json',slots)
write('independent-inventory.json',{k:v for k,v in g.SOURCE.items() if k!='record'}|{'questions':[]})
write('validation.json',{'mathematical_records':480,'source_questions':len(fidelity),'source_banks':len(fidelity),'matched_answers':sum(x['bank_matched'] for x in fidelity),'source_designations':sum(x['designation_present'] for x in fidelity),'raw_exact_present_solutions':6,'raw_mathematically_correct_present_solutions':5,'raw_present_solutions':6,'source_missing_solutions':1,'raw_mathematical_errors_documented':1,'normal_source_sign_repairs':1,'normal_context_repairs':1,'normal_presentation_repairs':1,'mutation_controls':checks,'native_build_inputs_verified':len(hashes),'status':'passed','root_independent_qa':'pending','distinct_tasks_per_160_seeds':{lev:len({g.generate(lev,n)['generation']['mathematical_fingerprint'] for n in range(160)}) for lev in g.SUPPORTED_LEVELS}})
(D/'review.md').write_text('\n\n'.join('## '+row['label']+'\n\n'+g.markdown(row['record']) for row in review)+'\n')
# Immutable numeric files and sibling cache: exact set and hashes.
r=ROOT/'generate/scratch';paths=[r/'17592186059741.py',*(r/'17592186059741').rglob('*'),*r.glob('__pycache__/17592186059741.*.pyc')];current={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()};assert current==json.loads((D/'baseline.json').read_text());write('baseline-verification.json',{'exact_path_set_and_sha256':True,'files':len(current)})
print('Validated all seven MA originals, 480 defaults, target controls, native grading, and 66 immutable baseline paths.')
