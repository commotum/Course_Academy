import json,re,sys,difflib
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import normalize_prose,normalize_tex
p=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/foundations')
def sig(s):return re.sub(r'\s|[{}]|\\(?:left|right|displaystyle)|⁡','',s).replace('\\operatorname','\\').replace('\\text','').replace('\\textrm','').replace('\\mathrm','')
for d in sorted(p.glob('175*')):
 qs={q[':db/id']:q for q in json.load(open(d/'questions-before.json'))};rows=[]
 for r in json.load(open(d/'reextracted.json')):
  q=qs[r['entity']];row={'entity':r['entity'],'mid':r['mid']}
  for role,key,attr in [('prompt_sources','problem',':question/problem'),('solution_sources','worked_solution',':question/worked-solution')]:
   new=r.get(role,{}).get(key,'');old=q.get(attr,'')
   if new and old and sig(new)!=sig(old):row[key]={'similarity':round(difflib.SequenceMatcher(None,sig(old),sig(new),autojunk=False).ratio(),3),'old_length':len(old),'source_length':len(new)}
  ff=r.get('prompt_sources',{}).get('fields',[])
  for f in q.get(':question/answer-fields',[]):
   src=next((x for x in ff if x['key']==f[':answer-field/key']),None)
   if src:
    srcvs={sig(a['value'])for a in src.get('choices',[])}
    alien=[a[':answer/value']for a in f[':answer-field/choices']if sig(a[':answer/value'])not in srcvs]
    if alien:row.setdefault('alien_choices',[]).append({'field':f[':db/id'],'values':alien})
  rows.append(row)
 (d/'source-comparison.json').write_text(json.dumps(rows,indent=2));print(d.name)
 print([(r['entity'],r.get('problem'),r.get('worked_solution'))for r in rows if any(r.get(k,{}).get('similarity',1)<.90 for k in ['problem','worked_solution'])])
 print('aliens',[(r['entity'],r['alien_choices'])for r in rows if r.get('alien_choices')][:6])
