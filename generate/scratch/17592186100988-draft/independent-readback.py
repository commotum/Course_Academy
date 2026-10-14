#!/usr/bin/env python3
"""Private independent readback: parsed learner text, complete source shapes, stages.
No generation metadata is used to derive correct entries or operation banks.
"""
import collections, copy, difflib, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('isolated_matrix_draft',SCRIPT)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
SOURCE=ROOT/'generate/runs/current/sources/17592186100988.json'
assert SHA(SOURCE)==SHA(HERE/'source.json')
old=json.loads(SOURCE.read_text())
assert old['basis']==1356
sources={q[':question/math-academy-id']:q for q in old['record'][':knowledge-point/questions']}
STYLE={'q-13488':'inline_radio','q-13496':'inline_radio','q-279260':'display_radio','q-279539':'display_blank','q-279540':'display_blank','q-13497':'display_should_radio','q-125561':'display_noperiod_radio'}
normalize=lambda text:text.replace(r'[\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}')

def parse(text):
 matrices=[]
 for m in re.finditer(r'\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\1\}',text,re.S):
  cells=[[int(c.strip()) for c in row.split('&')] for row in m[2].split(r'\\')]
  assert cells and len({len(row) for row in cells})==1
  matrices.append(cells)
 return matrices

def task(text):
 matrices=parse(text);assert len(matrices)==1
 M=matrices[0];idx=re.search(r'\$\{?([a-z])\}?_\{([1-9])([1-9])\}',text);assert idx
 i,j=int(idx[2]),int(idx[3]);name=idx[1].upper();assert re.search(r'\$([A-Z])\$',text)[1]==name
 assert re.search(r'\b'+name+r'\s*=\s*(?:\[)?\\begin',text)
 value=M[i-1][j-1] if i<=len(M) and j<=len(M[0]) else 'No such entry'
 return M,i,j,name,value

def formatcheck(text):
 assert not any(ord(c)<32 and c not in '\n\t' for c in text)
 assert text.count('$')%2==0
 depth=0
 for c in text:
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0
 assert depth==0

# Convert the original captured schema into the local public representation,
# retaining every learner attribute and presence, removing only database/source
# identity/provenance. References are compared by complete typed answer value.
def shape(q):
 out={k:v for k,v in q.items() if k not in (':db/id',':question/id',':question/math-academy-id',':question/answer-fields')}
 if isinstance(out.get(':question/difficulty'),dict):out[':question/difficulty']=out[':question/difficulty'][':db/ident']
 if ':question/answer-fields' in q:
  fields=[]
  for f in q[':question/answer-fields']:
   F={k:v for k,v in f.items() if k not in (':db/id',':answer-field/id',':answer-field/choices',':answer-field/correct')}
   if isinstance(F[':answer-field/type'],dict):F[':answer-field/type']=F[':answer-field/type'][':db/ident']
   def ashape(a):
    a={k:v for k,v in a.items() if k not in (':db/id',':answer/id')}
    if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
    return a
   F[':answer-field/choices']=sorted((ashape(a) for a in f[':answer-field/choices']),key=lambda a:json.dumps(a,sort_keys=True))
   if ':answer-field/correct' in f:
    ref=f[':answer-field/correct']
    a=ref if isinstance(ref,dict) else next(a for a in f[':answer-field/choices'] if a[':answer/id']==ref[1])
    F[':answer-field/correct']=ashape(a)
   fields.append(F)
  out[':question/answer-fields']=fields
 return out

