"""Verify actual printed mathematics independently of generation metadata."""
from collections import Counter, defaultdict
import copy
import importlib.util
import json
from pathlib import Path
import re
import sys
import math

import sympy as s

H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import prepare_records, content_fingerprint, validate_question
from scripts.trig_substitution_batch_policy import validate_delivery_batch
import read_printed as p


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2)+'\n')


def scalar(text):
    text=text.replace(r'\ln u',r'\ln(u)').replace('&','').strip().rstrip('.')
    if text in ('-','+'):
        return s.Integer(-1 if text=='-' else 1)
    # Extend the retained source reader only for explicit n-th root notation.
    while match:=re.search(r'\\sqrt\[(\d+)\]',text):
        arg,end=p.group(text,match.end())
        replacement='(('+str(scalar(arg))+')**(1/'+match[1]+'))'
        text=text[:match.start()]+replacement+text[end:]
    return p.scalar(text)


def integral(text):
    t=text.replace(r'\left','').replace(r'\right','').replace(r'\,','')
    start=t.index(r'\int');prefix=t[:start].strip().rstrip('(').strip()
    factor=scalar(prefix) if prefix else s.Integer(1)
    index=start+4;lo=hi=None
    if t[index:index+1]=='_':
        lo,index=p.group(t,index+1);assert t[index]=='^'
        hi,index=p.group(t,index+1);lo,hi=scalar(lo),scalar(hi)
    match=re.search(r'\\mathrm\{d\}([xu])',t[index:]);assert match,t
    body=scalar(t[index:index+match.start()])
    return factor*body,{'x':p.x,'u':p.u}[match[1]],lo,hi,factor


def equal(a,b):
    difference=s.trigsimp(s.expand(a-b))
    if difference==0:return True
    if difference.has(s.sin,s.cos,s.tan,s.cot,s.sec,s.csc):
        if s.trigsimp(difference.rewrite(s.sin))==0:return True
    if difference.has(s.log):return s.simplify(s.expand_log(difference,force=True))==0
    return s.simplify(difference)==0


def check(record):
    q=record['question'];validate_question(q)
    problem=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/problem'],re.S)[0]
    body,var,lo,hi,_=integral(problem);assert var==p.x
    sol=q[':question/worked-solution']
    inner=scalar(re.search(r'Let \$u=(.*?)\$\.',sol).group(1))
    blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
    du=scalar(blocks[0].split('=',1)[1]);assert equal(du,s.diff(inner,p.x)),('du',sol)
    substitution=next(block for block in blocks if block.count(r'\int')==2)
    left,right=substitution.split('=',1)
    left_body,left_var,left_lo,left_hi,_=integral(left)
    assert left_var==p.x and equal(left_body,body) and left_lo==lo and left_hi==hi
    transformed,u,ulo,uhi,factor=integral(right);assert u==p.u
    assert equal(body,transformed.subs(p.u,inner)*du),('substitution',sol)
    if lo is not None:
        assert s.N(lo)<s.N(hi)
        assert equal(ulo,inner.subs(p.x,lo)) and equal(uhi,inner.subs(p.x,hi)),('bounds',sol)
        bound_block=next(block for block in blocks if r'\Longrightarrow' in block)
        rows=bound_block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
        for row,xvalue,uvalue in zip(rows,(lo,hi),(ulo,uhi)):
            lhs,rhs=row.replace('&','').split(r'\Longrightarrow')
            assert equal(scalar(lhs.split('=',1)[1]),xvalue)
            assert equal(scalar(rhs.split('=',1)[1]),uvalue)
        eval_block=blocks[-2]
        left,right=eval_block.split('=',1)
        if r'\left[' in left:
            prefix,rest=left.split(r'\left[',1)
            prefix=prefix.replace(r'\left(','')
            primitive_tex,limits=rest.split(r'\right]',1)
            primitive=scalar(primitive_tex)*(scalar(prefix) if prefix.strip() else 1)
        else: # times(factor,[ln u] bounds) in the logarithmic family
            start=left.index(r'\left[')
            prefix=left[:start].replace(r'\left(','').strip()
            primitive_tex=left[start+len(r'\left['):].split(r'\right]',1)[0]
            primitive=scalar(primitive_tex)*(scalar(prefix) if prefix else 1)
        assert equal(s.diff(primitive,p.u),transformed),('primitive',eval_block,primitive,transformed)
        expected=s.simplify(primitive.subs(p.u,uhi)-primitive.subs(p.u,ulo))
        assert equal(scalar(right),expected),('evaluation',eval_block)
    else:
        antiderivative=next(block for block in blocks if block.count(r'\int')==1 and '=' in block)
        primitive=scalar(antiderivative.split('=',1)[1])
        assert equal(s.diff(primitive,p.u),transformed),('primitive',sol)
        expected=primitive.subs(p.u,inner)
    field=q[':question/answer-fields'][0];assert len(field[':answer-field/choices'])==1
    key=field[':answer-field/choices'][0][':answer/value']
    assert blocks[-1].strip().rstrip('.')==key,'Unshown final-to-key conversion'
    answer=scalar(key)
    assert equal(answer,expected),('key',key,expected)
    if lo is not None:assert not equal(answer,0),'Zero-answer repetition'
    # Check the actual trig-argument range on every closed definite interval.
    # All supported inner angle functions are monotone powers on positive x or affine.
    if lo is not None:
        for atom in body.atoms(s.sec,s.csc,s.tan,s.cot):
            angle=atom.args[0]
            ends=sorted([float(s.N(angle.subs(p.x,t))) for t in (lo,hi)])
            shift=float(s.pi/2) if atom.func in (s.sec,s.tan) else 0
            bins=[(value+shift)/float(s.pi) for value in ends]
            assert all(abs(value-round(value))>1e-9 for value in bins)
            assert math.floor(bins[0])==math.floor(bins[1]),('pole crossing',ends)
    return key,answer,body


