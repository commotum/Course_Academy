#!/usr/bin/env python3
"""Independent displayed-TeX arithmetic, complete-bank fidelity and native grading."""
import functools, copy, hashlib, importlib.util, itertools, json, platform, re, subprocess, sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('homogeneous_generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y,T=sp.symbols('x y t',positive=True)

# Restricted source-grammar parser. It reads emitted TeX, including grouped
# implicit products, rather than regenerate expression values from metadata.
class Parser:
    def __init__(self,text,f=None):
        text=re.sub(r'\\operatorname\{(sin|cos|arctan|ln)\}',r'\\\1',text)
        text=re.sub(r'\\text\{[^}]*\}','',text)
        text=text.replace('\u2061',' ').replace('\\,','').replace('\\cdot','*').replace('\\left','').replace('\\right','').strip().rstrip('.')
        self.tokens=re.findall(r'\\[a-zA-Z]+|\d+|[a-zA-Z]|[{}()^+*/,\-]',text)
        leftovers=re.sub(r'\\[a-zA-Z]+|\d+|[a-zA-Z]|[{}()^+*/,\-\s.]','',text)
        assert not leftovers,(text,leftovers)
        self.i=0;self.f=f
    def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else None
    def take(self):v=self.peek();self.i+=1;return v
    def atom(self):
        v=self.take()
        if v in ('{','('):
            val=self.expr();assert self.take()==('}' if v=='{' else ')');return val
        if v==r'\frac':return self.atom()/self.atom()
        if v in (r'\sin',r'\cos',r'\arctan',r'\ln'):
            return {r'\sin':sp.sin,r'\cos':sp.cos,r'\arctan':sp.atan,r'\ln':sp.log}[v](self.power())
        if v=='f':
            assert self.take()=='(';a=self.expr();assert self.take()==',';b=self.expr();assert self.take()==')'
            assert self.f is not None;return self.f.subs({X:a,Y:b},simultaneous=True)
        if v and v.isdigit():return sp.Integer(v)
        if v in ('x','y','t','e'):return {'x':X,'y':Y,'t':T,'e':sp.E}[v]
        raise AssertionError(('unexpected atom',v,self.tokens))
    def power(self):
        if self.peek()=='-':self.take();return -self.power()
        result=self.atom()
        if self.peek()=='^':self.take();result=result**self.power()
        return result
    def product(self):
        result=self.power()
        while self.peek() and self.peek() not in ('+','-',')','}',','):
            if self.peek()=='*':self.take();result*=self.power()
            elif self.peek()=='/':self.take();result/=self.power()
            else:result*=self.power()
        return result
    def expr(self):
        result=self.product()
        while self.peek() in ('+','-'):
            v=self.take();result=result+self.product() if v=='+' else result-self.product()
        return result
    def parse(self):
        val=self.expr();assert self.i==len(self.tokens),(self.tokens,self.i);return val

def parse(text,f=None):return Parser(text,f).parse()
@functools.lru_cache(maxsize=20000)
def zero(e):
    # The recovered grammar has rational arithmetic over fixed elementary
    # function atoms; no trig-identity rewriting is required. cancel is exact
    # and avoids expanding sin(n*z) for one-digit coordinate coefficients.
    return sp.cancel(sp.expand_log(e,force=True))==0
@functools.lru_cache(maxsize=10000)
def homogeneous(e):
    # Euler condition independently verifies every displayed expression, and
    # direct simultaneous scaling checks the same criterion without degrees.
    euler=zero(X*sp.diff(e,X)+Y*sp.diff(e,Y))
    scaling=zero(e.subs({X:T*X,Y:T*Y},simultaneous=True)-e)
    assert euler==scaling,(e,euler,scaling)
    return euler

def values(record):return [[parse(a[':answer/value'].split('=',1)[1]) for a in f[':answer-field/choices']] for f in record['question'][':question/answer-fields']]

def check_record(record,raw=False):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    q=record['question'];meta=record['generation'];is_not='NOT' in q[':question/problem']
    assert is_not==(q[':question/difficulty']==':question.difficulty/moderate')
    strings=[q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
    for text in strings:
        assert not any(ord(c)<32 and c not in '\n\t' for c in text)
        assert text.count('$')%2==0
        assert text.count('{')==text.count('}')
        assert '\\\\frac' not in text
    solution=q[':question/worked-solution'];assert '**Method 1**' in solution and '**Method 2**' in solution
    bank_values=values(record);correct_functions=[]
    for f,exprs in zip(q[':question/answer-fields'],bank_values):
        assert len(exprs)==5
        results=[homogeneous(e) for e in exprs]
        qualifying=[i for i,b in enumerate(results) if b!=is_not]
        assert len(qualifying)==1,(meta,results)
        for a,b in itertools.combinations(exprs,2):assert not zero(a-b),(a,b)
        chosen=qualifying[0];correct_functions.append(exprs[chosen])
        if ':answer-field/correct' in f:assert f[':answer-field/correct'][1]==f[':answer-field/choices'][chosen][':answer/id']
        else:assert raw and meta['source_ids']==['q-8739']
    f=correct_functions[-1]
    if raw and meta['source_ids']==['q-14322']:
        assert meta['evidence_only'] and not meta['eligible_for_learning'];return
    for definition in re.findall(r'f\(x,y\)=([^$]+)',solution):
        # Full f definitions, including the polynomial coefficient restatement.
        if '\n' not in definition:
            for rhs in definition.split('='):
                assert zero(parse(rhs)-f),('stale inline function definition',rhs,f)
    for equation in re.findall(r'\$\$\s*(\\frac\{\\text\{d\}y\}\{\\text\{d\}x\}=[\s\S]*?)\$\$',solution):
        rhs=equation.split('=',1)[1].strip().rstrip('.')
        if rhs!='f(x,y)':assert zero(parse(rhs)-f),(rhs,f)
    # Each displayed aligned equality is checked, with f evaluated from the
    # actual displayed keyed ODE. Degree statements cannot hide a wrong row.
    aligned=re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',solution)
    assert aligned
    chains=[]
    for block in aligned:
        members=[]
        for row in block.split('\\\\'):
            row=row.replace('&','').replace('\\,','').strip()
            for member in row.split('='):
                if member.strip():members.append(parse(member.strip(),f))
        if meta['source_ids']==['q-14322']:
            point=re.search(r'For \$x=(\d+)\$, \$y=(\d+)\$ and \$t=(\d+)\$',solution)
            u,v,t=map(int,point.groups());members=[value.subs({X:u,Y:v,T:t}) for value in members]
        assert all(zero(v-members[0]) for v in members),('invalid displayed chain',block,members)
        chains.append(members)
    source_id=meta['source_ids'][0]
    expected={'q-8739':[6],'q-14319':[6],'q-8369':[6],'q-8741':[3],'q-90597':[4],'q-14322':[6,5]}
    assert [len(c) for c in chains]==expected[source_id],(source_id,[len(c) for c in chains])
    # Operation guards reject removal of an operative stage even if equal.
    if source_id in ('q-8739','q-14319','q-8369'):
        rows=aligned[0].split('\\\\');degree=3 if source_id=='q-14319' else 2
        assert '(tx)' in rows[0] or '(t(' in rows[0]
        assert rows[1].count('{t}^{'+str(degree)+'}')>=2
        assert '{t}^{'+str(degree)+'}(' in rows[2]
        assert rows[-1].strip().endswith('f(x,y)')
    if source_id=='q-14322':
        assert 'constant term cannot cancel' in solution
        m=re.search(r'For \$x=(\d+)\$, \$y=(\d+)\$ and \$t=(\d+)\$',solution);assert m
        u,v,t=map(int,m.groups());assert not zero(f.subs({X:t*u,Y:t*v})-f.subs({X:u,Y:v}))
        assert zero(chains[0][0]-f.subs({X:t*u,Y:t*v})) and zero(chains[1][0]-f.subs({X:u,Y:v}))


def native_checks(record,label):
    checks=[]
    for i,f in enumerate(record['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'whole displayed bank independently classified; actual radio UUID selection'})
    return {'label':label,'record':record,'checks':checks}

def main():
    originals=[];source_cases=[];fidelity=[];engine=[];review=[]
    for template,source_id in g.TEMPLATES.items():
        level='moderate' if template in g.LEVELS['moderate'] else 'easy'
        p={'sx':1,'sy':1}
        if template=='constant_offset_not':p.update(x0=1,y0=2,t=3)
        r=g.generate(level,template=template,parameters=p,profile='raw');q=g.QUESTIONS[source_id]
        check_record(r,True)
        assert r['question'][':question/problem']==q[':question/problem']
        assert r['question'][':question/worked-solution']==q[':question/worked-solution']
        for rf,sf in zip(r['question'][':question/answer-fields'],q[':question/answer-fields']):
            assert [a[':answer/value'] for a in rf[':answer-field/choices']]==[a[':answer/value'] for a in sf[':answer-field/choices']]
            assert (':answer-field/correct' in rf)==(':answer-field/correct' in sf)
            assert rf[':answer-field/key']==sf[':answer-field/key']
        source_cases.append({'source_id':source_id,'template':template,'level':level,'parameters':p,'profile':'raw','bank_profile':'captured complete bank(s)'})
        fidelity.append({'source_id':source_id,'prompt_exact':True,'solution_exact':True,'banks':len(q[':question/answer-fields']),'choices':sum(len(f[':answer-field/choices']) for f in q[':question/answer-fields']),'correct_presence_exact':True,'eligible_for_learning':r['generation']['eligible_for_learning']})
        originals.append(r);review.append({'role':'exact raw source replay','record':r})
        normal=g.generate(level,template=template,parameters=p);check_record(normal);engine.append(native_checks(normal,'original-normal/'+template))
        review.append({'role':'supported normal at source parameters','record':normal})
    capacities={};mathematical=[];identities={}
    for level,templates in g.LEVELS.items():
        unique=set();count=0;examples=0;per_template={}
        for template in templates:
            template_unique=set();template_instances=0
            for a,b in itertools.product(range(1,10),repeat=2):
                if level=='easy' and min(a,b)!=1:continue
                if level=='hard' and min(a,b)<2:continue
                if template=='constant_offset_not' and max(a,b)>3:continue
                p={'sx':a,'sy':b}
                if template=='constant_offset_not':p.update(x0=1,y0=2,t=3)
                r=g.generate(level,template=template,parameters=p);check_record(r);count+=1
                unique.add(r['generation']['mathematical_identity']);template_unique.add(r['generation']['mathematical_identity']);template_instances+=1;identities[(level,template,a,b)]=r['generation']['mathematical_identity']
            per_template[template]={'enumerated_instances':template_instances,'mathematical_tasks':len(template_unique)}
            print('Validated '+level+'/'+template,flush=True)
            for seed in (11,24):
                r=g.generate(level,seed,template=template);check_record(r)
                assert r==g.generate(level,seed,template=template)
                same=g.generate(level,seed+100,template=template,parameters=r['generation']['parameters'])
                assert r['question']==same['question']
                engine.append(native_checks(r,f'{level}/{template}/seed={seed}'))
                review.append({'role':'generated '+level+' variant','record':r});examples+=1
            # Boundary native checks use both ends, rather than only random draws.
            for bound in ('lower','upper'):
                a=2 if level=='hard' else 1;b=a
                if bound=='upper':a=3 if template=='constant_offset_not' else 9;b=(1 if level=='easy' else a)
                p={'sx':a,'sy':b}
                if template=='constant_offset_not':p.update(x0=1,y0=2,t=3)
                r=g.generate(level,template=template,parameters=p);engine.append(native_checks(r,f'{level}/{template}/{bound}'))
        capacities[level]={'enumerated_instances':count,'mathematical_tasks':len(unique),'review_variants':examples,'templates':per_template}
    # Easy/hard workload domains cannot supply identical mathematical banks.
    assert not {v for k,v in identities.items() if k[0]=='easy'} & {v for k,v in identities.items() if k[0]=='hard'}
    default_coverage={level:sorted({g.generate(level,seed)['generation']['template'] for seed in range(90)}) for level in g.LEVELS}
    assert all(set(default_coverage[l])==set(g.LEVELS[l]) for l in g.LEVELS)
    invalid=[('easy','quadratic_difference',{'sx':2,'sy':2}),('hard','cubic_quotient',{'sx':1,'sy':2}),('easy','cubic_quotient',{'sx':10,'sy':1}),('moderate','constant_offset_not',{'sx':4,'sy':1,'x0':1,'y0':2,'t':3})]
    for l,t,p in invalid:
        try:g.generate(l,template=t,parameters=p)
        except ValueError:pass
        else:raise AssertionError('invalid explicit bounds accepted')
    def omit_factoring(solution):
        block=re.search(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',solution).group(1)
        rows=block.split('\\\\');rows[2]=rows[3]
        return solution.replace(block,'\\\\'.join(rows))
    mutations=[]
    r=g.generate('hard',template='cubic_quotient',parameters={'sx':2,'sy':3})
    for label,operation in [('wrong implicit product',lambda s:s.replace('(2x)(3y)','x(3y)',1)),('missing factoring stage',omit_factoring),('control character',lambda s:s+'\x0c')]:
        bad=copy.deepcopy(r);bad['question'][':question/worked-solution']=operation(bad['question'][':question/worked-solution'])
        if bad==r:
            # Replace the actual cubic mixed product as emitted.
            bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('(2x){(3y)}','x{(3y)}',1)
        try:check_record(bad)
        except (AssertionError,TypeError):mutations.append(label)
        else:raise AssertionError('mutation not rejected: '+label)
    (ROOT/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n')
    (ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
    harness=REPO/'generate/runs/current/check-engine'
    subprocess.run([str(harness),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
    native=json.loads((ROOT/'engine-report.json').read_text())
    calc=json.loads((REPO/'generate/runs/current/refresh-2026-10-14/priority13-calculator-requirements.json').read_text())
    assert len(calc['records'])==86
    assert all(':question/requires-calculator' not in r for kp,r in calc['records'])
    calculator={'wrapper_records':86,'kp_records':[r for kp,r in calc['records'] if kp==g.KP_ID],'status':'unknown: all captured calculator attributes absent'}
    (ROOT/'calculator.json').write_text(json.dumps(calculator,indent=2)+'\n')
    report={'status':'worker_validation_passed_parent_QA_pending','source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_questions':6,'source_banks':7,'source_choices':35,'source_distractors':28,'exact_raw_solution_replays':6,'fidelity':fidelity,'normal_repairs':['q-8739: supported keyed field only; raw legacy field retained','q-14322: consistent simultaneous scaling witness and cancellation-qualified degree argument'],
        'capacities':capacities,'default_template_coverage':default_coverage,'mutations_rejected':mutations,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},'raw_grading_unavailable':['q-8739 raw two-field record has unkeyed legacy field; native fixture requires every field keyed'],
        'raw_mathematical_ineligibility':['q-14322 historical witness and degree implication retained as evidence'], 'versions':{'python':platform.python_version(),'sympy':sp.__version__},'hashes':{'script_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((ROOT/'source.json').read_bytes()).hexdigest(),'native_binary_sha256':hashlib.sha256(harness.read_bytes()).hexdigest(),'native_source_sha256':hashlib.sha256((harness.with_suffix('.rs')).read_bytes()).hexdigest()}}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