C=collections.Counter();records=[];native=[];profiles=set();targets=collections.defaultdict(set)
def check(r,require_bank=True):
 q=r['question'];M,i,j,name,value=task(q[':question/problem']);m,n=len(M),len(M[0])
 formatcheck(q[':question/problem']);assert m!=n
 for a,I,J in re.findall(r'\{?([a-z])\}?_\{([1-9])([1-9])\}',q[':question/problem']):assert (a.upper(),int(I),int(J))==(name,i,j)
 f,=q[':question/answer-fields'];bank=f[':answer-field/choices'];values=[]
 for a in bank:
  formatcheck(a[':answer/value']);v=a[':answer/value'] if a[':answer/type']==':answer.type/text' else int(a[':answer/value'])
  assert a[':answer/type']==(':answer.type/text' if v=='No such entry' else ':answer.type/math')
  assert v not in values;values.append(v);C['displayed_values']+=1
 assert values.count(value)==1
 if ':answer-field/correct' in f:
  correct=f[':answer-field/correct'];assert correct[0]==':answer/id'
  assert next(v for a,v in zip(bank,values) if a[':answer/id']==correct[1])==value
  C['read_correct_refs']+=1
 else:assert not r['generation']['eligible_for_learning']
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];formatcheck(sol)
  assert parse(sol)==[M];C['identical_repeated_matrices']+=1
  for a,I,J in re.findall(r'\{?([a-z])\}?_\{([1-9])([1-9])\}',sol):assert (a.upper(),int(I),int(J))==(name,i,j)
  prose=re.search(r'intersection of the \$([1-9])\$(st|nd|rd|th) row and \$([1-9])\$(st|nd|rd|th) column',sol);assert prose
  suffix=lambda k:{1:'st',2:'nd',3:'rd'}.get(k,'th')
  assert prose.groups()==(str(i),suffix(i),str(j),suffix(j))
  C['row_column_prose']+=1
  if value=='No such entry':assert f'has ${m}$ rows and ${n}$ columns' in sol and 'no such entry' in sol
  else:
   final=re.search(r'Therefore, \$\{?([a-z])\}?_\{([1-9])([1-9])\}=(-?\d+)\.\$',sol);assert final and (final[1].upper(),int(final[2]),int(final[3]),int(final[4]))==(name,i,j,value)
  # Two-sentence source chain: locate intersection, therefore entry; repeated
  # matrix follows. Missing-entry completion uses the recorded dimension stage.
  assert sol.startswith('The entry $') and sol.count('intersection of the')==1
  assert sol.count('Therefore,')==(value!='No such entry')
  assert sol.find('intersection of the')<sol.find(r'\begin{')
  if value!='No such entry':assert sol.find('Therefore,')<sol.find(r'\begin{')
  C['operative_stage_sequences']+=1
 if r['generation']['eligible_for_learning'] and require_bank:
  profile=r['generation']['profile'];profiles.add(profile)
  row=i+1 if i<m else i-1;col=j+1 if j<n else j-1
  if profile=='overflow_locations':
   assert (i==m+1 and j<=n) or (j==n+1 and i<=m)
   pos=[None,(m,j),(1,j),(m,col),(1,col)] if i==m+1 else [None,(i,n),(i,1),(row,n),(row,1)]
  else:
   pos=[(i,j)]
   if profile=='location_no_entry':pos +=[(row,j),(i,col),(row,col),None]
   elif profile=='four_locations':
    other=j-1 if j>1 and j-1!=col else j+2 if j+2<=n else j-2
    pos +=[(row,j),(i,col),(row,col),(i,other)]
   elif profile=='swap_no_entry':pos +=[(j,i),(row,j),(i,col),None]
   else:assert profile=='blank'
  expected=['No such entry' if p is None else M[p[0]-1][p[1]-1] for p in pos]
  assert len(expected)==len(values) and set(expected)==set(values);C['whole_method_banks']+=1
  level=q[':question/difficulty'].split('/')[-1];targets[level].add((m,n,i,j))
  assert (m,n) in {'easy':((2,3),(3,2),(3,4),(5,4)),'moderate':((5,6),(6,5)),'hard':((6,7),(7,6))}[level]
  assert level=='easy' or max(i,j)>=({'moderate':4,'hard':5}[level])
 C['records']+=1;records.append(r)
 return r

