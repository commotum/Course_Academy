"""Parse rendered equations, check every solution line, replay sources and grade."""
import copy,hashlib,importlib.util,json,re,subprocess,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2,default=str)+'\n')
def expr(text):
 text=re.sub(r'\{\{(.*?)\}_\{⏟\}\}_\{[ab]\}',r'\1',text)
 text=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',text.strip().rstrip('.'))
 text=re.sub(r'([xyzuvwpqrkmn])(?=[xyzuvwpqrkmn])',r'\1*',text)
 return parse_expr(text,local_dict={c:sp.Symbol(c) for c in 'xyzuvwpqrkmn'},transformations=standard_transformations+(implicit_multiplication_application,))
def parse(problem):
 eq=re.search(r'\$\$\s*(.*?)\s*\$\$',problem,re.S)
 if eq: eq=eq[1]
 else:eq=re.search(r'\$([^$]*=[^$]*)\$',problem)[1]
 match=re.fullmatch(r'(-?\d*)([pqrkmn])([xyzuvw])([+-]\d+)?=(-?\d*)([xyzuvw])([+-]\d+)?',re.sub(r'\s+','',eq));assert match,eq
 a,k,x,b,c,y,d=match.groups();assert x==y
 return {'variable':x,'parameter':k,'a':int(a) if a not in ('','-') else (-1 if a=='-' else 1),'b':int(b or 0),'c':int(c) if c not in ('','-') else (-1 if c=='-' else 1),'d':int(d or 0)}
def independent(rec):
 q=rec['question'];m=rec['generation'];p=parse(q[':question/problem']);assert p==m['parameters'];assert rec['knowledge_point']['db_id']==g.KP_ID
 level=q[':question/difficulty'].split('/')[-1];assert rec==g.generate(level,m['seed'],m['template'],p,m['bank_profile'])
 x,k=sp.Symbol(p['variable']),sp.Symbol(p['parameter']);eq=re.search(r'\$\$\n(.*?)\n\$\$',q[':question/problem'],re.S)[1];left,right=map(expr,eq.split('='));diff=sp.expand(left-right);roots=sp.solve(diff.coeff(x),k);assert len(roots)==1
 root=roots[0];constant=diff.subs(x,0);assert constant!=0
 assert sp.solveset(sp.Eq(left.subs(k,root),right),x,domain=sp.S.Reals)==sp.S.EmptySet
 assert sp.solveset(sp.Eq(left.subs(k,root+1),right),x,domain=sp.S.Reals)!=sp.S.EmptySet
 f=q[':question/answer-fields'][0];a=f[':answer-field/choices'];values=[expr(v[':answer/value']) for v in a];assert len(set(values))==len(a);assert values[0]==root
 assert f[':answer-field/correct']==[':answer/id',a[0][':answer/id']]
 assert len(a)==(5 if level=='easy' else 1);assert f[':answer-field/type']==':answer-field.type/'+('radio' if level=='easy' else 'blank')
 assert q[':question/problem'].count('{{field-1}}')==(0 if level=='easy' else 1)
 displays=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
 for display in displays[:-1]:
  for line in display.split(r'\\'):
   l,r=map(expr,line.replace('&','').split('='));assert sp.expand(l-r-diff)==0,line
 for line in displays[-1].split(r'\\'):
  l,r=map(expr,line.replace('&','').split('='));assert sp.solve(l-r,k)==roots,line
 for display in re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S):
  if '\\begin' in display or display in ('ax=b',) or '=' not in display:continue
  l,r=map(expr,display.split('='));delta=sp.expand(l-r)
  if x in delta.free_symbols:assert delta==diff,display
  elif k in delta.free_symbols:assert sp.solve(delta,k)==roots,display
 for text in (q[':question/problem'],q[':question/worked-solution']):assert text.count('$')%2==0 and text.count('{')==text.count('}')
 ids=[q[':question/id'],f[':answer-field/id']]+[z[':answer/id'] for z in a];assert len(set(ids))==len(ids)
 for v in ids:uuid.UUID(v)
def checks(rec):
 f=rec['question'][':question/answer-fields'][0];a=f[':answer-field/choices'];root=expr(a[0][':answer/value'])
 if f[':answer-field/type'].endswith('/radio'):
  return [{'field_index':0,'submitted_answer_id':v[':answer/id'],'expected':'accepted' if i==0 else 'rejected','purpose':'Select each source-profile option using actual radio grading'} for i,v in enumerate(a)]
 return [{'field_index':0,'submitted':v,'expected':expected,'purpose':'Equivalent rational and incorrect submissions through actual blank grader'} for expected,entries in [('accepted',[a[0][':answer/value'],str(root),str(root)+'+0',r'\frac{'+str(2*root.p)+'}{'+str(2*root.q)+'}']),('rejected',[str(root+1),str(root-1),'0'])] for v in entries]
