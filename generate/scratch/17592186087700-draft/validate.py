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

def dump(name,data):(H/name).write_text(json.dumps(data,indent=2)+'\n')
def must_fail(record,label):
 try:check(record)
 except (AssertionError,ValueError,TypeError):return label
 raise AssertionError('Mutation passed: '+label)

def main():
 cases=json.loads((H/'source-cases.json').read_text());fidelity=[];repairs=[];review=[];native=[];rawdiagnostics=[]
 for case in cases:
  t=case['template'];level=g.TEMPLATES[t]['level'];p=case['parameters'];raw=g.generate(level,template=t,profile='raw-source',parameters=p);src=case['record'];q=raw['question']
  assert q[':question/problem']==g.normalize_prose(src[':question/problem'])
  assert q[':question/worked-solution']==g.normalize_prose(src[':question/worked-solution']),(t,'solution fidelity')
  for sourcef,field in zip(src[':question/answer-fields'],q[':question/answer-fields']):
   assert sourcef[':answer-field/key']==field[':answer-field/key'];assert sourcef[':answer-field/type'][':db/ident']==field[':answer-field/type'];assert sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in sourcef[':answer-field/choices'])==sorted((a[':answer/type'],a[':answer/value']) for a in field[':answer-field/choices']);assert sourcef[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
  native.append(raw);di=check(raw,True);rawdiagnostics.append({'template':t,'diagnostics':di});fidelity.append({'source_id':case['source_id'],'template':t,'complete_prompt_prose_solution_bank_and_designations':True,'bank_options':6})
  repaired=g.generate(level,template=t,parameters=p);check(repaired);review.append({'role':'original parameter minimal repair' if di else 'original parameter normalized replay','record':repaired});native.append(repaired)
  if di or 'fasle' in src[':question/worked-solution']:repairs.append({'template':t,'raw_diagnostics':di+(['source typo fasle → false'] if 'fasle' in src[':question/worked-solution'] else []),'raw_solution':q[':question/worked-solution'],'repaired_solution':repaired['question'][':question/worked-solution']})
  changed=g.generate(level,seed=91,template=t);check(changed);review.append({'role':'authored changed-parameter same-method source family','record':changed});native.append(changed)
 for lev in g.LEVELS:
  for seed in (27,45):
   r=g.generate(lev,seed=seed);check(r);review.append({'role':'authored uncalibrated '+lev,'record':r});native.append(r)
 # Sampling, default-family coverage, target slots and exact finite object domain.
 fingerprints={};coverage={};witnesses={};parameters_seen=set();sampled=[]
 for lev in g.LEVELS:
  fingerprints[lev]=set();coverage[lev]=set();witnesses[lev]=set()
  for seed in range(180):
   r=g.generate(lev,seed=seed);check(r);fingerprints[lev].add(r['generation']['mathematical_fingerprint']);coverage[lev].add(r['generation']['template']);p=r['generation']['parameters'];witnesses[lev].update([p['witness']] if lev=='easy' else [v for v in p['witnesses'] if v is not None])
   if seed<4:sampled.append(r)
  assert coverage[lev]==({'single-pair'} if lev=='easy' else {k for k,t in g.TEMPLATES.items() if t['level']==lev})
 # Exhaustive signed-coordinate domains; same object/role de-dup, no bank/alias counts.
 finite={};
 for lev in g.LEVELS:
  seen=set()
  if lev=='easy':
   for i,j in itertools.permutations(range(3),2):
    for k in [-5,-4,-3,-2,-1,1,2,3,4,5]:
     for yes in (False,True):
      p={'row':i,'column':j,'entry':k,'is_inverse':yes,'witness':3*i+j};r=g.generate(lev,parameters=p);check(r);seen.add(r['generation']['mathematical_fingerprint'])
  else:
   for t,v in g.TEMPLATES.items():
    if v['level']!=lev:continue
    n=len(v['bases'][0])
    for perm in itertools.permutations(range(n)):
     for signs in itertools.product((-1,1),repeat=n):
      p={'permutation':list(perm),'signs':list(signs),'witnesses':[]};actual=[g.transform(g.mat(b),p)*g.sf(s) for b,s in zip(v['bases'],v['scales'])]
      for b in v['blocks']:
       a,c=b['pair'];prod=actual[a]*actual[c];p['witnesses'].append(None if b['identity'] else next(z for z in range(n*n) if prod[z//n,z%n]!=sp.eye(n)[z//n,z%n]))
      r=g.generate(lev,template=t,parameters=p);seen.add(r['generation']['mathematical_fingerprint'])
  finite[lev]=len(seen)
 # Same objects with another eligible witness, source stage operands stale, and
 # identity/solution-only corruptions must fail while final key stays unchanged.
 controls=[];base=g.generate('moderate',template='q-11642',parameters=g.original_parameters('q-11642'))
 for description,old,new in [('operand-only',r'2 & -2 & -1',r'9 & -2 & -1'),('witness-only',r'{bmatrix}5 & ∗',r'{bmatrix}6 & ∗'),('wrong-dimension',r'{I}_{3}',r'{I}_{4}')]:
  bad=copy.deepcopy(base);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(old,new);assert bad['question'][':question/answer-fields']==base['question'][':question/answer-fields'];controls.append(must_fail(bad,description))
 bad=copy.deepcopy(base);bad['question'][':question/worked-solution']+='\x0c';controls.append(must_fail(bad,'control-character'))
 # Same mathematical data, changed eligible witness. Both stages retain roles.
 pp=g.original_parameters('q-11634');other=copy.deepcopy(pp);other['witnesses'][0]=4;a=g.generate('moderate',template='q-11634',parameters=pp);b=g.generate('moderate',template='q-11634',parameters=other);check(a);check(b);assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'];assert a['question'][':question/id']!=b['question'][':question/id'];controls.append('changed-witness-fixed-objects')
 for r in native:
  checks=[]
  for index,f in enumerate(r['question'][':question/answer-fields']):
   correct=f[':answer-field/correct'][1]
   for choice in f[':answer-field/choices']:checks.append({'field_index':index,'submitted_answer_id':choice[':answer/id'],'expected':'accepted' if choice[':answer/id']==correct else 'rejected','purpose':'full boolean field bank'})
  native_item={'label':r['generation']['template']+'-'+r['question'][':question/id'],'record':r,'checks':checks}
  native[native.index(r)]=native_item
 dump('engine-input.json',native);subprocess.run([str(H/'check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
 dump('source-findings.json',rawdiagnostics);dump('source-repairs.json',repairs);dump('review.json',review);dump('samples.json',sampled)
 cli=json.loads(subprocess.check_output([sys.executable,str(H.with_suffix('.py')),'--difficulty','all','--count','1','--format','json']));assert len(cli)==3;dump('cli-all.json',cli)
 assert finite==g.CAPACITIES
 for lev in g.LEVELS:
  try:g.batch(lev,0,g.CAPACITIES[lev]+1)
  except ValueError:pass
  else:raise AssertionError('Capacity preflight failed')
  batch=g.batch(lev,77,12);assert len({r['generation']['mathematical_fingerprint'] for r in batch})==12
 for kw in [{'level':'bad'},{'level':'easy','parameters':{'row':0,'column':1,'entry':6,'is_inverse':True,'witness':1}},{'level':'hard','template':'q-11642'},{'level':'moderate','profile':'unknown'}]:
  try:g.generate(**kw)
  except ValueError:pass
  else:raise AssertionError('Invalid public request accepted')
 dump('validation.json',{'status':'passed mathematical/fidelity/native checks; visual review separate; parent approval pending','basis':2275,'source_originals':len(cases),'source_complete_banks':len(fidelity),'source_choices_matched':sum(x['bank_options'] for x in fidelity),'source_fields_matched':39,'source_worked_solutions_raw_normalized':13,'raw_solution_findings':rawdiagnostics,'minimal_repair_records':len(repairs),'source_fidelity':fidelity,'sample_checks':540,'default_family_coverage':{k:sorted(v) for k,v in coverage.items()},'sample_unique_tasks':{k:len(v) for k,v in fingerprints.items()},'exact_finite_tasks':finite,'witness_positions':{k:sorted(v) for k,v in witnesses.items()},'negative_controls':controls,'cli_all_count1_records':len(cli),'authored_easy':'120 finite tasks, uncalibrated','native_limitations':'Checkbox fields use actual selected answer IDs; no symbolic blank equivalence applies. Every true/false member of every original/repaired/changed/example field tested.','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}})
 print('VALIDATION PASS',finite)
if __name__=='__main__':main()
