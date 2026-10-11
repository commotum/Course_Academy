import json,pathlib,sys
BASE=pathlib.Path(__file__).parent
latest={}
for x in (BASE.parent/'math/reviews.jsonl').read_text().splitlines():
 r=json.loads(x);latest[r['id']]=r
H=[r for r in latest.values() if not r['ready']]
def source(k):
 r=latest[k];s=json.load(open(r['directory']+'/state.json'))['questions'][k];c=json.load(open(r['directory']+'/content.json'));branch='after' if (s.get('after') or {}).get('worked_solution') else 'history';return r,s,c,branch
if __name__=='__main__':
 for n,r in list(enumerate(H))[int(sys.argv[1]):int(sys.argv[2])]:
  k=r['id'];r,s,c,branch=source(k);print('\n###',n,k);print('PROMPT',s['before']['problem']);print('SOLUTION',s[branch]['worked_solution'])
  for f in s['before']['fields']:print('FIELD',f['key'],f['type']);print('CHOICES',json.dumps([{x:y for x,y in t.items() if x!='html'} for t in f.get('choices',[])],ensure_ascii=False))
  print('ASSETS',s['before'].get('assets'))

def write(specs):
 existing={json.loads(x)['id'] for x in (BASE/'hold-peer-review.jsonl').read_text().splitlines()} if (BASE/'hold-peer-review.jsonl').exists() else set()
 with open(BASE/'hold-peer-review.jsonl','a') as out:
  for k,confirmed,reason,note,*release in specs:
   assert k not in existing
   old,s,c,branch=source(k);sol=s[branch]['worked_solution'];file=old['directory']+'/state.json';ptr=f'/questions/{k}/{branch}/worked_solution'
   evidence=dict(problem=s['before']['problem'],fields=s['before']['fields'],worked_solution=sol,source_location=dict(file=file,json_pointer=ptr),method='Independent peer review of full original prompt, all original before options, content.json and complete saved Math Academy worked solution; diagrams reviewed where domain depends on them.')
   record=dict(id=k,confirmed_hold=confirmed,reason=reason,explanation=note,source_evidence=evidence)
   if release:
    index=release[0];b=s['before']['fields'][0];choice=b['choices'][index]
    record['resolve_record']=dict(id=k,ready=True,directory=old['directory'],fields=[dict(key=b['key'],choice_index=index,answer={x:choice[x] for x in ('type','value')},binding='Requested acceleration in original prompt units cm/s², for the sole original radio field.',source_quote=sol,source_location=dict(file=file,json_pointer=ptr),method=note)],situation_types=['harmless_solution_unit_typo'],disagreements=['Saved final solution labels its dimensionally correct second-derivative calculation with m/s²; original prompt and original correct choice both use cm/s².'])
   out.write(json.dumps(record,ensure_ascii=False)+'\n');existing.add(k)
 print('peer checkpoint',len(existing))
