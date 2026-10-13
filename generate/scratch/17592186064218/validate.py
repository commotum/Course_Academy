"""Independent rendered-math, whole-bank, solution-row and learner-grader validation."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('inverse_sine_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
X=sp.Symbol('x',real=True);U=sp.Symbol('u',real=True);C=sp.Symbol('C',real=True)
ENGINE=HERE/'check-current-engine'
def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def latex(s):
 s=s.replace('\u2061','').replace('\u00a0',' ').replace(r'\,','').replace(r'\left','').replace(r'\right','')
 s=re.sub(r'\\(?:operatorname|text|textrm)\{(arcsec|arcsin|arctan|arccos)\}',lambda m:{'arcsec':'asec','arcsin':'asin','arctan':'atan','arccos':'acos'}[m[1]],s)
 def group(s,start):
  assert s[start]=='{',s
  depth=1;i=start+1
  while depth:
   depth+=(s[i]=='{')-(s[i]=='}');i+=1
  return s[start+1:i-1],i
 def convert(s):
  out='';i=0
  while i<len(s):
   if s.startswith(r'\frac',i) or s.startswith(r'\dfrac',i):
    i+=6 if s.startswith(r'\dfrac',i) else 5;a,i=group(s,i);b,i=group(s,i);out+='(('+convert(a)+')/('+convert(b)+'))'
   elif s.startswith(r'\sqrt',i):
    i+=5;a,i=group(s,i);out+='sqrt('+convert(a)+')'
   elif s[i]=='|':
    j=s.index('|',i+1);out+='Abs('+convert(s[i+1:j])+')';i=j+1
   else:out+=s[i];i+=1
  return out
 s=convert(s).replace('{','(').replace('}',')').replace('^','**')
 s=re.sub(r'(asin|acos|atan|asec)([xu])',r'\1(\2)',s)
 return parse_expr(s,local_dict={'x':X,'u':U,'C':C,'asec':sp.asec,'asin':sp.asin,'atan':sp.atan,'acos':sp.acos,'Abs':sp.Abs,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))

def clean(s):
 return s.replace(r'\frac{\text{d}u}',r'\frac{1}').replace(r'\frac{\text{d}x}',r'\frac{1}').replace(r'\,','').replace(r'\cdot','*').replace(r'\text{d}x','').replace(r'\textrm{d}x','').replace(r'\text{d}u','').replace(r'\textrm{d}u','').strip().rstrip('.')
def integrand(q):
 s=q[':question/problem'].split(r'\int',1)[1].split('$')[0]
 s=s.split('=')[0].rstrip('.');return sp.simplify(latex(clean(s)))
def fingerprint(q):
 e=integrand(q);z=sp.expand(sp.simplify(1/e**2));a=z.subs(X,0);assert a>0 and sp.Poly(z,X).degree()==2
 return g.digest(sp.sstr(sp.simplify(1/sp.sqrt(a)))+'|'+sp.sstr(sp.simplify(-z.coeff(X,2)/a)))
def check_question(q,solution=True):
 e=integrand(q);f=q[':question/answer-fields'][0]
 assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio'and f[':answer-field/key']=='selection'
 values=[latex(a[':answer/value'])for a in f[':answer-field/choices']];assert len(values)==5
 assert len({a[':answer/id']for a in f[':answer-field/choices']})==5
 correct=f[':answer-field/correct'][1];right=next(i for i,a in enumerate(f[':answer-field/choices'])if a[':answer/id']==correct)
 assert sp.simplify(sp.diff(values[right],X)-e)==0,(q[':question/problem'],values[right],e)
 # Numeric witnesses on the real connected neighborhood of zero establish that
 # each wrong bank member differs from the correct family and all peers.
 derivatives=[sp.diff(z,X)for z in values]
 for i,z in enumerate(derivatives):
  for j,w in enumerate(derivatives[:i]):
   witnesses=[]
   for sample in (sp.Rational(1,97),sp.Rational(-1,89),sp.Rational(1,79)):
    try:witnesses.append(complex(sp.N((z-w).subs(X,sample),20)))
    except (TypeError,ValueError):pass
   assert any(abs(a)>1e-10 for a in witnesses),(i,j,'equivalent/unresolved bank')
 if solution:solution_check(q,e)
 return right

def solution_check(q,e=None):
 e=e if e is not None else integrand(q)
 # Extract the actual u-substitution; numerator and square coefficient alone
 # cannot establish that the rendered calculation is right.
 sol=q[':question/worked-solution'];m=re.search(r"substitute \$u=(.*?)\.\$",sol);assert m,sol
 substitution=latex(m[1]);slope=sp.diff(substitution,X);assert not slope.has(X)and slope>0
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);rows_checked=0
 for block in blocks:
  if r'\begin{aligned}'not in block:continue
  s=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  parts=s.split('& =')
  for part in parts:
   part=part.replace(r'\\','').strip().rstrip('.')
   if not part:continue
   if r'\int'in part:
    variable=U if r'\text{d}u'in part else X
    expression=latex(clean(part.replace(r'\int','')))
    if variable==U:expression=expression.subs(U,substitution)*slope
    assert sp.simplify(expression-e)==0,('solution integral',part,e,expression)
   else:
    expression=latex(part).subs(U,substitution)
    assert sp.simplify(sp.diff(expression,X)-e)==0,('solution primitive',part)
   rows_checked+=1
 assert rows_checked>=6
 # du/dx and dx/du display must both agree with the parsed substitution.
 diff=next(b for b in blocks if r'\frac{\text{d}u}'in b)
 left,right=diff.split('⟹');displayed=latex(clean(left.split('=')[1]));assert displayed==slope
 inverse=latex(clean(right.split('=')[1]));assert sp.simplify(inverse-1/slope)==0
 return rows_checked

def check(rec):
 q=rec['question'];meta=rec['generation'];assert not meta['evidence_only']and meta['eligible_for_learning']
 assert rec==g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],meta['profile'],meta['parameters'])
 check_question(q)
 assert fingerprint(q)==meta['mathematical_fingerprint']
 for text in (q[':question/problem'],q[':question/worked-solution']):
  assert text.count('$')%2==0 and text.count('{')==text.count('}')and '!['not in text
 assert ':question/math-academy-id'not in q
 return rec

def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'Every source-bank member graded by actual radio learner grader'}for a in f[':answer-field/choices']]}

def normalized(q):
 n=copy.deepcopy(q);n[':question/difficulty']=str(n[':question/difficulty'][':db/ident'])
 for f in n[':question/answer-fields']:
  f[':answer-field/type']=str(f[':answer-field/type'][':db/ident']);f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
  for a in f[':answer-field/choices']:a[':answer/id']=str(a[':answer/id'])
 return n

def main():
 replays=[];inputs=[];review=[];rows=[];counts={l:set()for l in g.SUPPORTED_LEVELS}
 for sid,(level,template,base,_)in g.PROFILES.items():
  print('Validating',sid,flush=True);old=g.ORIGINALS[sid];raw=g.generate(level,0,sid,{'t':base},replay=True);q=raw['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem']and q[':question/worked-solution']==old[':question/worked-solution']
  assert [a[':answer/value']for a in f[':answer-field/choices']]==[a[':answer/value']for a in of[':answer-field/choices']]
  assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  # Raw q-49535 has a source solution error; the unmodified evidence is retained.
  if sid!='q-2506':check_question(normalized(old),solution=sid!='q-49535')
  replays.append({'source':sid,'profile':sid,'template':template,'matched_distractors':4,'total_distractors':4,'matched_complete_bank':True,'correct_designation_matched':True,'exact_prompt':True,'exact_solution':True,'evidence_only':sid=='q-2506','source_error':sid=='q-49535'})
  if sid=='q-2506':continue
  first=None
  for params in g.candidates(sid):
   rec=check(g.generate(level,7,sid,params));assert rec['question']==g.generate(level,999,sid,params)['question']
   rows.append(rec);counts[level].add(fingerprint(rec['question']));inputs.append(native(sid+' '+str(params),rec))
   if params['t']!=base and first is None:first=rec
  review.append('## '+sid+'\n\n### Original\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\n### Exact bank replay\n\n'+g.markdown(raw)+'\n\n### Validated variant\n\n'+g.markdown(first or g.generate(level,7,sid,{'t':base})))
 for level in ('hard','unclassified'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('unsupported band accepted')
 for sid,values in g.PROFILES.items():
  for invalid in (-1,0,1,13,True,'2'):
   try:g.generate(values[0],0,sid,{'t':invalid})
   except ValueError:pass
   else:raise AssertionError('invalid parameter accepted')
 try:g.generate('moderate',0,'q-49547',{'t':9})
 except ValueError:pass
 else:raise AssertionError('equivalent bank accepted')
 save('native-input.json',inputs);subprocess.run([str(ENGINE),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('source-replay.json',{'passed':True,'complete_banks_matched':14,'complete_banks_total':14,'distractors_matched':56,'distractors_total':56,'supported_source_banks':13,'excluded_ambiguous_banks':['q-2506'],'profiles':replays,'missing_extra_choices':[],'mathematical_equivalence':'Exact identical LaTeX values at original parameters for every bank; symbolic correct primitives and distinct derivative witnesses for all supported profiles. Ambiguous arcsec-squared source is exact evidence-only replay, excluded from practice.'})
 save('capabilities.json',{'supported_levels':list(g.SUPPORTED_LEVELS),'unsupported_levels':['hard'],'reason':'All 14 sources at basis '+str(g.SOURCE['basis'])+' use linear u substitution with normalized constant or quadratic radicand; none establish a hard template. Larger coefficients alone do not establish hard difficulty. Shifted/nonlinear substitutions and additional algebra are outside this validated bounded package; reopen on new evidence.','distinct_bounded_tasks':{l:len(v)for l,v in counts.items()},'exceptions':[{'level':'hard','supported':False,'shortage':5,'reason':'No validated hard template; hard remains explicit and unfilled'},{'profile':'q-49535','bounded_variants':1,'reason':'Conflicting repeated numeric slots; only original parameters supported, corrected opening numerator, no new inventory from this finite profile'}, {'profile':'q-2506','reason':'Ambiguous arcsec superscript interpretation; exact replay only, no generated practice from this profile'}],'sampling_bounds':{p:list(g.domain(p))for p in g.PROFILES},'plots':'none'})
 save('previews.json',[r for l in g.SUPPORTED_LEVELS for r in g.batch(l,5,1948)])
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'source_basis':g.SOURCE['basis'],'exhaustive_instances':len(rows),'distinct_tasks':{l:len(v)for l,v in counts.items()},'source_fidelity':'14/14 exact evidence banks, 56/56 distractors; 13/13 supported banks. All source prose and solution layouts retained except documented numerator correction in generated q-49535.','correctness':'Independent displayed-integrand parsing; symbolic correct-answer differentiation; distinct derivative witnesses; every rendered integral/primitive stage; parsed substitution slope and reciprocal; deterministic replay; boundaries; malformed parameter rejection.','grading':'All five choices for each bounded eligible instance through course_academy_engine::learning::grade_field','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'capabilities.json',ENGINE)}})
 print('Validated',len(rows),'instances; distinct tasks:',{l:len(v)for l,v in counts.items()},flush=True)
if __name__=='__main__':main()
