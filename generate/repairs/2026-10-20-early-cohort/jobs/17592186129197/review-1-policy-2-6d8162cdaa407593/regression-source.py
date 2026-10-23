import sys,pathlib,importlib.util,json,os
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(E/'mpl-cache')
entry=pathlib.Path(sys.argv[1]);label=sys.argv[2]
spec=importlib.util.spec_from_file_location('source_regression',entry);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((E.parent/'source/source.json').read_text());out=[]
for q in source['material']['kp'][':knowledge-point/questions']:
 try:
  r=g.generate('hard',97,profile='raw:'+q[':question/math-academy-id'],parameters={'scale':1})
  fields=q[':question/answer-fields'];actual=r['question'][':question/answer-fields'];passed=len(actual)==len(fields) and sorted(sorted(a[':answer/value']for a in f[':answer-field/choices'])for f in actual)==sorted(sorted(a[':answer/value']for a in f[':answer-field/choices'])for f in fields)
  out.append({'source_id':q[':question/id'],'field_count':[len(fields),len(actual)],'complete_bank_match':passed,'record':r,'passed':passed})
 except ValueError as ex:out.append({'source_id':q[':question/id'],'error':str(ex),'passed':False})
(E/(label+'-source-regression.json')).write_text(json.dumps(out,indent=2))
print('Source contract failures:',sum(not r['passed']for r in out))
assert all(r['passed']for r in out),'SOURCE CONTRACT: current banks missing or stale'
