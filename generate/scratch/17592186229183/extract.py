"""Private source extraction: positional numeric roles within complete source blocks.
No global substring replacement: every token becomes one explicit, audited slot.
"""
import json,re,shutil
from pathlib import Path
D=Path(__file__).parent
src=Path('generate/runs/current/sources/17592186229183.json')
shutil.copyfile(src,D/'source.json')
s=json.loads(src.read_text())['record']; masks={}; cases=[]; bytes_evidence=[]
PARAMS=[(300,180,54,'0.8',6,4),(210,120,30,'0.5',9,6),(210,70,20,'0.5',21,14),(150,75,25,'2/3',9,6),(200,50,10,'0.8',15,10),(180,100,20,'0.6',15,10),(160,100,25,'1.0',6,4)]
roles={4:['1','c','rin'],5:['c','rin','c','rin','A'],6:['2','v','rin','rout'],7:['v','rin','rout','d','a'],9:['d','a'],10:['rout'],11:['rout','d','a','rout','d','a','rout','d','a','n','a'],12:['3'],13:['A','n','a'],15:['n','a','A'],16:['4'],17:['n','a','n','a','a','n','a','n'],18:['a','n'],19:['a','n','n','a','a','n','A','a','n','n','a','A','a','n','a','n','A','a','n'],21:['a','n','A','a','n','a','n','A','1','np','a','np','k','a','a','n'],22:['q','0','q'],23:['0','q','k','a','0','a','0','n','q','cv','a','n','q','a','n','D','D','a','n'],25:['k','a','D','a','n','a','n','k','a','D','a','a','n'],26:['H','H'],27:['H','v','rin','rout','H','v','d','H','d','gap','to'],29:['to','k','a','to','D','a','a','to','n','cH','D','a','end','n','rounded']}
num=re.compile(r'(?<![A-Za-z])\d+(?:\.\d+)?')
def make_mask(text,rs):
 # Fractional concentration is a COMPLETE component slot, not two number slots.
 text=text.replace(r'\frac{2}{3}','@CONCENTRATION@')
 if '@CONCENTRATION@' in text:
  text=text.replace('@CONCENTRATION@','987654321')
 matches=list(num.finditer(text));assert len(matches)==len(rs),(text,rs,len(matches))
 out='';pos=0
 for m,r in zip(matches,rs):
  out+=text[pos:m.start()]+(m.group() if r.isdigit() else '<<'+r+'>>');pos=m.end()
 return out+text[pos:]
for q,vals in zip(s[':knowledge-point/questions'],PARAMS):
 sid=q[':question/math-academy-id']; p=dict(zip(['H','v','q','c','rin','rout'],vals));cases.append({'source_id':sid,'template':sid,'level':'easy','difficulty_provenance':'observed' if ':question/difficulty'in q else 'authored inference for completed version only','parameters':p,'bank_profile':'observed:'+sid})
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
widget=json.load(open('/home/jake/Developer/MA/DATA/Lessons/6700/Source/6700.json'))
(D/'widget-context.json').write_text(json.dumps(widget,indent=2)+'\n')
