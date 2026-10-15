"""Root verifies supplied 3x3/4x4 product roles, scaled operands and witness cells."""
import sys,importlib.util,re,json,hashlib,copy
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ROOT=R.parents[2];D=ROOT/'generate/scratch/17592186087700-draft'
def load(name,path):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
p=load('root_matrix_product_parser',R/'matrix-product-readback.py');s=p.s;g=load('root_larger_inverse_generator',D.with_suffix('.py'))
from scripts.question_capture.math_format import normalize_prose
n=dict(records=0,supplied_cells=0,individual_operand_cells=0,concrete_product_cells=0,nonidentity_witnesses=0,statement_values=0,choices=0,source_values=0,source_keys=0,source_solutions=0)
def truth(text,ms):
 raw=re.findall(r'^(?:- \*\*)?(?:I|II|III)\.(?:\*\*)? \$(.*?)\$',text,re.M);values=[]
 for t in raw:
  t=t.replace(' ','').replace('{','').replace('}','');m=re.fullmatch(r'([A-Z])([A-Z])=([A-Z])([A-Z])=I_(\d)',t)
  if m:
   a,b,c,d,size=m.groups();assert (a,b)==(d,c) and all(ms[v].rows==int(size) for v in (a,b,c,d));values.append(ms[a]*ms[b]==s.eye(int(size)) and ms[c]*ms[d]==s.eye(int(size)))
  else:
   m=re.fullmatch(r'([A-Z])(=|\\ne)([A-Z])\^-1',t);assert m,t;a,op,b=m.groups();v=ms[a]*ms[b]==s.eye(ms[a].rows) and ms[b]*ms[a]==s.eye(ms[a].rows);values.append(v if op=='=' else not v)
 assert len(values) in (1,3),(text,raw);return values

def check(r):
 q=r['question'];ms,bases=p.named(q[':question/problem']);assert len(ms) in (2,3);size=next(iter(ms.values())).rows;assert size in (3,4);values=truth(q[':question/problem'],ms);n['statement_values']+=len(values)
 sol=q[':question/worked-solution'];assert all(int(i)==size for i in re.findall(r'\{?I\}?_\{?(\d)\}?',sol))
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
 for block in blocks:
  rows=p.rows(block);pair=re.match(r'\s*([A-Z])([A-Z])',rows[0]);assert pair,rows[0];a,b=pair.groups();wanted=ms[a]*ms[b]
  initial=p.expression(rows[0].split('=',1)[1]);assert initial[0]==wanted and len(initial[1])==2
  assert s.Matrix(initial[1][0])==bases[a] and s.Matrix(initial[1][1])==bases[b]
  result,shown=p.expression(rows[1].split('=',1)[1]);assert len(shown)==1;concrete=[]
  for i in range(size):
   for j in range(size):
    if shown[0][i][j] is not None:assert result[i,j]==wanted[i,j];concrete.append((i,j));n['concrete_product_cells']+=1
  if len(concrete)==1:
   i,j=concrete[0];assert wanted[i,j]!=s.eye(size)[i,j] and r'\ne' in rows[-1];n['nonidentity_witnesses']+=1
  else:assert len(concrete)==size*size and result==wanted==s.eye(size)
  n['individual_operand_cells']+=2*size*size
 for roman,word in re.findall(r'[Ss]tatement (I|II|III) is (true|false)',sol):assert values[('I','II','III').index(roman)]==(word=='true')
 for f in q[':question/answer-fields']:
  assert f[':answer-field/type']==':answer-field.type/checkbox' and sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true'];correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==str(values[('I','II','III').index(f[':answer-field/key'])]).lower();n['choices']+=2
 if len(values)==3:
  ending=sol.rsplit('Therefore,',1)[-1];assert set(re.findall(r'(?<!I)(?:III|II|I)(?!I)',ending))=={v for v,t in zip(('I','II','III'),values) if t}
 n['supplied_cells']+=sum(m.rows*m.cols for m in ms.values());n['records']+=1
for c in json.loads((D/'source-cases.json').read_text()):
 o=c['record'];sid=o[':question/math-academy-id'];level=o[':question/difficulty'][':db/ident'].rsplit('/',1)[1];r=g.generate(level,template=sid,profile='raw-source',parameters=g.original_parameters(sid));q=r['question'];assert q[':question/problem']==normalize_prose(o[':question/problem']) and q[':question/worked-solution']==normalize_prose(o[':question/worked-solution']);n['source_solutions']+=1
 for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
  assert f[':answer-field/key']==of[':answer-field/key'] and sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_values']+=2;n['source_keys']+=1
 # Raw erroneous references remain evidence; supported normal render checked separately.
for item in json.loads((D/'review.json').read_text()):
 r=item['record']
 if r['generation'].get('profile')!='raw-source':check(r)
for level in g.LEVELS:
 for seed in range(12):check(g.generate(level,seed=seed+300))
saved=dict(n);bad=copy.deepcopy(g.generate('hard',seed=31));text=bad['question'][':question/worked-solution'];bad['question'][':question/worked-solution']=text.replace('{I}_{4}','{I}_{3}',1)
try:check(bad)
except AssertionError:pass
else:raise AssertionError('unchanged-final-key wrong identity size escaped')
n=saved;out=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),independent_readback=n,unchanged_finalkey_controls=1,finite_math_capacities={'easy':120,'moderate':204,'hard':288},scope='supplied matrix direct verification only; signed simultaneous permutations and actual failing cells, no inversion algorithm',limits='Three mathematical source references plus one typo explicitly repaired in normal output; raw evidence remains separate. Easy authored single-pair verification.')
(R/'qa/17592186087700-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
