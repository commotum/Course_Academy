"""Usage: python -B nearest_zero_regression.py [candidate-records.json]
Independent conditional cue regression. Default regenerates seeds 764300..764314
against the current package. Explicit file evaluates those complete records.
Exit 1 flags a reproducible above-chance cue within a sufficiently sampled template;
a single success is reported but never, alone, treated as statistical proof.
"""
from audit_helpers import *
from math import comb

def probe(r):
 f=field(r)
 if not f[':answer-field/type'].endswith('/radio'):return None
 values=[latex(a[':answer/value']) for a in f[':answer-field/choices']]
 if not all(v.is_Rational for v in values):return None
 mag=[abs(v) for v in values];m=min(mag)
 if mag.count(m)!=1:return None
 i=mag.index(m);choice=f[':answer-field/choices'][i]
 return {'question_id':r['question'][':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'parameters':r['generation']['parameters'],'predicted_answer':choice[':answer/value'],'prediction_uses':'Only displayed choice magnitudes; function and target are ignored.','success':choice[':answer/value']==correct(r)}

def evaluate(records):
 rows=[p for r in records if (p:=probe(r)) is not None];groups={}
 for row in rows:
  group=groups.setdefault(row['template'],{'correct':0,'total':0,'baseline':0.2});group['total']+=1;group['correct']+=int(row['success'])
 for v in groups.values():
  n=v['total'];k=v['correct'];v['binomial_tail']=sum(comb(n,i)*.2**i*.8**(n-i) for i in range(k,n+1));v['flag']=n>=15 and k/n>=.5 and v['binomial_tail']<.01
 return {'results':rows,'groups':groups,'failed':any(v['flag'] for v in groups.values()),'limits':'Diagnostic for this specific conditional cue, not a universal diversity quota. Short files report witnesses without statistical certification. The holdout seeds were selected after the initial cue was observed; no failed draw is discarded.'}
if __name__=='__main__':
 if len(sys.argv)>1:target=pathlib.Path(sys.argv[1]);rs=json.load(open(target));name=target.parent.name+'-'+target.stem
 else:
  rs=[g.generate('easy',seed=764300+i,template='slope_sqrt_radio') for i in range(15)];name='fresh';save('nearest-zero-fresh-records.json',rs)
 result=evaluate(rs);result['command']=' '.join(sys.argv);result['records']=rs;save('nearest-zero-'+name+'.json',result);print(json.dumps(result['groups']));sys.exit(int(result['failed']))
