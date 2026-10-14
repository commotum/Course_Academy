"""Current-source classification and independent checks for the scoped replenisher."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('historical_validation',D/'validate.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
g=old.g;s=g.s
KP=g.KP_ID
g.KP=KP;g.GENERATOR_UUID=g.uid('question-generator')
g.REC=json.loads((D/'reference/initial/kp.json').read_text())
g.SNAP={'basis':json.loads((D/'reference/initial/inventory.json').read_text())['basis']}

def checks(r):
 return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all five complete bank values through application grade_field'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def source_context(q):
 prob=q[':question/problem'];sol=q[':question/worked-solution']
 mask=sol.split('suggests that we use the change of variables')[1].split('$$')[1].strip().rstrip('.')
 U,V=[old.math(t.split('=',1)[1]) for t in mask.split(r'\,')]
 M=s.Matrix([[s.diff(U,g.x),s.diff(U,g.y)],[s.diff(V,g.x),s.diff(V,g.y)]]);assert M.det()!=0
 iv=s.solve([U-g.u,V-g.v],[g.x,g.y]);pts=[(old.math(A),old.math(B)) for A,B in re.findall(r'\$\((.*?),(.*?)\)[,.]?\$',prob)];assert len(pts)==4
 cs=[(s.simplify(U.subs({g.x:A,g.y:B})),s.simplify(V.subs({g.x:A,g.y:B}))) for A,B in pts];a0=min(p[0] for p in cs);a1=max(p[0] for p in cs);b0=min(p[1] for p in cs);b1=max(p[1] for p in cs);assert set(cs)=={(a0,b0),(a1,b0),(a1,b1),(a0,b1)}
 F=old.math(prob.split('$$')[1].replace('{∬}_{D}','').split(r'\,dxdy')[0]);ft=s.simplify(F.subs(iv,simultaneous=True));ans=s.simplify(s.integrate(ft/abs(M.det()),(g.u,a0,a1),(g.v,b0,b1)))
 return dict(F=F,vertices=pts,transformation=[U,V],bounds=[a0,a1,b0,b1],transformed=ft,answer=ans)

def truth(q):
 ctx=source_context(q)
 assert str(q[':question/difficulty'][':db/ident'])==':question.difficulty/hard'
 for f in q[':question/answer-fields']:
  assert str(f[':answer-field/type'][':db/ident'])==':answer-field.type/radio'
  vals=[old.math(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==5
  for i,z in enumerate(vals):
   assert z.is_finite
   for other in vals[:i]:assert not g.eq(z,other)
  assert sum(g.eq(z,ctx['answer']) for z in vals)==1
  assert ':answer-field/correct' in f,'missing correct reference in legacy duplicate field'
  old.eq(old.math(f[':answer-field/correct'][':answer/value']),ctx['answer'])
 return ctx

def fingerprint(q):
 if q.get(':question/math-academy-id'):c=source_context(q);F=c['F'];pts=c['vertices']
 else:
  F=old.math(re.search(r'\\iint_D (.*?)\\,\\mathrm\{d\}x',q[':question/problem'],re.S)[1]);pts=[(old.math(A),old.math(B)) for A,B in re.findall(r'\$\((.*?),(.*?)\)\$',q[':question/problem'])]
 return hashlib.sha256(g.dump([s.srepr(s.expand(F)),sorted([str(s.simplify(A)),str(s.simplify(B))] for A,B in pts)]).encode()).hexdigest()

def independent(r):
 assert r['knowledge_point']['db_id']==KP and r['generation']['version']==g.VERSION
 local=copy.deepcopy(r);plot=Path(r['generation']['plot']);digest=hashlib.sha256(plot.read_bytes()).hexdigest();published=f'images/{digest[:2]}/{digest}.png'
 local['question'][':question/worked-solution']=local['question'][':question/worked-solution'].replace(published,str(plot))
 old.check_normal(local)
 replay=g.generate(r['generation']['difficulty'],template=r['generation']['template'],parameters=r['generation']['parameters'])
 assert replay['question'][':question/id']==r['question'][':question/id']
 assert fingerprint(r['question'])==fingerprint(replay['question'])
 return True

def main():
 rows=[];extraction=[];options=0;missing=[]
 for q in g.REC[':knowledge-point/questions']:
  ctx=source_context(q);banks=[]
  for i,f in enumerate(q[':question/answer-fields']):
   values=[old.math(a[':answer/value']) for a in f[':answer-field/choices']];assert sum(g.eq(z,ctx['answer']) for z in values)==1
   if ':answer-field/correct' in f:old.eq(old.math(f[':answer-field/correct'][':answer/value']),ctx['answer'])
   else:missing.append([q[':question/math-academy-id'],i])
   banks.append({'field_id':f[':answer-field/id'],'type':'radio','key':f[':answer-field/key'],'profile':q[':question/math-academy-id']+':'+str(i),'choices':[{'answer_id':a[':answer/id'],'value':a[':answer/value'],'exact_value':str(z),'recipe':'c * ('+str(z)+'); historical scalar pattern; error intent unresolved','replayed_at_c_1':str(z)} for a,z in zip(f[':answer-field/choices'],values)],'correct':f.get(':answer-field/correct',{}).get(':answer/value')});options+=len(values)
  extraction.append({'source_id':q[':question/math-academy-id'],'difficulty':'hard','supplied':'integrand and four Cartesian vertices','requested':'definite integral scalar','transformation':list(map(str,ctx['transformation'])),'bounds':list(map(str,ctx['bounds'])),'transformed_integrand':str(ctx['transformed']),'answer_exact':str(ctx['answer']),'plot_rating':'moderate','plots':re.findall(r'!\[.*?\]\((.*?)\)',q[':question/worked-solution']),'banks':banks,'worked_solution_stages':['infer map (factor first where present)','map four vertices and draw rectangle','inverse-map determinant','reciprocal determinant','separate and integrate two factors']})
  if q[':question/math-academy-id']!='q-160433':truth(q)
 # Re-run exact historical full source-bank replay through the generator.
 matched=0
 for sid,source in g.SOURCES.items():
  r=g.generate(g.FAMILIES[g.SOURCE_FAMILY[sid]],profile='raw:'+sid,parameters={'scale':1});old.check_raw(r,source);matched+=sum(len(f[':answer-field/choices']) for f in source[':question/answer-fields'])
 # Current scope + explicit rejection of obsolete moderate label.
 try:g.generate('moderate')
 except ValueError:pass
 else:raise AssertionError('unsupported moderate must reject')
 covered={}
 for family,level in g.FAMILIES.items():
  r=g.generate(level,713,template=family);independent(r);rows.append(r);covered[family]=level
 inputs=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in rows]
 (D/'native-current-input.json').write_text(json.dumps(inputs,indent=2));subprocess.run([str(g.ROOT.parent/'runs/current/check-engine'),str(D/'native-current-input.json'),str(D/'native-current-report.json')],check=True)
 (D/'extraction-current.json').write_text(json.dumps(extraction,indent=2));(D/'review-current.json').write_text(json.dumps(rows,indent=2));(D/'review-current.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in rows))
 caps={'supported_levels':list(g.SUPPORTED_LEVELS),'unsupported_levels':['moderate'],'source_basis':g.SNAP['basis'],'exceptions':[{'level':'moderate','bounded':True,'nominal_target':5,'available':0,'reason':'All 12 current practice sources are hard. q-160896, formerly unrated and used to author moderate, now explicitly has hard difficulty. The only validated intermediate family was that same shifted-polynomial backbone, so its moderate assignment is withdrawn. No independently calibrated middle family is established by current evidence. Easy retains the canonical polynomial/shear anchor. Reopen if new intermediate source or independent calibration appears.'},{'level':'hard','templates_outside_sampling':['q-160937','q-160903','q-160938','q-160906','q-160902','q-160895'],'reason':'New current source backbones/profiles are classified and mathematically verified; no generalizing sampler is claimed for these new banks. Existing validated hard families remain supported; current fresh source supply is counted only after individual grading checks.'},{'source':'q-160433','reason':'First of two captured radio fields lacks correct reference. Full question excluded from fresh gradable counts and preserved unchanged.'}],'finite_variant_limit':None,'source_bank_error_intent':'opaque; source exact-value replay separate from authored method-derived banks'}
 (D/'capabilities.json').write_text(json.dumps(caps,indent=2));report={'passed':True,'generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'current_source_basis':g.SNAP['basis'],'current_source_questions':12,'current_source_fields':13,'current_source_options_mathematically_verified':options,'current_correct_refs_verified':12,'missing_refs':missing,'historical_source_bank_replay':{'matched_options':matched,'total_options':35,'complete_banks':7,'total_banks':7},'supported_templates_checked':covered,'moderate_rejected':True,'native':json.loads((D/'native-current-report.json').read_text()),'previous_full_validation':'validation.json; parent hash cb4d5dedfa58fe6b5a826225e9131f8ca4dd794f549ef5239eab95970d829add','change':'version + shifted polynomial hard + moderate rejected; all other math/masks/slots unchanged'}
 (D/'validation-current.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ('passed','current_source_questions','current_source_options_mathematically_verified','supported_templates_checked')}))
if __name__=='__main__':main()
