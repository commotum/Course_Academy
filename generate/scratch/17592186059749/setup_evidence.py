import importlib.util,json,pathlib
R=pathlib.Path(__file__).parent
sp=importlib.util.spec_from_file_location('g',R.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
src=json.loads((R/'source.json').read_text())
cases=[]
for q in src['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];name=next(k for k,v in g.TEMPLATES.items() if sid in v[4]);p=dict(g.DEFAULTS[name])
 if sid=='q-317374':p.update(n=6,c=4)
 cases.append({'source_id':sid,'template':name,'level':g.TEMPLATES[name][0],'parameters':p,'bank_profile':'observed-'+sid if g.TEMPLATES[name][1]=='radio' else 'blank','authored_level_assignment':sid=='q-1088','missing_correct_inferred':sid=='q-1088','missing_worked_solution_authored':sid=='q-1088'})
(R/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
for c in cases:
 q=next(q for q in src['record'][':knowledge-point/questions'] if q[':question/math-academy-id']==c['source_id'])
 try:rec=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])
 except Exception as e:print('ERROR',c['source_id'],repr(e));continue
 nq=rec['question'];print(c['source_id'],'prompt',q[':question/problem']==nq[':question/problem'],'solution',q.get(':question/worked-solution')==nq[':question/worked-solution'])
 if q.get(':question/worked-solution') and q[':question/worked-solution']!=nq[':question/worked-solution']:
  print('OLD',q[':question/worked-solution']);print('NEW',nq[':question/worked-solution'])
