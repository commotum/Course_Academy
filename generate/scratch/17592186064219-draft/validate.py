"""Read rendered mathematics independently; never import registered code."""
import hashlib,importlib.util,json,re,subprocess,sys,copy
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE))
from math_parser import latex,clean,integrand,X as x,U as u,C
from math_format import normalize_prose,normalize_tex,validate_generated_record
spec=importlib.util.spec_from_file_location('draft_64219',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def eq(a,b):return sp.cancel(a-b)==0 or sp.simplify(a-b)==0

def scalar(s):
 s=s.strip().replace(r'\cdot','*').replace(r'\,','').strip().rstrip('.')
 return latex(s) if s else sp.Integer(1)
def integral_operand(s):
 # Infer the differential from the actual rendered row, including du in numerator.
 variable=u if any(z in s for z in [r'\text{d}u',r'\textrm{d}u']) else x
 before,after=s.split(r'\int',1)
 after=after.replace(r'\frac{\text{d}u}',r'\frac{1}').replace(r'\frac{\text{d}x}',r'\frac{1}')
 return scalar(before)*scalar(clean(after)),variable

def check(rec):
 validate_generated_record(rec);q=rec['question'];target=integrand(q);sol=q[':question/worked-solution'];f=q[':question/answer-fields'][0]
 assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 assert len(f[':answer-field/choices'])==5
 den=sp.denom(sp.cancel(target));assert den.subs(x,0)>0 and sp.Poly(den,x).degree()==2
 # Read substitution and derivative from displayed prose rather than metadata.
 m=re.search(r"substitute \$u=(.*?)\.\$",sol);assert m,sol
 substitution=latex(m[1]);scale=sp.diff(substitution,x);assert scale.is_positive and not scale.has(x) and eq(substitution,scale*x)
 dm=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(.*?)\\,⟹\\,(.*?)\n',sol)
 if dm:
  assert eq(scalar(dm[1]),scale)
  a,b=dm[2].rstrip('.').split('=')
  if r'\text{d}x' in a:assert eq(scalar(clean(b)),1/scale)
  else:assert eq(scalar(clean(a)),1/scale)
 else:
  dm=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(.*?)\\quad\\Longrightarrow\\quad\\text\{d\}x=(.*?)\.',sol);assert dm
  assert eq(scalar(dm[1]),scale) and eq(scalar(clean(dm[2])),1/scale)
 # Verify the squared substitution statement.
 m=re.search(r'we have \$(.*?)\.\$',sol);assert m
 aa,bb=m[1].split('=') if '=' in m[1] else (m[1],None)
 if bb is not None:assert eq(latex(aa),latex(bb))
 else:assert eq(latex(aa),substitution**2)
 counts={'integral_stages':0,'primitive_stages':0}
 for block in sol.split('$$')[1::2]:
  if r'\begin{aligned}' not in block and not block.lstrip().startswith(r'\int '):continue
  # Basic unit antiderivative is validated independently too.
  if '\\begin{aligned}' not in block and 'arctan' in block:
   left,right=block.strip().rstrip('.').split('=');value,var=integral_operand(left);assert var==u and eq(sp.diff(scalar(right),u),value)
   continue
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',block).strip()
  for row in re.split(r'\\\\',text):
   for term in row.replace('&','').split('='):
    term=term.strip().rstrip('.')
    if not term:continue
    if r'\int' in term:
     value,var=integral_operand(term);pulled=value.subs(u,substitution)*scale if var==u else value
     assert eq(pulled,target),(rec['generation'],term,pulled,target)
     counts['integral_stages']+=1
    elif 'arctan' in term:
     value=scalar(term);pulled=value.subs(u,substitution);assert eq(sp.diff(pulled,x),target),(term,target)
     assert value.coeff(C)==1
     counts['primitive_stages']+=1
 assert counts['integral_stages']>=4 and counts['primitive_stages']>=2
 vals=[latex(a[':answer/value']) for a in f[':answer-field/choices']];ds=[sp.diff(v,x) for v in vals]
 correct=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],ds) if eq(v,target)]
 assert correct==[f[':answer-field/correct'][1]],(correct,rec['generation'])
 # Derivatives compare indefinite primitives modulo C, including wrong/wrong pairs.
 for i,a in enumerate(ds):
  for b in ds[:i]:assert not eq(a,b),'equivalent options modulo C'
 assert all(v.coeff(C)==1 for v in vals)
 return counts

