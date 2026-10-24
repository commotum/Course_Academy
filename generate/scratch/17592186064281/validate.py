"""Independent parsing/calculus, complete source banks, fixed solution math and native grading."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=sp.Symbol('x',real=True);Y=sp.Symbol('y',real=True);U=sp.Symbol('u',real=True)
def expr(s):
 s=re.sub(r'\\d?frac\s+(\d)\s+(\d)',r'\\frac{\1}{\2}',s)
 s=s.strip().strip('$').replace('\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\pi','pi')
 s=re.sub(r'\\operatorname\{(sin|cos|tan|sec|cot|csc)\}',r'\1',s)
 s=re.sub(r'\{(sin|cos|tan|sec|cot|csc)\}',r'\1',s)
 s=re.sub(r'\\(sin|cos|tan|sec|cot|csc)',r'\1',s)
 s=re.sub(r'(sin|cos|tan|sec|cot|csc)\^\{2\}',r'\g<1>sq',s)
 def group(i):
  assert s[i]=='{',s
  j=i+1;depth=1
  while depth:
   depth+=(s[j]=='{')-(s[j]=='}');j+=1
  return s[i+1:j-1],j
 while r'\frac' in s or r'\dfrac' in s:
  m=re.search(r'\\d?frac',s);a,j=group(m.end());b,k=group(j);s=s[:m.start()]+'(('+str(expr(a))+')/('+str(expr(b))+'))'+s[k:]
 s=s.replace('{','(').replace('}',')').replace('^','**')
 # Captured macros concatenate a trig name and integer argument.
 s=re.sub(r'(sin|cos|tan|sec|cot|csc)(-?\d+)(?![\d.])',r'\1(\2)',s)
 local={'x':X,'y':Y,'u':U,'pi':sp.pi}
 for name in ['sin','cos','tan','sec','cot','csc']:
  local[name]=getattr(sp,name);local[name+'sq']=lambda z,fun=getattr(sp,name):fun(z)**2
 return parse_expr(s,local_dict=local,transformations=standard_transformations+(implicit_multiplication_application,))

def content(q):
 p=q[':question/problem'];math=re.findall(r'\$(.*?)\$',p,re.S)
 function=next(m for m in math if re.match(r'(y|f\(x\))\s*=',m))
 f=expr(function.split('=',1)[1].rstrip('.'))
 if 'slope' in p or 'equation of the tangent' in p:
  x0=re.search(r'(?:at .*?\$x\s*=\s*|where \$x=)(.*?)(?:[.$])',p)
  if x0:at=expr(x0[1])
  elif 'point' in p:
   # Source tangent point (1+pi,-A); parentheses normalized separately.
   point=next(m for m in math if ',' in m and '(' in m)
   point=point.replace(r'\left','').replace(r'\right','').strip().rstrip('.')
   at=expr(point.split(',')[0].lstrip('('));point_y=expr(point.split(',')[1].rstrip(')'))
   assert sp.simplify(f.subs(X,at)-point_y)==0
  else:raise ValueError('Cannot parse evaluation point: '+p)
  kind='tangent' if 'equation' in p else 'slope'
 else:at=None;kind='derivative'
 return f,at,kind

def fingerprint(q):
 f,at,kind=content(q)
 return json.dumps([kind,sp.srepr(sp.expand_trig(f)),sp.srepr(at) if at is not None else None],separators=(',',':'))

def bank_check(q):
 f,at,kind=content(q);expected=sp.diff(f,X)
 if at is not None:
  m=sp.simplify(expected.subs(X,at));expected=sp.simplify(m*(X-at)+f.subs(X,at)) if kind=='tangent' else m
 fields=q.get(':question/answer-fields',[]);assert len(fields)==1
 field=fields[0];values=[]
 for a in field[':answer-field/choices']:
  value=a[':answer/value'];values.append(expr(value.split('=',1)[1] if kind=='tangent' else value))
 hits=[i for i,z in enumerate(values) if sp.simplify((z-expected).rewrite(sp.cos))==0]
 assert len(hits)==1,('Incorrect or ambiguous bank',q[':question/problem'],hits)
 c=field[':answer-field/correct'];cid=str(c[':answer/id']) if isinstance(c,dict) else c[1]
 assert str(field[':answer-field/choices'][hits[0]][':answer/id'])==cid
 assert all(sp.simplify(sp.trigsimp(z-w))!=0 for i,z in enumerate(values) for w in values[:i])
 return expected

def solution_check(q):
 expected=bank_check(q);f,at,kind=content(q);s=q[':question/worked-solution']
 # Parse displayed u and compare its composition and derivative to problem.
 match=re.search(r'u\s*=\s*(.*?)(?:\.|\n|\\\])',s)
 assert match,(q[':question/problem'],'missing substitution')
 u=expr(match[1].strip().rstrip(','))
 if 'tan' in str(f):outer=sp.tan(U)
 elif 'cos' in str(f) and kind=='tangent':outer=sp.Integer(expr(q[':question/problem'].split('y=')[1].split(r'\operatorname')[0]))*sp.cos(U)
 elif 'cos' in str(f):outer=sp.cos(U)
 else:outer=sp.sin(U)
 target=f+6*X**3 if 'cubic' in s or 'h(x)' in s else f
 assert sp.simplify(outer.subs(U,u)-target)==0
 for prefix in [r'\frac{\text{d}u}{\text{d}x}=',r'\dfrac{\textrm d u}{\textrm d x} = ']:
  if prefix in s:
   printed=s.split(prefix,1)[1].split('\n',1)[0].rstrip('.')
   assert sp.simplify(expr(printed)-sp.diff(u,X))==0,('Incorrect printed inner derivative',printed)
   break
 else:raise AssertionError('Missing printed inner derivative')
 # Extract the last displayed expression in every derivation chain;
 # verify final derivative/evaluation/tangent mathematics from printed text.
 if kind=='derivative':
  if 'h(x)' in s:
   last=re.search(r'=([^=\n]+)\.\n\$\$',s[s.index('Hence,'):])[1]
  else:last=s.split('& =')[-1].split(r'\end{aligned}')[0].rstrip('.')
  assert sp.simplify((expr(last)-expected).rewrite(sp.cos))==0,last
 elif kind=='slope':
  if '\\bbox' in s:
   last=s.split('lightgray]{')[1].split('}')[0]
  elif str(q[':question/answer-fields'][0][':answer-field/type']).endswith('/radio'):
   last=s.split(' is $')[-1].split('$')[0].rstrip('.')
  else:last=s.split('=')[-1].split('\n$$')[0].strip().rstrip('.')
  assert sp.simplify(expr(last)-expected)==0,last
 else:
  last=s.split(' & =')[-1].split(r'\end{aligned}')[0].rstrip('.')
  assert sp.simplify(expr(last)-expected)==0,last
 return expected

def representation_check(q):
 # Equivalence alone cannot catch an unexplained identity between the final
 # solution line and the keyed choice. Read the displayed forms independently.
 if 'h(x)' not in q[':question/worked-solution']:return
 def notation(s):
  s=re.sub(r'\\operatorname\{(sin|cos)\}',r'\\\1',s)
  return re.sub(r'[\s{}\u2061.]','',s.replace(r'\left','').replace(r'\right',''))
 problem=notation(q[':question/problem']);solution=notation(q[':question/worked-solution'])
 inner=re.search(r'\\cos\(([^)]+)\)',problem)[1]
 field=q[':question/answer-fields'][0];correct=field[':answer-field/correct']
 cid=str(correct[':answer/id']) if isinstance(correct,dict) else correct[1]
 for answer in field[':answer-field/choices']:
  value=notation(answer[':answer/value'])
  assert re.findall(r'\\(?:sin|cos)\(([^)]+)\)',value)==[inner],('Unexplained trig argument rewrite',value,inner)
  if str(answer[':answer/id'])==cid:
   final=solution.split('Hence,',1)[1].split('=')[-1].split('$$')[0]
   assert value==final,('Keyed choice differs from final solution form',value,final)

def independent(r):
 q=r['question'];m=r['generation'];profile=m['profile'];t=m['parameters']['t'];level=q[':question/difficulty'].split('/')[-1]
 assert r==g.generate(level,m['seed'],profile,t)
 assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
 assert fingerprint(q)==m['parameter_fingerprint']
 solution_check(q)
 representation_check(q)
 assert q[':question/problem'].count('$')%2==0
 assert q[':question/worked-solution'].count('$')%2==0
 assert q[':question/problem'].count('{')==q[':question/problem'].count('}')
 assert q[':question/worked-solution'].count('{')==q[':question/worked-solution'].count('}')
 ids=[q[':question/id']]+[f[':answer-field/id'] for f in q[':question/answer-fields']]+[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
 assert len(ids)==len(set(ids)) and ':question/math-academy-id' not in q

def checks(r):
 f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every field-owned choice through application grader'} for a in f[':answer-field/choices']]
 ans=f[':answer-field/choices'][0][':answer/value'];equiv=str(expr(ans)).replace('**','^')
 wrong=str(expr(ans)+1).replace('**','^')
 return [{'field_index':0,'submitted':value,'expected':out,'purpose':why} for value,out,why in [(ans,'accepted','canonical math'),(equiv,'accepted','Equivalent SymPy notation'),('('+equiv+')+0','accepted','Equivalent expanded entry'),(wrong,'rejected','Incorrect answer offset by one')]]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 rows=[];replay=[];review=[]
 build=json.loads((H/'engine-build.json').read_text())
 assert all(sha(ROOT/p)==digest for p,digest in build['hashes'].items()),'Native grading build changed'
 original_grading=json.loads((H/'reference/source-grading-summary.json').read_text())
 assert {r['source_id'] for r in original_grading if not r['validated_for_inventory']}=={'q-310182'}
 for profile,v in g.PROFILES.items():
  print('Validating',profile,flush=True)
  original=g.ORIGINALS[profile];r=g.generate(v[0],0,profile,v[2]);independent(r)
  f=original[':question/answer-fields'][0];new=r['question'][':question/answer-fields'][0]
  old_vals=[expr(a[':answer/value'].split('=',1)[-1].strip('$')) for a in f[':answer-field/choices']]
  new_vals=[expr(a[':answer/value'].split('=',1)[-1]) for a in new[':answer-field/choices']]
  matches=[[i for i,z in enumerate(new_vals) if sp.simplify(sp.trigsimp(z-w))==0] for w in old_vals]
  assert all(len(m)==1 for m in matches) and len({m[0] for m in matches})==len(old_vals)
  assert old_vals[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])]==new_vals[next(i for i,a in enumerate(new[':answer-field/choices']) if a[':answer/id']==new[':answer-field/correct'][1])]
  assert r['question'][':question/problem'].removesuffix('\n\n{{selection}}')==original[':question/problem']
  assert r['question'][':question/worked-solution']==original[':question/worked-solution']
  tested=[]
  for t in v[3]:
   if g.eligible(profile,t):
    z=g.generate(v[0],71,profile,t);independent(z);rows.append(z);tested.append(t)
    assert z['question']==g.generate(v[0],892,profile,t)['question']
  replay.append({'source_id':profile,'template':v[1],'source_bank_options':len(old_vals),'matched_options':len(old_vals),'matched_distractors':max(0,len(old_vals)-1),'complete_bank_match':True,'correct_designation_match':True,'parameters_tested':tested,'invalid_rejected_parameters':[t for t in v[3] if t not in tested]})
  review.append('## '+profile+' source replay\n\n'+g.markdown(r)+'\n\n### New variant\n\n'+g.markdown(g.generate(v[0],71,profile,tested[-1])))
 (H/'review.md').write_text('\n\n'.join(review))
 engine=[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(rows)]
 (H/'engine-input.json').write_text(json.dumps(engine,indent=2))
 subprocess.run([str(H/'check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
 er=json.loads((H/'engine-report.json').read_text());assert er['documented_unresolved_checks']==0
 bounds={level:len({r['generation']['parameter_fingerprint'] for r in rows if r['question'][':question/difficulty'].endswith('/'+level)}) for level in g.SUPPORTED_LEVELS}
 caps={'source_basis':g.SOURCE['basis'],'supported_levels':list(g.SUPPORTED_LEVELS),'finite_distinct_task_domain':bounds,'unsupported_levels':['easy'],'exceptions':{'easy':'No rated easy source evidence at captured basis. Two legacy unrated radio questions lack keys, solutions and difficulty; preserved and excluded. Absence is not impossibility: reopen on rated or reviewed source evidence.','incomplete_templates':'q-31241, q-48508 and q-48636 have no fields. Their mathematical results are described in classification but no answer-shape extensions are generated.','lexical_math_source':'q-310182 preserves its delimited text bank; actual learner grader rejects an equivalent -4*pi response. The unchanged source is excluded from validated availability; new variants use supported mathematical blanks. See reference/source-grading-summary.json.', 'narrow_sampling':'Only one observed coefficient varies per supported family, finite ranges in script; no claims beyond these ranges. tan requires cos(u) != 0. Signed -2 linear slope and -6 cubic retained.'},'plots':'none; no source diagrams or required new assets','new_source_evidence_reopens_classification':True}
 (H/'capabilities.json').write_text(json.dumps(caps,indent=2))
 result={'status':'pass','source_basis':g.SOURCE['basis'],'exhaustive_instances':len(rows),'source_replay':replay,'complete_banks_matched':len(replay),'total_supported_banks':len(g.PROFILES),'matched_distractors':sum(r['matched_distractors'] for r in replay),'total_supported_distractors':12,'fidelity':'All supported source banks matched completely with correct designation; source prompt and fixed solution exact at source parameters; generated blanks use delimiter-free math; radio controls render separately. Unsupported source records unchanged.','correctness':'Independent rendered prompt parsing, symbolic differentiation, slope/point evaluation, tangent equation RHS equivalence, distinct incorrect banks, printed substitution and final solution checks; all bounded parameters enumerated.','representation':'Cosine-plus-cubic choices preserve the prompt inner argument; keyed choice matches the final worked-solution form without a parity identity.','grading':{k:er[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [H.with_suffix('.py'),Path(__file__),H/'source.json',H/'source.edn',H/'capabilities.json',H/'check-engine',H/'check-engine.rs',H/'replenish.py',H/'reference/source-grading-summary.json']}}
 (H/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps({'status':result['status'],'instances':len(rows),'grading':result['grading'],'bounds':bounds}))
if __name__=='__main__':main()
