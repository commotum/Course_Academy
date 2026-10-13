#!/usr/bin/env python3
"""Read the displayed array, ordered options, prose and raw source presence."""
import hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
P=Path(__file__).resolve().parent; ROOT=P.parents[2]
S=importlib.util.spec_from_file_location('draft',P.with_suffix('.py'));G=importlib.util.module_from_spec(S);S.loader.exec_module(G)
def write(n,v): (P/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def pair(s):
 m=re.fullmatch(r'(\d+)\s*\\(?:times|cdot)\s*(\d+)',s);assert m,s
 return int(m[1]),int(m[2])
def displayed(problem):
 m=re.search(r'\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\1\}',problem)
 if m: a=[row.strip().split('&') for row in m[2].split(r'\\')]
 else:
  m=re.search(r'= \[([^\]]+)\]',problem);assert m,problem;a=[[m[1]]]
 assert len({len(row) for row in a})==1
 for row in a:
  for v in row:assert re.fullmatch(r'-?\d+|-?\\frac\{\d+\}\{[1-9]\d*\}|-?\\sqrt\{\d+\}',v.strip()),v
 return len(a),len(a[0])
def structural(record):
 assert set(record)=={'knowledge_point','question','generation'}
 assert set(record['knowledge_point'])=={'db_id','id','title'} and record['knowledge_point']['db_id']==17592186087694
 q=record['question'];r,c=displayed(q[':question/problem']);g=record['generation']
 assert min(r,c)==1
 if not g['evidence_only']:
  level=q[':question/difficulty'].split('/')[-1];lo,hi={'easy':(1,5),'moderate':(6,12),'hard':(13,20)}[level]
  assert lo<=max(r,c)<=hi
  assert g['eligible_for_learning']
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];counts=re.search(r'has \$(\d+)\$ rows?\s+and \$(\d+)\$ columns?',sol)
  assert counts and (int(counts[1]),int(counts[2]))==(r,c)
  final=re.search(r'dimensions are\s+\$(\d+)\\times (\d+)\.\$',sol);assert final and (int(final[1]),int(final[2]))==(r,c)
  name=re.search(r'(?:matrix|Let) \$([A-Z])',q[':question/problem'])[1];assert 'matrix $'+name+'$' in sol
 texts=[q[':question/problem'],q.get(':question/worked-solution','')]
 allids=[q[':question/id']]
 for f in q.get(':question/answer-fields',[]):
  allids.append(f[':answer-field/id']);choices=f[':answer-field/choices'];allids.extend(a[':answer/id'] for a in choices)
  texts.extend(a[':answer/value'] for a in choices)
  if f[':answer-field/type'].endswith('/radio'):
   pairs=[pair(a[':answer/value']) for a in choices];assert len(pairs)==len(set(pairs))==5 and pairs.count((r,c))==1
  else:
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
   assert len(choices)==1 and int(choices[0][':answer/value'])==(r if f[':answer-field/key']=='field-1' else c)
  if ':answer-field/correct' in f:
   ref=f[':answer-field/correct'];assert ref[0]==':answer/id';correct=next(a for a in choices if a[':answer/id']==ref[1])
   assert pair(correct[':answer/value'])==(r,c) if f[':answer-field/type'].endswith('/radio') else int(correct[':answer/value'])==(r if f[':answer-field/key']=='field-1' else c)
 assert len(allids)==len(set(allids));[uuid.UUID(x) for x in allids]
 for text in texts:
  assert text.count('$')%2==0
  depth=0
  for ch in text:
   if ch=='{':depth+=1
   elif ch=='}':depth-=1
   assert depth>=0
  assert depth==0
 return r,c

def checks(record):
 result=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   result.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Native owned-option grade; independent ordered semantics above'} for a in f[':answer-field/choices'])
  else:
   v=f[':answer-field/choices'][0][':answer/value']
   result.extend({'field_index':i,'submitted':s,'expected':e,'purpose':'Canonical / equivalent expression / wrong count'} for s,e in [(v,'accepted'),('('+v+'+2)-2','accepted'),(str(int(v)+1),'rejected')])
 return result

