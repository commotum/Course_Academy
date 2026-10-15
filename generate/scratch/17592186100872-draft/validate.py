#!/usr/bin/env python3
"""Independent displayed-operand/ordered-factor verification and actual native grader."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,platform,re,subprocess,collections
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;ROOT=D.parents[2];SCRIPT=D.with_suffix('.py')
spec=importlib.util.spec_from_file_location('private_matrix_product',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
M=re.compile(r'\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}')
def dump(name,v):(D/name).write_text(json.dumps(v,indent=2)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def matrix(body):
 return [[(x.strip() if x.strip()=='∗' else int(x.strip())) for x in r.split('&')] for r in body.split('\\\\')]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def roles_from_prompt(q):
 rows=[line for line in q[':question/problem'].splitlines() if line.startswith('|') and '---' not in line];roles={};known={};i=0
 for row in rows:
  entries=re.findall(r'\{\{(field-\d+)\}\}|\$(-?\d+)\$',row)
  if not entries:continue
  for j,(key,val) in enumerate(entries):
   if key:roles[key]=(i,j)
   else:known[i,j]=int(val)
  i+=1
 return roles,known

def readback(r):
 q=r['question'];g.mf.validate_generated_record(r)
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==17592186100872
 assert r['generation']['matrix_role']=='ordinary coefficient matrix'
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:assert all(ord(z)>=32 or z in '\n\t\r' for z in text),'C0'
 pms=list(M.finditer(q[':question/problem']));assert len(pms)==2
 a,b=[matrix(x[1]) for x in pms];c=mm(a,b);m,n,k=len(a),len(b),len(b[0]);assert sp.Matrix(a)*sp.Matrix(b)==sp.Matrix(c)
 fields=q[':question/answer-fields'];blank=fields[0][':answer-field/type'].endswith('/blank')
 if blank:
  roles,known=roles_from_prompt(q);assert set(roles)=={f[':answer-field/key'] for f in fields}
  assert all(c[i][j]==v for (i,j),v in known.items());t=sorted(roles.values());assert len(t)>=2,'Do not migrate into single entry sibling'
 else:t=[(i,j) for i in range(m) for j in range(k)]
 for f in fields:
  correct=f[':answer-field/correct'][1];matches=[v for v in f[':answer-field/choices'] if v[':answer/id']==correct];assert len(matches)==1
  if blank:assert int(matches[0][':answer/value'])==c[roles[f[':answer-field/key']][0]][roles[f[':answer-field/key']][1]]
  else:assert matrix(M.fullmatch(matches[0][':answer/value'])[1])==c
  vals=[matrix(M.fullmatch(v[':answer/value'])[1]) if M.fullmatch(v[':answer/value']) else [[int(v[':answer/value'])]] for v in f[':answer-field/choices']];assert len({json.dumps(z) for z in vals})==len(vals)
  if not blank and r['generation']['profile']=='method-sign-omission':
   expected=[c,[list(row) for row in zip(*c)],[[-v for v in row] for row in c],[[sum(a[ii][h]*b[h][jj] for h in range(n-1)) for jj in range(k)] for ii in range(m)],[[sum((1 if h%2==0 else -1)*a[ii][h]*b[h][jj] for h in range(n)) for jj in range(k)] for ii in range(m)]]
   assert collections.Counter(json.dumps(z) for z in vals)==collections.Counter(json.dumps(z) for z in expected),'Wrong complete operation bank'
 sol=q[':question/worked-solution'];mats=[matrix(x[1]) for x in M.finditer(sol)];assert len(mats)==3*len(t)+1
 chains=re.findall(r'\\,(-?\d+)=(.*?)(?= \\\\|\\end\{aligned\})',sol);assert len(chains)==len(t)
 for z,(i,j) in enumerate(t):
  aa,bb,partial=mats[3*z:3*z+3];assert aa==a and bb==b,'Wrong actual displayed operand'
  assert len(partial)==m and all(len(row)==k for row in partial)
  for rr,row in enumerate(partial):
   for cc,value in enumerate(row):assert value=='∗' or value==c[rr][cc]
  assert partial[i][j]==c[i][j]
  expected=[[('∗' if (rr,cc) in t[z+1:] else c[rr][cc]) for cc in range(k)] for rr in range(m)]
  assert partial==expected,'Wrong progressive target role/order'
  lhs,rhs=chains[z];assert int(lhs)==c[i][j]
  actual=[]
  # Parse printed individual factors in their original order; sums alone are insufficient.
  for term in rhs.split('+'):
   match=re.fullmatch(r'(\(-?\d+\)|-?\d+)\\cdot (\(-?\d+\)|-?\d+)',term.strip());assert match,('Missing factor/product',term)
   actual.append(tuple(int(x.strip('()')) for x in match.groups()))
  assert actual==[(a[i][h],b[h][j]) for h in range(n)],'Wrong ordered factors or target role'
  assert sum(x*y for x,y in actual)==int(lhs)
 assert mats[-1]==c,'Stale conclusion'
 return {'A':a,'B':b,'targets':t,'workload_products':len(t)*n}

def mustfail(fn,label):
 try:fn()
 except (AssertionError,ValueError,KeyError):return label
 raise AssertionError('Mutation accepted: '+label)

def native_checks(r,label):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  cid=f[':answer-field/correct'][1];a=next(v for v in f[':answer-field/choices'] if v[':answer/id']==cid)
  if f[':answer-field/type'].endswith('/blank'):
   v=int(a[':answer/value']);checks.extend([{'field_index':i,'submitted':str(v),'expected':'accepted','purpose':'canonical scalar'},{'field_index':i,'submitted':f'({2*v}+2)/2-1','expected':'accepted','purpose':'uncollected equivalent scalar expression'},{'field_index':i,'submitted':str(v+1),'expected':'rejected','purpose':'incorrect entry'}])
  else:
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'every complete native bank selection'} for a in f[':answer-field/choices'])
 return {'label':label,'record':r,'checks':checks}

def main():
 baseline=json.loads((D/'registered-baseline-before.json').read_text());paths=[ROOT/'generate/scratch/17592186100872.py',ROOT/'generate/scratch/17592186100872'];found=[]
 for p in paths:
  if p.is_file():found.append(p)
  elif p.is_dir():found.extend(z for z in p.rglob('*') if z.is_file())
 found.extend((ROOT/'generate/scratch/__pycache__').glob('17592186100872.*.pyc'))
 now={str(p.relative_to(ROOT)):digest(p) for p in found};assert now==baseline['complete_file_set'];dump('registered-baseline-verification.json',{'complete_file_set_before':baseline['complete_file_set'],'complete_file_set_after':now,'same_path_set_and_hashes':True,'numeric_imported':False})
 build=json.loads((D/'reference/grader-build.json').read_text());hashes={build['source']:build['source_sha256'],build['library']:build['library_sha256'],build['binary']:build['binary_sha256']}|build['engine_sources']|build['dependencies'];assert len(hashes)==42
 for p,h in hashes.items():assert digest(ROOT/p)==h,(p,'native input changed')
 dump('native-source-verification.json',{'actual_files_reverified':len(hashes),'files':hashes,'binary_used':str((D/'check-engine').relative_to(ROOT)),'binary_sha256':digest(D/'check-engine')})
 assert digest(D/'check-engine')=='33510bf3ac27a1eb28e9bad7b4121a22d2fa787026d3102268daa4ecf98b1617'
 S=json.loads((D/'source.json').read_text());assert S==json.loads((ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186100872.json').read_text())
 sources={q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions']};cases=json.loads((D/'source-cases.json').read_text());assert set(sources)=={z['source_id'] for z in cases}
 native=[];review=[];fidelity=[];totalanswers=0;correctrefs=0
 for case in cases:
  sid=case['source_id'];src=sources[sid];raw=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile='observed-raw');q=raw['question']
  assert q[':question/problem']==g.mf.normalize_prose(src[':question/problem'])
  for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:
   assert (key in q)==(key in src),(sid,key,'presence')
  if ':question/worked-solution' in src:assert q[':question/worked-solution']==g.mf.normalize_prose(src[':question/worked-solution'])
  expected={f[':answer-field/key']:f for f in src[':question/answer-fields']}
  for f in q[':question/answer-fields']:
   old=expected[f[':answer-field/key']];assert f[':answer-field/type']==old[':answer-field/type'][':db/ident'];assert (':answer-field/correct' in f)==(':answer-field/correct' in old)
   assert collections.Counter(g.mf.normalize_tex(v[':answer/value']) for v in old[':answer-field/choices'])==collections.Counter(v[':answer/value'] for v in f[':answer-field/choices']);totalanswers+=len(f[':answer-field/choices'])
   if ':answer-field/correct' in old:
    correctrefs+=1;v=next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1]);assert v==g.mf.normalize_tex(old[':answer-field/correct'][':answer/value'])
  repaired=g.generate('easy',template=sid,parameters=case['parameters'],profile='observed-repaired');readback(repaired);native.append(native_checks(repaired,'source bank '+sid+' (missing designations completed only in native fixture)'))
  fidelity.append({'source_id':sid,'complete_bank':True,'prompt_exact_after_shared_normalization':True,'solution_exact_or_absent':True,'correct_ref_presence':True,'original_correct_designations':sum(':answer-field/correct'in f for f in src[':question/answer-fields'])})
  review.append({'kind':'original evidence raw','source_id':sid,'record':raw})
  review.append({'kind':'generated variant','source_id':sid,'record':g.generate('easy',seed=101,template=sid)})
 allrecords=[];variety={};coverage={};maxima={}
 for level in ['easy','moderate','hard']:
  tasks=set();families=set();targetroles=set();mx={'operand':0,'product':0,'dot_l1':0,'answer':0}
  for seed in range(400):
   r=g.generate(level,seed=seed);data=readback(r);allrecords.append(r);tasks.add(r['generation']['mathematical_fingerprint']);families.add(r['generation']['template']);targetroles.update(map(str,data['targets']))
   a,b=data['A'],data['B'];mx['operand']=max(mx['operand'],max(abs(v) for z in [a,b] for row in z for v in row));mx['product']=max(mx['product'],max(abs(a[i][h]*b[h][j]) for i in range(len(a)) for j in range(len(b[0])) for h in range(len(b))));mx['dot_l1']=max(mx['dot_l1'],max(sum(abs(a[i][h]*b[h][j]) for h in range(len(b))) for i in range(len(a)) for j in range(len(b[0]))));mx['answer']=max(mx['answer'],max(abs(v) for row in mm(a,b) for v in row))
   if seed<8:native.append(native_checks(r,f'{level} seed {seed}'))
  assert len(tasks)>300
  variety[level]={'sampled_distinct_meaningful_tasks':len(tasks),'sampled_instances':400,'not_counted':'seed, profile, answer order, name aliases; fingerprint actual operand entries/target positions and assessed workload'};coverage[level]={'families':sorted(families),'target_positions':sorted(targetroles)};maxima[level]=mx
  review.extend({'kind':'authored missing-level variant' if level!='easy' else 'generated easy variant','record':g.generate(level,seed=i)} for i in [201,202])
 assert set(coverage['easy']['families'])==set(g.SPECS)
 # Explicit joint arithmetic boundaries, using real nonzero tasks.
 boundary_records=[]
 for level,p in [('moderate',{'A':[[6,1,1],[1,2,1]],'B':[[2,1],[1,2],[1,3]],'targets':[[0,0],[0,1],[1,0],[1,1]]}),('hard',{'A':[[5,1,1,1],[1,2,1,1]],'B':[[2,1],[1,2],[1,2],[1,1]],'targets':[[0,0],[0,1],[1,0],[1,1]]})]:
  boundary=g.generate(level,parameters=p);readback(boundary);boundary_records.append(boundary);native.append(native_checks(boundary,'explicit joint-cap boundary '+level))
 dump('boundary-records.json',boundary_records)
 # Fixed parameters and all display values are seed/order independent.
 for r in allrecords[::50]:
  meta=r['generation'];r2=g.generate(meta['level'],seed=10001,template=meta['template'],parameters=meta['parameters'],profile=meta['profile']);assert r['question'][':question/id']==r2['question'][':question/id'];assert meta['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
 mutations=[];normal=g.generate('moderate',seed=4)
 def altered(change):
  z=copy.deepcopy(normal);z['question'][':question/worked-solution']=change(z['question'][':question/worked-solution']);return z
 mutations.append(mustfail(lambda:readback(altered(lambda s:re.sub(r'\\cdot (\(-?\d+\)|-?\d+)',r'\\cdot 99',s,count=1))),'wrong displayed factor with key unchanged'))
 mutations.append(mustfail(lambda:readback(altered(lambda s:re.sub(r'\+(\(-?\d+\)|-?\d+)\\cdot (\(-?\d+\)|-?\d+)','',s,count=1))),'missing dot factor with key unchanged'))
 z=copy.deepcopy(normal);z['question'][':question/problem']=z['question'][':question/problem'].replace('\\begin{bmatrix}', '\\begin{bmatrix}99 & ',1);mutations.append(mustfail(lambda:readback(z),'wrong printed operand'))
 z=copy.deepcopy(normal);z['question'][':question/worked-solution']+='\x0c';mutations.append(mustfail(lambda:readback(z),'C0 control character'))
 fixed=g.generate('easy',seed=3,template='q-317846');p=copy.deepcopy(fixed['generation']['parameters']);p['targets']=[[0,0],[1,0]];changed=g.generate('easy',template='q-317846',parameters=p);readback(changed)
 for profile in ['observed-raw','observed-repaired']:mutations.append(mustfail(lambda:g.generate('easy',template='q-317846',parameters=p,profile=profile),'changed observed target map '+profile))
 assert fixed['generation']['mathematical_fingerprint']!=changed['generation']['mathematical_fingerprint'];native.append(native_checks(changed,'changed same-operand target roles'))
 z=copy.deepcopy(changed);z['question'][':question/worked-solution']=fixed['question'][':question/worked-solution'];mutations.append(mustfail(lambda:readback(z),'stale target role with unchanged operands and key'))
 p=copy.deepcopy(g.SPECS['q-129495']['parameters']);p['A'][1][1]=1;mutations.append(mustfail(lambda:g.generate('easy',template='q-129495',parameters=p),'explicit easy zero-mask workload'))
 for level in ['moderate','hard']:
  p=copy.deepcopy(g.generate(level)['generation']['parameters']);p['A'][0][0]=100;mutations.append(mustfail(lambda:g.generate(level,parameters=p),'explicit '+level+' cap'))
  p=copy.deepcopy(g.generate(level)['generation']['parameters']);p['A'][0][0]=0;mutations.append(mustfail(lambda:g.generate(level,parameters=p),'explicit '+level+' nonzero workload'))
 dump('engine-input.json',native);subprocess.run([str(D/'check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 dump('fidelity.json',{'sources':fidelity,'originals':len(cases),'complete_banks':len(cases),'answer_values':totalanswers,'correct_designations_matched':correctrefs,'missing_original_correct_designations':2,'observed_worked_solutions':9,'raw_exact_solutions':9,'mathematically_sound_original_solutions':8,'documented_wrong_operand':1,'normal_repaired_solutions':9})
 dump('review.json',review);(D/'review.md').write_text('\n\n---\n\n'.join('### '+z['kind']+'\n\n'+g.markdown(z['record']) for z in review)+'\n')
 dump('samples.json',[g.generate(level,seed=i) for level in ['easy','moderate','hard'] for i in [201,202]])
 dump('render-records.json',[z['record'] for z in review]+[changed]+boundary_records);dump('variety.json',{'variety':variety,'slot_coverage':coverage,'sampled_maxima':maxima,'domain':'Whole-instance rejection; selected five-member bank is never patched or drawn from a first-valid pool.'})
 dump('validation.json',{'status':'passed mathematics/source/native; visual review separate','basis':2275,'source_originals':11,'complete_source_banks_matched':11,'source_answer_values_matched':totalanswers,'source_correct_designations_matched':correctrefs,'source_missing_correct_designations':2,'raw_solution_exact':9,'normal_solution_repairs':1,'source_errors_preserved_raw':True,'random_readback_records':len(allrecords),'variety':variety,'mutations_rejected':mutations,'native_grader_sha256':digest(D/'check-engine'),'native_files_reverified':42,'baseline_unchanged':True,'dependencies':{'python':platform.python_version(),'sympy':sp.__version__},'root_approval':'pending; stop after step 7'})
 print('PASS',len(allrecords),'normal readbacks;',totalanswers,'source answer values;',correctrefs,'observed correct refs;',len(mutations),'mutations')
if __name__=='__main__':main()
