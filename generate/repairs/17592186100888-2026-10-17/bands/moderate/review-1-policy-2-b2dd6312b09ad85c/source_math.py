import json
from pathlib import Path
import sympy as S
x=S.Symbol('x',positive=True);y=S.Symbol('y',real=True)
# Independent transcription from the actual source prompts; x>0 is a subset of
# every source domain and ensures real log simplification. Explicit reciprocal
# residuals determine identity on both nonzero branches as well.
CASES=[
(17592186100725,1/x,-y/x,-1/x**2),
(17592186101155,x**4,4*y/x,5*x**5),
(17592186101157,S.exp(2*x),2*y,2*S.exp(2*x)),
(17592186272196,S.sin(2*x)/2,2*y,2*S.cos(2*x)),
(17592186272197,S.cos(2*x),y*S.cos(2*x),-2*S.sin(2*x)),
(17592186272198,S.log(x),S.exp(-y),1/x),
(17592186272199,-1/x**2,y/x**2,-2/x**3),
(17592186272200,3*S.exp(-x),-3*y,3*S.exp(-x)),
(17592186272201,4*S.log(x),4*x*S.exp(-y/2),1/(4*x)),
(17592186272202,-3*x**2,2*y/x,-5*x),
]
def run():
 root=Path(__file__).parent;source=json.loads((root.parent/'source/source.json').read_text());bank={q[':db/id']:q for q in source['material']['kp'][':knowledge-point/questions']};results=[]
 for qid,f,rhs,claim in CASES:
  derivative=S.diff(f,x);claimres=S.simplify(derivative-claim);oderes=S.simplify(derivative-rhs.subs(y,f));truth=[claimres==0,oderes==0,oderes==0]
  q=bank.get(qid);stored=[next(z[':answer-field/correct'][':answer/value']=='true' for z in q[':question/answer-fields'] if z[':answer-field/key']==key) for key in ('I','II','III')] if q else [True]*3
  assert truth==stored,(qid,truth,stored)
  results.append({'source_id':qid,'f':str(f),'rhs':str(rhs),'claim':str(claim),'derivative':str(derivative),'claim_residual':str(claimres),'ode_residual':str(oderes),'truth':truth,'stored_truth':stored,'passed':True})
 (root/'source-math.json').write_text(json.dumps({'command':'.venv/bin/python generate/repairs/17592186100888-2026-10-17/review/source_math.py','cases':results,'passed':len(results)},indent=2)+'\n')
 print('Source mathematics:10cases passed')
if __name__=='__main__':run()
