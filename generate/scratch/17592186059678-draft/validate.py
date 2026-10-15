"""Private independent rendered mathematics and actual frozen-native grading audit."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;ROOT=H.parents[2];ENGINE=ROOT/'generate/runs/current/check-engine';SCRIPT=H.with_suffix('.py')
spec=importlib.util.spec_from_file_location('draft59678',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
p=g.parser;x=p.x

def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(n,v):(H/n).write_text(json.dumps(v,indent=2,ensure_ascii=False,default=str)+'\n')
def eq(a,b):assert p.equivalent(a,b),(a,b)
def data(profile,parameters):
 vals=list(map(sp.Rational,parameters['multipliers']));a,b=vals[:2];c=vals[2]if len(vals)==3 else None;s=g.sid_for(profile)
 if s=='q-10903':f=5*a*x**4+4*b*x**2;bank=[60*a*x*x+12*b,60*a*x*x+8*b,60*a*x*x+8*b*x,30*a*x*x+8*b,60*a*x**3+8*b]
 elif s=='q-10884':f=3*a*x**5+4*b*x**3-10*c*x*x;bank=[60*a*x**3-24*b*x-20*c,60*a*x**3+24*b*x-22*c,60*a*x**3+24*b*x-20*c,60*a*x**3+48*b*x-20*c,30*a*x**3+24*b*x-20*c]
 elif s=='q-104191':f=a*sp.log(x)+b/(6*x*x);bank=[a/x**2-b/(2*x**4),b/(2*x**4)+a/x,b/x**4-a/x**2,b/(3*x**3)-2*a/x,-a/x**2-b/x**4]
 elif s=='q-104192':f=4*a/sp.sqrt(x)+2*b*sp.sin(x);bank=[3*a/x**sp.Rational(5,2)-2*b*sp.sin(x),-3*a/x**sp.Rational(5,2)+b*sp.cos(x),3*a*x**sp.Rational(5,2)-b*sp.sin(x),4*a/(3*x**sp.Rational(5,2))+2*b*sp.sin(x),-a*x**sp.Rational(5,2)-2*b*sp.cos(x)]
 elif s=='q-342868':f=a*x**8/4+b*x-4*c/sp.sqrt(x);bank=[14*a*x**6-3*c/x**sp.Rational(5,2)]
 elif s=='q-342877':f=(6*a*x**3+2*b*x**2-8*c)/(2*x);bank=[6*a-8*c/x**3]
 elif s=='q-342966':f=6*a*sp.sqrt(x)+5*b*sp.cos(x);bank=[-3*a/(2*x**sp.Rational(3,2))-5*b*sp.cos(x)]
 else:assert s=='q-342970';f=a*x**5+3*b*sp.sin(x)-c/x**2;bank=[20*a*x**3-3*b*sp.sin(x)]
 return f,bank

def independent(r):
 g.fmt.validate_generated_record(r);q=r['question'];m=r['generation'];s=g.sid_for(m['profile']);g.check_parameters(m['profile'],m['parameters']);f,bank=data(m['profile'],m['parameters']);actual=p.function(q);eq(actual,f)
 assert q[':question/difficulty']==':question.difficulty/'+g.PROFILES[m['profile']]
 assert m['domain']==('x>0'if s in ('q-104191','q-104192','q-342868','q-342966')else 'x!=0'if s in ('q-342877','q-342970')else 'real x')
 operator=r'\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}';assert q[':question/problem'].startswith('Calculate $'+operator+'$ for $y=')
 # No alternative function/variable, evaluation target or derivative order is eligible.
 assert not actual.free_symbols-{x};assert set(re.findall(r'\\operatorname\{([^}]+)\}',q[':question/problem']))<= {'sin','cos'}
 fs=q[':question/answer-fields'];old=g.SOURCES[s][':question/answer-fields'];assert len(fs)==len(old)==1
 field=fs[0];of=old[0];assert field[':answer-field/key']==of[':answer-field/key'];assert field[':answer-field/type']==of[':answer-field/type'][':db/ident']
 assert len(field[':answer-field/choices'])==len(bank);actual_bank=[p.expr(a[':answer/value'])for a in field[':answer-field/choices']]
 for value,target in zip(actual_bank,bank):eq(value,target)
 assert all(not p.equivalent(a,b)for i,a in enumerate(actual_bank)for b in actual_bank[i+1:])
 assert len({a[':answer/id']for a in field[':answer-field/choices']})==len(bank)
 assert all(a[':answer/type']==':answer.type/math'for a in field[':answer-field/choices'])
 suffix=re.search(r'\{\{field-1\}\}\s*\$(.*?)\$',q[':question/problem'],re.S)
 target=sp.diff(f,x,2)-(p.expr(suffix[1])if suffix else 0)
 assert bool(suffix)==(s=='q-342970');indices=[i for i,v in enumerate(actual_bank)if p.equivalent(v,target)];assert len(indices)==1
 assert field[':answer-field/correct']==[':answer/id',field[':answer-field/choices'][indices[0]][':answer/id']]
 solution=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S);assert len(blocks)==2
 original=g.SOURCES[s][':question/worked-solution'];original_blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',original,re.S)
 prefix=r'\frac{\text{d}}{\text{d}x}(';lhs=[r'\frac{\text{d}y}{\text{d}x}',operator];stages=0
 assert re.sub(r'\$\$.*?\$\$','MATH',solution,flags=re.S)==re.sub(r'\$\$.*?\$\$','MATH',original,flags=re.S)
 for bi,(block,oldblock)in enumerate(zip(blocks,original_blocks)):
  rows=block.split(r' \\ ');oldrows=oldblock.split(r' \\ ');assert len(rows)==len(oldrows)
  assert rows[0].split('& =')[0].strip()==lhs[bi]
  for ri,(row,oldrow)in enumerate(zip(rows,oldrows)):
   assert '& ='in row;left,rhs=row.split('& =',1);rhs=rhs.strip();oldrhs=oldrow.split('& =',1)[1].strip()
   if ri:assert not left.strip()
   assert rhs.startswith(prefix)==oldrhs.startswith(prefix)
   if rhs.startswith(prefix):assert rhs.endswith(')');operand=p.expr(rhs[len(prefix):-1]);eq(operand,sp.diff(f,x,bi));value=sp.diff(operand,x)
   else:value=p.expr(rhs)
   eq(value,sp.diff(f,x,bi+1));stages+=1
 # Source expression masks retain every ordered source stage and operand structure.
 # Checked separately from mathematical equality so swapping equal stages fails.
 assert solution==g.fmt.normalize_prose(g.render(m['profile'],'solution',m['parameters']))
 assert q[':question/problem']==g.fmt.normalize_prose(g.render(m['profile'],'problem',m['parameters']))
 return stages

def checks(r):
 f=r['question'][':question/answer-fields'][0];bank=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'Every owned original-profile bank option'}for a in bank]
 val=bank[0][':answer/value'];z=p.expr(val);entries=[(val,'accepted'),('('+val+')','accepted'),(sp.sstr(z).replace('**','^'),'accepted'),('0','rejected'),('1','rejected'),(val+'+1','rejected')]
 if r['generation']['profile']=='q-342970':entries.append((sp.latex(sp.diff(p.function(r['question']),x,2)),'rejected'))
 return [{'submitted':s,'expected':expected,'purpose':'Ordinary canonical/equivalent/0/1/+1 native blank grading'}for s,expected in entries]
def fail(fn):
 try:fn()
 except (ValueError,TypeError,KeyError,AssertionError):return
 raise AssertionError('Invalid request/mutation accepted')
def main():
 baseline=json.loads((H/'registered-baseline.json').read_text());paths=[ROOT/'generate/scratch/17592186059678.py']+sorted(z for z in (ROOT/'generate/scratch/17592186059678').rglob('*')if z.is_file());assert set(map(str,paths))=={str(ROOT/a['path'])for a in baseline['files']};assert all(sha(ROOT/a['path'])==a['sha256']for a in baseline['files'])
 assert sha(ENGINE)=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea';assert g.SOURCE['basis']==2275
 raw=[];served=[];fidelity=[]
 for sid,q in g.SOURCES.items():
  r=g.observed_raw(sid);assert r['question']==q;raw.append({'source_id':sid,'parameters':r['generation']['parameters'],'record':r,'role':'observed MA source practice','eligible':sid in g.MASKS})
  entry={'source_id':sid,'whole_raw_original_exact':True,'attrs_omissions_exact':True,'served':sid in g.MASKS}
  if sid in g.MASKS:
   rec=g.generate(g.PROFILES[sid],template=sid,parameters=r['generation']['parameters']);independent(rec);served.append(rec);assert rec['question'][':question/problem']==g.fmt.normalize_prose(g.typography(q[':question/problem']));assert rec['question'][':question/worked-solution']==g.fmt.normalize_prose(g.typography(q[':question/worked-solution']))
   f=rec['question'][':question/answer-fields'][0];of=q[':question/answer-fields'][0]
   assert [a[':answer/value']for a in f[':answer-field/choices']]==[g.fmt.normalize_tex(g.typography(a[':answer/value']))for a in of[':answer-field/choices']]
   eq(p.expr(of[':answer-field/correct'][':answer/value']),p.expr(next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])))
   entry.update(normalized_prompt_solution_exact=True,complete_bank=True,matched_values=len(f[':answer-field/choices']),matched_distractors=len(f[':answer-field/choices'])-1,correct_designation=True)
  else:entry['raw_only_reason']='Missing difficulty/correct key/worked solution'if sid=='q-10894'else'Missing answer fields; no inferred field contract'
  fidelity.append(entry)
 save('source-cases.json',{'basis':2275,'lineage':g.SOURCE['lineage'],'questions':raw});save('source-replay.json',fidelity);save('served-originals.json',served)
 inventory=[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Registered generator common positive scale of q-342868; inventory evidence only, excluded from MA source counts'}for q in g.SOURCE['record'][':knowledge-point/questions']if ':question/math-academy-id'not in q]
 save('independent-inventory.json',{'basis':2275,'lineage':g.SOURCE['lineage'],'questions':inventory})
 allrecords=[];stages=0;capacity={};coverage={};reviews=[]
 for level in g.SUPPORTED_LEVELS:
  records=[g.generate(level,173,template=s,parameters=par)for s,par in g.catalog(level)]
  for r in records:stages+=independent(r)
  fingerprints={g.mathematical_fingerprint(r)for r in records};assert len(fingerprints)==len(records)
  assert g.batch(level,len(records),173)==g.batch(level,len(records),173);capacity[level]=len(records);coverage[level]={s:len(g.candidates(s))for s,l in g.PROFILES.items()if l==level};allrecords+=records
  for s,l in g.PROFILES.items():
   if l==level:reviews.append({'profile':s,'original':next((r for r in served if r['generation']['profile']==s),None),'variant':next(r for r in records if r['generation']['profile']==s and any(z!='1'for z in r['generation']['parameters']['multipliers']))})
  fail(lambda:g.batch(level,len(records)+1))
 assert len(g.batch('all',1))==3
 for level in ['all','easy','moderate','hard']:
  for outformat in ['json','markdown']:
   proc=subprocess.run([sys.executable,str(SCRIPT),'--difficulty',level,'--count','1','--format',outformat],capture_output=True,text=True);assert proc.returncode==0,proc.stderr
   if outformat=='json':assert isinstance(json.loads(proc.stdout),list)and len(json.loads(proc.stdout))==(3 if level=='all'else 1)
 mutations=[];ref=served[0]
 actions=[('operator order',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('^{2}y','^{3}y',1))),('input operand',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('5{x}^{4}','6{x}^{4}'))),('variable',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('y=','z='))),('intermediate',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('20{x}^{3}','21{x}^{3}',1))),('bank',lambda r:r['question'][':question/answer-fields'][0][':answer-field/choices'][0].__setitem__(':answer/value','999')),('key',lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id','foreign'])),('field type',lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/type',':answer-field.type/blank')),('function name',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('y=','f(x)=')))]
 for name,action in actions:
  bad=copy.deepcopy(ref);action(bad);assert bad!=ref;fail(lambda:independent(bad));mutations.append(name)
 for r in served:
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',r['question'][':question/worked-solution'],re.S)
  for bi,block in enumerate(blocks):
   for ri,row in enumerate(block.split(r' \\ ')):
    bad=copy.deepcopy(r);new=row.replace('& =','& =1+',1);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(row,new,1);fail(lambda:independent(bad));mutations.append(f'{r["generation"]["profile"]} stage {bi}/{ri}')
 for fn in [lambda:g.generate('unknown'),lambda:g.generate('easy',True),lambda:g.generate('easy',template=''),lambda:g.generate('easy',template='q-104191'),lambda:g.generate('hard',profile='q-342868'),lambda:g.generate('easy',parameters={}),lambda:g.generate('easy',template='q-10903',parameters={'multipliers':[1,1]}),lambda:g.generate('easy',template='q-10903',parameters={'multipliers':['0','1']}),lambda:g.generate('easy',template='q-10903',parameters={'multipliers':['1','1'],'extra':1}),lambda:g.batch('easy',True),lambda:g.batch('easy',0),lambda:g.batch('easy',1,0.5),lambda:g.observed_raw('missing'),lambda:g.observed_raw('q-10903',{'multipliers':['2','1']})]:fail(fn)
 native=[{'label':str(i),'record':r,'checks':checks(r)}for i,r in enumerate(allrecords)];save('native-input.json',native);run=subprocess.run([str(ENGINE),str(H/'native-input.json'),str(H/'native-grading.json')],capture_output=True,text=True);assert run.returncode==0,run.stderr
 report=json.loads((H/'native-grading.json').read_text());assert report['documented_unresolved_checks']==0
 diagnostics=[{'label':'foreign ID diagnostic','record':ref,'checks':[{'submitted':'999999','expected':'unresolved','purpose':'Isolated foreign ID diagnostic; no owned math failures hidden'}]}];save('native-diagnostics-input.json',diagnostics);subprocess.run([str(ENGINE),str(H/'native-diagnostics-input.json'),str(H/'native-diagnostics.json')],check=True)
 save('capacity.json',{'finite_distinct_mathematical_tasks':capacity,'coverage':coverage,'hard_calibration':'No observed hard practice. Authored fractional coefficient variants use the same moderate three-term radical/power method. Difficulty confidence limited; no new topic, operation order, evaluation target or solution stage.','excluded_cosmetic_capacity':['linear summand coefficient in q-342868 and q-342877 fixed to 1','seed and option order','names'],'target_order_policy':'Order 2 fixed by KP; full derivative or source partial-blank fragment fixed by response contract. Changing target order is outside this KP.'})
 save('side-by-side.json',reviews);(H/'review.md').write_text('\n\n'.join('## '+r['profile']+'\n\n'+('Original\n\n'+g.markdown(r['original'])if r['original']else'Authored hard; no observed hard original.')+'\n\nVariant\n\n'+g.markdown(r['variant'])for r in reviews)+'\n')
 save('validation.json',{'status':'worker_validated_root_review_pending','basis':2275,'raw_MA_originals':len(raw),'complete_served_MA_profiles':len(served),'raw_only_incomplete':2,'complete_banks_matched':len(served),'values_matched':sum(e.get('matched_values',0)for e in fidelity),'distractors_matched':sum(e.get('matched_distractors',0)for e in fidelity),'independent_inventory':len(inventory),'exhaustive_public_instances':len(allrecords),'every_rendered_solution_stage_checked':stages,'structural_and_stage_mutations_rejected':len(mutations),'mutations':mutations,'native_grading':{k:report[k]for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'native_engine_sha256':sha(ENGINE),'registered_baseline_whole_path_set_and_hashes_preserved':True,'capacity':capacity,'generator_sha256':sha(SCRIPT),'database_writes':0,'registration_changes':0})
 save('runtime.json',{'python_executable':sys.executable,'python_version':sys.version,'sympy_version':sp.__version__,'sympy_init_sha256':sha(Path(sp.__file__)),'private_parser_sha256':sha(H/'display_parser.py'),'private_formatter_sha256':sha(H/'math_format.py'),'native_engine_sha256':sha(ENGINE)})
 files=[SCRIPT]+[f for f in H.iterdir()if f.is_file()and f.name!='freeze.json'];save('freeze.json',{'status':'draft_worker_validated_root_review_pending','basis':2275,'files':{str(f.relative_to(ROOT)):sha(f)for f in sorted(files)},'database_writes':0,'registration_changes':0})
 print(json.dumps({'capacity':capacity,'instances':len(allrecords),'native':run.stdout.strip(),'generator_sha256':sha(SCRIPT)}))
if __name__=='__main__':main()
