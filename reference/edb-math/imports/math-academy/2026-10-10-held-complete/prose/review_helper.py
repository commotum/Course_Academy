import json,sys,pathlib,re
ROOT=pathlib.Path(__file__).parent
A=json.load(open(ROOT/'assignment.json'))
def get(qid):
 a=A[qid];s=json.load(open(pathlib.Path(a['directory'])/'state.json'));q=s['questions'][qid];p=a['source_solution_location'];v=s
 for part in p.split('/')[1:]:v=v[int(part)] if isinstance(v,list) else v[part]
 c=json.load(open(pathlib.Path(a['directory'])/'content.json'));cq=next(x for x in c['questions'] if x.get('math_academy_id')==qid)
 return a,q,v,p,cq
if sys.argv[1]=='read':
 for qid in list(A)[int(sys.argv[2]):int(sys.argv[3])]:
  a,q,sol,p,cq=get(qid);print('\nID',qid,'TOPIC',a['knowledge_point']);print('PROMPT',q['before']['problem']);print('SOLUTION',sol)
  for f in q['before']['fields']:print('FIELD',f['key'],[(i,x['type'],x['value']) for i,x in enumerate(f.get('choices',[]))])
  print('CONTENT_SAME',cq['problem']==q['before']['problem'],'SOLUTION_SAME',cq['worked_solution']==sol,'HTML_LAYOUT',re.findall(r'<(?:input|select|table|ol)[^>]*>',q['before'].get('html',''))[:15])
elif sys.argv[1]=='write':
 rows=json.load(sys.stdin)
 with open(ROOT/'reviews.jsonl','a') as out:
  for row in rows:
   qid=row['id'];a,q,sol,p,cq=get(qid);fields=[]
   for item in row.get('fields',[]):
    key=item['key'];f=next(f for f in q['before']['fields'] if f['key']==key);choice=f['choices'][item['choice_index']];quote=item['source_quote'];assert quote in sol,(qid,quote)
    fields.append(dict(key=key,choice_index=item['choice_index'],answer={k:choice[k] for k in ('type','value')},binding=item['binding'],source_quote=quote,source_location={'file':a['directory']+'/state.json','json_pointer':p},method=item.get('method','Read full captured prompt and worked solution; independently checked mathematics and matched the requested role to the original before choices.')))
   if row.get('ready',True):assert len(fields)==len(q['before']['fields']),qid
   result=dict(id=qid,ready=row.get('ready',True),directory=a['directory'],fields=fields,situation_types=row.get('situation_types',['prose_semantic_choice']),disagreements=row.get('disagreements',[]))
   for k in ('hold_reason','explanation','supporting_evidence','restored_problem','layout_note','revision_reason'):
    if k in row:result[k]=row[k]
   out.write(json.dumps(result,ensure_ascii=False)+'\n');out.flush()
 print('appended',len(rows))
if sys.argv[1]=='compactwrite':
 with open(ROOT/'reviews.jsonl','a') as out:
  for qid,index,binding,*extra in json.load(sys.stdin):
   a,q,sol,p,cq=get(qid);assert len(q['before']['fields'])==1;f=q['before']['fields'][0];c=f['choices'][index];r=dict(id=qid,ready=True,directory=a['directory'],fields=[dict(key=f['key'],choice_index=index,answer={k:c[k] for k in ('type','value')},binding=binding,source_quote=sol,source_location={'file':a['directory']+'/state.json','json_pointer':p},method='Full original prompt, full saved worked solution, all original choices and layout reviewed; independent mathematical check and semantic matching.')],situation_types=['roman_statement_subset'] if '<ol class="questionStatements"' in q['before'].get('html','') else ['prose_semantic_choice'],disagreements=extra)
   out.write(json.dumps(r,ensure_ascii=False)+'\n');out.flush()
 print('checkpointed')
