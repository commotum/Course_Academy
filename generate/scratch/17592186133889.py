"""Three-dimensional divergence: source scale masks and same-KP authored banks.

Evidence recipes preserve all captured prose/stages and scale complete components,
not text fragments. Opaque observed banks are ineligible for learner sampling.
Authored workload is guarded identically for explicit and sampled parameters.
"""
from pathlib import Path
import argparse, hashlib, json, random, re, uuid, importlib.util
import sympy as s
ROOT=Path(__file__).resolve().parent/'17592186133889'
SOURCE=json.loads((ROOT/'source.json').read_text()); KP=SOURCE['record']
VERSION='divergence3d-1.0'
_read_spec=importlib.util.spec_from_file_location('divergence_private_readback',ROOT/'readback.py'); READ=importlib.util.module_from_spec(_read_spec);_read_spec.loader.exec_module(READ)
x,y,z=s.symbols('x y z',real=True)
VARS=(x,y,z)
Q={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
LEVELS=('easy','moderate','hard')
TEMPLATES={'easy':('exp_sine','monomial','shared_square'), 'moderate':('evaluated_monomial','evaluated_square','evaluated_exp_trig'), 'hard':('product_exp','product_log')}
class Rejected(ValueError): pass

def assessed_components(components,variables=VARS):
    # Drop terms constant in the coordinate being differentiated.
    return [s.srepr(s.Add(*[term for term in s.Add.make_args(s.expand(comp)) if term.has(v)])) for comp,v in zip(components,variables)]

def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+v))
def tex(v): return s.latex(v).replace(r'\log',r'\ln')
def group(v): return '('+v+')'
def scale(v,c): return v if c==1 else ('('+str(c)+')' if c<0 else str(c))+r'\left('+v+r'\right)'
def extract_components(solution):
    row=next(t for t in solution.split(r'\\') if r'\frac{∂}{∂x}(' in t)
    parts=[]
    for coord in 'xyz':
        start=row.index(r'\frac{∂}{∂'+coord+'}(')+len(r'\frac{∂}{∂'+coord+'}(')
        depth=1; end=start
        while depth:
            if row[end]=='(': depth+=1
            if row[end]==')': depth-=1
            end+=1
        parts.append(row[start:end-1])
    return parts

def prompt_mask(q,components):
    """Replace only complete component spans inside the displayed F declaration."""
    prompt=q[':question/problem']; pos=prompt.find('F=')
    if pos<0: return prompt
    begin=pos+2; end=prompt.find('$',begin)
    region=prompt[begin:end]; replacements=[]; search_start=0
    for idx,comp in enumerate(components):
        # Components often have outer parentheses in derivative arguments and
        # displayed basis terms, while tuple constants omit spacing commands.
        target=comp
        at=region.find(target,search_start)
        if at<0: raise ValueError(('component missing from prompt',q[':question/math-academy-id'],comp))
        replacements.append((at,at+len(target),'{'+('B' if comp.startswith('-') and idx>0 else 'C')+str(idx)+'}')); search_start=at+len(target)
    for a,b,replacement in sorted(replacements,reverse=True): region=region[:a]+replacement+region[b:]
    return prompt[:begin]+region+prompt[end:]

def evidence_recipe(q):
    components=extract_components(q[':question/worked-solution'])
    prompt=prompt_mask(q,components)
    # Mark every RHS stage individually. Formal operators are component slots;
    # all remaining mathematical rows are complete scalar arithmetic slots.
    solution=q[':question/worked-solution']; slots={}; n=0
    def aligned(m):
        nonlocal n
        body=m.group(1); rows=body.split(r'\\'); result=[]
        for row in rows:
            if '& =' not in row: raise ValueError(row)
            left,right=row.split('& =',1)
            if r'\frac{∂P}' in right: result.append(row); continue
            if r'\frac{∂}{∂x}' in right:
                result.append(left+'& ='+ '+'.join(r'\frac{∂}{∂'+v+'}({C'+str(i)+'})' for i,v in enumerate('xyz'))+' ' if right.endswith(' ') else left+'& ='+ '+'.join(r'\frac{∂}{∂'+v+'}({C'+str(i)+'})' for i,v in enumerate('xyz')))
                continue
            # Preserve terminal punctuation and whitespace independently.
            stripped=right.rstrip(); trailing=right[len(stripped):]; punct='.' if stripped.endswith('.') else ''
            value=stripped[:-1] if punct else stripped
            slot='S'+str(n);n+=1;slots[slot]=value
            result.append(left+'& ={'+slot+'}'+punct+trailing)
        return r'\begin{aligned}'+r'\\'.join(result)+r'\end{aligned}'
    solution=re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',aligned,solution,flags=re.S)
    # Answer values are complete mathematical objects, including vector errors.
    f=q[':question/answer-fields'][0]
    return {'prompt':prompt,'solution':solution,'components':components,'stages':slots,'answers':[a[':answer/value'] for a in f[':answer-field/choices']], 'correct':next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])}
