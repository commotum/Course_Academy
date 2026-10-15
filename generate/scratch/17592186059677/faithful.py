"""Served source templates with whole-function common-scalar slots.

Original shared prose, mathematical row sequence and complete choice-bank profile
are immutable. At scale=1 this replays normalized original content. At scale>1
we scale every complete derivative operand and every non-operator mathematical
row, so the same linear differentiation method and source error bank survive.
Opaque distractor intent remains unknown; scaling is a mathematical mask only.
"""
import copy,re
import sympy as sp
SOURCES={'faithful_q10883':'q-10883','faithful_q10892':'q-10892','faithful_q10902':'q-10902','faithful_q28556':'q-28556','faithful_q342851':'q-342851'}
SCALES=(1,2,3,4,5,6)

def split_punctuation(value):
 match=re.search(r'([.,]+)$',value.strip());suffix=match[1] if match else ''
 return (value.strip()[:-len(suffix)] if suffix else value.strip()),suffix

def scaled(value,scale):
 if scale==1:return value
 core,punctuation=split_punctuation(value)
 return str(scale)+r'\left('+core+r'\right)'+punctuation

def formal(value,scale):
 if scale==1:return value
 core,punctuation=split_punctuation(value)
 match=re.fullmatch(r'(.*)(\^\{[′\x27]+\})',core,re.S)
 if not match:raise ValueError('source formal operator missing')
 operand=match[1]
 # Retain the captured one-derivative power and put the entire common scalar
 # inside its input. A coefficient outside the operator would conceal stale data.
 return r'\left('+str(scale)+r'\left('+operand+r'\right)\right)'+match[2]+punctuation

def mask_solution(solution,scale):
 if scale==1:return solution
 def block(match):
  body=match[1];begin=r'\begin{aligned}';end=r'\end{aligned}'
  assert begin in body and end in body
  body=body.replace(begin,'').replace(end,'');new=[]
  for row in body.split(r'\\'):
   lhs,rhs=row.split('=',1)
   # Captured stray alignment markers are presentation; retain until canonical
   # formatter handles them. Scale only actual mathematical content.
   rhs=rhs.strip();extra=''
   if rhs.endswith('&'):rhs=rhs[:-1].strip();extra=' &'
   suffix=''
   if rhs.endswith(r'\,.'):rhs=rhs[:-3];suffix=r'\,.'
   elif rhs.endswith(r'\,'):rhs=rhs[:-2];suffix=r'\,'
   transform=formal if re.search(r'\^\{[′\x27]+\}[.,]?$',rhs.strip()) else scaled
   new.append(lhs+'= '+transform(rhs,scale)+suffix+extra)
  return '$$'+begin+r'\\'.join(new)+end+'$$'
 return re.sub(r'\$\$(.*?)\$\$',block,solution,flags=re.S)

def render(g,template,level,seed,parameters,field_type):
 sid=SOURCES[template];source=g.ORIGINALS[sid];source_level=source[':question/difficulty'][':db/ident'].split('/')[-1]
 if level!=source_level:raise ValueError('source template/difficulty mismatch')
 kind=source[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
 if field_type not in [None,kind,':answer-field.type/'+kind]:raise ValueError('source field contract')
 if set(parameters)!={'scale'} or type(parameters['scale']) is not int or parameters['scale'] not in SCALES:raise ValueError('faithful common-scalar domain1–6')
 scale=parameters['scale']
 def inline(match):
  math=match[1];function=re.match(r'([fg]\(x\)\s*=\s*)(.*)',math,re.S)
  return '$'+(function[1]+scaled(function[2],scale) if function else math)+'$'
 prompt=re.sub(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',inline,source[':question/problem'],flags=re.S)
 solution=mask_solution(source[':question/worked-solution'],scale)
 prompt=g._fmt.normalize_prose(prompt);solution=g._fmt.normalize_prose(solution)
 old_field=source[':question/answer-fields'][0];bank=[g._fmt.normalize_tex(scaled(a[':answer/value'],scale)) for a in old_field[':answer-field/choices']]
 correct=g._fmt.normalize_tex(scaled(old_field[':answer-field/correct'][':answer/value'],scale))
 identity=g.digest([g.VERSION,'faithful-source-template',sid,prompt,solution,sorted(bank),correct]);fid=g.uid(identity+'/field')
 choices=[{':answer/id':g.uid(fid+'/'+value),':answer/type':':answer.type/math',':answer/value':value} for value in bank]
 field={':answer-field/id':fid,':answer-field/key':old_field[':answer-field/key'],':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',g.uid(fid+'/'+correct)]}
 original_parameters=copy.deepcopy(g.SOURCE_PARAMETERS[sid]);point=original_parameters.get('t')
 function_text=re.search(r'[fg]\(x\)\s*=\s*([^$]+)',prompt)[1].strip().rstrip('.')
 # Fingerprinting is derived from rendered prompt through the private reader.
 # This avoids counting a faithful bank and an authored bank on the same function
 # as two independent mathematical tasks.
 from importlib.util import spec_from_file_location,module_from_spec
 ps=spec_from_file_location('faithful_fingerprint_reader',g.ROOT/'readback.py');reader=module_from_spec(ps);ps.loader.exec_module(reader)
 expr=reader.parse(function_text)
 record={'knowledge_point':{'db_id':g.KP_ID,'id':g.KP[':knowledge-point/id'],'title':g.KP[':knowledge-point/title']},'question':{':question/id':g.uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':g.VERSION,'level':level,'seed':seed,'template':template,'profile':'source_faithful','bank_profile':sid+'_complete_observed_bank','bank_recipes':['common scalar times complete observed value: '+a[':answer/value'] for a in old_field[':answer-field/choices']],'parameters':dict(parameters),'original_parameters':original_parameters,'source_id':sid,'source_ids':[sid],'domain':'x>0' if 'sqrt' in function_text else 'all real x','source':{k:g.SOURCE[k] for k in ['database','basis','lineage']},'origin':'faithful served source template; common-scalar extension' if scale!=1 else 'faithful served source template at original parameters','evidence_only':False,'eligible_for_learning':True,'relationship_to_source_templates':'Complete original prompt/layout, source shared prose, ordered rows/operators, field contract and complete observed bank; whole-function scalar is the only slot. Original evaluation target retained in this source-bank mask; independently authored templates vary eligible targets.','mathematical_fingerprint':g.digest(['function',str(sp.expand(expr)),point]),'content_fingerprint':identity}}
 return g._fmt.validate_generated_record(record)
