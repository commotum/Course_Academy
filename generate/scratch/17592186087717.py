#!/usr/bin/env python3
"""Exact table substitution; immutable math basis 1356. No DB writes or plots.

Observed templates are parameterized by a common nonzero output multiplier k:
every printed x(t), y(t), table cell, substitution stage and requested combination
is recomputed. Scalar source distractors have underdetermined intent: whole banks
are explicit scalar-replay profiles, never the default authored error bank.
Normal easy tables additionally offer independently parameterized affine functions.
Moderate quadratic and hard cubic tables are authored fixed-workload extensions, documented in evidence.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP=17592186087717
TITLE='Filling a Table of Values for a Parametric Curve'
VERSION='parametric-table-1'
ROOT=Path(__file__).with_suffix('')
T=sp.Symbol('t', real=True)
NS=uuid.UUID('bbf50e27-a8c3-52e7-be21-5d7ed61e5512')
SOURCE=json.loads((ROOT/'source.json').read_text())
RAW={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)

def tex(v): return sp.latex(sp.simplify(v))
def scalar(s):
    """Small independent parser for the observed exact scalar/polynomial notation."""
    s=s.strip().rstrip('.,').replace('−','-').replace('\u2061','').replace(r'\,','').replace(r'\left','').replace(r'\right','')
    s=re.sub(r'\\operatorname\{(sin|cos|tan)\}',r'\1',s)
    s=re.sub(r'\\(sin|cos|tan)',r'\1',s)
    def group(i):
        assert s[i]=='{'; n=1;j=i+1
        while n:
            if s[j]=='{':n+=1
            elif s[j]=='}':n-=1
            j+=1
        return s[i+1:j-1],j
    while r'\frac' in s or r'\sqrt' in s:
        hits=[(s.find(z),z) for z in (r'\frac',r'\sqrt') if z in s];i,z=min(hits)
        a,j=group(i+len(z))
        if z==r'\frac':b,j=group(j);replacement=f'(({scalar(a)})/({scalar(b)}))'
        else:replacement=f'sqrt({scalar(a)})'
        s=s[:i]+replacement+s[j:]
    s=s.replace(r'\pi','pi').replace('{','(').replace('}',')').replace('^','**')
    return sp.simplify(parse_expr(s,local_dict={'t':T,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,)))

def uid(s):return str(uuid.uuid5(NS,s))
def fingerprint(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def table_rows(prompt):return [line for line in prompt.splitlines() if line.startswith('|')]
def cells(row):return [s.strip() for s in row.split('|')[1:-1]]
def inner(s):return s[2:-2] if s.startswith('$$') else s[1:-1]
def scaled(s,k):
    # Preserve original notation at unit scale by ordinary coefficient omission.
    return s if k==1 else tex(k)+r'\left('+s+r'\right)'

def extract(qid):
    q=RAW[qid]; p=q[':question/problem']; rows=table_rows(p)
    times=[int(s.strip('$')) for s in cells(rows[0])[1:]]
    formula_match=next(m for m in MATH.finditer(p) if 'x=' in m.group() or 'x =' in m.group())
    formula_token=formula_match.group();formula=inner(formula_token)
    # Protect spacing commands without changing character offsets. Capture whole
    # mathematical components and store their exact spans in the formula token.
    protected=formula.replace(r'\,','§§')
    m=re.search(r'x\s*=\s*(.*?)\s*,.*?y\s*=\s*(.*?)(?=,)',protected,re.S)
    fx,fy=[formula[m.start(i):m.end(i)].strip() for i in (1,2)]
    delimiter=2 if formula_token.startswith('$$') else 1
    formula_slots={axis:(delimiter+m.start(i),delimiter+m.end(i)) for axis,i in (('x',1),('y',2))}
    grid={axis:cells(rows[i])[1:] for i,axis in ((2,'x'),(3,'y'))}
    slots={}
    for axis in ('x','y'):
        for i,c in enumerate(grid[axis]):
            marker=c.strip('$')
            if marker in ('a','b','c') or marker.startswith('{{'):slots[marker.strip('{}')]=(axis,i)
    combo_match=re.search(r'Find the value of \$(.*?)\$',p)
    combo=combo_match[1].rstrip('.') if combo_match else None
    return {'id':qid,'fx':fx,'fy':fy,'times':times,'grid':grid,'slots':slots,'combo':combo,'problem':p,'formula_span':formula_match.span(),'formula_token':formula_token,'formula_slots':formula_slots,'solution':q.get(':question/worked-solution','')}
SPECS={qid:extract(qid) for qid in RAW}
# Minimal corrections are explicit, raw source.json is immutable.
REPAIRS={
 'q-69923': [('b=2(-2)-4.','b=2(-2)=-4.')],
 'q-326242':[('x(2)=','x(3)=')],
 'q-326250':[('y(0)=','y(5)=')],
 'q-326255':[('y(1)=','y(4)=')],
 'q-6832':[(r'into $y=\operatorname{sin}',r'into $x=\operatorname{sin}')],
 'q-6825':[('a=3(3)','c=3(3)')],
}

def make_source(spec,k):
    fx,fy=(scalar(spec[key]) for key in ('fx','fy'))
    values={axis:[sp.simplify(k*f.subs(T,t)) for t in spec['times']] for axis,f in (('x',fx),('y',fy))}
    slots={name:values[axis][i] for name,(axis,i) in spec['slots'].items()}
    p=spec['problem']
    # Replace each whole formula component; then regenerate every nonblank table cell.
    token=spec['formula_token']
    for start,end in sorted(spec['formula_slots'].values(),reverse=True):
        token=token[:start]+scaled(token[start:end],k)+token[end:]
    start,end=spec['formula_span'];p=p[:start]+token+p[end:]
    old=table_rows(spec['problem']);new=[]
    for row,axis in ((old[2],'x'),(old[3],'y')):
        c=cells(row)
        for i,raw in enumerate(c[1:]):
            if raw.strip('$') not in ('a','b','c') and not raw.startswith('{{'):
                c[i+1]='$'+(raw.strip('$') if k==1 else tex(values[axis][i]))+'$'
        new.append('| '+' | '.join(c)+' |')
    p=p.replace(old[2],new[0]).replace(old[3],new[1])
    sol=spec['solution']
    for a,b in REPAIRS.get(spec['id'],[]):sol=sol.replace(a,b)
    if not sol:
        # q-6827 has no captured solution; authored supported sequence, not observed.
        sections=[]
        for name in ('a','b','c'):
            axis,i=spec['slots'][name];t=spec['times'][i];f=spec['f'+axis]
            sections.append(f'- To find the value of ${name},$ we substitute $t={t}$ into ${axis}={f}.$ This gives\n\n$$\n{name}='+re.sub(r'(?<![A-Za-z\\])t(?![A-Za-z])','('+str(t)+')',f)+'='+tex(slots[name]/k)+'.\n$$')
        sol='\n\n'.join(sections)+'\n\nFinally, we have\n\n$$\n'+spec['combo']+'=2+0+12=14.\n$$'
    # Each numeric RHS in every equality stage represents a value of x, y or
    # the requested linear combination; common scaling preserves all equalities.
    def transform(m):
        token=m.group();body=inner(token)
        if k==1 or '=' not in body or body.strip().startswith('t=') or 'le' in body:return token
        left,*rhs=body.strip().split('=')
        punctuation='.' if rhs[-1].rstrip().endswith('.') else ''
        rhs[-1]=rhs[-1].rstrip().removesuffix('.')
        rendered=[scaled(stage,k) for stage in rhs]
        # The last numeric simplification is the evaluated coordinate/result,
        # rather than an unevaluated multiplier around the old final answer.
        final=scalar(rhs[-1])
        if not final.free_symbols:rendered[-1]=tex(k*final)
        output=left+'='+'='.join(rendered)+punctuation
        return '$$\n'+output+'\n$$' if token.startswith('$$') else '$'+output+'$'
    sol=MATH.sub(transform,sol)
    # Final completed tables must use computed values, preserve source whitespace.
    for axis in ('x','y'):
        for row in table_rows(sol):
            if cells(row)[0]=='$'+axis+'$':
                original=cells(row);updated=[original[0]]+['$'+(original[i+1].strip('$') if k==1 else tex(v))+'$' for i,v in enumerate(values[axis])]
                sol=sol.replace(row,'| '+' | '.join(updated)+' |')
    return p,sol,values,slots

def authored(level,p,combination=False):
    times=list(range(-1,5)) if level=='easy' else list(range(0,6))
    fx=scalar(p['fx']);fy=scalar(p['fy']);ft={'x':tex(fx),'y':tex(fy)}
    values={axis:[sp.simplify(f.subs(T,t)) for t in times] for axis,f in (('x',fx),('y',fy))}
    slots={'field-1':('x',0),'field-2':('x',4),'field-3':('y',2)} if level=='easy' else {'field-1':('x',2),'field-2':('y',3),'field-3':('x',4)}
    if combination:slots={n:loc for n,loc in zip(('a','b','c'),slots.values())}
    def table(blank):
        rows=['| **$t$** | '+' | '.join('$'+str(t)+'$' for t in times)+' |','| --- | '+' | '.join('---' for t in times)+' |']
        for axis in ('x','y'):
            cs=[]
            for i,v in enumerate(values[axis]):
                names=[n for n,loc in slots.items() if loc==(axis,i)]
                cs.append(('$'+names[0]+'$' if combination else '{{'+names[0]+'}}') if blank and names else '$'+tex(v)+'$')
            rows.append('| $'+axis+'$ | '+' | '.join(cs)+' |')
        return '\n'.join(rows)
    prompt='Consider the curve with parametric equations\n\n$$\nx='+ft['x']+r',\,y='+ft['y']+r',\,'+str(times[0])+r'\le t\le '+str(times[-1])+'.\n$$\n\nFill in the blanks in the following table of values:\n\n'+table(True)
    if combination:
        prompt=prompt.replace('Consider the curve with parametric equations','For the parametric curve').replace('Fill in the blanks in the following table of values:','consider the following table of values:')
        prompt+='\n\nFind the value of $a-b-c.$'
    parts=[]
    for name,(axis,i) in slots.items():
        t=times[i];f=ft[axis];sub=re.sub(r'(?<![A-Za-z\\])t(?![A-Za-z])','('+str(t)+')',f)
        # Keep a fixed direct-substitution stage and an expanded numerical-terms
        # stage when nontrivial; exactly the same workload in each authored level.
        terms=sp.Add.make_args(fx if axis=='x' else fy)
        partial='+'.join('('+tex(term.subs(T,t))+')' for term in terms)
        label=name if combination else f'{axis}({t})'
        parts.append(f'- To find the value of ${label},$ we substitute $t={t}$ into ${axis}={f}.$ This gives\n\n$$\n{label}={sub}={partial}='+tex(values[axis][i])+'.\n$$')
    solved={n:values[a][i] for n,(a,i) in slots.items()}
    ending='\n\nThen the table is\n\n'+table(False)
    if combination:
        a,b,c=[solved[n] for n in ('a','b','c')]
        ending='\n\nFinally, we have\n\n$$\na-b-c=('+tex(a)+')-('+tex(b)+')-('+tex(c)+')='+tex(a-b-c)+'.\n$$'
    return prompt,'\n\n'.join(parts)+ending,values,solved,slots,times

def sample_authored(level,rng):
    if level=='easy':
        def slope():return rng.choice([-5,-3,-1,1,3,5])
        return {'fx':str(slope()*T+rng.randint(-3,3)), 'fy':str(slope()*T+rng.randint(-3,3))}
    def poly():
        a=sp.Rational(rng.choice([-5,-3,-1,1,3,5]),4)
        b=sp.Rational(rng.choice([-4,-2,-1,1,2,4]),3)
        c=rng.choice(list(range(-6,0))+list(range(1,7)))
        return a*T**(2 if level=='moderate' else 3)+b*T**(1 if level=='moderate' else 2)+c
    return {'fx':str(poly()),'fy':str(poly())}

def bounds(level,p):
    if set(p)!={'fx','fy'}:raise ValueError('Expected exactly fx and fy')
    for key in p:
        f=scalar(p[key]);poly=sp.Poly(f,T)
        if level=='easy':
            if poly.degree()!=1 or not -3<=poly.nth(0)<=3 or poly.nth(1) not in (-5,-3,-1,1,3,5):raise ValueError('Affine workload bounds')
        else:
            degree=2 if level=='moderate' else 3
            if poly.degree()!=degree or (level=='hard' and poly.nth(1)!=0) or poly.nth(degree) not in [sp.Rational(v,4) for v in (-5,-3,-1,1,3,5)] or poly.nth(degree-1) not in [sp.Rational(v,3) for v in (-4,-2,-1,1,2,4)] or poly.nth(0) not in list(range(-6,0))+list(range(1,7)):raise ValueError('Fractional polynomial workload bounds')
            if any(poly.eval(t).is_integer for t in (2,3,4)):raise ValueError('All assessed cells must retain rational arithmetic')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    rng=random.Random(seed);template=template or (rng.choice(['affine_table','affine_combination']) if level=='easy' else 'quadratic_table' if level=='moderate' else 'cubic_table')
    if template in SPECS:
        if level!='easy':raise ValueError('All observed templates are easy (q-6827 authored assignment)')
        spec=SPECS[template];p={'k':rng.choice([-3,-2,-1,1,2,3])} if parameters is None else dict(parameters)
        if set(p)!={'k'} or type(p['k']) is not int or p['k'] not in (-3,-2,-1,1,2,3):raise ValueError('k must be nonzero integer with |k|<=3')
        problem,solution,values,slots=make_source(spec,p['k']);locs=spec['slots'];times=spec['times'];combo=spec['combo']
        kind='radio' if combo else 'blank';profile=profile or ('authored-combination-blank' if combo and not RAW[template].get(':question/answer-fields') else 'authored-sign-input' if combo else 'blank')
        if combo:
            ans=scalar(combo).subs({sp.Symbol(n):v for n,v in slots.items()})
            if str(ans).find('a')>=0: # Symbols are parsed independently; explicit locals avoid namespace ambiguities.
                ans=sp.sympify(combo,locals={n:v for n,v in slots.items()})
            rawfields=RAW[template].get(':question/answer-fields',[])
            if profile=='authored-combination-blank':
                if rawfields:raise ValueError('Combination blank repair only for fieldless sources')
                kind='blank';bank=[ans];recipes=[];problem+='\n\n{{selection}}'
            elif profile=='observed-scalar-replay':
                if not rawfields:raise ValueError('No observed bank exists for this fieldless source')
                bank=[sp.simplify(p['k']*scalar(a[':answer/value'])) for a in rawfields[0][':answer-field/choices']]
                recipes=['opaque scalar replay: k × '+a[':answer/value'] for a in rawfields[0][':answer-field/choices']]
            elif profile=='authored-sign-input':
                # Whole bank: correct, reverse entire requested combination,
                # reverse each of the three substituted slot values in turn.
                coeff=[sp.sympify(combo).coeff(sp.Symbol(n)) for n in ('a','b','c')]
                bank=[ans,-ans]+[ans-2*c*slots[n] for c,n in zip(coeff,('a','b','c'))]
                recipes=['correct','reverse combination sign','reverse a sign','reverse b sign','reverse c sign']
            else:raise ValueError('Unsupported bank profile')
            if len(set(bank))!=(1 if kind=='blank' else 5):raise ValueError('Reject complete ambiguous bank')
            fields_data=[('selection',bank,ans)]
        else:
            if profile!='blank':raise ValueError('Blank table has no choice profile')
            fields_data=[(key,[slots[key]],slots[key]) for key in locs];recipes=[]
        refs=[template];origin='observed source components; authored errors' if profile=='authored-sign-input' else 'observed explicit replay'
    else:
        expected='cubic_table' if level=='hard' else 'quadratic_table' if level=='moderate' else 'affine_table'
        if template!=expected and not (level=='easy' and template=='affine_combination'):raise ValueError('Template outside difficulty scope')
        combo_mode=template=='affine_combination'
        if profile not in (None,'authored-sign-input' if combo_mode else 'blank'):raise ValueError('Incompatible authored bank profile')
        p=sample_authored(level,rng) if parameters is None else dict(parameters);bounds(level,p)
        for attempt in range(100):
            problem,solution,values,slots,locs,times=authored(level,p,combo_mode)
            if not combo_mode:break
            ans=slots['a']-slots['b']-slots['c']
            bank=[ans,-ans,ans-2*slots['a'],ans+2*slots['b'],ans+2*slots['c']]
            if len(set(bank))==5:break
            if parameters is not None:raise ValueError('Reject complete ambiguous authored radio bank')
            p=sample_authored(level,rng);bounds(level,p)
        else:raise ValueError('No complete eligible radio instance sampled')
        kind='radio' if combo_mode else 'blank';profile='authored-sign-input' if combo_mode else 'blank';combo='a-b-c' if combo_mode else None
        fields_data=[('selection',bank,ans)] if combo_mode else [(key,[slots[key]],slots[key]) for key in locs]
        refs=['q-69922'] if combo_mode else ['q-326242'] if level=='easy' else ['q-326247','q-326242','q-326250','e-5075'];origin='authored'
        recipes=['correct','reverse combination sign','reverse a sign','reverse b sign','reverse c sign'] if combo_mode else []
    if field_type and field_type.removeprefix(':answer-field.type/')!=kind:raise ValueError('Wrong field type')
    # Mathematical identity normalizes actual expressions, independent of template,
    # input spelling, option order, seed or source provenance.
    if template in SPECS:fx,fy=[p['k']*scalar(SPECS[template][key]) for key in ('fx','fy')]
    else:fx,fy=[scalar(p[key]) for key in ('fx','fy')]
    canonical_combination=str(sp.sympify(combo).subs({sp.Symbol(n):sp.Symbol(axis+'_at_'+str(times[i])) for n,(axis,i) in locs.items()})) if combo else None
    mathematical={'fx':str(sp.expand(fx)),'fy':str(sp.expand(fy)),'times':times,'slots':sorted(locs.values()),'combination':canonical_combination}
    mathematical_id=fingerprint(mathematical)
    content=fingerprint({'version':VERSION,'problem':problem,'solution':solution,'fields':[(key,sorted(tex(v) for v in bank),tex(ans)) for key,bank,ans in fields_data],'math':mathematical_id})
    fields=[]
    for key,bank,ans in fields_data:
        fid=uid(content+':field:'+key);answers=[{':answer/id':uid(fid+':answer:'+tex(v)),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in bank]
        correct=uid(fid+':answer:'+tex(ans))
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
    return {'knowledge_point':{'db_id':KP,'id':str(NS),'title':TITLE},'question':{':question/id':uid(content),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'origin':origin,'recipes':recipes,'source':{k:v for k,v in SOURCE.items() if k!='record'},'source_question_ids':refs,'parameter_fingerprint':mathematical_id,'content_fingerprint':content,'plot_rating':'none','plot_assets':{},'mathematics':mathematical,'source_repairs':REPAIRS.get(template,[])}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
    q=r['question'];out=q[':question/problem']
    for f in q[':question/answer-fields']:
        if f[':answer-field/type'].endswith('/radio'):
            out+='\n\n'+f[':answer-field/key']+' (review choices):\n'
            for i,a in enumerate(f[':answer-field/choices']):
                label=' [correct]' if a[':answer/id']==f[':answer-field/correct'][1] else ''
                out+='\n- '+chr(65+i)+'. $'+a[':answer/value']+'$'+label
        else:
            out+='\n\n'+f[':answer-field/key']+': $'+f[':answer-field/choices'][0][':answer/value']+'$'
    return out+'\n\nWorked solution:\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
