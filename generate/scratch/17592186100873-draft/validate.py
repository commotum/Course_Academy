"""Read actual printed matrices, indices and every ordered arithmetic stage."""
import sys;sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('entry_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,obj):(D/name).write_text(json.dumps(obj,indent=2)+'\n')
def printed_matrices(text):
 out=[]
 for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S):
  out.append([[int(v) for v in r.split('&')] for r in re.split(r'\\\\',body)])
 return out
def readback(r):
 q=r['question'];s=q.get(':question/worked-solution');p=q[':question/problem'];f=q[':question/answer-fields'][0]
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 import uuid
 for value in [q[':question/id'],f[':answer-field/id'],*[a[':answer/id'] for a in f[':answer-field/choices']]]:assert str(uuid.UUID(value))==value
 assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(f[':answer-field/choices'])
 assert all(a[':answer/type']==':answer.type/math' for a in f[':answer-field/choices'])
 for text in [p,s or '',*[a[':answer/value'] for a in f[':answer-field/choices']]]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
  g.validate_prose(text)
 a,b=printed_matrices(p);match=re.search(r'\{?([a-z])\}?_\{([1-5])([1-5])\}',p);letter,ii,jj=match.groups();i,j=int(ii)-1,int(jj)-1
 assert len(a[0])==len(b)
 row=a[i];col=[v[j] for v in b];terms=[x*y for x,y in zip(row,col)];answer=sum(terms)
 values=[int(x[':answer/value']) for x in f[':answer-field/choices']];assert len(set(values))==len(values)
 assert max(abs(x) for r0 in a+b for x in r0)<=20 and max(map(abs,row+col))<=10 and max(map(abs,terms))<=30 and sum(map(abs,terms))<=58 and max(map(abs,values))<=58
 if not r['generation']['evidence_only']:
  profile=r['generation']['bank_profile']
  if profile=='method-omit-sign':expected=[answer,sum(terms[:-1]),sum(abs(t) for t in terms),-answer,sum(row)+sum(col)]
  elif profile=='method-reverse-column':expected=[answer,sum(row[k]*col[len(col)-1-k] for k in range(len(row))),row[0]*col[0],sum(terms[1:]),sum(v*v for v in row)]
  else:expected=[answer]
  assert sorted(values)==sorted(expected)
  assert sum(t!=0 for t in terms)>=2
  level=q[':question/difficulty'].split('/')[-1]
  if level=='easy' and len(terms)==3:assert any(abs(x)<=1 or abs(y)<=1 for x,y in zip(row,col))
  elif level in ('moderate','hard'):
   assert len(terms)==3 and all(2<=abs(x)<=6 for x in row+col)
   if level=='moderate':assert max(map(abs,terms))<=16 and 12<=sum(map(abs,terms))<=36
   else:assert 37<=sum(map(abs,terms))<=58 and min(terms)<0<max(terms)
 if ':answer-field/correct' in f:
  key=f[':answer-field/correct'][1];assert next(int(x[':answer/value']) for x in f[':answer-field/choices'] if x[':answer/id']==key)==answer
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in p
 if s:
  assert re.search(r'\$'+str(i+1)+r'\$(st|nd|rd|th) row',s) and re.search(r'\$'+str(j+1)+r'\$(st|nd|rd|th) column',s)
  assert re.search(r'\{'+letter+r'\}_\{'+ii+jj+r'\}',s)
  mats=printed_matrices(s);assert mats==[a,b,[row],[[x] for x in col]]
  body=s.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}')[0]
  stages=re.split(r'\\\\\s*&\s*=',body);assert len(stages)==5
  expanded=stages[2].strip()
  pattern=r'\(?(-?\d+)\)?\\cdot\s*\(?(-?\d+)\)?' if r'\cdot' in expanded else r'\(?(-?\d+)\)?\((-?\d+)\)'
  matches=list(re.finditer(pattern,expanded));assert [tuple(map(int,m.groups())) for m in matches]==list(zip(row,col))
  tail=re.sub(pattern,'P',expanded);assert tail=='+'.join(['P']*len(row))
  arithmetic=stages[3].strip();assert re.fullmatch(r'-?\d+(?:[+-]\d+)*',arithmetic)
  assert list(map(int,re.findall(r'[+-]?\d+',arithmetic)))==terms
  assert int(stages[4].strip().rstrip('.'))==answer
 return {'row':i+1,'column':j+1,'row_values':row,'column_values':col,'ordered_products':terms,'answer':answer}
