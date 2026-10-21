import json,re,collections,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
load=lambda p:json.loads((R/p).read_text())
def choice(r):
 f=r['question'][':question/answer-fields'][0];return f,f[':answer-field/choices'],f[':answer-field/correct'][1]
def groups(r):
 m=r['generation'];p=m['parameters'];t=m['template'];out=[t]
 if 'trig' in p:out.append(t+'/trig='+p['trig'])
 if 'c' in p:out.append(t+'/c_sign='+('negative' if p['c']<0 else 'positive'))
 return out

def analyze(rs):
 coverage=collections.defaultdict(lambda:collections.Counter());stats=collections.defaultdict(lambda:[0,0,0])
 for r in rs:
  m=r['generation'];p=m['parameters'];t=m['template'];coverage[t]['count']+=1;coverage[t]['missing='+str(m.get('missing_term'))]+=1
  if 'trig' in p:coverage[t]['trig='+p['trig']]+=1
  if 'c' in p:coverage[t]['sign='+('negative' if p['c']<0 else 'positive')]+=1
  f,cs,k=choice(r)
  if not f[':answer-field/type'].endswith('/radio'):continue
  norms=[re.sub(r'\\(?:left|right)|\s|[{}]','',c[':answer/value']) for c in cs]
  predictors={'choose_first':0,'choose_last':len(cs)-1}
  for name,arr in [('tex_length',list(map(len,norms))),('parenthesis_count',[z.count('(') for z in norms]),('plus_count',[z.count('+') for z in norms]),('minus_count',[z.count('-') for z in norms])]:
   for op,fun in [('min',min),('max',max)]:
    extreme=fun(arr);ix=[i for i,z in enumerate(arr) if z==extreme]
    predictors[name+'_'+op]=ix[0] if len(ix)==1 else None
  for group in groups(r):
   for name,i in predictors.items():
    stats[group+'|'+name][2]+=1
    if i is not None:stats[group+'|'+name][1]+=1;stats[group+'|'+name][0]+=cs[i][':answer/id']==k
 return {'coverage':dict(coverage),'probes':[{'subgroup':k.split('|')[0],'strategy':k.split('|')[1],'correct':v[0],'attempts_when_unique':v[1],'total':v[2],'random_baseline':0.2} for k,v in stats.items()]}
rs=load('samples.json');acc=load('delivery/accepted.json');batch=load('runner-batch.json') if (R/'runner-batch.json').exists() else json.loads((R.parent/'samples.json').read_text());data={'raw':analyze(rs),'delivered':analyze(acc),'runner':analyze(batch)}
(R/'distribution-probes.json').write_text(json.dumps(data,indent=2)+'\n')
print('perfect predictors at >=4 attempts, delivered:')
for p in data['delivered']['probes']:
 if p['correct']==p['attempts_when_unique'] and p['correct']>=4:print(p)
print('coverage:',dict(data['delivered']['coverage']))
