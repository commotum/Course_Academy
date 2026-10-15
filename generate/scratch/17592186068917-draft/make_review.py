"""Read-only source + private generator review artifact writer."""
import importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
parts=['# Original sources and generated variants\n\nRaw profiles are ineligible evidence. Normal examples use authored method banks; easy is an authored level. All examples use the public generate API.']
records=[]
for t,source in g.SOURCES.items():
 parts+=['\n## '+t+' — captured original\n',source[':question/problem'],'\n\nOriginal complete bank:\n']
 for field in source[':question/answer-fields']:
  parts+=['- $'+a[':answer/value']+'$' for a in field[':answer-field/choices']]
 parts+=['\n'+source.get(':question/worked-solution','[No captured solution, difficulty or correct designation.]')]
 params=g.defaults(t);params['A']=params['A']%12+1
 raw=g.generate(g.LEVELS[t],seed=19,template=t,parameters=params,profile='observed_raw');v.validate_display(raw);records.append(raw)
 parts+=['\n### Changed evidence-bank variant (ineligible)\n',g.markdown(raw)]
 for idx,seed in enumerate((19,53),1):
  normal=g.generate(g.LEVELS[t],seed=seed,template=t);v.validate_display(normal);records.append(normal)
  parts+=['\n### Generated normal variant '+str(idx)+'\n',g.markdown(normal)]
parts+=['\n## Authored easy from the preceding nonlinear-product tutorial\n']
for family,k in [('cos',2),('sin',5)]:
 r=g.generate_easy(template='authored-easy',parameters=dict(A=2*k,k=k,kind=family));v.validate_display(r);records.append(r);parts+=['\n### Generated easy '+family+'\n',g.markdown(r)]
(H/'review.md').write_text('\n\n'.join(parts)+'\n');(H/'review.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print('review records',len(records))