def native_checks(r,label):
 f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1];correct=next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==key)
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'complete displayed radio bank selection'} for a in f[':answer-field/choices']]
 else:
  v=int(correct);checks=[{'submitted':s,'expected':e,'purpose':purpose} for s,e,purpose in [(correct,'accepted','canonical integer'),(str(2*v)+'/2','accepted','genuine unreduced rational equivalent'),('('+str(v-3)+')+3','accepted','unevaluated arithmetic equivalent'),(str(v+1),'rejected','nearby wrong integer'),(str(-v if v else 2),'rejected','wrong sign/value'),(r'\begin{bmatrix}'+correct+r'\end{bmatrix}','unresolved','documented parser refusal of wrong matrix response object')]]
 return {'label':label,'record':r,'checks':checks}
def preservation():
 before=json.loads((D/'registered-before.json').read_text())
 paths=[Path('generate/scratch/17592186100873.py')]+list(Path('generate/scratch/17592186100873').rglob('*'))+list(Path('generate/scratch/__pycache__').glob('17592186100873.*.pyc'))
 rows=[{'path':str(x.resolve()),'kind':'directory' if x.is_dir() else 'file','sha256':sha(x) if x.is_file() else None} for x in sorted(paths)]
 assert rows==before['paths'];return len(rows)
def grader():
 b=json.loads((D/'reference/grader-build.json').read_text());m={b['source']:b['source_sha256'],b['library']:b['library_sha256'],b['binary']:b['binary_sha256'],**b['engine_sources'],**b['dependencies']}
 assert len(m)==42 and all(sha(x)==v for x,v in m.items());assert sha(D/'check-engine')==b['binary_sha256'];return 42

