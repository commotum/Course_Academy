import collections
from visible_math import matrix,equations
def sign(v):return (v>0)-(v<0)
def correct(r):return r['question'][':question/answer-fields'][0][':answer-field/correct'][1]
def signature(a):return tuple(sign(v) for v in matrix(a[':answer/value'])[0][1:])
def sign_strategy(r):
 # Inspect only signs of first displayed equation and signs of choice top rows.
 # Does not calculate any quotient, inspect other equations or inspect metadata/key.
 row=equations(r['question'][':question/problem'])[0];want=tuple(sign(v)*sign(row[0]) for v in row[1:])
 candidates=[a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if signature(a)==want]
 return candidates[0] if len(candidates)==1 else None

def measure(rs):
 answers=[]
 for r in rs:
  pred=sign_strategy(r);f=r['question'][':question/answer-fields'][0];m=[matrix(a[':answer/value']) for a in f[':answer-field/choices']]
  answers.append({'id':r['question'][':question/id'],'success':pred==correct(r),'prediction':pred,'correct':correct(r),'same_absolute_bank':len({tuple(abs(x) for row in v for x in row) for v in m})==1,'correct_position':next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==correct(r)),'first_pivot_sign':sign(equations(r['question'][':question/problem'])[0][0]),'plan':r.get('generation',{}).get('parameters',{}).get('plan')})
 return {'count':len(rs),'successes':sum(a['success'] for a in answers),'same_absolute_bank':sum(a['same_absolute_bank'] for a in answers),'position_counts':dict(collections.Counter(a['correct_position'] for a in answers)),'conditional':{s:{'count':sum(a['first_pivot_sign']==s for a in answers),'successes':sum(a['success'] for a in answers if a['first_pivot_sign']==s)} for s in (-1,1)},'results':answers}
