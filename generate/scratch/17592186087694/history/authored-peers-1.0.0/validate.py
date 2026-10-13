#!/usr/bin/env python3
"""Independent prompt-array, ordered answer, source, identity and native checks."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('generator',P.with_suffix('.py')); G=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(G)
ROOT=P.parents[2]
def write(name,x): (P/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def pair(s):
 m=re.fullmatch(r'(\d+)\s*\\(?:times|cdot)\s*(\d+)',s); assert m,s
 return int(m[1]),int(m[2])
def actual_array(problem):
 m=re.search(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',problem)
 if m: return [row.strip().split('&') for row in m[1].split(r'\\')]
 m=re.search(r'= \[([^\]]+)\]',problem); assert m,problem
 return [[m[1]]]
def structural(record):
 assert set(record)=={'knowledge_point','question','generation'}
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 q=record['question']; a=actual_array(q[':question/problem']); r,c=len(a),len(a[0])
 assert all(len(row)==c for row in a) and min(r,c)==1 and max(r,c)<=5
 # Verify actual printed scalar entries independently of metadata.
 for row in a:
  for entry in row: assert G.entry_value(entry.strip()).is_real
 sol=q[':question/worked-solution']
 counts=re.search(r'has \$(\d+)\$ rows?\s+and \$(\d+)\$ columns?',sol)
 assert counts and (int(counts[1]),int(counts[2]))==(r,c)
 final=re.search(r'dimensions are\s+\$(\d+)\\times (\d+)\.\$',sol)
 assert final and (int(final[1]),int(final[2]))==(r,c)
 for text in [q[':question/problem'],sol]+[ans[':answer/value'] for f in q[':question/answer-fields'] for ans in f[':answer-field/choices']]:
  assert text.count('$')%2==0
  depth=0
  for ch in text:
   if ch=='{':depth+=1
   if ch=='}':depth-=1
   assert depth>=0
  assert depth==0
 ids=[]
 for f in q[':question/answer-fields']:
  assert f[':answer-field/correct'][0]==':answer/id'
  choices=f[':answer-field/choices']; ids.extend(x[':answer/id'] for x in choices)
  correct=next(x for x in choices if x[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type'].endswith('/radio'):
   pairs=[pair(x[':answer/value']) for x in choices]
   assert len(pairs)==len(set(pairs))==5 and pairs.count((r,c))==1 and pair(correct[':answer/value'])==(r,c)
  else:
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
   expected=r if f[':answer-field/key']=='field-1' else c
   assert len(choices)==1 and int(correct[':answer/value'])==expected
 assert len(ids)==len(set(ids))
 return r,c

def checks(record):
 result=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   for x in f[':answer-field/choices']:
    result.append({'field_index':i,'submitted_answer_id':x[':answer/id'],'expected':'accepted' if x[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual owned choice grading; ordered-dimension semantics checked independently'})
  else:
   v=f[':answer-field/choices'][0][':answer/value']
   for submitted,expected in [(v,'accepted'),(v+'+0','accepted'),(str(int(v)+1),'rejected')]:
    result.append({'field_index':i,'submitted':submitted,'expected':expected,'purpose':'Canonical, unevaluated equivalent or wrong scalar count'})
 return result

def main():
 source=json.loads((P/'source.json').read_text())['record'][':knowledge-point/questions']; cases=json.loads((P/'source-cases.json').read_text()); by={q[':question/math-academy-id']:q for q in source}
 bank_count=choice_count=distractors=correct_refs=prompt_count=solution_count=field_count=0
 native=[]; review=[]; source_reports=[]
 for case in cases:
  original=by[case['source_id']]
  record=G.generate(case['level'],17,case['template'],parameters=case['parameters'],profile=case['bank_profile']); structural(record)
  q=record['question']; assert q[':question/problem']==original[':question/problem']; prompt_count+=1
  if ':question/worked-solution' in original:
   assert q[':question/worked-solution']==original[':question/worked-solution']; solution_count+=1
  source_fields=original[':question/answer-fields']; generated_fields=q[':question/answer-fields']
  assert [f[':answer-field/key'] for f in source_fields]==[f[':answer-field/key'] for f in generated_fields]
  for orig,gen in zip(source_fields,generated_fields):
   assert orig[':answer-field/type'][':db/ident']==gen[':answer-field/type']; field_count+=1
   original_values=sorted(x[':answer/value'] for x in orig[':answer-field/choices']); generated_values=sorted(x[':answer/value'] for x in gen[':answer-field/choices']); assert original_values==generated_values
   choice_count+=len(original_values)
   if gen[':answer-field/type'].endswith('/radio'): bank_count+=1; distractors+=len(original_values)-1
   if ':answer-field/correct' in orig:
    actual=next(a[':answer/value'] for a in gen[':answer-field/choices'] if a[':answer/id']==gen[':answer-field/correct'][1]); assert actual==orig[':answer-field/correct'][':answer/value']; correct_refs+=1
  source_reports.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact':':question/worked-solution' in original,'source_correct_designation_present':all(':answer-field/correct' in f for f in source_fields),'bank_values_exact':True})
  native.append({'label':case['source_id'],'record':record,'checks':checks(record)}); review.append({'label':'Source replay '+case['source_id'],'record':record})
  # Genuine changed-object variants for every source profile.
  variant=G.generate(case['level'],43,case['template'],profile=case['bank_profile']); structural(variant); review.append({'label':'Generated variant of '+case['source_id'],'record':variant}); native.append({'label':'variant '+case['source_id'],'record':variant,'checks':checks(variant)})
 shape_coverage={}; positions=set()
 for level in ('easy','moderate','hard'):
  shapes=set()
  for seed in range(150):
   record=G.generate(level,seed); shapes.add(structural(record)); native.append({'label':level+'-'+str(seed),'record':record,'checks':checks(record)})
   if seed<4: review.append({'label':'Generated '+level+' peer' if level!='easy' else 'Generated easy','record':record})
   gen=record['generation']; replay=G.generate(level,seed+1000,gen['template'],parameters=gen['parameters'],profile=gen['bank_profile'])
   assert record['question'][':question/id']==replay['question'][':question/id'] and gen['content_fingerprint']==replay['generation']['content_fingerprint']
   for f in record['question'][':question/answer-fields']:
    if f[':answer-field/type'].endswith('/radio'): positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
  assert shapes==set(G.SHAPES); shape_coverage[level]=sorted(shapes)
 assert positions==set(range(5))
 # All profiles exercise parameterized replay beyond the source numbers.
 for prof,(template,_) in G.PROFILES.items():
  for seed in range(25): structural(G.generate('easy',seed,template,profile=prof))
 # Scope and explicit-input constraints must fail, not silently repair.
 for entries in [[['1','2'],['3','4']],[['1']]*6,[['1'],['2','3']],[['x']],[]]:
  for level in ('easy','moderate','hard'):
   try:G.generate(level,parameters={'name':'A','entries':entries});raise AssertionError('Invalid parameters accepted')
   except ValueError:pass
 # Incidental entries are content identity, not distinct assessed dimension tasks.
 a=G.generate('easy',template='aligned_radio',parameters={'name':'A','entries':[['1','2']]}); b=G.generate('easy',template='aligned_radio',parameters={'name':'A','entries':[['3','4']]})
 assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id']
 c=G.generate('easy',template='aligned_radio',parameters={'name':'A','entries':[['1'],['2']]})
 assert c['generation']['parameter_fingerprint']!=a['generation']['parameter_fingerprint']
 write('review.json',review); originals='\n\n'.join('## Original '+x[':question/math-academy-id']+'\n\n'+x[':question/problem']+'\n\n'+'\n'.join('- '+f[':answer-field/key']+': $'+a[':answer/value']+'$' for f in x[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\nWorked solution: '+x.get(':question/worked-solution','[Absent in capture; authored replay solution is labeled below.]') for x in source)
 (P/'review.md').write_text('# Original evidence and generated peers\n\nModerate/hard are authored peers, with no recovered harder skill claim.\n\n'+originals+'\n\n---\n\n'+ '\n\n---\n\n'.join('## '+x['label']+'\n\n'+G.markdown(x['record']) for x in review))
 write('engine-input.json',native)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(P/'engine-input.json'),str(P/'engine-report.json')],check=True)
 engine=json.loads((P/'engine-report.json').read_text())
 assert engine['documented_unresolved_checks']==0
 results={'passed':True,'database_writes':0,'source_coverage':{'questions':len(source),'replayed':len(cases),'exact_prompts':prompt_count,'exact_existing_solutions':solution_count,'existing_solution_total':sum(':question/worked-solution' in x for x in source),'exact_field_layouts':field_count,'exact_answer_values':choice_count,'complete_radio_banks':bank_count,'matched_radio_distractors':distractors,'matched_existing_correct_designations':correct_refs,'existing_correct_designation_total':sum(':answer-field/correct' in f for x in source for f in x[':question/answer-fields']),'missing_correct_designations_derived':2,'missing_solutions_authored':2,'unrated_levels_authored_easy':2},'source_reports':source_reports,'generated_instances_checked':450,'all_profiles_extra_samples':200,'shape_coverage':shape_coverage,'meaningful_shapes_per_level':9,'math_fingerprint_excludes_entries_and_labels':True,'content_identity_includes_entries_and_complete_bank':True,'native_grading':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','entry_point')},'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'unresolved_findings':[]}
 write('validation.json',results)
 print(json.dumps(results['source_coverage'],indent=2)); print('Validation PASS')
if __name__=='__main__':main()
