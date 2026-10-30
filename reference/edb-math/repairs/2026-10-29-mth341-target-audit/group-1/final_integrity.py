import collections,importlib.util,json,re,sys
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import validate_math_structure,validate_tex
spec=importlib.util.spec_from_file_location('gm',H/'math_verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);qs=json.loads((H/'proposed-questions.json').read_text());render=json.loads((H/'all-render-input.json').read_text());errors=[];banks=[]
for r in render:
 try:validate_tex(r['value'])if r.get('bare_math')else validate_math_structure(r['value'])
 except Exception as ex:errors.append({'entity':r['entity'],'attribute':r['attribute'],'error':str(ex)})
for q in qs:
 for f in q.get(':question/answer-fields',[]):
  assert f[':answer-field/correct'][':db/id']in[a[':db/id']for a in f[':answer-field/choices']]
  values=[a[':answer/value']for a in f[':answer-field/choices']];assert len(set(values))==len(values),(q[':db/id'],values)
  if not f[':answer-field/type'][':db/ident'].endswith('radio'):continue
  right=next(a for a in f[':answer-field/choices']if a[':db/id']==f[':answer-field/correct'][':db/id']);v=right[':answer/value'];mm=m.mats(v)
  try:
   if mm and len(mm)==1 and r'\{'not in v and not mm[0][2].free_symbols:
    target=mm[0][2];same=[a[':db/id']for a in f[':answer-field/choices']if len(m.mats(a[':answer/value']))==1 and m.mats(a[':answer/value'])[0][2]==target and r'\{'not in a[':answer/value']]
   elif not mm and not any(x in v for x in ['{','\\text','\\operatorname','$','Undefined','invertible','Invertible']):
    target=m.scalar(v);same=[]
    for a in f[':answer-field/choices']:
     try:actual=m.scalar(a[':answer/value'])
     except Exception:continue
     if isinstance(actual,S.Expr)and S.simplify(actual-target)==0:same.append(a[':db/id'])
   else:continue
   assert same==[right[':db/id']],(q[':db/id'],same,right[':db/id']);banks.append({'entity':q[':db/id'],'field':f[':db/id'],'canonical_equivalent_options':same,'passed':True})
  except Exception as ex:errors.append({'entity':q[':db/id'],'check':'semantic bank uniqueness','error':str(ex)})
(H/'final-integrity.json').write_text(json.dumps({'passed':not errors,'strict_math_structure_fields':len(render),'all_active_banks_have_distinct_literal_values':True,'exact_numeric_scalar_vector_bank_uniqueness_checks':banks,'errors':errors},indent=2)+'\n');print('Integrity fields',len(render),'numeric/vector banks',len(banks),'errors',len(errors));assert not errors,errors
