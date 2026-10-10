"""Materialize manually reviewed source-to-choice bindings; never infer new keys.

The numeric choice positions below were reviewed against each saved MA solution
and original before-answer layout. Analysis candidates are used only to locate
an exact original radio option already reviewed; their labels grant no authority.
"""
import copy,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
read=lambda p:json.loads(Path(p).read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
source=read(ROOT/'recovery-input.json')
patterns=read(ROOT/'radio-analysis-input.json')['questions']
radios={
1187:'The solution explicitly names {a} as the subset. Preserve the singleton set braces.',
1203:'The final P(X) equality gives the entire power set, including each singleton subset and the empty set. Match every brace exactly.',
1208:'The prompt asks for the statement NOT true; the solution explicitly singles out C⊆Z as false.',
1270:'The solution names this complete collection as the only partition before rejecting the other collections.',
1275:'The solution names this complete three-subset collection as the only partition before discussing distractors.',
2549:'The concluding sentence gives the volume increase rate 16π cm^3/s at radius 2 cm; retain the complete units.',
2870:'The prompt asks how fast the circumference is decreasing; the final sentence gives the positive magnitude 8π/5 cm/s, distinct from the signed derivative.',
6529:'The conclusion states 3,628,800 arrangements of the ten books.',
6534:'The conclusion states 40,320 orders for calling the eight guests.',
6664:'The solution explicitly states that only -3/2 among the choices has the rational-roots-theorem form.',
6671:'The prompt asks which CANNOT be a root; the solution explicitly rejects -6.',
7210:'The final sentence applies t>0 and states t=5/3 seconds. Do not include the rejected zero-time root.',
7945:'The inverse Q^-1 is the complete 2x2 matrix [-2,-1;-5,-3] before the subsequent identity-product verification. The final identity matrix is not the requested inverse.',
8005:'The final sentence gives both intersection points (5,±9/4). Preserve the paired coordinates.',
8739:'The solution explicitly names the sole homogeneous ODE before its two verification methods; retain the complete differential equation.',
9455:'The conclusion binds (1,0) to the requested x-axis intersection.',
9463:'The conclusion binds (0,-2) to the requested y-axis intersection.',
12498:'The integration chain gives the entire antiderivative 2/15 sqrt((5x+1)^3)+C before differentiating to check it. The later integrand is not the answer.',
13497:'The solution explicitly identifies c24=5, the second-row fourth-column entry; do not substitute the entire displayed matrix.',
14144:'The source counts sixteen distinct potential roots after removing duplicates, including both signs.',
14191:'The final sentence gives the full x-axis intersection (2/13,0).',
15589:'The source evaluates t1 at approximately 95 minutes, explicitly rounded to the nearest minute.',
20512:'The source concludes x=5,y=4,z=-4 and explicitly supplies the complete vector in that order.',
20849:'The source substitutes t=0 into dy/dx=4t and concludes 0 at the requested point.',
21496:'The source derivative-sign table and conclusion identify x=2 as a local minimum on the positive domain.',
29664:'The requested product, rather than either angle, is explicitly rounded to -6,741 in the final calculation.',
29938:'The requested product, rather than either angle, is explicitly rounded to 6,741 in the final calculation.',
32531:'The concluding sentence identifies l21=5/2 and u22=0 and explicitly gives their requested sum 5/2.',
34422:'The source explicitly calls B={[-1;0;1]} a basis of Null(A). Retain the singleton set around the full three-entry column.',
35620:'The final sentence distinguishes semi-major length 4 from requested full major-axis length 8.',
36751:'The source selects x1=1 and explicitly names the entire vector [1;0;0] for eigenvalue 3.',
36911:'The source concludes that the full point (0,3) makes the gradient zero.',
37180:'The source explicitly names the inhibited-growth initial value problem, including P(0)=690, before rejecting other initial conditions.',
37250:'The source identifies v1=[1;1;1] and places it in the first column of the displayed P. Preserve all three entries.',
37701:'The maximum-value calculation gives 3 sqrt(3)/8 before a later comparison example. The later value 1/2 is not the requested maximum.',
37846:'The source states diagonalizability and explicitly gives D=diag(-9,-3,5), in the option ordering, before an alternate ordering.',
37959:'The source calls f(4,4,4)=48 the minimum before the later comparison example 54.',
38012:'The source concludes b is not in Im(T) because the system is inconsistent; the conditional requested coordinate expression has no value.',
38229:'The final statement names the image line y=3x.',
39626:'The final statement calls the singleton set containing [-1;0;1] a basis of the orthogonal complement; preserve set braces and all vector entries.',
105123:'The final P(T) equality lists the complete power set including singleton subsets {k},{m},{o}; preserve every brace.',
5144:'The final sentence gives both center (-2,3) and radius 4, matching the two labeled parts of the option.',
5183:'The final sentence gives both center (4,5) and radius 7, matching the two labeled parts of the option.',
6913:'The final sentence states that the function has no vertical asymptotes.',
6993:'The final sentence states that there is no horizontal asymptote.',
7596:'The source separately names major-axis length 6 sqrt(2) and minor-axis length 6, in the order requested.',
7597:'The source separately names major-axis length 4 sqrt(5) and minor-axis length 8, in the order requested.',
7639:'The source explicitly says I and III are true and II false; bind to the three statements in prompt order.',
7643:'The solution sets y=0 for x-intercepts and solves x=0,4. The corresponding full points in the original option are (0,0) and (4,0).',
7644:'The final sentence explicitly gives both y-axis intercepts (0,-6) and (0,0).',
7830:'The source says the matrix has no special name, which binds to the original Other choice.',
7835:'The source classifies K as nonsquare and L and M as square, concluding only L and M.',
7915:'The source concludes only P and Q are singular; R is nonsquare and is not called singular.',
8049:'The source checks both linearity conditions and explicitly concludes only statement III is true.',
8054:'The source explicitly identifies a dilation and scale factor 3.',
8060:'The final sentence explicitly identifies reflection in y=-x.',
8331:'The source explicitly concludes all three listed statements are true.',
8408:'The conclusion explicitly gives both p=4 and q=-6.',
8460:'The final sentence gives rotation π/6 anticlockwise about the origin; anticlockwise matches counterclockwise with the same angle and center.',
8801:'The solution explicitly concludes that the circle has no x-intercepts.',
9347:'The final sentence gives both real eigenvalues 5 and 1.',
9467:'The final sentence states that the ellipse has no y-intercepts.',
9913:'The final sentence gives the complete pair k=0 and k=2.',
10485:'The source explicitly concludes there are no real solutions and hence no intersection with y=x.',
10662:'The source explicitly concludes the linear system has no solution.',
11983:'The source gives both eigenvalues sqrt(3) and 2 before its general triangular-matrix note.',
12008:'The source explicitly concludes that all three listed statements are true.',
12043:'The source identifies dilation with scale factor 12.',
12044:'The final statement identifies a horizontal shear with factor 10, preserving both direction and factor.',
12549:'The solution computes P(A∩B)=0.2≠0 and concludes the events are not mutually exclusive. Both clauses of the option are supported.',
12997:'The source gives p+q=68 before solving and then gives both roots a=-12 and a=4. All three clauses are required.',
13635:'The final AB calculation gives the entire 3x2 matrix [0,0;-2,-4;-3,-6]. Retain its original text answer type and display-math wrapper.',
13759:'The solution explicitly classifies A as lower triangular and rejects upper triangular and diagonal.',
13781:'The solution explicitly classifies A as upper triangular and rejects lower triangular and diagonal.',
13912:'The solution states R=1, then verifies both endpoints and concludes I=[0,2]. Preserve both closed endpoints and both requested results.',
14050:'The final sentence gives both x-intercepts 7 and -1.',
14241:'The final sentence gives both y-intercepts 2 and 6.',
14619:'The final sentence gives center (2,-2) and radius sqrt(13/2); preserve the original source working including its separately noted typo.',
15460:'The final sentence gives both center (-1,5) and radius 9.',
15681:'The final sentence gives both complete x-intercept points (-9,0) and (1,0).',
15684:'The final sentence gives both complete x-intercept points (-5,0) and (7,0).',
}
selects={
183328:([1,0],['Constructed element 3·2^n','Index domain Z following n∈']),
183690:([1,1,0],['Ambient set Z following x∈','Inclusive lower bound -6','Inclusive upper bound 12']),
183691:([1,0],['Ambient set Z following x∈','Inclusive lower bound -25 following x≥']),
183765:([3,0],['Constructed element 3n','Full condition ∈Z following n; do not duplicate ∈']),
183770:([0,2],['Constructed element 4n-9','Full condition ∈Z following n; do not duplicate ∈']),
183771:([0,1],['Constructed element (-2)^n','Index domain Z following n∈']),
331821:([3,3,2,0],['First integral integrand e^(-st)·e^t b(t)','Second integral exponential factor e^(-(s-1)t), before fixed b(t)','Whole transformed function B(s-1)','Full domain qualifier s>s0+1 after for']),
334652:([3,3,2,4],['LTE at step size 0.5','LTE at step size 0.25','LTE reduction factor','Order p rounded to integer 3, not the exponent p+1']),
334685:([0,1,4,0,0],['L1: reflexive property','L4: premise lines L1 and L3','L4: absorption property','L5: premise line L4','L5: constant multiple property']),
334709:([1,2,4,0],['LTE at step size 0.3','LTE at step size 0.1','LTE reduction factor','Order p rounded to integer 2']),
334710:([4,0,0,0],['LTE at step size 0.6','LTE at step size 0.4','LTE reduction factor','Order p rounded to integer 4']),
334724:([1,4,0,0],['LTE at step size 0.5','LTE at step size 0.2','LTE reduction factor','Order p rounded to integer 4']),
334754:([1,1,0,0],['Trajectory action circles around','Object: nonzero equilibrium','Prey from A to B: decreases','Predators from A to B: increases']),
334829:([3,1,0],['L1 to L2: definition of derivative with respect to s','L3 and L4 to L5: substitution','L5 to L6: definition of Laplace transform']),
334874:([1,2,1],['L1 to L2: definition of second derivative with respect to s','L2 to L3: differentiating under integral sign','L4: chain rule']),
334879:([2,2,2],['L1 to L2: definition of second derivative with respect to s','L2 to L3: differentiating under integral sign','L3 and L4 to L5: substitution']),
334924:([2,0],['Top entry of integral vector e^(2s) cosh(2(t-s)); keep s and t-s','Bottom entry of homogeneous vector 3 sinh(2(t-1))+cosh(2(t-1))']),
334942:([3,1],['Entire 2x2 determinant |0,2;2,0| at (1,1), not just its scalar value -4','Classification almost linear at that point']),
334988:([1,0],['x-prime is a rate of change','x represents the predator, as the source explicitly explains']),
335040:([0,0,0,0],['Trajectory circles around','Object: nonzero equilibrium','Prey from A to B: decreases','Predators from A to B: decreases']),
335099:([3,0],['Entire 2x2 determinant |-1,0;π,0| at (0,1), not just scalar zero','Classification not almost linear at that point']),
335175:([0],['Top entry x(t)=cosh(2t)-1; fixed bottom entry is sinh(2t)']),
}
restored={
183328:r'S={ {{field-1}}\,:\,n\in {{field-2}} }',
183690:r'S={x\in {{field-1}}\,:\,{{field-2}}\le x\le {{field-3}}}',
183691:r'S={x\in {{field-1}}\,:\,x\ge {{field-2}}}',
183765:r'S={ {{field-1}}\,:\,n {{field-2}} }',
183770:r'S={ {{field-1}}\,:\,n {{field-2}} }',
183771:r'S={ {{field-1}}\,:\,n\in {{field-2}} }',
331821:r'\begin{aligned}L{{e}^{t}b(t)}&={\int}_{0}^{\infty}{{field-1}}\,\mathrm{d}t\\&={\int}_{0}^{\infty}{{field-2}}b(t)\,\mathrm{d}t\\&={{field-3}}\quad\text{for }{{field-4}}.\end{aligned}'
}
review={}
for n,note in radios.items():
 mid=f'q-{n}';p=patterns[mid]['occurrences'][0]
 o=next(x for x in source[mid]['occurrences'] if x['directory']==p['directory'])
 assert o['source_problem']==p['source_problem'] and o['worked_solution']==p['worked_solution']
 assert len(o['before_fields'])==1 and len(p['candidates'])==1
 c=p['candidates'][0];choices=o['before_fields'][0]['choices']
 ix=[i for i,x in enumerate(choices) if {k:x[k] for k in ('type','value')}==c];assert len(ix)==1,(mid,c)
 review[mid]={'directory':o['directory'],'fields':[{'key':o['before_fields'][0]['key'],'choice_index':ix[0],'answer':c,'binding':note}],'category':patterns[mid]['category']}
for n,(indices,notes) in selects.items():
 mid=f'q-{n}';o=source[mid]['occurrences'][0];assert len(indices)==len(notes)==len(o['before_fields'])
 fs=[]
 for f,i,note in zip(o['before_fields'],indices,notes):
  c={k:f['choices'][i][k] for k in ('type','value')};fs.append({'key':f['key'],'choice_index':i,'answer':c,'binding':note})
 review[mid]={'directory':o['directory'],'fields':fs,'category':'select_questions'}
 if n in restored:
  from bs4 import BeautifulSoup
  b=read(Path(o['directory'])/'state.json')['questions'][mid]['before']
  soup=BeautifulSoup(b['html'],'html.parser');widget=soup.select_one('.questionWidget-text')
  controls=widget.select('.selectList');assert [c['id'] for c in controls]==[f['dom_id'] for f in o['before_fields']]
  math=widget.select('math')[-1]
  mathtext=math.get_text(' ',strip=True)
  assert all(f'S {i}' in mathtext for i in range(len(indices)))
  folder=ROOT/'layout-evidence';folder.mkdir(exist_ok=True)
  (folder/(mid+'-before.html')).write_text(b['html'])
  (folder/(mid+'-template.mathml')).write_text(str(math))
  prefix=o['source_problem'].rsplit('$$',2)[0].rstrip()
  review[mid]['restored_problem']=prefix+'\n\n$$\n'+restored[n]+'\n$$'
  review[mid]['layout_recovery']={'source_file':str(Path(o['directory'])/'state.json'),'json_pointer':f'/questions/{mid}/before/html','original_dom_ids':[c['id'] for c in controls],'source_mathml_text':mathtext,'binding':'S0,S1,... in the captured final MathML template bind to the same-numbered selectList question controls and hence field-1,field-2,... . Replace only those widgets; retain the outer set, relations, integral factors and domain text.'}
for mid,r in review.items():
 o=next(x for x in source[mid]['occurrences'] if x['directory']==r['directory']);d=Path(r['directory']);state=read(d/'state.json');rec=state['questions'][mid]
 sol=rec.get(o['source_solution_stage']) or read(d/(('history-'+mid if o['source_solution_stage']=='history' else mid+'-after')+'.json'))
 assert sol['worked_solution']==o['worked_solution']
 r['source']=':org/Math-Academy';r['review_method']='agent interpretation of saved MA worked solution and exact original field layout'
 r['source_problem']=o['source_problem'];r['source_quote']=o['worked_solution']
 r['solution_location']={'file':str(d/'state.json'),'json_pointer':f'/questions/{mid}/{o["source_solution_stage"]}/worked_solution'}
 r['source_hashes']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [d/'state.json',d/'content.json']}
 r['before_layout_sha256']=hashlib.sha256(json.dumps(rec['before'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 for f in r['fields']:
  f['source_location']=r['solution_location'];f['source_quote']=r['source_quote'];f['binding']='Field '+f['key']+': '+f['binding']
 # Explicit numbered-list references must keep their labels visible in Markdown.
 if mid in {'q-7639','q-8049','q-8331','q-12008'}:
  p=o['source_problem'];lines=p.splitlines();i=0
  for j,line in enumerate(lines):
   if line.startswith('- '):lines[j]=['I. ','II. ','III. '][i]+line[2:];i+=1
  assert i==3
  r['restored_problem']='\n'.join(lines)
  r['layout_note']='Restore Roman labels I/II/III in existing source statement order because the original choices refer to those labels.'
 assert all(f['answer']['value'].strip(' $\n') for f in r['fields'])
save(ROOT/'answer-review.json',review)
print('REVIEWED',len(review),'RADIO',len(radios),'SELECT',len(selects),'FIELDS',sum(len(q['fields']) for q in review.values()))
