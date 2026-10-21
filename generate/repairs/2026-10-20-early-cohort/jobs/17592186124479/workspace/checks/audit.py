"""Independent checks of visible matrices, annotations, and answer banks."""
import re
import sympy as S
def matrices(text):
    return [S.Matrix([[S.Rational(c.strip()) for c in r.split('&')] for r in body.split(r'\\')])
            for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def field(r):return r['question'][':question/answer-fields'][0]
def answer(r):
    f=field(r);key=f[':answer-field/correct'];key=key[':answer/id'] if isinstance(key,dict) else key[1]
    return int(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key))
def check(r):
    q=r['question'];a=matrices(q[':question/problem'])[0];states=matrices(q[':question/worked-solution'])
    errors=[]
    if states[0]!=a:errors.append('solution starts with other matrix')
    if int(a.rank())!=answer(r):errors.append('wrong key')
    if not states[-1].is_echelon:errors.append('final not REF')
    for i,(before,after) in enumerate(zip(states,states[1:])):
        changed=[j for j in range(a.rows) if before.row(j)!=after.row(j)]
        if len(changed)!=1:errors.append('not one row replacement');continue
        j=changed[0];delta=after.row(j)-before.row(j)
        candidates=[]
        for k in range(a.rows):
            if k==j:continue
            h=next((h for h in range(a.cols) if before[k,h]),None)
            if h is not None:
                c=delta[h]/before[k,h]
                if c and delta==c*before.row(k):candidates.append((j,k,c))
        if not candidates:errors.append('not elementary row equivalent')
        # Verify the displayed annotation, independently of generation metadata.
        clean=q[':question/worked-solution'].replace(r'\left', '').replace(r'\right', '')
        annotations=re.findall(r'\{R\}_\{(\d+)\} :=\{R\}_\{\1\}\+\((.*?)\)\{R\}_\{(\d+)\}',clean)
        if i>=len(annotations):errors.append('missing operation annotation')
        else:
            dest,c,src=annotations[i]
            frac=re.fullmatch(r'(-?)\s*\\frac\{(\d+)\}\{(\d+)\}',c)
            coefficient=S.Rational((-1 if frac[1] else 1)*int(frac[2]),int(frac[3])) if frac else S.Rational(c)
            if (int(dest)-1,int(src)-1,coefficient) not in candidates:errors.append('wrong displayed operation')
    endrank=sum(any(states[-1].row(i)) for i in range(a.rows))
    if endrank!=answer(r):errors.append('pivot count inconsistent')
    if f'${answer(r)}$ pivots' not in q[':question/worked-solution']:errors.append('wrong conclusion')
    return {'id':q[':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],
            'shape':[a.rows,a.cols],'rank':int(a.rank()),'errors':errors}
