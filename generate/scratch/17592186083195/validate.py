"""Independent printed-integral parser, exact integral, banks, replay and native grading."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
spec=importlib.util.spec_from_file_location('g',P.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
def write(name,x):(P/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def value(text):
 text=re.sub(r'\s+','',text)
 def group(pos):
  assert text[pos]=='{';depth=1;start=pos+1;pos+=1
  while depth:
   if text[pos]=='{':depth+=1
   elif text[pos]=='}':depth-=1
   pos+=1
  return text[start:pos-1],pos
 if re.fullmatch(r'-?\d+',text):return s.Integer(text)
 if text.startswith(r'\frac'):
  a,pos=group(5);b,pos=group(pos);assert pos==len(text)
  return value(a)/value(b)
 m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',text)
 if m:return s.Integer(m[1] or 1)*s.sqrt(s.Integer(m[2]))
 raise ValueError('Unrecognized exact answer '+text)
def printed(problem):
 L=s.Integer(re.search(r'\\int\s*\}_\{(\d+)\}',problem)[1])
 C=s.Integer(re.search(r'\\frac\{(\d+)\}',problem)[1])
 m=re.search(r'\\sqrt(?:\[(\d+)\])?\{\{(?:\\theta |[a-z])\}\^\{(\d+)\}\}',problem)
 if m:
  degree=s.Integer(m[1] or 2);p=s.Rational(m[2])/degree
  d=re.search(r'\\frac\{\d+\}\{(\d+)\\sqrt',problem)
  if d:C/=s.Integer(d[1])
 else:
  m=re.search(r'\\frac\{\d+\}\{\{(?:\\theta |[a-z])\}\^\{(\d+)\}\}',problem);assert m,problem
  p=s.Integer(m[1])
 return C,p,L
def fingerprint(q):
 C,p,L=printed(q[':question/problem'])
 return G.digest({'coefficient':str(C),'exponent':str(p),'lower':int(L)})
def structural(r):
 q=r['question'];C,p,L=printed(q[':question/problem']);assert C>0 and p>1 and L>0
 x=s.Symbol('x',positive=True);a=s.Symbol('a',positive=True)
 # Independent exact definite integration; limit, rather than generator's formula.
 primitive=s.integrate(C*x**(-p),x);expected=s.simplify(s.limit(primitive.subs(x,a)-primitive.subs(x,L),a,s.oo))
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];correct=next(z for z in choices if z[':answer/id']==f[':answer-field/correct'][1]);assert value(correct[':answer/value'])==expected
 assert fingerprint(q)==r['generation']['parameter_fingerprint']
 vals=[value(z[':answer/value']) for z in choices if z[':answer/type']==':answer.type/math']
 assert len(vals)==len(set(vals)) and vals.count(expected)==1
 assert len({z[':answer/id'] for z in choices})==len(choices)
 if f[':answer-field/type'].endswith('/blank'):assert len(choices)==1 and '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 else:assert len(choices)==5
 last=q[':question/worked-solution'].split(r' \\  & =')[-1].split('\\end{aligned}')[0].rstrip('.')
 assert value(last)==expected
 assert r['knowledge_point']['db_id']==G.KP_ID
 for text in (q[':question/problem'],q[':question/worked-solution']):
  assert text.count('$')%2==0 and '@' not in text
  depth=0
  for ch in text:
   depth+=(ch=='{')-(ch=='}');assert depth>=0
  assert depth==0
 return expected
def checks(r):
 f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned choice grading; separate exact integral checks validate displayed mathematics'} for a in f[':answer-field/choices']]
 v=f[':answer-field/choices'][0][':answer/value'];correct=structural(r)
 return [{'field_index':0,'submitted':x,'expected':e,'purpose':'Actual blank canonical/equivalent/wrong-entry grading'} for x,e in [(v,'accepted'),(str(correct.p*2)+'/'+str(correct.q*2), 'accepted'),(str(correct),'accepted'),(str(correct+1),'rejected')]]
def main():
 source=json.loads((P/'source.json').read_text())['record'][':knowledge-point/questions'];by={q[':question/math-academy-id']:q for q in source}
 native=[];review=[];reports=[];banks=answers=distractors=0
 for t in G.TEMPLATES:
  r=G.generate(t['level'],17,t['template'],parameters=t['source_parameters'],profile=t['bank_profile']);structural(r);q=r['question'];original=by[t['source_id']]
  assert q[':question/problem']==original[':question/problem'],t['source_id']
  assert q[':question/worked-solution']==original[':question/worked-solution'],t['source_id']
  f=q[':question/answer-fields'][0];of=original[':question/answer-fields'][0];assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
  orig=sorted((a[':answer/type'][':db/ident'],a[':answer/value'],a[':answer/id']==of[':answer-field/correct'][':answer/id']) for a in of[':answer-field/choices']);gen=sorted((a[':answer/type'],a[':answer/value'],a[':answer/id']==f[':answer-field/correct'][1]) for a in f[':answer-field/choices']);assert orig==gen
  answers+=len(orig);banks+=len(orig)>1;distractors+=len(orig)-1
  reports.append({'source_id':t['source_id'],'prompt_exact':True,'solution_exact':True,'complete_bank_and_correct_designation_exact':True,'matched_options':len(orig),'missing_options':[],'extra_options':[]})
  native.append({'label':'Source '+t['source_id'],'record':r,'checks':checks(r)});review.append({'label':'Source replay '+t['source_id'],'record':r})
  for i in range(25):
   r=G.generate(t['level'],i,t['template']);structural(r)
   r2=G.generate(t['level'],i+1000,t['template'],parameters=r['generation']['parameters']);assert r['question'][':question/id']==r2['question'][':question/id']
   native.append({'label':t['source_id']+' variant '+str(i),'record':r,'checks':checks(r)})
   if i==0:review.append({'label':'Variant '+t['source_id'],'record':r})
  bounds=['1/2','1/2000'] if t['source_id']=='q-152754' else ['1','2000']
  for C in bounds:structural(G.generate(t['level'],parameters={'coefficient':C},template=t['template']))
  for C in ['0','-1','2001','3/2']:
   try:G.generate(t['level'],template=t['template'],parameters={'coefficient':C});raise AssertionError('Invalid coefficient accepted')
   except ValueError:pass
 for level in G.SUPPORTED_LEVELS:
  b=G.batch(level,10,9925);assert len({fingerprint(r['question']) for r in b})==10
 try:G.batch('hard',5);raise AssertionError('Hard unexpectedly supported')
 except ValueError:pass
 write('engine-input.json',native);subprocess.run([str(P/'check-engine'),str(P/'engine-input.json'),str(P/'engine-report.json')],check=True)
 engine=json.loads((P/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 write('review.json',review);(P/'review.md').write_text('# Source replay and variants\n\n'+ '\n\n---\n\n'.join('## '+r['label']+'\n\n'+G.markdown(r['record']) for r in review)+'\n')
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P.with_suffix('.py'),P/'templates.json',P/'source.json',Path(__file__)]}
 write('validation.json',{'passed':True,'source_basis':json.loads((P/'source.json').read_text())['basis'],'source_total':len(source),'source_replayed':len(reports),'excluded_source_ids':['q-128340'],'exclusion':'Prompt uses undefined f(x); no integrand or plot is present. Rational template is excluded from this package, preserving source unchanged.','source_replay':reports,'complete_banks_matched':banks,'matched_options':answers,'matched_distractors':distractors,'missing_or_extra_options':0,'generated_instances_checked':300,'supported_levels':list(G.SUPPORTED_LEVELS),'unsupported_levels':['hard'],'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':hashes,'engine_sha256':hashlib.sha256((P/'check-engine').read_bytes()).hexdigest(),'fidelity':'Exact prompt, solution, field and bank replay for all 12 supported source layouts; one defective source explicitly excluded','correctness':'Independent parse of displayed integrand, exact definite integration and infinite limit for each instance','grading':'Actual engine canonical/equivalent and incorrect blank submissions, and every owned radio choice','narrow_policy':'Coefficient only; fixed exponent and endpoint per source. Complete observed scaled banks; distractor interpretations unresolved, values and replay fully resolved.','database_writes':0})
 print('Validation PASS:',len(reports),'source replays,',banks,'banks,',distractors,'distractors, 300 variants')
if __name__=='__main__':main()
