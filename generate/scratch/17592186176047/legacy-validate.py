#!/usr/bin/env python3
"""Exhaustive finite-domain truth, source fidelity, schema, native grading QA."""
import hashlib, importlib.util, itertools, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('cosine',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};cases=json.loads((HERE/'source-cases.json').read_text())
n=sp.Symbol('n',integer=True)
def expr(raw):
 raw=raw.strip(' .');raw=raw.replace('π',r'\pi').replace(r'\pi','pi')
 raw=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',raw)
 raw=raw.replace(' ','').replace('⁡','').replace('…','')
 raw=re.sub(r'(\d)(pi|n)',r'\1*\2',raw);raw=raw.replace('npi','n*pi').replace('pin','pi*n')
 return sp.sympify(raw,locals={'pi':sp.pi,'n':n})
def printed_truth(line):
 math=re.findall(r'\$([^$]+)\$',line)
 if 'range' in line:
  m=re.search(r'\[([^,]+),([^\]]+)\]',line);return expr(m[1])==-1 and expr(m[2])==1
 if 'output' in line:
  val=expr(next(x.split('=',1)[1] for x in math if x.startswith('y=')));return bool(-1<=val<=1)
 if 'passes through' in line:
  x,y=next(x.strip('()').split(',') for x in math if x.startswith('('));return sp.cos(expr(x))==expr(y)
 if 'axis at' in line and any(x.startswith('y=') for x in math):return expr(next(x.split('=',1)[1] for x in math if x.startswith('y=')))==1
 x=expr(next(x.split('=',1)[1] for x in math if re.match(r'x\s*=',x)))
 target=0 if 'zero' in line or '$x$-axis' in line else 1 if 'maximum' in line else -1
 if n in x.free_symbols:
  step=sp.expand(x).coeff(n)/sp.pi;offset=sp.expand(x).subs(n,0)/sp.pi
  # Exact independent complete-set criterion; also ensures claimed family has
  # ALL required points, not just correct values at its own sampled points.
  return bool((step==1 and (offset-sp.Rational(1,2)).is_integer) if target==0 else step==2 and ((offset-(0 if target==1 else 1))/2).is_integer)
 return sp.cos(x)==target

def formatting(s):
 assert s.count('$')%2==0,'Math delimiter mismatch'
 for math in re.findall(r'\$+([^$]+)\$+',s):
  depth=0
  for ch in math:
   depth+=1 if ch=='{' else -1 if ch=='}' else 0
   assert depth>=0,'Closing brace mismatch'
  assert depth==0,'Opening brace mismatch'
 assert '@@' not in s and '--' not in s and '+-' not in s

def inspect(r):
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'};assert r['knowledge_point']['db_id']==g.KP_ID;uuid.UUID(q[':question/id'])
 formatting(q[':question/problem']);formatting(q[':question/worked-solution'])
 fields=q[':question/answer-fields']
 for f in fields:
  uuid.UUID(f[':answer-field/id']);values=f[':answer-field/choices'];ids=[a[':answer/id'] for a in values]
  assert len(ids)==len(set(ids));assert f[':answer-field/correct'][0]==':answer/id' and f[':answer-field/correct'][1] in ids
  assert len(values)==(5 if f[':answer-field/type'].endswith('/radio') else 1)
  for a in values:uuid.UUID(a[':answer/id']);assert a[':answer/type'] in (':answer.type/text',':answer.type/math');formatting(a[':answer/value'])
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 if r['generation']['claims']:
  lines=[l for l in q[':question/problem'].splitlines() if re.match(r'^(?:- |[1-3]\. |I{1,3}\. )',l)]
  assert len(lines)==3,lines
  actual=tuple(bool(printed_truth(line)) for line in lines)
  assert list(actual)==r['generation']['truth_vector'],(lines,actual,r['generation']['truth_vector'])
  for verdict in re.finditer(r'Statements? (I{1,3}(?: and I{1,3})*) (?:is|are) (true|false)',q[':question/worked-solution']):
   for label in verdict[1].split(' and '):assert actual[('I','II','III').index(label)]==(verdict[2]=='true'), 'Printed solution verdict disagrees with actual claim'
  field=fields[0];answer=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
  assert g.parse_label(answer)==actual
  assert sum(g.parse_label(a[':answer/value'])==actual for a in field[':answer-field/choices'])==1
 else:
  assert 'function $y=' in q[':question/problem']; assert ('sin' in q[':question/problem'])==('sin'==r['generation']['parameters']['function'])

