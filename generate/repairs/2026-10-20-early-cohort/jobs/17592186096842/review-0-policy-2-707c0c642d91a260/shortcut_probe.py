"""Usage: python shortcut_probe.py [candidate-records.json]. Fails if a radio bank
leaks its answer via coefficient times answer-spacing; writes complete evidence.
The strategy reads the displayed coefficient and choices, never the stored key.
"""
from audit_helpers import *
# Helpers use argv[1] as optional package path; for this CLI the package is fixed.
def probe(r):
 f=field(r)
 if not f[':answer-field/type'].endswith('/radio'):return None
 prompt=r['question'][':question/problem'].replace('y =','y='); y=latex(prompt.split('$y=',1)[1].split('$')[0].rstrip(',.'))
 # Restrict to linear root/reciprocal tasks; sum/quadratic require different analysis.
 if y.is_Add:return None
 inner=[p.base for p in s.preorder_traversal(y) if isinstance(p,s.Pow) and p.exp in [s.Rational(1,2),-s.Rational(1,2)]]
 if len(inner)!=1 or s.Poly(inner[0],X).degree()!=1:return None
 a=s.Poly(inner[0],X).coeff_monomial(X);recip=any(p.exp==-s.Rational(1,2) for p in s.preorder_traversal(y) if isinstance(p,s.Pow))
 vals=[latex(c[':answer/value']) for c in f[':answer-field/choices']]
 # Common positive denominator allows ordering scalar coefficients; a domain
 # witness orders these symbolic options only. Slope options are already numbers.
 witness=(1-inner[0].subs(X,0))/a
 vals=sorted(vals,key=lambda v:float(v.subs(X,witness)))
 diffs=[s.simplify(vals[i+1]-vals[i]) for i in range(len(vals)-1)]
 equal=all(s.simplify(d-diffs[0])==0 for d in diffs)
 prediction=s.simplify((-1 if recip else 1)*a*diffs[0])
 correct_value=latex(correct(r));success=s.simplify(s.powdenest(prediction,force=True)-s.powdenest(correct_value,force=True))==0
 return {'question_id':r['question'][':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'parameters':r['generation']['parameters'],'prompt':prompt,'common_spacing':str(diffs[0]),'arithmetic_progression':equal,'visible_coefficient':str(a),'prediction':str(prediction),'stored_correct':correct(r),'success':bool(equal and success),'used_evaluation_point':False,'used_radicand_constant':False}
if __name__=='__main__':
 target=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'batch-records.json'
 records=json.load(open(target));result=[p for r in records if (p:=probe(r)) is not None]
 out=ROOT/('shortcut-'+target.parent.name+'-'+target.stem+'.json');out.write_text(json.dumps({'input':str(target),'command':f'{sys.executable} -B {__file__} {target}','records':records,'results':result,'correct':sum(x['success'] for x in result),'total':len(result),'baseline':0.2},indent=2))
 print(str(out.name),sum(x['success'] for x in result),len(result))
 sys.exit(1 if any(x['success'] for x in result) else 0)
