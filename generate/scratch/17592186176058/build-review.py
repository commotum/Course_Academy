#!/usr/bin/env python3
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sources=json.loads((ROOT/'source.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/'source-cases.json').read_text());byid={q[':db/id']:q for q in sources}
records=[];pages=['# Source and generated review','Every original appears with its exact prompt, complete bank and full solution (where present). Generated examples are labeled by family/profile and authored status. Evidence-only profiles retain raw historical patterns. Moderate is an authored level assignment. Local image links below point to the exact copied source raster; API records retain the original image reference.']
appendix=['\n## Per-option source recipe appendix\n','All values below are exact captured fragments, assigned one-to-one to their source-owned field; recipe descriptions are in Stage 3 above. No source option is omitted.']
for case in cases:
 q=byid[case['source_id']];f=q[':question/answer-fields'][0]
 pages+=['\n## Original '+str(q[':db/id'])+' / '+q[':question/math-academy-id'], '\nObserved difficulty: '+q.get(':question/difficulty',{}).get(':db/ident','absent'),q[':question/problem'],'\nChoices:']
 for a in f[':answer-field/choices']:pages.append('- $'+a[':answer/value']+'$'+(' (source correct)' if a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id') else ''))
 pages+=['\n'+q.get(':question/worked-solution','**Source worked solution and correct designation absent.**')]
 replay=g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters=case['parameters'])
 appendix+=['\n### Source '+str(q[':db/id'])+' — field `'+f[':answer-field/id']+'`', '| Exact source value | Parameterized recipe | Original correct designation |','|---|---|---|']
 for a in f[':answer-field/choices']:
  recipe=replay['generation']['recipes'][a[':answer/value']]
  designation='absent' if ':answer-field/correct' not in f else ('correct' if a[':answer/id']==f[':answer-field/correct'][':answer/id'] else 'incorrect')
  appendix.append('| $'+a[':answer/value']+'$ | '+recipe+' | '+designation+' |')
 for i in range(2):
  r=g.generate(case['level'],seed=47+i,template=case['template'],profile=case['bank_profile']);records.append(r)
  pages+=['\n### Generated changed-parameter variant '+str(i+1)+' — '+case['template']+'/'+case['bank_profile'],'\nMetadata: '+('**evidence-only; not eligible for learner defaults**' if r['generation']['evidence_only'] else '**eligible generated family**')+'; parameters `'+json.dumps(r['generation']['parameters'],sort_keys=True)+'`',g.markdown(r)]
pages+=['\n## Normal defaults and authored completions','These examples cover every source-shaped template under its default eligible bank, including completed moderate and authored hard banks. Canonical mathematical counts are easy 92, moderate 92 and hard 245. Integer-period aliases yield 2,208 moderate and 5,880 hard presentation variants; these do not increase mathematical task counts.']
for template,level in g.TEMPLATES.items():
 for seed in [71,72]:
  r=g.generate(level,seed=seed,template=template);records.append(r)
  pages+=['\n### '+level+' / '+template+' / '+r['generation']['profile']+' — generated '+str(seed),'\n'+('Authored moderate completion and level assignment.' if level=='moderate' else 'Observed solution structure; '+('authored method-derived whole bank.' if level=='hard' else 'parameterized whole eligible bank.')),g.markdown(r)]
pages+=['\n## Known limitations','Raw q-136549 omits difficulty, worked solution and correct ref; it cannot run through a keyed native grading fixture. A completed record with identical prompt and bank is separately graded after independent derivation of -1/2. Negative square-root and fractional opaque scalar distractors preserve complete banks in evidence profiles without claims about historical author intent. See validation.json for exact denominators and canonical meaningful task counts separately from period-shift presentation variants.']
(ROOT/'review.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
(ROOT/'review.md').write_text('\n\n'.join(pages).replace(g.IMAGE,'tangent-source.png')+'\n')
p=ROOT/'template-extraction.md';s=p.read_text();s=s.split('\n## Per-option source recipe appendix')[0];p.write_text(s+'\n'.join(appendix)+'\n')
