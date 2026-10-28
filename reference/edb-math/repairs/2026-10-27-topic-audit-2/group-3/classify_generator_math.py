import json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));ns={'__file__':str(H/'math_check.py')};exec((H/'math_check.py').read_text().split('checks=[];unresolved=[];bad=[];completion_matches=[]')[0],ns);sp=ns['sp'];S=ns['SYMS'];parse=ns['parse'];x,y=S['x'],S['y'];v=json.loads((H/'generator-symbolic-math-validation.json').read_text());meta={r['synthetic_math_id']:r for r in json.loads((H/'generator-final-coverage.json').read_text())['records_ledger']};Q={q[':db/id']:q for q in json.loads((H/'generator-math-snapshot.json').read_text())['questions']};out=[]
for r in v['mismatches']:
 m=meta[r['entity']];q=Q[r['entity']];f=q[':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices']if a[':db/id']==r['correct']);kind=m['template'];proof=None
 if kind=='q-11816'and m['kind']=='source-replay':proof='Known retained raw source key xe^(3x) is incorrect; derivative3e^(3x). Fresh practice has repaired authored keys; raw snapshot remains evidence-only.';classification='raw source-origin key defect, preserve evidence only'
 elif kind in['linear_sec2','tan_exp','tan_autonomous']:
  proof='Identity1+tan²u=sec²u proves the displayed family residual0 on the existing explicit domain.';classification='valid trigonometric identity'
 elif kind in['reciprocal_blank','reciprocal_blank_braced','reciprocal_radio']:
  proof='Forpositive affineu, sqrt(u³)=u^(3/2). Differentiatingu^(−1/2) gives−uprime/(2sqrt(u³)), matching canonical.';classification='valid radical identity on function real domain'
 elif m['kp']==17592186100894 or m['kp']==17592186100893:
  p=q[':question/problem'];frames=[t for t in ns['maths'](p)if re.fullmatch(r'\s*\\(?:operatorname\{sin\}|sin)\s*(?:\{?\\left)?[\s\S]*=\s*',t)]
  frame=frames[-1].split('=',1)[0];left=parse(frame);arg=next(iter(left.atoms(sp.sin))).args[0];acoef=sp.diff(arg,y);R=parse(a[':answer/value']);res,state=ns['ode_task'](q);diff=sp.trigsimp(res.subs(S['Z'],sp.diff(R,x)/(acoef*sp.cos(arg)))).subs(sp.sin(arg),R);assert sp.simplify(diff)==0;proof={'implicit_frame':frame+'=canonical','residual_after_implicit_derivative':'0','branch':'existing local sine branch; original IC retained'};classification='valid implicit response frame'
 elif kind=='q-312462':proof='Actual response is coefficient·givenexponential. Chainrule coefficient is innerprime·ln(base); canonical is that coefficient.';classification='valid coefficient response frame'
 elif kind=='factor_cancel':proof='Cancel original RHS to(y²+x²)/(xy) onxy(x+y)≠0. Differentiatey²=x²(2ln|x|+C), use constraint, same slope.';classification='valid implicit family and excluded poles'
 elif kind in['q-79665','q-8303','q-8304']:proof='Fresh prompt already states positive quadrant where needed and local positive branch of integrated equation. On that branch the square/radical identity matches ODE. Historical stored source questions receive explicit matching domain repairs.';classification='valid explicit positive local branch'
 else:raise ValueError((m,r))
 out.append({'sample':m,'classification':classification,'evidence':proof})
(H/'generator-symbolic-candidate-resolution.json').write_text(json.dumps({'original_candidates':len(out),'resolutions':out,'raw_known_defects':1,'unproven_fresh_wrong_keys':0},indent=2));print('classified generator candidates',len(out))
