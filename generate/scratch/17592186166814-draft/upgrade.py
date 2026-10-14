from pathlib import Path
p=Path('generate/scratch/17592186166814-draft.py');s=p.read_text()
s=s.replace('local frozen draft, basis 1356','separate registered-generator revalidation draft, basis 2275')
s=s.replace("VERSION='autonomous-ode-v1'","VERSION='autonomous-ode-draft-v2'")
s=s.replace("ROOT=Path(__file__).resolve().parent/str(KP_ID)","ROOT=Path(__file__).resolve().with_suffix('')\nsys.dont_write_bytecode=True\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]))\nfrom scripts.question_capture.math_format import checked_math_content, normalize_prose, validate_prose")
s=s.replace("QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}","QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions'] if ':question/math-academy-id' in q}")
start=s.index('class MathReader:');s=s[:start]+'''BINDING_PAIRS=(('x','y'),('t','u'),('s','v'),('t','y'))
NOTATIONS=('leibniz','prime')

def binding_parameters(p, rng=None, sampled=False, source=False):
    p=dict(p)
    if sampled:
        independent,dependent=rng.choice(BINDING_PAIRS)
        notation=rng.choice(NOTATIONS)
    else:
        independent,dependent='x','y';notation='source' if source else 'leibniz'
    p.setdefault('independent',independent);p.setdefault('dependent',dependent);p.setdefault('notation',notation)
    if (p['independent'],p['dependent']) not in BINDING_PAIRS:
        raise ValueError('eligible distinct independent/dependent-variable pair required')
    if p['notation'] not in (NOTATIONS+('source',) if source else NOTATIONS):
        raise ValueError('unsupported derivative notation')
    return p

def derivative(independent,dependent,notation='leibniz'):
    return (r'\\frac{\\text{d}'+dependent+r'}{\\text{d}'+independent+'}' if notation=='leibniz' else '{'+dependent+"}^{'}")

def bind_math(text,p,change_notation=True):
    # Slots are complete derivative components and single mathematical variable
    # tokens. TeX commands stay protected; their mathematical arguments do not.
    if change_notation and p['notation']!='source':
        text=text.replace(DERIV,'[[DERIVATIVE]]')
        text=re.sub(r"\\{y\\}\\^\\{[′']\\}|y'",'[[DERIVATIVE]]',text)
    names={'x':p['independent'],'y':p['dependent']}
    text=re.sub(r'\\\\[A-Za-z]+|[xy]|.',lambda m:names.get(m[0],m[0]),text,flags=re.S)
    return text.replace('[[DERIVATIVE]]',derivative(p['independent'],p['dependent'],p['notation']))

def bind_prose(text,p,change_notation=True):
    from scripts.question_capture.math_format import MATH
    def replace(m):
        body=m[0];size=2 if body.startswith(('$$',r'\\[',r'\\(')) else 1
        return body[:size]+bind_math(body[size:-size],p,change_notation)+body[-size:]
    return MATH.sub(replace,text)

def displayed_binding(prompt):
    declaration=re.search(r'Let \\$(\\w)=(\\w)\\((\\w)\\)\\$\\.',prompt)
    if declaration:
        assert declaration[1]==declaration[2] and declaration[1]!=declaration[3]
        return declaration[3],declaration[1]
    # The original lesson and original MA prompts conventionally use y=y(x).
    return 'x','y'

'''+s[start:]
s=s.replace('def __init__(self,s):\n        s=s.replace(DERIV,\'D\')\n        s=re.sub(r\'\\{y\\}\\^\\{[′\\\']\\}\', \'D\',s).replace("y\'",\'D\')', '''def __init__(self,s,independent='x',dependent='y'):
        self.independent=independent;self.dependent=dependent
        complete=derivative(independent,dependent)
        s=s.replace(complete,'D')
        s=re.sub(r'\\{'+dependent+r"\\}\\^\\{[′']\\}",'D',s).replace(dependent+"'",'D')''')
