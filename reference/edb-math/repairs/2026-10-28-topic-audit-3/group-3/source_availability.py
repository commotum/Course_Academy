import json,re,collections
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());M=json.loads((H/'source-manifest.json').read_text());R=json.loads((H/'source-records.json').read_text());proof=collections.defaultdict(lambda:collections.defaultdict(list))
for r in R:proof[r['source_identity']][r['attribute']].append(r['path'])
for sid,paths in M.items():
 for path in paths:
  p=Path(path)
  if not re.search(r'\.json(?:\.previous)?$',str(p)):continue
  d=json.loads(p.read_text());html=d.get('html')or d.get('raw_html')or''
  if d.get('fields'):proof[sid]['bank'].append(path)
  # Presence uses owned original widget wrappers, so explanation-only captures never inflate prompt availability.
  soup=BeautifulSoup(html,'html.parser')
  for attr,classes in [('question/problem',['questionWidget-text','questionText','exampleQuestion']),('question/worked-solution',['questionExplanation','questionWidget-explanation','workedSolution','exampleExplanation'])]:
   if any(soup.find(class_=c)is not None for c in classes):proof[sid][attr].append(path)
  if soup.select('.questionStatements > li'):proof[sid]['checkbox statements'].append(path)
rows=[]
for q in D['questions']:
 sid=q.get(':question/math-academy-id');r={'entity':q[':db/id'],'source_identity':sid,'classification':'generated/no original MA identity'if sid is None else'original source identity','evidence':{k:sorted(set(v))for k,v in proof[sid].items()}if sid else{}}
 for a in['question/problem','question/worked-solution','bank','checkbox statements']:r[a+'_available']=bool(r['evidence'].get(a))
 rows.append(r)
summary={'basis':9837,'questions':len(rows),'source_identity_questions':sum(r['source_identity']is not None for r in rows),'generated_no_original_id':sum(r['source_identity']is None for r in rows),'original_problems_available':sum(r['question/problem_available']for r in rows),'original_solutions_available':sum(r['question/worked-solution_available']for r in rows),'original_banks_available':sum(r['bank_available']for r in rows),'true_original_prompt_gaps':[{'entity':r['entity'],'source_identity':r['source_identity'],'other_evidence_attributes':list(r['evidence'])}for r in rows if r['source_identity']and not r['question/problem_available']],'tutorials_available':len({r['source_identity']for r in R if r['attribute']=='tutorial/content'}),'identity_captures_verified':len(json.loads((H/'source-identity-evidence.json').read_text()))}
(H/'source-availability-ledger.json').write_text(json.dumps({'summary':summary,'questions':rows},indent=2));print(json.dumps({k:v for k,v in summary.items()if k!='true_original_prompt_gaps'},indent=2));print('prompt gaps',len(summary['true_original_prompt_gaps']))
