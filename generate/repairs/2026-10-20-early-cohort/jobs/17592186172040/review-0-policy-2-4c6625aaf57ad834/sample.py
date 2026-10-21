from review import *
import importlib.util,math,collections
s=importlib.util.spec_from_file_location('gen',PK/(KP+'.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
source=json.loads((J/'source/source.json').read_text()); src={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
records=[]; replay=[]; checks=[]
def correct(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
for i,(name,sq) in enumerate(src.items()):
 level='moderate' if 'could be' in sq[':question/problem'] else 'hard';r=g.generate(level,seed=901+i,profile=name);replay.append(r)
 sf=sq[':question/answer-fields'][0]; actual=r['question'][':question/answer-fields'][0]; key=sf.get(':answer-field/correct')
 checks.append({'source_id':sq[':question/id'],'profile':name,'bank_equal':sorted(a[':answer/value'] for a in actual[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']),'prompt_equal':r['question'][':question/problem']==sq[':question/problem'],'solution_equal':r['question'][':question/worked-solution']==sq.get(':question/worked-solution'),'key_equal':correct(r)==key[':answer/value'] if key else None,'source_gap':key is None})
for level,templates in [('moderate',['possible_product','possible_mixed','possible_exp']),('hard',['impossible_x','impossible_y']),('easy',['possible_linear'])]:
 for t in templates:
  for seed in [891273,560834,190427,378213,601902]:records.append(g.generate(level,seed=seed,template=t))
p={'a':1,'b':1,'c':0,'px':1,'py':1,'orientation':'y','single':'linear'}
cf=[g.generate('moderate',seed=8723,template='possible_product',parameters=p),g.generate('moderate',seed=8723,template='possible_product',parameters={**p,'a':-1}),g.generate('moderate',seed=8723,template='possible_product',parameters={**p,'single':'exp'}),g.generate('hard',seed=8723,template='impossible_x',parameters=p),g.generate('hard',seed=8723,template='impossible_y',parameters=p)]
# independently use the explicit source x+y to replay canonical easy method; no canonical bank replay API exists.
canonical=g.generate('easy',seed=991,template='possible_linear',parameters=p)
dump('source-replay-records.json',replay+[canonical]);dump('source-replay-results.json',checks)
dump('fresh-records.json',records);dump('counterfactual-records.json',cf)
# Parse each serialized plot slope using independent scalar arithmetic for the generated explicit expressions.
import sympy as sp
x,y=sp.symbols('x y',real=True)
mathchecks=[]
for r in records+cf+json.loads((E/'batch-records.json').read_text()):
 gen=r['generation']; failures=[]; matrices=[]
 for obj in gen['plot_objects']:
  expr=sp.sympify(obj['expression'],locals={'x':x,'y':y}); pts=g.points(expr)
  # scalar substitutions, independent from generator's lambdified evaluator
  for a,b,m in pts:
   target=float(expr.subs({x:sp.Rational(str(a)),y:sp.Rational(str(b))}))
   if not math.isclose(m,target,rel_tol=1e-12,abs_tol=1e-12):failures.append([a,b,m,target])
  matrices.append([float(expr.subs({x:a,y:b})) for a,b in [(-1,-1),(-1,1),(1,-1),(1,1),(.5,.75)]])
 deps=[('x' if sp.diff(sp.sympify(o['expression'],locals={'x':x,'y':y}),x)!=0 else '')+('y' if sp.diff(sp.sympify(o['expression'],locals={'x':x,'y':y}),y)!=0 else '') for o in gen['plot_objects']]
 # Real PNG sidecars in each choice identify actual delivered slopes, without trusting declared dependence labels.
 fld=r['question'][':question/answer-fields'][0]; image_results=[]
 for a in fld[':answer-field/choices']:
  path=pathlib.Path(a[':answer/value']); data=json.loads(path.with_suffix('.json').read_text()); pts=data['points']; fits=[]
  for i,o in enumerate(gen['plot_objects']):
   expr=sp.sympify(o['expression'],locals={'x':x,'y':y});
   if all(math.isclose(m,float(expr.subs({x:sp.Rational(str(xx)),y:sp.Rational(str(yy))})),rel_tol=1e-11,abs_tol=1e-11) for xx,yy,m in pts):fits.append(i)
  iskey=a[':answer/id']==fld[':answer-field/correct'][1]; qualifies=len(fits)==1 and ((deps[fits[0]]=='xy')==(gen['template'].startswith('possible')))
  image_results.append({'choice_id':a[':answer/id'],'fits':fits,'is_key':iskey,'qualifies':qualifies})
  if iskey!=qualifies:failures.append({'choice':a[':answer/id'],'key':iskey,'qualifies':qualifies})
 mathchecks.append({'question_id':r['question'][':question/id'],'template':gen['template'],'equation':gen['equation'],'deps':deps,'point_failures':failures,'images':image_results})
dump('math-results.json',mathchecks)
reject=[]
for kw in [{'parameters':{**p,'a':0}},{'template':'possible_linear'},{'field_type':'checkbox'},{'profile':'q-98229'}]:
 try:g.generate('moderate',seed=891273,**kw);reject.append({'args':kw,'rejected':False})
 except Exception as ex:reject.append({'args':kw,'rejected':True,'exception':repr(ex)})
r1=g.generate('moderate',891273);r2=g.generate('moderate',891273)
dump('sampling-results.json',{'record_count':len(records),'deterministic_replay':r1==r2,'invalid_inputs':reject,'templates':dict(collections.Counter(r['generation']['template'] for r in records))})
print('Saved',len(records),'fresh records,',len(cf),'controlled records;',sum(bool(v['point_failures']) for v in mathchecks),'math failures')
