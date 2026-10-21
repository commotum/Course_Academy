from review import *
records=json.load(open('records.json'))+json.load(open('source-replays.json'))+json.load(open('runner-batch.json'))+sum([[p['before'],p['after']] for p in json.load(open('point-pairs.json'))],[])
results=[]
for i,r in enumerate(records):
 f,v=expected(r);power=next(z for z in f.atoms(s.Pow) if z.base.is_Integer and z.base>1);exponent=power.exp
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',r['question'][':question/worked-solution'],re.S)
 row={'index':i,'id':r['question'][':question/id'],'checks':[],'unparsed_source_steps':[]}
 for j,block in enumerate(blocks):
  rhses=re.split(r'&\s*=',block)[1:]
  if not rhses:continue
  if j==len(blocks)-1 and 'equation of the tangent' in r['question'][':question/problem']:
   rhses=[rhses[-1]];target=v
  else:
   target=s.diff(f,x) if j==0 else v
   if j>0 and 'equation of the tangent' in r['question'][':question/problem']:
    tpoint=parse(re.search(r'where \$x=(.*?)\$',r['question'][':question/problem'])[1].rstrip(' .'));target=s.diff(f,x).subs(x,tpoint)
    if 'y' in block.split('&')[0] and 'frac' not in block.split('&')[0]:target=f.subs(x,tpoint)
  for k,rhs in enumerate(rhses):
   rhs=rhs.split('\\\\')[0].strip().rstrip('.')
   if any(z in rhs for z in [r'\text{d}',r'\mathrm{d}',r'\textrm',r'\frac{dy}', '|']):continue
   try:
    actual=parse(rhs).subs(u,exponent);row['checks'].append({'block':j,'rhs':rhs,'passed':eq(actual,target)})
   except Exception as ex:row['unparsed_source_steps'].append({'rhs':rhs,'error':str(ex)})
 results.append(row)
save('solution-stages.json',results)
source=json.load(open('../source/source.json'))['material']['kp'];srcs=source[':knowledge-point/questions'];replays=json.load(open('source-replays.json'));fidelity=[]
for r in replays:
 q=next(q for q in srcs if q[':question/math-academy-id']==r['generation']['template']);sourceprompt=q[':question/problem'];generated=r['question'][':question/problem'];base={'question':{':question/problem':sourceprompt}}
 # Input fieldless source still has a complete mathematical function/demand.
 _,v1=expected(base);_,v2=expected(r)
 fidelity.append({'source_id':q[':question/id'],'ma_id':q[':question/math-academy-id'],'prompt_function_and_response_math_equal':eq(v1,v2),'solution_observed':bool(q.get(':question/worked-solution')),'source_field_count':len(q.get(':question/answer-fields',[])),'served_field_count':len(r['question'][':question/answer-fields']),'difficulty_observed':q.get(':question/difficulty'),'served_difficulty':r['question'][':question/difficulty'],'notes':'Source repairs documented in independent source-analysis.json; complete banks verified separately.'})
save('source-replay-results.json',{'supported_replays':fidelity,'canonical_unsupported':'e-728; canonical-gap.json','complete_bank_matches':sum(z['matched'] for z in json.load(open('source-bank-comparison.json'))),'complete_bank_entries':len(json.load(open('source-bank-comparison.json')))})
print('checked solution expressions',sum(len(z['checks']) for z in results),'failures',[(z['index'],v) for z in results for v in z['checks'] if not v['passed']][:4]);print('unparsed',sum(len(z['unparsed_source_steps']) for z in results));print('source math prompts',sum(z['prompt_function_and_response_math_equal'] for z in fidelity))
