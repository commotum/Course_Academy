"""Read rendered mathematics independently; replay banks and use real grader."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x')
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def math(text):
 text=text.strip().rstrip('.').replace('{)}',')').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\,','')
 text=text.replace(r'\operatorname{ln}', 'log').replace(r'\text{d}', 'd')
 def group(s,i):
  assert s[i]=='{',(s,i);depth=1;j=i+1
  while depth:
   if s[j]=='{':depth+=1
   elif s[j]=='}':depth-=1
   j+=1
  return s[i+1:j-1],j
 while r'\frac' in text or r'\dfrac' in text:
  m=re.search(r'\\d?frac\s*',text);i=m.end();a,j=group(text,i);b,k=group(text,j);text=text[:m.start()]+'(('+a+')/('+b+'))'+text[k:]
 text=re.sub(r'e\^\{([^{}]+)\}',r'exp(\1)',text)
 text=text.replace('{','(').replace('}',')').replace('^','**')
 assert '\\' not in text,text
 return parse_expr(text,local_dict={'x':x,'e':sp.E,'exp':sp.exp},transformations=standard_transformations+(implicit_multiplication_application,))
def supplied(q):
 prompt=q[':question/problem']
 m=re.search(r'y\s*=\s*([^$]+)\$',prompt)
 if m and m[1]=='f(x)':return None
 if m and m[1]!='k(x)':f=math(m[1])
 else:
  m=re.search(r'k\(x\)=([^$]+)\$',prompt)
  if not m:m=re.search(r'We have \$k\(x\)=([^$]+)\$',q[':question/worked-solution'])
  if not m:return None
  f=math(m[1])
 t=int(re.search(r'where \$x\s*=\s*(-?\d+)',prompt)[1])
 return f,t
def fingerprint(q):
 z=supplied(q)
 if z is None:return g.digest(['excluded-context',str(q.get(':question/id'))])
 f,t=z;return g.digest([str(sp.cancel(sp.diff(f,x))),t])
def correct_value(q):
 f=q[':question/answer-fields'][0];c=f[':answer-field/correct'];cid=c[1] if isinstance(c,list) else str(c[':answer/id'])
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if str(a[':answer/id'])==cid)
def check(rec):
 q=rec['question'];meta=rec['generation'];sid=meta['template'];p=meta['parameters'];level=q[':question/difficulty'].split('/')[-1]
 assert rec['knowledge_point']['db_id']==g.KP_ID and rec==g.generate(level,meta['seed'],sid,p)
 f,t=supplied(q);assert sp.simplify(f-g.expression(sid,p))==0 and t==p[-1]
 slope=sp.diff(f,x).subs(x,t);assert slope.is_Rational and slope.is_finite
 field=q[':question/answer-fields'][0];values=[math(a[':answer/value']) for a in field[':answer-field/choices']]
 assert len(values)==(5 if field[':answer-field/type'].endswith('/radio') else 1)
 assert len(set(values))==len(values) and math(correct_value(q))==slope
 sol=q[':question/worked-solution'].replace(r'^{\prime}',r'\prime');assert '{{' not in sol and '@@' not in sol and '@@' not in q[':question/problem']
 intro=re.search(r'(?:We have \$k|Let \$f)\(x\)=([^$]+)\$',sol);assert intro and sp.simplify(math(intro[1])-f)==0
 if sid=='q-167637':
  for z in re.findall(r'k\\prime\(x\)=([^$\n]+)',q[':question/problem'].replace(r'^{\prime}',r'\prime')+'\n'+sol):assert sp.simplify(math(z)-sp.diff(f,x))==0
 else:
  block=re.search(r'\\begin\{aligned\}f\\prime\(x\)(.*?)\\end\{aligned\}',sol,re.S)[1]
  stages=re.split(r' \\\\ & =',block)
  # Every derivative stage after the formal d/dx operation is independently read.
  if sid=='q-1853':
   rewritten=re.search(r'\\frac\{\\text\{d\}\}\{\\text\{d\}x\}\((.*)\)',stages[1])[1]
   assert sp.simplify(math(rewritten)-f)==0
   stages=stages[2:]
  else:stages=stages[1:]
  for stage in stages:assert sp.simplify(math(stage)-sp.diff(f,x))==0,(sid,stage)
 block=re.search(r'\\begin\{aligned\}[kf]\\prime\((-?\d+)\) & =(.*?)\\end\{aligned\}',sol,re.S)
 assert block and int(block[1])==t
 for stage in re.split(r' \\\\ & =',block[2]):assert sp.simplify(math(stage)-slope)==0,(sid,stage,slope)
 conclusion=sol.split('Therefore,')[-1];assert tex_final(slope) in conclusion
 assert fingerprint(q)==meta['mathematical_fingerprint']
 return rec
def tex_final(z):return g.tex(z)
def native(label,rec):
 f=rec['question'][':question/answer-fields'][0];ci=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ci else 'rejected','purpose':'actual radio selection'} for a in f[':answer-field/choices']]
 else:
  z=math(correct_value(rec['question']));equiv=[str(z),str(2*z.p)+'/'+str(2*z.q),g.tex(z)]
  checks=[{'submitted':a,'expected':'accepted','purpose':'exact and equivalent blank'} for a in dict.fromkeys(equiv)]
  checks +=[{'submitted':str(z+1),'expected':'rejected','purpose':'incorrect blank'},{'submitted':str(-z if z else 2),'expected':'rejected','purpose':'incorrect sign or zero'}]
 return {'label':label,'record':rec,'checks':checks}
def main():
 import sys
 sys.path.insert(0,str(ROOT/'scripts/question_capture'))
 from edn import loads
 native_source=loads((HERE/'reference/initial/source.edn').read_text())[0][0]
 source_fps=[fingerprint(q) for q in native_source[':knowledge-point/questions']+[native_source[':knowledge-point/canonical-example']]]
 assert len(source_fps)==11 and len(set(source_fps))==11
 save('native-source-validation.json',{'passed':True,'typed_edb_records_checked':11,'fingerprints':source_fps})
 raw=json.loads((HERE/'source.json').read_text());sources={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']};replay=[];inputs=[];review=[];total=0;coverage={}
 for sid,t in g.PROFILES.items():
  rec=check(g.generate(t['difficulty'],0,sid,t['original']));old=sources[sid];of=old[':question/answer-fields'][0]
  original=[math(a[':answer/value']) for a in of[':answer-field/choices']];generated=[math(a[':answer/value']) for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert sorted(original,key=str)==sorted(generated,key=str) and math(correct_value(old))==math(correct_value(rec['question']))
  original_fn=supplied(old);assert original_fn is not None and sp.simplify(original_fn[0]-g.expression(sid,t['original']))==0
  replay.append({'source':sid,'choices_matched':len(original),'choices_total':len(original),'distractors_matched':len(original)-1,'complete_bank_match':True,'source_backbone_preserved':True,'literal_layout_match':False,'documented_changes':'normalized TeX and whitespace; easy restores given function/derivative and removes prior-step reference; q-342107 corrects opening function identity'})
  variant=check(g.generate(t['difficulty'],42,sid));review.append('## '+sid+'\n\nOriginal\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nReplay (documented corrections)\n\n'+g.markdown(rec)+'\n\nVariant\n\n'+g.markdown(variant))
  ps=g.candidates(sid);slots=[sorted({p[i] for p in ps}) for i in range(len(t['original']))];coverage[sid]={'instances':len(ps),'slot_values':slots,'all_bounded_tuples_checked':True}
  for p in ps:
   r=check(g.generate(t['difficulty'],0,sid,p));assert g.generate(t['difficulty'],91,sid,p)['question']==r['question'];inputs.append(native(sid+' '+str(p),r));total+=1
  if len(slots[-1])>1:
   p1=next(p for p in ps if p[:-1]==t['original'][:-1] and p[-1]!=t['original'][-1]) if sid!='q-10742' else None
   # q-10742 c is intentionally dependent on target to retain cancellation.
   if p1:
    other=check(g.generate(t['difficulty'],0,sid,p1));assert supplied(other['question'])[0]==supplied(rec['question'])[0];assert other['question'][':question/problem']!=rec['question'][':question/problem'];coverage[sid]['held_function_changed_target_check']=True
   else:coverage[sid]['target_dependency']='c adjusts to preserve small cancellation slope; independently validates all targets'
 save('source-replay.json',{'passed':True,'complete_banks_matched':6,'complete_banks_total':6,'distractors_matched':8,'distractors_total':8,'profiles':replay,'exclusions':{'q-1896':'unrated, no correct answer or solution','q-1899':'unrated, no correct answer or solution','q-128332':'function and prior derivative context absent from prompt','q-167695':'point A and prior piecewise context absent from prompt'}})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('slot-coverage.json',coverage);save('previews.json',g.batch('easy',5,2206)+g.batch('moderate',5,2206));(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'exhaustive_instances':total,'mathematics':'independent parser reads rendered function, derivative stages, evaluation stages, banks and conclusion; SymPy differentiates rendered function','fidelity':'6/6 complete supported banks; 8/8 distractors; documented source corrections and exclusions','native_grading':'actual learning::grade_field for every bounded variant; equivalent correct blanks and incorrect responses','supported_levels':['easy','moderate'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py')}})
 print(json.dumps({'passed':True,'instances':total,'coverage':coverage}))
if __name__=='__main__':main()