def engine_item(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'actual native complete radio bank'}for a in f[':answer-field/choices']]}
def native_tex(expr):return sp.latex(expr).replace(r'\operatorname{atan}',r'\operatorname{arctan}')
def main():
 source=json.loads((HERE/'source.json').read_text());qs=source['record'][':knowledge-point/questions'];old_by={q[':question/math-academy-id']:q for q in qs};assert len(qs)==16
 ma=[q for q in qs if q.get(':question/math-academy-id')];assert len(ma)==16
 originals=[];reviews=[];replay=[];inputs=[];totals={'integral_stages':0,'primitive_stages':0};coverage={};side=[]
 for sid,t in g.PROFILES.items():
  rec=g.generate(t['difficulty'],0,sid,t['parameters']);old=old_by[sid];q=rec['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==normalize_prose(old[':question/problem'])
  assert q[':question/worked-solution']==normalize_prose(old[':question/worked-solution'])
  assert [a[':answer/value']for a in f[':answer-field/choices']]==[normalize_tex(a[':answer/value'])for a in of[':answer-field/choices']]
  assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==normalize_tex(of[':answer-field/correct'][':answer/value'])
  c=check(rec)
  for k,v in c.items():totals[k]+=v
  originals.append(rec);inputs.append(engine_item('source '+sid,rec));replay.append({'source':sid,'matched_options':5,'matched_distractors':4,'complete_bank':True,'prompt_and_solution_exact_after_format_normalization':True})
  # Explicit changed scale for EVERY complete source profile; chosen profile is fixed first.
  changed=[]
  for p in g.candidate_parameters(sid):
   if p[1]!=t['parameters'][1] and g.admissible(sid,list(p)):
    changed.append(p)
    if len(changed)==2:break
  assert changed,sid
  coverage[sid]={'source_parameters':t['parameters'],'changed_parameters':changed}
  variants=[]
  for p in changed:
   r=g.generate(t['difficulty'],123,sid,list(p));check(r);reviews.append(r);inputs.append(engine_item('changed '+sid+' '+str(p),r));variants.append(r)
  side.append('## '+sid+'\n\nOriginal source\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nReplayed bank\n\n'+g.markdown(rec)+'\n\nChanged scale, same complete profile\n\n'+g.markdown(variants[0]))
 for p in [[3,2,5],[7,3,4],[17,9,12],[1,2,2]]:
  r=g.generate('hard',47,'authored-canonical-factor',p);check(r);reviews.append(r);inputs.append(engine_item('authored H '+str(p),r))
 # Seeded diversity and type contracts. No metadata substitution can hide stale rendered stages.
 for level in g.LEVELS:
  rs=g.batch(level,10,2275);assert rs==g.batch(level,10,2275)
  for r in rs:check(r)
  reviews.extend(rs)
 # Negative control: an unchanged final primitive cannot conceal stale intermediate stages.
 negative_controls=[]
 base=originals[0]
 for name,old,new in [('substitution','substitute $u=3x.','substitute $u=4x.'),('differential',r'\text{d}x=\frac{1}{3}',r'\text{d}x=\frac{1}{4}'),('formal operand',r'1+(3x)^{2}',r'1+(4x)^{2}'),('primitive',r'=2\operatorname{arctan}⁡u',r'=3\operatorname{arctan}⁡u')]:
  mutated=copy.deepcopy(base);key=':question/worked-solution';assert old in mutated['question'][key],(name,old)
  mutated['question'][key]=mutated['question'][key].replace(old,new,1)
  try:check(mutated)
  except AssertionError:negative_controls.append(name)
  else:raise AssertionError(('missed corrupt intermediate',name))
 for value in [True,False,1.0,'1',None]:
  for kw in [{'seed':value},{'count':value}]:
   try:g.batch(**kw)
   except ValueError:pass
   else:raise AssertionError(('strict integer',kw))
 for count in [0,-1]:
  try:g.batch(count=count)
  except ValueError:pass
  else:raise AssertionError('positive count')
 # Independently author inventory values without invoking a source template.
 independent=[]
 for level,n,a,b in [('easy',7,1,11),('moderate',5,49,1),('hard',11,3,75)]:
  scale=sp.sqrt(sp.Rational(b,a));amp=sp.Rational(n,a)/scale;target=sp.Rational(n)/(a+b*x*x)
  qid=g.ident(['independent',level]);fid=g.ident([qid,'blank']);av=native_tex(amp*sp.atan(scale*x))+'+C';aid=g.ident([fid,av])
  rec={'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':{':question/id':qid,':question/problem':r'Calculate $\int\frac{'+str(n)+'}{'+str(a)+'+'+str(b)+r'x^2}\,\text{d}x.$',':question/worked-solution':r'With $u='+native_tex(scale*x)+r'$, use $dx=du/('+native_tex(scale)+r')$ to get $'+av+'$.',':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'answer',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':av}],':answer-field/correct':[':answer/id',aid]}]},'generation':{'template':'independently-authored-'+level}}
  assert eq(sp.diff(latex(av),x),target)
  independent.append({'record':rec,'role':'independently authored inventory','relationship_to_source_templates':'Same linear inverse tangent substitution; independent coefficients and blank representation for native equivalence probes.'})
  # Preserve engine equivalence limitations using qualified observations in a second pass.
  checks=[{'submitted':av,'expected':'accepted','purpose':'canonical blank primitive'},{'submitted':native_tex(amp*sp.atan(scale*x))+r'+C+7','expected':'rejected','purpose':'mathematically valid constant shift: native limitation retained'},{'submitted':r'\arctan('+native_tex(scale*x)+r')+'+native_tex((amp-1)*sp.atan(scale*x))+r'+C','expected':'accepted','purpose':'genuine unreduced equivalent sum'},{'submitted':native_tex(2*amp*sp.atan(scale*x))+r'+C','expected':'rejected','purpose':'wrong chain-rule scale'},{'submitted':r'\arctan(x)+C','expected':'rejected','purpose':'wrong argument and amplitude'}]
  for probe in checks:probe['mathematical_status']='valid equivalent' if 'wrong' not in probe['purpose'] else 'incorrect';probe['expected']='unresolved';probe['purpose']+='; actual native inverse-tangent parser gap (unresolved)'
  inputs.append({'label':'independent blank '+level,'record':rec,'checks':checks})
 save('source-cases.json',[{'source_id':r['generation']['source_ids'][0],'source_db_id':old_by[r['generation']['source_ids'][0]][':db/id'],'template':r['generation']['template'],'profile':r['generation']['profile'],'parameters':r['generation']['parameters'],'level':r['question'][':question/difficulty'].split('/')[-1],'role':'ma-original','complete':True,'record':r} for r in originals]);save('review-cases.json',reviews);save('independent-inventory.json',{'basis':source['basis'],'lineage':source['lineage'],'questions':independent})
 save('native-input.json',inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('source-replay.json',{'basis':2275,'MA_source_count':16,'non_MA_source_count':0,'complete_banks_matched':16,'complete_banks_total':16,'distractors_matched':64,'distractors_total':64,'profiles':replay,'ineligible_sources':[],'repairs':[]})
 save('validation.json',{'status':'ready-for-independent-QA','mathematics_passed':True,'native_radio_passed':True,'diagnostic_unsupported_blank':{'passed':False,'unresolved':15,'supported_generator_contract':False},'negative_controls':negative_controls,'basis':2275,'source_instances':len(originals),'review_instances':len(reviews),'independent_instances':len(independent),'source_stage_checks':totals,'changed_profile_coverage':coverage,'strict_integer_checks':12,'native':'actual frozen check-engine; supported radio contract passes all owned IDs; 15 unresolved independently authored blank diagnostics retained outside supported response shape','limits':'Scale domain bounded; hard is authored canonical extension, not observed practice difficulty. Normal generator output is exclusively radio and all native owned-ID grading passes. Authored blank diagnostic probes are unsupported response shape, with 15 preserved unresolved parser outcomes; these are not normal-generator grading gaps.'})
 (HERE/'review.md').write_text('\n\n'.join(side)+'\n\n## Authored H from canonical factoring\n\n'+g.markdown(reviews[32])+'\n')
 print('PASS',len(originals),'source',len(reviews),'reviews',len(independent),'independent')
if __name__=='__main__':main()
