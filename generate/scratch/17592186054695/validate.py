"""Independent prompt/solution parsing, exact line banks, plot hashes, native grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.Symbol('x')
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def equation(t):
 t=t.strip().rstrip('.?').replace(' ','');t=re.sub(r'\\d?frac\{([^}]+)\}\{([^}]+)\}',r'(\1/\2)',t);t=re.sub(r'(\d|\))(?=x)',r'\1*',t)
 return sp.sympify(t,locals={'x':x})
def prompt_parameters(q):
 m=re.search(r'\$y\s*=\s*(.*?)\$',q[':question/problem']);assert m,q
 poly=sp.Poly(equation(m[1]),x);assert poly.degree()==1
 return [str(poly.coeff_monomial(x)),str(poly.coeff_monomial(1))]
def fingerprint(q):return g.fingerprint(prompt_parameters(q))
def check(rec):
 q=rec['question'];meta=rec['generation'];p=prompt_parameters(q);assert p==meta['parameters'];sid=meta['template'];m,b=map(sp.Rational,p)
 assert rec==g.generate('easy',meta['seed'],sid,p)
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];assert len(choices)==5
 # Independently derived source profiles, rather than generator bank equality alone.
 objects=[(-m,m),(m,-m),(m/2,0),(m,0),(-m,0)] if sid=='q-102054' else [(-m,-b),(m,2*b),(m,b),(-m,0),(m,0)]
 assert len(set(objects))==5
 assert [[str(z) for z in obj] for obj in objects]==meta['choice_lines']
 ci=next(i for i,z in enumerate(choices) if z[':answer/id']==f[':answer-field/correct'][1]);assert objects[ci]==(m,b)
 asset_lines={a['path']:tuple(map(sp.Rational,a['line'])) for a in meta['assets']};asset_lines.update({k:tuple(map(sp.Rational,v)) for k,v in g.CONTRACT['source_asset_lines'].items()})
 assert [asset_lines[a[':answer/value']] for a in choices]==objects
 points=[tuple(map(sp.Rational,z.split(','))) for z in re.findall(r'\$\(([-\d]+,[-\d]+)\)\.\$',q[':question/worked-solution'])];assert len(points)==2,points
 assert points[0][0]!=points[1][0] and all(m*px+b==py for px,py in points)
 solution=q[':question/worked-solution'];assert '@@' not in solution
 equations=re.findall(r'\$y=(.*?)\$',solution);assert equations and all(equation(z)==m*x+b for z in equations)
 for tex in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S):
  stages=tex.split(r'\\');values=[z.split('=')[-1].strip().rstrip('.') for z in stages[1:]]
  vals=[]
  for z in values:
   z=re.sub(r'\\d?frac\{([^}]+)\}\{([^}]+)\}',r'(\1/\2)',z);z=re.sub(r'(\d|\))(?=\()',r'\1*',z);vals.append(sp.sympify(z))
  assert vals and len(set(vals))==1,(p,vals)
 for a in meta['assets']:
  assert hashlib.sha256(Path(a['local']).read_bytes()).hexdigest()==a['sha256'];assert a['path']==f"images/{a['sha256'][:2]}/{a['sha256']}.png"
  for px,py in a['points']:assert sp.Rational(a['line'][0])*sp.Rational(px)+sp.Rational(a['line'][1])==sp.Rational(py)
  from PIL import Image
  im=Image.open(a['local']);assert im.width==540 and im.height==540
 assert meta['mathematical_fingerprint']==g.fingerprint(p)
 return rec
def native(label,rec):
 f=rec['question'][':question/answer-fields'][0];ci=f[':answer-field/correct'][1]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==ci else 'rejected','purpose':'actual image-radio learner grading'} for z in f[':answer-field/choices']]}
def main():
 raw=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']};replays=[];inputs=[];allrs=[];reviews=[]
 for sid,t in g.PROFILES.items():
  r=check(g.generate('easy',0,sid,t['parameters']));q=r['question'];old=qs[sid];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'];assert q[':question/worked-solution']==old[':question/worked-solution']
  assert [z[':answer/value'] for z in f[':answer-field/choices']]==[z[':answer/value'] for z in of[':answer-field/choices']]
  assert f[':answer-field/choices'][t['correct_index']][':answer/value']==of[':answer-field/correct'][':answer/value']
  replays.append({'source':sid,'complete_bank_match':True,'choices_matched':5,'distractors_matched':4,'prompt_exact':True,'solution_exact':True,'unchanged_source_assets':True})
  for p in g.candidates(sid):
   z=check(g.generate('easy',0,sid,p));assert g.generate('easy',99,sid,p)['question']==z['question'];inputs.append(native(sid+' '+str(p),z));allrs.append(z)
  variant=next(z for z in allrs if z['generation']['template']==sid and z['generation']['parameters']!=r['generation']['parameters']);reviews.append('## '+sid+'\n\nOriginal\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(r)+'\n\nVariant\n\n'+g.markdown(variant))
 save('source-replay.json',{'passed':True,'complete_banks_matched':2,'complete_banks_total':2,'distractors_matched':8,'distractors_total':8,'profiles':replays,'excluded_incomplete_sources':['q-54286','q-59678'],'exclusion_reason':'unrated and missing correct and worked solution; evidence and every observed graph retained; no invented grading key'})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('previews.json',allrs);(HERE/'review.md').write_text('\n\n'.join(reviews)+'\n')
 save('validation.json',{'passed':True,'exhaustive_instances':len(allrs),'distinct_bounded_lines':len({r['generation']['mathematical_fingerprint'] for r in allrs}),'mathematics':'independent rendered prompt and solution arithmetic; exact five distinct graph equations, two points lie on the selected line, plot parameter linkage and hashes','fidelity':'2/2 complete graded source banks and 8/8 distractors; exact source prompts, solutions and asset replay','native_grading':'all five choices for every bounded parameter tuple through learning::grade_field','supported_levels':['easy'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'contract.json',HERE/'validate.py')}})
if __name__=='__main__':main()
