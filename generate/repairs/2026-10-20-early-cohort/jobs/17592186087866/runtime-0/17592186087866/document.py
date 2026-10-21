import hashlib,json,sys
from pathlib import Path
from fractions import Fraction
P=Path(__file__).resolve().parent;R=P.parents[2];sys.path.insert(0,str(P))
import validate as v
g=v.g
families=[]
for level,templates in g.FAMILIES.items():
 for sid in templates:
  q=g.SOURCES[sid];m=g.data(sid,g.ORIGINAL[sid]);fields=[]
  for f in q[':question/answer-fields']:
   fields.append({'db_id':f[':db/id'],'id':f[':answer-field/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'correct_id':f.get(':answer-field/correct',{}).get(':answer/id'),'choices':[{'original_id':a[':answer/id'],'field_id':f[':answer-field/id'],'value':a[':answer/value'],'correct':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id'),'mapped_slot':next(i for i,e in enumerate(m['bank']) if v.same(v.equation(a[':answer/value'])[0],e[0]) and v.same(v.equation(a[':answer/value'])[1],e[1]))} for a in f[':answer-field/choices']]})
  families.append({'source_id':sid,'source_db_id':q[':db/id'],'difficulty':level,'specific_problem':q[':question/problem'],'original_solution':q[':question/worked-solution'],'original_parameters':g.ORIGINAL[sid],'profile':sid,'plot_rating':'none','domain':g.DOMAINS.get(sid,'real x,y'),'fields':fields,'step_count':len(m['stages']),'recipe_implementation':'generate/scratch/17592186087866.py:data, branch '+sid,'unknown_distractor_intent':sid in ('q-16396','q-79697')})
(P/'template-extraction.json').write_text(json.dumps({'database':'math','basis':g.RAW['basis'],'lineage':g.RAW['lineage'],'templates':families},indent=2,ensure_ascii=False)+'\n')
(P/'source-cases.json').write_text(json.dumps([{'source_id':x['source_id'],'template':x['source_id'],'difficulty':x['difficulty'],'parameters':x['original_parameters'],'bank_profile':x['source_id']} for x in families],indent=2)+'\n')
ph={Fraction(h,a) for h in range(1,9) for a in range(2,6)};qc={Fraction(b,c) for b in range(1,6) for c in range(1,6)}
products={a*b for a in range(1,7) for b in range(1,5)}
counts={'q-16400':len(ph)*len(qc),'q-8359':8,'q-103349':6,'q-103354':6,'q-16396':8,'q-79697':8,'q-79699':7,'q-8360':8,'q-16401':len(products)*6}
cap={'supported_levels':['easy','hard'],'unsupported_levels':['moderate'],'observed_levels':['easy','hard'],'authored_levels':[],'templates_by_level':g.FAMILIES,'finite_domain_counts_before_database_exclusions':counts,'total_easy':sum(counts[t] for t in g.FAMILIES['easy']),'total_hard':counts['q-16401'],'count_derivation':'Easy trig-rearrangement uses distinct reduced h/a and b/c pairs; other easy profiles vary one coefficient/frequency. Hard counts unique products ab times frequencies n. Each normalized forcing shape discards global dependent scaling. Source/canonical tasks excluded during replenishment. No seeds, choices or UUIDs counted.','exceptions':[{'level':'moderate','reason':'No classified source/layout or validated independent workload; no moderate generator','available':0,'rolling_target':5,'unfilled':5,'classification_basis':g.RAW['basis'],'reopen':'New evidence'}],'source_anomalies':[{'source_id':'q-16400','reason':'Additional duplicate selection field has no correct reference','policy':'Preserve original in database, omit malformed field from new instances'}],'plots':'none','runtime':{'python':sys.version.split()[0],'sympy':g.s.__version__}}
(P/'capabilities.json').write_text(json.dumps(cap,indent=2)+'\n')
print(json.dumps({'finite_easy':cap['total_easy'],'finite_hard':cap['total_hard'],'complete_source_templates':len(families)}))
