"""Build local source replay cases and human review from parameterized API."""
import importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
p0=dict(a=1,sx=1,sy=1,swap=False)
cases=[{'source_id':name,'level':spec[0],'template':spec[1],'bank_profile':name,'parameters':p0,'source_question':g.QUESTIONS[name], 'difficulty_assignment':'authored moderate; source unrated' if name=='q-122296' else 'observed'} for name,spec in g.PROFILES.items()]
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
variants=[];originals=[]
review=['# Vector field identification review\n\nAll originals are at math basis 1356. Generated variants are labeled below. Source image references are resolved to captured local assets. Choice order is presentation only.']
for name,spec in g.PROFILES.items():
 r=g.generate(spec[0],profile=name,parameters=p0);originals.append(r)
 source=g.QUESTIONS[name];original=r['question'][':question/problem']+'\n\n'+'\n\n'.join('- '+('$'+a[':answer/value']+'$' if a[':answer/type'][':db/ident'].endswith('/math') else a[':answer/value']) for a in source[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+source.get(':question/worked-solution','[Original has no worked solution or correct designation.]')
 review+=['\n## Original '+name+' ('+spec[0]+')\n\n'+original]
 if name=='q-122296':review+=['\nAuthored source-format completion: plot has horizontal component x and vertical component -1; correct F. Moderate label and worked solution are authored.']
 if name=='q-122629':review+=['\nSource solution correction: eliminated F must be F(x,y)=-i-j, the bank choice. Raw original prose above retains its mismatched -i+xj formula.']
 for n,p in enumerate([dict(a=-1,sx=1,sy=1,swap=False),dict(a=1,sx=1,sy=-1,swap=True)]):
  v=g.generate(spec[0],seed=101+n,profile=name,parameters=p);variants.append(v)
  review+=['\n### Generated variant '+name+' '+str(n+1)+'\n\n'+g.markdown(v)]
for n,p in enumerate([dict(a=1,sx=1,sy=-1,swap=False),dict(a=1,sx=-1,sy=1,swap=True)]):
 v=g.generate_hard(seed=301+n,parameters=p);variants.append(v)
 review+=['\n## Authored missing-hard variant '+str(n+1)+'\n\n'+g.markdown(v)]
(HERE/'review.md').write_text('\n'.join(review)+'\n')
(HERE/'review.json').write_text(json.dumps({'original_replays':originals,'generated':variants},indent=2)+'\n')
