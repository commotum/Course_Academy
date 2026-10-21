import os,sys,json,pathlib,re,collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(E.parent/'workspace'));import generator as g
save=lambda n,d:(E/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def field(r):return r['question'][':question/answer-fields'][0]
def applies(r):return r'\frac{' in r['question'][':question/problem'] and r'}{x^{4}}' in r['question'][':question/problem']
def prediction(r):
 return max(field(r)[':answer-field/choices'],key=lambda a:max(map(int,re.findall(r'x\^\{(\d+)\}',a[':answer/value']))))
# Enumerate exactly the allowed quotient p,a,b slots in the demonstrated denominator-4 branch.
records=[g.generate('quotient',a,b,p=p,target=4,seed=584029) for p in [3,4,5] for a in [-3,-2,-1,1,2,3] for b in list(range(-8,0))+list(range(1,9))]
assert len(records)==288 and all(applies(r) for r in records)
save('shortcut-exhaustive.json',records)
sets={'exhaustive':'shortcut-exhaustive.json','raw':'raw-attempts.json','resampled':'sample.json','delivered':'delivery-sample/accepted.json','runner':'runner-batch.json','runner-delivered':'delivery-batch/accepted.json','maximum-count-boundary':'boundary-1000.json'}
results={};grader=json.load(open(E/'grader-input.json'))
for name,path in sets.items():
 rr=[r for r in json.load(open(E/path)) if applies(r)]
 ok=sum(prediction(r)[':answer/id']==field(r)[':answer-field/correct'][1] for r in rr)
 results[name]={'correct':ok,'total':len(rr),'baseline':.2,'sample_file':path,'qids':[r['question'][':question/id'] for r in rr]}
 for i,r in enumerate(rr):grader.append({'label':f'incidental-max-exponent-{name}-{i}','record':r,'checks':[{'submitted_answer_id':prediction(r)[':answer/id'],'expected':'accepted','purpose':'incidental cue: denominator x^4 -> largest visible exponent; no integration or numerator inspection'}]})
# Confirm the published payloads also grade normally, including alternative free entries.
for path in ['delivery-sample/accepted.json','delivery-batch/accepted.json']:
 for i,r in enumerate(json.load(open(E/path))):
  f=field(r);correct=f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'post-delivery complete bank'} for a in f[':answer-field/choices']]
  else:
   ans=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
   checks=[{'submitted':ans,'expected':'accepted','purpose':'post-delivery bare TeX correct'}, {'submitted':'0','expected':'rejected','purpose':'wrong zero primitive'}]
  grader.append({'label':f'{path}:{i}','record':r,'checks':checks})
save('grader-all-input.json',grader)
proof={'strategy':'When prompt quotient denominator is x^4, choose the answer containing the largest visible x exponent. Ignore numerator, coefficient, signs and integration.','implementation':'Select max over each choice of integer matches x^{k}; native grader receives that predicted choice UUID.','results':results,'structural_reason':'The quotient bank always puts the largest polynomial exponent p+2 in candidate 4; the other polynomial exponents are p or p-1, and reciprocal denominators have exponents at most 3. make_data gives denominator x^4 only when candidate 4 is chosen. Thus a denominator cue fixes the answer-producing rank across all allowed p, a and b.','pedagogical_judgment':'The assessed operation is coefficient/exponent integration after quotient expansion. The exponent rank across choices is not an integration law, and the denominator x^4 does not mathematically require the correct polynomial exponent to be the largest listed. The reverse bank construction adds this correlation. In contrast, deriving the reciprocal exponent -3 from x^-4 is an intended mathematical simplification.','source_basis':['tutorial 703 sum and constant factor rule','q-49059 c3b5e67d-32a5-5a89-860d-1eeac5fbca6e'], 'repair':'Within each recognizable denominator profile, vary eligible primitive/distractor roles so the correct answer is not identified by a fixed exponent or coefficient rank. Preserve quotient simplification, two power integrals, and source replay.'}
save('shortcut-results.json',proof)
print(json.dumps({'results':{k:{a:b for a,b in v.items() if a!='qids'} for k,v in results.items()},'grader_records':len(grader)}))
