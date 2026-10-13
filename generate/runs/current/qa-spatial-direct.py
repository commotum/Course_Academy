"""Root complete 3D direct Jacobian banks/prose/partials/matrices/stages."""
import sys,re,json,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent

def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'spatial-jacobian-readback.py','spatial');u,v,w=p.u,p.v,p.w
n=dict(records=0,choices=0,whole_banks=0,partial_rows=0,cofactor_minors=0,determinant_rows=0,source_banks=0,source_values=0,source_distractors=0,source_refs=0,source_prose_sequences=0,raw_exact_prompts=0,raw_exact_solutions=0)
def expected(name,F,J,D):
 if name=='sparse_trig':
  A=J[0,1];B=s.expand(F[1]).coeff(u**2);d=s.expand(F[2]).coeff(v*w);return [D,-D,D/2,-2*A*B*d*u*w,-2*B*d*u*v]
 if name=='sparse_exp':
  A=s.simplify(J[0,0]/s.exp(w));B=-J[1,0];C=J[1,2];d=-J[2,1];return [D,-D,A*d*C*s.exp(w),A*d*B*u*s.exp(w),A*s.exp(w)*(C+B*u)]
 if name=='sparse_square':
  A=s.expand(F[0]).coeff(u**2);d=J[1,2];e=-J[2,1];return [D,-D,2*A*e*u,2*A*d*e*v,0]
 if name=='log_product':
  A=s.simplify(J[0,2]*w);B=J[1,0];d=s.simplify(J[2,0]/v);return [D,-D,A*B*d/w,A*B*d*u/v,0]
 if name=='rotation':return [D,-D,D*s.cos(p.p.k)**2,D*s.sin(p.p.k)**2,0]
 if name=='polynomial_column':
  B=J[0,2];C=s.expand(F[1]).coeff(u**3);d=J[1,1];e=s.expand(F[2]).coeff(u*v);return [D,-D,B*e*(C*u**3-d*v),B*e*(3*C*u**3+d*v),3*B*C*e*u**3]
 if name=='polynomial_mixed':
  A=s.expand(F[0]).coeff(u**2);B=s.expand(F[0]).coeff(v*w);C=-s.expand(F[1]).coeff(u*v);d=s.expand(F[2]).coeff(v**2)
  return [D,-D,2*A*C*u**2+2*B*C*d*v**3+B*C*v*w,2*A*C*u**2-2*B*C*d*v**3+B*C*v*w,2*A*C*u**2-B*C*v*w]
 if name=='linear_offdiag':
  P=J[0,1]*J[1,2]*J[2,0];Q=J[0,2]*J[1,0]*J[2,1];return [D,-D,P-Q,P,Q]
 if name=='symbolic_diagonal':return [D,-D,s.trace(J),-s.trace(J),0]
 assert name=='spherical';K=s.simplify(D/(u*u*s.sin(v)));return [D,-D,K*u*s.sin(v),K*u*u*s.sin(v)**3,K*u*u*s.sin(v)*s.cos(v)**2]

def check(rec):
 q=rec['question'];g=rec['generation'];F=p.components(q[':question/problem']);J=s.Matrix(F).jacobian((u,v,w));D=s.trigsimp(s.expand(J.det()));shown=p.partials(q[':question/worked-solution'],'xyz','uvw');assert all(p.same(a,b) for a,b in zip(shown,J));st=p.determinant_stages(q[':question/worked-solution'],J)
 # Every source's complete formal coordinate/matrix introduction is preserved.
 fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];vs=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vs)==5 and all(not p.same(a,b) for idx,a in enumerate(vs) for b in vs[:idx]);valid=[idx for idx,z in enumerate(vs) if p.same(z,D)];assert len(valid)==1 and f[':answer-field/choices'][valid[0]][':answer/id']==f[':answer-field/correct'][1]
 assert g['evidence_only']==g['bank_profile'].endswith('-observed') and g['eligible_for_learning']==(not g['evidence_only'])
 if g['eligible_for_learning']:assert all(sum(p.same(z,e) for z in vs)==1 for e in expected(g['template'],F,J,D))
 n['records']+=1;n['choices']+=5;n['whole_banks']+=1;n['partial_rows']+=9;n['cofactor_minors']+=st['cofactor_minors'];n['determinant_rows']+=st['determinant_rows']
if __name__=='__main__':
 kp=17592186129271;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');source=json.load(open(D/'source.json'));assert source==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 def prose(text):return re.sub(r'\$\$.*?\$\$','<DISPLAY>',text,flags=re.S)
 for c in json.load(open(D/'source-cases.json')):
  lv=c.get('level',c.get('difficulty'));rec=g.generate(lv,parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(rec);q=rec['question'];o=olds[c['source_id']]
  assert q[':question/difficulty']==o[':question/difficulty'][':db/ident'];assert prose(q[':question/problem'])==prose(o[':question/problem']);assert prose(q[':question/worked-solution'])==prose(o[':question/worked-solution'])
  oldF=p.components(o[':question/problem']);newF=p.components(q[':question/problem']);assert all(p.same(a,b) for a,b in zip(oldF,newF));oldJ=s.Matrix(oldF).jacobian((u,v,w));oldst=p.determinant_stages(o[':question/worked-solution'],oldJ);newst=p.determinant_stages(q[':question/worked-solution'],oldJ);assert oldst==newst
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']]
  for a in of[':answer-field/choices']:assert sum(p.same(p.scalar(a[':answer/value']),v) for v in vals)==1
  newcorrect=next(p.scalar(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert p.same(newcorrect,p.scalar(of[':answer-field/correct'][':answer/value']))
  n['source_banks']+=1;n['source_values']+=5;n['source_distractors']+=4;n['source_refs']+=1;n['source_prose_sequences']+=1;n['raw_exact_prompts']+=int(q[':question/problem']==o[':question/problem']);n['raw_exact_solutions']+=int(q[':question/worked-solution']==o[':question/worked-solution'])
 for item in json.load(open(D/'review.json')):check(item.get('record',item))
 for lv in ('easy','moderate','hard'):
  for seed in range(15):check(g.generate(lv,seed=330000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