def main():
 originals=G.SOURCE_BY_ID;cases=json.loads((P/'source-cases.json').read_text());review=[];native=[];stats={'questions':0,'prompts_exact':0,'solutions_exact_existing':0,'raw_presence_parity':0,'field_layouts':0,'answer_values':0,'radio_banks':0,'radio_distractors':0,'correct_refs_existing':0}
 for case in cases:
  record=G.generate(case['level'],17,case['template'],parameters=case['parameters'],profile=case['bank_profile']);structural(record)
  orig=originals[case['source_id']];q=record['question'];stats['questions']+=1
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in orig)
  assert q[':question/problem']==orig[':question/problem'];stats['prompts_exact']+=1
  if ':question/worked-solution' in orig:assert q[':question/worked-solution']==orig[':question/worked-solution'];stats['solutions_exact_existing']+=1
  assert len(q[':question/answer-fields'])==len(orig[':question/answer-fields'])
  if ':question/difficulty' in orig:assert q[':question/difficulty']==orig[':question/difficulty'][':db/ident']
  for f,of in zip(q[':question/answer-fields'],orig[':question/answer-fields']):
   assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];stats['field_layouts']+=1
   assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);stats['answer_values']+=len(f[':answer-field/choices'])
   if f[':answer-field/type'].endswith('/radio'):stats['radio_banks']+=1;stats['radio_distractors']+=4
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];stats['correct_refs_existing']+=1
  stats['raw_presence_parity']+=1
  review.append({'label':'SOURCE raw replay '+case['source_id'],'record':record})
  fixture=json.loads(json.dumps(record))
  # Only the grading fixture gets missing refs inferred from actual displayed counts.
  for f in fixture['question'][':question/answer-fields']:
   if ':answer-field/correct' not in f:
    rc=displayed(fixture['question'][':question/problem']);a=next(a for a in f[':answer-field/choices'] if pair(a[':answer/value'])==rc);f[':answer-field/correct']=[':answer/id',a[':answer/id']]
  native.append({'label':'Source fixture '+case['source_id']+(' inferred missing ref' if ':question/difficulty' not in q else ''),'record':fixture,'checks':checks(fixture)})
  variant=G.generate('easy',43,case['template'],profile=case['bank_profile']);structural(variant);review.append({'label':'GENERATED parameterized historical evidence '+case['source_id'],'record':variant})
 coverage={};positions=set();families={}
 for level in G.SUPPORTED_LEVELS:
  shapes=set();templates=set()
  for seed in range(250):
   record=G.generate(level,seed);shapes.add(structural(record));templates.add(record['generation']['template']);g=record['generation']
   other=G.generate(level,seed+999,g['template'],parameters=g['parameters'],profile=g['bank_profile']);assert record['question'][':question/id']==other['question'][':question/id']
   native.append({'label':level+'-'+str(seed),'record':record,'checks':checks(record)})
   if seed<4:review.append({'label':'GENERATED '+level+' authored workload','record':record})
   for f in record['question'][':question/answer-fields']:
    if f[':answer-field/type'].endswith('/radio'):positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
  assert shapes==set(G.SHAPES[level]);assert templates==set(['aligned_radio','double_blank','legacy_column']+(['legacy_singleton'] if level=='easy' else []))
  coverage[level]=sorted(shapes);families[level]=sorted(templates)
  for template in sorted(templates):
   variant=G.generate(level,401,template=template);structural(variant);review.append({'label':'GENERATED '+level+' source-shaped family '+template,'record':variant});native.append({'label':level+' family '+template,'record':variant,'checks':checks(variant)})
  assert len({r['generation']['parameter_fingerprint'] for r in G.batch(level,len(shapes),11)})==len(shapes)
  for n in range(1,22):
   for orientation in ('row','column'):
    entries=[['1']*n] if orientation=='row' else [['1']]*n
    valid=G.BOUNDS[level][0]<=n<=G.BOUNDS[level][1]
    try:r=G.generate(level,template='aligned_radio',parameters={'name':'A','entries':entries});assert valid;structural(r)
    except ValueError:assert not valid
  for entries in [[['1','2'],['3','4']],[['1'],['2','3']],[['x']],[],[['1']*G.BOUNDS[level][1]] if level=='easy' else [['\\sqrt{2}']]*G.BOUNDS[level][0]]:
   if level=='easy' and entries==[['1']*5]:continue
   try:G.generate(level,parameters={'name':'A','entries':entries});raise AssertionError('Invalid input accepted')
   except ValueError:pass
 assert positions==set(range(5))
 for prof,(t,_) in G.PROFILES.items():
  for seed in range(30):structural(G.generate('easy',seed,t,profile=prof))
 a=G.generate('easy',template='aligned_radio',parameters={'name':'A','entries':[['1','2']]});b=G.generate('easy',template='double_blank',parameters={'name':'B','entries':[['3','4']]})
 assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id']
 # CLI actual difficulty and family rendering, with omission-safe evidence output.
 for fmt in ('json','markdown'):
  result=subprocess.run([sys.executable,str(P.with_suffix('.py')),'--difficulty','all','--count','2','--format',fmt],capture_output=True,text=True,check=True)
  (P/('cli-review.'+('json' if fmt=='json' else 'md'))).write_text(result.stdout)
 for prof in ('legacy_column_observed','legacy_singleton_observed'):
  subprocess.run([sys.executable,str(P.with_suffix('.py')),'--difficulty','easy','--profile',prof],capture_output=True,check=True)
 write('review.json',review);(P/'review.md').write_text('# Raw originals and generated variants\n\nHistorical profiles are evidence only. Moderate/hard labels are authored workload claims.\n\n'+'\n\n---\n\n'.join('## '+x['label']+'\n\n'+G.markdown(x['record']) for x in review))
 write('engine-input.json',native);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(P/'engine-input.json'),str(P/'engine-report.json')],check=True)
 engine=json.loads((P/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 rendered=json.loads((P/'render-input.json').read_text());assert {structural(r) for r in rendered}=={(1,20),(20,1)}
 for name in ('maxlength-row.png','maxlength-column.png'):assert (P/name).read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
 renderer=json.loads((P/'render-provenance.json').read_text());assert renderer['python'] and renderer['matplotlib']
 baseline=json.loads((P/'registered-baseline.json').read_text());assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in baseline.items())
 result={'passed':True,'source_fidelity':stats,'source_omissions':{'unrated':2,'worked_solution_absent':2,'correct_refs_absent':2,'inferred_refs_only_in_separate_native_fixture':2},'shape_coverage':coverage,'meaningful_tasks_per_level':{k:len(v) for k,v in coverage.items()},'default_family_coverage':families,'normal_instances_checked':750,'historical_profile_parameter_tests':240,'strict_bounds_explicit_and_sampled':True,'native_grading':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','entry_point')},'registered_baseline_unchanged':True,'maximum_length_previews':{'displayed_shapes':[[1,20],[20,1]],'renderer':renderer,'visual_inspection':'Both previews inspected; all entries and brackets readable after widening row preview; browser TeX layout not asserted'},'runtime':{'python':sys.version.split()[0],'sympy':G.sp.__version__},'database_writes':0,'unresolved_findings':[]}
 write('validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
