"""Parent reads actual scalar line integrals, every substitution and endpoint stage."""
import sys,re,json,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'function-of-y-readback.py','reader');t=p.t;u=p.p.u
n=dict(records=0,choices=0,substitutions=0,evaluation_integrals=0,primitive_rows=0,endpoint_rows=0,endpoint_components=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
def clean(raw):
 return raw.replace('&','').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().rstrip('.,?')
def substitution(text):
 found=re.search(r'substitution \$u=(.*?)\$',text)
 if not found:return None
 expr=p.scalar(found[1].rstrip(','));m=re.search(r'\\(?:text|mathrm)\{d\}u=(.*?)\\(?:text|mathrm)\{d\}t',text);assert m
 factor=m[1].replace(r'\,','').strip();factor='-1' if factor=='-' else factor
 assert p.equal(p.scalar(factor),s.diff(expr,t));n['substitutions']+=1;return expr
def evaluation(raw):
 raw=raw.replace(r'\left[','[').replace(r'\right]',']')
 if ']_' in raw:raw=raw.replace('[','(').replace(']_',')|_')
 return p.p.e.evaluated(raw)
def endpoint_components(raw):
 # Read top-level additive components separately, preserving displayed signs.
 raw=raw.replace(r'\left','').replace(r'\right','');depth=0;parts=[];start=0
 for i,c in enumerate(raw):
  if c in '({[':depth+=1
  elif c in ')}]':depth-=1
  elif c in '+-' and depth==0 and i>start:parts.append(raw[start:i]);start=i
 parts.append(raw[start:]);return [p.scalar(z.replace('[','(').replace(']',')')) for z in parts]
def stages(text,details):
 F,curve,bounds,ft,speed,I,missing,prefix=details
 counts=p.stages(text,details,integral_counts=(2,3))
 for k,v in counts.items():n[k]=n.get(k,0)+v
 expected=p.value(I,*bounds);sub=substitution(text);primitive=None;parts_previous=None;last_u=None;last_orientation=1
 groups=[clean(z) for z in p.p.blocks(text) if r'\begin{aligned}' in z and r'\int' in z and not re.search(r'\\int(?:\s*\})?_\{?C\}?',z)]
 assert len(groups)==1
 for row in groups[0].split(r'\\'):
  raws=row.split('=');raws=[clean(z) for z in raws]
  # The initial left-hand integral is also a printed mathematical stage.
  for raw in raws:
   if not raw:continue
   if r'\int' in raw:
    raw=raw.replace(r'\cdot (-\text{d}u)',r'\cdot (-1)\,\text{d}u')
    a,b,fn,var=p.integral(raw)
    if var==t:assert p.equal(a,bounds[0]) and p.equal(b,bounds[1]) and p.equal(fn,I,bounds),(raw,fn,I)
    else:
     assert sub is not None
     a0,b0=(sub.subs(t,z) for z in bounds);orientation=1
     if p.equal(a,b0) and p.equal(b,a0):orientation=-1
     else:assert p.equal(a,a0) and p.equal(b,b0),(raw,a0,b0)
     assert p.equal(orientation*fn.subs(u,sub)*s.diff(sub,t),I,bounds),(raw,fn,sub,I)
     last_u=(fn,a,b)
    n['evaluation_integrals']+=1
   elif '|' in raw or ']_' in raw or r'\right]_' in raw:
    anti,var,a,b,value=evaluation(raw);primitive=(anti,var,a,b)
    assert p.same_value(s.N(value,65),expected),(raw,value,expected)
    if var==t:assert p.equal(a,bounds[0]) and p.equal(b,bounds[1]) and p.equal(s.diff(anti,t),I,bounds)
    else:
     assert sub is not None;a0,b0=(sub.subs(t,z) for z in bounds);orientation=1
     if p.equal(a,b0) and p.equal(b,a0):orientation=-1
     else:assert p.equal(a,a0) and p.equal(b,b0)
     assert p.equal(orientation*s.diff(anti,u).subs(u,sub)*s.diff(sub,t),I,bounds),(raw,anti,I)
    last_orientation=orientation if var!=t else 1;n['primitive_rows']+=1
   else:
    value=p.scalar(raw.replace('[','(').replace(']',')'));assert p.same_value(s.N(value,65),expected),(raw,value,expected)
    parts=endpoint_components(raw)
    if parts_previous and len(parts)==len(parts_previous):
     assert all(sum(bool(p.equal(a,b)) for b in parts_previous)==1 for a in parts),(raw,parts,parts_previous);n['endpoint_components']+=len(parts)
    # First endpoint row, written as common factor times a difference, can
    # simplify to two signed terms; compare each to its actual primitive endpoint.
    if primitive:
     anti,var,a,b=primitive;expanded=s.expand(value);want=[s.expand(anti.subs(var,b)),s.expand(-anti.subs(var,a))]
     if len(parts)==2 and p.equal(parts[0],want[0]) and p.equal(parts[1],want[1]):n['endpoint_components']+=2
    parts_previous=parts;n['endpoint_rows']+=1
 assert primitive is not None
 anti,var,a,b=primitive;H=last_orientation*anti.subs(u,sub) if var==u else anti
 return H,last_u,sub
def check(rec):
 q=rec['question'];details=p.prompt(q[':question/problem']);expected=p.value(details[5],*details[2]);f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];vs=[p.scalar(a[':answer/value']) for a in choices];assert len(vs)==5
 assert all(not p.equal(z,w) for i,z in enumerate(vs) for w in vs[:i])
 good=[p.same_value(s.N(z,65),expected) for z in vs];assert sum(bool(z) for z in good)==1,(rec['generation']['template'],vs,expected)
 if ':answer-field/correct' in f:assert good[next(i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1])]
 else:assert rec['generation']['evidence_only'] and not rec['generation']['eligible_for_learning']
 if ':question/worked-solution' in q:
  H,tu,sub=stages(q[':question/worked-solution'],details)
  if rec['generation']['eligible_for_learning']:
   F,curve,bounds,ft,speed,I,missing,prefix=details;lo,hi=bounds;correct=s.simplify(H.subs(t,hi)-H.subs(t,lo));omit=s.integrate(ft,(t,lo,hi));name=rec['generation']['template']
   if name=='line_log':
    assert s.diff(speed,t)==0;C=s.simplify(I*sub);A,B=[sub.subs(t,z) for z in bounds];want=[correct,omit,correct*speed,C*s.log(A),C*(A-B)]
   else:
    if name=='line_power':wrong=s.integrate(I*t,(t,lo,hi))
    else:
     fn,a,b=tu;fn=s.expand(fn);replacements={node:u**(node.exp+s.Rational(1,2)) for node in s.preorder_traversal(fn) if isinstance(node,s.Pow) and node.base==u and node.exp.is_Rational and node.exp.q==2};assert replacements
     wrong=s.integrate(fn.xreplace(replacements),(u,a,b))
    want=[correct,omit,H.subs(t,hi)+H.subs(t,lo),H.subs(t,hi),wrong]
   assert all(sum(bool(p.equal(v,w)) for w in want)==1 for v in vs),(name,vs,want)
   n['complete_method_banks']=n.get('complete_method_banks',0)+1
 n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186179718;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(rec);q=rec['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for rec in json.load(open(D/'review.json')):check(rec)
 for level,fs in g.LEVELS.items():
  for family in fs:
   for seed in range(5):check(g.generate(level,seed=8400+seed,template=family))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
