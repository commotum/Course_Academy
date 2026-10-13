"""Root actual inverse maps, full coordinate rewrites, minors and answer banks."""
import sys,re,json,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent

def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'spatial-jacobian-readback.py','reader');x,y,z=p.x,p.y,p.z;u,v,w=p.u,p.v,p.w
n=dict(records=0,choices=0,whole_banks=0,partial_rows=0,cofactor_minors=0,determinant_rows=0,coordinate_rows=0,reciprocal_rows=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,known_raw_minor_errors=0,known_raw_label_errors=0,cubic_sign_checks=0)
def simplify(expr,sid,raw=False):
 if sid=='q-39300':return s.simplify(s.refine(expr,s.Q.positive(y)))
 if sid=='q-161806' or sid=='q-161807' and not raw:
  a,b,c=s.symbols('xpos ypos zpos',positive=True);return s.simplify(expr.subs({x:a,y:b,z:c},simultaneous=True))
 return s.simplify(expr)
def same(a,b,sid,raw=False):return simplify(a-b,sid,raw)==0

def real_fractional(expr):
 return expr.replace(lambda q:q.is_Pow and q.exp.is_Rational and q.exp.q==3,lambda q:s.real_root(q.base,3)**q.exp.p)

def check(rec,olds):
 q=rec['question'];g=rec['generation'];sid=g.get('source_id');raw=g['profile']=='observed';F=p.components(q[':question/problem'],'uvw');J=s.Matrix(F).jacobian((x,y,z));det=J.det();back={u:F[0],v:F[1],w:F[2]};shown=p.partials(q[':question/worked-solution'],'uvw','xyz');assert all(same(a,b,sid,raw) for a,b in zip(shown,J));sol=q[':question/worked-solution'];section=sol.split('Therefore,',1)[1];block=p.displays(section)[0];arr=p.leaf_arrays(block);numeric=[a['matrix'] for a in arr if not a['formal']];assert numeric and numeric[0]==J
 # Coordinate scaling can be factored out of the cofactor arrays explicitly.
 if sid:
  original=p.components(olds[sid][':question/problem'],'uvw');baseJ=s.Matrix(original).jacobian((x,y,z));scales=[s.simplify(a/b) for a,b in zip(F,original)];assert all(v.is_Integer and v>0 for v in scales)
  for (_,M) in [(a['span'],a['matrix']) for a in arr if not a['formal']][1:]:
   candidates=[A.minor_submatrix(i,j) for A in (J,baseJ) for i,j in itertools.product(range(3),repeat=2)]
   if not any(M==A for A in candidates):assert raw and sid=='q-161807';n['known_raw_minor_errors']+=1
  scale=scales[0]
 else:scale=J[0,0]
 rows=p.teaching_rows(block)
 for row in rows[1:]:rhs=row.split('=',1)[1].replace('&','').strip();assert same(p.scalar(rhs),det,sid,raw),(sid,row,det)
 # Here prose component definitions, including their output-coordinate labels.
 if 'Here, we have' in sol:
  here=p.displays(sol.split('Here, we have',1)[1])[0];parts=re.split(r'\\,',here.strip().rstrip('.'));assert len(parts)==3
  labels=[q.split('=',1)[0] for q in parts]
  if labels!=['u(x,y,z)','v(x,y,z)','w(x,y,z)']:assert raw and sid=='q-39300';n['known_raw_label_errors']+=1
  assert all(same(p.scalar(part.split('=',1)[1]),actual,sid,raw) for part,actual in zip(parts,F))
 f=q[':question/answer-fields'][0];vs=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vs)==5
 def equal_answer(a,b):
  delta=(a-b).subs(back,simultaneous=True)
  if sid=='q-161807' and raw:
   positive={x:s.Symbol('X',positive=True),y:s.Symbol('Y',positive=True),z:s.Symbol('Z',positive=True)}
   return s.simplify(delta.subs(positive))==0
  return same(delta,0,sid,raw)
 assert all(not equal_answer(a,b) for i,a in enumerate(vs) for b in vs[:i]);hits=[i for i,a in enumerate(vs) if equal_answer(a,1/det)];assert len(hits)==1 and f[':answer-field/choices'][hits[0]][':answer/id']==f[':answer-field/correct'][1]
 if g['eligible_for_learning']:
  expected=[1/det,det,-1/det,1,1/(scale*det)] if q[':question/difficulty'].endswith('/easy') else [1/det,det,-1/det,scale/det,1/(scale*det)]
  mapped=[a.subs(back,simultaneous=True) for a in vs];assert all(sum(same(a,b,sid,raw) for a in mapped)==1 for b in expected)
 tail=sol.split('Therefore,',1)[1];blocks=p.displays(tail)
 for display in blocks[1:]:
  reciprocal=('∂(x,y,z)' in display or r'\partial(x,y,z)' in display);target=1/det if reciprocal else det
  for row in p.teaching_rows(display):
   if '=' not in row:continue
   left,right=row.replace('&','').split('=',1)
   if '∂' in right or r'\partial' in right:continue
   value=p.scalar(right).subs(back,simultaneous=True)
   if sid=='q-161807' and raw:
    original=p.scalar(right)
    for signs in itertools.product((-1,1),repeat=3):
     sub={x:signs[0]*2,y:signs[1]*3,z:signs[2]*4};mapped={a:b.subs(sub) for a,b in back.items()};actual=real_fractional(original).subs(back,simultaneous=True).subs(sub);want=target.subs(sub);assert s.simplify(actual-want)==0,(sid,row,signs,actual,want);n['cubic_sign_checks']+=1
   else:assert same(value,target,sid,raw),(sid,row,value,target)
   n['reciprocal_rows' if reciprocal else 'coordinate_rows']+=1
 n['records']+=1;n['choices']+=5;n['whole_banks']+=1;n['partial_rows']+=9;n['cofactor_minors']+=len(numeric)-1;n['determinant_rows']+=len(rows)-1
if __name__=='__main__':
 kp=17592186129269;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');source=json.load(open(D/'source.json'));assert source==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c.get('level',c.get('difficulty')),parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(rec,olds);q=rec['question'];o=olds[c['source_id']]
  assert q[':question/problem']==o[':question/problem'] and q[':question/worked-solution']==o[':question/worked-solution'];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert val==of[':answer-field/correct'][':answer/value'];n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=1;n['source_refs']+=1
 for item in json.load(open(D/'review.json')):check(item.get('record',item),olds)
 for lv in ('easy','moderate','hard'):
  for seed in range(10):check(g.generate(lv,seed=770000+seed),olds)
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
