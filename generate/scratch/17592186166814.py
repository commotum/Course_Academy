#!/usr/bin/env python3
"""Autonomous ODE recognition, local frozen draft, basis 1356.

Observed checkbox triplets replay via complete numeric component masks, never
literal-return cases or an answer lookup. Text and mathematical stages are held
fixed; classification is independently recomputed from the displayed equations.
Explicit raw profiles retain one documented source solution error and are
ineligible for learner use. Default levels are authored finite categorical
catalogs: numerical coefficients are presentation variety, never task counts.
No solves, integration, IVPs, new derivative orders, plots or database operations.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186166814
TITLE='Determining Whether an Ordinary Differential Equation is Autonomous or Nonautonomous'
VERSION='autonomous-ode-v1'
ROOT=Path(__file__).resolve().parent/str(KP_ID)
CAPTURE=json.loads((ROOT/'source.json').read_text())
SOURCE=CAPTURE['record']
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
X,Y,D=sp.symbols('x y D', real=True)
ROMAN=['I','II','III']
DERIV=r'\frac{\text{d}y}{\text{d}x}'
OPENING=next(iter(QUESTIONS.values()))[':question/worked-solution'].split('\n\nWith')[0]

def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+str(v)))
def tex(v): return sp.latex(v).replace(r'\log',r'\ln')

class MathReader:
    """Small independent TeX reader for the complete supported displayed grammar.
    Reads actual prompt/solution bytes; no generation metadata is consulted.
    """
    def __init__(self,s):
        s=s.replace(DERIV,'D')
        s=re.sub(r'\{y\}\^\{[′\']\}', 'D',s).replace("y'",'D')
        s=re.sub(r'\\operatorname\{(\w+)\}',r'\\\1 ',s)
        s=s.replace('⁡','').replace(r'\left','').replace(r'\right','')
        self.tokens=re.findall(r'\\[A-Za-z]+|\d+|[{}()+\-*/^]|[a-zA-Z]',s); self.i=0
        assert ''.join(self.tokens)==re.sub(r'\s+', '',s),('unread notation',s)
    def peek(self): return self.tokens[self.i] if self.i<len(self.tokens) else ''
    def pop(self): v=self.peek(); self.i+=1; return v
    def group(self):
        op=self.pop(); assert op in ('{','('),op
        v=self.expr(); assert self.pop()==('}' if op=='{' else ')'); return v
    def atom(self):
        t=self.peek()
        if t in ('{','('): v=self.group()
        elif t=='-': self.pop(); return -self.atom()
        elif t=='+': self.pop(); return self.atom()
        elif t in (r'\frac',r'\dfrac'):
            self.pop(); a=self.atom(); b=self.atom(); v=a/b
        elif t==r'\sqrt': self.pop(); v=sp.sqrt(self.atom())
        elif t in (r'\sin',r'\cos',r'\tan',r'\sec',r'\ln',r'\arctan'):
            self.pop(); fn={r'\sin':sp.sin,r'\cos':sp.cos,r'\tan':sp.tan,r'\sec':sp.sec,r'\ln':sp.log,r'\arctan':sp.atan}[t];v=fn(self.atom())
        elif t==r'\pi': self.pop();v=sp.pi
        elif t.isdigit(): self.pop();v=sp.Integer(t)
        elif t in ('x','y','D','e'):self.pop();v={'x':X,'y':Y,'D':D,'e':sp.E}[t]
        else: raise ValueError(('unexpected math token',t,self.tokens))
        if self.peek()=='^': self.pop();v=v**self.atom()
        return v
    def term(self):
        v=self.atom()
        while self.peek() and self.peek() not in ('+','-','}',')'):
            t=self.peek()
            if t in ('*','/'): self.pop(); w=self.atom(); v=v*w if t=='*' else v/w
            else: v*=self.atom()
        return v
    def expr(self):
        v=self.term()
        while self.peek() in ('+','-'):
            t=self.pop();w=self.term();v=v+w if t=='+' else v-w
        return v
    def read(self):
        v=self.expr();assert self.i==len(self.tokens);return v

def read(s): return MathReader(s).read()
def isolate(eq):
    l,r=eq.split('='); residual=read(l)-read(r)
    coefficient=sp.diff(residual,D)
    assert not coefficient.has(D) and coefficient!=0
    return sp.simplify(-residual.subs(D,0)/coefficient)
def autonomous(eq): return sp.simplify(sp.diff(isolate(eq),X))==0

def prompt_equations(prompt): return re.findall(r'- \*\*(?:I|II|III)\.\*\* \$(.*?)\$',prompt)
def designation(prompt,equations):
    negate='**not**' in prompt
    return [('true' if autonomous(eq)!=negate else 'false') for eq in equations]

# Source extraction: slots are complete integer coefficient/exponent components.
# Each same-valued source component is intentionally tied across all occurrences.
# Zero/unit constants remain fixed; exposed slots cannot erase an x/y dependence.
def source_parameters(q):
    return {'n'+n:int(n) for n in sorted(set(re.findall(r'\d+',q[':question/problem']))) if int(n)>=2}
def mask(text,parameters):
    return re.sub(r'\d+',lambda m:str(parameters.get('n'+m[0],int(m[0]))),text)
def observed(level,template,p,profile):
    q=QUESTIONS[template]; original=source_parameters(q)
    if p is None: p=original
    if set(p)!=set(original): raise ValueError('source parameter keys must match complete component slots')
    if any(type(v)!=int or not 2<=v<=8 for v in p.values()): raise ValueError('observed complete integer slots require 2..8')
    # Preserve power arithmetic: any component used as an exponent is at most 3,
    # except original non-variable exponent e^2 and coefficients tied to powers.
    for key,val in p.items():
        n=key[1:]
        if re.search(r'\}\^\{'+n+r'\}',q[':question/problem']) and n not in ('2','3'): raise ValueError('unsupported exponent')
        if re.search(r'\}\^\{'+n+r'\}',q[':question/problem']) and val>3: raise ValueError('variable powers require 2..3')
    prompt=mask(q[':question/problem'],p)
    solution_source=q[':question/worked-solution']
    if template=='q-96705':
        # The x-square denominator is a computed power, independent of the
        # coefficient 2 in Equation II. Freeze its complete component first.
        solution_source=solution_source.replace('{x}^{2}','[[DERIVED_X_SQUARE]]')
    solution=mask(solution_source,p).replace('[[DERIVED_X_SQUARE]]','{x}^{2}')
    raw=profile=='observed_raw'
    if not raw:
        if template=='q-96702':
            bad=r'\frac{\sqrt{y}+'+str(p['n2'])+'}{'+str(p['n2'])+'}'
            solution=solution.replace(bad,r'\frac{\sqrt{y}+'+str(p['n2'])+'}{y}')
    return prompt,solution,p,{'source_id':q[':db/id'],'source_ma_id':template,'evidence_only':raw,'eligible_for_learning':not raw}

# EASY: authored direct recognition. Each of three isolated equations requires
# exactly the same test: does the explicit RHS depend on x? Four function forms,
# either independent or dependent argument. No rearrangement, powers 2..3.
EASY=[f'{fn}:{v}' for fn in ('power','exp','sqrt','log') for v in ('y','x')]
# MODERATE: authored one subtraction and one division for EACH equation.
# Dependent or independent multiplicative coefficient, plus a mixed/no-x term.
MODERATE=[f'{fn}:{v}' for fn in ('power','exp','sqrt','sin','cos') for v in ('y','x')]
# HARD: authored cancellation classification. EACH equation needs division of a
# factored RHS by an affine x coefficient, then checks equal versus unequal
# independent factors. At most two affine factors, no polynomial expansion.
HARD=[f'{fn}:{v}' for fn in ('power','exp','sqrt','sin') for v in ('y','x')]
CATALOG={'easy':EASY,'moderate':MODERATE,'hard':HARD}
def function(fn,v,n):
    z=X if v=='x' else Y
    return {'power':lambda:z**n,'exp':lambda:sp.exp(z),'sqrt':lambda:sp.sqrt(z),'log':lambda:sp.log(z),'sin':lambda:sp.sin(z),'cos':lambda:sp.cos(z)}[fn]()
def authored(level,p,rng):
    if p is None:
        while True:
            kinds=rng.sample(CATALOG[level],3)
            if {k.split(':')[1] for k in kinds}=={'x','y'}: break
        p={'kinds':kinds,'a':rng.randint(2,4),'b':rng.randint(1,4),'n':rng.randint(2,3),'c':rng.randint(5,7),'negate':bool(rng.getrandbits(1))}
    if set(p)!=set(('kinds','a','b','n','c','negate')): raise ValueError('authored parameter keys')
    if len(p['kinds'])!=3 or len(set(p['kinds']))!=3 or any(k not in CATALOG[level] for k in p['kinds']):raise ValueError('three distinct eligible structures required')
    if {k.split(':')[1] for k in p['kinds']}!={'x','y'}:raise ValueError('mixed autonomous/nonautonomous structures required')
    for k,lo,hi in [('a',2,4),('b',1,4),('n',2,3),('c',5,7)]:
        if type(p[k])!=int or not lo<=p[k]<=hi:raise ValueError('authored workload bound '+k)
    if type(p['negate'])!=bool:raise ValueError('boolean response criterion required')
    eqs=[];blocks=[];selected=[]
    for i,kind in enumerate(p['kinds']):
        fn,v=kind.split(':');F=function(fn,'y' if level=='hard' else v,p['n']);a=p['a'];b=p['b'];c=p['c']
        if level=='easy': eq=DERIV+'='+tex(F); rhs=F
        elif level=='moderate':
            coefficient=Y if v=='y' else X
            eq=tex(coefficient)+DERIV+'+'+str(b)+'='+str(a)+r'\left('+tex(F)+r'\right)'
            rhs=(a*F-b)/coefficient
        else:
            numerator_offset=a if v=='y' else c
            eq=r'\left(x+'+str(a)+r'\right)'+DERIV+r'=\left(x+'+str(numerator_offset)+r'\right)\left('+tex(F)+'+'+str(b)+r'\right)'
            rhs=(X+numerator_offset)*(F+b)/(X+a)
        A=sp.simplify(sp.diff(rhs,X))==0
        if A!=p['negate']:selected.append(ROMAN[i])
        eqs.append(eq)
        opening=('- Equation '+ROMAN[i]+' is '+('an autonomous' if A else 'not an autonomous')+' differential equation. ')
        if level=='easy':
            opening+=('We see that it is of the form $'+DERIV+'=f(y),$ where $f(y)='+tex(rhs)+'.$' if A else 'It is not of the form $'+DERIV+'=f(y).$')
        else:
            opening+=('Writing the equation in the form $'+DERIV+'=f(y),$ we get' if A else 'If we isolate the derivative term, we get')
            l,r=eq.split('=');form='f(y)' if A else 'f(x,y)'
            # Distinct original, divided-factored, reduced and formal stages.
            divided=(r'\frac{'+r+'}{'+l.replace(DERIV,'')+'}' if level=='hard' else r'\frac{'+str(a)+r'\left('+tex(F)+r'\right)-'+str(b)+'}{'+tex(coefficient)+'}')
            rows=[l+' & ='+r,DERIV+' & ='+divided]
            if level=='hard' and A:rows.append(DERIV+' & ='+tex(sp.simplify(rhs)))
            rows.append(DERIV+' & ='+form)
            opening+='\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\nwhere $'+form+'='+tex(sp.simplify(rhs))+'.$'
            if not A:opening+=' So, it is not possible to write the equation in the form $'+DERIV+'=f(y).$'
        blocks.append(opening)
    prompt='Which of the following are '+('**not** ' if p['negate'] else '')+'autonomous ordinary differential equations?\n\nSelect all that apply.\n\n'
    if level=='hard':prompt+="Consider intervals where the coefficients of the derivative are nonzero.\n\n"
    prompt+='\n'.join('- **'+r+'.** $'+e+'$' for r,e in zip(ROMAN,eqs))
    answer=' and '.join(selected)+' only'
    solution=OPENING+"\n\nWith that in mind, let's check each of the differential equations:\n\n"+'\n\n'.join(blocks)+'\n\nTherefore, the correct answer is "'+answer+'."'
    return prompt,solution,p,{'evidence_only':False,'eligible_for_learning':True,'authored':True}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in CATALOG:raise ValueError('difficulty must be easy/moderate/hard')
    if field_type not in (None,'checkbox',':answer-field.type/checkbox'):raise ValueError('only source checkbox layout supported')
    rng=random.Random(seed)
    if template in QUESTIONS:
        actual=QUESTIONS[template][':question/difficulty'][':db/ident'].split('/')[-1]
        if actual!=level:raise ValueError('observed difficulty mismatch')
        if profile not in (None,'observed_raw','observed_repaired'):raise ValueError('source profile')
        profile=profile or 'observed_repaired'
        prompt,solution,p,meta=observed(level,template,parameters,profile)
    else:
        if template not in (None,'authored_triplet'):raise ValueError('unknown template')
        if profile not in (None,'authored_boolean'):raise ValueError('authored profile')
        template='authored_triplet';profile='authored_boolean'
        prompt,solution,p,meta=authored(level,parameters,rng)
    equations=prompt_equations(prompt);values=designation(prompt,equations)
    # Content includes actual learner-visible bank, criterion, solution and level.
    identity=digest([VERSION,level,prompt,solution,[[r,['false','true'],v] for r,v in zip(ROMAN,values)]])
    fields=[]
    for roman,correct in zip(ROMAN,values):
        field_id=uid(identity+roman)
        choices=[{':answer/id':uid(field_id+v),':answer/type':':answer.type/text',':answer/value':v} for v in ('false','true')]
        rng.shuffle(choices)
        fields.append({':answer-field/id':field_id,':answer-field/key':roman,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(field_id+correct)]})
    q={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields}
    if template in QUESTIONS and profile=='observed_raw':
        # The captured schema has these original attributes. Preserve presence.
        q[':question/math-academy-id']=QUESTIONS[template][':question/math-academy-id']
        q[':db/id']=QUESTIONS[template][':db/id']
        for f,s in zip(fields,QUESTIONS[template][':question/answer-fields']):
            f[':db/id']=s[':db/id']
            for a in f[':answer-field/choices']:
                a[':db/id']=next(o[':db/id'] for o in s[':answer-field/choices'] if o[':answer/value']==a[':answer/value'])
    # Numerical constants alone do not establish new categorical tasks.
    if template=='authored_triplet':semantic=[level,sorted(p['kinds']),p['negate']]
    else:semantic=[level,template,'**not**' in prompt]
    return {'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'content_identity':identity,'mathematical_fingerprint':digest(semantic),'domain':'Real ordinary first-order ODEs, on intervals where displayed expressions are defined and derivative coefficients are nonzero.','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},**meta}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def main():
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['json','markdown'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
    if args.count<1:a.error('count must be positive')
    records=[]
    for level in (CATALOG if args.difficulty=='all' else [args.difficulty]):
        seen=set();selected=[]
        # Coefficients, seeds, and permutations cannot replenish categorical tasks.
        # Source-mask sampling offers only one task per selected source template.
        limit=1 if args.template in QUESTIONS else {'easy':96,'moderate':200,'hard':96}[level]
        if args.count>limit:a.error(f'finite-limit: {level} template offers at most {limit} semantic tasks')
        for offset in range(10000):
            record=generate(level,args.seed+offset,template=args.template,profile=args.profile)
            fingerprint=record['generation']['mathematical_fingerprint']
            if fingerprint not in seen:
                seen.add(fingerprint);selected.append(record)
            if len(selected)==args.count:break
        if len(selected)<args.count:a.error(f'finite-limit: bounded search found {len(selected)} distinct {level} tasks')
        records.extend(selected)
    if args.format=='json': print(json.dumps(records,indent=2))
    else:
        for r in records:
            q=r['question'];meta=r['generation']
            label=('Observed source replay (evidence only)' if meta['evidence_only'] else
                   'Generated authored variant' if meta.get('authored') else 'Generated source-template variant')
            level=q.get(':question/difficulty','unrated').split('/')[-1]
            print('## '+label+' | '+level+' | '+meta['template']+' | '+meta['profile']+'\n')
            print(q[':question/problem'])
            print('\nAuthor review: complete checkbox banks and correct lookup refs.\n')
            for f in q.get(':question/answer-fields',[]):
                bank=', '.join(a[':answer/value']+' ['+a[':answer/id']+']' for a in f[':answer-field/choices'])
                correct_value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
                print('- '+f[':answer-field/key']+' (checkbox): '+bank+'; correct='+correct_value+'; ref='+json.dumps(f[':answer-field/correct']))
            print('\nWorked solution:\n\n'+q.get(':question/worked-solution','(absent in source)')+'\n')

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':main()
