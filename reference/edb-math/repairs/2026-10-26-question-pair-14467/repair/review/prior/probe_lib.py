from review_lib import *
def predictions(rec):
 cs=rec['question'][':question/answer-fields'][0][':answer-field/choices'];values=[line(c[':answer/value']) for c in cs];slopes=[m for m,b in values];intercepts=[b for m,b in values]
 raw=[coeff(c[':answer/value'].split('=')[0]) for c in cs]
 strategies={**{'position-'+str(i+1):i for i in range(5)}}
 for name,vals in [('slope',slopes),('intercept',intercepts),('printed-length',[len(c[':answer/value']) for c in cs]),('abs-x-coefficient',[abs(x[0]) for x in raw]),('abs-y-coefficient',[abs(x[1]) for x in raw])]:
  strategies['minimum-'+name]=min(range(5),key=lambda i:vals[i]);strategies['maximum-'+name]=max(range(5),key=lambda i:vals[i])
  ordered=sorted(range(5),key=lambda i:vals[i]);strategies['median-'+name]=ordered[2]
 for sign in (-1,1):
  for name,vals in [('slope',slopes),('intercept',intercepts),('printed-x-coefficient',[x[0] for x in raw]),('printed-y-coefficient',[x[1] for x in raw])]:
   inds=[i for i,v in enumerate(vals) if v*sign>0];strategies['first-'+str(sign)+'-'+name]=inds[0] if inds else 0
 for name,vals in [('slope',slopes),('intercept',intercepts),('printed-x-coefficient',[x[0] for x in raw]),('printed-y-coefficient',[x[1] for x in raw])]:
  freq=Counter(vals);strategies['modal-'+name]=max(range(5),key=lambda i:freq[vals[i]])
 strategies['opposite-slope-counterpart']=next((i for i,m in enumerate(slopes) if -m in slopes),0)
 strategies['fractional-slope']=next((i for i,m in enumerate(slopes) if m.denominator>1),0)
 strategies['integer-slope']=next((i for i,m in enumerate(slopes) if m.denominator==1),0)
 # This combines two bank-only modes without consulting any target or catalog of keys.
 freqA=Counter(x[0] for x in raw);freqB=Counter(x[1] for x in raw);strategies['intersect-modal-coefficients']=max(range(5),key=lambda i:freqA[raw[i][0]]+freqB[raw[i][1]])
 return strategies