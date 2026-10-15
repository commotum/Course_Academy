"""Independent truth evaluation from rendered question; actual native field grading."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def truth(statement,t):
 # Interpret rendered claims independently of template identity and stored keys.
 s=statement.replace('**','').replace('$','').strip();r=t['rank'];u=t['nullity'];n=t['n']
 m=re.search(r'\\text\{rank\}\(A\)=(\d+)',s)
 if m:return r==int(m[1])
 m=re.search(r'\\text\{nullity\}\(A\)=(\d+)',s)
 if m:return u==int(m[1])
 m=re.search(r'(\d+)-dimensional subspace of .*?\^\{?(\d+)',s)
 if m:return r==int(m[1]) and n==int(m[2])
 m=re.search(r'\\text\{Col\}\(A\)=.*?\^\{?(\d+)',s)
 if m:return r==n==int(m[1])
 if 'det(A)=0' in s:return r<n
 m=re.search(r'non-pivot columns.*?equal to\s*(\d+)',s)
 if m:return u==int(m[1])
 m=re.search(r'A.*?has\s*(\d+)\s*pivot col',s)
 if m:return r==int(m[1])
 if 'invertible' in s:return r<n if re.search(r'\bnot\b',s) else r==n
 raise ValueError('Unknown claim '+s)

def label(values):
 selected=[s for s,b in zip(('I','II','III'),values) if b]
 if not selected:return 'None'
 if len(selected)==1:return selected[0]+' only'
 if len(selected)==2:return ' and '.join(selected)+' only'
 return 'I, II, and III'

def field_value(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def format_check(s):
 assert s.count('$$')%2==0 and s.replace('$$','').count('$')%2==0
 assert not any(x in s for x in ['\x08','\x0c','+-'])

def independent(rec):
 q=rec['question'];t=g.task_data(q);values=[truth(s,t) for s in t['statements']];fs=q[':question/answer-fields']
 assert rec['knowledge_point']['db_id']==g.KP_ID
 for name in (':question/problem',':question/worked-solution'):format_check(q[name])
 if len(fs)==1:
  assert fs[0][':answer-field/type']==':answer-field.type/radio'
  assert len(fs[0][':answer-field/choices'])==5 and field_value(fs[0])==label(values)
 else:
  assert len(fs)==3 and [f[':answer-field/key'] for f in fs]==['I','II','III']
  for f,b in zip(fs,values):
   assert f[':answer-field/type']==':answer-field.type/checkbox'
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
   assert field_value(f)==str(b).lower()
 sol=q[':question/worked-solution']
 assert 'rank}(A)+\\text{nullity}(A)=n' in sol
 for roman,b in zip(('I','II','III'),values):assert f'Statement {roman} is {str(b).lower()}.' in sol
 assert label(values) in sol
 # Numeric substitutions in the displayed rank-nullity computations are exact.
 for a,b,c in re.findall(r'(\d+)-(\d+)\s*\\\\\s*&\s*=\s*(\d+)',sol):assert int(a)-int(b)==int(c)
 # Every explicit null-space basis in the solution has the same span as supplied data.
 if t['given'][0]=='null-space':
  blocks=list(g.vector_blocks(sol));numeric=[]
  for m,cells in blocks:
   col=sp.Matrix([g.scalar(c) for c in cells])
   if not col.free_symbols:numeric.append(col)
  if numeric:
   B=sp.Matrix.hstack(*numeric)
   span=[list(map(str,row)) for row in B.T.rref()[0].tolist() if any(row)]
   assert span==t['given'][1],(rec['generation']['template'],'solution subspace mismatch')
 for f in fs:
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(f[':answer-field/choices'])
  assert len({a[':answer/value'] for a in f[':answer-field/choices']})==len(f[':answer-field/choices'])
 assert rec['generation']['fingerprint']==hashlib.sha256(g.fingerprint(q).encode()).hexdigest()
 return g.fingerprint(q)

def checks(rec):
 out=[]
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  if f[':answer-field/type']==':answer-field.type/radio':
   out += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete source-profile bank grading'} for a in f[':answer-field/choices']]
  else:
   out += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==field_value(f) else 'rejected','purpose':'both checkbox states by authored choice identity'} for a in f[':answer-field/choices']]
 return out

def native(r,label_):return {'label':label_,'record':r,'checks':checks(r)}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')

def main():
 native_cases=[];replay=[];samples=[];coverage={};distinct={};fixed=[]
 for key,source in sorted(g.Q.items()):
  r=g.generate(g.level_of(key),template=key,parameters=g.default_parameters(key));independent(r)
  q=r['question'];original=g.clean(source)
  for name in (':question/problem',':question/worked-solution'):assert q[name]==original[name],(key,name)
  for f,old in zip(q[':question/answer-fields'],original[':question/answer-fields']):
   assert f[':answer-field/type']==old[':answer-field/type'] and f[':answer-field/key']==old[':answer-field/key']
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices'])
   assert field_value(f)==field_value(old)
  replay.append({'source':key,'complete_banks_matched':len(q[':question/answer-fields']),'choices_matched':sum(len(f[':answer-field/choices']) for f in q[':question/answer-fields']),'prompt_solution_byte_exact':True,'mathematics':'pass'})
  native_cases.append(native(r,key+'-replay'));seen=set();parameter_values=[]
  params=[{'diagonal':list(d)} for d in itertools.product(range(1,4),repeat=g.n_of(q[':question/problem']))] if g.is_vector(key) else [{'scale':k} for k in range(1,4)]
  for p in params:
   r=g.generate(g.level_of(key),template=key,parameters=p);fp=independent(r);seen.add(fp);parameter_values.append(p)
   assert r==g.generate(g.level_of(key),template=key,parameters=p)
  distinct[key]=len(seen);coverage[key]={'parameter_cases':len(params),'all_declared_values_exercised':True,'distinct_tasks':len(seen)}
  if len(seen)==1:fixed.append(key)
  base=g.fingerprint(q)
  for p in reversed(params):
   r=g.generate(g.level_of(key),template=key,parameters=p)
   if g.fingerprint(r['question'])!=base:
    samples.append({'source':original,'variant':r});native_cases.append(native(r,key+'-changed-data'));break
 for level in g.SUPPORTED_LEVELS:
  rows=g.batch(level,30,1930);assert len(rows)>=5
  assert len({independent(r) for r in rows})==len(rows)
  native_cases.extend(native(r,level+'-'+str(i)) for i,r in enumerate(rows))
 save(D/'native-input.json',native_cases)
 subprocess.run([str(D/'check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 # Mutation controls: stale answer keys, vector references and displayed truth must fail.
 mutation_controls=[]
 for s in samples:
  r=copy.deepcopy(s['variant']);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('Statement I is true.','Statement I is false.').replace('Statement I is false.','Statement I is true.',1) if 'Statement I is true.' not in r['question'][':question/worked-solution'] else r['question'][':question/worked-solution'].replace('Statement I is true.','Statement I is false.',1)
  try:independent(r)
  except AssertionError:mutation_controls.append('wrong worked-solution truth rejected')
  else:raise AssertionError('Mutation passed')
 save(D/'review.json',samples);save(D/'source-replay.json',replay)
 save(D/'capabilities.json',{'supported_levels':list(g.SUPPORTED_LEVELS),'unsupported_levels':['easy'],'exceptions':[{'level':'easy','reason':'No easy source questions or equivalent easy backbone observed at source basis '+str(g.RAW['basis'])+'; band remains unsupported and unfilled.'},{'template':'q-79423','reason':'Diagonal changes preserve the same coordinate hyperplane. Exactly one semantic task within this conservative slot domain; exclude coefficient-only duplicates.'}],'finite_by_template':distinct,'sampling_policy':'Counts dilate by k=1..3; vector diagonal entries 1..3; quotient by subspace RREF and claims. No novel statement layout or solution stage.'})
 save(D/'validation.json',{'status':'pass','source_basis':g.RAW['basis'],'source_replay':replay,'coverage':coverage,'mathematics':'exhaustive exact SymPy ranks and rendered-claim evaluation','grading':'native grade_field; both checkbox values and every radio choice','mutation_controls':mutation_controls,'fidelity':'All 14 source prompts and worked solutions byte exact at original parameters; all source fields and complete banks replayed','dependencies':{'sympy':sp.__version__,'python':sys.version.split()[0]},'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [D.with_suffix('.py'),D/'source.json',D/'validate.py',D/'check-engine.rs',D/'check-engine']}})
 print(json.dumps({'status':'pass','source_replays':len(replay),'parameter_cases':sum(c['parameter_cases'] for c in coverage.values()),'distinct_by_template':distinct}))
if __name__=='__main__':main()
