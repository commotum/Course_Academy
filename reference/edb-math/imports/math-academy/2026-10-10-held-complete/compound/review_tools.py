import json,pathlib,sys,re
BASE=pathlib.Path(__file__).parent
A=json.load(open(BASE/'assignment.json'))
def source(k):
 v=A[k]; s=json.load(open(v['directory']+'/state.json'))['questions'][k]
 c=json.load(open(v['directory']+'/content.json'))
 return v,s,c

def show(start,end):
 for n,k in list(enumerate(A))[start:end]:
  v,s,c=source(k); b=s['before']; aft=s.get('after') or {}; hist=s.get('history') or {}
  sol=aft.get('worked_solution') or hist.get('worked_solution') or ''
  print('\n###',n,k,v['knowledge_point']); print('PROMPT:',b['problem']);print('SOLUTION:',sol)
  for f in b['fields']:
   print('FIELD:',f['key'],f['type'],f.get('dom_id','')); print('CHOICES:',json.dumps([{x:y for x,y in t.items() if x!='html'} for t in f.get('choices',[])],ensure_ascii=False))
  print('ASSETS:',b.get('assets')); print('OL:',re.findall(r'<ol[^>]*>',b.get('html','')))
  cc=next((t for t in c['questions'] if t['math_academy_id']==k),None)
  print('CONTENT_AGREES:',bool(cc and cc['problem']==b['problem'] and cc['worked_solution']==sol))
def append(specs):
 existing={json.loads(x)['id'] for x in (BASE/'reviews.jsonl').read_text().splitlines()} if (BASE/'reviews.jsonl').exists() else set()
 with open(BASE/'reviews.jsonl','a') as out:
  for spec in specs:
   k,indices,note=spec[:3]; extra=spec[3] if len(spec)>3 else {}
   assert k not in existing,k
   v,s,c=source(k); b=s['before']; aft=s.get('after') or {};hist=s.get('history') or {}
   branch='after' if aft.get('worked_solution') else 'history'; sol=s[branch]['worked_solution']; assert sol
   fields=[]
   assert len(indices)==len(b['fields'])
   for j,(f,i) in enumerate(zip(b['fields'],indices)):
    ch=f['choices'][i]
    fields.append(dict(key=f['key'],choice_index=i,answer={x:ch[x] for x in ('type','value')},binding=f"Original {f['type']} field {j+1} ({f['key']}): "+note,source_quote=sol,source_location=dict(file=v['directory']+'/state.json',json_pointer=f'/questions/{k}/{branch}/worked_solution'),method='Full original prompt, before choices and saved MA worked solution reviewed; independent mathematical and option-uniqueness check. '+note))
   r=dict(id=k,ready=True,directory=v['directory'],fields=fields,situation_types=['saved_solution_field_binding'],disagreements=[])
   r.update(extra)
   out.write(json.dumps(r,ensure_ascii=False)+'\n');existing.add(k)
 print('checkpoint',len(existing))
if __name__=='__main__':show(int(sys.argv[1]),int(sys.argv[2]))
def hold(k,reason,explanation,evidence=None):
 v,s,c=source(k); existing={json.loads(x)['id'] for x in (BASE/'reviews.jsonl').read_text().splitlines()};assert k not in existing
 r=dict(id=k,ready=False,directory=v['directory'],fields=[],situation_types=['substantive_source_defect'],disagreements=[explanation],hold_reason=reason,explanation=explanation,supporting_evidence=evidence or {'problem':s['before']['problem'],'worked_solution':s.get('after',{}).get('worked_solution') or s.get('history',{}).get('worked_solution'),'file':v['directory']+'/state.json'})
 with open(BASE/'reviews.jsonl','a') as out:out.write(json.dumps(r,ensure_ascii=False)+'\n')
 print('hold',k,reason)
