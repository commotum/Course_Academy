import collections,json,math,re,sys
from pathlib import Path
import sympy as S
from texmath import parse
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH
def maths(p):return[m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1]for m in MATH.finditer(p)]
X,Y=S.symbols('x y',positive=True);U,V=S.symbols('u v',positive=True);out=[]
for file in['generator-samples.json','staged-samples.json','template-samples.json']:
 for record in json.loads((H/file).read_text()):
  kp=record['knowledge_point'].get('db_id')if isinstance(record['knowledge_point'],dict)else record['knowledge_point']
  if kp not in[17592186172038,17592186172039,17592186172040,17592186172041]:continue
  q=record['question'];g=record['generation'];r={'file':file,'kp':kp,'identity':q[':question/id'],'template':g.get('template'),'checks':[]}
  try:
   formula=next((m for m in maths(q[':question/problem'])if '='in m and('frac'in m or"y'"in m)),None);expr=parse(formula.split('=',1)[1].rstrip('?.'))if formula and'f(x,y)'not in formula else None
   if kp==17592186172038:
    expected=[S.simplify(expr.subs({X:S.Rational(a),Y:S.Rational(b)}))for a,b in g['parameters']['points']];f=q[':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);geometry=g['choice_geometry'];actual=list(map(S.sympify,geometry[a[':answer/value']]));r['checks'].append({'equation_from_prompt':str(expr),'exact_expected_slopes':list(map(str,expected)),'chosen_image_slopes':list(map(str,actual)),'pass':expected==actual});paths=list(geometry)
    # Read actual renderer sidecar, independently of metadata's point list.
    for path in paths:
     data=json.loads(Path(path).with_suffix('.json').read_text());r['checks'].append({'image':path,'sidecar_points':data.get('exact_points',data['points']),'pass':len(data['slopes'])==3 and len(data['points'])==3})
    angles=[]
    for i,p in enumerate(paths):
     for p0 in paths[:i]:
      deltas=[]
      for a,b in zip(geometry[p],geometry[p0]):
       aa=math.pi/2 if a=='oo'else math.atan(float(S.Rational(a)));bb=math.pi/2 if b=='oo'else math.atan(float(S.Rational(b)));delta=abs(aa-bb);deltas.append(min(delta,math.pi-delta))
      angles.append(max(deltas))
    r['min_whole_bank_separation_degrees']=min(angles)*180/math.pi;r['checks'].append({'pass':min(angles)>=math.radians(8)-1e-12})
   elif kp==17592186172040:
    f=q[':question/answer-fields'][0];cid=f[':answer-field/correct'][1];models=g['choice_models'];verdicts=[]
    for aid,m in models.items():
     model=S.sympify(m['expression'],locals={'x':X,'y':Y});both=S.diff(model,X)!=0 and S.diff(model,Y)!=0;truth=not both if g['template'].startswith('impossible')else S.simplify(model-expr)==0;verdicts.append(aid if truth else None)
    r['checks'].append({'expected_correct_ids':[v for v in verdicts if v],'canonical_id':cid,'pass':[v for v in verdicts if v]==[cid]})
   else:
    truths=[]
    for f in q[':question/answer-fields']:
     label=f[':answer-field/key'];cid=f[':answer-field/correct'][1];observed=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==cid)
     if label=='None of the above':truth=not any(truths);proof='Negation of all three independently derived claims'
     else:
      quad=next((i for i,w in enumerate(['first','second','third','fourth'],1)if w+' quadrant'in label),None)
      if quad:signs={1:(1,1),2:(-1,1),3:(-1,-1),4:(1,-1)};sx,sy=signs[quad];regional=S.simplify(expr.subs({X:sx*U,Y:sy*V},simultaneous=True))
      else:
       conditions=[t for t in maths(label)if re.match(r'[xy][<>]',t)];assert len(conditions)==2,conditions;sub={}
       for c in conditions:variable=X if c[0]=='x'else Y;offset=parse(c[2:]);sub[variable]=offset+(U if variable==X else V)*(1 if c[1]=='>'else -1)
       regional=S.simplify(expr.subs(sub,simultaneous=True))
      sign=S.sign(regional);assert sign in[-1,0,1],regional;truth=sign==(-1 if'negative'in label else 1);proof={'regional_expression':str(regional),'exact_sign':str(sign),'domain':'u,v>0, strict open-region inequalities'};truths.append(truth)
     r['checks'].append({'display_statement':label,'truth':truth,'canonical':observed,'proof':proof,'pass':observed==('true'if truth else'false')})
   r['status']='checked'if all(c['pass']for c in r['checks'])else'review'
  except Exception as ex:r['status']='unresolved';r['reason']=str(ex)
  out.append(r)
(H/'slope-model-validation.json').write_text(json.dumps(out,indent=2));print(collections.Counter((r['kp'],r['status'])for r in out));print([r for r in out if r['status']!='checked'][:8])