s=s.replace("elif t in ('x','y','D','e'):self.pop();v={'x':X,'y':Y,'D':D,'e':sp.E}[t]", "elif t in (self.independent,self.dependent,'D','e'):\n            self.pop();v={self.independent:X,self.dependent:Y,'D':D,'e':sp.E}[t]")
s=s.replace('def read(s): return MathReader(s).read()','def read(s,binding=(\'x\',\'y\')): return MathReader(s,*binding).read()')
s=s.replace('def isolate(eq):\n    l,r=eq.split(\'=\'); residual=read(l)-read(r)', "def isolate(eq,binding=('x','y')):\n    l,r=eq.split('='); residual=read(l,binding)-read(r,binding)")
s=s.replace('def autonomous(eq): return sp.simplify(sp.diff(isolate(eq),X))==0',"def autonomous(eq,binding=('x','y')): return sp.simplify(sp.diff(isolate(eq,binding),X))==0")
s=s.replace("negate='**not**' in prompt\n    return [('true' if autonomous(eq)!=negate else 'false')", "negate='**not**' in prompt\n    binding=displayed_binding(prompt)\n    return [('true' if autonomous(eq,binding)!=negate else 'false')")
s=s.replace("return {'n'+n:int(n) for n in sorted(set(re.findall(r'\\d+',q[':question/problem']))) if int(n)>=2}","return binding_parameters({'n'+n:int(n) for n in sorted(set(re.findall(r'\\d+',q[':question/problem']))) if int(n)>=2},source=True)")
s=s.replace('def observed(level,template,p,profile):','def observed(level,template,p,profile,rng):')
s=s.replace('if p is None: p=original\n    if set(p)!=set(original)', '''if p is None:
        p=dict(original)
        if profile!='observed_raw':
            for key in p:
                if key.startswith('n') and key[1:].isdigit():
                    maximum=3 if re.search(r'\\}\\^\\{'+key[1:]+r'\\}',q[':question/problem']) else 8
                    p[key]=rng.randint(2,maximum)
            p=binding_parameters({k:v for k,v in p.items() if k not in ('independent','dependent','notation')},rng,sampled=True,source=True)
    else: p=binding_parameters(p,source=True)
    if set(p)!=set(original)''')
s=s.replace("if any(type(v)!=int or not 2<=v<=8 for v in p.values())", "if any(type(v)!=int or not 2<=v<=8 for k,v in p.items() if k.startswith('n') and k[1:].isdigit())")
s=s.replace('for key,val in p.items():\n        n=key[1:]', "for key,val in p.items():\n        if not key.startswith('n') or not key[1:].isdigit():continue\n        n=key[1:]")
s=s.replace("    return prompt,solution,p,{'source_id'",'''    prompt=bind_prose(prompt,p)
    # Keep the two equivalent forms in the definition; apply selected notation
    # to all actual input equations, formal target references and operative rows.
    opening,tail=solution.split('\\n\\nWith',1)
    solution=bind_prose(opening,p,False)+'\\n\\nWith'+bind_prose(tail,p)
    if (p['independent'],p['dependent'])!=('x','y'):
        prompt='Let $'+p['dependent']+'='+p['dependent']+'('+p['independent']+')$.\\n\\n'+prompt
    return prompt,solution,p,{'source_id' ''')
s=s.replace("    if set(p)!=set(('kinds','a','b','n','c','negate'))", "    p=binding_parameters(p,rng,sampled=sampled)\n    if set(p)!=set(('kinds','a','b','n','c','negate','independent','dependent','notation'))")
s=s.replace('def authored(level,p,rng):\n    if p is None:', 'def authored(level,p,rng):\n    sampled=p is None\n    if p is None:')
s=s.replace("    return prompt,solution,p,{'evidence_only':False",'''    prompt=bind_prose(prompt,p)
    opening,tail=solution.split('\\n\\nWith',1)
    solution=bind_prose(opening,p,False)+'\\n\\nWith'+bind_prose(tail,p)
    prompt='Let $'+p['dependent']+'='+p['dependent']+'('+p['independent']+')$.\\n\\n'+prompt
    return prompt,solution,p,{'evidence_only':False''')
s=s.replace('def generate(level,seed=0', '@checked_math_content\ndef generate(level,seed=0')
s=s.replace('observed(level,template,parameters,profile)','observed(level,template,parameters,profile,rng)')
s=s.replace('    equations=prompt_equations(prompt);values=designation(prompt,equations)', '''    raw=profile=='observed_raw'
    if not raw:prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    for text in (prompt,solution):
        if any(ord(ch)<32 and ch not in '\\n\\t' for ch in text):raise ValueError('C0 control character in math content')
    equations=prompt_equations(prompt);values=designation(prompt,equations)''')
s=s.replace("'domain':'Real ordinary first-order ODEs, on intervals where displayed expressions are defined and derivative coefficients are nonzero.'", "'bindings':{'independent':p['independent'],'dependent':p['dependent'],'notation':p['notation']},'domain':'Real ordinary first-order ODEs with dependent '+p['dependent']+' and independent '+p['independent']+', on intervals where displayed expressions are defined and derivative coefficients are nonzero.'")
p.write_text(s)