def load(kp):
    path=H/str(kp)/'package/generator.py'
    spec=importlib.util.spec_from_file_location('g'+str(kp),path);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    return g


def main():
    summary={};all_render=[]
    for kp in (17592186068916,17592186068917,17592186068918):
        g=load(kp);directory=H/str(kp)
        pool=[];regression=[];grader=[];coverage=defaultdict(Counter)
        for band in ('easy','moderate','hard'):
            pool.extend(g.batch(band,8,24681357))
            regression.extend(g.batch(band,16,123456))
        for record in pool+regression:
            key,answer,body=check(record)
            band=record['question'][':question/difficulty'].rsplit('/',1)[-1]
            coverage[band][record['generation']['family']]+=1
        assert g.batch('easy',8,24681357)==pool[:8],'Nondeterministic replay'
        for band in ('easy','moderate','hard'):
            validate_delivery_batch([r for r in pool if r['question'][':question/difficulty'].endswith('/'+band)],kp)
        inventory=json.loads((directory/'inventory/inventory.json').read_text())
        existing={content_fingerprint(q) for q in inventory['questions']+[inventory['canonical_example']]}
        accepted,duplicates=prepare_records(pool,kp,g.EVIDENCE['kp']['id'],existing,ROOT,directory/'package')
        assert len(accepted)==24 and duplicates==0
        for row in accepted:check(row)
        for index,row in enumerate(accepted):
            key,answer,_=check(row)
            wrong=s.latex(answer+1) if row['generation']['model']['lower'] is not None else s.latex(2*answer)
            checks=[{'submitted':key,'expected':'accepted'},
                    {'submitted':r'\frac{2\left('+key+r'\right)}{2}','expected':'accepted'},
                    {'submitted':wrong,'expected':'rejected'}]
            grader.append({'label':str(kp)+' '+str(index),'record':row,'checks':checks})
        negatives=[]
        bad=copy.deepcopy(pool[0]);bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+=' + 1'
        try:validate_delivery_batch([bad],kp)
        except ValueError:negatives.append('final/key mismatch rejected')
        else:raise AssertionError('Unshown conversion accepted')
        try:validate_delivery_batch([pool[0],copy.deepcopy(pool[0])],kp)
        except ValueError:negatives.append('amplitude/task clone rejected')
        else:raise AssertionError('Clone accepted')
        for bad_band,bad_count in [('easy',0),('hard',201),('unknown',1)]:
            try:g.batch(bad_band,bad_count,0)
            except ValueError:continue
            raise AssertionError('Unsupported request accepted')
        save(directory/'candidate-pool.json',pool);save(directory/'accepted-pool.json',accepted)
        save(directory/'regression-samples.json',regression);save(directory/'grader-input.json',grader)
        save(directory/'retirement-candidates.json',[q for q in inventory['questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')])
        report={'passed':True,'printed_records_checked':len(pool)+len(regression),'delivery_records_rechecked':len(accepted),
                'pool_counts':dict(Counter(r['question'][':question/difficulty'] for r in accepted)),
                'coverage':{band:dict(counts) for band,counts in coverage.items()},'negative_controls':negatives,
                'mathematical_duplicates_filtered':duplicates,'response_policy':'Authored exact-entry; archived source banks preserved',
                'imported_difficulty_counts':g.EVIDENCE['source_counts'],'authored_band_origins':g.EVIDENCE['band_origin']}
        save(directory/'generator-verification.json',report);summary[str(kp)]=report
        # At least one case per band; include the two complex quotient hard cases.
        all_render.extend([accepted[0],accepted[8],accepted[16]])
        if kp==17592186068918:all_render.extend(next(r for r in accepted if r['generation']['family']==case) for case in ('nested_tan','rearranged'))
        print(kp,'printed checks passed; delivery',len(accepted),flush=True)
    save(H/'render-input.json',all_render);save(H/'generator-verification.json',summary)


if __name__=='__main__':main()
