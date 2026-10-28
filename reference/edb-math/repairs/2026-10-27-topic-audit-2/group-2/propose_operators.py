import json,re
from pathlib import Path
H=Path(__file__).resolve().parent;src=json.loads((H/'sources.json').read_text());out=[]
pattern=re.compile(r'(?<![A-Za-z])\{(sin|cos|tan|sec|csc|cot|ln|log|exp)\}(?=\s*\^)')
for e,a,v,ident,bare in json.loads((H/'fields.json').read_text()):
 if not pattern.search(v):continue
 after=pattern.sub(lambda m:r'\operatorname{'+m[1]+'}',v)
 evidence={'source_identity':ident,'source_archives_or_captures':sorted({s['path']for s in src if s['identity']==ident}),'retained_function_application_marker':'⁡'in v,'source_shape':'Powered mi operator followed by U+2061 function application; power belongs to function result. Independent derivative/integral context confirms operator role.'}
 assert evidence['retained_function_application_marker'],(e,a)
 out.append({'entity':e,'attribute':a,'before':v,'after':after,'reason':'Preserve powered trigonometric function operator, replacing italic letter product produced by importer missing enclosing-msup function application','evidence':evidence,'confidence':'high'})
(H/'operator-proposals.json').write_text(json.dumps(out,indent=2)+'\n');print('operators',len(out))
