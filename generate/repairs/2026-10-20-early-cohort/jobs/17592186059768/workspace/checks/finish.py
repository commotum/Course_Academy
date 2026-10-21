"""Prepare read-only grading, delivery and render inputs; test affected inventory.
Runtime files are never modified. Run after checks/regression.py.
"""
import sys
sys.dont_write_bytecode=True
import copy,json,pathlib,re,subprocess,platform,shutil,collections
from regression import *
REPO=pathlib.Path('/home/jake/Developer/Course_Academy');JOB=W.parent

def inventory():
 sys.path.insert(0,str(REPO))
 from scripts.generator_publish import normalized_question
 inv=json.loads((JOB/'source/inventory.json').read_text());stored={q[':question/id']:q for q in inv['questions']}
 archive=json.loads((W/'17592186059768/reference/replenishment/basis-2204/generated.json').read_text())
 reproduced=[];affected=[]
 for old in archive:
  meta=old['generation'];name=meta['template'];params=meta['parameters'];src=g.PROFILES[name]
  r=copy.deepcopy(old);q=r['question']
  # Reconstruct prose and complete bank from source, not the inventory's expected content.
  for k in (':question/problem',':question/worked-solution'):
   q[k]=re.sub(r'\d+',lambda m:str(params.get(m[0],int(m[0]))),src[k])
  f=field(r);oldmap={a[':answer/value']:a[':answer/id'] for a in field(old)[':answer-field/choices']}
  values=[g.normalize_tex(g.render(a[':answer/value'],params)) for a in src[':question/answer-fields'][0][':answer-field/choices']]
  f[':answer-field/choices']=[{':answer/id':oldmap[v],':answer/type':':answer.type/math',':answer/value':v} for v in values]
  correct=g.normalize_tex(g.render(src[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],params));f[':answer-field/correct']=[':answer/id',oldmap[correct]]
  actual=stored[q[':question/id']];assert normalized_question(q)==normalized_question(actual);check(r)
  target=mask(matrix(src[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],True)[0]);matches=[i for i,m in enumerate(bank(r)) if mask(m)==target]
  assert len(matches)==1 and field(r)[':answer-field/choices'][matches[0]][':answer/id']==key(r)
  reproduced.append(r);affected.append({'question_id':q[':question/id'],'entity_id':actual[':db/id'],'finding':'Memorized source sign mask uniquely selects the correct matrix; '+('sole negative bottom-right entry also selects it' if negative_corner(r) else 'fixed within-template sign topology'),'reproduction':str(REPO/'.venv/bin/python')+' -B checks/finish.py','evidence_path':'generated-records.json'})
 generated_ids={r['question'][':question/id'] for r in archive};unreproduced=[q[':question/id'] for q in inv['questions'] if ':question/math-academy-id' not in q and q[':question/id'] not in generated_ids]
 assert not unreproduced
 save('generated-records.json',reproduced);save('affected-inventory.json',{'affected_questions':affected});save('inventory-results.json',{'basis':inv['basis'],'exact_complete_reproductions':len(reproduced),'tested_generated':len(generated_ids),'unreproduced_generated_ids':unreproduced,'original_assessed_sources_excluded':len(inv['questions'])-len(generated_ids),'generation_metadata':'Exact archived metadata; source-driven reconstruction compared with publisher normalized_question including identities; no database writes'})
 return reproduced

def extra_probes(records):
 groups=collections.defaultdict(list)
 for r in records:groups[r['generation']['template']].append(r)
 out={}
 for name,rs in groups.items():
  results=collections.Counter()
  for r in rs:
   bs=bank(r);target=next(i for i,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==key(r))
   for strategy,fun in [('sum',lambda m:sum(sum(row) for row in m)),('negative_count',lambda m:sum(v<0 for row in m for v in row)),('zero_count',lambda m:sum(v==0 for row in m for v in row)),('corner',lambda m:m[-1][-1]),('first_entry',lambda m:m[0][0]),('first_row_sum',lambda m:sum(m[0])),('diagonal_sum',lambda m:sum(row[i] for i,row in enumerate(m))),('lexicographic',lambda m:tuple(v for row in m for v in row)),('unit_count',lambda m:sum(abs(v)==1 for row in m for v in row))]:
    vals=[fun(m) for m in bs]
    for direction,op in [('min',min),('max',max)]:
     good=[i for i,v in enumerate(vals) if v==op(vals)]
     results[strategy+'_'+direction]+=len(good)==1 and good[0]==target
   # Every sampled choice has precisely the same signed-entry multiset.
   assert len({tuple(sorted(v for row in m for v in row)) for m in bs})==1
  assert all(n<len(rs) for n in results.values())
  out[name]={'count':len(rs),'unique_extreme_correct':dict(results),'equal_signed_multiset_banks':len(rs)}
 return out

def main():
 historical=inventory();records=json.loads((E/'records.json').read_text());replays=json.loads((E/'source-replays.json').read_text());controls=json.loads((E/'counterfactual-records.json').read_text());batch=json.loads((E/'batch.json').read_text())
 for r in batch:check(r)
 save('surface-probes.json',extra_probes(records))
 allrecords=replays+records+controls+batch+historical
 cases=[]
 for i,r in enumerate(allrecords):
  check(r);cases.append({'label':str(i)+'-'+r['generation']['template'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(r) else 'rejected','purpose':'Independent visible-equation derivation, every radio option'} for a in field(r)[':answer-field/choices']]})
 save('grader-input.json',cases)
 for level in ('easy','moderate'):
  save(level+'.json',[r for r in records if r['question'][':question/difficulty'].endswith('/'+level)])
 # One new example per affected profile, old exact failure and signed counterfactual.
 preview=[next(r for r in records if r['generation']['template']==p) for p in g.PROFILES]+controls[-2:]
 save('render-input.json',preview)
 save('runtime.json',{'python':platform.python_version(),'dependencies':json.loads((W/'package.json').read_text())['dependencies'],'runtime_files':json.loads((W/'package.json').read_text())['files']})
 print(json.dumps({'inventory_reproduced':len(historical),'grader_records':len(cases),'grader_checks':5*len(cases),'render_records':len(preview)}))
if __name__=='__main__':main()
