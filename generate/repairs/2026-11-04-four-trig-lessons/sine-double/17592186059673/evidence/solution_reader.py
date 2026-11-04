"""Numeric witnesses for derivation equalities; retain every parse limitation."""
import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from numeric_audit import MATH,Numeric,nodes,target

def check(q,label,kid):
    solution=q.get(':question/worked-solution','')
    if not solution.strip():return {'label':label,'kp':kid,'status':'missing','checks':0}
    checked=0;bad=[];unparsed=[]
    for point in [.371,.823,1.197]:
        bind={n:point+off for n,off in [('x',0),('y',.17),('t',.23),('w',.31),('theta',.43),('u',.51),('v',.63),('A',.71),('B',.83),('a',.91),('b',1.03)]}
        try:bind['E']=Numeric(nodes(target(q)),bind).evaluate()
        except Exception:pass
        for span in MATH.finditer(solution):
            body=span[0].strip('$').strip()
            if '=' not in body:continue
            body=re.sub(r'\\(?:begin|end)\{aligned\}','',body)
            body=re.sub(r'\\cancel(?![A-Za-z])','',body)
            body=re.sub(r'\\color\{[^{}]+\}','',body)
            body=body.replace('&','').replace(r'\qquad','').replace(r'\quad','')
            lines=[s.strip().rstrip('.,;:') for s in re.split(r'\\\\|(?<!\\),',body)];combined=[]
            for line in lines:
                if not line:continue
                if '=' not in line and combined:combined[-1]+=line
                else:combined.append(line)
            previous=None
            for line in combined:
                parts=[p.strip().rstrip('.,;:') for p in line.split('=')]
                if len(parts)<2:continue
                if parts[0] in ('x','y','t','w','u','v','s','c','a','b','A','B') and len(parts)==2:
                    try:bind[parts[0]]=Numeric(nodes(parts[1]),bind).evaluate()
                    except Exception:pass
                    continue
                if parts[0]:previous=parts[0]
                for right in parts[1:]:
                    if not previous:previous=right;continue
                    try:
                        a=Numeric(nodes(previous),bind).evaluate();b=Numeric(nodes(right),bind).evaluate();checked+=1
                        if abs(a-b)>1e-7*max(1,abs(a),abs(b)):bad.append({'left':previous,'right':right,'values':[a,b]})
                    except Exception as e:unparsed.append({'left':previous,'right':right,'error':str(e)})
                    previous=right
    # Keep unique witnesses rather than printing a failure at each test point.
    def uniq(rows):return list({json.dumps({k:v for k,v in r.items() if k!='values'},sort_keys=True):r for r in rows}.values())
    return {'label':label,'kp':kid,'status':'checked','checks':checked,'suspected_bad_equalities':uniq(bad),'unparsed_equalities':uniq(unparsed)}
