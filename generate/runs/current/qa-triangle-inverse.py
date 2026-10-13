"""Parent source/actual-expression/whole-bank and inverse triangle geometry QA."""
import importlib.util,json,re,hashlib,math
from pathlib import Path
import sympy as s
from PIL import Image
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186105904
sp=importlib.util.spec_from_file_location('inverseparser',R/'qa-gradients.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
def scalar(t):return p.scalar(t.replace(r'^{\circ}','').replace('^{∘}','').strip().rstrip('.,').replace('cm','').replace('mm','').replace(r'\cancel',''))
def quantity(text):
 m=re.search(r'area .*? is \$([^$]+)',text);assert m,text;t=re.split(r'cm|mm|\\,|\\text|\{\\text',m[1])[0].rstrip('{');return scalar(t)
def eq(a,b):return s.simplify(a-b)==0
def expression(text,b,c,A,theta):
 S=s.sin(s.pi*theta/180);text=text.replace('m∠A',str(theta)).replace(r'\operatorname{sin}⁡A','('+s.latex(S)+')')
 text=re.sub(r'\\operatorname\{sin\}⁡\{(\d+)\}\^\{∘\}',lambda m:'('+s.latex(s.sin(s.pi*int(m[1])/180))+')',text)
 text=re.sub(r'\{(\d+)\}\^\{∘\}',r'\1',text)
 parts=re.split(r'(\\[A-Za-z]+)',text)
 for j in range(0,len(parts),2):parts[j]=parts[j].translate(str.maketrans({'b':'x','c':'y','A':'z'}))
 e=scalar(''.join(parts));return e.subs({p.axes[0]:b,p.axes[1]:c,p.axes[2]:A},simultaneous=True)
def check():
 g=p.load(ROOT/f'generate/scratch/{K}.py','inverseg');orig=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];counts=dict(prompts=0,solutions=0,values=0,keys=0)
 for case in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  q0=next(q for q in orig if case['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));q=g.generate(case.get('level','moderate'),template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile')))['question'];assert q[':question/problem']==q0[':question/problem'];counts['prompts']+=1
  for key in (':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in q0)
   if key in q:assert q[key]==(q0[key].get(':db/ident') if isinstance(q0[key],dict) else q0[key])
  counts['solutions']+=(':question/worked-solution' in q0);f=q[':question/answer-fields'][0];f0=q0[':question/answer-fields'][0];assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);counts['values']+=len(f[':answer-field/choices'])
  if ':answer-field/correct' in f:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];counts['keys']+=1
 stats=dict(records=0,equation_stages=0,choices=0,complete_method_banks=0,raster_edges=0,acute_branches=0)
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];sol=q[':question/worked-solution'];A=quantity(q[':question/problem']);blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);givens=blocks[1];m=re.search(r'AB=(.*?)(?=\\text|\\,|,|\\\\|\\end)',givens);assert m,givens;c=scalar(m[1]);kind='angle' if 'm∠A & ' not in givens else 'side'
  if kind=='angle':
   m=re.search(r'AC=(.*?)(?=\\text|\\,|,|\\\\|\\end)',givens);assert m,givens;b=scalar(m[1]);sine=2*A/(b*c);poss=[t for t in (30,45,60) if eq(s.sin(s.pi*t/180),sine)];assert len(poss)==1;theta=poss[0];answer=s.Integer(theta);assert 'with acute $∠A$' in q[':question/problem'];stats['acute_branches']+=1
  else:
   m=re.search(r'm∠A\s*&\s*=\{(\d+)\}',givens);assert m,givens;theta=int(m[1]);b=s.simplify(2*A/(c*s.sin(s.pi*theta/180)));answer=b
  for row in blocks[-1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
   lhs,rhs=re.split(r'&\s*=',row,maxsplit=1);assert eq(expression(lhs,b,c,A,theta),expression(rhs,b,c,A,theta)),(r['generation']['template'],row,b,c,A,theta);stats['equation_stages']+=1
  f=q[':question/answer-fields'][0];vals=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
  for a,v in zip(f[':answer-field/choices'],vals):assert eq(v,answer)==(a[':answer/id']==f[':answer-field/correct'][1]);stats['choices']+=1
  if f[':answer-field/type'].endswith('/radio'):
   expected=[b,b/2,b*c*c,c,b/c] if kind=='side' else [30,45,60,120,135];assert len(vals)==len(expected) and all(any(eq(v,w) for w in expected) for v in vals) and all(not eq(v,w) for i,v in enumerate(vals) for w in vals[:i]),(kind,vals,expected);stats['complete_method_banks']+=1
  path=Path(re.search(r'!\[\]\(([^)]+)\)',q[':question/problem'])[1]);plot=json.loads(path.with_suffix('.json').read_text());assert hashlib.sha256(path.read_bytes()).hexdigest()==plot['sha256'];P,B,C=[plot['vertices'][v] for v in 'ABC'];assert abs(math.dist(P,B)-float(c))<1e-8 and abs(math.dist(P,C)-float(b))<1e-8;measured=math.degrees(math.acos(sum((B[j]-P[j])*(C[j]-P[j]) for j in (0,1))/(float(b)*float(c))));assert abs(measured-theta)<1e-8;assert abs(float(A)-abs((B[0]-P[0])*(C[1]-P[1])-(B[1]-P[1])*(C[0]-P[0]))/2)<1e-8
  assert eq(scalar(plot['labels']['AB']),c) and (eq(scalar(plot['labels']['AC']),b) if kind=='angle' else plot['labels']['AC'] is None) and plot['labels']['angle']==(theta if kind=='side' else None)
  im=Image.open(path).convert('RGB')
  for pair in ('AB','BC','CA'):
   U,V=[plot['pixel_vertices_bottom_origin'][name] for name in pair]
   for f0 in (.25,.5,.75):
    x=round(U[0]+f0*(V[0]-U[0]));y=round(im.height-1-U[1]-f0*(V[1]-U[1]));assert any(max(im.getpixel((xx,yy)))<100 for xx in range(max(0,x-3),min(im.width,x+4)) for yy in range(max(0,y-3),min(im.height,y+4)));stats['raster_edges']+=1
  stats['records']+=1
 out=dict(status='passed',kp_id=K,source=counts,readback=stats,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
