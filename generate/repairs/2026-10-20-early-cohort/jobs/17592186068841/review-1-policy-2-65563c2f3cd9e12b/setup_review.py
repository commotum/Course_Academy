import json,hashlib,shutil
from pathlib import Path
E=Path(__file__).resolve().parent; J=E.parent; P=J/'workspace'; O=J/'review-0-policy-2-75766812ae9ead5b'
def save(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')
save('package-before.json',{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()})
provenance=[]
for name in ['review.py','independent_math.py','grade_and_pairs.py','reproduce_failures.py']:
 shutil.copyfile(O/name,E/name);provenance.append({'file':name,'source':str(O/name),'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest()})
s=(E/'review.py').read_text().replace('[-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9,10,11,12]','[-12,-2,-1,1,2,12]')
s=s.replace("[('easy_linear','easy',2,-2),", "[('q-128198','moderate',1,8),('q-128191','moderate',1,4),('easy_linear','easy',2,-2),")
(E/'review.py').write_text(s)
s=(E/'independent_math.py').read_text().replace("n=int(re.search(r'\\$y=-(\\d+)\\(',q[':question/problem'])[1]);expr=-n/(expr+K)","m=re.search(r'\\$y=-(\\d+)\\(',q[':question/problem']);expr=-int(m[1])/(expr+K) if m else s.sqrt(expr+K)")
(E/'independent_math.py').write_text(s)
# Redirect all author regression writes into this review; unchanged test body.
shutil.copyfile(P/'checks/printed_math.py',E/'printed_math.py')
s=(P/'checks/regressions.py').read_text().replace("W=Path(__file__).resolve().parents[1]",f"W=Path({str(P)!r})").replace("EV=W/'evidence';EV.mkdir(exist_ok=True)","EV=Path(__file__).resolve().parent/'author-rerun';EV.mkdir(exist_ok=True)")
(E/'author_regressions.py').write_text(s)
(E/'author-rerun').mkdir(exist_ok=True)
for name in ['before.json','before-grader-input.json']:
 shutil.copyfile(P/'evidence'/name,E/'author-rerun'/name)
save('reuse-provenance.json',provenance)
print('Evidence scripts copied and adapted; package hashes captured')
