"""Independent checks parse the learner's actual rendered mathematical strings."""
import sys
sys.dont_write_bytecode=True
import copy,functools,hashlib,importlib.util,itertools,json,pathlib,re,subprocess
import sympy as sp
H=pathlib.Path(__file__).resolve().parent;ROOT=H.parents[2];spec=importlib.util.spec_from_file_location('larger_inverse_draft',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
M=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
@functools.lru_cache(maxsize=1024)
def exact(s):
 s=s.strip().replace('−','-');s=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(-?\d+)\}',r'(\1)/(\2)',s)
 if not re.fullmatch(r'[-+\d()/ ]+',s):raise AssertionError('Unsupported printed scalar '+s)
 return sp.Rational(sp.sympify(s))
def rows(m):return [[x.strip() for x in row.split('&')] for row in m.split('\\\\')]
def matrix(m):return sp.Matrix([[exact(x) for x in row] for row in rows(m)])
def coefficient(s):
 s=s.strip();return sp.Integer(1) if not s else exact(s)
def parse_prompt(p):
 result={};prev=0
 for match in M.finditer(p):
  label=re.search(r'([A-Z])=(.*)$',p[prev:match.start()],re.S);assert label
  result[label[1]]=coefficient(label[2])*matrix(match[1]);prev=match.end()
 return result

def field_truth(r):
 q=r['question'];p=q[':question/problem'];obj=parse_prompt(p);truth=[]
 for line in p.splitlines():
  mm=re.search(r'(?:\*\*|\b)(I{1,3})\.(?:\*\*)?\s*\$([^$]+)\$',line)
  if not mm:continue
  eq=mm[2].replace(' ','');prod=re.fullmatch(r'([A-Z])([A-Z])=([A-Z])([A-Z])=\{?I\}?_\{?(\d)\}?',eq)
  if prod:
   a,b,c,d,n=prod.groups();n=int(n);assert obj[a].rows==n;truth.append(obj[a]*obj[b]==sp.eye(n) and obj[c]*obj[d]==sp.eye(n))
  else:
   inv=re.fullmatch(r'([A-Z])(=|\\ne)\{?([A-Z])\}?\^\{?-1\}?',eq);assert inv,eq;a,op,b=inv.groups();n=obj[a].rows;yes=obj[a]*obj[b]==sp.eye(n) and obj[b]*obj[a]==sp.eye(n);truth.append(not yes if op==r'\ne' else yes)
 assert len(truth)==len(q[':question/answer-fields'])
 for f,v in zip(q[':question/answer-fields'],truth):
  assert f[':answer-field/type']==':answer-field.type/checkbox';assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
  key=f[':answer-field/correct'][1];assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key)==str(v).lower()
 return obj,truth

