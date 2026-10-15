"""Root reads actual corresponding matrix entries, symbolic expansion and scalar recovery."""
import re,json,sys,importlib.util,hashlib,copy
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ROOT=R.parents[2];D=ROOT/'generate/scratch/17592186059741-draft'
z=importlib.util.spec_from_file_location('root_scalar_gen',D.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
z=importlib.util.spec_from_file_location('root_scalar_parser',R/'ode-scalar-parser.py');p=importlib.util.module_from_spec(z);z.loader.exec_module(p);k=p.k
from scripts.question_capture.math_format import normalize_prose
n=dict(records=0,prompt_cells=0,expanded_cells=0,selected_prose_operands=0,formal_scalar_equations=0,choices=0,source_values=0,source_refs=0,source_solutions=0)
def scalar(t):return p.scalar(t.replace('&','').strip().rstrip('.,:'))
def matrices(t):
 return [s.Matrix([[scalar(c) for c in row.split('&')] for row in b.split(r'\\')]) for b in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',t,re.S)]
def check(r):
 q=r['question'];pr=q[':question/problem'];sol=q[':question/worked-solution'];pm=matrices(pr);assert len(pm)==2;B,A=pm;assert A.shape==B.shape and all(x.is_Integer for x in A) and all(x.is_Integer for x in B)
 ratios={b/a for a,b in zip(A,B) if a};assert len(ratios)==1;value=ratios.pop();assert value!=0 and value*A==B
 sm=matrices(sol);assert len(sm)==4 and sm[0]==A and sm[1]==k*A and sm[2]==k*A and sm[3]==B
 segment=sol.split("Let's choose ")[1].split('Equating these elements')[0];spans=re.findall(r'\$([^$]+)\$',segment);a,b=map(scalar,spans[-2:]);assert a.has(k) and a==a.coeff(k)*k and b==a.coeff(k)*value
 location=segment.split(', $')[0];rc=re.search(r'row \$(\d+)\$ and column \$(\d+)\$',location)
 if rc:i,j=int(rc[1])-1,int(rc[2])-1
 elif 'third row' in location:i,j=2,0
 elif 'top-right' in location:i,j=0,A.cols-1
 elif 'bottom-left' in location:i,j=A.rows-1,0
 elif 'top-left' in location or 'leftmost' in location:i,j=0,0
 elif 'rightmost' in location:i,j=0,A.cols-1
 else:raise AssertionError(location)
 assert A[i,j]*k==a and B[i,j]==b
 aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(aligned)==2
 # Protect all matrix row separators before counting outer equality stages.
 first=re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}','MATRIX',aligned[0],flags=re.S);firstrows=first.split(r'\\');assert len(firstrows)==2 and firstrows[0].split('=')[1].strip().startswith('k')
 rows=aligned[1].split(r'\\');assert len(rows)==2
 l,r0=rows[0].replace('&','').split('=');assert scalar(l)==a and scalar(r0)==b
 l,r0=rows[1].replace('&','').split('=');assert scalar(l)==k and scalar(r0)==value
 f=q[':question/answer-fields'][0];values=[scalar(a[':answer/value'].split('=')[-1]) for a in f[':answer-field/choices']];assert len(values)==len(set(values));assert next(a[':answer/id'] for a,v in zip(f[':answer-field/choices'],values) if v==value)==f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  assert len(values)==5 and all(a[':answer/value'].startswith('k=') for a in f[':answer-field/choices']);aa=A[i,j];bb=B[i,j];assert set(values)=={value,aa/bb,aa*bb,bb-aa,bb+aa}
 else:assert len(values)==1 and '{{'+f[':answer-field/key']+'}}' in pr
 level=q[':question/difficulty'].rsplit('/',1)[1]
 assert value.q==1 and 2<=abs(value)<=9 if level=='easy' else abs(value.p)==1 and 2<=value.q<=6 if level=='moderate' else 2<=abs(value.p)<=5 and 2<=value.q<=6
 n['prompt_cells']+=len(A)+len(B);n['expanded_cells']+=sum(len(m) for m in sm);n['selected_prose_operands']+=2;n['formal_scalar_equations']+=2;n['choices']+=len(values);n['records']+=1
source=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions']
for o in source:
 sid=o[':question/math-academy-id'];q=g.generate('easy',template=sid,parameters=g.DEFAULTS[sid],profile='raw-'+sid)['question'];assert q[':question/problem']==normalize_prose(o[':question/problem'])
 for attr in (':question/difficulty',':question/worked-solution'):assert (attr in q)==(attr in o)
 if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
 f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);n['source_values']+=len(of[':answer-field/choices'])
 assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
 if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
for r in json.loads((D/'review.json').read_text()):
 if not r['record']['generation']['evidence_only']:check(r['record'])
for level in g.SUPPORTED_LEVELS:
 for seed in range(12):check(g.generate(level,seed=seed+300))
saved=dict(n);bad=copy.deepcopy(g.generate('easy',seed=21,template='q-320536'));bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('kB & =k','kB & =2k',1)
try:check(bad)
except AssertionError:pass
else:raise AssertionError('wrong distributed scalar unchangedkey escaped')
n=saved;out=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),independent_readback=n,unchanged_finalkey_controls=1,scope='Recover one scalar by corresponding entry division only, ordered matrix expansion/equation/selected-cell solve retained; all eligible nonzero target cells vary',limits='Raw erroneous q320536 signs and incomplete payoff context remain ineligible; opaque source radio offsets separate from method banks. Moderate/hard number workloads authored.')
(R/'qa/17592186059741-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
