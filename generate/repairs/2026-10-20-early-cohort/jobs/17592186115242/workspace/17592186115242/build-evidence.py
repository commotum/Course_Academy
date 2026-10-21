import json,re, pathlib, shutil
D=pathlib.Path(__file__).parent
capture=json.load(open('generate/runs/current/sources/17592186115242.json'))
(D/'source.json').write_text(json.dumps(capture,indent=2)+'\n')
qs=capture['record'][':knowledge-point/questions']
pars=[(3,4,12,1,1,0,4), (2,3,1,6,1,3,-5),(-3,2,1,6,1,9,5),(1,-3,-1,4,3,0,3),(-1,4,-2,-3,3,15,-4),(-2,7,6,1,1,0,-3),(-2,6,-4,5,1,-6,10),(2,-1,3,4,1,0,4),(-4,-1,2,8,1,0,5),(1,4,2,2,1,1,3),(1,2,-4,3,2,0,-2),(4,2,-8,1,1,0,-2),(2,6,4,1,1,1,2),(3,2,12,1,1,0,4),(1,2,3,-3,-1,-1,-9)]
# Full banks. Opaque arithmetic offset patterns are explicit replay profiles only.
banks=[['0','t','1/t','-b','-t'],['r*b','t','t-2','-a','t+1'],['t','h+1','t+1','h','t-1'],['t-9','h','t+1','r*b','t'],['-t','t','t-1','0','-2*t'],['1/t','-b','-t','t','0'],['t','v','0','-t','t-3'],['0','2*t','-t','t','-2*t'],['t','0','-e','-d','-t'],['t-2','e','v','t+2','t'],['-u','-1','-t','t','u'],['t/2','-t/2','t','1/t','t/4'],['1/t','-1/t','-t','t','-2*t'],['b','0','t','-t','1/t'],['-v','d','-t','b','t']]
specs={};cases=[]
# Loading generator below supplies exact renderer, so extraction can compare complete math slots.
import importlib.util
spec=importlib.util.spec_from_file_location('gen',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
for q,vs,bank in zip(qs,pars,banks):
 sid=q[':question/math-academy-id'];p=dict(zip('a b c d u v e'.split(),vs));hard='hard' in q[':question/difficulty'][':db/ident']
 swap=sid in ['q-32246','q-131729','q-74695','q-131730']
 if swap:template='dependent_swap'
 elif hard:template='dependent_negative' if p['u']<0 else 'dependent_fractional'
 else:template='inconsistent_scaled_shift' if p['u']!=1 and p['v'] else 'inconsistent_scaled' if p['u']!=1 else 'inconsistent_shift' if p['v'] else 'inconsistent_bare'
 style={'swap':swap,'rowop':'subtract' if sid in ['q-131727','q-131728','q-131730'] else 'plus_parenthesized' if sid in ['q-32246','q-42059','q-32245','q-74646','q-74688','q-74695','q-74650'] else 'plus', 'negative_coeff_factored':sid=='q-42021'}
 comps=g.components(p,style)
 problem=q[':question/problem'];sol=q[':question/worked-solution']
 # Error repairs before extraction; original is retained in source.json.
 if sid=='q-74695':sol=sol.replace('x+ky=2','x+ky=-2')
 if sid=='q-42021':sol=sol.replace('1 & 2 & -3','1 & 2 & 3').replace('1-2y=3','x+2y=3')
 # Replace complete mathematical objects, longest first, with atomic slots.
 # Matrices precede equation strings so their inner scalars never get touched.
 for key in ['matrix0','matrix1','matrix2','rowop','equation1','equation2','pivot_equation','reduced_equation','answer','zero_equation']:
  value=comps.get(key)
  if value:
   problem=problem.replace(value,'@@'+key+'@@');sol=sol.replace(value,'@@'+key+'@@')
 # Generic parameter k formulas with same original notation are all handled above.
 item={'template':template,'level':'hard' if hard else 'moderate','parameters':p,'style':style,'problem_mask':problem,'solution_mask':sol,'bank':bank,'bank_interpretation':'Explicit observed arithmetic expression patterns; opaque offsets have unresolved error intent and are never default banks.'}
 # Assert every numeric math object is slotted (prose y/x unaffected).
 assert not re.search(r'(?<!\$)\$[^$]*\d[^$]*\$',re.sub(r'@@[^@]+@@','',sol).replace('$$','')), (sid,sol)
 specs[sid]=item;cases.append({'source_id':sid,'template':template,'parameters':p,'level':item['level'],'bank_profile':sid})
(D/'recipes.json').write_text(json.dumps(specs,indent=2)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
