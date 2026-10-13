"""One-time extraction: compiled masks are the generator's runtime recipes."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('gen',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def mathparse(t):
    t=t.replace('−','-').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').strip().removesuffix('.')
    def group(text,i):
        assert text[i]=='{',(text,i)
        depth=1;j=i+1
        while depth:
            if text[j]=='{':depth+=1
            if text[j]=='}':depth-=1
            j+=1
        return text[i+1:j-1],j
    def convert(text):
        out='';i=0
        while i<len(text):
            if text.startswith(r'\frac',i):
                a,j=group(text,i+5);b,i=group(text,j);out+='(('+convert(a)+')/('+convert(b)+'))'
            elif text.startswith(r'\sqrt',i):
                a,i=group(text,i+5);out+='sqrt('+convert(a)+')'
            elif text[i]=='{':
                a,i=group(text,i);out+='('+convert(a)+')'
            elif text[i]=='^':out+='**';i+=1
            else:out+=text[i];i+=1
        return out
    return parse_expr(convert(t),local_dict={'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))

def numeric_rows(q):
    sol=q.get(':question/worked-solution','');res=[]
    for ib,block in enumerate(re.finditer(r'\\begin\{aligned\}.*?\\end\{aligned\}',sol,re.S)):
        which=['P','Q','R'][ib]
        for ir,rhs in enumerate(re.finditer(r' & =(.*?)(?= \\\\  & =|\\end\{aligned\})',block.group(),re.S)):
            if which in ('P','Q') and ir<2:continue
            value=rhs.group(1);punct='.' if value.endswith('.') else '';value=value.removesuffix('.')
            begin=block.start()+rhs.start(1);end=block.start()+rhs.end(1)-len(punct)
            res.append((begin,end,value,which,ir))
    return res
r=json.load(open(ROOT/'source.json'))['record'];recipes={};cases=[];normalized=[];unmapped=[]
for q in r[':knowledge-point/questions']:
    sid=q[':question/math-academy-id'];prompt=q[':question/problem'];vectors=re.findall('⟨([^⟩]+)⟩',prompt)
    p={'a':[str(mathparse(x)) for x in vectors[0].split(',')],'b':[str(mathparse(x)) for x in vectors[1].split(',')],'operation':'single' if 'scalar projection' in prompt else ('sum' if '+' in prompt.split('Find',1)[1] else 'difference')}
    d=g.data(p);f=q[':question/answer-fields'][0];level=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1];kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
    mask=prompt.replace('⟨'+vectors[0]+'⟩','@A@',1).replace('⟨'+vectors[1]+'⟩','@B@',1)
    root_forms={key:[i for i,x in enumerate(vectors[j].split(',')) if x.strip().startswith(r'\sqrt')] for j,key in enumerate(('a','b'))}
    for key in ('a','b'):d[key+'t']=[r'\sqrt{'+g.tex(x*x)+'}' if i in root_forms[key] else g.tex(x) for i,x in enumerate(d[key])]
    recipe={'root_forms':root_forms,'level':level,'field_type':kind,'prompt_mask':mask,'parameters':p,'reference_result':str(d['R']),'correct_missing':':answer-field/correct' not in f,'bank':[],'rows':[]}
    if sid=='q-126501':recipe.update(separator=', ',spaced_negative=True)
    for i,a in enumerate(f[':answer-field/choices']):
        value=mathparse(a[':answer/value']);correct=s.simplify(value-d['R'])==0
        recipe['bank'].append({'name':'correct' if correct else 'observed_'+str(i),'ratio':str(s.simplify(value/d['R'])),'mask':r'\left(@MULTIPLIER@\right)\left('+a[':answer/value']+r'\right)','original_value':a[':answer/value'],'interpretation':'opaque complete-expression ratio; evidence-only, no error-intent inference'})
    if ':question/worked-solution' in q:
        rows=numeric_rows(q);solution=q[':question/worked-solution']
        for i,(a,b,original,which,ir) in enumerate(rows):
            candidates=[]
            if which in ('P','Q'):
                if which=='P' and ir==2:
                    candidates=[f'sub:{sty}:{nst}:{bare}' for sty in ['dot','paren'] for nst in ['default','braced_radical'] for bare in ['0','1']]
                elif which=='Q' and ir==2:candidates=['known_dot','known_dot_braced']
                else:candidates=['raw','raw_inside','norm','norm_inside','eval','final','rationalized']
            else:candidates=['combine','combine_raw','factor','lcm','common_radical','collect_same_den','result']
            rendered=[]
            for tag in candidates:
                try:rendered.append((tag,g.row_value(tag,d,which)))
                except Exception:pass
            exact=[tag for tag,v in rendered if v==original]
            if exact:tag=exact[0]
            else:
                # Source spelling may have an unreduced radical fraction; keep stage shape.
                equiv=[tag for tag,v in rendered if s.simplify(mathparse(v)-mathparse(original))==0]
                if not equiv:unmapped.append((sid,i,original,rendered));tag='UNKNOWN'
                else:
                    tag=('final' if which!='R' and 'final' in equiv and i==len(rows)-1 else equiv[0]);normalized.append({'source_id':sid,'row':i,'original':original,'normalized':g.row_value(tag,d,which),'tag':tag})
            recipe['rows'].append({'tag':tag,'which':which,'original':original})
        for i,(a,b,original,which,ir) in reversed(list(enumerate(rows))):solution=solution[:a]+'@ROW'+str(i)+'@'+solution[b:]
        recipe['solution_mask']=solution
    recipes[sid]=recipe;cases.append({'source_id':sid,'template':sid,'level':level,'parameters':p,'bank_profile':'observed:'+sid})
(ROOT/'recipes.json').write_text(json.dumps(recipes,indent=2,ensure_ascii=False)+'\n');(ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(ROOT/'notation-normalizations.json').write_text(json.dumps(normalized,indent=2)+'\n')
print('recipes',len(recipes),'normalizations',normalized,'unmapped',unmapped)
assert not unmapped
