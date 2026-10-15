"""Independent rendered-TeX arithmetic, source complete banks and native grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('draft_unit',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)
def group(s):
 assert s[0]=='{',s
 depth=0
 for i,c in enumerate(s):
  depth+=(c=='{')-(c=='}')
  if not depth:return s[1:i],s[i+1:]
 raise ValueError('unbalanced')
def same(a,b):
 if isinstance(a,sp.MatrixBase) or isinstance(b,sp.MatrixBase):
  return isinstance(a,sp.MatrixBase) and isinstance(b,sp.MatrixBase) and a.shape==b.shape and all(sp.simplify(v)==0 for v in a-b)
 return sp.simplify(a-b)==0

def expr(s,env=None):
 env=dict(env or {});s=s.strip().rstrip('.').replace('&','').replace(r'\,','').replace(r'\mid','|').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*')
 s=re.sub(r'\\mathbf\{([^{}]+)\}',r'\1',s)
 def mat(m):
  name='M'+str(len(env));env[name]=sp.Matrix([expr(t,env) for t in m[1].split(r'\\')]);return name
 s=re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',mat,s,flags=re.S)
 def norm(m):
  name='N'+str(len(env));v=expr(m[1],env);env[name]=sp.sqrt(sum(z*z for z in v));return name
 s=re.sub(r'\|([^|]+)\|',norm,s)
 while r'\frac' in s or r'\sqrt' in s:
  # replace innermost macro first (its arguments can themselves contain macros).
  positions=[(s.rfind(r'\frac'),'frac'),(s.rfind(r'\sqrt'),'sqrt')];i,kind=max(positions)
  if i<0:break
  size=5;before=s[:i];arg,tail=group(s[i+size:].lstrip())
  if kind=='frac':den,tail=group(tail.lstrip());replacement='(('+str_expr(arg)+')/('+str_expr(den)+'))'
  else:replacement='sqrt('+str_expr(arg)+')'
  s=before+replacement+tail
 s=str_expr(s)
 return parse_expr(s,local_dict={**env,'sqrt':sp.sqrt},transformations=TRANS)
def str_expr(s):return s.replace('{','(').replace('}',')').replace('^','**')
def matrices(text):return [expr(m[0]) for m in re.finditer(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def task(q):
 vs=matrices(q[':question/problem']);target=re.search(r'parallel to \$(.*?)\$',q[':question/problem'])[1]
 if len(vs)==2:env={'a':vs[0],'b':vs[1]}
 else:
  label=re.search(r'Let \$([a-z])',q[':question/problem'])[1];env={label:vs[0]}
 v=expr(target,env);n=sp.sqrt(sum(z*z for z in v));return v,n,env,target

def solution(q,allow_missing=False):
 v,n,env,target=task(q);assert n>0;env['u']=v/n
 text=q.get(':question/worked-solution')
 if not text:
  assert allow_missing;return 0
 count=0
 for block in re.findall(r'\$\$(.*?)\$\$',text,re.S):
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  # Protect vector row separators before separating aligned rows.
  protected=[]
  def keep(m):protected.append(m[0]);return '@'+str(len(protected)-1)+'@'
  block=re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',keep,block,flags=re.S)
  previous=None
  for row in block.split(r'\\'):
   for i,value in enumerate(protected):row=row.replace('@'+str(i)+'@',value)
   if not row.strip():continue
   parts=row.replace('&','').split('=');assert len(parts)==2,row
   left,right=parts;value=expr(right,env)
   if left.strip():assert same(expr(left,env),value),(left,right)
   else:assert previous is not None and same(previous,value),(previous,right)
   previous=value;count+=1
 return count

def check(q,allow_missing=False):
 v,n,env,target=task(q);equalities=solution(q,allow_missing);f=q.get(':question/answer-fields',[])
 if not f:return {'equalities':equalities,'options':0,'eligible':False}
 assert len(f)==1;f=f[0];choices=f[':answer-field/choices'];values=[expr(a[':answer/value']) for a in choices]
 assert len(choices)==5
 for i,a in enumerate(values):assert all(not same(a,b) for b in values[:i])
 positive='same direction' in q[':question/problem']
 valid=[]
 for i,a in enumerate(values):
  unit=same(a.dot(a),1);parallel=same(v[0]*a[1]-v[1]*a[0],0);direction=sp.simplify(v.dot(a))>0
  if unit and parallel and (not positive or direction):valid.append(i)
 assert len(valid)==1,(target,valid)
 key=f.get(':answer-field/correct')
 if key:
  cid=key[1] if isinstance(key,list) else key[':answer/id'];assert cid==choices[valid[0]][':answer/id']
 return {'equalities':equalities,'options':len(values),'eligible':bool(key),'inferred_correct_index':valid[0]}

def source_parameter(q):
 v,n,env,target=task(q);p={'x':int(v[0]),'y':int(v[1])}
 if len(env)==1:return {**p,'mode':'direct','label':list(env)[0]}
 t=re.sub(r'\\mathbf\{(.*?)\}',r'\1',target).replace(' ','');m=re.fullmatch(r'(\d*)a\+(\d*)b',t)
 return {**p,'mode':'combination','ca':int(m[1] or 1),'cb':int(m[2] or 1),'a1':int(env['a'][0]),'a2':int(env['a'][1])}

def main():
 raw=json.loads((D/'source.json').read_text());qs=raw['record'][':knowledge-point/questions'];ma=[q for q in qs if ':question/math-academy-id' in q];non=[q for q in qs if q not in ma]
 findings=[];replays=[];native=[];equality_count=0;options=0;rendered=[]
 for q in [raw['record'][':knowledge-point/canonical-example'],*qs]:
  sourceid=q.get(':question/math-academy-id','inventory-'+str(q[':db/id']));result=check(q,True);equality_count+=result['equalities'];options+=result['options'];p=source_parameter(q)
  profile='q-125135' if sourceid=='q-125135' else ('q-18058' if sourceid in ('q-18058','q-70409') else 'q-17709')
  bank_coverage=None
  if q.get(':question/answer-fields'):
   vals,index=g.bank(profile,p['x'],p['y']);actual=[expr(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
   matches=[[i for i,b in enumerate(vals) if same(a,sp.Matrix(b))] for a in actual];assert all(len(m)==1 for m in matches);assert len({m[0] for m in matches})==5
   bank_coverage={'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'recipe_mapping':matches,'source_key_present':result['eligible']}
  if p['x'] and p['y']:
   rec=g.generate('hard' if p['mode']=='combination' else 'moderate',p,profile)
   check(rec['question']);rendered.append(rec)
   # source sentences retained, no source operative stage dropped.
   original=q.get(':question/worked-solution','');generated=rec['question'][':question/worked-solution']
   for sentence in ('First, let\'s compute the sum:','Using the formula for the magnitude of a vector, we get','Finally, we divide'):
    if sentence in original:assert sentence in generated
   if original:
    assert result['equalities']<=solution(rec['question'])
    prose=lambda text: ' '.join(re.sub(r'\$\$.*?\$\$|\$(?:\\.|[^$])*?\$', '<math>',text,flags=re.S).split())
    assert prose(original)==prose(generated),(sourceid,prose(original),prose(generated))
  findings.append({'source_id':sourceid,'role':'MA practice' if q in ma else ('canonical' if q not in qs else 'nonMA captured inventory'),'parameters':p,**result,'complete_bank':bank_coverage,'raw_eligible':result['eligible'],'missing_fields':not bool(q.get(':question/answer-fields')),'missing_solution':not bool(q.get(':question/worked-solution'))})
 samples=[];coverage={};all_count=0
 for level in g.SUPPORTED_LEVELS:
  rows=g.catalog(level);indices=range(len(rows)) if level=='easy' else sorted(set([0,1,2,len(rows)-1,*range(0,len(rows),max(1,len(rows)//90))]))
  checked=[]
  for i in indices:
   p,profile=rows[i];rec=g.generate(level,p,profile,17);r=check(rec['question']);equality_count+=r['equalities'];options+=r['options'];checked.append(rec);all_count+=1
  assert len({g.task_fingerprint(p) for p,profile in rows})==len(rows)
  assert g.batch(level,3,7)==g.batch(level,3,7)
  assert len(g.batch(level,1,2))==1
  for count,seed in [(True,0),(1,False),(1.0,0),(1,2.0),(0,0),(-1,0),(len(rows)+1,0)]:
   try:g.batch(level,count,seed)
   except (ValueError,TypeError):pass
   else:raise AssertionError('boundary accepted')
  for fmt in ['json','markdown']:
   for count in [1,3]:
    output=subprocess.check_output([sys.executable,str(D.with_suffix('.py')),'--difficulty',level,'--count',str(count),'--seed','2','--format',fmt],text=True)
    if fmt=='json':assert isinstance(json.loads(output),list) and len(json.loads(output))==count
    else:assert output.count('Find a unit vector')==count
  samples+=checked[:3];rendered+=checked[:3]
  coverage[level]={'capacity':len(rows),'independently_checked':len(checked),'x_values':sorted({p['x'] for p,_ in rows}),'y_values':sorted({p['y'] for p,_ in rows}),'profiles':sorted({profile for _,profile in rows}),'coefficient_pairs':sorted({(p['ca'],p['cb']) for p,_ in rows if p['mode']=='combination'}),'operand_first_coordinates':sorted({p['a1'] for p,_ in rows if p['mode']=='combination'}),'operand_second_coordinates':sorted({p['a2'] for p,_ in rows if p['mode']=='combination'})}
  # All finite domains get exact bank uniqueness and designation algebraically;
  # parsed rendered equality tests above separately cover every slot boundary.
  for p,profile in rows:
   values,ci=g.bank(profile,p['x'],p['y']);n=sp.sqrt(p['x']**2+p['y']**2);target=sp.Matrix([p['x']/n,p['y']/n]);assert same(sp.Matrix(values[ci]),target)
   assert len(set(values))==5, 'canonical exact SymPy bank collision'
 for p in g.original_parameters():check(g.generate('hard' if p['mode']=='combination' else 'moderate',p)['question'])
 # Negative controls: mutate rendered intermediate arithmetic, keep final correct.
 control=copy.deepcopy(g.generate('hard',g.original_parameters()[0]));text=control['question'][':question/worked-solution'];control['question'][':question/worked-solution']=text.replace('0+(5)','1+(5)',1)
 assert text!=control['question'][':question/worked-solution']
 try:check(control['question'])
 except AssertionError:pass
 else:raise AssertionError('invalid intermediate accepted')
 for old,new in [(r'\sqrt{169}',r'\sqrt{170}'),(r'\frac{1}{13}',r'\frac{1}{14}')]:
  bad=copy.deepcopy(g.generate('hard',g.original_parameters()[0]));before=bad['question'][':question/worked-solution'];bad['question'][':question/worked-solution']=before.replace(old,new,1);assert before!=bad['question'][':question/worked-solution']
  try:check(bad['question'])
  except AssertionError:pass
  else:raise AssertionError('invalid magnitude/normalization intermediate accepted')
 # Parallel-only meaning admits the negative unit direction; directional wording does not.
 v=sp.Matrix([3,4]);assert same((-v/5).dot(-v/5),1) and same(v[0]*(-v/5)[1]-v[1]*(-v/5)[0],0) and v.dot(-v/5)<0
 for rec in [*samples,*rendered[:10]]:
  f=rec['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'Canonical radio selection; every rendered option independently checked'} for a in f[':answer-field/choices']]
  native.append({'label':rec['question'][':question/id'],'record':rec,'checks':checks})
 (D/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n');subprocess.run([str(D/'check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 # Every original supported field, missing key explicitly inferred in synthetic local fixture.
 sourcefixtures=[]
 for q in qs:
  if not q.get(':question/answer-fields'):continue
  qq=copy.deepcopy(q);f=qq[':question/answer-fields'][0];r=check(qq,True)
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
  f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][r['inferred_correct_index']][':answer/id']]
  rec={'question':qq,'knowledge_point':{'title':g.TITLE},'generation':{'template':'source-local-key-fixture'}};sourcefixtures.append({'label':q[':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==r['inferred_correct_index'] else 'rejected','purpose':'Captured complete original bank; missing keys inferred only in local synthetic fixture'} for i,a in enumerate(f[':answer-field/choices'])]})
 (D/'source-engine-input.json').write_text(json.dumps(sourcefixtures,indent=2)+'\n');subprocess.run([str(D/'check-engine'),str(D/'source-engine-input.json'),str(D/'source-engine-report.json')],check=True)
 (D/'samples.json').write_text(json.dumps(samples,indent=2)+'\n');(D/'review.json').write_text(json.dumps([{'record':r} for r in rendered],indent=2)+'\n');(D/'source-findings.json').write_text(json.dumps(findings,indent=2)+'\n')
 baseline=json.loads((D/'reference/registered-baseline.json').read_text());changed=[z['path'] for z in baseline['paths'] if not Path(z['path']).exists() or hashlib.sha256(Path(z['path']).read_bytes()).hexdigest()!=z['sha256']];assert not changed
 registered=ROOT/'generate/scratch/17592186059716';actual={str(p.relative_to(ROOT)) for p in registered.rglob('*') if p.is_file()}|{'generate/scratch/17592186059716.py'}|{str(p.relative_to(ROOT)) for p in (registered.parent/'__pycache__').glob('17592186059716*') if p.is_file()}
 assert actual=={z['path'] for z in baseline['paths']},'registered path inventory changed'
 assert {str(p.relative_to(ROOT)) for p in [registered,*registered.rglob('*')] if p.is_dir()}==set(baseline['tree_directories'])
 (D/'registered-baseline-verification.json').write_text(json.dumps({'unchanged':True,'files':len(baseline['paths']),'complete_path_inventory_unchanged':True,'directories_unchanged':True,'cache_paths_unchanged':True,'changed':changed},indent=2)+'\n')
 report={'status':'ready for independent ROOT QA, not approved','basis':2275,'source_counts':{'MA_practice':len(ma),'canonical':1,'nonMA_captured_inventory':len(non),'MA_complete_banks':3,'MA_complete_choices':15,'MA_distractors':12,'nonMA_complete_banks':5,'nonMA_complete_choices':25,'nonMA_distractors':20,'all_captured_complete_banks':8,'all_captured_choices':40},'parsed_rendered_equalities':equality_count,'parsed_options':options,'independently_checked_generated':all_count,'variation':coverage,'negative_controls':{'invalid_intermediate_final_unchanged':'sum, magnitude and reciprocal normalization mutations rejected','parallel_only_opposite_unit':'mathematically valid; no negative-key inference'},'native_field':'radio: canonical ID selection and every wrong option; textual equivalent entry not supported by this field contract','source_limitations':'2 MA complete banks lack keys; 2 MA and canonical lack fields; q17709/q18058 lack worked solutions; canonical prompt omits a/b labels; immutable raw evidence retained. Local synthetic repairs explicitly qualified.','registered_baseline_unchanged':True}
 report.update(current_engine_build_manifest='reference/grader-build.json',source_json_sha256=hashlib.sha256((D/'source.json').read_bytes()).hexdigest(),source_byte_exact=(D/'source.json').read_bytes()==(ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186059716.json').read_bytes(),all_source_worked_solutions_every_equality_checked=True,canonical_generated_replay_limit='Axis-vector canonical has no captured field or applicable complete five-choice source bank; only immutable raw source/solution replay is eligible for evidence, no field invented.',full_finite_domain_validation='Every bank in all24/510/1596 finite tasks checked using canonical exact SymPy expressions for pairwise distinctness and correct normalization; rendered-text equality chains and independent unit/parallel/direction tests are exhaustive for easy, representative for moderate/hard as counted.')
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