def check(r,allow_source_errors=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'};q=r['question'];obj,truth=field_truth(r);s=q[':question/worked-solution'];diagnostics=[]
 assert not any(ord(c)<32 and c not in '\n\t\r' for c in q[':question/problem']+s)
 fields=q[':question/answer-fields'];allids=[f[':answer-field/id'] for f in fields]+[a[':answer/id'] for f in fields for a in f[':answer-field/choices']];assert len(allids)==len(set(allids))
 for block in re.finditer(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S):
  v=block[1];mm=list(M.finditer(v));assert len(mm)==3
  name=re.match(r'([A-Z]{2})\s*&\s*=',v)[1];a,b=name
  prefix=v[:mm[0].start()].split('=')[-1];c=coefficient(prefix)
  left,right=matrix(mm[0][1]),matrix(mm[1][1]);actual=c*left*right
  # Check operands individually, permitting the captured factor to move outside.
  if c*left!=obj[a] and left!=obj[a]:diagnostics.append('left operand differs from printed '+a)
  if c*right!=obj[b] and right!=obj[b]:diagnostics.append('right operand differs from printed '+b)
  if actual!=obj[a]*obj[b]:diagnostics.append('complete product differs from '+name)
  result_factor=coefficient(v[mm[1].end():mm[2].start()].split('=')[-1]);rr=rows(mm[2][1]);assert len(rr)==actual.rows and all(len(row)==actual.cols for row in rr)
  shown=0
  for i,row in enumerate(rr):
   for j,x in enumerate(row):
    if x=='∗':continue
    shown+=1
    if result_factor*exact(x)!=actual[i,j]:diagnostics.append('printed product cell incorrect')
  if r'\ne' in v:
   assert shown==1
   witness=[(i,j) for i,row in enumerate(rr) for j,x in enumerate(row) if x!='∗'][0];assert result_factor*exact(rr[witness[0]][witness[1]])!=sp.eye(actual.rows)[witness]
  else:assert shown==actual.rows**2 and actual==sp.eye(actual.rows)
  for n in re.findall(r'\{?I\}?_\{?(\d)\}?',v):assert int(n)==actual.rows
 # Introductory prose must name the identity of the printed matrices' dimension.
 n=next(iter(obj.values())).rows
 if any(int(k)!=n for k in re.findall(r'\{?I\}?_\{?(\d)\}?',s)):diagnostics.append('wrong identity dimension in solution prose')
 if not allow_source_errors:assert not diagnostics,diagnostics
 return diagnostics


def native_checks(r):
 return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every Boolean bank member'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def task(q):
 objects=parse_prompt(q[':question/problem'])
 # Same actual matrices and same statement relations, regardless of formatting,
 # seed, witness, solution text, choice order or question identity.
 relations=[]
 for line in q[':question/problem'].splitlines():
  m=re.search(r'(?:\*\*|\b)(I{1,3})\.(?:\*\*)?\s*\$([^$]+)\$',line)
  if m:relations.append(re.sub(r'[\s{}]','',m[2]))
 return g.digest({'matrices':[g.serial(m) for m in objects.values()],'relations':relations})

def main():
 from scripts.generator_publish import validate_question
 fidelity=[];records=[]
 for case in json.loads((H/'source-cases.json').read_text()):
  t=case['template'];level=g.TEMPLATES[t]['level'];p=case['parameters'];src=case['record'];raw=g.generate(level,template=t,profile='raw-source',parameters=p);q=raw['question']
  assert q[':question/problem']==g.normalize_prose(src[':question/problem'])
  assert q[':question/worked-solution']==g.normalize_prose(src[':question/worked-solution'])
  assert len(q[':question/answer-fields'])==len(src[':question/answer-fields'])==3
  for a,b in zip(q[':question/answer-fields'],src[':question/answer-fields']):
   assert a[':answer-field/key']==b[':answer-field/key']
   assert a[':answer-field/type']==b[':answer-field/type'][':db/ident']
   assert sorted((c[':answer/type'],c[':answer/value']) for c in a[':answer-field/choices'])==sorted((c[':answer/type'][':db/ident'],c[':answer/value']) for c in b[':answer-field/choices'])
   assert next(c[':answer/value'] for c in a[':answer-field/choices'] if c[':answer/id']==a[':answer-field/correct'][1])==b[':answer-field/correct'][':answer/value']
  fidelity.append({'template':t,'source_id':case['source_id'],'matched_choices':6,'complete_banks':3,'raw_diagnostics':check(raw,True)})
  r=g.generate(level,template=t,parameters=p);check(r);validate_question(r['question']);records.append(r)
 coverage={};slots={}
 for l in g.LEVELS:
  coverage[l]=set();slots[l]={'permutations':set(),'signs':set(),'witnesses':set()}
  for seed in range(180):
   r=g.generate(l,seed=seed);check(r);validate_question(r['question']);assert r==g.generate(l,seed=seed)
   coverage[l].add(r['generation']['template']);p=r['generation']['parameters']
   slots[l]['permutations'].add(tuple(p['permutation']));slots[l]['signs'].add(tuple(p['signs']));slots[l]['witnesses'].update(x for x in p['witnesses'] if x is not None)
   if seed<12:records.append(r)
  assert coverage[l]=={k for k,t in g.TEMPLATES.items() if t['level']==l}
 # Exhaust the finite domains and independently validate every distinct task.
 finite={}
 for l in g.LEVELS:
  seen=set()
  for t,v in g.TEMPLATES.items():
   if v['level']!=l:continue
   n=len(v['bases'][0])
   for perm in itertools.permutations(range(n)):
    for signs in itertools.product((-1,1),repeat=n):
     p={'permutation':list(perm),'signs':list(signs),'witnesses':[]};actual=[g.transform(g.mat(b),p)*g.sf(s) for b,s in zip(v['bases'],v['scales'])]
     for b in v['blocks']:
      a,c=b['pair'];prod=actual[a]*actual[c];p['witnesses'].append(None if b['identity'] else next(z for z in range(n*n) if prod[z//n,z%n]!=sp.eye(n)[z//n,z%n]))
     r=g.generate(l,template=t,parameters=p);fp=r['generation']['mathematical_fingerprint']
     if fp not in seen:check(r);seen.add(fp)
  finite[l]=len(seen)
 assert finite==g.CAPACITIES
 pp=g.original_parameters('q-11634');other=copy.deepcopy(pp);other['witnesses'][0]=4
 a=g.generate('moderate',template='q-11634',parameters=pp);b=g.generate('moderate',template='q-11634',parameters=other)
 check(a);check(b);assert task(a['question'])==task(b['question']);assert a['question'][':question/worked-solution']!=b['question'][':question/worked-solution']
 controls=[];base=g.generate('moderate',template='q-11642',parameters=g.original_parameters('q-11642'))
 for label,old,new in [('operand-only',r'2 & -2 & -1',r'9 & -2 & -1'),('witness-only',r'{bmatrix}5 & ∗',r'{bmatrix}6 & ∗'),('dimension',r'{I}_{3}',r'{I}_{4}')]:
  bad=copy.deepcopy(base);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(old,new)
  try:check(bad)
  except AssertionError:controls.append(label)
  else:raise AssertionError('Negative control passed '+label)
 try:g.generate('easy')
 except ValueError:pass
 else:raise AssertionError('Unclassified easy became supported')
 native=[{'label':str(i),'record':r,'checks':native_checks(r)} for i,r in enumerate(records)]
 (H/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'native-input.json'),str(H/'native-report.json')],check=True)
 report={'status':'passed','source_complete_questions':13,'source_choices_matched':78,'source_choices_total':78,'source_fields_matched':39,'source_fidelity':fidelity,'sample_checks':360,'finite_unique_tasks':finite,'coverage':{l:sorted(x) for l,x in coverage.items()},'slots':{l:{k:sorted(v) for k,v in d.items()} for l,d in slots.items()},'negative_controls':controls,'changed_witness_same_task':True,'plots':'none','unsupported_levels':{'easy':'No observed easy practice; the draft single-pair experiment changes the three-statement backbone and is excluded.'},'grader':str((ROOT/'generate/runs/current/check-engine').relative_to(ROOT)),'grader_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()}
 (H/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'validation':'passed','finite_unique_tasks':finite,'source_banks':13,'native_records':len(native)}))
if __name__=='__main__':main()
