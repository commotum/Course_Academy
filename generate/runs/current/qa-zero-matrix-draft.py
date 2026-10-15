"""Independent root reading of displayed entries, nonzero witnesses and full selection banks."""
import importlib.util,json,re,hashlib,sys,copy
from pathlib import Path
from fractions import Fraction
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ROOT=R.parents[2];D=ROOT/'generate/scratch/17592186087695-draft'
z=importlib.util.spec_from_file_location('zero_root_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
from scripts.question_capture.math_format import normalize_prose
n=dict(records=0,actual_cells=0,classification_bullets=0,nonzero_witnesses=0,choices=0,source_values=0,source_keys=0,exact_source_solutions=0,repaired_source_solutions=0)
def matrices(text):
 out={}
 for m in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S):
  rows=[[Fraction(c.strip()) for c in row.split('&')] for row in m[2].split(r'\\')];assert len({len(v) for v in rows})==1;out[m[1]]=rows
 assert len(out)==3;return out
def check(r):
 q=r['question'];ms=matrices(q[':question/problem']);truth={k for k,vs in ms.items() if not any(v for row in vs for v in row)}
 n['actual_cells']+=sum(sum(map(len,vs)) for vs in ms.values())
 sol=q[':question/worked-solution'];bullets=re.findall(r'^- \$([A-Z])\$ is (.*?)matrix(.*)$',sol,re.M);assert len(bullets)==3 and {b[0] for b in bullets}==set(ms)
 for name,status,detail in bullets:
  assert ('not' not in status)==(name in truth)
  if name not in truth:
   m=re.search(r'\$\{?([a-z])\}?_\{([1-4])([1-6])\}=([0-9.]+)\\n(?:eq|e)\s*0\$',detail);assert m,(name,detail)
   label,row,col,value=m.groups();row,col=int(row)-1,int(col)-1;assert label==name.lower() and Fraction(value)!=0 and ms[name][row][col]==Fraction(value)
   n['nonzero_witnesses']+=1
  else:assert 'all' in detail or 'all' in status
  n['classification_bullets']+=1
 ending=sol.split('Therefore,')[1];assert set(re.findall(r'\$([A-Z])\$',ending))==truth
 fs=q[':question/answer-fields'];assert len(fs) in (1,3)
 for f in fs:
  vals=f[':answer-field/choices'];correct=next(a[':answer/value'] for a in vals if a[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type'].endswith('/checkbox'):
   assert sorted(a[':answer/value'] for a in vals)==['false','true'] and f[':answer-field/key'] in ms
   assert correct==str(f[':answer-field/key'] in truth).lower()
  else:
   banks=[frozenset(re.findall(r'\$([A-Z])\$',a[':answer/value'])) for a in vals];assert len(banks)==len(set(banks))==5 and banks.count(frozenset(truth))==1
   assert set(re.findall(r'\$([A-Z])\$',correct))==truth
  n['choices']+=len(vals)
 n['records']+=1
cases=json.loads((D/'source-cases.json').read_text())
for row in cases:
 r=g.generate('easy',template=row['template'],parameters=row['parameters']);check(r);o=row['record'];q=r['question'];assert q[':question/problem']==normalize_prose(o[':question/problem'])
 ofs={f[':answer-field/key']:f for f in o[':question/answer-fields']}
 for f in q[':question/answer-fields']:
  of=ofs[f[':answer-field/key']];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(normalize_prose(a[':answer/value']) for a in of[':answer-field/choices']);n['source_values']+=len(of[':answer-field/choices'])
  if ':answer-field/correct' in of:
   assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_keys']+=1
 if ':question/worked-solution' in o:
  original=normalize_prose(o[':question/worked-solution'])
  if row['source_id']=='q-126201':assert original.replace('{i}_{12}','{i}_{21}')==q[':question/worked-solution'];n['repaired_source_solutions']+=1
  else:assert original==q[':question/worked-solution'];n['exact_source_solutions']+=1
for level in ('easy','moderate','hard'):
 for template in g.DEFAULT_TEMPLATES:
  for seed in range(6):check(g.generate(level,seed=seed+700,template=template))
# Every feasible witness in a 4x6 matrix role is checked with remaining data held.
slot_cases=0
for row in cases:
 for j,matrix in enumerate(row['parameters']['matrices']):
  count=sum(Fraction(v)!=0 for rr in matrix for v in rr)
  if not count:continue
  for cell in range(24):
   par=copy.deepcopy(row['parameters']);small=[['0']*6 for _ in range(4)];locations=[cell]+[i for i in range(24) if i!=cell][:count-1]
   for loc in locations:small[loc//6][loc%6]='0.1'
   par['matrices'][j]=small;par['witnesses'][j]=[cell//6+1,cell%6+1]
   if sum(len(z)*len(z[0]) for z in par['matrices'])>46:continue
   check(g.generate('hard',template=row['template'],parameters=par));slot_cases+=1
before=copy.deepcopy(n);bad=copy.deepcopy(g.generate('easy',template='q-126201',parameters=next(c['parameters'] for c in cases if c['source_id']=='q-126201')));sol=bad['question'][':question/worked-solution'];assert '{i}_{21}' in sol;bad['question'][':question/worked-solution']=sol.replace('{i}_{21}','{i}_{12}')
try:check(bad)
except AssertionError:pass
else:raise AssertionError('wrong source witness coordinate with unchanged key escaped')
n=before
out=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),independent_readback=n,held_data_witness_slot_records=slot_cases,unchanged_final_key_negative_controls=1,scope='All three levels use the same supplied-numerical-matrix zero predicate; moderate/hard are authored uncalibrated, no added matrix computation',limits='Shape/support and actual witness positions vary; aliases, nonzero magnitudes and matrix order do not establish new tasks.')
(R/'qa/17592186087695-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
