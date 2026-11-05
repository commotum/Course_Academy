import sys as _archive_sys
from pathlib import Path as _ArchivePath
_archive_sys.path.insert(0, str(_ArchivePath(__file__).resolve().parents[5] / 'scripts'))
from archive_json import read_text as read_archive_text, write_text as write_archive_text, exists as archive_exists
import json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH
p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';ns={'__file__':str(p)};s=p.read_text();exec(compile(s.split('parents=json.loads')[0]+s[s.index('def roots(s):'):s.index('def visible(tex):')],str(p),'exec'),ns)
ss=json.loads((read_archive_text(H/'sources.json')));out=[]
for s in ss:
 if s['attribute']!='question/problem'or not any(name in s['html']for name in ['freeResponseTextbox','selectList']):continue
 r=ns['CompleteSourceRenderer'](None)
 try:
  rendered=r.text(BeautifulSoup(s['html'],'html.parser'),True)
  fs=[]
  for m in MATH.finditer(rendered):
   k=2 if m[0].startswith(('$$',r'\[',r'\('))else 1;fs.append(m[0][k:-k].strip())
  if r.errors:raise ValueError(str(r.errors))
  if r.fields:
   s.setdefault('uncontrolled_formula_stream',s['formulas']);s['formulas']=fs;s['observed_control_text']=rendered;s['observed_controls']=r.fields;s['formula_stream_kind']='Actual observed input/select control slots retained; historical entered/default option formulas excluded from visible problem formula stream.'
   out.append({'identity':s['identity'],'path':s['path'],'control_keys':[f['key']for f in r.fields],'problem':rendered,'fields':r.fields,'errors':[]})
 except Exception as ex:out.append({'identity':s['identity'],'path':s['path'],'error':str(ex)})
(write_archive_text(H/'sources.json', json.dumps(ss,indent=2)+'\n'));(H/'source-control-reconstructions.json').write_text(json.dumps(out,indent=2)+'\n');print('original prompt input streams',len(out),'success',sum(not o.get('error')for o in out),'errors',[(o['identity'],o.get('error'))for o in out if o.get('error')])
