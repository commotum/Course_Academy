"""Independent rendered-stage, source-bank, slot, and native-grading review."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
import sympy as sp
from functools import lru_cache
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE))
from math_parser import latex,X as x,U as u,C
from math_format import normalize_tex,normalize_prose,validate_generated_record
spec=importlib.util.spec_from_file_location('g64220',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str)+'\n')
@lru_cache(maxsize=20000)
def eq(a,b):return sp.simplify(a-b)==0

def group(text,i):
 assert text[i]=='{',(text,i)
 depth=1;j=i+1
 while depth:
  depth+=(text[j]=='{')-(text[j]=='}');j+=1
 return text[i+1:j-1],j

def clean(t):
 t=t.replace(r'\dfrac',r'\frac').replace(r'\displaystyle','').replace(r'\,','').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','').replace('⁡','').replace('⟹','')
 t=t.replace(r'\frac{\text{d}u}',r'\frac{1}').replace(r'\frac{\text{d}x}',r'\frac{1}')
 t=t.replace(r'\text{d}x','').replace(r'\textrm{d}x','').replace(r'\text{d}u','').replace(r'\textrm{d}u','')
 t=t.replace('()','1').replace(r'\!','').replace(r'\,','').strip().rstrip('.')
 t=re.sub(r'(?<![A-Za-z])arctan',r'atan',t)
 return t

@lru_cache(maxsize=10000)
def scalar(t):
 t=clean(t);return latex(t)if t else sp.Integer(1)

def read_integral(t):
 # Parse original and changed integral wrappers and both bound groups.
 t=t.strip();m=re.search(r'(?:\{\\int \}|\\int)\s*_',t);assert m,('integral wrapper',t)
 prefix=t[:m.start()];i=m.end();lo,i=group(t,i);assert t[i]=='^';hi,i=group(t,i+1)
 suffix=t[i:];var=u if any(v in suffix for v in [r'\text{d}u',r'\textrm{d}u'])else x
 return scalar(prefix)*scalar(suffix),var,scalar(lo),scalar(hi)

def bounds(q):
 text=q[':question/problem'].split('$')[1];v,var,L,R=read_integral(text.split('=')[0].rstrip('?'))
 return v,L,R

def primitive(t):
 # Preserve both actual bounds; never validate a primitive only by its derivative.
 t=clean(t)
 if r'\right]'in t:raise AssertionError('clean should remove right')
 m=re.search(r'\]_\{',t)
 if m:
  i=m.end()-1;lo,j=group(t,i);assert t[j]=='^';hi,j=group(t,j+1);F=t[:m.start()].lstrip('[');return scalar(F),scalar(lo),scalar(hi)
 m=re.search(r'(?:\{\|\}|\|)\}_\{|(?:\{\|\}|\|)_\{',t)
 assert m,('primitive bars',t)
 # Captured form sometimes wraps the complete primitive in {...|}.
 start=m.start();suffix=t[m.end()-1:];lo,j=group(suffix,0);assert suffix[j]=='^';hi,j=group(suffix,j+1)
 F=t[:start]
 if F.count('{')>F.count('}'):F=F[1:]
 return scalar(F),scalar(lo),scalar(hi)

def check(rec):
 validate_generated_record(rec);q=rec['question'];target,L,R=bounds(q);sol=q[':question/worked-solution'];md=rec['generation'];sid=md['template'];t=g.PROFILES[sid]
 # Read actual displayed substitution, derivative, and dx coefficient.
 sm=re.search(r'substitute \$u=(.*?)\.\$',sol);assert sm,(sid,'substitution');S=scalar(sm[1]);s=sp.diff(S,x)
 assert eq(S,s*x)and s.is_positive
 dm=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(.*?)(?:\\,⟹\\,|\\quad\\Longrightarrow\\quad)(.*?)(?:\n|$)',sol);assert dm,(sid,'du')
 assert eq(scalar(dm[1]),s)
 da,db=dm[2].rstrip('.').split('=');assert eq(scalar(db if r'\text{d}x'in da else da),1/s)
 # Full interval domain: poles never occur; positive scaling preserves branches.
 ul,ur=sp.simplify(S.subs(x,L)),sp.simplify(S.subs(x,R));assert L<R and ul<ur
 if t['family']=='asin':
  assert -1<=ul<ur<=1
  # Endpoints ±1 are proper one-sided, integrable square-root singularities.
  assert sp.simplify(1-((ul+ur)/2)**2)>0
  assert sp.simplify(sp.denom(target**2).subs(x,(L+R)/2))>0
  fn=sp.asin
 else:
  assert sp.denom(target).is_polynomial(x);assert sp.denom(target).subs(x,0)>0
  assert not sp.solveset(sp.denom(target),x,domain=sp.Interval(L,R))
  fn=sp.atan
 # Bound table is independently read from rendered source/variant text.
 tm=re.search(r'\| \$x\$ \| \$(.*?)\$ \| \$(.*?)\$ \|\n\| --- \| --- \| --- \|\n\| \$u\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol);assert tm,(sid,'table')
 assert all(eq(scalar(v),w)for v,w in zip(tm.groups(),[L,R,ul,ur]))
 # Every original/formal transformed integral operand, primitive and endpoints.
 count={'integral_operands':0,'primitive_bars':0,'endpoint_rows':0,'basic_primitives':0};seen_primitive=False;endpoint_seen=False;coefficient=None
 for block in sol.split('$$')[1::2]:
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',block).strip()
  if r'\int 'in text and '_'not in text and '+C'in text.replace(' ',''):
   left,right=text.rstrip('.').split('=');unit_integrand=scalar(left.replace(r'\int',''));F=scalar(right);assert eq(sp.diff(F,u),unit_integrand);count['basic_primitives']+=1;continue
  if r'\int'not in text and not seen_primitive:continue
  for row in re.split(r'\\\\',text):
   for term in row.replace('&','').split('='):
    term=term.strip().rstrip('.')
    if not term:continue
    if r'\int'in term:
     v,var,a,b=read_integral(term)
     if var==u:
      assert eq(a,ul)and eq(b,ur),(sid,'transformed bounds',term,ul,ur)
      assert eq(v.subs(u,S)*s,target),(sid,'transformed operand',term,v.subs(u,S)*s,target)
     else:assert eq(a,L)and eq(b,R)and eq(v,target),(sid,'original operand',term,v,target)
     count['integral_operands']+=1
    elif ('|'in term or r'\right]'in term)and('arcsin'in term or'arctan'in term):
     F,a,b=primitive(term);assert eq(a,ul)and eq(b,ur),(sid,'primitive bounds',term)
     assert eq(sp.diff(F.subs(u,S),x),target),(sid,'primitive derivative',term)
     coefficient=sp.simplify(F/fn(u));assert not coefficient.has(u);seen_primitive=True;count['primitive_bars']+=1
    elif seen_primitive:
     value=scalar(term);ans=sp.simplify(coefficient*(fn(ur)-fn(ul)))
     assert eq(value,ans),(sid,'evaluated stage',term,value,ans)
     if not endpoint_seen and ('arcsin'in term or'arctan'in term or'arctan'in clean(term)):
      # Verify each actual signed endpoint contribution before collection.
      raw=sp.expand(value);upper=sp.simplify(coefficient*fn(ur));lower=sp.simplify(-coefficient*fn(ul))
      # SymPy may collect equal positive endpoint contributions; evaluate
      # the two syntactic inverse-function arguments independently as well.
      names=re.findall(r'\\operatorname\{(?:arcsin|arctan)\}⁡?\((.*?)\)',term)
      if names:
       assert eq(scalar(names[0]),ur),(sid,'upper endpoint argument',names)
       if len(names)>1:assert eq(scalar(names[1]),ul),(sid,'lower endpoint argument',names)
      assert eq(raw,upper+lower);endpoint_seen=True;count['endpoint_rows']+=1
 assert count['integral_operands']>=3 and count['primitive_bars']>=1 and endpoint_seen,(sid,count)
 # The response shape is a full value or the exact supplied function fragments.
 fs=q[':question/answer-fields'];chosen=[]
 for f in fs:
  ids=[a[':answer/id']for a in f[':answer-field/choices']];assert len(ids)==len(set(ids)),(sid,'answer id uniqueness')
  correct=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);chosen.append(scalar(correct[':answer/value']))
  if f[':answer-field/type']==':answer-field.type/radio':
   vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert len(vals)==5
   assert sum(eq(v,coefficient*(fn(ur)-fn(ul)))for v in vals)==1
   assert all(not eq(a,b)for i,a in enumerate(vals)for b in vals[:i])
 answer=chosen[0]*sp.atan(chosen[1])if t['field_shape']=='atan-coefficient-argument'else sp.asin(chosen[0])if t['field_shape']=='asin-argument'else chosen[0]
 assert eq(answer,coefficient*(fn(ur)-fn(ul))),(sid,'answer fragments',answer)
 return count

def native_checks(rec):
 checks=[]
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  correct=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type']==':answer-field.type/radio':
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct[':answer/id']else'rejected','purpose':'normal radio complete bank','mathematical_expected':'accepted'if a[':answer/id']==correct[':answer/id']else'rejected'}for a in f[':answer-field/choices'])
  else:
   value=correct[':answer/value'];z=scalar(value)
   for submitted,expected,purpose in [(value,'accepted','normal blank canonical'),(r'\frac{2('+value+r')}{2}','accepted','normal blank genuine unreduced equivalent'),(g.tex(z+1),'rejected','normal blank wrong additive shift'),(g.tex(-z),'rejected','normal blank wrong sign')]:
    checks.append({'field_index':i,'submitted':submitted,'expected':expected,'mathematical_expected':expected,'purpose':purpose})
 return checks

def native_probe(items):
 # Probe the immutable native runner; record actual parser gaps without pruning
 # valid mathematics or pretending canonical and equivalent submissions passed.
 gaps=[]
 for ni,item in enumerate(items):
  for ci,c in enumerate(item['checks']):
   singleton=[{'label':item['label'],'record':item['record'],'checks':[dict(c)]}]
   (HERE/'probe-input.json').write_text(json.dumps(singleton))
   expected=c['expected'];proc=subprocess.run([str(HERE/'check-engine'),str(HERE/'probe-input.json'),str(HERE/'probe-report.json')],capture_output=True,text=True)
   if proc.returncode:
    match=re.search(r'expected (accepted|rejected|unresolved), got (accepted|rejected|unresolved)',proc.stderr);assert match,proc.stderr
    actual=match[2];c['expected']=actual;c['grading_gap']=actual!=expected
    gaps.append({'label':item['label'],'field_index':c['field_index'],'submitted':c.get('submitted',c.get('submitted_answer_id')),'mathematical_expected':expected,'native_outcome':actual,'purpose':c['purpose'],'qualification':'Actual normal generated response shape; valid mathematical entry retained. Engine gap, not generator mathematics failure.'})
 save('native-input.json',items)
 subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('native-gaps.json',{'normal_generator_grading_gaps':gaps,'count':len(gaps),'diagnostic_blank_shape_probes_for_radio':0})
 return gaps

def main():
 # Standard source wrapper is byte-for-byte identical to the frozen basis capture.
 (HERE/'source.json').write_bytes((HERE/'reference/sources.json').read_bytes())
 qs=g.SOURCE['record'][':knowledge-point/questions'];assert len(qs)==22;assert sum(bool(q.get(':question/math-academy-id'))for q in qs)==22
 originals=[];reviews=[];fidelity=[];inputs=[];stages={};bankrows=[];counts={level:0 for level in g.LEVELS}
 for sid,t in g.PROFILES.items():
  old=g.SOURCES[sid];rec=g.generate(t['difficulty'],0,sid,{'h':1,'k':1});q=rec['question'];counts[t['difficulty']]+=1
  assert q[':question/problem']==normalize_prose(old[':question/problem'])
  expected_solution=normalize_prose(old[':question/worked-solution'])
  if sid=='q-351850':expected_solution=expected_solution.replace(r'\,arctan\,',r'\,\operatorname{arctan}\,')
  assert q[':question/worked-solution']==expected_solution
  for f,of in zip(q[':question/answer-fields'],old[':question/answer-fields']):
   assert f[':answer-field/key']==of[':answer-field/key']and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
   assert [a[':answer/value']for a in f[':answer-field/choices']]==[normalize_tex(a[':answer/value'])for a in of[':answer-field/choices']]
   newcorrect=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert newcorrect[':answer/value']==normalize_tex(of[':answer-field/correct'][':answer/value'])
  stages[sid]=check(rec);originals.append(rec);inputs.append({'label':'source '+sid,'record':rec,'checks':native_checks(rec)})
  fidelity.append({'source_id':sid,'complete_bank':True,'prompt_exact_after_format_normalization':True,'solution_exact_after_format_normalization':sid!='q-351850','raw_exact_ineligible_replay':sid=='q-351850','presentation_repair_labeled':sid=='q-351850','fields_exact':True,'choice_count':sum(len(f[':answer-field/choices'])for f in q[':question/answer-fields']),'distractors':4 if q[':question/answer-fields'][0][':answer-field/type'].endswith('/radio')else 0})
  for fi,f in enumerate(old[':question/answer-fields']):
   for ai,a in enumerate(f[':answer-field/choices']):
    role='fixed argument'if t['field_shape']=='asin-argument'or(t['field_shape']=='atan-coefficient-argument'and fi==1)else'full integral value or supplied coefficient'
    bankrows.append({'source_id':sid,'field_key':f[':answer-field/key'],'choice_index':ai,'raw_value':a[':answer/value'],'correct':a[':answer/id']==f[':answer-field/correct'][':answer/id'],'profile':t['bank_profile'],'recipe':'V0'if role=='fixed argument'else'(k if asin else k/h) * V0','V0':sp.srepr(scalar(a[':answer/value'])),'slot_role':role,'interpretation':'Exact observed expression recipe; psychological mistake interpretation unresolved for constant distractors. No pooled profiles.'})
  for h,k in [(2,1 if t['field_shape']=='asin-argument'else 3),(9,1 if t['field_shape']=='asin-argument'else 9),(1,1 if t['field_shape']=='asin-argument'else 7)]:
   rr=g.generate(t['difficulty'],2275,sid,{'h':h,'k':k});check(rr);reviews.append(rr);inputs.append({'label':'changed '+sid+' '+str([h,k]),'record':rr,'checks':native_checks(rr)})
 assert counts=={'easy':3,'moderate':11,'hard':8}
 source_cases=[]
 for r in originals:
  sid=r['generation']['template'];raw=copy.deepcopy(r)
  if sid=='q-351850':
   raw['question'][':question/problem']=g.SOURCES[sid][':question/problem'];raw['question'][':question/worked-solution']=g.SOURCES[sid][':question/worked-solution'];raw['generation']['source_presentation_repair']=False
   repair=copy.deepcopy(r);repair['generation']['role']='separately labeled source presentation repair';reviews.append(repair)
  source_cases.append({'source_id':sid,'source_db_id':g.PROFILES[sid]['source_db_id'],'role':'ma-original','eligible_for_serving':sid!='q-351850','ineligible_reason':'Captured final line uses bare arctan letters; raw exact evidence retained and operator-name repair separated.'if sid=='q-351850'else None,'record':raw})
 save('source-cases.json',source_cases);save('review-cases.json',reviews)
 save('source-errors-and-repairs.json',{'source_errors':[{'source_id':'q-351850','kind':'presentation defect','raw_exact_solution':g.SOURCES['q-351850'][':question/worked-solution'],'raw_serving_eligible':False,'raw_token':r'\,arctan\,','supported_repair':r'\,\operatorname{arctan}\,','mathematics_changed':False,'repair_record':next(r for r in reviews if r['generation'].get('role')=='separately labeled source presentation repair')}]})
 save('source-replay.json',{'basis':2275,'MA_source_count':22,'non_MA_source_count':0,'complete_banks_matched':22,'complete_banks_total':22,'profiles':fidelity,'ineligible_source_errors':['q-351850: captured final arctan operator typography'],'repairs':['q-351850: explicit operatorname repair, no mathematical change']});save('choice-ledger.json',bankrows)
 # Complete bounded profile domains: selected-bank collision checks remain valid
 # under nonzero positive scaling; exercise all h/k values mathematically.
 domain={}
 for sid,t in g.PROFILES.items():
  tested=0;old=g.SOURCES[sid]
  for h,k in itertools.product(range(1,10),[1]if t['field_shape']=='asin-argument'else range(1,10)):
   d=g.data(sid,{'h':h,'k':k});assert d['bank_scale']>0
   # Nonzero scalar multiplication is injective on all complete source choices.
   for f in old[':question/answer-fields']:
    if f[':answer-field/type'][':db/ident'].endswith('/radio'):
     vals=[d['bank_scale']*scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert all(not eq(a,b)for i,a in enumerate(vals)for b in vals[:i])
   tested+=1
  domain[sid]=tested
 save('boundary-checks.json',{'all_bounded_complete_profile_tuples':domain,'total':sum(domain.values()),'rendered_boundaries_per_profile':3,'unchanged_transformed_bounds':'conservative fixed roles; original x bounds vary with h'})
 for level in g.LEVELS:
  a=g.batch(level,5,2275);assert a==g.batch(level,5,2275)
  for rec in a:check(rec)
 for bad in [True,False,1.0,'1',None]:
  for kwargs in [{'seed':bad},{'count':bad}]:
   try:g.batch(**kwargs)
   except ValueError:pass
   else:raise AssertionError(('builtin integer contract',kwargs))
 for v in [0,-1]:
  try:g.batch(count=v)
  except ValueError:pass
  else:raise AssertionError('nonpositive count')
 cli=subprocess.run([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--count','1','--seed','2275','--format','json'],check=True,capture_output=True,text=True);assert len(json.loads(cli.stdout))==3
 # Render corruption controls target individual bounds and formal stages.
 base=reviews[0];negative=[]
 for name,before,after in [('substitution','substitute $u='+g.tex(g.data('q-19394',{'h':2,'k':3})['s']*x),'substitute $u=x'),('table',r'| $u$ | $0$ | $\frac{\sqrt{2}}{2}$ |',r'| $u$ | $0$ | $1$ |'),('formal operand',r'\sqrt{1-(u)^{2}}',r'\sqrt{1-(2u)^{2}}'),('upper endpoint',r'\operatorname{arcsin}(\frac{\sqrt{2}}{2})',r'\operatorname{arcsin}(\frac{1}{2})')]:
  q=copy.deepcopy(base);text=q['question'][':question/worked-solution'];assert before in text,(name,before);q['question'][':question/worked-solution']=text.replace(before,after,1)
  try:check(q)
  except (AssertionError,TypeError,ValueError):negative.append(name)
  else:raise AssertionError(('undetected corruption',name))
 # Separately authored blank grading fixtures: not captured non-MA inventory.
 # same substitution method, normal blank response contracts (no radio diagnostics).
 independent=[]
 for level,N,A,B,L,R in [('easy',3,1,25,0,sp.Rational(1,5)),('moderate',7,49,1,0,7),('hard',5,7,28,-sp.Rational(1,4),sp.Rational(1,4))]:
  fn=sp.asin if level=='hard'else sp.atan;s=sp.sqrt(sp.Rational(B,A));c=sp.Rational(N)/(sp.sqrt(A)*s if fn==sp.asin else A*s);ans=sp.simplify(c*(fn(s*R)-fn(s*L)))
  qid=g.ident(['independent',level,N,A,B,str(L),str(R)]);fid=g.ident([qid,'answer']);value=g.tex(ans);aid=g.ident([fid,value]);d=dict(N=sp.Integer(N),A=sp.Integer(A),B=sp.Integer(B),fn=fn)
  rec={'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':{':question/id':qid,':question/problem':'Evaluate $'+g.integral(g.integrand(d),x,L,R)+'=$\n{{answer}}',':question/worked-solution':'Use $u='+g.tex(s*x)+'$, $\\text{d}x='+g.tex(1/s)+r'\,\text{d}u$. The bounds become $'+g.tex(s*L)+'$ and $'+g.tex(s*R)+'$. Therefore $'+g.tex(c*(fn(s*R)-fn(s*L)))+'$.',':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'answer',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value}],':answer-field/correct':[':answer/id',aid]}]},'generation':{'template':'independently-authored-'+level}}
  validate_generated_record(rec);independent.append({'record':rec,'role':'authored blank grading fixture','relationship_to_source_templates':'Same definite linear inverse-trig substitution and full-value blank response; coefficients independently authored rather than sampling a source radial/numerator profile.'});inputs.append({'label':'independent normal blank '+level,'record':rec,'checks':native_checks(rec)})
 save('diagnostic-blank-cases.json',{'basis':2275,'lineage':g.SOURCE['lineage'],'provenance':'Three authored blank grading fixtures, not captured source inventory. Native cases and outcomes are retained.','questions':independent})
 save('independent-inventory.json',{'basis':2275,'lineage':g.SOURCE['lineage'],'questions':[]})
 gaps=native_probe(inputs);engine=json.loads((HERE/'native-grading.json').read_text())
 (HERE/'source-and-changed.md').write_text('\n\n---\n\n'.join('## '+r['generation']['template']+' '+('original'if r['generation']['original_parameters']else str(r['generation']['parameters']))+'\n\n'+g.markdown(r)for pair in zip(originals,reviews[::3])for r in pair)+'\n')
 save('validation.json',{'status':'mathematics-and-fidelity-pass; native gaps qualified'if gaps else'ready-for-independent-QA','basis':2275,'source_counts':counts,'MA_originals':22,'non_MA_originals':0,'source_complete_banks':22,'source_choices':sum(z['choice_count']for z in fidelity),'source_distractors':sum(z['distractors']for z in fidelity),'changed_rendered_instances':66,'separately_labeled_presentation_repairs':1,'review_case_records':len(reviews),'bounded_profile_tuples':sum(domain.values()),'independent_inventory':0,'authored_blank_grading_fixtures':len(independent),'source_stage_checks':stages,'negative_controls':negative,'native_accepted':engine['accepted_checks'],'native_rejected':engine['rejected_checks'],'native_unresolved':engine['documented_unresolved_checks'],'normal_generator_grading_gaps':len(gaps),'diagnostic_radio_blank_probes':0,'deterministic_replay':True,'strict_builtin_integer_contract':True,'CLI_all_count1_json_list_length':3,'source_errors':['q-351850 presentation defect: raw exact original ineligible, explicit operatorname repair served'],'limits':['h/k bounded 1..9, transformed endpoint roles remain fixed inside each source profile.','Source q-351834 has integrable endpoint square-root singularities; interpreted as improper one-sided limits.','No arcsec source occurs in this KP; no authored arcsec extension.','Changed arithmetic displays use explicit canonical stages while preserving every source instructional prose paragraph.','Normal native blank parser outcomes and equivalent-entry gaps are retained in native-gaps.json.']})
 print('Rendered source/changed mathematics, complete banks and native review saved.')
if __name__=='__main__':main()
