"""Independent printed linear-expression and geometry checks; native learner grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('parallel_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.Symbol('x',real=True)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def expression(t):
 t=t.strip().replace(' ','')
 t=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t)
 t=re.sub(r'(\d|\))x',r'\1*x',t)
 if '=' in t:t=t.split('=',1)[1]
 return sp.expand(sp.sympify(t,locals={'x':x}))
def fingerprint(q):return g.fingerprint(q)
def check(rec):
 q=rec['question'];meta=rec['generation'];p=meta['parameters'];m=sp.Rational(p['m']);c=sp.Rational(p['c']);x0=p['x0'];y0=p['y0'];b=sp.Integer(y0)-m*x0
 assert meta['version']==g.VERSION
 expected=g.generate(g.TEMPLATES[meta['template']]['level'],meta['seed'],meta['template'],p,replay=not meta['asset_local'])['question']
 actual=dict(q);actual[':question/problem']=actual[':question/problem'].replace(meta['asset'],expected[':question/problem'].split('![](',1)[1].split(')',1)[0])
 assert actual==expected,'Generator content or stable identity mismatch'
 assert rec['knowledge_point']['db_id']==g.KP_ID and g.allowed(meta['template'],p)
 assert q[':question/difficulty']==':question.difficulty/'+g.TEMPLATES[meta['template']]['level']
 printed=re.search(r'line \$l_\{1\}\$ is \$y =([^$]+)\$',q[':question/problem']);assert printed
 line1=expression(printed[1]);assert line1==m*x+c
 f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];assert len(q[':question/answer-fields'])==1
 vals=[expression(a[':answer/value']) for a in bank]
 assert len(set(vals))==len(vals) and len({a[':answer/id'] for a in bank})==len(bank)
 correct=[a[':answer/id'] for a,v in zip(bank,vals) if v==m*x+b];assert correct==[f[':answer-field/correct'][1]]
 assert (m*x+b).subs(x,x0)==y0 and sp.diff(m*x+b,x)==sp.diff(line1,x)
 assert fingerprint(q)==meta['mathematical_fingerprint']
 sol=q[':question/worked-solution'];assert f'point $({x0},{y0})$' in sol
 rows=re.findall(r'y &= (.*?)(?:\n|$)',sol);assert len(rows)==2
 assert all(expression(row.rstrip('\\').strip())==m*x+b for row in rows)
 if f[':answer-field/type']==':answer-field.type/blank':
  assert len(bank)==1 and q[':question/problem'].endswith('$y =$\n{{field-1}}') and '=' not in bank[0][':answer/value']
 else:assert len(bank)==5 and f[':answer-field/key']=='selection'
 if meta['asset_local'] and Path(meta['asset']).exists():
  a=json.loads(Path(meta['asset']+'.json').read_text());assert a['parameters']==p and a['l2_intercept']==str(b) and a['marked_point']==[x0,y0]
  assert hashlib.sha256(Path(meta['asset']).read_bytes()).hexdigest()==a['sha256']
 return rec
def native(label,r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete native radio bank'} for a in f[':answer-field/choices']]
 else:
  p=r['generation']['parameters'];m=sp.Rational(p['m']);b=sp.Integer(p['y0'])-m*p['x0']
  checks=[{'submitted':str(m*x+b),'expected':'accepted','purpose':'canonical expression'}, {'submitted':f'({m})*(x-({p["x0"]}))+({p["y0"]})','expected':'accepted','purpose':'equivalent point-slope RHS'}, {'submitted':str(m*x+b+1),'expected':'rejected','purpose':'wrong intercept'}, {'submitted':str(-m*x+b),'expected':'rejected','purpose':'wrong slope'}]
 return {'label':label,'record':r,'checks':checks}
def main():
 source=json.loads((HERE/'source.json').read_text());byid={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};replays=[];inputs=[];review=[]
 assert fingerprint(source['record'][':knowledge-point/canonical-example'])==g.digest(['2/3',0,1])
 assert {fingerprint(q) for q in byid.values()}=={g.digest(['-1',0,-1]),g.digest(['1/2',-4,4])}
 for t,p in g.SOURCE_PARAMETERS.items():
  r=check(g.generate(g.TEMPLATES[t]['level'],0,t,p,replay=True));old=byid[g.SOURCE_IDS[t]];q=r['question'];assert old[':question/problem']==q[':question/problem']
  of=old[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
  if t=='intercept_radio':
   observed=[expression(a[':answer/value']) for a in of[':answer-field/choices']];generated=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
   assert set(observed)==set(generated) and len(observed)==len(generated)==5
   assert [a[':answer/value'] for a in of[':answer-field/choices']]==[a[':answer/value'] for a in f[':answer-field/choices']]
  replays.append({'source':g.SOURCE_IDS[t],'template':t,'prompt_exact':True,'field_contract_exact':True,'matched_choices':5 if t=='intercept_radio' else 0,'total_choices':5 if t=='intercept_radio' else 0,'source_correct_marker_present':False,'source_solution_present':False,'derived_correct':f[':answer-field/choices'][0][':answer/value'],'complete_observed_bank_match':True if t=='intercept_radio' else None})
  inputs.append(native('source-'+t,r));review.append('## '+g.SOURCE_IDS[t]+'\n\nOriginal\n\n'+old[':question/problem']+'\n\nReplay (answer and solution authored)\n\n'+g.markdown(r))
 # Exhaustive bounded parameter validation with renderer stub; geometry is
 # validated via the same exact line data, plots are checked separately below.
 render=g.render_plots;g.render_plots=lambda p,d:'validation-only-plot.png';counts={};fps=set()
 try:
  for t in g.TEMPLATES:
   ps=list(g.candidates(t));counts[t]=len(ps)
   for p in ps:
    r=check(g.generate(g.TEMPLATES[t]['level'],0,t,p));inputs.append(native(t+str(p),r));fps.add(fingerprint(r['question']))
    assert g.generate(g.TEMPLATES[t]['level'],99,t,p)['question']==r['question']
 finally:g.render_plots=render
 previews=g.batch('easy',5,1909)+g.batch('moderate',5,1909)
 for r in previews:check(r);inputs.append(native('preview-'+r['question'][':question/id'],r));review.append('## Variant\n\n'+g.markdown(r))
 for t,p in [('intercept_radio',{'m':'0','c':'2','x0':0,'y0':1}),('intercept_radio',{'m':'1','c':'0','x0':0,'y0':0}),('point_blank',{'m':'1/2','c':'2','x0':0,'y0':1})]:
  try:g.generate(g.TEMPLATES[t]['level'],0,t,p)
  except ValueError:pass
  else:raise AssertionError('Invalid boundary accepted')
 save('source-replay.json',{'passed':True,'basis':source['basis'],'complete_observed_banks':1,'complete_observed_banks_matched':1,'source_distractors_reproduced':4,'source_distractors_total':4,'source_answer_values_matched':5,'missing_or_extra_options':[],'source_results':replays,'fidelity_limits':'Both sources unrated; correct markers and worked solutions missing. Blank bank empty. Derived graph answers and canonical-style solutions are authored additions; no claim of source key/solution fidelity.'})
 save('previews.json',previews);save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'exhaustive_instances':sum(counts.values()),'counts':counts,'distinct_bounded_tasks':len(fps),'math':'independently parsed printed reference-line slope, every answer expression, every simplified solution RHS, point incidence, bank distinctness, asset data consistency','native_grading':'every bank option and equivalent/incorrect blank submissions at every bounded parameter tuple','source_fidelity':'one complete bank 5/5, 4/4 distractors; both prompts and field contracts exact; missing source keys/solutions explicitly authored','supported_levels':['easy','moderate'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json')}})
 print('Validated',counts,'distinct',len(fps))
if __name__=='__main__':main()
