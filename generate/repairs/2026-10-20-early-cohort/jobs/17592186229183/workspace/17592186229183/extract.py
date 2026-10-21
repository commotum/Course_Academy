"""Private source extraction: positional numeric roles within complete source blocks.
No global substring replacement: every token becomes one explicit, audited slot.
"""
import json,re,sys
import sympy as sym
from pathlib import Path
D=Path(__file__).parent
src=Path(sys.argv[1]) if len(sys.argv)>1 else D.parent.parent/'source/source.json'
capture=json.loads(src.read_text())
s=capture['material']['kp']; masks={}; cases=[]; bytes_evidence=[]
# Preserve the supplied snapshot metadata, with the legacy runtime record shape.
(D/'source.json').write_text(json.dumps({**{k:capture[k] for k in ('database','basis','lineage')},'record':s},indent=2)+'\n')
roles={4:['1','c','rin'],5:['c','rin','c','rin','A'],6:['2','v','rin','rout'],7:['v','rin','rout','d','a'],9:['d','a'],10:['rout'],11:['rout','d','a','rout','d','a','rout','d','a','n','a'],12:['3'],13:['A','n','a'],15:['n','a','A'],16:['4'],17:['n','a','n','a','a','n','a','n'],18:['a','n'],19:['a','n','n','a','a','n','A','a','n','n','a','A','a','n','a','n','A','a','n'],21:['a','n','A','a','n','a','n','A','1','np','a','np','k','a','a','n'],22:['q','0','q'],23:['0','q','k','a','0','a','0','n','q','cv','a','n','q','a','n','D','D','a','n'],25:['k','a','D','a','n','a','n','k','a','D','a','a','n'],26:['H','H'],27:['H','v','rin','rout','H','v','d','H','d','gap','to'],29:['to','k','a','to','D','a','a','to','n','cH','D','a','end','n','rounded']}
num=re.compile(r'(?<![A-Za-z])\d+(?:\.\d+)?')
def make_mask(text,rs):
 # Fractional concentration is a COMPLETE component slot, not two number slots.
 if 'c' in rs:text=re.sub(r'\\frac\{\d+\}\{\d+\}', '@CONCENTRATION@', text)
 if '@CONCENTRATION@' in text:
  text=text.replace('@CONCENTRATION@','987654321')
 matches=list(num.finditer(text));assert len(matches)==len(rs),(text,rs,len(matches))
 out='';pos=0
 for m,r in zip(matches,rs):
  out+=text[pos:m.start()]+(m.group() if r.isdigit() else '<<'+r+'>>');pos=m.end()
 return out+text[pos:]
def physical(prompt):
 vals=re.findall(r'\$(\\frac\{\d+\}\{\d+\}|\d+(?:\.\d+)?)(?:\\,)?(?:\\text\{|\\textrm\{)?(?:gal|lb)',prompt)
 assert len(vals)==6,vals
 def lexical(z):
  m=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',z)
  return m[1]+'/'+m[2] if m else z
 return dict(zip(['H','v','q','c','rin','rout'],map(lexical,vals)))
for q in s[':knowledge-point/questions']:
 sid=q[':question/math-academy-id']; p=physical(q[':question/problem']);cases.append({'source_id':sid,'template':sid,'level':'easy','difficulty_provenance':'observed' if ':question/difficulty'in q else 'authored inference for completed version only','parameters':p,'bank_profile':'observed:'+sid})
 prompt=make_mask(q[':question/problem'],['H','v','q','c','rin','rout']);sol=q.get(':question/worked-solution');sm=None
 if sol is not None:
  blocks=sol.split('$$'); pieces=[]
  for i,b in enumerate(blocks):
   rs=roles.get(i,[])
   if sid=='q-336451' and i==23:rs=['0','q','k','a','0','a','0','n','q','cv','a','n','q','D','a','n']
   if sid=='q-336451' and i==27:rs=['H','d','a','H','a','end','to']
   if sid=='q-336451' and i==29:rs=roles[29][:-4]+['reduced_num','reduced_den','n','rounded']
   pieces.append(make_mask(b,rs))
  sm='$$'.join(pieces)
 fields=[]
 for f in q[':question/answer-fields']:
  opts=[]
  for a in f[':answer-field/choices']:
   val=a[':answer/value'];m=re.match(r'([\d.]+)(.*)',val)
   opts.append({'display_suffix':m[2],'observed_numeric':m[1],'correct':f.get(':answer-field/correct',{}).get(':answer/id')==a[':answer/id']})
   pairs=[i for i in range(len(val)-1) if ord(val[i])==92 and ord(val[i+1])==92]
   if pairs:bytes_evidence.append({'source_id':sid,'value':val,'length':len(val),'adjacent_backslash_indices':pairs,'ord_values':[ord(x) for x in val]})
  fields.append({'key':f[':answer-field/key'],'has_correct':':answer-field/correct'in f,'options':opts})
 masks[sid]={'prompt':prompt,'solution':sm,'fields':fields,'has_difficulty':':question/difficulty'in q,'base':p}
(D/'masks.json').write_text(json.dumps(masks,indent=2)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(D/'decoded-byte-evidence.json').write_text(json.dumps(bytes_evidence,indent=2)+'\n')
