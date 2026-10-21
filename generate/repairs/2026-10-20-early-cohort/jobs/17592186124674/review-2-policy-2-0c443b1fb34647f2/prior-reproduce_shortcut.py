"""Strict independent acceptance probe. Exit 1 when the whole supplied set is solved by length alone."""
import argparse,json,pathlib,re
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--index',type=int);p.add_argument('--output',required=True);a=p.parse_args()
records=json.load(open(a.input));records=records if a.index is None else [records[a.index]]
results=[]
for r in records:
 f=r['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];lengths=[len(re.sub(r'\s+','',x[':answer/value'])) for x in choices];i=min(range(len(lengths)),key=lengths.__getitem__)
 results.append({'question_id':r['question'][':question/id'],'generation':r.get('generation'),'lengths':lengths,'selected_value':choices[i][':answer/value'],'unique_shortest':lengths.count(lengths[i])==1,'correct':choices[i][':answer/id']==f[':answer-field/correct'][1]})
failed=all(x['unique_shortest'] and x['correct'] for x in results)
out={'strategy':'Choose the uniquely shortest equation without reading the prompt or interpreting its mathematics.','baseline':0.2,'correct':sum(x['unique_shortest'] and x['correct'] for x in results),'total':len(results),'acceptance_failed':failed,'cases':results}
pathlib.Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'}));raise SystemExit(1 if failed else 0)
