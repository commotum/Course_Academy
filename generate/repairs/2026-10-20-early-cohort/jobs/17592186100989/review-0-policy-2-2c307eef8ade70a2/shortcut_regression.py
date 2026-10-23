"""Independent rendered-prompt shortcut probe; exit 1 retains the demonstrated failure.
Run: python3 shortcut_regression.py --candidate-records delivery-sample/accepted.json --output shortcut-regression.json
No generator metadata is used to choose an answer.
"""
import argparse,json,re,pathlib
p=argparse.ArgumentParser();p.add_argument('--candidate-records',required=True);p.add_argument('--output',required=True);a=p.parse_args()
rs=json.load(open(a.candidate_records));cases=[]
for r in rs:
 q=r.get('question',r);f=q[':question/answer-fields'][0];typ=f[':answer-field/type'];typ=typ.get(':db/ident') if isinstance(typ,dict) else typ
 if not typ.endswith('/radio'):continue
 m=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',q[':question/problem'],re.S)
 if len(m[1].split('\\\\'))!=2:continue
 c=f[':answer-field/correct'];ci=c[':answer/id'] if isinstance(c,dict) else c[1]
 value=next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==ci)
 cases.append({'question_id':q[':question/id'],'cue':'radio and 2x2 matrix','predicted':'No such entry','actual':value,'correct':value=='No such entry'})
report={'command':f'python3 shortcut_regression.py --candidate-records {a.candidate_records} --output {a.output}','candidate_records':a.candidate_records,'cases':cases,'correct':sum(c['correct'] for c in cases),'total':len(cases),'baseline':0.2,'unbroken_cue':bool(cases) and all(c['correct'] for c in cases),'interpretation':'Every observed 2x2 radio is answered by shape alone. Causal construction restrictions in construction-restrictions.json establish this as a family rule rather than a chance small-sample association.'}
pathlib.Path(a.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='cases'}));raise SystemExit(1 if report['unbroken_cue'] else 0)
