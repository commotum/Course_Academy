"""Compare each original compound equation to the pinned curriculum; exact-anchor proposals only."""
from pathlib import Path
import collections,html,importlib.util,json,re
from scripts.question_capture.math_format import MATH,normalize_tex,validate_tex
P=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('previous_matrix_audit',P.parent/'2026-10-15-compound-math-loss/audit.py');a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
lookup={x['html']:x for x in json.loads((P/'source-mml-extracted.json').read_text())}
records={}
for kind in ['question','tutorial']:
 for q in json.loads((P/(kind+'s.json')).read_text()):
  if ':'+kind+'/math-academy-id' in q:records[(kind,q[':'+kind+'/math-academy-id'])]=q
results=[];changes={}
def norm(t):return a.norm(normalize_tex(t))
for c in json.loads((P/'source-candidates.json').read_text()):
 rec=records.get((c['kind'],c['sourceId']));base={k:c[k] for k in ['lessonId','kind','sourceId','attribute','sourceFile','line','domId']}
 if not rec:results.append({**base,'status':'not-in-current-scope-projection'});continue
 base['entity']=rec[':db/id'];extracted=[]
 def replace(m):
  fragments=a.MML.findall(m[0]);assert len(fragments)==1
  x=lookup[fragments[0]];assert not x['errors'],x['errors'];t=x['problem'];assert t.startswith('$') and t.endswith('$');t=t.strip('$').strip();extracted.append(t);return t
 try:
  full=normalize_tex(html.unescape(a.CONTAINER.sub(replace,c['sourceTitleHtml'])).strip());validate_tex(full)
 except (ValueError,AssertionError,KeyError) as ex:results.append({**base,'status':'unsupported-source','error':str(ex)});continue
 first=extracted[0];key=(base['entity'],c['attribute']);text=changes.get(key,{}).get('new',rec.get(':'+c['attribute'],''))
 if c['attribute']=='answer/value':
  texts=[ch[':answer/value'] for f in rec.get(':question/answer-fields',[]) for ch in f.get(':answer-field/choices',[])]
  results.append({**base,'status':'answer-bank-present' if any(norm(full)==norm(t) for t in texts) else 'answer-bank-review','full':full});continue
 if norm(full) in norm(text):results.append({**base,'status':'complete','full':full});continue
 # A canonical matrix-layout block can split the equation across several math spans.
 full_matrices=a.current_matrices(full);actual=a.current_matrices(text);labels=re.findall(r'([A-Z])=FORMULA',a.norm(c['outerTex']))
 if full_matrices and all(m in actual for m in full_matrices) and all(re.search(r'(?<![A-Za-z])'+l+r'=',norm(text)) for l in labels):
  results.append({**base,'status':'matrices-and-labels-present','full':full});continue
 matches=[m for m in MATH.finditer(text) if norm(m[0].strip('$'))==norm(first)]
 if len(matches)==1 and norm(first)!=norm(full):
  m=matches[0];new=text[:m.start()]+'$$\n'+full+'\n$$'+text[m.end():]
  change=changes.setdefault(key,dict(entity=key[0],attribute=key[1],old=rec.get(':'+c['attribute'],''),new=text,sources=[]));change['new']=new;change['sources'].append({**base,'first':first,'full':full});results.append({**base,'status':'exact-first-fragment-loss','full':full})
 else:results.append({**base,'status':'review','full':full,'first':first,'anchorCount':len(matches)})
(P/'source-comparison.json').write_text(json.dumps(results,indent=2));(P/'source-proposals.json').write_text(json.dumps(list(changes.values()),indent=2));print(collections.Counter(x['status'] for x in results));print('Proposals',len(changes));print('Priority',[(v['entity'],v['attribute']) for v in changes.values() if any(s['lessonId'] in [862,146,232] for s in v['sources'])])
