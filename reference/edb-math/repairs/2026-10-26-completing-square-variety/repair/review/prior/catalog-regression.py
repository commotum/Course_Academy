import sys,importlib.util,json,re
from pathlib import Path
from fractions import Fraction as F
W=Path(sys.argv[1]).resolve();sys.path.insert(0,str(W.parent))
spec=importlib.util.spec_from_file_location('tested_generator',W);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Probe the full supported pool using the public CLI-equivalent callable.
# Original inputs are independent constants, not extracted from generator metadata.
anchors={(7,F(5,4)),(7,F(8)),(11,F(25)),(11,F(30)),(3,F(3))}
report={}
for band in ('easy','moderate','hard'):
 try:g.generate(band,100000,49173)
 except ValueError as e:lo=int(re.search(r'band has (\d+) semantic',str(e))[1])
 records=g.generate(band,lo,49173)
 def cparse(s):
  s=re.sub(r"\\frac\{(-?\d+)\}\{(\d+)\}",r"\1/\2",s)
  return F(s)
 seen=set()
 for r in records:
  p=r['question'][':question/problem'];s=re.search(r"\$([^$]+)\$",p)[1]
  if band=='hard':
   c,m=re.match(r"(.+?)-(\d+)[xytz]\+[xytz]\^2",s).groups()
  else:
   m,c=re.match(r"[xytz]\^2-(\d+)[xytz](.*)",s).groups();c=c.lstrip('+') or '0'
  seen.add((int(m),cparse(c)))
 missing=sorted((m,str(c)) for m,c in anchors-seen)
 report[band]={'capacity':lo,'missing_complete_source_inputs':missing,'negative_original_constant':any(c<0 for m,c in seen)}
print(json.dumps(report,indent=2))
assert all(not r['missing_complete_source_inputs'] and r['negative_original_constant'] for r in report.values()),'Legitimate source-style original constants suppressed'
