"""Offline extraction of complete-component masks and observational profiles."""
import json,re,copy
from pathlib import Path
import sympy as S
R=Path(__file__).resolve().parent
source=json.loads((R/'source.json').read_text());qs=source['record'][':knowledge-point/questions'];ts={};ps={};cases=[];maps=[]
def parse(text):
 # Convert only numerical arithmetic source fragments (not arbitrary TeX).
 def conv(s):
  out='';i=0
  while i<len(s):
   if s.startswith('\\frac',i) or s.startswith('\\sqrt',i):
    op='frac' if s.startswith('\\frac',i) else 'sqrt';i+=5
    def take(j):
     assert s[j]=='{';d=1;k=j+1
     while d:
      d+=(s[k]=='{')-(s[k]=='}');k+=1
     return s[j+1:k-1],k
    a,i=take(i)
    if op=='frac':b,i=take(i);out+='(('+conv(a)+')/('+conv(b)+'))'
    else:out+='sqrt('+conv(a)+')'
   else:out+=s[i];i+=1
  return out
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 return parse_expr(conv(text),transformations=standard_transformations+(implicit_multiplication_application,))
def vals(q):return {a:tuple(map(int,x.split(','))) for a,x in re.findall(r'([A-Z])\(([-\d, ]+)\)',q[':question/problem'])}
for q in qs:
 sid=q[':question/math-academy-id'];p={'vertices':{k:list(v) for k,v in vals(q).items()}};sol=q.get(':question/worked-solution');f=q[':question/answer-fields'][0];field=f[':answer-field/type'][':db/ident'].split('/')[-1]
 if sol:
  bs=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);edges=re.findall(r'\\overset\{\\to \}\{([A-Z]{2})\}',bs[1]);base=re.search(r'\\cdot ([A-Z]{2})',bs[0])[1];alt=re.search(r'([A-Z]{2})\\cdot ',bs[0])[1]
 else:
  edges=['PQ','PR'];base='PQ';alt='RH';bs=[]
  # Source has no teaching solution; reconstruct the common full seven-block
  # solution from q-20027 using complete symbolic names only.
  sol=qs[0][':question/worked-solution']
  for old,new in [('ABC','PRQ'),('AB','PQ'),('AC','PR'),('CH','RH')]:sol=sol.replace(old,new)
  bs=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
 t={'level':'hard','field':field,'key':f[':answer-field/key'],'edges':edges,'base':base,'alt':alt,'source_ids':[sid],'authorship':'observed' if q.get(':question/worked-solution') else 'observed prompt/bank; authored hard assignment and solution'}
 # Preserve every source paragraph and its placement; dynamic blocks are complete
 # mathematical components, with original punctuation/row masks retained.
 idx=[0]
 def blockslot(m):n=idx[0];idx[0]+=1;return '$$\n@BLOCK'+str(n)+'@\n$$'
 t['solution']=re.sub(r'\$\$\n(.*?)\n\$\$',blockslot,sol,flags=re.S)
 prompt=q[':question/problem'];styles={}
 def coordslot(m):
  name,body=m.groups();parts=body.split(',');styles[name]=[x[len(x.rstrip()):] for x in parts]
  # Whitespace belongs before each number in source tuples.
  styles[name]=['']*3
  return name+'(@'+name+'@)'
 t['prompt']=re.sub(r'([A-Z])\(([-\d, ]+)\)',coordslot,prompt);t['coordinate_styles']=styles
 t['coordinate_prefixes']={name:[re.match(r'\s*',x)[0] for x in body.split(',')] for name,body in re.findall(r'([A-Z])\(([-\d, ]+)\)',prompt)}
 t['initial']=bs[0]
 # Source masks retain optional arithmetic rows independently of simplification.
 t['cross_raw']=len(re.findall(r' & =',bs[3]))==4;t['base_raw']=len(re.findall(r' & =',bs[5]))==4
 t['base_punct']='.' if bs[5].endswith('.\\end{aligned}') else ''
 t['area_prefix']=r'{A}_{△}=\frac{1}{2}A=';t['area_simplify']=bs[4].count('=')==3
 t['final_mode']='short' if len(re.split(r' \\\\ ',bs[6]))==3 else 'full'
 t['final_empty']=bool(re.search(r' \\\\  & =[^&]+\.\\end',bs[6]));t['reversed_reduced']=sid=='q-316409'
 t['formal_altspace']=r'\,' if sid in ('q-316392','q-316395') else ''
 t['alt_space']=r'\,' if sid in ('q-316392','q-316395','q-316409') else ''
 t['edge_zeros']=[[],[]];t['cross_zeros']=[]
 if sid=='q-316553':t['edge_zeros'][0]=['k']
 if sid=='q-316400':t['cross_zeros']=['i']
 # Each displayed determinant product records its operand order and dot style.
 row=re.search(r' & =(\(.*\)k) \\\\ ',bs[2])[1];terms=re.findall(r'\((.*?)\)([ijk])(?=[-+]|$)',row)
 u=S.Matrix(p['vertices'][edges[0][1]])-S.Matrix(p['vertices'][edges[0][0]]);v=S.Matrix(p['vertices'][edges[1][1]])-S.Matrix(p['vertices'][edges[1][0]])
 # Sources q-316xxx commonly order u_z*v_y, others v_y*u_z.
 t['swap']=[sid not in ('q-316392','q-316395','q-316400','q-316409','q-316553','q-316556','q-316558')]*3
 t['implicit']=[sid=='q-316558',sid=='q-316558',False]
 ts[sid]=t
 N=S.sqrt(u.cross(v).dot(u.cross(v)));b=S.Matrix(p['vertices'][base[1]])-S.Matrix(p['vertices'][base[0]]);h=N/S.sqrt(b.dot(b))
 profile='observed_'+sid if field=='radio' else 'none'
 if field=='radio':
  values=[parse(x[':answer/value']) for x in f[':answer-field/choices']];ratios=[str(S.simplify(x/h)) for x in values]
  ps[profile]={'template':sid,'ratios':ratios,'interpretation':'Parameterized scalar pattern h*r; observational only; error intent underdetermined','source_id':sid}
  maps.append({'source_id':sid,'template':sid,'profile':profile,'field_key':f[':answer-field/key'],'source_field_id':f[':answer-field/id'],'choices':[{'source_answer_id':a[':answer/id'],'value':a[':answer/value'],'recipe':'h*('+r+')','correct_designation_observed':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')} for a,r in zip(f[':answer-field/choices'],ratios)]})
 if field=='blank':maps.append({'source_id':sid,'template':sid,'profile':'none','field_key':f[':answer-field/key'],'source_field_id':f[':answer-field/id'],'choices':[{'source_answer_id':x[':answer/id'],'value':x[':answer/value'],'recipe':'crossnorm/base_norm','correct_designation_observed':True} for x in f[':answer-field/choices']]})
 cases.append({'source_id':sid,'source_db_id':q[':db/id'],'template':sid,'level':'hard','parameters':p,'bank_profile':profile,'authored_level_assignment':sid=='q-20028','missing_correct_ref':':answer-field/correct' not in f})
# Easy/moderate/hard use the observed common complete method with neutral names.
for level in ('easy','moderate','hard'):
 for field in ('radio','blank'):
  t=copy.deepcopy(ts['q-20027']);t.update(level=level,field=field,key='field-1' if field=='blank' else 'selection',source_ids=['e-4346'],authorship='authored '+level+' extension');t['cross_raw']=True;t['base_raw']=True;t['area_simplify']=True
  t['prompt']='Calculate the length of the altitude $CH$ of the $△\\,ABC$, if $A(@A@)$, $B(@B@)$, $C(@C@).$'+('\n\n$CH=${{field-1}}' if field=='blank' else '')
  t['coordinate_styles']={x:['','',''] for x in 'ABC'};t['coordinate_prefixes']={x:['','',''] for x in 'ABC'};ts['authored_'+level+'_'+field]=t
for name,data in [('templates',ts),('profiles',ps),('source-cases',cases),('choice-map',maps)]: (R/(name+'.json')).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print(len(ts),'templates',len(ps),'observed banks',len(cases),'source cases')
