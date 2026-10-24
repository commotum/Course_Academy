#!/usr/bin/env python3
"""Order of an ODE, frozen scratch generator; math basis1356, no database access.

Easy: one equation, identify highest derivative (Leibniz notation).
Moderate: three independent prime-notation equations, test requested order1–3.
Hard (authored): three equations; four derivative occurrences each, mixed
Leibniz/prime notation and powers/products, requested order4–8. No differentiation,
solving, or classification is required. Levels have separate workload guards.

Observed source templates use complete derivative-component masks, not literal
question lookup. Observed numerical banks are explicit evidence-only relative
order catalogs: recovered values do not establish historical error intentions.
Normal easy bank operations: highest, lower, displayed ordinary exponent,
highest−1, highest+1, all together with collision rejection.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186166813-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186166813
TITLE='Identifying the Order of an Ordinary Differential Equation'
VERSION='ode-order-frozen-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP_UUID=SOURCE['record'][':knowledge-point/id']
PROVENANCE={k:SOURCE[k] for k in ('database','basis','lineage')}
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
ORDINAL={1:'first',2:'second',3:'third',4:'fourth',5:'fifth',6:'sixth',7:'seventh',8:'eighth'}
# Full fraction/prime components, including source ASCII/Unicode notation.
FRACTION=re.compile(r'\\(?:d?frac)\{\{\\text\{d\}\}\^\{(?P<n>\d+)\}y\}\{\\text\{d\}\{x\}\^\{(?P<den>\d+)\}\}|\\frac\{\\text\{d\}y\}\{\\text\{d\}x\}')
PRIME=re.compile(r'\{y\}\^\{(?P<prime>\'+|[′″‴])\}')
def derivatives(text):
    found=[]
    for m in FRACTION.finditer(text):
        n=int(m['n'] or 1)
        if m['den'] is not None and int(m['den'])!=n: raise ValueError('inconsistent derivative fraction')
        found.append((m.start(),m.end(),n,m.group()))
    for m in PRIME.finditer(text):
        p=m['prime'];n={'′':1,'″':2,'‴':3}.get(p,len(p))
        found.append((m.start(),m.end(),n,m.group()))
    return sorted(found)
def highest(text):
    ds=derivatives(text)
    if not ds: raise ValueError('No printed derivative')
    return max(d[2] for d in ds)
def derivative(n,style='fraction'):
    if style=='fraction':
        return r'\frac{\text{d}y}{\text{d}x}' if n==1 else r'\frac{{\text{d}}^{'+str(n)+r'}y}{\text{d}{x}^{'+str(n)+'}}'
    if style=='unicode' and n<=3:return '{y}^{'+{1:'′',2:'″',3:'‴'}[n]+'}'
    if n<=3:return "{y}^{"+"'"*n+'}'
    # Higher derivatives use the familiar Leibniz form, not ambiguous y^(n).
    return derivative(n)
def change_component(text,mapping):
    chunks=[];prev=0
    for start,end,n,old in derivatives(text):
        chunks.extend([text[prev:start],old if mapping[n]==n else derivative(mapping[n],'unicode' if any(c in old for c in '′″‴') else 'ascii' if "'" in old else 'fraction')]);prev=end
    chunks.append(text[prev:]);return ''.join(chunks)
def hash_value(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def ident(*x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'ode-order:'+hash_value(x)))
def strict_int(x,name,lo,hi):
    if type(x) is not int or not lo<=x<=hi:raise ValueError(f'{name} must be integer{lo}–{hi}')
    return x

def source_parameters(sid):
    q=ORIGINALS[sid];orders=sorted(set(d[2] for d in derivatives(q[':question/problem'])))
    return {'orders':{str(n):n for n in orders}}
def render_source(sid,p,profile):
    q=ORIGINALS[sid];old_orders=source_parameters(sid)['orders']
    if set(p)!= {'orders'} or not isinstance(p['orders'],dict) or set(p['orders'])!=set(old_orders):raise ValueError('source parameters require exact derivative-order keys')
    mapping={int(k):strict_int(v,'order',1,8) for k,v in p['orders'].items()}
    values=[mapping[n] for n in sorted(mapping)]
    if values!=sorted(set(values)):raise ValueError('source order map must be strictly increasing')
    problem=change_component(q[':question/problem'],mapping)
    solution=change_component(q[':question/worked-solution'],mapping)
    # Whole ordinal words and whole source order conclusions only.
    solution=re.sub(r'\b('+ '|'.join(ORDINAL[n] for n in mapping)+r')-order\b',lambda m:ORDINAL[mapping[next(n for n in mapping if ORDINAL[n]==m[1])]]+'-order',solution)
    old_high=max(mapping);new_high=mapping[old_high]
    solution=solution.replace('$'+str(old_high)+'.$','$'+str(new_high)+'.$')
    specs=[]
    if len(q[':question/answer-fields'])==3:
        target_word=re.search(r'are (\w+)-order',q[':question/problem'])[1]
        old_target=next(n for n in ORDINAL if ORDINAL[n]==target_word);target=mapping[old_target]
        problem=problem.replace(target_word+'-order',ORDINAL[target]+'-order')
        rows=re.findall(r'- \*\*(I|II|III)\.\*\* \$(.*?)\$',problem)
        for key,equation in rows:specs.append((key,'checkbox',['false','true'],'true' if highest(equation)==target else 'false','text'))
        task={'demand':'three order-membership decisions','target':target,'equations':semantic_equations(problem)}
    else:
        f=q[':question/answer-fields'][0];kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
        old_correct=int(f[':answer-field/correct'][':answer/value'])
        offsets=[int(a[':answer/value'])-old_correct for a in f[':answer-field/choices']]
        bank=[str(new_high+o) for o in offsets]
        if min(map(int,bank))<1 or len(set(bank))!=len(bank):raise ValueError('complete source relative catalog invalid')
        specs=[(f[':answer-field/key'],kind,bank,str(new_high),'math')]
        task={'demand':'one highest-order decision','equations':semantic_equations(problem)}
    if sid=='q-167787' and profile=='source_repaired':
        solution=solution.replace(r'\frac{1}{2}{e}^{x}', 'f(x)')
    return problem,solution,specs,task

def semantic_equations(problem):
    """Order workload fingerprint; coefficients/variable aliases do not count.

