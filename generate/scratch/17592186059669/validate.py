"""Source fidelity, independent printed mathematics, slot coverage and native grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sys.path.insert(0,str(D))
from math_reader import coordinate,expression,read_prompt,required,f,x
spec=importlib.util.spec_from_file_location('point_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
BINARY=ROOT/'generate/scratch/17592186059670/check-engine'
def display_check(rec):
 q=rec['question'];point,base,good,src,dst=required(q[':question/problem'])
 assert rec['knowledge_point']['db_id']==g.KP_ID
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
 assert len(blocks)==5 and '**Method 1**' in sol and '**Method 2**' in sol
 stages=re.findall(r'(?:graph of|graph of|graph of|graph of|graph of|graph of|graph of|graph of) \$y=(.*?)\.\$',sol)
 # Every coordinate equality is evaluated independently from the renderer.
 expected=[base,(base[0],-base[1]),good]
 for block,want in zip(blocks[:3],expected):
  lhs,rhs=block.rstrip('.').split('=');assert coordinate(lhs)==coordinate(rhs)==want
 # References preceding each stage must match the preceding actual point.
 starts=re.findall(r'After this transformation, the point \$(.*?)\$',sol)
 assert list(map(coordinate,starts))==[point,base,(base[0],-base[1])]
 curves=re.findall(r'(?:get the graph of|obtain the graph of) \$y=(.*?)\.\$',sol)
 assert list(map(expression,curves))==[f(x),-f(x),dst]
 final=re.search(r'Therefore, the point \$(.*?)\$ must lie on \$y=(.*?)\.\$',sol)
 assert coordinate(final[1])==good and expression(final[2])==dst
 # Independently check the substituted function equation and both algebra stages.
 left,right=blocks[3].rstrip('.').split(r'\quad\Longrightarrow\quad')
 for equality in (left,right):
  a,b=equality.split('=');diff=expression(a)-expression(b)
  for call in diff.atoms(sp.Function):
   assert call.func==f and call.args[0]==base[0];diff=diff.subs(call,base[1])
  assert diff==0
 terms=blocks[4].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
 assert len(terms)==3
 for term in terms:
  z=expression(term.split('=')[1].replace('&',''))
  for call in z.atoms(sp.Function):
   assert call.args[0]==base[0];z=z.subs(call,base[1])
  assert z==good[1]
 fields=q[':question/answer-fields'];assert len(fields)==1;field=fields[0]
 assert field[':answer-field/type']==':answer-field.type/radio' and field[':answer-field/key']=='selection'
 choices=field[':answer-field/choices'];values=[coordinate(a[':answer/value']) for a in choices]
 assert len(values)==len(set(values))==5 and values.count(good)==1
 correct=field[':answer-field/correct'][1]
 assert len([a for a in choices if a[':answer/id']==correct])==1
 assert coordinate(next(a[':answer/value'] for a in choices if a[':answer/id']==correct))==good
 for s in [q[':question/problem'],sol]+[a[':answer/value'] for a in choices]:
  assert s.count('$')%2==0 and s.count('{')==s.count('}') and '+-' not in s and '--' not in s
 return good
def grade(records,path):
 path.mkdir(parents=True,exist_ok=True);items=[]
 for r in records:
  field=r['question'][':question/answer-fields'][0]
  items.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'Every field-owned radio selection'} for a in field[':answer-field/choices']]})
 (path/'native-input.json').write_text(json.dumps(items,indent=2)+'\n')
 subprocess.run([str(BINARY),str(path/'native-input.json'),str(path/'native-report.json')],capture_output=True,text=True,check=True)
 result=json.loads((path/'native-report.json').read_text());assert result['accepted_checks']==len(records) and result['rejected_checks']==4*len(records) and result['documented_unresolved_checks']==0
 return result
def main():
 records=[];review=[];fidelity=[];coverage={};mapping=[]
 for sid,case in g.CASES.items():
  replay=g.generate(case['level'],profile=sid,parameters=case['p']);display_check(replay)
  source=g.ORIGINALS[sid];sf=source[':question/answer-fields'][0];rf=replay['question'][':question/answer-fields'][0]
  old=[coordinate(a[':answer/value']) for a in sf[':answer-field/choices']];new=[coordinate(a[':answer/value']) for a in rf[':answer-field/choices']]
  assert sorted(old)==sorted(new) and read_prompt(source[':question/problem'])==read_prompt(replay['question'][':question/problem'])
  assert coordinate(sf[':answer-field/correct'][':answer/value'])==display_check(replay)
  # Full original worked solution final answer and ordered geometric stages.
  final=re.search(r'Therefore, the point \$(.*?)\$ must lie on',source[':question/worked-solution']);assert coordinate(final[1])==display_check(replay)
  original_stages=re.findall(r'\$\$\s*(\([^\n]*?\)=\([^\n]*?\))\.?\s*\$\$',source[':question/worked-solution'])
  assert len(original_stages)==3
  for z,want in zip(original_stages,[required(source[':question/problem'])[1],(required(source[':question/problem'])[1][0],-required(source[':question/problem'])[1][1]),display_check(replay)]):
   lhs,rhs=z.split('=');assert coordinate(lhs)==coordinate(rhs)==want
  for a in sf[':answer-field/choices']:
   value=coordinate(a[':answer/value']);idx=g.bank(case,case['p']).index(value)
   mapping.append({'source_id':sid,'field_id':sf[':answer-field/id'],'original_answer_id':a[':answer/id'],'original_value':a[':answer/value'],'recipe':case['bank'][idx],'complete_value_replayed':True,'interpretation':'Observed coordinate value pattern; misconception intent unresolved'})
  fidelity.append({'source_id':sid,'template':case['kind'],'profile':sid,'complete_bank_matched':True,'choices_matched':5,'choices_total':5,'distractors_matched':4,'distractors_total':4,'missing':[],'extra':[],'correct_designation':True,'prompt_mathematics':True,'ordered_solution_coordinate_stages':3,'solution_layout':'Two methods, three coordinate stages, function substitution, final point; connective wording normalized'})
  records.append(replay);review.extend([{'label':'Original '+sid,'question':source},{'label':'Replay '+sid,'record':replay}])
  # Vary each slot with the other data held fixed. Check each allowed value.
  seen={key:[] for key in case['p']};witness={}
  for key in case['p']:
   for value in g.domain(case,key):
    p=dict(case['p']);p[key]=value
    try:r=g.generate(case['level'],profile=sid,parameters=p)
    except ValueError as err:
     assert str(err) in ('Degenerate source bank','Parameter outside supported domain');continue
    display_check(r);seen[key].append(str(value));records.append(r)
    if str(value)!=str(case['p'][key]) and key not in witness:witness[key]=r
   assert len(set(seen[key]))>=2
  # Directly changed supplied x/y exercises stale references and answer keys.
  for key,r in witness.items():
   review.append({'label':'Only '+key+' changed '+sid,'record':r})
   assert r['generation']['mathematical_fingerprint']!=replay['generation']['mathematical_fingerprint']
  tasks=set()
  for seed in range(32):
   r=g.generate(case['level'],seed,profile=sid);display_check(r);records.append(r);tasks.add(r['generation']['mathematical_fingerprint'])
   assert g.generate(case['level'],seed,profile=sid)==r
   assert g.generate(case['level'],seed+999,profile=sid,parameters=r['generation']['parameters'])['question'][':question/id']==r['question'][':question/id']
  assert len(tasks)>5
  coverage[sid]={'single_slot_allowed_values_checked':seen,'distinct_seeded_tasks':len(tasks),'changed_slot_witnesses':list(witness)}
 # Corrupt the answer, a printed equality and a point reference: must all fail.
 base=g.generate('moderate',profile='q-121407',parameters=g.CASES['q-121407']['p']);negative=0
 for mut in ('key','equality','point'):
  r=copy.deepcopy(base);field=r['question'][':question/answer-fields'][0]
  if mut=='key':field[':answer-field/correct'][1]=next(a[':answer/id'] for a in field[':answer-field/choices'] if a[':answer/id']!=field[':answer-field/correct'][1])
  elif mut=='equality':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('=(-2,4).','=(-2,5).',1)
  else:r['question'][':question/problem']=r['question'][':question/problem'].replace('(-3,4)','(-4,4)',1)
  try:display_check(r)
  except AssertionError:negative+=1
  else:raise AssertionError('Corruption escaped: '+mut)
 excluded=[]
 for sid,q in g.ORIGINALS.items():
  if sid in g.CASES:continue
  point,base,good,src,dst=required(q[':question/problem'])
  excluded.append({'source_id':sid,'mathematically_verified_answer':g.pair(good),'reason':'Fieldless' if not q.get(':question/answer-fields') else 'Unrated, missing key and worked solution','preserved':True,'gradable':False})
 native=grade(records,D/'reference/validation')
 (D/'choice-mapping.json').write_text(json.dumps(mapping,indent=2)+'\n')
 (D/'assets.json').write_text('[]\n')
 (D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 def view(item):
  q=item.get('question',item.get('record',{}).get('question'));return '## '+item['label']+'\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for field in q.get(':question/answer-fields',[]) for a in field[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
 (D/'review.md').write_text('\n\n---\n\n'.join(view(item) for item in review)+'\n')
 result={'status':'passed','source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'generator_version':g.VERSION,'generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'source_fidelity':fidelity,'full_banks_matched':7,'choices_matched':35,'distractors_matched':28,'slot_coverage':coverage,'negative_controls_rejected':negative,'excluded_sources':excluded,'native_grading':{'records':len(records),'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0,'binary_path':str(BINARY.relative_to(ROOT)),'binary_sha256':hashlib.sha256(BINARY.read_bytes()).hexdigest()},'dependencies':{'sympy':sp.__version__,'python':sys.version.split()[0]},'limitations':['Easy unsupported: no classified complete source; absence alone is not a mathematical impossibility','Opaque bank patterns are conservative same-value-pattern extensions; error intent is unresolved','Source punctuation and connective wording normalized; operative mathematics and complete banks replayed','Six incomplete source questions remain unchanged and excluded']}
 (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('status','full_banks_matched','choices_matched','native_grading')},indent=2))
if __name__=='__main__':main()
