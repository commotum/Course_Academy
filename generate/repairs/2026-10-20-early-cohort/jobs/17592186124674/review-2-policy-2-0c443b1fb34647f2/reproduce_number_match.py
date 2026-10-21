"""Strict mixed-bank regression: sole positive prompt numeral must not identify one correct option.
Run: <job-python> -B reproduce_number_match.py --output number-match-results.json
Exit 1 = a demonstrated mixed-bank bypass. No package writes.
"""
import sys,pathlib,json,re,importlib.util,argparse
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;W=E.parent/'workspace'
p=argparse.ArgumentParser();p.add_argument('--input');p.add_argument('--output',default='number-match-results.json');a=p.parse_args()
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
if a.input:records=json.loads((E/a.input).read_text())
else:
 s=importlib.util.spec_from_file_location('g',W/'17592186124674.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
 records=[g.generate_easy(seed=3,parameters={'context':'deer','capacity':60})];save('number-match-minimal-records.json',records)
rows=[]
for r in records:
 q=r['question'];f=q[':question/answer-fields'][0];options=f[':answer-field/choices'];numbers=sorted({int(x) for x in re.findall(r'\d+',q[':question/problem']) if int(x)>0})
 # This is token equality only: no interpretation of the derivative or RHS.
 matches=[c for c in options if len(numbers)==1 and numbers[0] in [int(x) for x in re.findall(r'\d+',c[':answer/value'])]]
 correct=len(matches)==1 and matches[0][':answer/id']==f.get(':answer-field/correct',[None,None])[1]
 rows.append({'question_id':q[':question/id'],'generation':r.get('generation'),'positive_prompt_numbers':numbers,'matching_choice_count':len(matches),'selected':matches[0][':answer/value'] if len(matches)==1 else None,'correct_without_modeling':correct,'all_options':[c[':answer/value'] for c in options]})
failed=bool(rows) and all(x['correct_without_modeling'] for x in rows)
report={'strategy':'Copy the sole positive numeral from the prompt; select its unique matching option, without interpreting signs, variable factors, powers, or equation form.','baseline':0.2,'correct':sum(x['correct_without_modeling'] for x in rows),'total':len(rows),'acceptance_failed':failed,'cases':rows};save(a.output,report);print(json.dumps({k:v for k,v in report.items() if k!='cases'}));raise SystemExit(1 if failed else 0)
