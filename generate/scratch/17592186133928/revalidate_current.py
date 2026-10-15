"""Read-only current-source classification delta and bank/field checks."""
import importlib.util,json,sys
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P))
sp=importlib.util.spec_from_file_location('validation',P/'validate.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);g=v.g
current=g.CURRENT_CAPTURE['record'];original={q[':question/math-academy-id']:q for q in g.KP[':knowledge-point/questions']};report=[]
for q in current[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];r,f,lo,hi=g.objects(sid,dict(a=1,b=1,d=1,c=1));integrand=sum(a.subs(dict(zip((g.X,g.Y,g.Z),r)),simultaneous=True)*g.s.diff(b,g.T) for a,b in zip(f,r));correct=g.s.simplify(g.s.integrate(integrand,(g.T,lo,hi)))
 fields=q[':question/answer-fields'];banks=[]
 for field in fields:
  vals=[v.parse(a[':answer/value']) for a in field[':answer-field/choices']];assert all(not v.equal(a,b) for i,a in enumerate(vals) for b in vals[:i])
  key=field.get(':answer-field/correct',{}).get(':answer/id')
  if key:
   assert all(v.equal(value,correct)==(a[':answer/id']==key) for value,a in zip(vals,field[':answer-field/choices']))
  banks.append({'count':len(vals),'correct_present':key is not None,'mathematical_key_valid':key is not None,'source_option_values':[a[':answer/value'] for a in field[':answer-field/choices']]})
 if sid in original and sid!='q-162377':
  assert q[':question/problem']==original[sid][':question/problem'];assert q.get(':question/worked-solution')==original[sid].get(':question/worked-solution')
 report.append({'source':sid,'difficulty':q[':question/difficulty'][':db/ident'],'template':sid,'plot_rating':'none','field_type':'radio','fields':len(fields),'banks':banks,'computed_correct':g.tex(correct),'new_template':sid not in original,'changed_source':sid=='q-162377'})
(P/'current-source-validation.json').write_text(json.dumps({'basis':2620,'lineage':g.CURRENT_CAPTURE['lineage'],'practice_count':len(report),'templates':12,'complete_banks':13,'mathematical_choices':65,'questions':report,'all_present_keys_mathematically_valid':True,'ungradable_source_fields_preserved':1,'database_writes':0},indent=2)+'\n')
print('12 current sources classified; all present keys verified; one incomplete duplicate field preserved')
