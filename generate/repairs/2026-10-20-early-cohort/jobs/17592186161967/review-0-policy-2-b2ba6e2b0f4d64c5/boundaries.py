import sys,importlib.util,pathlib,json,hashlib,ast
sys.dont_write_bytecode=True
root=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',root.parent/'workspace/17592186161967.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
mod=ast.parse((root/'audit.py').read_text());exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,(ast.Import,ast.ImportFrom)) or isinstance(n,ast.FunctionDef) and n.name in ['ops','mats','apply','check']],type_ignores=[]),'helpers','exec'))
rows=[]
A=[[1,1,3],[2,1,5],[4,3,7]]
for p,c in [(0,0),(0,1),(1,1)]:
 ks=[0 if r==p else -A[r][c]//A[p][c] for r in range(3)]
 rows.append(g.generate(seed=61417,bank_profile='q-42531',parameters={'A':A,'pivot':p,'column':c,'ks':ks}))
canonical=g.generate(seed=61967,bank_profile='q-130444',parameters={'A':[[1,4,-7],[2,2,-8],[-3,-2,1]],'pivot':0,'column':0,'ks':[0,-2,3]});rows.append(canonical)
assert mats(canonical['question'][':question/problem'])[1]==[[1,4,-7],[0,-6,6],[0,10,-20]]
for p in range(3):
 for c in range(3):
  A=[[2,4,7],[3,5,8],[1,6,9]];A[p][c]=-3;t=[r for r in range(3) if r!=p];ks=[0,0,0];ks[t[0]]=4;ks[t[1]]=-4
  for r in t:A[r][c]=-ks[r]*A[p][c]
  rows.append(g.generate(seed=81427,bank_profile='q-42531',parameters={'A':A,'pivot':p,'column':c,'ks':ks}))
for r in rows:check(r)
(root/'boundary-records.json').write_text(json.dumps(rows,indent=2))
cases=[]
for i,r in enumerate(rows):
 f=r['question'][':question/answer-fields'][0];ix=check(r);cases.append({'label':f'boundary-{i}','record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if j==ix else 'rejected','purpose':'Independent all-nine target coordinates and fixed-A target changes'} for j,c in enumerate(f[':answer-field/choices'])]})
(root/'boundary-grader-input.json').write_text(json.dumps(cases,indent=2))
assert json.load(open('relocated-output.json'))==g.batch('easy',2,38191)
old=json.load(open('packaging.json'))['hashes']; now={str(p.relative_to(root.parent/'workspace')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root.parent/'workspace').rglob('*') if p.is_file()};assert old==now
(root/'boundary-results.json').write_text(json.dumps({'canonical':'399b7598-c793-5032-9f33-ac02c7b85fe1 matrices and operations replayed; no observed bank to compare','fixed_A_targets':[(0,0),(0,1),(1,1)],'all_nine_pivot_column_pairs':True,'boundary_values':'pivot -3, targets +/-12, coefficients +/-4','relocation_equal':True,'package_unchanged':True},indent=2))
# Retain attempt counts for rejection/resampling on representative seeds.
counts=[]
orig=g.recipes
for p in g.PROFILES:
 for seed in [38191,38192,38193]:
  calls=[]
  def trace(profile,a,b):calls.append((a,b));return orig(profile,a,b)
  g.recipes=trace;r=g.generate(seed=seed,bank_profile=p);g.recipes=orig
  counts.append({'profile':p,'seed':seed,'attempts':len(calls)-1,'final_parameters':r['generation']['parameters']})
(root/'resampling.json').write_text(json.dumps(counts,indent=2))
print('13 additional records pass; relocated package matches; package unchanged')
