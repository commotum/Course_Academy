"""Root checks extrema averaging and every signed range-transformation stage."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
H=load(R/'qa-sinusoidal-properties.py','h');P=H.p
def scalar(z):return H.read(z.replace(r'^{\circ}',''))
def interval(z):
 m=re.fullmatch(r'(?:y|f\(x\))\\in\s*([\[(])(.*),(.*)([\])])',z);assert m,z
 def endpoint(a):return s.oo if a.strip()==r'\infty' else -s.oo if a.strip()==r'-\infty' else scalar(a)
 return s.Interval(endpoint(m[2]),endpoint(m[3]),left_open=m[1]=='(',right_open=m[4]==')')
def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','g'+str(k));src=H.source(g,k);records=json.loads((R/f'qa/{k}-sampled.json').read_text());equalities=stages=choices=0
 for r in records:
  q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];f=q[':question/answer-fields'][0];profile=r['generation']['bank_profile']
  if k==17592186129123:
   m=re.search(r'minimum value of \$([^$]+)\$ and a maximum value of \$([^$]+)\$',prompt);assert m
   lo,hi=scalar(m[1]),scalar(m[2]);center=(lo+hi)/2;assert lo<hi
   values=[scalar(a[':answer/value'].removeprefix('y=')) for a in f[':answer-field/choices']]
   if profile=='method_average':expected=[center,lo,hi,(hi-lo)/2,lo+hi]
   elif profile=='method_reverse_difference':expected=[center,lo,hi,(lo-hi)/2,lo+hi]
   elif profile=='zero_minimum':assert lo==0;expected=[center,lo,hi,-hi,-center]
   elif profile=='zero_maximum':assert hi==0;expected=[center,lo,hi,-lo,-center]
   else:raise AssertionError(profile)
   assert set(values)==set(expected)
   def parse(z):
    return scalar(z.replace(r'{y}_{\text{min}}','('+s.latex(lo)+')').replace(r'{y}_{\text{max}}','('+s.latex(hi)+')')).subs(P.y,center)
   for block in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',sol,re.S):
    body=next(z for z in block if z).replace(r'\begin{aligned}','').replace(r'\end{aligned}','');lhs=None
    for row in body.split(r'\\'):
     parts=row.replace('&','').split('=')
     if len(parts)<2:continue
     if not parts[0].strip():parts[0]=lhs
     else:lhs=parts[0]
     vals=[parse(z) for z in parts]
     for v in vals[1:]:assert s.simplify(vals[0]-v)==0,(row,vals);equalities+=1
   assert scalar(re.search(r'Therefore, the midline is \$y=(.*?)\$',sol)[1])==center;target=center
  else:
   env=H.physics(prompt.replace(r'^{\circ}',''));A,B,C,D=(env[z] for z in ('A','B','C','D'));lo,hi=D-abs(A),D+abs(A);minimum='minimum value' in prompt;values=[scalar(a[':answer/value']) if minimum else interval(a[':answer/value']) for a in f[':answer-field/choices']]
   target=lo if minimum else s.Interval(lo,hi)
   if profile=='extrema':expected=[lo,hi,D,abs(A),-abs(A)]
   elif profile=='endpoints':expected=[s.Interval(lo,hi),s.Interval(lo,hi,True,True),s.Interval(lo,hi,True,False),s.Interval(lo,hi,False,True),s.Interval(-s.oo,s.oo)]
   elif profile=='outer_transform':expected=[s.Interval(lo,hi),s.Interval(-abs(A),abs(A)),s.Interval(-D-abs(A),-D+abs(A)),s.Interval(D-1,D+1),s.Interval(D-abs(A*B),D+abs(A*B))]
   else:raise AssertionError(profile)
   assert set(values)==set(expected)
   blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==3
   op=env['trig'].func;shifted=env['trig'];scaled=A*shifted;F=env['F'];base=op(P.x);direction=r'\ge' if A<0 else r'\le'
   expectedrows=[(-1,base,1,r'\le'),(-1,shifted,1,r'\le'),(-1,shifted,1,r'\le'),(-A,scaled,A,direction),(D-A,F,D+A,direction),(lo,F,hi,r'\le')]
   actualrows=[]
   for block in blocks:
    block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
    actualrows.extend(row.replace('&','').strip().rstrip('.') for row in block.split(r'\\'))
   assert len(actualrows)==len(expectedrows)
   for row,(left,middle,right,operator) in zip(actualrows,expectedrows):
    sides=re.split(r'(\\le|\\ge)',row);assert len(sides)==5 and sides[1]==sides[3]==operator,(row,operator)
    parsed=[H.read(z.replace(r'^{\circ}',''),env) for z in sides[::2]];assert parsed[0]==left and parsed[2]==right and s.expand(parsed[1]-middle)==0,(row,parsed,(left,middle,right));stages+=1
   if minimum:assert scalar(re.search(r'Therefore, the minimum value is \$(.*?)\$',sol)[1])==lo
   else:assert interval(re.search(r'Therefore, the range is \$(.*?)\$',sol)[1].rstrip('.'))==target
  assert len(values)==len(set(values))==5
  for a,v in zip(f[':answer-field/choices'],values):assert (v==target)==(a[':answer/id']==f[':answer-field/correct'][1]);choices+=1
 report=dict(status='passed',kp_id=k,source=src,normal_records=len(records),complete_choice_values=choices,actual_average_equalities=equalities,signed_range_stages=stages,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