Includes ordered derivative occurrences, ordinary exponents, power/root/product
structure and left/right layout. It deliberately excludes coefficient magnitudes.
    """
    equations=re.findall(r'- \*\*(?:I|II|III)\.\*\* \$(.*?)\$',problem)
    if not equations:
        equations=[problem.split('$$')[1] if '$$' in problem else problem.split('$')[1]]
    result=[]
    for eq in equations:
        sides=eq.split('=');res=[]
        for side in sides:
            orders=[d[2] for d in derivatives(side)]
            masked=side
            for a,b,n,_ in reversed(derivatives(side)):masked=masked[:a]+'D'+masked[b:]
            exponents=re.findall(r'\^\{(\d+)\}',masked)
            res.append({'derivative_orders':orders,'ordinary_exponents':list(map(int,exponents)),'root':r'\sqrt' in masked,'derivative_power':bool(re.search(r'\)\}\^|\)\^',masked)),'derivative_product':bool(re.search(r'D(?:\s*|\\cdot\s*)D',masked))})
        result.append(res)
    return result

# Easy authored: two derivative occurrences, scalar order response, five choices.
# Bounds:3<=n<=7;1<=m<=n−2;n+2<=e<=9. No algebra/differentiation.
def easy_parts(p):
    if set(p)!= {'n','m','e','layout'}:raise ValueError('easy keys n,m,e,layout')
    n=strict_int(p['n'],'n',3,7);m=strict_int(p['m'],'m',1,n-2);e=strict_int(p['e'],'e',n+2,9)
    if p['layout'] not in ('left','right'):raise ValueError('easy layout')
    eq=(f'y{derivative(n)}+3x{derivative(m)}={{x}}^{{{e}}}' if p['layout']=='left' else f'{{x}}^{{{e}}}{derivative(m)}-3x=y{derivative(n)}')
    problem='What is the order of the ordinary differential equation $'+eq+'?$'
    solution=('The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.\n\n'
      +'The highest derivative in the given ODE is $'+derivative(n)+',$ which has order $'+str(n)+'.$\n\n'
      +'Therefore, the order of the ODE is $'+str(n)+'.$')
    bank=[str(v) for v in (n,m,e,n-1,n+1)]
    return problem,solution,[('selection','radio',bank,str(n),'math')],{'demand':'one highest-order decision','equations':semantic_equations(problem)}

# Moderate authored: exactly3 equations, at most2 derivative occurrences each;
# orders1–3, target1–3, source-root/power/product layouts. No higher order notation.
def selection_parts(p,hard=False):
    keys={'target','orders','forms'} | ({'lower','powers','exponents'} if hard else set())
    if set(p)!=keys:raise ValueError('selection parameter keys')
    target=strict_int(p['target'],'target',4 if hard else 1,8 if hard else 3)
    for name in keys-{'target'}:
        if not isinstance(p[name],list) or len(p[name])!=3:raise ValueError(name+' must be three entries')
    equations=[]
    for i,n in enumerate(p['orders']):
        strict_int(n,'equation order',4 if hard else 1,8 if hard else 3)
        form=strict_int(p['forms'][i],'form',0,2)
        d=derivative(n,'unicode');first=derivative(1,'unicode')
        if hard:
            m=strict_int(p['lower'][i],'lower',1,n-2);power=strict_int(p['powers'][i],'derivative power',2,5);e=strict_int(p['exponents'][i],'ordinary exponent',n+1,10)
            dn=derivative(n);dm=derivative(m,'unicode');ds=derivative(m+1)
            a=rf'{dm}({dn})^{{{power}}}';b=rf'{{x}}^{{{e}}}{first}';c=rf'y{ds}'
            eq=[a+'+'+b+'='+c,a+'='+b+'+'+c,b+'+'+c+'='+a][form]
        else:
            # All forms require distinguishing a derivative from an ordinary
            # power/root; one or two occurrences, as the observed moderate bank.
            eq=[f'{d}+3x{first}={{x}}^{{5}}y',rf'\sqrt{{{d}+x}}=3{{y}}^{{4}}',f'({d})^{{2}}+x{first}={{y}}^{{5}}'][form]
        equations.append(eq)
    problem=f'Which of the following are {ORDINAL[target]}-order ordinary differential equations?\n\nSelect all that apply.\n\n'+'\n'.join(f'- **{key}.** ${eq}$' for key,eq in zip(('I','II','III'),equations))
    solution=f'A differential equation is of {ORDINAL[target]}-order if the largest derivative term in the equation is $'+derivative(target,'unicode')+'.$\n\nKeeping this in mind, let\'s check each given equation.'
    selected=[];specs=[]
    for key,eq in zip(('I','II','III'),equations):
        n=highest(eq);correct=n==target
        matching='also ' if correct and selected else ''
        if correct:
            sentence=f'- Equation {key} is {matching}a {ORDINAL[target]}-order differential equation. The highest derivative in this equation is $'+derivative(n,'unicode')+'.$';selected.append(key)
        else:sentence=f'- Equation {key} is not a {ORDINAL[target]}-order differential equation. The highest derivative in this equation is $'+derivative(n,'unicode')+f',$ so this is a {ORDINAL[n]}-order differential equation.'
        solution+='\n\n'+sentence
        specs.append((key,'checkbox',['false','true'],'true' if correct else 'false','text'))
    label=('none' if not selected else 'all three' if len(selected)==3 else ' and '.join(selected)+' only')
    solution+='\n\nTherefore, the correct answer is "'+label+'."'
    return problem,solution,specs,{'demand':'three mixed-notation four-occurrence order-membership decisions' if hard else 'three order-membership decisions','target':target,'equations':semantic_equations(problem)}

# Hard entrypoint: authored same-KP workload extension, defined above. The actual
# scan is four derivatives per equation (lower, highest, first and next lower).
def sample(level,rng):
    if level=='easy':
        n=rng.randint(3,7);return {'n':n,'m':rng.randint(1,n-2),'e':rng.randint(n+2,9),'layout':rng.choice(['left','right'])}
    p={'target':rng.randint(4,8) if level=='hard' else rng.randint(1,3),'orders':[rng.randint(4,8) if level=='hard' else rng.randint(1,3) for _ in range(3)],'forms':[rng.randint(0,2) for _ in range(3)]}
    if level=='hard':p.update(lower=[rng.randint(1,n-2) for n in p['orders']],powers=[rng.randint(2,5) for _ in range(3)],exponents=[rng.randint(n+1,10) for n in p['orders']])
    return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    rng=random.Random(seed);template=template or {'easy':'single','moderate':'selection','hard':'mixed_selection'}[level]
    source_id=None
    if template in ORIGINALS:
        source_id=template;q=ORIGINALS[template];original_level=q[':question/difficulty'][':db/ident'].split('/')[-1]
        if level!=original_level:raise ValueError('source difficulty mismatch')
        profile=profile or 'observed';
        if profile not in ('observed','source_repaired'):raise ValueError('source profile')
        p=source_parameters(template) if parameters is None else parameters
        problem,solution,specs,task=render_source(template,p,profile)
        authored=False;eligible=False;recipes='complete relative-order source catalog; historical interpretation unresolved' if specs[0][1]!='checkbox' else 'printed highest derivative equals requested target'
    else:
        if template!={'easy':'single','moderate':'selection','hard':'mixed_selection'}[level]:raise ValueError('template is not eligible for difficulty')
        profile=profile or 'authored';
        if profile!='authored':raise ValueError('authored template profile')
        p=sample(level,rng) if parameters is None else parameters
        problem,solution,specs,task=easy_parts(p) if level=='easy' else selection_parts(p,level=='hard')
        authored=True;eligible=True;recipes=['highest derivative','lower derivative','displayed ordinary exponent','one too few derivative applications','one too many derivative applications'] if level=='easy' else 'printed highest derivative equals requested target'
    kinds={s[1] for s in specs}
    if field_type is not None and field_type not in kinds and field_type not in {':answer-field.type/'+k for k in kinds}:raise ValueError('unsupported field type')
    for key,kind,bank,correct,atype in specs:
        if len(set(bank))!=len(bank) or bank.count(correct)!=1:raise ValueError('whole bank invalid')
    identity=hash_value({'version':VERSION,'level':level,'problem':problem,'solution':solution,'specs':[(a,b,sorted(c),d,e) for a,b,c,d,e in specs]})
    fields=[]
    for key,kind,bank,correct,atype in specs:
        fid=ident(identity,key);answers=[{':answer/id':ident(identity,key,v),':answer/type':':answer.type/'+atype,':answer/value':v} for v in bank]
        if kind=='radio':rng.shuffle(answers)
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',ident(identity,key,correct)]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':ident(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'template':template,'profile':profile,'level':level,'seed':seed,'parameters':p,'source':PROVENANCE,'source_id':source_id,'authored':authored,'eligible_for_learning':eligible,'evidence_only':not eligible,'recipes':recipes,'domain':{'source':'strictly increasing original derivative-order map, integers1–8; complete original-relative-bank positive','easy':'3<=n<=7;1<=m<=n−2;n+2<=e<=9;two derivative occurrences','moderate':'target/orders1–3;three equations;forms0–2','hard':'target/orders4–8;lower1..n−2;powers2–5;ordinary exponentsn+1..10;four derivative occurrences each'},'mathematical_fingerprint':hash_value(task),'content_fingerprint':identity,'plots':'none','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
    q=r['question'];lines=[f"Difficulty: {r['generation']['level']} | {'authored' if r['generation']['authored'] else 'observed replay'}",q[':question/problem']]
    for f in q[':question/answer-fields']:
        correct=f[':answer-field/correct'][1];lines.append('\nField '+f[':answer-field/key']+' ('+f[':answer-field/type']+')')
        for a in f[':answer-field/choices']:lines.append('- '+a[':answer/value']+(' [correct]' if a[':answer/id']==correct else ''))
    lines.extend(['\nWorked solution:',q[':question/worked-solution']]);return '\n'.join(lines)

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')


from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186166813-source-policy.json'))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
