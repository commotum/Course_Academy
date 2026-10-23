import os,sys,json,re,copy,hashlib,importlib.util,pathlib,shutil
E=pathlib.Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(E/'mpl-cache');os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
spec=importlib.util.spec_from_file_location('reviewed',E/'runtime/17592186129197.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,u,v=s.symbols('x y u v',real=True)
def save(n,d): (E/n).write_text(json.dumps(d,indent=2,ensure_ascii=False,default=str)+'\n')
def parse(t):
 t=t.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace('⁡','').replace(r'\operatorname{ln}',r'\ln').strip().rstrip('.,')
 def group(text,i):
  assert text[i]=='{',(text,i)
  level=1;j=i+1
  while level:
   level+=(text[j]=='{')-(text[j]=='}');j+=1
  return text[i+1:j-1],j
 while r'\frac' in t:
  i=t.index(r'\frac');a,j=group(t,i+5);b,k=group(t,j);t=t[:i]+f'(({a})/({b}))'+t[k:]
 t=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',t)
 t=re.sub(r'\\ln\s*(\d+)',r'log(\1)',t).replace(r'\ln', 'log')
 t=t.replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(t,local_dict={'x':x,'y':y,'u':u,'v':v},transformations=standard_transformations+(implicit_multiplication_application,))
def correct(q):
 f=q[':question/answer-fields'][0];c=f.get(':answer-field/correct');cid=c.get(':answer/id') if isinstance(c,dict) else c[1] if c else None
 return next((a for a in f[':answer-field/choices'] if a[':answer/id']==cid),None)
def oracle(q):
 prompt=q[':question/problem'];maps=re.search(r'u\s*=\s*(.*?),\s*(?:\\,|\\quad|\\qquad)?\s*v\s*=\s*([^$\n]*|[^$]*)',prompt)
 # Extract the complete math chunk with both affine definitions, not generator metadata.
 chunks=re.findall(r'\$\$(.*?)\$\$|\$([^$]*)\$',prompt,re.S)
 m=next(a or b for a,b in chunks if re.search(r'u\s*=',a or b) and re.search(r'v\s*=',a or b))
 U,V=re.split(r',\s*(?:\\,|\\quad|\\qquad)?\s*v\s*=',m.split('=',1)[1]);U=parse(U);V=parse(V)
 inv=s.solve([u-U,v-V],(x,y));det=s.det(s.Matrix([U,V]).jacobian([x,y]));tail=prompt.split('bounded by',1)[1]
 equations=[]
 for t in re.findall(r'\$([^$]*)\$',tail):
  lhs,rhs=t.split('=');equations.append(s.expand((parse(lhs)-parse(rhs)).subs(inv)))
 verts=[]
 for i,a in enumerate(equations):
  for b in equations[:i]:
   for d in s.solve([a,b],(u,v),dict=True):
    if u in d and v in d and d[u].is_real and d[v].is_real: verts.append(d)
 us=sorted(set(d[u] for d in verts),key=float);lo,hi=us[0],us[-1];mid=(lo+hi)/2
 funcs=[]
 for eq in equations:
  funcs.extend(s.solve(eq,v))
 funcs=sorted(funcs,key=lambda z:float(z.subs(u,mid)));lower,upper=funcs[0],funcs[-1]
 area=s.simplify(s.integrate(upper-lower,(u,lo,hi))/abs(det))
 return {'U':str(U),'V':str(V),'det':str(det),'lo':str(lo),'hi':str(hi),'lower':str(lower),'upper':str(upper),'area':area}
def probe(r):
 q=r['question'];bank=q[':question/answer-fields'][0][':answer-field/choices'];vals=[parse(a[':answer/value']) for a in bank]
 candidates=[a for a,z in zip(bank,vals) if z>0 and any(s.simplify(z+w)==0 for w in vals)]
 key=correct(q)
 return {'id':q[':question/id'],'template':r.get('generation',{}).get('template'),'seed':r.get('generation',{}).get('seed'),'parameters':r.get('generation',{}).get('parameters'),'candidate_count':len(candidates),'selected':candidates[0][':answer/id'] if len(candidates)==1 else None,'key':key[':answer/id'] if key else None,'success':len(candidates)==1 and key is not None and candidates[0][':answer/id']==key[':answer/id'],'bank':[a[':answer/value'] for a in bank]}
records=[]
for level in ['easy','moderate','hard']:
 for f,(_,band) in g.FAMILIES.items():
  if band==level:
   for seed in [701,911,1237]: records.append(g.generate(level,seed,template=f))
for seed in range(6061,6073):records.append(g.generate('easy',seed))
pairs=[g.generate('easy',8191,parameters={'a':1,'h':1,'k':0}),g.generate('easy',8191,parameters={'a':1,'h':4,'k':0}),g.generate('easy',8191,parameters={'a':8,'h':1,'k':0})]
save('counterfactual-records.json',pairs);records+=pairs;save('samples.json',records)
for level in ['easy','moderate','hard']:save('samples-'+level+'.json',[r for r in records if r['question'][':question/difficulty']==':question.difficulty/'+level])
batch=json.load(open(E/'batch.json'))
math=[];checks=[]
for label,rs in [('samples',records),('batch',batch)]:
 for i,r in enumerate(rs):
  q=r['question'];o=oracle(q);key=correct(q); ok=s.simplify(parse(key[':answer/value'])-o['area'])==0
  choices=q[':question/answer-fields'][0][':answer-field/choices']; unique=all(s.simplify(parse(a[':answer/value'])-parse(b[':answer/value']))!=0 for i,a in enumerate(choices) for b in choices[:i]);math.append({'group':label,'index':i,'oracle':o,'correct':ok,'unique_bank':unique})
  checks.append({'label':f'{label}-{i}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if s.simplify(parse(a[':answer/value'])-o['area'])==0 else 'rejected','purpose':'Independent integration of printed boundaries; all five choices tested'} for a in choices]})
save('math.json',math)
save('shortcut-results.json',{'strategy':'Choose the unique positive choice with an equal-magnitude negative choice; do not inspect the prompt.','samples':[probe(r) for r in records],'batch':[probe(r) for r in batch]})
# Source replay against current source capture, not the older packaged source.
source=json.load(open(E.parent/'source/source.json')); replay=[];raw=[]
for q in source['material']['kp'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id']
 try:
  r=g.generate('hard',97,profile='raw:'+sid,parameters={'scale':1});raw.append(r)
  fields=q[':question/answer-fields'];gen=r['question'][':question/answer-fields'];banks=[[a[':answer/value'] for a in f[':answer-field/choices']] for f in fields];gbanks=[[a[':answer/value'] for a in f[':answer-field/choices']] for f in gen]
  replay.append({'source':q[':question/id'],'ma_id':sid,'prompt_equal':q[':question/problem']==r['question'][':question/problem'],'field_count':[len(fields),len(gen)],'banks_equal':sorted(map(sorted,banks))==sorted(map(sorted,gbanks))})
 except Exception as ex:replay.append({'source':q[':question/id'],'ma_id':sid,'error':str(ex)})
save('source-replay-records.json',raw);save('source-replay.json',replay)
# Reproduce retained generated records from exact historical seed/parameters.
archive=json.load(open(E.parent/'workspace/17592186129197/reference/replenishment/basis-2715/generated.json'));inventory=json.load(open(E.parent/'source/inventory.json'));byid={q[':question/id']:q for q in inventory['questions']};historical=[];affected=[];invresults=[]
plot=g.plot
for old in archive:
 meta=old['generation'];sid=old['question'][':question/id'];stored=byid.get(sid)
 if not stored:continue
 def output_plot(f,p,d):
  plot(f,p,d)
  return meta['plot']
 g.plot=output_plot
 r=g.generate(old['question'][':question/difficulty'].split('/')[-1],meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
 g.plot=plot
 # Publication localizes images without changing generated identity metadata.
 old_image=re.search(r'!\[\]\((.*?)\)',stored[':question/worked-solution']).group(1)
 canonical=pathlib.Path('/media/jake/SSD/EDB/math')/old_image
 fresh=pathlib.Path(plot(meta['template'],meta['parameters'],g.model(meta['template'],meta['parameters'])))
 image_match=canonical.is_file() and hashlib.sha256(canonical.read_bytes()).digest()==hashlib.sha256(fresh.read_bytes()).digest()
 r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(meta['plot'],old_image)
 # Compare through the application's canonical math formatter; stored TeX has normalization-only changes.
 sys.path.insert(0,'/home/jake/Developer/Course_Academy')
 from scripts.question_capture.math_format import normalize_prose
 solution_equivalent=normalize_prose(r['question'][':question/worked-solution'])==normalize_prose(stored[':question/worked-solution'])
 if solution_equivalent:r['question'][':question/worked-solution']=stored[':question/worked-solution']
 match=image_match and solution_equivalent and (r['question'][':question/id']==sid and r['generation']==meta and r['question'][':question/problem']==stored[':question/problem'] and r['question'][':question/worked-solution']==stored[':question/worked-solution'] and sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in stored[':question/answer-fields'][0][':answer-field/choices']) and correct(r['question'])[':answer/id']==correct(stored)[':answer/id'])
 pr=probe(r);eligible=not stored.get(':question/retired',False) and correct(stored) is not None and bool(stored.get(':question/worked-solution'))
 invresults.append({'id':sid,'entity_id':stored[':db/id'],'exact_reproduction':match,'canonical_math_solution_equal':solution_equivalent,'image_bytes_equal':image_match,'eligible':eligible,'probe':pr})
 if match and eligible and pr['success']:
  historical.append(r);affected.append({'question_id':sid,'entity_id':stored[':db/id'],'finding':'The unique positive choice with an equal-magnitude negative counterpart is the correct area; answer-bank-only shortcut bypasses transformation and integration.','reproduction':'Run .venv/bin/python '+str(E/'audit.py')+'; historical reproduction uses archived seed '+str(meta['seed'])+', template '+meta['template']+', parameters '+json.dumps(meta['parameters'])+'; plot bytes are generated under evidence and the original saved plot reference is restored in memory to verify exact content identity.','evidence_path':'generated-records.json'})
  checks.append({'label':'inventory-'+sid,'record':r,'checks':[{'submitted_answer_id':pr['selected'],'expected':'accepted','purpose':'Answer-bank-only shortcut on exactly reproduced eligible stored question'}]})
save('generated-records.json',historical);save('affected-inventory.json',{'affected_questions':affected});save('inventory-results.json',{'basis':inventory['basis'],'checks':invresults,'original_source_questions_not_classified_as_generated':12})
save('grader-input.json',checks)
# Guards and deterministic replay. No writes outside evidence.
guards=[]
for level,f,p in [('easy','simple',{'a':0,'h':1,'k':0}),('easy','simple',{'a':1,'h':2,'k':0}),('hard','hyper_y',{'a':1,'h':9,'k':3}),('hard','quartic',{'a':1,'h':4,'k':0})]:
 try:g.generate(level,17,template=f,parameters=p);result='accepted'
 except ValueError as ex:result=str(ex)
 guards.append({'level':level,'template':f,'parameters':p,'result':result})
repeat=g.generate('easy',8191,parameters={'a':1,'h':1,'k':0});save('packaging-tests.json',{'relocated_minimal_runtime':str(E/'runtime'),'deterministic_replay':repeat==pairs[0],'guards':guards,'installed':{'python':sys.version.split()[0],'packages':{k:__import__(k).__version__ for k in ['sympy','matplotlib','numpy']}},'declared':json.load(open(E.parent/'workspace/package.json'))['dependencies']})
print(json.dumps({'samples':len(records),'math_failures':sum(not a['correct'] or not a['unique_bank'] for a in math),'shortcut_successes':sum(probe(r)['success'] for r in records),'batch_shortcut_successes':sum(probe(r)['success'] for r in batch),'source_replay':replay,'affected_inventory':len(affected),'inventory_reproduction_failures':sum(not z['exact_reproduction'] for z in invresults)},indent=2))
