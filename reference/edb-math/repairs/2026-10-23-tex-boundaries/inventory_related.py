import json,re,collections,sys
from pathlib import Path
sys.path.insert(0,'scripts/question_capture');from math_format import MATH
H=Path('reference/edb-math/repairs/2026-10-23-tex-boundaries');P=Path('.local/edb/tex-boundary-current.jsonl');attrs={'question/problem','question/worked-solution','tutorial/content','multistep/context','answer/feedback','answer-field/feedback','assigned-problem/instructions'};out=[];seen=set();stats=collections.Counter()
for r in map(json.loads,P.open()):
 if r['a'] not in attrs or (r['e'],r['a']) in seen:continue
 seen.add((r['e'],r['a']));s=r['v'];outside=MATH.sub(lambda m:' '*len(m[0]),s);k=[]
 if re.search(r'(?<!\\)\$',outside):k.append('unpaired-dollar')
 if re.search(r'\[(?:/?math|/?latex|/?tex|/?displaymath)\]',s):k.append('legacy-bracket-delimiter')
 if re.search(r'\${3,}',s):k.append('dollar-run')
 if re.search(r'(?m)^\s*\|.*(?<!\\)\$\$\s*\|',s):k.append('empty-table-math')
 if re.search(r'(?<!\\)\\(?:begin|end)\{',outside):k.append('unprotected-environment')
 if re.search(r'(?<!\\)\\(?:d?frac|sqrt|sum|int|prod|lim)\b',outside):k.append('unprotected-command')
 if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',s):k.append('control-character')
 if k:out.append({**r,'kinds':k});stats.update(k)
(H/'related-inventory.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print('strings scanned',len(seen),'flagged',len(out),'kinds',stats)
for kind in ['legacy-bracket-delimiter','control-character','unpaired-dollar','dollar-run']:
 print('\n',kind)
 for r in [r for r in out if kind in r['kinds']][:7]:print(r['e'],r['a'],repr(r['v'][:210]))
