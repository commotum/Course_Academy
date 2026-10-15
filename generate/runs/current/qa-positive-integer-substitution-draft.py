"""Root polynomial substitution, every formal derivative operand and whole bank."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064203;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_posint_gen',D.with_suffix('.py'));P=load('root_posint_math',R/'elementary-integral-readback.py');x,u=P.x,P.u
N=dict(records=0,integral_sides=0,primitive_sides=0,formal_integrals=0,verification_sides=0,formal_derivatives=0,whole_primitive_operands=0,values=0,pairs=0,substitutions=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(raw=0,served_banks=0,values=0,solutions=0,incomplete=0)
for sid,o in olds.items():
 assert G.source_record(sid,raw=True)==o;fidelity['raw']+=1
 if ':question/worked-solution'not in o:fidelity['incomplete']+=1;continue
 t=G.TEMPLATES[sid];q=G.generate(t['difficulty'],template=sid,parameters={'b':t['source_b']},profile=sid)['question'];assert q[':question/problem']==G.normalize_prose(o[':question/problem'])and q[':question/worked-solution']==G.normalize_prose(o[':question/worked-solution']);fidelity['solutions']+=1
 f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(G.normalize_tex(a[':answer/value'])for a in of[':answer-field/choices']);assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==G.normalize_tex(of[':answer-field/correct'][':answer/value']);fidelity['served_banks']+=1;fidelity['values']+=len(f[':answer-field/choices'])
DER=r'\frac{\text{d}}{\text{d}x}'
def verification(raw):
 text=P.clean(raw.replace('✓',''));operands=[]
 while DER in text:
  at=text.index(DER);i=at+len(DER)
  while text[i].isspace():i+=1
  opening=text[i];assert opening in '([';closing=')'if opening=='('else']';depth=1;j=i+1
  while depth:
   assert j<len(text);depth+=(text[j]==opening)-(text[j]==closing);j+=1
  operand=P.scalar(text[i+1:j-1]);operands.append(operand);computed=s.diff(operand,x);text=text[:at]+'('+s.latex(computed)+')'+text[j:]
 return P.scalar(text),operands
seen={l:set()for l in G.SUPPORTED_LEVELS}
def check(r):
 q,m=r['question'],r['generation'];F,var=P.prompt(q[':question/problem']);assert var==x and s.Poly(F,x).degree()>=2
 sol=q[':question/worked-solution'];U=P.scalar(re.search(r'Let \$u=([^$]+)\$',sol)[1]);a=s.diff(U,x);assert a!=0 and not a.has(x);N['substitutions']+=1
 f=q[':question/answer-fields'][0];assert f[':answer-field/type'].endswith('/radio')and len(f[':answer-field/choices'])==5;correct=P.scalar(next(z[':answer/value']for z in f[':answer-field/choices']if z[':answer/id']==f[':answer-field/correct'][1]))
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==3;d=blocks[0];left,right=d.split('⟹');assert P.clean(left.split('=')[0])==r'\frac{\text{d}u}{\text{d}x}'and P.eq(P.scalar(left.split('=',1)[1]),a);l,rr=right.strip().split('=');assert P.clean(l)=='\\text{d}x';dm=re.fullmatch(r'(.*?)'+P.DIFF+r'[.]?',rr.strip());assert dm and dm[2]=='u'and P.eq(P.scalar(dm[1])*a,1)
 block=re.sub(r'\\(?:begin|end)\{aligned\}','',blocks[1]).replace('&','')
 for row in block.split(r'\\'):
  for part in row.split('='):
   if not part.strip():continue
   value,formal=P.side(part,x,U);assert P.eq(value,F),('incorrect actual integral/primitive stage',m['template'],m['parameters'],part,value,F);N['integral_sides'if formal else'primitive_sides']+=1;N['formal_integrals']+=len(formal)
 block=re.sub(r'\\(?:begin|end)\{aligned\}','',blocks[2]).replace('&','');first=True
 for row in block.split(r'\\'):
  for part in row.split('='):
   if not part.strip():continue
   value,operands=verification(part);assert P.eq(value,F),('incorrect formal derivative-check stage',m['template'],m['parameters'],part,value,F)
   if first:assert len(operands)==1 and P.eq(operands[0],correct);N['whole_primitive_operands']+=1;first=False
   N['formal_derivatives']+=len(operands);N['verification_sides']+=1
 values=[P.derivative(P.scalar(a[':answer/value']),x)for a in f[':answer-field/choices']];hits=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],values)if P.eq(v,F)];assert hits==[f[':answer-field/correct'][1]]
 for i,v in enumerate(values):
  for w in values[:i]:assert not P.eq(v,w);N['pairs']+=1
 N['records']+=1;N['values']+=len(values);seen[q[':question/difficulty'].split('/')[-1]].add(s.srepr(s.expand(F)))
for i,e in enumerate(json.load(open(D/'engine-input.json'))):
 check(e['record'])
 if i%100==0:print('Root positive integer records read',i,flush=True)
for level in G.SUPPORTED_LEVELS:
 for seed in range(18):check(G.generate(level,seed))
 assert len(seen[level])==G.capacity(level)
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
