"""Read-only closure check against the two actually published theorem packages."""
import importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;root=Path('/media/jake/SSD/EDB/math');publications={p['kp']:p for p in json.loads((H.parent.parent/'2026-10-27-linear-algebra-audit/group-2/generator-publications.json').read_text())};out=[]
for kp in [17592186124629,17592186124630]:
 publication=publications[kp];entry=root/publication['new_reference'];sys.path.insert(0,str(entry.parent));spec=importlib.util.spec_from_file_location('closure_'+str(kp),entry);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 if kp==17592186124629:
  raw={q[':question/math-academy-id']:q for q in m.SOURCE[':knowledge-point/questions']};assert'q-47586'in raw and'q-47586'not in m.CASES;assert'q-47586'in m.EXCLUDED
  try:m.generate('moderate',0,'q-47586',{'premise':'decision'})
  except ValueError as ex:rejection=str(ex)
  else:raise AssertionError('Excluded source could generate')
  profiles=[];total=0
  for sid,slots in m.SLOTS.items():
   if'basis'not in slots:continue
   i=slots.index('basis');counts={'invertible':0,'singular':0,'positive_basis':0,'negative_basis':0};ids=[]
   for p in m.domain(sid):
    r=m.generate('moderate',0,sid,p);q=r['question'];assert'Every finite-dimensional subspace has a basis. The zero subspace has the empty basis.'in q[':question/worked-solution'];statement=m.proposition('basis',p['truths'][i],m.DIMENSIONS.get(sid,'n'));assert statement in q[':question/problem']or any(f[':answer-field/key']==statement for f in q[':question/answer-fields'])
    correct=[f[':answer-field/correct']for f in q[':question/answer-fields']]
    if m.checkbox(sid):
     f=q[':question/answer-fields'][i];a=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert(a[':answer/value']=='true')==p['truths'][i]
    else:
     f=q[':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert m.subset(a[':answer/value'])==tuple(p['truths'])
    counts['invertible'if p['invertible']else'singular']+=1;counts['positive_basis'if p['truths'][i]else'negative_basis']+=1;total+=1
   profiles.append({'source_profile':sid,'counts':counts,'basis_truth_rule':'has a basis is always true; has no basis is always false, for both invertible and singular matrices'})
  out.append({'kp':kp,'published_reference':publication['new_reference'],'source_q47586_retained_as_evidence_only':True,'eligible_for_fresh_generation':False,'explicit_exclusion':m.EXCLUDED['q-47586'],'eligibility_filter':'CASES requires difficulty and worked solution; q-47586 has neither and is absent from CASES/SLOTS','explicit_generate_rejection':rejection,'fresh_basis_cases_exhaustively_checked':total,'profiles':profiles,'reason':'If det(A)≠0, Null(A)={0}; the empty set spans {0} and is linearly independent, so it is a basis. The no-basis statement is false. Correct existing banks and authored empty-basis explanations are used.'})
 else:
  assert'q-47586'not in m.SOURCES and'q-47586'not in m.TARGETS;assert m.TERMS['null-space-rhs']==r'\{0\}'and m.TERMS['null-dimension-value']=='0';assert'no basis'not in m.theorem()
  out.append({'kp':kp,'published_reference':publication['new_reference'],'source_q47586_present':False,'eligible_for_fresh_generation':False,'null_space_term':m.TERMS['null-space-rhs'],'null_dimension_term':m.TERMS['null-dimension-value'],'reason':'This separate missing-fragment KP contains no q-47586 source and generates the correct null-space/nullity theorem rather than a no-basis claim.'})
 sys.path.pop(0)
(H/'q47586-recurrence-verification.json').write_text(json.dumps({'passed':True,'database_writes':0,'successor_needed':False,'checks':out},indent=2)+'\n');print(json.dumps({'passed':True,'successor_needed':False,'fresh_basis_cases_checked':out[0]['fresh_basis_cases_exhaustively_checked'],'published_references':[p['published_reference']for p in out]},indent=2))
