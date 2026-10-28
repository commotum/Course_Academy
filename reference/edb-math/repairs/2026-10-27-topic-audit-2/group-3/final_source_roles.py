import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ns={'__file__':str(H/'prepare_source_proposals.py')};exec((H/'prepare_source_proposals.py').read_text().split('options=collections.defaultdict(dict)')[0],ns);F,S,MATH=ns['F'],ns['S'],ns['MATH'];props={(r['entity'],r['attribute']):r for r in json.loads((H/'proposals.json').read_text())};source=collections.defaultdict(list)
for r in S:source[r['entity'],r['attribute']].append(r)
def core(t):return re.sub(r'\\(?:[,;:! ]|left|right)\s*','',ns['core'](t))
changes=[]
for key,rs in source.items():
 before=F[key]['value'];text=props.get(key,{}).get('after',before);matches=list(MATH.finditer(text));replacements={}
 for i,m in enumerate(matches):
  old=ns['mathvalues'](m[0])[0];candidates={new for r in rs for new in r['formulas']if core(old)==core(new)and ns['role_missing'](old,new)}
  if len(candidates)==1:replacements[i]=next(iter(candidates))
 if not replacements:continue
 for i in reversed(sorted(replacements)):
  m=matches[i];text=text[:m.start()]+('$$\n'+replacements[i]+'\n$$'if m[0].startswith('$$')else'$'+replacements[i]+'$')+text[m.end():]
 ns['validate_math_structure'](text,bare_math=F[key]['bare']);oldprop=props.get(key,{});props[key]={'entity':key[0],'attribute':key[1],'before':before,'after':text,'reason':oldprop.get('reason','Recover retained source mathematical fonts and visible set braces.')+' Recover equivalent source roles across harmless spacing commands.','evidence':{**oldprop.get('evidence',{}),'spacing_equivalent_source_role_formulas':list(replacements),'source_paths':sorted({r['path']for r in rs})},'confidence':'high'};changes.append({'entity':key[0],'attribute':key[1],'indices':list(replacements)})
(H/'proposals.json').write_text(json.dumps(list(props.values()),indent=2));(H/'source-final-role-evidence.json').write_text(json.dumps(changes,indent=2));print('source roles additionally restored',len(changes),'total',len(props))
