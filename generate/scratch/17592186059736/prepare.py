"""Extract lexical components and ordered arithmetic nodes, no database reads."""
import importlib.util,json,re
from pathlib import Path
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
source=json.loads((D/'source.json').read_text())['record']
recipes={};cases=[];inventory=[]
for q in source[':knowledge-point/questions']:
 id=q[':question/math-academy-id'];prompt=q[':question/problem'];mask=prompt;vectors=[];labels=[]
 matches=list(re.finditer(r'\$([auv b])\s*=\s*([^$]+)\$',prompt))[:2]
 assert len(matches)==2,(id,prompt)
 for m in reversed(matches):
  text=m.group(2);raw=text.rstrip('.')
  mask=mask[:m.start(2)]+('@@A@@' if m==matches[0] else '@@B@@')+text[len(raw):]+mask[m.end(2):]
 for m in matches:
  raw=m.group(2).rstrip('.');vectors.append((raw,G.vector(raw)));labels.append(m.group(1))
 ar,a=vectors[0];br,b=vectors[1]
 if id=='q-1408':mask=mask.replace(r'\cdot',r'\times')
 sol=q.get(':question/worked-solution','');rows=[];prefix='';suffix=''
 if sol:
  prefix,body=sol.split(r'\begin{aligned}',1);prefix+=r'\begin{aligned}'
  body,suffix=body.rsplit(r'\end{aligned}',1);suffix=r'\end{aligned}'+suffix
  chunks=body.split(r' \\  & =')
  for chunk in chunks:
   atoms=G.ATOM.findall(chunk)
   if r'\begin{aligned}' in chunk:
    scalers=[]
    # Each determinant has fixed row ownership; header carries no scalars.
    for m in re.finditer(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',chunk):
     lines=m.group(1).split(r'\\');lines=lines[1:] if 'i & j & k' in lines[0] else lines
     assert len(lines)==2
     scalers.extend(['a']*len(G.ATOM.findall(lines[0]))+['b']*len(G.ATOM.findall(lines[1])))
    assert len(scalers)==len(atoms)
    kind='matrix'
   elif len(atoms)==12:
    kind='product';scalers=[]
    expected=[(a[1],b[2]),(a[2],b[1]),(a[0],b[2]),(a[2],b[0]),(a[0],b[1]),(a[1],b[0])]
    for n,(x,y) in enumerate(expected):
     r,t=map(G.scalar,atoms[n*2:n*2+2]);r,t=abs(r),abs(t)
     if (r,t)==(abs(x),abs(y)):scalers+=['a','b']
     elif (r,t)==(abs(y),abs(x)):scalers+=['b','a']
     else:raise ValueError((id,chunk,n,r,t,x,y))
   else:kind='evaluated-or-final';scalers=[]
   rows.append({'text':chunk,'kind':kind,'scalers':scalers})
 fields=[];legacy=[];missing=0
 for f in q[':question/answer-fields']:
  typ=f[':answer-field/type'][':db/ident'].split('/')[-1];key=f[':answer-field/key'];vals=[v[':answer/value'] for v in f[':answer-field/choices']]
  correct=f.get(':answer-field/correct');missing+=correct is None
  if correct:idx=next(n for n,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==correct[':answer/id'])
  elif typ=='radio':idx=next(n for n,z in enumerate(vals) if G.vector(z)==a.cross(b))
  else:raise ValueError('missing blank key')
  fs={'key':key,'type':typ,'values':vals,'correct_index':idx,'original_correct_present':correct is not None}
  if id=='q-1405' and correct is None:legacy.append(fs)
  else:fields.append(fs)
 base={'id':id,'a':[str(z) for z in a],'b':[str(z) for z in b],'a_raw':ar,'b_raw':br,'labels':labels,'prompt_mask':mask,'solution_prefix':prefix,'solution_rows':rows,'solution_suffix':suffix,'fields':fields}
 recipes[id]=base
 cases.append({'source_id':q[':question/id'],'source_math_academy_id':id,'template':id,'parameters':{'a_scale':1,'b_scale':1},'bank_profile':'observed:'+id,'difficulty':'easy','source_difficulty_present':':question/difficulty' in q})
 if legacy:
  extra=dict(base,id=id+'-legacy',fields=legacy);recipes[id+'-legacy']=extra
  cases.append({'source_id':q[':question/id'],'source_math_academy_id':id,'template':id+'-legacy','parameters':{'a_scale':1,'b_scale':1},'bank_profile':'observed:'+id+'-legacy','difficulty':'easy','legacy_evidence_only':True})
 inventory.append({'id':id,'source_db_id':q[':db/id'],'vectors':[base['a'],base['b']],'field_layout':[f['key'] for f in fields],'field_type':fields[0]['type'],'bank_count':sum(len(f['values']) for f in fields+legacy),'source_missing_keys':missing,'solution_stages':[r['kind'] for r in rows]})
(D/'recipes.json').write_text(json.dumps(recipes,indent=2,ensure_ascii=False)+'\n')
(D/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False)+'\n')
(D/'inventory.json').write_text(json.dumps(inventory,indent=2,ensure_ascii=False)+'\n')
print(len(inventory),'sources;',len(cases),'public replay profiles')
