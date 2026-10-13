"""Parent complete banks and individual displayed triangle-area stages."""
import importlib.util,json,re,hashlib
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186105905
def rnd(e,d):return format(Decimal(str(s.N(e,60))).quantize(Decimal(10)**-d,rounding=ROUND_HALF_UP),f'.{d}f')
def load(path,name):
 sp=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g);return g
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','quadrilateralg');orig=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];counts=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,fieldless=0)
 for c in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  q0=next(q for q in orig if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));q=g.generate(c.get('level','moderate'),template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile')))['question'];assert q[':question/problem']==q0[':question/problem'];counts['prompts']+=1
  for key in (':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in q0)
   if key in q and key!=':question/answer-fields':assert q[key]==(q0[key].get(':db/ident') if isinstance(q0[key],dict) else q0[key])
  counts['solutions']+=(':question/worked-solution' in q0)
  if ':question/answer-fields' not in q0:counts['fieldless']+=1;continue
  for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);counts['fields']+=1;counts['values']+=len(f[':answer-field/choices'])
   if ':answer-field/correct' in f:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];counts['keys']+=1
 stats=dict(records=0,printed_triangle_inputs=0,half_product_rows=0,rounded_component_rows=0,rounded_sum_rows=0,choices=0,complete_method_banks=0,geometric_side_labels=0,geometric_angle_labels=0)
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);para='parallelogram' in q[':question/problem'];inputs=[];areas=[];rounded=[]
  for block in blocks[:-1]:
   pattern=r'\\frac\{1\}\{2\}(?:\\cdot )?(?:\(([\d.]+)\)\(([\d.]+)\)|([\d.]+)\\cdot ([\d.]+)\\cdot )\\operatorname\{sin\}⁡?\{([\d.]+)\}'
   m=re.search(pattern,block);assert m,block;a,b=s.Rational(m[1] or m[3]),s.Rational(m[2] or m[4]);theta=s.Rational(m[5]);T=a*b*s.sin(s.pi*theta/180)/2;inputs.append((a,b,theta));areas.append(T);stats['printed_triangle_inputs']+=3
   half=re.search(r'&\s*=([\d.]+)\\cdot \\operatorname\{sin\}⁡?\{([\d.]+)\}',block);assert half and s.Rational(half[1])==a*b/2 and s.Rational(half[2])==theta;stats['half_product_rows']+=1
   approx=re.search(r'&\s*(?:≈|\\approx)\s*([\d.]+(?:\\,\d+)?)',block);assert approx,block;display=approx[1].replace(r'\,','').rstrip('.,');places=len(display.split('.')[1]);assert display==rnd(T,places),(block,T,display);rounded.append(s.Rational(display));stats['rounded_component_rows']+=1
  assert len(areas)==(1 if para else 2);total=2*areas[0] if para else sum(areas);display_total=2*rounded[0] if para else sum(rounded)
  # Check the actual addition/doubling row's operands individually, beyond the
  # final sum; equal and opposite component errors cannot conceal wrong inputs.
  last=blocks[-1];op=re.search(r'&\s*(?:≈|=)\s*([\d.]+(?:\\,\d+)?)(\+|\\cdot )([\d.]+(?:\\,\d+)?)',last);assert op,last;left=s.Rational(op[1].replace(r'\,',''));right=s.Rational(op[3].replace(r'\,',''));assert [left,right]==([2,rounded[0]] if para else rounded)
  final=list(re.finditer(r'&\s*(?:≈|\\approx)\s*([\d.]+(?:\\,\d+)?)',last))[-1][1].replace(r'\,','').rstrip('.,');assert s.Rational(final)==display_total;stats['rounded_sum_rows']+=1
  digits=1 if 'nearest tenth' in q[':question/problem'] else 0;answer=rnd(total,digits);f=q[':question/answer-fields'][0];vals=[a[':answer/value'] for a in f[':answer-field/choices']]
  for a in f[':answer-field/choices']:assert (a[':answer/value']==answer)==(a[':answer/id']==f[':answer-field/correct'][1]);stats['choices']+=1
  if len(vals)>1:
   a,b,theta=inputs[0];expected=[rnd(e,digits) for e in ([total,areas[0],a*b,2*a*b,a*b/2] if para else [total,*areas,2*total,s.Abs(areas[0]-areas[1])])];assert sorted(vals)==sorted(expected) and len(set(vals))==5;stats['complete_method_banks']+=1
  path=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]);spec=json.loads(path.with_suffix('.json').read_text());assert hashlib.sha256(path.read_bytes()).hexdigest()==spec['png_sha256'];verts=spec['vertices'];labels=spec['side_labels'];angles=spec['angle_labels'];assert len(labels)==(2 if para else 4)
  # Label values are matched to the exact inputs actually printed in the
  # solution; coordinates independently establish lengths and included angles.
  assert sorted(s.Rational(str(v)) for _,_,v in labels)==sorted(v for a,b,t in inputs for v in (a,b))
  for U,V,value in labels:
   P,Q=verts[U],verts[V];length=((P[0]-Q[0])**2+(P[1]-Q[1])**2)**.5;assert abs(length-float(value))<1e-8;stats['geometric_side_labels']+=1
  assert sorted(s.Rational(str(v)) for _,v in angles)==sorted(t for a,b,t in inputs)
  for vertex,shown in angles:
   idx='ABCD'.index(vertex);A=verts[vertex];B=verts['ABCD'[(idx-1)%4]];C=verts['ABCD'[(idx+1)%4]];u=[B[j]-A[j] for j in (0,1)];v=[C[j]-A[j] for j in (0,1)];import math;actual=math.degrees(math.acos(sum(u[j]*v[j] for j in (0,1))/(math.hypot(*u)*math.hypot(*v))));tolerance=.500001 if float(shown).is_integer() else .050001;assert abs(actual-shown)<tolerance,(path,vertex,actual,shown);stats['geometric_angle_labels']+=1
  solution_path=Path(re.findall(r'!\[\]\((.*?)\)',sol)[0]);other=json.loads(solution_path.with_suffix('.json').read_text());assert other['vertices']==verts and other['diagonal'] in ('AC','BD');assert spec['diagonal']==(other['diagonal'] if ':question.difficulty/easy'==q[':question/difficulty'] else None)
  stats['records']+=1
 out=dict(status='passed',kp_id=K,source=counts,readback=stats,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