def main():
 source=json.loads((HERE/'source.json').read_text());cases=[];excluded=[];records=[];reviews=[]
 for q in source['record'][':knowledge-point/questions']:
  mid=q[':question/math-academy-id'];p=parse(q[':question/problem']);fields=q[':question/answer-fields']
  if ':question/difficulty' not in q or ':question/worked-solution' not in q or ':answer-field/correct' not in fields[0]:excluded.append({'source':mid,'reason':'Unrated; missing correct designation and/or solution/bank. Preserve unchanged; excluded.'});continue
  level=q[':question/difficulty'][':db/ident'].split('/')[-1];template='right-constant' if level=='easy' else 'both-constants-ax-layout' if mid=='q-288678' else 'both-constants'
  rec=g.generate(level,parameters=p,template=template);independent(rec);n=rec['question'];f=n[':question/answer-fields'][0];old=fields[0]
  assert n[':question/problem']==q[':question/problem'],(mid,'prompt')
  assert n[':question/worked-solution']==q[':question/worked-solution'],(mid,'solution',n[':question/worked-solution'])
  assert old[':answer-field/type'][':db/ident']==f[':answer-field/type'] and old[':answer-field/key']==f[':answer-field/key']
  original=[expr(a[':answer/value']) for a in old[':answer-field/choices']];new=[expr(a[':answer/value']) for a in f[':answer-field/choices']];assert sorted(original)==sorted(new)
  assert expr(old[':answer-field/correct'][':answer/value'])==new[0]
  cases.append({'source_id':mid,'difficulty':level,'template':template,'parameters':p,'bank_profile':rec['generation']['bank_profile'],'matched_values':len(new),'total_values':len(original),'complete_bank_matched':True,'exact_prompt':True,'exact_solution':True})
  records.append(rec);reviews.append('## Source '+mid+' — exact replay\n\n'+g.markdown(rec))
 for level in g.SUPPORTED_LEVELS:
  for seed in range(60):
   rec=g.generate(level,seed);independent(rec);records.append(rec)
  rows=g.batch(level,20,991);assert len({r['generation']['parameter_fingerprint'] for r in rows})==20
  for rec in rows:independent(rec)
  reviews.append('## '+level+' variant\n\n'+g.markdown(rows[0]))
 boundaries=[]
 for a in (-9,-2,2,9):
  for c in (-9,-1,1,9):
   for b in (-9,9):
    for d in (-9,0,9):
     if b==d:continue
     r=g.generate('moderate',parameters={'variable':'x','parameter':'p','a':a,'c':c,'b':b,'d':d});independent(r);boundaries.append(r)
 records+=boundaries
 ref=records[0];p=ref['generation']['parameters'];changed=dict(p,variable='w',parameter='k',d=9);assert g.fingerprint(p)==g.fingerprint(changed)
 assert g.generate('easy',1,parameters=p)['question']==g.generate('easy',99,parameters=p)['question']
 negative=0
 for level,p in [('hard',None),('moderate',dict(p,b=1,d=1)),('easy',dict(p,a=0)),('easy',dict(p,c=2))]:
  try:g.generate(level,parameters=p)
  except ValueError:negative+=1
  else:raise AssertionError('invalid accepted')
 for slot in ('answer','solution'):
  bad=copy.deepcopy(ref)
  if slot=='answer':bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='0'
  else:bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('p & =','p & =1+')
  try:independent(bad)
  except AssertionError:negative+=1
  else:raise AssertionError('corruption accepted')
 save('source-cases.json',cases);save('excluded-source.json',excluded);save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)])
 binary=ROOT/'generate/runs/current/check-engine';r=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True);(HERE/'engine.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
 engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 (HERE/'review.md').write_text('\n\n---\n\n'.join(reviews)+'\n');save('review.json',{'replays':records[:len(cases)],'variants':[g.generate(l,991) for l in g.SUPPORTED_LEVELS]})
 save('validation.json',{'status':'pass','source_basis':source['basis'],'lineage':source['lineage'],'supported_levels':list(g.SUPPORTED_LEVELS),'source_coverage':{'complete_source_questions':len(cases),'complete_banks_matched':len(cases),'matched_values':sum(c['matched_values'] for c in cases),'total_values':sum(c['total_values'] for c in cases),'missing_options':[],'extra_options':[],'excluded_incomplete':excluded},'fidelity':'Exact prompts, fixed solutions, fields and complete banks for every complete source. Source q-288678 uses ax in explanatory prose; retained as a layout branch. Easy distractor interpretation unresolved; observed recipes recorded explicitly.','mathematics':{'independent_display_checks':len(records),'boundaries':len(boundaries),'negative_controls':negative},'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',binary)}})
 print(r.stdout)
if __name__=='__main__':main()
