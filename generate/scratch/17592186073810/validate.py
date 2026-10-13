"""Exhaustive independent geometry, complete bank replay, actual radio grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('axis_distance_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def check(rec):
 meta=rec['generation'];q=rec['question'];sid,k=meta['parameters'];assert rec==g.generate('easy',meta['seed'],sid,[sid,k])
 match=re.fullmatch(r'Find the shortest distance between the point \$\((-?\d+),(-?\d+)\)\$ and the line \$([xy])=(-?\d+)\.\$',q[':question/problem']);assert match
 x,y,c=map(sp.Integer,(match[1],match[2],match[4]));axis=match[3];A,B=(sp.Integer(1),sp.Integer(0)) if axis=='x' else (sp.Integer(0),sp.Integer(1))
 d=sp.simplify(abs(A*x+B*y-c)/sp.sqrt(A*A+B*B));assert d>0
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 vals=[sp.Integer(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==len(set(vals))==5
 correct=[v for a,v in zip(f[':answer-field/choices'],vals) if a[':answer/id']==f[':answer-field/correct'][1]];assert correct==[d] and vals.count(d)==1
 sol=q[':question/worked-solution'];assert f'point $({x},{y})$' in sol and f'${axis}={c}$' in sol and f'${c}.$' in sol
 eq=re.search(r'\$\$\s*d\s*=\s*\|(-?\d+)-\(?(-?\d+)\)?\|\s*=\s*(\d+)\.\s*\$\$',sol);assert eq
 assert sp.Integer(eq[1])==(x if axis=='x' else y) and sp.Integer(eq[2])==c and sp.Integer(eq[3])==d
 assert meta['mathematical_fingerprint']==fingerprint(q)
 for asset in meta['assets']:
  p=Path(asset['local_path']);p=p if p.is_absolute() else ROOT/p;assert hashlib.sha256(p.read_bytes()).hexdigest()==asset['sha256'] and asset['path'] in sol
  if k>1:
   z=json.loads(p.with_suffix('.json').read_text());assert z['parameters']==[axis,int(x),int(y),int(c)] and z['distance']==d
   assert z['foot']==([int(c),int(y)] if axis=='x' else [int(x),int(c)])
 return rec

def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all options through actual application radio grader'} for a in f[':answer-field/choices']]}
def main():
 banks=[];options=[];rs=[];inputs=[];review=[]
 for sid,old in g.CASES.items():
  r=check(g.generate('easy',0,sid,[sid,1]));f=r['question'][':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  assert r['question'][':question/problem']==old[':question/problem'] and r['question'][':question/worked-solution']==old[':question/worked-solution']
  banks.append({'source':sid,'profile':sid,'matched_choices':5,'matched_distractors':4,'complete_bank_match':True,'correct_designation':True,'prompt_exact':True,'solution_exact':True,'missing':[],'extra':[]})
  for a in of[':answer-field/choices']:options.append({'source':sid,'field':'selection','profile':sid,'source_answer_id':a[':answer/id'],'original_value':a[':answer/value'],'recipe':'k * ('+a[':answer/value']+')','interpretation':'observed whole distance value under integral dilation; underlying error unresolved','reproduces_at_source':True})
  for k in range(1,4):
   r=check(g.generate('easy',0,sid,[sid,k]));assert g.generate('easy',99,sid,[sid,k])['question']==r['question'];rs.append(r);inputs.append(native(sid+' k='+str(k),r))
  review.append('## '+sid+'\n\nSource replay\n\n'+g.markdown(g.generate('easy',0,sid,[sid,1]))+'\n\nVariant\n\n'+g.markdown(g.generate('easy',0,sid,[sid,2])))
 assert len({fingerprint(r['question']) for r in rs})==15
 # Irrelevant coordinate changes and bank permutations must not create novelty.
 a={':question/problem':'Find the shortest distance between the point $(4,3)$ and the line $x=2.$'};b={':question/problem':'Find the shortest distance between the point $(4,-7)$ and the line $x=2.$'};assert fingerprint(a)==fingerprint(b)
 for level in ('moderate','hard','unclassified'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported difficulty admitted')
 try:g.batch('easy',11)
 except ValueError:pass
 else:raise AssertionError('Finite limit ignored')
 save('source-replay.json',{'passed':True,'complete_banks_matched':5,'complete_banks_total':5,'distractors_matched':20,'distractors_total':20,'profiles':banks,'excluded_sources':{'q-74033':'unrated; missing correct designation and worked solution; retained unchanged and not admitted'}})
 save('choice-recipes.json',options);save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('previews.json',g.batch('easy',10,73810));(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'exhaustive_instances':15,'new_distinct_bounded_geometries':10,'supported_levels':['easy'],'independent_checks':'entire displayed geometry via point-line formula; relevant coordinate and line constant; source correct answer; five unique bank values; every rendered distance equality and solution parameter; asset hashes and plot geometry; deterministic IDs and seed independence; irrelevant-coordinate exclusion','source_fidelity':'5/5 complete banks and 20/20 distractors; source prompt and solution exact at replay; numeric values and sketch normalized for dilations; no bank mixing','native_grading':'15 records, all 75 choices through course_academy_engine::learning::grade_field','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'replenish.py',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine')}})
if __name__=='__main__':main()