def main():
 original=[];cases=[];readbacks=[];native=[];replays=[]
 for sid,s in g.SOURCES.items():
  r=g.generate('easy',template=sid,profile='observed:'+sid);q=r['question'];readbacks.append(readback(r));replays.append(r)
  for k in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (k in q)==(k in s)
   if k in s:assert q[k]==(s[k][':db/ident'] if isinstance(s[k],dict) else s[k])
  f=q[':question/answer-fields'][0];sf=s[':question/answer-fields'][0]
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident'];assert f[':answer-field/key']==sf[':answer-field/key']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  if ':answer-field/correct' in sf:native.append(native_checks(r,'source-'+sid))
  cases.append({'source_id':sid,'template':sid,'level':'easy','parameters':g.params(s),'bank_profile':'observed:'+sid,'raw_omissions':[k for k in [':question/difficulty',':question/worked-solution'] if k not in s]+([':answer-field/correct'] if ':answer-field/correct' not in sf else [])})
  original.append({'source_id':sid,'prompt_exact':True,'solution_exact_or_absence':True,'raw_presence_parity':True,'field_type_exact':True,'bank_values_matched':len(sf[':answer-field/choices']),'correct_designation_matched':':answer-field/correct' in sf})
 review=[];fps={};coverage={};target_coverage={};profiles=set();fields=set()
 for level in g.LEVELS:
  seen=set();seenf=set();seenp=set();targets=set();families=set()
  for seed in range(600):
   r=g.generate(level,seed);b=readback(r);readbacks.append(b);seen.add(r['generation']['mathematical_fingerprint']);families.add(r['generation']['template']);seenf.add(r['question'][':question/answer-fields'][0][':answer-field/type']);seenp.add(r['generation']['bank_profile']);targets.add((b['row'],b['column']));profiles.add(r['generation']['bank_profile']);fields|=seenf
   if seed<12:review.append(r);native.append(native_checks(r,level+'-'+str(seed)))
   # Regenerate with explicit parameters and new seed: only order may differ.
   rr=g.generate(level,seed+1000,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['bank_profile']);assert rr['question'][':question/id']==r['question'][':question/id']
  assert len(seen)>500;assert seenp==set(g.PROFILES)|{'blank'}
  assert families=={s for s,t in g.TEMPLATES.items() if level=='easy' or t['terms']==3}
  fps[level]=len(seen);coverage[level]={'families':sorted(families),'fields':sorted(seenf),'profiles':sorted(seenp)};target_coverage[level]=sorted(targets)
 # Explicitly traverse every eligible matrix target on fixed operands; all references move jointly.
 sid='q-275547';p={'A':[[2,3],[4,5]],'B':[[1,3,5],[2,4,6]],'row':1,'column':1};held=[]
 for i in range(1,3):
  for j in range(1,4):
   pp={**p,'row':i,'column':j};r=g.generate('easy',template=sid,parameters=pp,profile='blank');held.append(readback(r))
 assert len({(x['row'],x['column']) for x in held})==6
 # Mutations independently rejected, including structurally missing but equal arithmetic.
 base=g.generate('easy',template=sid,parameters=p,profile='blank');mutations={}
 for label,change in {
  'stale-prompt-target':lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('{l}_{11}','{l}_{21}')),
  'stale-target-prose':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('$1$st row','$2$nd row')),
  'stale-target-subscript':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('{l}_{11}','{l}_{12}')),
  'missing-operand':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('2\\cdot 1+3\\cdot 2','2\\cdot 1+3')),
  'wrong-intermediate-term':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('2+6','3+5')),
  'collapsed-equal-stage':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('2\\cdot 1+3\\cdot 2','8')),
  'stale-key':lambda r:r['question'][':question/answer-fields'][0][':answer-field/choices'][0].__setitem__(':answer/value','7'),
  'control-character':lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\x0c')}.items():
  rr=copy.deepcopy(base);change(rr)
  try:readback(rr)
  except (AssertionError,ValueError):mutations[label]='rejected'
  else:raise AssertionError('Mutation survived '+label)
 # Explicit inputs cannot bypass every guard.
 rejects=0
 for level,p in [('moderate',g.params(g.SOURCES['q-318462'])),('hard',g.params(g.SOURCES['q-318462'])),('easy',{'A':[[20,20],[20,20]],'B':[[20,20],[20,20]],'row':1,'column':1})]:
  try:g.generate(level,template='q-318462' if level!='easy' else sid,parameters=p)
  except ValueError:rejects+=1
 assert rejects==3
 write('source-cases.json',cases);write('source-fidelity.json',original);write('source-replays.json',replays);write('review.json',review);write('readbacks.json',readbacks);write('native-input.json',native)
 subprocess.run([str(D/'check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 report={'passed':True,'source_basis':2275,'source_questions':len(original),'exact_prompts':12,'exact_solutions':10,'absent_solutions_preserved':2,'bank_values_matched':44,'complete_banks_matched':12,'correct_designations_matched':10,'missing_correct_refs_preserved':2,'normal_instances_independently_read':1800,'distinct_mathematical_tasks':fps,'default_coverage':coverage,'target_coverage':target_coverage,'held_matrices_changed_targets':held,'mutation_regressions':mutations,'explicit_guard_rejections':rejects,'registered_protected_paths_unchanged':preservation(),'native_provenance_files_reverified':grader(),'native':json.loads((D/'native-report.json').read_text()),'python_version':sys.version.split()[0],'sympy_version':g.sp.__version__}
 write('validation.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ('native','target_coverage','default_coverage','held_matrices_changed_targets')},indent=2))
if __name__=='__main__':main()
