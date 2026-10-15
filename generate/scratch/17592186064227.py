#!/usr/bin/env python3
"""Identity/substitution trig integrals: 20 complete source profiles, all levels.

The two independent slots implement k*f(a*x), with original bounds divided by a.
Every source choice recipe is (k/a)*D(a*x), including compound source mistakes.
The source's operative integral rows are retained rather than synthesized from
just a final antiderivative. Profiles are selected before sampling parameters.
"""
import sys
sys.dont_write_bytecode=True
import argparse,hashlib,importlib.util,json,random,re,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('')
def private(name):
 spec=importlib.util.spec_from_file_location('kp64227_'+name,HERE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=private('math_format');parser=private('math_parser')
x,u,C=parser.X,parser.U,parser.C
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];KP_ID=KP[':db/id'];KP_UUID=KP[':knowledge-point/id']
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
PROFILES=json.loads((HERE/'profiles.json').read_text());LEVELS=('easy','moderate','hard');VERSION='identity-substitution-trig-v1'
def sym(s):return sp.sympify(s,locals={'x':x,'u':u,'C':C,'sec':sp.sec,'csc':sp.csc,'cot':sp.cot})
def tex(z):return sp.latex(z)
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def ident(z):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(z)))
def integer(z,name,positive=False):
 if type(z)is not int or(positive and z<=0):raise ValueError(name+' must be a '+('positive 'if positive else'')+'builtin integer')
def scale_x(text,a):
 if a==1:return text
 return re.sub(r'(?<![A-Za-z])(\d*)x(?![A-Za-z])',lambda m:'{'+str(a*int(m[1]or'1'))+'x}',text)
def scale_bounds(t,a):
 # Only x-integrals call this: u endpoints stay exactly as observed.
 pat=r'(?:\{\\int \}|\\int)\s*_'
 matches=list(re.finditer(pat,t))
 for m in reversed(matches):
  lo,j=parser.group(t,m.end());assert t[j]=='^';hi,k=parser.group(t,j+1)
  t=t[:m.start()]+r'\int_{'+tex(parser.latex(lo)/a)+'}^{'+tex(parser.latex(hi)/a)+'}'+t[k:]
 return t

def operand(t,a,k):
 trailing='.'if t.rstrip().endswith('.')else'';t=t.strip().rstrip('.')
 if not t:return ''
 if r'\int'in t:
  is_x=any(v in t for v in (r'\text{d}x',r'\textrm{d}x'))
  if is_x:t=scale_bounds(t,a)
  t=t.replace(r'\text{d}x','@@DX@@').replace(r'\textrm{d}x','@@DX@@');t=scale_x(t,a).replace('@@DX@@',r'\text{d}x')
  factor=sp.Integer(k)if is_x else sp.Rational(k,a)
  return (tex(factor)+r'\cdot 'if factor!=1 else'')+t+trailing
 has_C='+C'in t.replace(' ','');t=re.sub(r'\+\s*C\s*$','',t)
 t=scale_x(t,a);factor=sp.Rational(k,a)
 return (tex(factor)+r'\left('+t+r'\right)'if factor!=1 else t)+('+C'if has_C else'')+trailing

def transform_block(block,a,k):
 # The derivative relation is a different mathematical role from an integral.
 if r'\frac{\text{d}u}{\text{d}x}'in block:
  left,right=block.strip().split('⟹');head,deriv=left.split('=',1);dl,dr=right.split('=',1)
  deriv=deriv.replace(r'\,','').strip();dl=dl.replace(r'\,','').strip();dr=dr.strip().rstrip('.')
  deriv=tex(a)+r'\left('+scale_x(deriv,a)+r'\right)'
  dl=tex(sp.Rational(1,a))+r'\left('+dl+r'\right)'
  dr=dr.replace(r'\text{d}x','@@DX@@');dr=scale_x(dr,a).replace('@@DX@@',r'\text{d}x')
  return head+'='+deriv+r'\,⟹\,'+dl+'='+dr+'.'
 # Preserve every source equality operand and every ordered row, including
 # uncancelled trigonometric products and post-integration reciprocal rewrites.
 starts=re.findall(r'\\begin\{aligned\}',block);ends=re.findall(r'\\end\{aligned\}',block)
 b=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','')
 rows=b.split(r'\\');out=[]
 for row in rows:out.append(' = '.join(operand(v,a,k)for v in row.split('=')))
 return ''.join(starts)+r' \\ '.join(out)+''.join(ends)

def changed_solution(old,a,k):
 sol=old[':question/worked-solution']
 # Work by display segments so inline substitution/identity statements are not
 # multiplied by the integral's numerator coefficient.
 pieces=re.split(r'(\$\$.*?\$\$)',sol,flags=re.S);out=[]
 for p in pieces:
  if p.startswith('$$'):out.append('$$\n'+transform_block(p[2:-2],a,k)+'\n$$');continue
  # x table labels denote the variable itself, not its value.
  def table(m):return '| $x$ | $'+tex(parser.latex(m[1])/a)+'$ | $'+tex(parser.latex(m[2])/a)+'$ |'
  p=re.sub(r'\| \$x\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',table,p)
  def inline(m):
   t=m[1]
   if t.strip().rstrip('.')in('x','u'):return m[0]
   if r'\text{d}x='in t:
    lhs,rhs=t.split('=',1);rhs=rhs.rstrip('.');return '$'+lhs+'='+tex(sp.Rational(1,a))+r'\left('+rhs+r'\right).$'
   # Table x values have already been adjusted and contain no x variable.
   return '$'+scale_x(t,a)+'$'
  out.append(re.sub(r'(?<!\$)\$(?!\$)(.*?)\$',inline,p))
 return ''.join(out)

