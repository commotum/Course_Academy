"""Non-runtime diagnostic: test whether small equivalent equation scalings remove length cues."""
import json
from pathlib import Path
import random
import re
import sys
from collections import defaultdict
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from math_reader import expression,Z,D
ORIGINAL={'q-14315':3,'q-8745':1,'q-14314':3,'q-14316':1,'q-14323':1,'q-8747':1,'q-90601':2,'q-90600':3}
def main():
    rows=json.loads((ROOT/'evidence/records.json').read_text());groups=defaultdict(list)
    for r in rows:
        t=r['generation']['template'];k=r['generation']['parameters']['k'];f=r['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];values=[]
        for a in choices:
            value=a[':answer/value']
            if k!=ORIGINAL[t]:
                left,right=value.split('=');coefficient=expression(left)/Z;rhs=expression(right)
                scale=random.Random(f'{t}:{k}:{a[":answer/id"]}:scale').choice([1,2,3])
                value=r'\left('+sp.latex(scale*coefficient)+r'\right)'+D+'='+sp.latex(scale*rhs)
            values.append(value)
        sizes=[len(re.sub(r'\\(?:left|right|operatorname)|[{}\s]|\u2061','',value)) for value in values];j=next(i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1])
        groups[t].append((sizes[j]==min(sizes) and sizes.count(min(sizes))==1,sizes[j]==max(sizes) and sizes.count(max(sizes))==1))
    results={t:{'records':len(c),'shortest_hits':sum(a for a,b in c),'longest_hits':sum(b for a,b in c)} for t,c in groups.items()}
    (ROOT/'evidence/equivalent-scaling-experiment.json').write_text(json.dumps({'adopted':False,'results':results,'conclusion':'Small common multipliers do not remove the main cues. No runtime changes made or mathematical variety claimed.'},indent=2)+'\n')
    print(json.dumps({'adopted':False,'perfect_cue_families':[t for t,c in results.items() if c['shortest_hits']==c['records'] or c['longest_hits']==c['records']]}))
if __name__=='__main__':main()