for sid,original in sources.items():
 r=check(g.generate('easy',profile='raw:'+sid))
 assert shape(r['question'])==shape(original),(sid,'raw attribute/feedback/presence mismatch')
 C['source_prompts']+=1;C['source_fields']+=len(original[':question/answer-fields']);C['source_values']+=sum(len(f[':answer-field/choices']) for f in original[':question/answer-fields']);C['source_banks']+=1
 C['source_solutions']+=(':question/worked-solution' in original);C['source_correct_refs']+=(':answer-field/correct' in original[':question/answer-fields'][0]);C['source_unrated']+=(':question/difficulty' not in original)
 # The public repaired evidence profile preserves all available stages after
 # notation normalization, with completed missing attributes explicitly labeled.
 repaired=check(g.generate('easy',profile='completed:'+sid))
 assert repaired['question'][':question/problem']==normalize(original[':question/problem'])
 if ':question/worked-solution' in original:assert repaired['question'][':question/worked-solution']==normalize(original[':question/worked-solution']);C['normalized_source_solutions']+=1
 changed=copy.deepcopy(r['generation']['parameters']);changed['letter']='Z';changed['matrix']=[[-v for v in row] for row in changed['matrix']];changed['external']={k:-v for k,v in changed['external'].items()}
 check(g.generate('easy',profile='raw:'+sid,parameters=changed));C['signed_source_banks']+=1

# Fresh records reuse the parent seeds and all eligible source-shaped styles.
for level in ('easy','moderate','hard'):
 for seed in range(18):check(g.generate(level,seed))
 for template in g.level_templates(level):
  for seed in (915,937):check(g.generate(level,seed,template=template))

# Change the requested coordinate with all matrix entries held fixed. This
# explicitly exercises the row/column slots, apart from sign/letter changes.
for level,m,n,a,b in [('easy',3,4,(2,3),(3,2)),('moderate',5,6,(4,4),(5,4)),('hard',6,7,(5,5),(6,5))]:
 matrix=[[(row*n+col)%19-9 for col in range(n)] for row in range(m)]
 pair=[check(g.generate(level,template='display_blank',profile='blank',parameters={'matrix':matrix,'i':i,'j':j,'letter':'A'})) for i,j in (a,b)]
 assert pair[0]['generation']['mathematical_fingerprint']!=pair[1]['generation']['mathematical_fingerprint']
 C['fixed_matrix_changed_target_pairs']+=1

# Reconstruct exact approved script bytes to demonstrate full change scope.
baseline=ROOT/'generate/scratch/17592186100988.py'
s=baseline.read_text();start=s.index(' # Keep raw capture replay intact;');end=s.index(" question={':question/problem':prompt}",start)
previous=(s[:start]+s[end:]).replace("VERSION='rectangular-entry-lookup-v5'","VERSION='rectangular-entry-lookup-v4'")
assert hashlib.sha256(previous.encode()).hexdigest()=='fe013d92f9ab53744195234eff02e784d82d9ffa7efd9ce8517762ba4a5998a3'
parent=json.loads((ROOT/'generate/runs/current/qa/17592186100988-sampled.json').read_text())
for r in parent:
 meta=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
 fresh=g.generate(level,meta['seed'],meta['template'],parameters=meta['parameters'],profile=meta['profile'])
 a=shape(r['question']);b=shape(fresh['question'])
 for k in (':question/problem',':question/worked-solution'):a[k]=normalize(a[k])
 assert a==b
 C['prior_parent_records_unchanged_except_notation']+=1

# The refreshed capture confirms the published notation repair while retaining
# exactly the seven MA originals. It does not replace the immutable raw basis.
refreshed_path=ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186100988.json'
refreshed=json.loads(refreshed_path.read_text());assert refreshed['basis']==2275
refreshed_sources={q[':question/math-academy-id']:q for q in refreshed['record'][':knowledge-point/questions']}
assert set(refreshed_sources)==set(sources)
changed_sources=[]
for sid,original in sources.items():
 a=shape(original);b=shape(refreshed_sources[sid])
 if a!=b:changed_sources.append(sid)
 for k in (':question/problem',':question/worked-solution'):
  if k in a:a[k]=normalize(a[k])
 assert a==b,(sid,'refresh includes a change beyond presentation')
