import ast, pathlib, sys, json, re, collections, subprocess, os, hashlib
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;W=E.parent/'workspace';sys.path.insert(0,str(W));import generator as g
# Reuse the independent text parser and exact math checker, without audit orchestration.
ns={'__file__':str(E/'audit.py')};tree=ast.parse((E/'audit.py').read_text());nodes=[]
for n in tree.body:
 if isinstance(n,(ast.Import,ast.ImportFrom)):nodes.append(n)
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['x','C'] for t in n.targets):nodes.append(n)
 if isinstance(n,ast.FunctionDef) and n.name in ['tex','parse','field','key','func','primitive','integral_eval','check']:nodes.append(n)
exec(compile(ast.Module(body=nodes,type_ignores=[]),'independent-text-checker','exec'),ns)
parse,field,key,check=[ns[n] for n in ['parse','field','key','check']]
def save(n,d):(E/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
# Complete relevant role pairs keep every bank component and denominator fixed.
pairs=[]
for i,pairing in enumerate(g.QUOTIENT_PAIRINGS):
 roles=[j for j,e in enumerate(pairing) if e==-1];u,v=roles[:2]
 pairs.append({'label':f'pairing-{i}-same-denominator-role-{u}-to-{v}','kind':'relevant','before':g.generate('quotient',2,3,p=4,target=u,reciprocal_exponents=pairing),'after':g.generate('quotient',2,3,p=4,target=v,reciprocal_exponents=pairing),'expected':'different','parameters':{'a':2,'b':3,'p':4,'pairing':pairing,'targets':[u,v]}})
checks=[];results=[]
for p in pairs:
 a,b=p['before'],p['after'];f=field(a);banks=lambda r:sorted(z[':answer/value'] for z in field(r)[':answer-field/choices'])
 assert banks(a)==banks(b)
 assert re.search(r'}\{x\^\{(\d+)\}\}',a['question'][':question/problem'])[1]==re.search(r'}\{x\^\{(\d+)\}\}',b['question'][':question/problem'])[1]
 assert parse(key(a)[':answer/value'])!=parse(key(b)[':answer/value'])
 for which,r,other in [('before',a,b),('after',b,a)]:
  results.append(check(r)); checks.append({'label':p['label']+'/'+which,'record':r,'checks':[{'submitted_answer_id':key(r)[':answer/id'],'expected':'accepted','purpose':'changed role current response'},{'submitted_answer_id':next(z[':answer/id'] for z in field(r)[':answer-field/choices'] if z[':answer/value']==key(other)[':answer/value']),'expected':'rejected','purpose':'old answer after relevant integrand change'}]})
save('revision-counterfactuals.json',pairs);save('revision-counterfactual-results.json',{'pairs':len(pairs),'checks':results,'bank_preserved':True,'denominator_preserved':True,'expected':'Prompt numerator, primitive, solution and accepted choice change together.'});save('revision-grader-input.json',checks)
# Count boundary/resampling with fresh seed and a deterministic replay.
audit={};boundary=g.sample(1000,90620477,audit=audit);save('boundary-1000.json',boundary)
assert boundary==g.sample(1000,90620477)
save('boundary-results.json',{'seed':90620477,'count':len(boundary),'unique_prompt_count':len(set(r['question'][':question/problem'] for r in boundary)),'audit':audit,'deterministic_replay':True,'source_inspection':'sample rejects only repeated prompt strings, no target-conditioned filter; 100*count retry cap. Exact boundaries 0,-1,1001 and difficulty errors exercised in audit.py.'})
print(json.dumps({'revision_pairs':len(pairs),'boundary':audit}))
