"""Full snapshot scan without requiring a particular existing TeX environment."""
import collections,json,sys,re
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/structural-math-2026-10-26';sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,normalize_limit_operators,normalize_piecewise_cases,normalize_sized_bars,legacy_choice
attrs={'question/problem','question/worked-solution','tutorial/content','answer/value','answer/feedback','answer-field/feedback','multistep/context','multistep/content','assigned-problem/instructions'}
meta=json.loads((W/'metadata.json').read_text());potential=[];counts=collections.Counter();fields={(f['entity'],f['attribute']):f for f in json.loads((H/'fields.json').read_text())};seen=set()
for line in(W/'after.jsonl').open():
 d=json.loads(line);e,a,v=d['e'],d['a'],d['v'];counts['facts']+=1
 if a=='answer/type':meta.setdefault(str(e),{})[a]=v
 if isinstance(v,str):counts['strings']+=1
 if(e,a)in fields:assert v==fields[e,a]['after'];seen.add((e,a))
 if a in attrs and isinstance(v,str)and('lim'in v or'\\mid'in v or'{'in v and(';'in v or'\\begin{aligned}'in v)):potential.append(d)
remaining=[];classes=collections.Counter()
for d in potential:
 math_answer=d['a']=='answer/value'and meta.get(str(d['e']),{}).get('answer/type')==17592186045498
 reasons=set()
 def fix(whole):
  match=MATH.fullmatch(whole);size=(2 if whole.startswith(('$$',r'\[',r'\('))else 1)if match else 0;body=whole[size:-size]if size else whole
  for name,fn in [('limit-operator',normalize_limit_operators),('piecewise-brace',normalize_piecewise_cases),('sized-bar',normalize_sized_bars),('flattened-system',legacy_choice)]:
   new=fn(body)
   if new!=body:reasons.add(name)
   body=new
  return whole[:size]+body+whole[-size:]if size else body
 after=fix(d['v'])if math_answer else MATH.sub(lambda m:fix(m[0]),d['v'])
 if after!=d['v']:remaining.append({**d,'after':after,'math_answer':math_answer,'reasons':sorted(reasons)});classes.update(reasons)
assert len(seen)==len(fields);(H/'postscan-remaining.json').write_text(json.dumps(remaining,indent=2)+'\n');report={'basis_t':json.loads((W/'after.manifest.json').read_text())['basis_t'],**counts,'repaired_fields_verified':len(seen),'remaining_fields':len(remaining),'remaining_classes':dict(classes)};(H/'postscan-initial.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
