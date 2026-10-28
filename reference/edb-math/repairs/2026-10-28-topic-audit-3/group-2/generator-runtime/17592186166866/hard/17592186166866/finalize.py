"""Update local review montage/mappings and record immutable file hashes after QA."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,hashlib,re
import sympy as sp
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
vs=importlib.util.spec_from_file_location('qa',HERE/'validate.py');qa=importlib.util.module_from_spec(vs);vs.loader.exec_module(qa)
canonical=g.KP[':knowledge-point/canonical-example'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',canonical[':question/worked-solution'],re.S)
setup=blocks[0].replace(r'\dfrac',r'\frac').replace(r'\qquad','').replace(r'\Longrightarrow','⟹').strip().rstrip('.')
for equation in setup.split('⟹'):
 lhs,rhs=equation.split('=');assert sp.cancel(qa.expr(lhs)-qa.expr(rhs)-((qa.x**2)/4+(qa.y**2)/16-1))==0
body=blocks[1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}');rows=body.split(r' \\ ');assert len(rows)==6
for row in rows:
 lhs,rhs=row.split(' & =');assert sp.cancel((qa.formal(lhs)-qa.formal(rhs)).subs(qa.z,-4*qa.x/qa.y))==0
(HERE/'canonical-math.json').write_text(json.dumps({'source_id':'e-9578','equation_stages':2,'ordered_derivative_rows':6,'all_formal_operator_inputs_and_intermediates_independently_checked':True,'extra_reduction_row_preserved_in_evidence':True},indent=2)+'\n')
mapping=[]
for c in g.CASES.values():
 q=g.KP[':knowledge-point/questions'][c['index']];vals=g.bank(c['parameters'],g.CODES[c['index']],'ascii' if c['index']==1 else 'tex');original=q[':question/answer-fields'][0]
 mapping.append({'source_id':c['source_id'],'parameters':c['parameters'],'profile':c['bank_profile'],'evidence_only':True,'eligible_for_learning':False,'choices':[{'original_answer_id':a[':answer/id'],'displayed':a[':answer/value'],'operation':v[0],'parameterized_value':str(v[1]),'exact_reproduced':a[':answer/value']==v[2],'captured_correct':a[':answer/id']==original.get(':answer-field/correct',{}).get(':answer/id'),'interpretation':'mathematical operation recoverable; historical cognitive intention hypothetical'} for a,v in zip(original[':answer-field/choices'],vals)]})
(HERE/'bank-mapping.json').write_text(json.dumps(mapping,indent=2)+'\n')
records=json.loads((HERE/'review.json').read_text())
for r in records:
 gen=r['generation'];profile=gen['bank_profile']
 if gen['evidence_only'] and profile.startswith('completed-'):
  case=g.CASES[profile.split('-',1)[1]]
  if gen['parameters']!=case['parameters']:gen['origin']='generated historical bank variant'
(HERE/'review.json').write_text(json.dumps(records,indent=2)+'\n')
(HERE/'review.md').write_text('# Ellipse generator review\n\nRaw originals, separate supported completions, six authored variants per level, and explicitly generated changed-parameter variants for every observed bank. Checked boxes mark designated correct choices; original omissions remain visible.\n\n'+'\n\n'.join(g.markdown(r) for r in records)+'\n')
selected=[r for r in records if not r['generation']['evidence_only']][:18];canvas=Image.new('RGB',(1500,1500),'white');d=ImageDraw.Draw(canvas)
for i,r in enumerate(selected):
 im=Image.open(r['generation']['plot']['prompt']).convert('RGB');im.thumbnail((245,450));x=i%6*250;y=i//6*500;canvas.paste(im,(x,y+45));p=r['generation']['parameters'];d.text((x+2,y+2),r['question'][':question/difficulty'].split('/')[-1]+' '+str(p),fill='black')
canvas.save(HERE/'generated-montage.png')
(HERE/'visual-review.md').write_text('Source and generated montages inspected on white. All ten source graphs have right/up positive axes and equal unit scales, matching centers/semiaxes recorded in source-geometry.json. All eighteen normal variants show unclipped ellipse extrema, legible integer ticks, correct signed center and positive guide endpoints. Hard diagrams change no method or response criterion. The source derivative answers, including every direction/sign and quotient reversal, pass independent full-bank mathematics. Generated PNG extents are verified under the actual rendering transform in generated-geometry.json. No unexplained raster endpoints remain.\n')
paths=[HERE.with_suffix('.py')]+[p for p in HERE.rglob('*') if p.is_file() and p.name!='freeze.json' and '__pycache__' not in p.parts]
inputs=[HERE.parents[1]/'runs/current/sources/17592186166866.json',HERE.parents[1]/'runs/current/topics/17592186049506.json',HERE.parents[1]/'runs/current/lessons/17592186049506.json',HERE.parents[1]/'runs/current/check-engine']
freeze={'basis':1356,'lineage':g.SOURCE['lineage'],'generator_version':g.VERSION,'artifact_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)},'input_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'limitations':['Hard is authored, not captured.','Historical wrong-answer cognitive intent remains hypothetical.','Two absent refs/difficulties/solutions remain absent in raw replay; completion is independently inferred.','Radio grader validates identity selections; mathematics and full-bank checks are separate.'],'cache_policy':'No pruning; retained all assets from active QA.'}
(HERE/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
print('Frozen',len(paths),'local artifacts; no database writes.')
