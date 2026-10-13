#!/usr/bin/env python3
"""Independent displayed-table, arrow, bullet, bank, identity and native-grader QA."""
import collections,concurrent.futures,difflib,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
from html.parser import HTMLParser
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('route_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Independently read from all seven actual captured images, rows = departure.
# This fixture is NOT computed from answers or generator metadata.
READ_IMAGES={'q-138940':[[0,1,1],[0,1,2],[1,0,0]],'q-139685':[[0,1,1],[0,0,1],[1,1,0]],'q-139689':[[1,1,0],[0,1,2],[0,1,0]],'q-139719':[[0,1,0,2],[0,0,1,0],[0,0,0,1],[0,0,1,0]],'q-319346':[[0,2,0],[1,0,3],[2,0,0]],'q-319412':[[0,1,2,0],[2,0,1,0],[1,0,0,2],[0,1,1,0]],'q-319429':[[1,1,3],[1,2,2],[0,1,1]]}
class TableReader(HTMLParser):
 def __init__(self):super().__init__();self.rows=[];self.cell=None
 def handle_starttag(self,tag,attrs):
  if tag=='tr':self.rows.append([])
  if tag=='td':self.cell=''
 def handle_data(self,data):
  if self.cell is not None:self.cell+=data
 def handle_endtag(self,tag):
  if tag=='td':self.rows[-1].append(self.cell);self.cell=None

def read_table(text):
 if '<table' in text:
  reader=TableReader();reader.feed(text);rows=reader.rows
 else:rows=[[x.strip() for x in line.split('|')[1:-1]] for line in text.splitlines() if line.startswith('|')]
 header=next(row for row in rows if all('**'+x+'**' in row or x in row for x in ['A','B','C']))
 headers=[x.strip('*') for x in header if x.strip('*') in 'ABCD' and x.strip('*')]
 n=len(headers);entries={};holes={};actualrows=[]
 for row in rows:
  labels=[i for i,x in enumerate(row) if x.strip('*') in 'ABCD' and x.strip('*')]
  if len(labels)!=1:continue
  k=labels[0];label=row[k].strip('*');values=row[k+1:k+1+n]
  if len(values)!=n:raise AssertionError('table row has incorrect entry count')
  actualrows.append(label)
  for c,value in zip(headers,values):
   value=value.strip('$')
   if re.fullmatch('[0-3]',value):entries[(label,c)]=int(value)
   elif re.fullmatch('[abc]',value) or re.fullmatch(r'\{\{field-[123]\}\}',value):holes[value]=(label,c)
   else:raise AssertionError('invalid full entry: '+value)
 assert len(actualrows)==n and len(set(actualrows))==n
 return entries,holes,actualrows,headers

def check(record,raw=False):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 q=record['question'];gen=record['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];fields=q[':question/answer-fields']
 for text in (prompt,sol):
  assert text.count('$')%2==0
  stack=0
  for char in text:
   if char=='{':stack+=1
   if char=='}':stack-=1
   assert stack>=0
  assert stack==0
 e,h,rows,cols=read_table(prompt);complete,unused,srows,scols=read_table(sol)
 assert not unused and srows==rows and scols==cols
 if gen['assets']['source_reuse']:m=READ_IMAGES[gen['source_ids'][0]]
 else:
  side=json.loads(Path(gen['assets']['prompt']).with_suffix('.json').read_text());n=len(side['coordinates']);m=[[0]*n for _ in range(n)]
  for edge in side['edges']:m[edge['from']][edge['to']]+=1
  assert m==side['matrix']
 assert len(m)==len(rows)
 for (r,c),value in complete.items():assert value==m['ABCD'.index(r)]['ABCD'.index(c)]
 for rc,value in e.items():assert value==complete[rc]
 expected={key:complete[rc] for key,rc in h.items()}
 assert len(expected)==3
 for i,f in enumerate(fields):
  assert isinstance(f[':answer-field/type'],str)
  values=[a[':answer/value'] for a in f[':answer-field/choices']]
  assert len(values)==len(set(values)) and all(re.fullmatch(r'\d+',x) for x in values)
  ids=[a[':answer/id'] for a in f[':answer-field/choices']];correct=f[':answer-field/correct'][1]
  assert len(ids)==len(set(ids)) and correct in ids
  answer=next(int(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==correct)
  if f[':answer-field/type'].endswith('/blank'):
   assert '{{'+f[':answer-field/key']+'}}' in prompt and len(values)==1
   assert answer==expected['{{'+f[':answer-field/key']+'}}']
  else:
   assert len(values)==5 and answer==sum(expected.values())
   if gen['bank_profile']=='authored_omissions':
    a,b,c=[expected[x] for x in 'abc'];reverse=sum(complete[(col,row)] for row,col in h.values())
    assert set(map(int,values))=={a+b+c,a+b,a+c,reverse,sum(complete.values())}
   elif gen['bank_profile']=='authored_count_window':
    start=max(0,answer-2)
    assert set(map(int,values))==set(range(start,start+5))
 bullets=re.findall(r'^- .*?(?=\n\n|$)',sol,re.M);assert len(bullets)==3
 for i,b in enumerate(bullets):
  match=re.search(r'There (?:is|are) (?:\$(\d+)\$|no) arrows? starting at Station ([A-D]) and ending at Station ([A-D])',b);assert match
  v=int(match[1] or '0');rc=(match[2],match[3]);assert v==complete[rc]
  # Raw q319429 refers to B->C rather than requested B->B; explicitly audited.
  target=h.get('abc'[i],h.get('{{field-'+str(i+1)+'}}'))
  if not raw:assert rc==target
  rhs=re.search(r'([abc])=(\d+)',b)
  if rhs:assert int(rhs[2])==expected[rhs[1]]
 if 'a+b+c=' in sol or 'a + b + c =' in sol:
  final=re.search(r'\$\$\n(.*?)\n\$\$',sol,re.S)[1].rstrip('.')
  parts=final.split('=');assert len(parts)==3
  assert sp.sympify(parts[1])==sp.sympify(parts[2])==sum(expected.values())
  summands=[int(x) for x in parts[1].split('+')];assert summands==[expected[x] for x in 'abc']
 assert Path(gen['assets']['prompt']).exists()
 return expected

def grading_fixture(label,rec):
 checks=[]
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  cid=f[':answer-field/correct'][1]
  for a in f[':answer-field/choices']:
   checks.append({'field_index':i,('submitted' if f[':answer-field/type'].endswith('/blank') else 'submitted_answer_id'):(a[':answer/value'] if f[':answer-field/type'].endswith('/blank') else a[':answer/id']),'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'canonical blank entry' if f[':answer-field/type'].endswith('/blank') else 'complete displayed bank selection'})
  if f[':answer-field/type'].endswith('/blank'):
   val=int(f[':answer-field/choices'][0][':answer/value'])
   checks.extend([{'field_index':i,'submitted':str(val)+'+0','expected':'accepted','purpose':'equivalent unreduced count expression'},{'field_index':i,'submitted':str(val+1),'expected':'rejected','purpose':'wrong count'}])
 return {'label':label,'record':rec,'checks':checks}

def main():
 cases=json.loads((HERE/'source-cases.json').read_text());review=[];fixtures=[];fidelity=[];bank_values=0;designation=0;solution_exact=0
 for case in cases:
  rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(rec)
  source=g.SOURCES[case['source_id']];q=rec['question']
  assert q[':question/problem'].split('\n',1)[1]==source[':question/problem'].split('\n',1)[1]
  bykey={f[':answer-field/key']:f for f in q[':question/answer-fields']}
  for f in source[':question/answer-fields']:
   new=bykey[f[':answer-field/key']];assert new[':answer-field/type']==f[':answer-field/type'][':db/ident']
   assert sorted(a[':answer/value'] for a in new[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
   bank_values+=len(f[':answer-field/choices'])
   if ':answer-field/correct' in f:
    assert next(a[':answer/value'] for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1])==f[':answer-field/correct'][':answer/value'];designation+=1
  original=source.get(':question/worked-solution');exact=original is not None and q[':question/worked-solution']==original
  if original and not exact:assert case['source_id']=='q-319429'
  solution_exact+=int(exact)
  fidelity.append({'source_id':case['source_id'],'prompt_exact_except_local_asset_path':True,'complete_bank':True,'correct_designation':'matched' if all(':answer-field/correct' in f for f in source[':question/answer-fields']) else 'absent in capture; independently inferred','solution':'exact' if exact else 'minimal direction repair' if original else 'absent in capture; authored three-count solution'})
  review.append({'label':'Original replay '+case['source_id'],'record':rec});fixtures.append(grading_fixture(case['source_id'],rec))
 rawcase=next(c for c in cases if c['source_id']=='q-319429');raw=g.generate('easy',template=rawcase['template'],parameters=rawcase['parameters'],profile='raw_solution_319429');check(raw,raw=True);assert raw['question'][':question/worked-solution']==g.SOURCES['q-319429'][':question/worked-solution']
 review.append({'label':'Raw observed prose q-319429 (direction error retained as evidence)','record':raw})
 # Two actual rendered variants of each template cover each observed bank layout.
 for name,level in g.TEMPLATES.items():
  for k in range(2):
   profile=('observed_'+g.SPECS[name]['source'][2:]) if name.startswith('sum_') and name in g.SPECS else None
   rec=g.generate(level,seed=103+k,template=name,profile=profile);check(rec)
   review.append({'label':'Generated variant '+level+' '+name+' '+str(k+1),'record':rec});fixtures.append(grading_fixture(name+'-'+str(k),rec))
   # Actual rendered identity stable under shuffled choice order.
   changed=g.generate(level,seed=997,template=name,parameters=rec['generation']['parameters'],profile=rec['generation']['bank_profile']);check(changed)
   assert changed['question'][':question/id']==rec['question'][':question/id']
   assert changed['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
 # Authored omission banks are not falsely declared source misconception recipes.
 for level,name in [('easy','sum_138940'),('moderate','sum_139689')]:
  for k in range(2):
   rec=g.generate(level,seed=200+k,template=name,profile='authored_omissions');check(rec);review.append({'label':'Optional authored omission bank '+level+' '+str(k+1),'record':rec});fixtures.append(grading_fixture('authored-'+level+str(k),rec))
 # Level guards and meaningful finite variation independent of renderer cost.
 variety={}
 for name,level in g.TEMPLATES.items():
  fingerprints=set();rng=__import__('random').Random(17)
  for i in range(500):
   p=g.sample(level,name,rng)
   try:g.guard(level,name,p)
   except ValueError:continue
   fingerprints.add(g.digest(p))
  assert len(fingerprints)>=50;variety[name]=len(fingerprints)
 authored_sums={}
 for name,level in g.TEMPLATES.items():
  if name.startswith('blanks'):continue
  rng=__import__('random').Random(33);sums=set()
  for i in range(1000):
   p=g.sample(level,name,rng)
   try:g.guard(level,name,p)
   except ValueError:continue
   m=p['matrix'];v=[m[r][c] for r,c in p['holes']]
   if name in g.SPECS:
    source=g.SOURCES[g.SPECS[name]['source']]
    bank={int(a[':answer/value']) for a in source[':question/answer-fields'][0][':answer-field/choices']}
    if sum(v) not in bank:continue
   sums.add(sum(v))
  assert len(sums)>=3;authored_sums[name]=sorted(sums)
 for invalid in [dict(rawcase['parameters'],matrix=[[4,1,3],[1,2,2],[0,1,1]]),dict(rawcase['parameters'],row_order=[2,0,1])]:
  try:g.generate('easy',template=rawcase['template'],parameters=invalid)
  except ValueError:pass
  else:raise AssertionError('explicit invalid input admitted')
 hard=next(x['record'] for x in review if x['record']['generation']['level']=='hard')
 bad=dict(hard['generation']['parameters'],col_order=hard['generation']['parameters']['row_order'])
 try:g.generate('hard',parameters=bad)
 except ValueError:pass
 else:raise AssertionError('hard workload guard bypassed')
 # Fresh concurrent same/different matrices; atomic PNGs and input isolation.
 inputs=[]
 for seed in range(500,5500):
  rng=__import__('random').Random(seed);p=g.sample('hard','sum_permuted_four',rng)
  try:g.guard('hard','sum_permuted_four',p)
  except ValueError:continue
  v=[p['matrix'][r][c] for r,c in p['holes']]
  if len(set([sum(v),v[0]+v[1],v[0]+v[2],sum(p['matrix'][c][r] for r,c in p['holes']),sum(map(sum,p['matrix']))]))!=5:continue
  out=HERE/'plots'/(g.digest({'matrix':p['matrix'],'renderer':'directed-v1'})+'.png')
  if not out.exists():inputs.append(p)
  if len(inputs)==2:break
 assert len(inputs)==2
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  concurrent_records=list(pool.map(lambda p:g.generate('hard',parameters=p),[inputs[0],inputs[0],inputs[1]]))
 for rec in concurrent_records:check(rec)
 assert concurrent_records[0]['question'][':question/id']==concurrent_records[1]['question'][':question/id']
 assert concurrent_records[0]['question'][':question/id']!=concurrent_records[2]['question'][':question/id']
 (HERE/'grading-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'grading-input.json'),str(HERE/'grading-report.json')],check=True)
 native=json.loads((HERE/'grading-report.json').read_text());assert native['documented_unresolved_checks']==0
 (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 blocks=['# Matrices for Route Planning: source and generated review','Basis 1356; raw capture in source.json. Source figure paths alone are localized. Observed scalar windows are catalogs with unresolved author intent, not inferred errors. Generated counts are independently read from arrow sidecars and displayed ordered tables.']
 for item in review:
  rec=item['record'];q=rec['question'];blocks.extend(['## '+item['label'],q[':question/problem']])
  for f in q[':question/answer-fields']:
   blocks.append('**'+f[':answer-field/key']+' ('+f[':answer-field/type'].split('/')[-1]+'):** '+', '.join(a[':answer/value']+(' ✓' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']))
  blocks.append(q[':question/worked-solution'])
 (HERE/'review.md').write_text('\n\n'.join(blocks)+'\n')
 report={'version':g.VERSION,'status':'passed with documented source repairs/absences','source':{k:g.CAPTURE[k] for k in ('database','basis','lineage')},'source_questions':7,'complete_banks_matched':7,'displayed_values_matched':bank_values,'displayed_values_total':29,'observed_correct_designations_matched':designation,'observed_correct_designations_total':11,'missing_designations_independently_inferred':2,'worked_solutions_raw_exact':5,'worked_solutions_raw_total':5,'normal_worked_solutions_exact':solution_exact,'normal_worked_solutions_observed_total':5,'normal_solution_direction_repairs':1,'missing_solutions_authored':2,'source_fidelity':fidelity,'generated_review_records':len(review)-8,'generated_templates':8,'generated_levels':['easy','moderate','hard'],'authored_missing_level':'hard: independent reordered row/column headings, same three direct-route entries','sampler_valid_unique_parameters_of_500':variety,'default_radio_correct_sums_in_1000_candidate_draws':authored_sums,'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks']},'concurrency':'3 fresh renders, identical and distinct matrices checked','database_writes':0,'remaining_unresolved_findings':['Original intent behind scalar wrong choices cannot be inferred from finite windows; source catalogs are retained as default and replay banks.','Original difficulty/correct refs/solutions absent for q-138940 and q-139685; assigned easy and derived from independently inspected images.'],'mathematics':'actual displayed ordered table entries, complete arrows and count bullet stages checked; matrices are not scalar products'}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
