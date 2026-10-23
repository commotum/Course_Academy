from pathlib import Path
import json
entry=Path('17592186129197.py');code=entry.read_text()
code=code.replace("Q={q[':question/math-academy-id']:q for q in R[':knowledge-point/questions']}","Q={q[':question/math-academy-id']:q for q in R[':knowledge-point/questions']}\nCURRENT=json.loads((ROOT/'current-source.json').read_text())\nCURRENT_Q={q[':question/math-academy-id']:q for q in CURRENT['material']['kp'][':knowledge-point/questions']}")
code=code.replace('def raw_generate(level,seed,source,parameters):\n q=Q[source];', 'def raw_generate(level,seed,source,parameters,historical=False):\n q=(Q if historical else CURRENT_Q)[source];')
code=code.replace("  family=next(f for f,z in FAMILIES.items() if z[0]==source)\n  m=model(family,ANCHORS[source]); det=m['det']; inv=m['J']\n  if s!=1:","  if s!=1:\n   if source not in ANCHORS:raise ValueError('current source supports exact scale=1 replay only')\n   family=next(f for f,z in FAMILIES.items() if z[0]==source)\n   m=model(family,ANCHORS[source]); det=m['det']; inv=m['J']")
code=code.replace("p,'raw:'+source,False,{'source_omissions'", "p,('historical:' if historical else 'raw:')+source,False,{'replay_capture':'historical' if historical else 'current','source_omissions'")
start=code.index('def recipes(');end=code.index("RENDERER_VERSION=",start)
code=code[:start]+'''def candidate_instances(f,rng):
 """Choose a bank without assigning the correct-answer role to any member."""
 candidates=[]
 for _ in range(1000):
  p=sample(f,rng);d=model(f,p)
  if all(not eq(d['A'],other['A']) for _,other in candidates):
   candidates.append((p,d))
   if len(candidates)==5:return candidates
 raise ValueError('could not construct five distinct counterfactual areas')
def recipes(f,d,p,profile,candidates):
 if profile!='method':raise ValueError('normal profile is method')
 bank=[other['A'] for _,other in candidates]
 # Explicit parameter calls retain the same bank whenever their area is a
 # member, allowing all five target assignments with the same choice values.
 if not any(eq(d['A'],value) for value in bank):bank[-1]=d['A']
 return bank
''' +code[end:]
code=code.replace(" folder=Path(output_dir) if output_dir else ROOT/'plots';folder.mkdir(parents=True,exist_ok=True)"," output_dir=output_dir or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')\n if not output_dir:raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required for generated assets')\n folder=Path(output_dir)/'plots';folder.mkdir(parents=True,exist_ok=True)")
code=code.replace(" if profile and profile.startswith('raw:'):\n  sid=profile[4:]\n  if sid not in Q:raise ValueError('source id')\n  return raw_generate(level,seed,sid,parameters)"," if profile and profile.startswith(('raw:','historical:')):\n  prefix,sid=profile.split(':',1); historical=prefix=='historical'\n  if sid not in (Q if historical else CURRENT_Q):raise ValueError('source id')\n  return raw_generate(level,seed,sid,parameters,historical)")
code=code.replace(" selected=profile or 'method' # Complete bank is fixed before parameter sampling."," selected=profile or 'method'")
code=code.replace(" for _ in range(1000):\n  p=dict(parameters) if parameters is not None else sample(f,rng);guards(f,p);d=model(f,p);bank=recipes(f,d,p,selected)"," candidates=candidate_instances(f,rng)\n target=rng.randrange(len(candidates))\n for _ in range(1):\n  p=dict(parameters) if parameters is not None else dict(candidates[target][0]);guards(f,p);d=model(f,p);bank=recipes(f,d,p,selected,candidates)")
code=code.replace("{'source_question':FAMILIES[f][0],'plot':asset", "{'bank_construction':'compatible-instance-areas','bank_parameters':[cp for cp,_ in candidates],'source_question':FAMILIES[f][0],'plot':asset")
code=code.replace("args.profile.startswith('raw:')", "args.profile.startswith(('raw:','historical:'))")
entry.write_text(code)
source=json.loads(Path('../source/source.json').read_text())
# Bundle only the supplied KP replay data and capture provenance, not whole lessons.
current={k:source[k] for k in ['database','basis','lineage','source_sha256']};current['material']={'kp':source['material']['kp']}
Path('17592186129197/current-source.json').write_text(json.dumps(current,indent=2,ensure_ascii=False)+'\n')
