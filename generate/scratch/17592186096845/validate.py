"""Source-bank replay, displayed LaTeX differentiation and real engine grading."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from functools import lru_cache
import sympy as s
sys.path.insert(0,'/home/jake/.cache/uv/wheels-v5/pypi/lark/1.2.2-py3-none-any')
from sympy.parsing.latex import parse_latex
from lark import Tree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
def norm(t):
    t=t.strip().rstrip('.,').replace('\u2061','').replace(r'\,','').replace(r'\cdot','*')
    t=re.sub(r'\\operatorname\{(sin|cos|tan|ln)\}',lambda m:'\\'+m[1],t)
    t=t.replace('{sin}',r'\sin').replace('{sec}',r'\sec')
    t=re.sub(r'\\(sec|sin)\^\{([0-9]+)\}\s*([x]|\([^()]*\))',lambda m:'{\\'+m[1]+'('+m[3]+')}^{'+m[2]+'}',t)
    t=re.sub(r'\\(sin|cos|tan|ln)\s*([0-9]*[x]|a)',lambda m:'\\'+m[1]+'('+m[2]+')',t)
    matches=list(re.finditer(r'\\(?:sin|cos|tan|sec|ln)\(',t))
    for m in reversed(matches):
        depth=1;end=m.end()
        while depth:
            if t[end]=='(':depth+=1
            if t[end]==')':depth-=1
            end+=1
        t=t[:m.start()]+'{'+t[m.start():end]+'}'+t[end:]
    t=re.sub(r'\{([aex])\}',r'\1',t)
    t=re.sub(r'(?<=[0-9x}\)])(?=\\(?:sqrt|sin|cos|tan|sec|ln))','*',t)
    t=re.sub(r'(?<=\))(?=[a-z{])','*',t)
    t=re.sub(r'(?<=[0-9x}\)])(?=\{\\(?:sin|cos|tan|sec|ln))','*',t)
    t=re.sub(r'(?<=\})(?=\()','*',t)
    t=re.sub(r'(?<=\})(?=\{)','*',t)
    return t
@lru_cache(None)
def expr(t):
    substitutions={s.Symbol('P'):s.pi}
    t=t.replace(r'\pi','P')
    def group(text,i):
        assert text[i]=='{',text
        depth=1;j=i+1
        while depth:
            if text[j]=='{':depth+=1
            if text[j]=='}':depth-=1
            j+=1
        return text[i+1:j-1],j
    while r'\frac' in t:
        pos=t.index(r'\frac');num,end=group(t,pos+5);den,stop=group(t,end)
        token=chr(ord('Z')-len(substitutions));substitutions[s.Symbol(token)]=expr(num)/expr(den)
        t=t[:pos]+token+t[stop:]
    try:z=parse_latex(norm(t),backend='lark')
    except Exception as e:raise AssertionError(('parse',t,norm(t))) from e
    if isinstance(z,Tree):
        vals=[v for v in z.children if isinstance(v,s.Basic)]; assert vals and all(s.simplify(v-vals[0])==0 for v in vals), (t,z);z=vals[0]
    z=z.subs(substitutions)
    return z.subs({v: {'x':g.x,'a':g.a,'e':s.E}.get(v.name,v) for v in z.free_symbols})
def equal(a,b):return s.simplify(s.trigsimp(a-b))==0

def fingerprint(q):
    # Normalize mathematical function from visible prompt; source tasks use same response.
    text=q[':question/problem'];spans=re.findall(r'\$([^$]+)\$',text)
    equation=next((t for t in spans if t.startswith('y=') or t.startswith('f(x)=') or t.startswith('y =')),None)
    if equation is None:return 'excluded|'+hashlib.sha256(text.encode()).hexdigest()
    fun=expr(equation.split('=',1)[1].rstrip(',').rstrip('.'))
    if 'slope' in text:
        point=next((t.split('=')[1].rstrip('.') for t in spans if t.startswith('x=')),None)
        shape='slope@'+s.srepr(expr(point)) if point else 'slope-context'
    elif '{{field-1}}' in text and ')' in text.split('{{field-1}}')[1]:shape='fragment'
    else:shape='derivative'
    return hashlib.sha256((s.srepr(fun)+'|'+shape).encode()).hexdigest()

def independent(rec):
    q,md=rec['question'],rec['generation'];m=md['template'];p=md['parameters']
    assert rec==g.generate(q[':question/difficulty'].split('/')[-1],md['seed'],m,p,md['bank_profile'])
    spans=re.findall(r'\$([^$]+)\$',q[':question/problem'])
    equation=next(t for t in spans if t.startswith('y=') or t.startswith('f(x)=') or t.startswith('y ='))
    fun=expr(equation.split('=',1)[1].rstrip(',').rstrip('.'));expected=s.diff(fun,g.x)
    if m=='q-10009':expected=expected.subs(g.x,s.pi/2)
    elif m=='q-9944':expected=expected.subs(g.x,0)
    elif m.startswith('q-343'):expected=s.simplify(expected/s.exp((p['k'] if m!='q-343332' else 1)*g.x))
    f=q[':question/answer-fields'][0];values=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
    correct=next(expr(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    assert equal(correct,expected),(m,p,'answer',correct,expected)
    assert sum(equal(v,expected) for v in values)==1
    assert not any(equal(v,w) for i,v in enumerate(values) for w in values[i+1:])
    # Every explicit derivative multiplication/simplification row must differentiate the prompt.
    block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)[0]
    for rhs in block.split(' & =')[1:]:
        rhs=rhs.split(r'\\')[0].strip().rstrip('.')
        if "u}^{" in rhs or "v}^{" in rhs:continue
        assert equal(expr(rhs),s.diff(fun,g.x)),(m,p,'solution',rhs)
    for text in (q[':question/problem'],q[':question/worked-solution']):
        assert text.count('$')%2==0 and text.count('{')==text.count('}')
    assert q[':question/problem'].count('{{field-1}}')==(1 if f[':answer-field/type']==':answer-field.type/blank' else 0)
    assert len(set(a[':answer/id'] for a in f[':answer-field/choices']))==len(values)
    assert fingerprint(q)==fingerprint(g.generate(q[':question/difficulty'].split('/')[-1],template=m,parameters=p)['question'])

def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    if f[':answer-field/type']==':answer-field.type/radio':
        return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every source-profile selection through actual engine'} for a in f[':answer-field/choices']]
    ans=f[':answer-field/choices'][0][':answer/value']
    return [{'field_index':0,'submitted':t,'expected':ex,'purpose':'Equivalent fragment and wrong answer through actual engine'} for t,ex in [(ans,'accepted'),('('+ans+')+0','accepted'),('0','rejected'),('('+ans+')+1','rejected')]]

def main():
    cases=[];replays=[];records=[];review=[]
    for m,p in g.DEFAULTS.items():
        old=g.SOURCES[m];level=old[':question/difficulty'][':db/ident'].split('/')[-1];rec=g.generate(level,template=m,parameters=p);independent(rec)
        q=rec['question'];f=q[':question/answer-fields'][0];oldf=old[':question/answer-fields'][0]
        assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in oldf[':answer-field/choices'])
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==oldf[':answer-field/correct'][':answer/value']
        cases.append({'source':m,'template':m,'profile':rec['generation']['bank_profile'],'matched_values':len(f[':answer-field/choices']),'total_values':len(f[':answer-field/choices']),'complete_bank':True,'exact_prompt':True,'exact_solution':True,'missing':[],'extra':[]});replays.append(rec)
        review.append('## Original and exact replay '+m+'\n\n'+g.markdown(rec))
    for level in g.SUPPORTED_LEVELS:
        for rec in g.batch(level,24,1962):independent(rec);records.append(rec)
        review.append('## '+level+' variants\n\n'+'\n\n---\n\n'.join(g.markdown(r) for r in records[-3:]))
    for m in g.VARIABLE:
        for k in ((3,12) if m=='q-9942' else (2,12)):
            p={'k':k}
            if m=='q-343354':p['c']=6
            if m=='q-9942':p['b']=-5 if k==3 else 0
            rec=g.generate(g.SOURCES[m][':question/difficulty'][':db/ident'].split('/')[-1],template=m,parameters=p);independent(rec);records.append(rec)
    allrecords=replays+records;save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(allrecords)])
    binary=ROOT/'generate/runs/current/check-engine'
    r=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True);(HERE/'engine.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    save('source-cases.json',cases);save('review.json',{'replays':replays,'variants':records});(HERE/'review.md').write_text('\n\n---\n\n'.join(review))
    save('validation.json',{'status':'pass','source_basis':1962,'complete_source_banks':len(cases),'matched_values':sum(c['matched_values'] for c in cases),'missing_options':[],'extra_options':[],'independent_display_checks':len(allrecords),'fidelity':'Exact complete banks, correct designations, prompt and worked solution for every supported source profile; other sources explicitly excluded in classification.','native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',binary]}})
    print('Passed source replay, independent displayed mathematics and engine grading')
if __name__=='__main__':main()
