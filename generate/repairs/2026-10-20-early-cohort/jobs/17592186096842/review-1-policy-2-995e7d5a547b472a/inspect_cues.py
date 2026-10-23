from audit_helpers import *
from shortcut_probe import probe

def inspect(records):
 details=[]
 for r in records:
  f=field(r)
  if not f[':answer-field/type'].endswith('/radio'):continue
  choices=f[':answer-field/choices']; vals=[latex(c[':answer/value']) for c in choices];key=next(i for i,c in enumerate(choices) if c[':answer/value']==correct(r))
  if any(v.has(X) for v in vals):
   for x in range(-40,41):
    numeric=[v.subs(X,x) for v in vals]
    if all(v.is_real and v.is_finite for v in numeric):break
  else:numeric=vals
  order=sorted(range(5),key=lambda i:float(numeric[i]));abso=sorted(range(5),key=lambda i:abs(float(numeric[i])))
  preds={'first_position':0,'minimum_value':order[0],'median_value':order[2],'maximum_value':order[4],'minimum_absolute':abso[0],'maximum_absolute':abso[4]}
  metrics={'length':[len(c[':answer/value']) for c in choices]}
  if all(v.is_Rational for v in vals):metrics['denominator']=[int(v.q) for v in vals]
  for m,values in metrics.items():
   for tag,fn in [('minimum',min),('maximum',max)]:
    best=fn(values);preds[f'unique_{tag}_{m}']=values.index(best) if values.count(best)==1 else None
  signs=[s.sign(v) for v in numeric];single=[i for i,v in enumerate(signs) if signs.count(v)==1];preds['unique_sign']=single[0] if len(single)==1 else None
  details.append({'question_id':r['question'][':question/id'],'template':r['generation']['template'],'key_index':key,'predictions':preds,'outcomes':{k:(v==key if v is not None else None) for k,v in preds.items()},'spacing':probe(r)})
 groups={}
 for row in details:
  for group in ['overall',row['template']]:
   group=groups.setdefault(group,{})
   for cue,val in row['outcomes'].items():
    cell=group.setdefault(cue,{'correct':0,'total':0,'abstained':0,'baseline':0.2})
    if val is None:cell['abstained']+=1
    else:cell['total']+=1;cell['correct']+=int(val)
 return {'groups':groups,'details':details}
if __name__=='__main__':
 target=pathlib.Path(sys.argv[1]);records=json.load(open(target));results=inspect(records);save('cues-'+target.stem+'.json',{'input':str(target),'results':results})
 print(json.dumps({g:{k:v for k,v in rows.items() if v['correct']>=3 and v['correct']/max(1,v['total'])>=.75} for g,rows in results['groups'].items()}))
