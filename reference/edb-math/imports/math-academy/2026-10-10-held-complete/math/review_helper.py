import json,sys,re
from pathlib import Path
base=Path(__file__).parent
a=json.loads((base/'assignment.json').read_text());ids=list(a)
def load(q):
 x=a[q];s=json.loads(Path(x['directory'],'state.json').read_text())['questions'][q];return x,s
if sys.argv[1]=='read':
 for q in ids[int(sys.argv[2]):int(sys.argv[3])]:
  x,s=load(q);content=json.loads(Path(x['directory'],'content.json').read_text());html=s['before'].get('html','');print('\nID',q,'TOPIC',x['knowledge_point']);print('PROMPT:',s['before']['problem']);print('SOLUTION:',s.get('history',{}).get('worked_solution') or s.get('after',{}).get('worked_solution'));print('OPTIONS:');
  for f in s['before']['fields']:
   print('FIELD',f['key']);
   for i,ch in enumerate(f.get('choices',[])):print(i,ch['type'],ch['value'])
if sys.argv[1]=='write':
 decisions=json.loads(sys.argv[2]);out=[]
 for q,desc in decisions.items():
  x,s=load(q);sel=desc['indices'];sf='history' if s.get('history',{}).get('worked_solution') else 'after';sol=s[sf]['worked_solution'];fields=[]
  for f,i in zip(s['before']['fields'],sel):
   ch=f['choices'][i];quote=desc.get('quote',sol);assert quote in sol
   fields.append(dict(key=f['key'],choice_index=i,answer={k:ch[k] for k in ['type','value']},binding=desc.get('binding',s['before']['problem']),source_quote=quote,source_location=dict(file=str(Path(x['directory'],'state.json')),json_pointer=f'/questions/{q}/{sf}/worked_solution'),method=desc.get('method','Full worked solution and prompt reviewed; original option matches the requested mathematical conclusion, with independent arithmetic/sign/domain check.')))
  out.append(dict(id=q,ready=True,directory=x['directory'],fields=fields,situation_types=desc.get('types',['equation_chain_conclusion']),disagreements=desc.get('disagreements',[])))
 for o in out:
  if decisions[o['id']].get('revision_reason'):o['revision_reason']=decisions[o['id']]['revision_reason']
 with (base/'reviews.jsonl').open('a') as f:
  for o in out:f.write(json.dumps(o,ensure_ascii=False)+'\n')
 print('checkpoint',len(out),'total',len((base/'reviews.jsonl').read_text().splitlines()))
if sys.argv[1]=='hold':
 decisions=json.loads(sys.argv[2]);path=base/'reviews.jsonl';old=[json.loads(l) for l in path.read_text().splitlines()] if path.exists() else [];out=[]
 for q,d in decisions.items():
  x,s=load(q);out.append(dict(id=q,ready=False,directory=x['directory'],fields=[],situation_types=d.get('types',['multiple_integral_expressions_same_value']),disagreements=[],hold_reason=d.get('reason','multiple_correct_options'),explanation=d['explanation'],supporting_evidence=dict(prompt=s['before']['problem'],worked_solution=s.get('history',{}).get('worked_solution') or s.get('after',{}).get('worked_solution'),source_location=dict(file=str(Path(x['directory'],'state.json')),json_pointer=x['source_solution_location']),valid_choice_indices=d.get('valid',[]),original_valid_choices=[s['before']['fields'][0]['choices'][i]['value'] for i in d.get('valid',[])],intended_choice_index=d.get('intended'),domain_verification=d.get('domain'))))
 for o in out:
  if any(previous['id']==o['id'] for previous in old):o['revision_reason']='Full mathematical review identified substantive ambiguity/content defect in earlier checkpoint.'
 with path.open('a') as f:
  for o in out:f.write(json.dumps(o,ensure_ascii=False)+'\n')
 print('held checkpoint',len(out),'total',len(path.read_text().splitlines()))
