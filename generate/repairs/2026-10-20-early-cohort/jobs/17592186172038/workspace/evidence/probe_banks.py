import importlib.util,random,math,json
from pathlib import Path
W=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('g',W/'17592186172038.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def score(rows):
 a=[[math.atan(float(x)) for x in r] for r in rows]
 return {'horizontal_count':[sum(x==0 for x in r) for r in rows], 'positive_count':[sum(bool(x>0) for x in r) for r in rows], 'absolute_angle':[sum(abs(x) for x in r) for r in a], 'signed_angle':[sum(r) for r in a], 'distance_to_others':[sum(sum(abs(x-y) for x,y in zip(r,s)) for s in a) for r in a]}
def probes(records):
 out={}
 for t in g.TEMPLATES:
  rs=[r for r in records if r['generation']['template']==t];stats={}
  for r in rs:
   f=r['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];ci=next(i for i,c in enumerate(choices) if c[':answer/id']==f[':answer-field/correct'][1]);rows=[[g.sp.sympify(x) for x in r['generation']['choice_geometry'][c[':answer/value']]] for c in choices]
   for pos in range(5):
    k='position_'+str(pos);st=stats.setdefault(k,[0,0]);st[0]+=ci==pos;st[1]+=1
   for k,values in score(rows).items():
    for which in ('min','max'):
     extreme=(min if which=='min' else max)(values);inds=[i for i,v in enumerate(values) if v==extreme];st=stats.setdefault(k+'_'+which,[0,0]);st[0]+=(1/len(inds) if ci in inds else 0);st[1]+=1
  out[t]={'records':len(rs),'strategies':{k:{'successes':round(v[0],3),'attempts':v[1],'rate':round(v[0]/v[1],3)} for k,v in stats.items()}} if rs else {'records':0}
 return out
if __name__=='__main__':
 records=[];rejections={}
 for t in g.TEMPLATES:
  rng=random.Random(90210);accepted=0;attempts=0
  while accepted<40:
   attempts+=1;p=g.sample('easy',t,rng)
   try:g.validate_parameters('easy',t,p);s,bank=g.banks(t,p,'authored')
   except ValueError:continue
   inds=list(range(5));rng.shuffle(inds);choices=[{':answer/id':str(i),':answer/value':str(i)} for i in inds]
   records.append({'question':{':question/answer-fields':[{':answer-field/choices':choices,':answer-field/correct':[':answer/id',str(bank.index(s))]}]},'generation':{'template':t,'parameters':p,'choice_geometry':{str(i):list(map(str,row)) for i,row in enumerate(bank)}}});accepted+=1
  rejections[t]={'attempts':attempts,'accepted':accepted}
 result={'rejections':rejections,'probes':probes(records)};(W/'evidence/bank-probes-before.json').write_text(json.dumps(result,indent=2))
 for t,v in result['probes'].items():print(t,'highest cue rate',max((x['rate'],k) for k,x in v['strategies'].items()))
