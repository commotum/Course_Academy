"""Strict source-domain regression. Exits nonzero on the current package.
Usage: .venv/bin/python regression.py --package PATH --output result.json [--candidate-records FILE]
"""
import argparse,importlib.util,sys,json,pathlib
sys.dont_write_bytecode=True
cli=argparse.ArgumentParser();cli.add_argument('--package',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent.parent/'workspace');cli.add_argument('--output',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent/'regression-results.json');cli.add_argument('--candidate-records',type=pathlib.Path);a=cli.parse_args()
spec=importlib.util.spec_from_file_location('candidate',a.package/'17592186100988.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
cases=[
 {'name':'canonical_2x4','source_id':'622baf41-fe35-55ee-bfc6-f1e6a2cb089a','kwargs':{'profile':'location_no_entry','parameters':{'matrix':[[-1,1,2,1],[0,1,-3,-1]],'i':2,'j':3,'letter':'A'}},'expected':'-3'},
 {'name':'source_numeric_only_3x2','source_id':'8904abf3-dbf2-549a-8f8b-9fbdb7308ad3','kwargs':{'profile':'four_locations','template':'display_noperiod_radio','parameters':{'matrix':[[1,2],[-1,5],[-3,4]],'i':3,'j':1,'letter':'E'}},'expected':'-3'},
 {'name':'display_absence_role','source_id':'5bfd6a33-c881-55bc-8200-148d7f57a946','kwargs':{'profile':'overflow_locations','template':'display_radio','parameters':{'matrix':[[1,2,3],[4,5,6]],'i':3,'j':2,'letter':'A'}},'expected':'No such entry'}]
results=[]
for c in cases:
 try:
  r=g.generate('easy',seed=981,**c['kwargs']);f=r['question'][':question/answer-fields'][0];v=next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1]);results.append({**c,'passed':v==c['expected'],'actual':v,'record':r})
 except ValueError as e:results.append({**c,'passed':False,'error':str(e)})
out={'command':'python regression.py --package PACKAGE --output OUTPUT [--candidate-records FILE]','cases':results}
if a.candidate_records:
 records=json.load(open(a.candidate_records));out['candidate_file']=str(a.candidate_records);out['candidate_count']=len(records)
a.output.write_text(json.dumps(out,indent=2));print(json.dumps([{'case':x['name'],'passed':x['passed'],'error':x.get('error')} for x in results]));sys.exit(0 if all(x['passed'] for x in results) else 1)