RECIPES={key:evidence_recipe(q) for key,q in Q.items()}

def substitute(mask,slots):
    return re.sub(r'\{([BCS]\d+)\}',lambda m:slots[m.group(1)],mask)

def assemble(level,template,p,profile,prompt,solution,values,correct,kind,seed,evidence=False,source=None):
    # Option order is presentation only. Complete bank values determine identity.
    fingerprint=digest(p.get('canonical_task',{'template':template,'parameters':p}))
    identity=digest({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(values),'type':kind,'level':level})
    field_id=uid(identity+':field'); answers=[{':answer/id':uid(identity+':answer:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct_id=answers[correct][':answer/id'];random.Random(seed).shuffle(answers)
    f={':answer-field/id':field_id,':answer-field/key':'field-1' if kind=='blank' else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
    question={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[f]}
    return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':{k:v for k,v in p.items() if k not in ('canonical_components','canonical_task')},'bank_profile':profile,'evidence_only':evidence,'eligible':not evidence,'eligible_for_learning':not evidence,'profile_origin':'observed_opaque' if evidence else 'supported_presentation_repair' if profile.startswith('supported_') else 'authored_supported','source_id':source,'basis':1356,'lineage':SOURCE['lineage'],'mathematical_fingerprint':fingerprint,'content_fingerprint':identity}}

def evidence(level,seed,template,p,profile,repair=False):
    key=template.removeprefix('source_');q=Q[key];recipe=RECIPES[key]
    actual=q[':question/difficulty'][':db/ident'].split('/')[-1]
    if level!=actual: raise ValueError('Source level mismatch')
    if set(p)!={'scale'} or type(p['scale']) is not int or not 1<=abs(p['scale'])<=3: raise ValueError('Evidence scale must be a nonzero integer of magnitude at most 3')
    c=p['scale']; slots={f'C{i}':scale(v,c) for i,v in enumerate(recipe['components'])};slots.update({f'B{i}':v if c==1 else '+'+scale(v,c) for i,v in enumerate(recipe['components'])});slots.update({k:scale(v,c) for k,v in recipe['stages'].items()})
    prompt=substitute(recipe['prompt'],slots);solution=substitute(recipe['solution'],slots)
    if repair:
        name='G' if key=='q-168624' else 'F'
        prompt='Consider the vector field $'+name+'=⟨'+',\\,'.join(slots[f'C{i}'] for i in range(3))+'⟩.$\n\n'+prompt
    vals=[scale(a,c) for a in recipe['answers']]
    kind=q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
    components=[READ.scalar(slots[f'C{i}']) for i in range(3)]; variables=(READ.x,READ.y,READ.z); derivatives=[s.diff(comp,v) for comp,v in zip(components,variables)]
    point_match=re.search(r'at the point \$\(([^)]+)\)',prompt); point=None if point_match is None else [READ.scalar(v) for v in point_match.group(1).split(',')]
    task={'components':assessed_components(components,variables),'derivatives':[s.srepr(s.expand(d)) for d in derivatives],'evaluation':None if point is None else [s.srepr(s.simplify(d.subs(dict(zip(variables,point))))) for d in derivatives]}
    return assemble(level,template,{**p,'canonical_task':task},profile,prompt,solution,vals,recipe['correct'],kind,seed,not repair,key)

# EASY: direct held-coordinate derivatives, at most three nonzero summands.
# Coefficients 1..3 in magnitude; powers fixed at 2/3; no point substitution.
def build_easy(template,p):
    a,b,c=p['a'],p['b'],p['c']
    if template=='exp_sine': return [a*s.exp(b*x)*s.sin(y*z),c*x*y*z,s.Integer(2)]
    if template=='monomial': return [a*x*y*z**2,b*x*s.exp(y),c*y*z**3]
    if template=='shared_square':
        l=a*x+b*y+c*z
        if a+b+c==0: raise Rejected('Zero divergence removes workload')
        return [l**2,l**2,l**2]
    raise ValueError('Unsupported easy template')

# MODERATE: same three coordinate derivatives followed by exact evaluation.
# All three derivative contributions are nonzero before evaluation; small points,
# exp arguments zero and trig arguments familiar integer multiples of pi.
def build_moderate(template,p):
    a,b,c=p['a'],p['b'],p['c']
    if template=='evaluated_monomial': return [a*x**2*y*z,b*x*y**2*z,c*x*y*z**2]
    if template=='evaluated_square': return [a*(x+y)**2,b*(y+z)**2,c*(x+z)**2]
    if template=='evaluated_exp_trig': return [a*x*z*s.cos(y),b*y*x**2,c*x*z**2*s.exp(y)]
    raise ValueError('Unsupported moderate template')

# HARD (authored): coordinate derivatives with two product/chain terms each.
# No new divergence theorem, curl, flux, or vector geometry; six substantive
# derivative summands, coefficient magnitude <=3, no higher powers than 2.
def build_hard(template,p):
    a,b,c=p['a'],p['b'],p['c']
    if template=='product_exp': return [a*x**2*s.exp(b*x*y),y*s.exp(c*y*z),z*(x+y*z)**2]
    if template=='product_log': return [a*x**2*s.sin(b*x*y),y*s.exp(c*y*z),z*s.log(2+x*z)]
    raise ValueError('Unsupported hard template')
BUILDERS={'easy':build_easy,'moderate':build_moderate,'hard':build_hard}

def guard(level,template,p):
    needed={'a','b','c'}|({'point'} if level=='moderate' else set())
    if set(p)!=needed: raise ValueError('Exact parameter keys required: '+str(needed))
    if any(type(p[k]) is not int or not 1<=abs(p[k])<=3 for k in ('a','b','c')): raise ValueError('Reduced integer coefficients must have magnitude 1..3')
    if level=='moderate':
        pt=p['point']
        if not isinstance(pt,(list,tuple)) or len(pt)!=3 or any(type(t) is not int or abs(t)>2 for t in pt): raise ValueError('Point coordinates must be integers of magnitude <=2')
        if template=='evaluated_exp_trig' and (pt[1]!=0 or pt[0]==0 or pt[2]==0): raise ValueError('Exponential/trig point must have y=0 and nonzero x,z')
        if template=='evaluated_monomial' and any(t==0 for t in pt): raise ValueError('Nonzero monomial point coordinates required')
        if template=='evaluated_square' and any(t==0 for t in (pt[0]+pt[1],pt[1]+pt[2],pt[0]+pt[2])): raise ValueError('Nonzero square arguments at evaluation required')

def aligned(rows): return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
OPENING=Q['q-131178'][':question/worked-solution'].split('Therefore, we have')[0]

def authored(level,seed,template,p,profile,kind):
    guard(level,template,p);components=BUILDERS[level](template,p);derivatives=[s.diff(comp,v) for comp,v in zip(components,VARS)];total=s.expand(sum(derivatives))
    prompt='Consider the vector field $F=⟨'+',\\,'.join(tex(t) for t in components)+'⟩.$ '
    point=p.get('point');answer=total if point is None else s.simplify(total.subs(dict(zip(VARS,point))))
    prompt+= ('Find $\\text{div}\\,F.$' if point is None else 'Evaluate $\\text{div}\\,F$ at the point $('+','.join(map(str,point))+').$')
    if template=='product_log': prompt+=' Assume $2+xz>0.$'
    if kind=='blank': prompt+='\n\n$\\text{div}\\,F='+'$ {{field-1}}' if point is None else '\n\n{{field-1}}'
    formal=r'\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}'
    args='+'.join(r'\frac{∂}{∂'+v+'}('+tex(comp)+')' for comp,v in zip(components,'xyz'))
    # Keep individually differentiated contributions (including zero terms)
    # as separate groups before simplification/collection.
    evaluated='+'.join('('+tex(d)+')' for d in derivatives)
    solution=OPENING+'Therefore, we have\n\n'+aligned([r'∇\cdot F & ='+formal,'& ='+args,'& ='+evaluated,'& ='+tex(total)+'.'])
    if point is not None:
        # Substitute every coordinate using exact simultaneous substitution;
        # unevaluated masks retain component arithmetic at each term.
        terms=[]
        for d in derivatives:
            rendered=tex(d)
            rendered=re.sub(r'(?<![A-Za-z\\])([xyz])(?![A-Za-z])',lambda m:'('+str(point['xyz'.index(m.group(1))])+')',rendered)
            terms.append('('+rendered+')')
        solution+='\n\nFinally, we evaluate $\\text{div}\\,F$ at the point $('+','.join(map(str,point))+'),$ and obtain\n\n'+aligned([r'(∇\cdot F)('+','.join(map(str,point))+') & ='+'+'.join(terms),'& ='+'+'.join('('+tex(s.simplify(d.subs(dict(zip(VARS,point)))))+')' for d in derivatives),'& ='+tex(answer)+'.'])
    # A complete bank is fixed before sampling; if any operation collides reject
    # the entire instance. No first-valid replacement or per-option perturbation.
    if kind=='blank': candidates=[answer]
    elif s.simplify(derivatives[2])==0:
        first,second=derivatives[:2]; candidates=[answer,first,second,-first+second,total+components[2]]
    else: candidates=[answer,total-derivatives[0],total-derivatives[1],total-derivatives[2],-total]
    if point is not None: candidates=[s.simplify(t.subs(dict(zip(VARS,point)))) for t in candidates]
    if any(s.simplify(a-b)==0 for i,a in enumerate(candidates) for b in candidates[i+1:]): raise Rejected('Whole-bank collision')
    pp={**p,'canonical_task':{'components':assessed_components(components),'derivatives':[s.srepr(s.expand(d)) for d in derivatives],'evaluation':None if point is None else [s.srepr(s.simplify(d.subs(dict(zip(VARS,point))))) for d in derivatives]}}
    return assemble(level,template,pp,profile,prompt,solution,[tex(v) for v in candidates],0,kind,seed)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS: raise ValueError('Unsupported difficulty')
    rng=random.Random(seed)
    if template in ('zero_terms','axial'):
        if level!='easy' or field_type not in (None,'blank'): raise ValueError('Supported blank repair is easy/blank only')
        key={'zero_terms':'q-168615','axial':'q-168624'}[template]
        required='supported_blank_'+key
        if profile not in (None,required): raise ValueError('Supported blank repair profile mismatch')
        r=evidence(level,seed,'source_'+key,parameters if parameters is not None else {'scale':rng.choice((-3,-2,-1,1,2,3))},required,True)
        r['generation']['template']=template
        return r
    if profile and profile.startswith('observed_'):
        implied='source_'+profile.removeprefix('observed_')
        if template and template!=implied: raise ValueError('Profile/template mismatch')
        template=implied
    if template and template.startswith('source_'):
        key=template.removeprefix('source_')
        if key not in Q: raise ValueError('Unknown source template')
        profile=profile or 'observed_'+key
        if profile!='observed_'+key: raise ValueError('Evidence profile required')
        if field_type and field_type!=Q[key][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]: raise ValueError('Source field type mismatch')
        return evidence(level,seed,template,parameters if parameters is not None else {'scale':rng.choice((-3,-2,-1,1,2,3))},profile)
    template=template or rng.choice(TEMPLATES[level])
    if template not in TEMPLATES[level]: raise ValueError('Unsupported template at this level')
    kind=field_type or 'radio'
    if kind not in ('radio','blank'): raise ValueError('Unsupported field type')
    profile=profile or ('authored_omission_sign' if kind=='radio' else 'authored_blank')
    if profile!=('authored_omission_sign' if kind=='radio' else 'authored_blank'): raise ValueError('Unsupported authored profile/type')
    for attempt in range(512):
        p=dict(parameters) if parameters is not None else {k:rng.choice((-3,-2,-1,1,2,3)) for k in ('a','b','c')}
        if level=='moderate' and parameters is None:
            p['point']=[rng.choice((-2,-1,1,2)),0 if template=='evaluated_exp_trig' else rng.choice((-2,-1,1,2)),rng.choice((-2,-1,1,2))]
        try: return authored(level,seed,template,p,profile,kind)
        except Rejected:
            if parameters is not None: raise
        except ValueError:
            if parameters is not None: raise
    raise Rejected('Bounded sampling exhausted')

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Direct coordinate derivatives, fixed easy workload bounds."""
    return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Coordinate derivatives and exact familiar-point substitution."""
    return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Authored six derivative summands from product and chain rules."""
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
    text='## Generated — '+q[':question/difficulty'].split('/')[-1]+'\n\nTemplate: `'+g['template']+'`; profile: `'+g['bank_profile']+'`; '+('evidence only' if g['evidence_only'] else 'authored eligible')+'\n\n'+q[':question/problem']+'\n\n'
    for a in f[':answer-field/choices']:
        text+='- $'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '')+'\n'
    return text+'\n**Worked solution**\n\n'+q[':question/worked-solution']

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type',choices=('radio','blank'));args=ap.parse_args()
    if args.count<1: ap.error('Positive count required')
    records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in (LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__': main()