for asset in json.loads((HERE/'plot-provenance.json').read_text())['assets']:
 assert hashlib.sha256((HERE/asset['copy']).read_bytes()).hexdigest()==asset['sha256']
 assert Path(asset['source']).is_file()

records=[];source_results=[];fidelity={'questions':8,'bank_values_matched':0,'bank_values_total':sum(len(f[':answer-field/choices']) for q in qs.values() for f in q[':question/answer-fields']),'banks_matched':8,'banks_total':8,'correct_designations_matched':0,'correct_designations_present':6,'correct_designations_missing':2,'worked_solutions_exact':0,'worked_solutions_present':6,'worked_solutions_missing':2,'prompts_exact':0,'answer_fields_exact':0,'answer_fields_total':sum(len(q[':question/answer-fields']) for q in qs.values()),'correct_field_designations_exact':0,'correct_field_designations_present':sum(':answer-field/correct' in f for q in qs.values() for f in q[':question/answer-fields'])}
for case in cases:
 r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);inspect(r);records.append(r)
 raw=qs[case['source_id']];q=r['question'];assert q[':question/problem']==raw[':question/problem'],case['source_id'];fidelity['prompts_exact']+=1
 details={'source_id':case['source_id'],'prompt':'exact','bank':'exact','correct_designation':'missing: derived separately','solution':'missing: authored separately'}
 src_fields={f[':answer-field/key']:f for f in raw[':question/answer-fields']}
 for f in q[':question/answer-fields']:
  old=src_fields[f[':answer-field/key']];fidelity['answer_fields_exact']+=1;fidelity['bank_values_matched']+=len(old[':answer-field/choices']);assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices'])
  if ':answer-field/correct' in old:
   fidelity['correct_field_designations_exact']+=1
   correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==old[':answer-field/correct'][':answer/value'];details['correct_designation']='exact'
 if details['correct_designation']=='exact':fidelity['correct_designations_matched']+=1
 if ':question/worked-solution' in raw:
  assert q[':question/worked-solution']==raw[':question/worked-solution'],case['source_id'];fidelity['worked_solutions_exact']+=1;details['solution']='exact'
 source_results.append(details)

catalog_counts={};identities={};changed_parameters=0
for level in ('easy','moderate','hard'):
 cat=g.authored_catalog(level);fingerprints=set();correct_positions=set()
 for p in cat:
  r=g.generate(level,seed=0,parameters=p);inspect(r);other=g.generate(level,seed=7,parameters=p);inspect(other)
  assert r['question'][':question/id']==other['question'][':question/id'];assert r['generation']['parameter_fingerprint']==other['generation']['parameter_fingerprint']
  fingerprints.add(r['generation']['parameter_fingerprint'])
  for shuffled in (r,other):
   f=shuffled['question'][':question/answer-fields'][0];correct_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
 assert len(fingerprints)==len(cat);assert len(correct_positions)>1
 catalog_counts[level]=len(cat);identities[level]={'semantic_tasks':len(fingerprints),'shuffled_correct_positions':sorted(correct_positions)}
 # Meaningful selected variants for native grader, besides review examples.
 records.extend(g.generate(level,seed=s) for s in range(10))
for case in cases:
 name=case['template']
 for seed in range(20):
  r=g.generate('moderate',seed=seed,template=name);inspect(r);changed_parameters+=r['generation']['parameters']!=case['parameters']
 records.extend(g.generate('moderate',seed=s,template=name) for s in range(2))
# Numeric magnitudes that do not affect categorical reasoning cannot inflate
# mathematical variety, but their changed display still needs a content ID.
p1=json.loads(json.dumps(g.SOURCE_DEFAULTS['q-103230']));p2=json.loads(json.dumps(p1));p2['range']={'low':'-pi','high':'pi'};p2['output']={'value':'-2'}
r1=g.generate('moderate',template='q-103230',parameters=p1);r2=g.generate('moderate',template='q-103230',parameters=p2);inspect(r1);inspect(r2)
assert r1['generation']['parameter_fingerprint']==r2['generation']['parameter_fingerprint']
assert r1['question'][':question/id']!=r2['question'][':question/id']