@fmt.checked_math_content
def generate(difficulty='easy',seed=0,template=None,parameters=None,bank_profile=None):
 integer(seed,'seed')
 if difficulty not in LEVELS:raise ValueError('Unknown difficulty')
 rng=random.Random(seed);eligible=[sid for sid,t in PROFILES.items()if t['difficulty']==difficulty]
 sid=template or rng.choice(eligible)
 if sid not in eligible:raise ValueError('Profile/difficulty mismatch')
 t=PROFILES[sid];profile=t['bank_profile']
 if bank_profile not in(None,profile):raise ValueError('Complete observed bank required')
 p=dict(parameters)if parameters is not None else {'a':rng.randint(1,6),'k':rng.choice(tuple(range(-6,0))+tuple(range(1,7)))}
 if set(p)!={'a','k'}:raise ValueError('Expected a and k')
 a,k=p['a'],p['k'];integer(a,'a',True);integer(k,'k')
 if not(1<=a<=6 and 1<=abs(k)<=6):raise ValueError('a in 1..6 and k in ±1..±6 required')
 old=SOURCES[sid];original=p=={'a':1,'k':1}
 if original:prompt=old[':question/problem'];solution=old[':question/worked-solution']
 else:
  prompt=re.sub(r'\$(.*?)\$',lambda m:'$'+operand(m[1],a,k)+'$'if r'\int'in m[1]else m[0],old[':question/problem'],flags=re.S)
  # A prompt's trailing response equals sign is not an operand to multiply.
  prompt=prompt.replace(r'\cdot =','=')
  solution=changed_solution(old,a,k)
 values=[]
 for f in old[':question/answer-fields']:
  vals=[]
  for ans in f[':answer-field/choices']:
   z=parser.latex(ans[':answer/value'])
   v=fmt.normalize_tex(ans[':answer/value'])if original else tex(sp.Rational(k,a)*(z-C if z.has(C)else z).subs(x,a*x)) + ('+C'if z.has(C)else'')
   vals.append(fmt.normalize_tex(v))
  ci=next(i for i,z in enumerate(f[':answer-field/choices'])if z[':answer/id']==f[':answer-field/correct'][':answer/id']);values.append((f,vals,ci))
 # Include actual displayed bank and field shape; profile avoids authored bank
 # collisions, while seed/order never enter semantic identity.
 task={'profile':profile,'a':a,'k':k,'prompt':fmt.normalize_prose(prompt),'fields':[(f[':answer-field/key'],f[':answer-field/type'][':db/ident'],sorted(vs))for f,vs,ci in values]};qid=ident(task);fields=[]
 for f,vs,ci in values:
  fid=ident([qid,f[':answer-field/key']]);answers=[{':answer/id':ident([fid,i,v]),':answer/type':':answer.type/math',':answer/value':v}for i,v in enumerate(vs)]
  fields.append({':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/problem':fmt.normalize_prose(prompt),':question/worked-solution':fmt.normalize_prose(solution),':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':sid,'bank_profile':profile,'parameters':p,'source_ids':[sid],'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'original_parameters':original,'task_fingerprint':digest(task),'domain':'Original domain in z=a*x: '+t['original_domain']+'. Each connected component retained; positive a preserves original definite interval. Log absolute values retained.','dependencies':{'sympy':sp.__version__},'plots':'none'}}

def batch(difficulty='all',count=1,seed=0):
 integer(seed,'seed');integer(count,'count',True);levels=LEVELS if difficulty=='all'else(difficulty,)
 if any(z not in LEVELS for z in levels):raise ValueError('Unknown difficulty')
 out=[];seen=set()
 for level in levels:
  n=0
  for i in range(count*100+100):
   r=generate(level,seed+i);fp=r['generation']['task_fingerprint']
   if fp in seen:continue
   out.append(r);seen.add(fp);n+=1
   if n==count:break
  if n!=count:raise ValueError('Unique bounded bank exhausted')
 return out

def markdown(rec):
 q=rec['question'];out=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  out+='Field '+f[':answer-field/key']+' ('+f[':answer-field/type'].split('/')[-1]+')\n\n'
  for a in f[':answer-field/choices']:out+='- $'+a[':answer/value']+'$'+(' (correct)'if a[':answer/id']==f[':answer-field/correct'][1]else'')+'\n'
 return out+'\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args()
 try:rs=batch(args.difficulty,args.count,args.seed)
 except ValueError as e:ap.error(str(e))
 print(json.dumps(rs,indent=2,ensure_ascii=False)if args.format=='json'else'\n\n---\n\n'.join(markdown(z)for z in rs))
