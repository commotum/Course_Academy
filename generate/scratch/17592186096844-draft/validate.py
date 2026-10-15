"""Independent displayed prompt/answer/solution readback plus real learner grader."""
import functools,copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('kp_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('strict_tex',H/'math_parser.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x=p.x;t=p.t

def scalar(raw):
 raw=raw.replace('[','(').replace(']',')').replace(r'\prime',"'").replace(r'\text{⧸}','').replace(r'\quad',',').replace(r'\!','')
 return p.scalar(raw)
@functools.lru_cache(maxsize=8192)
def equal(a,b):
 # Independent exact quotient-ring proof of rational trig identities.
 diff=s.cancel(a-b)
 if diff==0:return True
 if diff.has(s.sin,s.cos,s.tan,s.sec):
  args=sorted({f.args[0] for f in diff.atoms(s.sin,s.cos,s.tan,s.sec)},key=str)
  replacements={};relations=[];vars=[]
  for i,arg in enumerate(args):
   S,C=s.symbols('read_s'+str(i)+' read_c'+str(i));vars.extend([S,C]);relations.append(S*S+C*C-1)
   replacements.update({s.sin(arg):S,s.cos(arg):C,s.tan(arg):S/C,s.sec(arg):1/C})
  numerator=s.fraction(s.cancel(diff.xreplace(replacements)))[0]
  return s.groebner(relations,*vars,domain='EX').reduce(s.expand(numerator))[1]==0
 return s.simplify(diff)==0

def prompt_data(q):
 text=q[':question/problem']
 matches=re.findall(r'\$(?:y|f\(x\)|x\(t\))=(.*?)\$',text,re.S)
 if not matches:raise ValueError('Undefined function in standalone prompt')
 raw=matches[0].strip().rstrip('.,');raw=raw.split(r'\,t>0')[0];F=scalar(raw);var=t if F.has(t) else x
 point=None
 if 'tangent line' in text:
  point=scalar(re.search(r'at \$x=(.*?)\$',text)[1])
 elif re.search(r'find .*?\((\d+)\)',text):point=s.Integer(re.search(r'find .*?\((\d+)\)',text)[1])
 return F,var,point

def fingerprint(q):
 try:
  F,z,pt=prompt_data(q)
  fragment='| --- |' in q[':question/problem']
  return g.digest([s.srepr(s.cancel(F)),str(z),s.srepr(pt) if pt is not None else None,'fragment' if fragment else 'complete'])
 except (ValueError,AssertionError):
  # Incomplete prompts are unavailable, but their source solution's explicit
  # motion function still reserves its mathematical task against duplicates.
  match=re.search(r'x\(t\)=(.*?),\\,t>0',q.get(':question/worked-solution',''),re.S)
  if match:
   F=scalar(match[1]);return g.digest([s.srepr(s.cancel(F)),str(t),None,'complete'])
  return 'undefined:'+g.digest(q[':question/problem'])

def bank_check(q):
 F,z,pt=prompt_data(q);expected=s.diff(F,z)
 if pt is not None:expected=s.simplify(expected.subs(z,pt))
 fields=q.get(':question/answer-fields',[]);assert len(fields)==1,'Incomplete fields'
 f=fields[0];ft=f[':answer-field/type'];ft=ft.get(':db/ident') if isinstance(ft,dict) else ft
 correct=f[':answer-field/correct'];cid=str(correct[':answer/id']) if isinstance(correct,dict) else correct[1]
 values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
 if '| --- |' in q[':question/problem']:
  rows=q[':question/problem'].splitlines();denraw=rows[-1].split('|')[3].strip().strip('$');den=scalar(denraw)
  multiplier=1
  head=rows[-3].split('|')[3]
  if '{{field-1}}$)' in head:multiplier=scalar(head.split('{{field-1}}$)',1)[1].strip().strip('$'))
  values=[v*multiplier/den for v in values]
 assert len(values)==(5 if ft.endswith('/radio') else 1)
 valid=[equal(v,expected) for v in values];assert sum(valid)==1,('Invalid answer',q.get(':question/math-academy-id'),valid,expected,values)
 assert str(f[':answer-field/choices'][valid.index(True)][':answer/id'])==cid
 assert all(not equal(v,w) for i,v in enumerate(values) for w in values[:i])
 return F,z,pt

def solution_check(q):
 F,z,pt=bank_check(q);work=q[':question/worked-solution'];der=s.diff(F,z)
 # Read actual numerator/denominator definitions, then all computed stages.
 defs={}
 for name,var,raw in re.findall(r'\$([uvgh])\(([xt])\)=(.*?)\$',work,re.S):
  assert var==str(z),'Bound independent variable changed'
  defs[name]=scalar(raw)
 assert len(defs)==2,(q.get(':question/math-academy-id'),defs)
 assert set(defs)==({'g','h'} if z==t else {'u','v'})
 for name,arg in re.findall(r'([uvgh])\(([xt])\)',work):assert arg==str(z),'Stale solution variable reference'
 # Read formal quotient operator operands/order/square as printed, independently.
 formal=next(block for block in re.findall(r'\$\$(.*?)\$\$',work,re.S) if '&' in block)
 firstrow=re.sub(r'\\(?:begin|end)\{aligned\}','',formal).split(r'\\')[0]
 lhs,rule=firstrow.split(' & =',1)
 target_norm=lambda txt:re.sub(r'[{}^\s]','',txt.replace("'",'′').replace(r'\prime','′'))
 D=r'\frac{\text{d}y}{\text{d}x}'
 targets=[r'{x}^{′}(t)'] if z==t else [r'{f}^{′}(x)'] if 'f(x)=' in q[':question/problem'] else [D,r'{y}^{′}',r'{y}^{′}(x)',r'{y}^{′}='+D]
 assert target_norm(lhs) in {target_norm(v) for v in targets},('Printed derivative target',lhs)
 n,dn=('g','h') if z==t else ('u','v');Z=str(z)
 expected_rule=rf'\frac{{{{{n}}}^{{′}}({Z})\cdot {dn}({Z})-{n}({Z})\cdot {{{dn}}}^{{′}}({Z})}}{{[{dn}({Z})]^{{2}}}}'
 norm=lambda txt:re.sub(r'\s+','',txt.replace("'",'′'))
 assert norm(rule)==norm(expected_rule),(rule,expected_rule)
 names=list(defs);assert equal(defs[names[0]]/defs[names[1]],F)
 assert work.count('$')%2==0 and q[':question/problem'].count('$')%2==0
 def rhs(raw):
  raw=re.sub(r'\{([uvgh])\}',r'\1',raw).replace('′',"'")
  raw=re.sub(r"\^\{'\}","'",raw)
  for name,obj in defs.items():
   raw=re.sub(name+r"'\(([xt])\)",lambda m:'('+g.tex(s.diff(obj,z))+')',raw)
   raw=re.sub(name+r'\(([xt])\)',lambda m:'('+g.tex(obj)+')',raw)
   raw=re.sub(r"\b"+name+r"'",lambda m:'('+g.tex(s.diff(obj,z))+')',raw)
   raw=re.sub(r"\b"+name+r"\b",lambda m:'('+g.tex(obj)+')',raw)
  return scalar(raw)
 count=0
 for display in re.findall(r'\$\$(.*?)\$\$',work,re.S):
  display=re.sub(r'\\(?:begin|end)\{aligned\}','',display)
  rows=display.split(r'\\');is_derivative='&' in display
  if not is_derivative:
   # Directly test each displayed u' and v' definition as well.
   for name,arg,raw in re.findall(r"\{?([uvgh])\}?\^?\{?[′']\}?\(([xt])\)\s*=\s*(.*?)(?:,\\,|,\\quad|,|$)",display.strip().rstrip('.')):
    assert arg==str(z),'Derivative argument binding changed'
    assert equal(scalar(raw),s.diff(defs[name],z)),raw
   continue
  evaluated=pt is not None and any(marker in display for marker in ('m &',"y'(",'{y}^{′}(1)',r'{y}^{\prime}('))
  # Source evaluation blocks have m=f'(point), y'(point), and then numbers.
  if pt is not None and ('Therefore,' in work):
   position=work.find(display[:20]) if display[:20] in work else -1
   # Their first derivative block always contains the formal quotient rule.
   evaluated=not any(tag in display for tag in ("u}^{", "u'(","u'",'u}^{'))
  for row in rows:
   if '=' not in row:continue
   raw=row.rsplit('=',1)[1].replace('&','').strip().rstrip('.')
   raw=re.sub(r'\{([fy])\}',r'\1',raw)
   if pt is not None and re.search(r"(?:f|y)\s*\^?\{?[′']\}?\s*\\?,?\s*\(",raw):
    continue # evaluation label; subsequent substitutions carry the evidence
   got=rhs(raw);expected=der.subs(z,pt) if evaluated else der
   assert equal(got,expected),('Solution stage',row,got,expected)
   count+=1
 assert count>=3
 return count

def independent(rec):
 gen=rec['generation'];m=gen['template'];g.validate_parameters(m,gen['parameters'])
 assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 assert rec['question'][':question/difficulty']==':question.difficulty/'+g.LEVELS[m]
 assert gen['domain']==g.domain(m,gen['parameters'])
 F,z,point=prompt_data(rec['question'])
 actual_zeroes=[n for n in s.solve(s.denom(F),z) if n.is_real is not False]
 reported_zeroes=[scalar(n) for n in gen['domain']['denominator_zeroes']]
 assert len(actual_zeroes)==len(reported_zeroes) and all(any(equal(a,b) for b in reported_zeroes) for a in actual_zeroes),'Printed denominator zeroes/domain mismatch'
 if F.has(s.log):assert gen['domain']['restriction']==('x>1' if F.has(s.sqrt(s.log(x))) else 'x>0')
 if z==t:assert gen['domain']['restriction']=='t>0'
 if point is not None:assert s.denom(F).subs(z,point)!=0
 if F.has(s.tan):
  I=next(iter(F.atoms(s.tan))).args[0];assert equal(scalar(gen['domain']['chain_inner']),I)
 stages=solution_check(rec['question'])
 assert rec==g.generate(gen['level'],gen['seed'],template=m,parameters=gen['parameters'])
 return stages

def expected_bank_from_givens(q):
 F,z,pt=prompt_data(q);f=q[':question/answer-fields'][0]
 # Read source shape from visible functions, then derive complete operation patterns.
 if f[':answer-field/type'].endswith('/blank'):return
 m=q['_template'];expected=s.diff(F,z)
 if m=='q-11973':
  c=s.solve(s.denom(F),x)[0]*-3
  vals=[6*x/(3*x+c)**3,x/(3*x+c)**4,expected,2*x/(3*x+c)**4,c*x/(3*x+c)**4]
 elif m=='q-2396':
  T=next(iter(F.atoms(s.tan)));I=T.args[0];S=s.sec(I)**2
  vals=[expected,(7*S-T)/(16*x*x),(x*S+T)/(4*x*x),(7*x*S-T)/(16*x*x),(S-T)/(4*x*x)]
 elif m=='q-11978':
  a=s.sqrt(s.denom(F).subs(x,0));D=(x*x+a*a)**2
  vals=[(a-x)**2/D,2*(x+a)/D,expected,2*(a-x)/D,(a-2*x*x)/D]
 elif m=='q-2403':
  a=s.simplify(s.sqrt(s.log(x))/(x*F));L=s.log(x)
  vals=[(x-a*s.sqrt(L))/(a*a*x*x*L),(a/s.Integer(2)-a*L)/s.sqrt(L),(1+a*s.sqrt(L))/(a*x*x*s.sqrt(L)),expected,(L-a)/s.sqrt(L)]
 actual=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(actual)==len(vals) and all(sum(equal(a,b) for b in actual)==1 for a in vals),('whole bank',m)

def checks(rec):
 f=rec['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'Every owned radio ID'} for a in f[':answer-field/choices']]
 a=f[':answer-field/choices'][0][':answer/value']
 return [{'field_index':0,'submitted':v,'expected':e,'purpose':purpose} for v,e,purpose in [(a,'accepted','canonical fragment'),('2('+a+')/2','accepted','unreduced equivalent fragment'),('0','rejected','incorrect zero'),('1','rejected','incorrect one'),('('+a+')+1','rejected','incorrect offset')]]

def save(n,o):(H/n).write_text(json.dumps(o,indent=2,default=str)+'\n')
def rejected(fn):
 try:fn()
 except (AssertionError,ValueError,StopIteration,KeyError):return True
 raise AssertionError('Negative control accepted')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 raw=[];cases=[];normal=[];review=[];steps=0;stats={}
 snapshot=ROOT/'generate/runs/current/refresh-2026-10-14/sources'/f'{g.KP_ID}.json'
 assert g.SOURCE==json.loads(snapshot.read_text())
 for m,o in g.SOURCES.items():
  r=g.generate(g.LEVELS[m],template=m,parameters=g.DEFAULTS[m],profile='observed_raw');assert r['question']==o
  raw.append(r);cases.append({'source_id':m,'template':m,'level':g.LEVELS[m],'parameters':g.DEFAULTS[m],'profile':'observed_raw'})
 for m,l in g.LEVELS.items():
  if m in g.EXCLUDED:continue
  print('Validating whole public domain',m,flush=True);variants=[]
  for i,pv in enumerate(g.parameters_for(m)):
   r=g.generate(l,i,template=m,parameters=pv);steps+=independent(r)
   actual=copy.deepcopy(r['question']);actual['_template']=m;expected_bank_from_givens(actual)
   variants.append(r);normal.append(r)
  stats[m]={'count':len(variants),'parameters':[r['generation']['parameters'] for r in variants],'semantic_tasks':len({r['generation']['parameter_fingerprint'] for r in variants}),'normal_prose':'full source component masks' if m in g.SOURCES else 'authored source-common ordered quotient/chain stages'}
  review.extend([variants[0],variants[-1]])
  r=g.generate(l,template=m,parameters=g.DEFAULTS[m]);review.append(r)
  if m in g.SOURCES:
   sf=g.SOURCES[m][':question/answer-fields'][0];nf=r['question'][':question/answer-fields'][0]
   assert len(sf[':answer-field/choices'])==len(nf[':answer-field/choices'])
   for a in sf[':answer-field/choices']:assert sum(equal(scalar(a[':answer/value']),scalar(b[':answer/value'])) for b in nf[':answer-field/choices'])==1
   if m!='q-132975':assert r['question'][':question/problem']==g.math_format.normalize_prose(g.SOURCES[m][':question/problem'])
   if m!='q-132975':assert r['question'][':question/worked-solution']==g.math_format.normalize_prose(g.SOURCES[m][':question/worked-solution'])
 negatives=0
 for m,l in g.LEVELS.items():
  rejected(lambda:g.generate(l,template=m,parameters={k:99 for k in g.DEFAULTS[m]} if g.DEFAULTS[m] else {'x':99}));negatives+=1
  rejected(lambda:g.generate(next(v for v in g.SUPPORTED_LEVELS if v!=l),template=m));negatives+=1
 for m in g.EXCLUDED:rejected(lambda:g.generate(g.LEVELS[m],template=m));negatives+=1
 for m,l in g.LEVELS.items():
  if m in g.EXCLUDED:continue
  base=g.generate(l,template=m,parameters=g.DEFAULTS[m]);q=base['question']
  for part in ('prompt','formal-minus','formal-square','operand','target','derivative','intermediate','answer','key','domain'):
   mutated=copy.deepcopy(base);mq=mutated['question'];sol=mq[':question/worked-solution']
   if part=='prompt':mq[':question/problem']=mq[':question/problem'].replace('y=','y=2*',1).replace('f(x)=','f(x)=2*',1).replace('x(t)=','x(t)=2*',1)
   if part=='formal-minus':mq[':question/worked-solution']=sol.replace('-u(x)', '+u(x)',1).replace('-g(t)','+g(t)',1)
   if part=='formal-square':mq[':question/worked-solution']=sol.replace('[v(x)]^{2}','[v(x)]^{3}',1).replace('[h(t)]^{2}','[h(t)]^{3}',1)
   if part=='operand':mq[':question/worked-solution']=sol.replace('v(x)-u(x)','u(x)-u(x)',1).replace('h(t)-g(t)','g(t)-g(t)',1)
   if part=='target':mq[':question/worked-solution']=sol.replace('Differentiating $u(x)$','Differentiating $u(t)$',1).replace('Differentiating $g(t)$','Differentiating $g(x)$',1)
   if part=='derivative':mq[':question/worked-solution']=sol.replace("}(x)=","}(x)=2*",1).replace('}(t)=','}(t)=2*',1)
   if part=='intermediate':mq[':question/worked-solution']=sol.replace('& =\\frac','& =2*\\frac',1)
   if part=='answer':mq[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+=' + 1'
   if part=='key':mq[':question/answer-fields'][0][':answer-field/correct'][1]='wrong'
   if part=='domain':mutated['generation']['domain']={'restriction':'all real x'}
   if mutated!=base:rejected(lambda:independent(mutated));negatives+=1
 for l in g.SUPPORTED_LEVELS:
  for seed in range(24):independent(g.generate(l,seed))
 cli=subprocess.run([str(ROOT/'.venv/bin/python'),str(H.with_suffix('.py')),'--difficulty','all','--count','1','--format','json'],capture_output=True,text=True,check=True);assert len(json.loads(cli.stdout))==3
 engine=[{'label':str(i)+' '+r['generation']['template']+' '+str(r['generation']['parameters']),'record':r,'checks':checks(r)} for i,r in enumerate(normal)]
 save('source-cases.json',cases);save('engine-input.json',engine);binary=ROOT/'generate/runs/current/check-engine';assert sha(binary)=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 run=subprocess.run([str(binary),str(H/'engine-input.json'),str(H/'engine-report.json')],capture_output=True,text=True);(H/'engine.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr
 native=json.loads((H/'engine-report.json').read_text());assert native['documented_unresolved_checks']==0
 base=json.loads((H/'registered-baseline.json').read_text())['paths'];actual={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'generate/scratch/17592186096844.py']+list((ROOT/'generate/scratch/17592186096844').rglob('*')) if p.is_file()};assert actual==base
 save('review.json',{'source_evidence':raw,'eligible_variants':review})
 sections=['# Chain and quotient rule draft review','Full source raw objects retain every attribute and omission. All normal solutions use the complete shared source sentences and operative stages. Easy is authored; no source easy difficulty exists. q-132975 receives the exact function and domain stated in its solution and a standalone denominator differentiation sentence.']
 for r in raw+review:sections+=['## '+('Frozen raw evidence ' if r['generation']['evidence_only'] else 'Eligible '+r['generation']['level']+' ') + r['generation']['template']+' '+str(r['generation']['parameters']),g.markdown(r)]
 (H/'review.md').write_text('\n\n'.join(sections)+'\n')
 report={'status':'pass','source_basis':2275,'raw_source_questions':len(raw),'full_raw_object_replay':True,'eligible_domain_cases':len(normal),'domain_counts':stats,'semantic_tasks_by_level':{l:len({r['generation']['parameter_fingerprint'] for r in normal if r['generation']['level']==l}) for l in g.SUPPORTED_LEVELS},'solution_stages_checked':steps,'negative_controls':negatives,'source_bank_options':sum(len(f[':answer-field/choices']) for q in g.SOURCES.values() for f in q.get(':question/answer-fields',[])),'supported_source_banks':11,'supported_radio_distractors':16,'raw_only_exclusions':g.EXCLUDED,'grading':{k:v for k,v in native.items() if k!='records'},'registered_baseline_unchanged':True,'engine_sha256':sha(binary)}
 save('validation.json',report);save('freeze.json',{'version':g.VERSION,'registered_baseline_unchanged':True,'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [H.with_suffix('.py')]+sorted(H.rglob('*')) if p.is_file() and p.name!='freeze.json' and '__pycache__' not in str(p)}});print(json.dumps({k:v for k,v in report.items() if k!='domain_counts'},indent=2))
if __name__=='__main__':main()