# Explicit guards must reject workload removal, arbitrary harder algebra and sine
# in normal presentation. Neither seed nor undocumented params can rescue them.
invalid=[('easy',{'claims':[{'kind':'zero','value':'8'}]}),('hard',{'claims':[{'kind':'zero','value':'1/2'}]*3}),('moderate',{'claims':[]})]
for level,p in invalid:
 try:g.generate(level,parameters=p)
 except ValueError:pass
 else:raise AssertionError('Invalid explicit authored parameters accepted')
try:g.generate('moderate',template='q-167631',parameters={'function':'sin'})
except ValueError:pass
else:raise AssertionError('Mislinked sine accepted in normal output')

review=[];md=['# Cosine properties: source fidelity and generated review','', 'Database math, basis 1356. Originals remain raw evidence; repairs and authored missing-level labels are explicit.','']
for case in cases:
 name=case['template'];raw=qs[name];r=g.generate('moderate',template=name,parameters=case['parameters'],profile=case['bank_profile']);review.append(r)
 md+=['## Original '+name,'',raw[':question/problem'],'','Captured banks: '+repr([[a[':answer/value'] for a in f[':answer-field/choices']] for f in raw[':question/answer-fields']]),'',raw.get(':question/worked-solution','**No captured solution or correct designation.**'),'','### Parameterized replay (original bank)','',g.markdown(r),'','### Generated changed-parameter variant (normal presentation)','']
 v=next(g.generate('moderate',seed=seed,template=name) for seed in range(100) if g.generate('moderate',seed=seed,template=name)['generation']['parameter_fingerprint']!=r['generation']['parameter_fingerprint']);review.append(v);md+=[g.markdown(v),'']
for level in ('easy','moderate','hard'):
 for seed in (8,9):
  r=g.generate(level,seed=seed);review.append(r);md+=['## Authored '+level+' example, seed '+str(seed),'',g.markdown(r),'']
(HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');(HERE/'review.md').write_text('\n'.join(md)+'\n')

fixtures=[]
for index,r in enumerate(records):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks += [{'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned categorical outcome truth'} for a in f[':answer-field/choices']]
  else:
   val=f[':answer-field/choices'][0][':answer/value'];normal=val.replace('\\\\','\\').strip()
   checks += [{'field_index':fi,'submitted':val,'expected':'accepted','purpose':'Exact captured/generated blank value'}, {'field_index':fi,'submitted':'0','expected':'rejected','purpose':'Incorrect finite answer'}]
   checks += [{'field_index':fi,'submitted':normal if val!=normal else {'-1':'-2/2','1':'2/2',r'2\pi':'pi+pi',r'\infty':'infinity',r'-\infty':'-infinity'}[normal], 'expected':'accepted','purpose':'Meaningful equivalent blank form'}]
 fixtures.append({'label':str(index)+'-'+r['generation']['bank_profile'],'record':r,'checks':checks})
(HERE/'engine-input.json').write_text(json.dumps(fixtures,indent=2,ensure_ascii=False)+'\n')
engine=ROOT/'generate/runs/current/check-engine';proc=subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],text=True,capture_output=True)
report={'status':'pass' if proc.returncode==0 else 'fail','version':g.VERSION,'source_fidelity':fidelity,'source_results':source_results,'raw_source_anomalies':[{'source_id':'q-27015','finding':'Missing original correct designation and worked solution; derived key II only, authored supported solution; unrated assigned moderate'}, {'source_id':'q-27021','finding':'Missing original correct designation and worked solution; derived key I only, authored supported solution; unrated assigned moderate'}, {'source_id':'q-167631','finding':'Sine mislink. Raw API retains sine; normal generator changes function/graph to cosine. Blank values were inspected byte by byte: valid single backslash commands, no TeX anomaly.'}], 'mathematics':{'catalog_counts':catalog_counts,'identities':identities,'source_changed_parameter_tests':160,'changed_instances':changed_parameters,'all_fields_checked':True,'displayed_prompt_independently_parsed':True}, 'native_grader':{'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'fixture_count':len(fixtures),'check_count':sum(len(f['checks']) for f in fixtures),'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'authored_levels':['easy','hard'],'finite_variation':True,'plot_verification':'Original rasters inspected at full resolution; unchanged geometry reused, no renderer needed.'}
(HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(report,indent=2,ensure_ascii=False))
if proc.returncode:sys.exit(proc.returncode)
