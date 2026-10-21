"""Refresh scoped source evidence and exact replay masks from a captured EDB basis."""
import copy, importlib.util, json, re, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[2]/'scripts/question_capture'))
from edn import loads

def clean(s):
    return re.sub(r'\\{2,}',lambda m:'\\',s)

def capacity(q):
    text=q[':question/problem']
    m=re.search(r'(?:maximum.+?is|maximum capacity is) \$(\d+)\$',text)
    assert m,text
    return int(m[1])

def make_specs(kp):
    out={}
    for q in kp[':knowledge-point/questions']:
        A=capacity(q);f=q[':question/answer-fields'][0]
        m=re.search(r'(?:initially (?:has|contains|houses)|currently has) \$(\d+)\$',q[':question/problem'])
        I=int(m[1]) if m else None
        symbol=re.search(r'\$([A-Z])\(t\)\$',q[':question/problem']).group(1)
        def mask(s,n,name):return re.sub(r'(?<!\d)'+str(n)+r'(?!\d)','<<'+name+'>>',s)
        prompt=mask(q[':question/problem'],A,'capacity')
        if I is not None:prompt=mask(prompt,I,'initial')
        choices=[]
        for a in f[':answer-field/choices']:
            rhs=clean(a[':answer/value']).split('=',1)[1]
            nums=re.findall(r'(?<![\w])\d+',rhs)
            # All source options consist of one gap/sum constant, with optional squared population.
            nums=[int(n) for n in nums if int(n)!=2 or A==2]
            assert len(nums)==1,(a,nums)
            n=nums[0]
            choices.append({'mask':mask(a[':answer/value'],n,'constant'),'numerator':n,'denominator':A,'original':a[':answer/value'],'correct':bool(f.get(':answer-field/correct') and a[':answer/id']==f[':answer-field/correct'][':answer/id'])})
        out[q[':question/math-academy-id']]={'db_id':q[':db/id'],'capacity':A,'initial':I,'symbol':symbol,'problem_mask':prompt,'solution_mask':mask(q[':question/worked-solution'],A,'capacity') if q.get(':question/worked-solution') else None,'difficulty':str(q[':question/difficulty'][':db/ident']) if q.get(':question/difficulty') else None,'choices':choices,'source_error':'quantity in units but capacity in units/day' if q[':question/math-academy-id']=='q-106691' else None}
    return out

if __name__=='__main__':
    kp=loads((HERE/'reference/initial/before.edn').read_text())
    specs=make_specs(kp)
    (HERE/'current-source-recipes.json').write_text(json.dumps({'basis':2578,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','sources':specs},indent=2,ensure_ascii=False)+'\n')
