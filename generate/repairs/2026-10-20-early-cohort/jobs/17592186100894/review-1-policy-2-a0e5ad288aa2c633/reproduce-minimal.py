"""Strict independent shortcut regression. Exit 1 demonstrates the defect."""
from auditlib import *
from collections import Counter
r=g.generate('easy',492800,'q-104065',{'h':1,'a':4,'c':'0'})
save('minimal-failure.json',[r])
opts=field(r)[':answer-field/choices']; _,(_,ordinate)=prompt_data(r)
coeffs=[S.expand(explicit(r,a[':answer/value'])-S.log(S.sin(x-1))).coeff(x,2) for a in opts]
repeats=[v for v,n in Counter(coeffs).items() if n>1]
qualifies=simplify(ordinate/S.pi**2).is_Rational is True and len(repeats)==1
indices=[i for i,v in enumerate(coeffs) if v==repeats[0]] if qualifies else []
prediction=min(indices,key=lambda i:len(opts[i][':answer/value'])) if indices else None
success=prediction is not None and opts[prediction][':answer/id']==field(r)[':answer-field/correct'][1]
save('minimal-regression-result.json',{'seed':492800,'parameters':r['generation']['parameters'],'qualifies':qualifies,'repeated_coefficients':list(map(str,repeats)),'predicted_value':opts[prediction][':answer/value'] if prediction is not None else None,'shortcut_success':success,'expected':'No reliable incidental answer-bank shortcut','actual':'Reliable repeated-coefficient/shortest-expression cue'})
assert not success, 'Incidental bank cue selects the correct answer without solving the IVP'
