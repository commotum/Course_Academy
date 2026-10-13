"""Freeze reusable prose scaffolds from immutable evidence, not runtime payloads."""
import importlib.util,json,re,shutil
from pathlib import Path
root=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',root.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
captured=Path('generate/runs/current/sources/17592186096842.json');shutil.copyfile(captured,root/'source.json')
raw=json.loads(captured.read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
params={
 'q-48730':dict(a=5,b=-1), 'q-48846':dict(a=4,b=-3),'q-107291':dict(a=-6,b=3),
 'q-107360':dict(a=-4,b=1,t=-2),'q-314194':dict(a=2,b=7),'q-342680':dict(a=1,b=-6,c=0),
 'q-342683':dict(a=3,b=6),'q-342764':dict(a=5,b=1),'q-342802':dict(a=3,b=12,c=0,t=2)}
profiles={'q-48730':'source_reciprocal','q-48846':'source_spaced','q-107291':'source_constfirst','q-107360':'source_slope'}
templates={};cases=[]
for name,s in g.TEMPLATES.items():
 q=qs[s['source']];p=params[s['source']];parts=g.blocks(s,p)
 prompt=q[':question/problem'].replace(parts['function'],'<<function>>')
 if s.get('slope'):prompt=prompt.replace('x='+str(p['t']),'x=<<t>>')
 solution=q.get(':question/worked-solution')
 if solution:
  blockkeys=['chain','outer_deriv','inner_deriv','multiplication']+(['evaluation'] if s.get('slope') else [])
  chunks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S)
  assert len(chunks)==len(blockkeys)
  for chunk,key in zip(chunks,blockkeys):solution=solution.replace('$$\n'+chunk+'\n$$','$$\n<<'+key+'>>\n$$')
  solution=solution.replace('Let $u='+parts['z']+'.$','Let $u=<<z>>.$')
  solution=solution.replace('Then $y='+parts['outer']+'.$','Then $y=<<outer>>.$')
  if s.get('slope'):solution=solution.replace('x='+str(p['t']),'x=<<t>>')
 else:
  solution='We use the chain rule in the form\n\n$$\n<<chain>>\n$$\n\nLet $u=<<z>>.$ Then $y=<<outer>>.$ Differentiating, we have\n\n$$\n<<outer_deriv>>\n$$\n\nand\n\n$$\n<<inner_deriv>>\n$$\n\nMultiplying the two together gives\n\n$$\n<<multiplication>>\n$$'
 assert '<<function>>' in prompt
 assert '<<z>>' in solution and '<<outer>>' in solution
 templates[name]={'prompt':prompt,'solution':solution}
 cases.append({'source_id':q[':question/math-academy-id'],'source_uuid':q[':question/id'],'template':name,'level':s['level'],'parameters':p,'bank_profile':profiles.get(s['source'],'blank'),'repairs':['authored moderate assignment','inferred correct derivative','authored worked solution'] if s.get('repair') else []})
(root/'templates.json').write_text(json.dumps(templates,indent=2)+'\n');(root/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
for case in cases:
 r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
 q=qs[case['source_id']]
 import difflib
 for attr in [':question/problem',':question/worked-solution']:
  if attr in q and q[attr]!=r['question'][attr]:
   print(case['source_id'],attr)
   print('\n'.join(difflib.unified_diff(q[attr].splitlines(),r['question'][attr].splitlines())))