assert len(changed_sources)==5
C['refreshed_sources_unchanged_except_notation']=7

# Actual CLI output must match public calls and retain both unrated omissions.
for args in (['--difficulty','all','--seed','42','--count','2'],['--difficulty','easy','--profile','raw:q-13488'],['--difficulty','easy','--profile','raw:q-13496']):
 result=subprocess.run([sys.executable,str(SCRIPT),*args,'--format','json'],check=True,capture_output=True,text=True)
 rows=json.loads(result.stdout)
 if args[1]=='all':assert len(rows)==6
 for r in rows:
  check(r);m=r['generation'];level=r['question'].get(':question/difficulty',':question.difficulty/easy').split('/')[-1]
  replay=g.generate(level,m['seed'],m['template'],parameters=m['parameters'],profile=m['profile'])
  assert shape(r['question'])==shape(replay['question'])
  assert r['question'][':question/id']==replay['question'][':question/id']
  if m['profile'] in ('raw:q-13488','raw:q-13496'):assert ':question/difficulty' not in r['question'] and ':question/worked-solution' not in r['question']
 again=subprocess.run([sys.executable,str(SCRIPT),*args,'--format','json'],check=True,capture_output=True,text=True)
 assert result.stdout==again.stdout
 subprocess.run([sys.executable,str(SCRIPT),*args,'--format','markdown'],check=True,capture_output=True,text=True)
 C['deterministic_cli_commands']+=2

# Native fixture cases from the independent actual-text key: raw missing refs
# are preserved above; completed profiles author their checked refs for fixtures.
for k,r in enumerate(records):
 f=r['question'][':question/answer-fields'][0]
 if ':answer-field/correct' not in f:continue
 correct=task(r['question'][':question/problem'])[-1]
 if f[':answer-field/type']==':answer-field.type/radio':
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==str(correct) else 'rejected','purpose':'independent displayed entry'} for a in f[':answer-field/choices']]
 else:
  checks=[{'submitted':v,'expected':expected,'purpose':'independent scalar readback'} for v,expected in [(str(correct),'accepted'),(f'({correct*3})/3','accepted'),(str(correct+1),'rejected')]]
 native.append({'label':f'independent-{k}','record':r,'checks':checks})
(HERE/'independent-native-input.json').write_text(json.dumps(native,indent=2)+'\n')
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'independent-native-input.json'),str(HERE/'independent-native.json')],check=True)
report={'status':'passed','kp_id':17592186100988,'script_sha256':SHA(SCRIPT),'registered_baseline_sha256':SHA(baseline),'source_sha256':SHA(SOURCE),'source_basis':1356,'refreshed_source_comparison':{'basis':2275,'sha256':SHA(refreshed_path),'original_sources':7,'presentation_repaired_sources':changed_sources,'new_source_families':0},'counts':dict(C),'default_profiles':sorted(profiles),'observed_target_slots':{level:sorted(values) for level,values in targets.items()},'change_scope':'Exact old script reconstructed by removing bmatrix normalization block and reverting v5 to v4; presentation and version only, no math changes.','source_attribute_contract':'Exact learner attribute/feedback presence; original IDs/db IDs retained in immutable evidence, generated owned UUIDs checked through refs.','all_original_templates_included':True,'limitations':['No observed moderate/hard labels; explicit visual scan extensions remain design claims.','Two raw sources have no ratings/refs/solutions and remain evidence only.','Opaque external source distractors remain evidence only.'],'native':{k:v for k,v in json.loads((HERE/'independent-native.json').read_text()).items() if k!='records'}}
(HERE/'independent-sampled.json').write_text(json.dumps(records,indent=2)+'\n')
(HERE/'independent-readback.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='observed_target_slots'},indent=2))
