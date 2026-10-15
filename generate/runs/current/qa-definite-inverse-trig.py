"""Parent readback: definite inverse functions, formal operands and signed endpoints."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064220;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_definv_gen',D.with_suffix('.py'));H=load('root_definv_inverse',R/'inverse-substitution-readback.py');P=H.P;E=load('root_definv_elementary',R/'definite-elementary-readback.py');x,u=H.x,H.u
scalar=H.scalar;eq=H.eq;E.scalar=scalar
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
N=dict(records=0,raw=0,source_banks=0,source_values=0,source_keys=0,formal_inputs=0,bounds=0,differentials=0,basic_primitives=0,bars=0,individual_endpoint_components=0,equalities=0,values=0,pairs=0,fragment_fields=0);tasks={l:set()for l in G.LEVELS}
def integral(raw):
 text=E.clean(H.measure_text(raw));c,F,v,L,U,end=E.integral(text);assert not end.strip().rstrip('.,?'),end;return c*F,v,L,U
def rows(block):return re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','').split(r'\\')
def bar(raw):
 text=E.clean(raw).replace(']_','|_');m=re.search(r'\|_',text);assert m,text
 before=text[:m.start()];after=text[m.end():];lo,j=E.group(after,0);assert after[j]=='^';hi,j=E.group(after,j+1);assert not after[j:].strip(),text
 if before.startswith('['):before=before[1:]
 if before.startswith('{')and before.count('{')>before.count('}'):before=before[1:]
 return scalar(before),scalar(lo),scalar(hi)
def signed_pair(raw):
 text=E.clean(raw).strip();depth=0
 for i,c in enumerate(text):
  if c in '+-'and i>0 and depth==0 and text[i-1]not in '+-*/^':return scalar(text[:i]),(1 if c=='+'else-1)*scalar(text[i+1:])
  depth+=(c in '({')-(c in ')}')
 # A common scalar multiplying an explicitly separated endpoint pair.
 depth=0
 for i,c in enumerate(text):
  if c=='('and depth==0 and text.endswith(')'):
   pair=signed_pair(text[i+1:-1])
   if pair is not None:
    coef=scalar(text[:i])if text[:i].strip()else s.Integer(1);return tuple(coef*a for a in pair)
  depth+=(c in '({')-(c in ')}')
 return None
def response(prompt,fields,vals):
 # Reconstruct the rendered answer suffix, including supplied inverse function.
 text=prompt.split('=',1)[1].replace('$','').strip()
 for f,v in zip(fields,vals):text=text.replace('{{'+f[':answer-field/key']+'}}','('+v+')')
 assert '{{'not in text,text
 return scalar(text)
def check(rec,sid=None):
 q=rec['question'];given=next(b for b in E.blocks(q[':question/problem'])if r'\int'in b);given=given.split('=',1)[0].replace(r'\,','').strip().rstrip('.,?');F,var,L,U=integral(given);assert var==x and L<U
 sol=q[':question/worked-solution'];sub=re.search(r'\$u=(.*?)\$',sol);assert sub;V=scalar(sub[1]);k=s.diff(V,x);assert k.is_positive and not k.has(x)and eq(V,k*x);ul,uh=map(s.simplify,[V.subs(x,L),V.subs(x,U)])
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);basic=next(b for b in blocks if r'\int'in b and '_'not in b and '+C'in b.replace(' ',''));fn=s.asin if'arcsin'in basic else s.atan;kernel=1/s.sqrt(1-u*u)if fn==s.asin else 1/(1+u*u)
 coefficient=s.simplify(F/(kernel.subs(u,V)*k));assert not coefficient.has(x)and coefficient.is_positive
 primitive=coefficient*fn(u);expected=s.simplify(primitive.subs(u,uh)-primitive.subs(u,ul))
 # Complete interval certificate; asin singular endpoints are one-sided limits.
 if fn==s.asin:assert -1<=ul<uh<=1 and s.simplify(1-((ul+uh)/2)**2)>0
 else:assert ul.is_real and uh.is_real and s.ask(s.Q.positive(1+u*u))is True
 dm=next(b for b in blocks if r'\frac{\text{d}u}{\text{d}x}'in b);a,b=re.split(r'⟹|\\quad\\Longrightarrow\\quad',dm);assert eq(scalar(a.split('=',1)[1].replace(r'\,','')),k)
 def measure(raw):
  raw=raw.strip().rstrip('.,').replace(r'\,','');m=re.fullmatch(r'(.*?)'+P.DIFF,raw);assert m,raw;return(scalar(m[1])if m[1].strip()else s.Integer(1))*(k if m[2]=='u'else 1)
 a,b=b.split('=');assert eq(measure(a),measure(b));N['differentials']+=2
 table=re.findall(r'^\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.M);assert [z[0]for z in table]==['x','u'];assert all(eq(scalar(a),b)for a,b in zip(table[0][1:]+table[1][1:],[L,U,ul,uh]));N['bounds']+=4
 for part in basic.rstrip('.').split('='):
  der,ops=H.side(part,u);assert eq(der,kernel);N['basic_primitives']+=1
 seen=False;endpoint_count=0
 for block in blocks:
  if block==basic or r'\int'not in block:continue
  for row in rows(block):
   for term in row.split('='):
    term=term.strip().replace(r'\,','').rstrip('.,')
    if not term:continue
    if r'\int'in term:
     body,v,a,b=integral(term);assert eq(a,L if v==x else ul)and eq(b,U if v==x else uh);effective=body if v==x else body.subs(u,V)*k;assert eq(effective,F),('formal input',term,effective,F);N['formal_inputs']+=1;N['bounds']+=2
    elif ('|'in term or ']_'in E.clean(term)):
     prim,a,b=bar(term);assert eq(a,ul)and eq(b,uh)and eq(s.diff(prim.subs(u,V),x),F);assert eq(prim,primitive);seen=True;N['bars']+=1;N['bounds']+=2
    elif seen:
     assert eq(scalar(term),expected),('evaluated equality',term,expected)
     pair=signed_pair(term)
     if pair is not None:
      target=(primitive.subs(u,uh),-primitive.subs(u,ul));assert(eq(pair[0],target[0])and eq(pair[1],target[1]))or(eq(pair[0],target[1])and eq(pair[1],target[0])),('separate signed endpoint contributions',term,pair,target);endpoint_count+=2
    else:raise AssertionError(('unexpected pre-primitive stage',term))
    N['equalities']+=1
 assert seen and endpoint_count>=2;N['individual_endpoint_components']+=endpoint_count
 fs=q[':question/answer-fields'];selected=[]
 for f in fs:
  vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];aid=f[':answer-field/correct'][1];chosen=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==aid);selected.append(chosen)
  if f[':answer-field/type'].endswith('/radio'):
   assert[a[':answer/id']for a,v in zip(f[':answer-field/choices'],vals)if eq(v,expected)]==[aid]
   for i,v in enumerate(vals):
    for w in vals[:i]:assert not eq(v,w);N['pairs']+=1
  N['values']+=len(vals)
 if fs[0][':answer-field/type'].endswith('/blank'):
  assert eq(response(q[':question/problem'],fs,selected),expected);N['fragment_fields']+=len(fs)
  # All collected blank aliases must yield the same response in their context.
  for i,f in enumerate(fs):
   for a in f[':answer-field/choices']:
    alternate=selected[:];alternate[i]=a[':answer/value'];assert eq(response(q[':question/problem'],fs,alternate),expected)
 if sid:
  ofields=olds[sid][':question/answer-fields'];assert len(ofields)==len(fs)
  for of,f in zip(ofields,fs):
   assert of[':answer-field/key']==f[':answer-field/key']and of[':answer-field/type'][':db/ident']==f[':answer-field/type'];ov=[scalar(a[':answer/value'])for a in of[':answer-field/choices']];nv=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert len(ov)==len(nv)
   remaining=nv[:]
   for v in ov:
    i=next(i for i,w in enumerate(remaining)if eq(v,w));remaining.pop(i)
   oldcorrect=scalar(of[':answer-field/correct'][':answer/value']);newcorrect=scalar(next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]));assert eq(oldcorrect,newcorrect);N['source_keys']+=1;N['source_values']+=len(ov)
  N['source_banks']+=1
 N['records']+=1;tasks[q[':question/difficulty'].split('/')[-1]].add((s.srepr(F),str(L),str(U)))
for sid,o in olds.items():
 case=next(c for c in json.load(open(D/'source-cases.json'))if c['source_id']==sid);q=case['record']['question'];assert q[':question/problem']==o[':question/problem']or q[':question/problem']==G.fmt.normalize_prose(o[':question/problem']);assert q[':question/worked-solution']==o[':question/worked-solution']or q[':question/worked-solution']==G.fmt.normalize_prose(o[':question/worked-solution']);N['raw']+=1
 check(G.generate(G.PROFILES[sid]['difficulty'],template=sid,parameters={'h':1,'k':1}),sid)
 for p in({'h':2,'k':1},{'h':1,'k':1 if G.PROFILES[sid]['field_shape']=='asin-argument'else 3},{'h':9,'k':1 if G.PROFILES[sid]['field_shape']=='asin-argument'else 9}):check(G.generate(G.PROFILES[sid]['difficulty'],template=sid,parameters=p))
for l in tasks:
 for seed in range(18):check(G.generate(l,seed))
# A compensating endpoint corruption keeps the total answer correct but must fail.
import copy
probe=G.generate('hard',template='q-19394',parameters={'h':2,'k':1});block=probe['question'][':question/worked-solution'].split('$$')[-2]
term=next(t.strip()for row in rows(block)for t in row.split('=')if r'\int'not in t and '|'not in t and ']'not in t and signed_pair(t.strip())is not None and 'arcsin'in t)
pair=signed_pair(term);replacement='('+s.latex(pair[0]+1)+')-('+s.latex(-pair[1]+1)+')';assert eq(scalar(replacement),scalar(term));probe['question'][':question/worked-solution']=probe['question'][':question/worked-solution'].replace(term,replacement,1)
saved=N.copy()
try:check(probe)
except AssertionError as error:assert 'separate signed endpoint contributions'in str(error)
else:raise AssertionError('compensating endpoint corruption was missed')
N.clear();N.update(saved)
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,negative_controls=['equal total but offset each signed endpoint by1 rejected'],sampled_actual_tasks={l:len(t)for l,t in tasks.items()},domain_proof='Positive linear substitution independently read. Inverse sine full interval -1<=u<=1, strict interior; finite primitive endpoint values correctly evaluate integrable one-sided singularities. Inverse tangent denominator1+u² positive everywhere. Every formal operand and actual bound, primitive, signed endpoint contribution and supplied answer-fragment context verified.',scope='Observed definite inverse-sine and inverse-tangent normalization; positive radial/numerator slots preserve normalized endpoint roles and same method. No unsupported arcsec branch.',native_limitations='48 genuine normal blank equivalent-entry false rejections retained in private native-gaps.json; canonical answers/wrong answers correct; root generic sample canonical checks passed. Qualified local generation approval only; no engine edits or output pruning.',database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
