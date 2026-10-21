"""Retained reviewer unit-slope witness and conditional visible-bank probes.
No services, runtime writes, or database access. Evidence lives in the workspace.
"""
import collections,json,re,sys
sys.dont_write_bytecode=True
from validate_repair import g,E,dump,check,summarize
from witness import field,correct,system,vec,v,sp

def probe(r):
 candidates=[];cs=field(r)[':answer-field/choices']
 for i,c in enumerate(cs):
  value=c[':answer/value'];value=value.replace('\\\\','\\') if r'\\begin' in value else value
  match=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',value,re.S)
  if not match:continue
  rows=[x.strip() for x in match[1].split(r'\\')]
  if len(rows)==2 and rows[1]=='y' and re.search(r'(?<![0-9A-Za-z}])y(?![A-Za-z])',rows[0]):candidates.append(i)
 chosen=cs[candidates[0]][':answer/id'] if len(candidates)==1 else None
 return {'candidate_positions':[i+1 for i in candidates],'applicable':len(candidates)==1,'shortcut_correct':chosen==correct(r),'baseline':0.2}

def inspect(records):
 groups=collections.defaultdict(list);counts=collections.Counter();unit_probes=[];magnitude=collections.defaultdict(lambda:[0,0])
 for r in records:
  check(r);p=probe(r);unit_probes.append(p)
  assert not p['shortcut_correct'],(r['generation']['seed'],p)
  counts['applicable']+=p['applicable'];counts['successes']+=p['shortcut_correct']
  M=system(r['question'][':question/problem']);_,piv=M.rref();fc=next(j for j in range(M.cols-1) if j not in piv)
  cs=field(r)[':answer-field/choices'];xs=[vec(c[':answer/value']) for c in cs];key=next(i for i,c in enumerate(cs) if c[':answer/id']==correct(r))
  # Coefficient typography must not single out a supplied key coordinate.
  if r['generation']['bank_profile']!='authored_operations':
   for j in piv:
    a=sp.diff(xs[key][j],v[fc]);c=xs[key][j].subs(v[fc],0)
    if a!=0 and c!=0:assert all(sp.diff(x[j],v[fc])==a for x in xs)
    if abs(a)==1:assert sum(abs(sp.diff(x[j],v[fc]))==1 for x in xs)>=2
  # A profile name may conceal several mathematical structures; group by visible
  # equation size, free column, and zero/constant coordinate assignments as well.
  shape=(M.rows,M.cols,fc,tuple(j for j in piv if not xs[key][j].has(v[fc])),tuple(j for j in piv if xs[key][j].subs(v[fc],0)==0))
  groups[(r['generation']['template'],str(shape))].append(r)
  for name,scores in [('absolute_intercept',[abs(x[0].subs(v[fc],0)) for x in xs]),('absolute_slope',[abs(sp.diff(x[0],v[fc])) for x in xs])]:
   for side,extreme in [('min',min(scores)),('max',max(scores))]:
    indices=[i for i,value in enumerate(scores) if value==extreme]
    if len(indices)==1:
     tally=magnitude[(r['generation']['template'],str(shape),name+'_'+side)];tally[0]+=1;tally[1]+=indices[0]==key
 out={}
 for (template,shape),rs in groups.items():
  summary=summarize(rs)[template]
  for cue,(attempts,hits) in summary['probes'].items():
   assert not(attempts>=4 and attempts==hits),(template,shape,cue,attempts,hits)
  out[template+' / '+shape]=summary
 for cue,(attempts,hits) in magnitude.items():
  assert not(attempts>=4 and attempts==hits),(cue,attempts,hits)
 return {'absolute_magnitude_probes':{str(k):value for k,value in magnitude.items()},'records':len(records),'unit_strategy':dict(counts),'unit_probes':unit_probes,'within_template_probes':out,'limits':'These finite probes test specified typography, slope/intercept extrema, term counts, sign counts, positions and component frequencies; they do not prove absence of every possible shortcut.'}

def main():
 if len(sys.argv)>1:
  raw=json.load(open(E/'unit-records.json'));accepted=json.load(open(sys.argv[1]))
  before=inspect(raw);after=inspect(accepted)
  signature=lambda r:(str(system(r['question'][':question/problem'])),tuple(sorted(str(vec(c[':answer/value'])) for c in field(r)[':answer-field/choices'])),str(next(vec(c[':answer/value']) for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r))))
  assert {signature(r) for r in raw}=={signature(r) for r in accepted}
  dump('unit-delivery-results.json',{'before':before,'after':after,'same_semantic_instances':True})
  print(json.dumps({'raw':len(raw),'accepted':len(accepted),'successful_unit_shortcuts':0}));return
 exact=g.generate_easy(seed=71383,profile='q-32244')
 assert system(exact['question'][':question/problem'])==sp.Matrix([[2,2,-9],[-10,-10,45],[8,8,-36]])
 assert len(probe(exact)['candidate_positions'])==5
 records=[g.generate_easy(seed=seed,profile='q-32244') for seed in range(71381,71401)]
 # Other profiles already occur in the retained rational-support sample.
 records.extend(g.generate_easy(seed=seed,profile=profile) for profile in sorted(g.QUESTIONS) if profile!='q-32244' for seed in (71381,71382,71383,71384))
 # Zero-intercept units are a distinct branch; both signs and both eligible
 # coordinate assignments must be tested rather than resampling them away.
 boundary=[{'free_coefficients':[a,b],'constants':[c,d],'mix':[1,1]} for a,b,c,d in [(1,-3,0,4),(-1,-3,0,4),(2,1,4,0),(2,-1,4,0),(1,1,0,0),(-1,-1,0,0)]]
 records.extend(g.generate_easy(seed=71383,parameters=p) for p in boundary)
 homogeneous=g.generate_easy(seed=71574,profile='q-32244')
 assert system(homogeneous['question'][':question/problem'])==sp.Matrix([[2,2,0],[-10,-10,0],[8,8,0]])
 assert all(vec(c[':answer/value'])[0].subs(v[1],0)==0 for c in field(homogeneous)[':answer-field/choices'])
 assert len(probe(homogeneous)['candidate_positions'])>=2
 records.append(homogeneous)
 dump('unit-zero-source-render-records.json',[homogeneous])
 report=inspect(records);dump('unit-records.json',records);dump('unit-results.json',report);dump('unit-counterexample-after.json',{'record':exact,'probe':probe(exact)})
 dump('unit-grader-input.json',[{'label':'unit-'+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct(r) else 'rejected','purpose':'independent complete solution with coefficient-notation controls'} for c in field(r)[':answer-field/choices']]} for i,r in enumerate(records)])
 dump('unit-render-records.json',[exact,records[-7],records[-6]])
 inventory=json.load(open(E/'generated-records.json'));inventory_tests=[{'question_id':r['question'][':question/id'],'probe':probe(r)} for r in inventory]
 dump('inventory-unit-cue.json',{'tested_generated_records':inventory_tests,'demonstrated_unit_shortcuts':sum(x['probe']['shortcut_correct'] for x in inventory_tests),'limits':'Only ten stored generated records have reproduced generation metadata. Remaining captured inventory is untested for this cue. The historical component-frequency affected report is retained separately.'})
 print(json.dumps({'records':len(records),'source_profiles':14,'successful_unit_shortcuts':0,'exact_system_retained':True}))
if __name__=='__main__':main()
