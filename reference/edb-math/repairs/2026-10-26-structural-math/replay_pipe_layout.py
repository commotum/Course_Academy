import collections,json,re,sys,types
from pathlib import Path
from bs4 import BeautifulSoup
R=Path.cwd();H=R/'reference/edb-math/repairs/2026-10-26-structural-math';p=H/'recover_formulas.py';ns={'__file__':str(p)};exec(compile(p.read_text().split('index=collections.defaultdict(list)')[0],str(p),'exec'),ns);MATH=ns['MATH'];formulas=ns['formulas'];roots=ns['roots']
mod=types.ModuleType('pipe_legacy_json');mod.__file__='/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py';sys.modules[mod.__name__]=mod;s=(H/'external-json-replay-base.py').read_text();a=s.index('    if name == "mtable":',s.index('def mathml_to_text'));b=s.index('    if name == "mtr":',a);s=s[:a]+'''    if name == "mtable":
        return clean_math_text("; ".join(mathml_to_text(child) for child in node.children if isinstance(child, Tag)))

'''+s[b:]
s=s.replace('''            if re.fullmatch(r"0(?:\\.0+)?(?:[A-Za-z%]+)?", node.get("linethickness", "")):
                return r"\\genfrac{}{}{0pt}{}{" + numerator + "}{" + denominator + "}"
''','')
a=s.index('    for title in node.find_all("title"):',s.index('def extract_math_from_node'));b=s.index('    math_node: Tag | None = None',a);s=s[:a]+s[b:]
exec(compile(s,mod.__file__,'exec'),mod.__dict__)
md=types.ModuleType('pipe_legacy_md');md.__file__='/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py';sys.modules[md.__name__]=md;exec(compile((H/'external-legacy-md.py').read_text(),md.__file__,'exec'),md.__dict__)
from question_capture.math_format import normalize_limit_operators
def canon(t):
 t=normalize_limit_operators(t).replace('→',r'\to ').replace('∞',r'\infty')
 t=re.sub(r'\\(?:displaystyle|left|right|big|Big|bigg|Bigg)(?![A-Za-z])','',t)
 return re.sub(r'\s+','',t).strip('$').rstrip('.')
index=collections.defaultdict(list)
for d in json.loads(Path('/tmp/structural-pipe-source-index.json').read_text()):index[d['identity'],d['attribute']].append(d)
props=json.loads(Path('/tmp/structural-pipe-proposals.json').read_text());targets=json.loads(Path('/tmp/structural-pipe-extended.json').read_text());meta=json.loads((R/'.local/edb/structural-math-2026-10-26/metadata.json').read_text());base={(d['entity'],d['attribute']):d for d in props};extra=[];left=[];cache={}
for d in targets:
 ident='tutorial:'+str(meta[str(d['e'])].get('tutorial/math-academy-id'))if d['a']=='tutorial/content'else meta[str(d['e'])].get('question/math-academy-id');chosen={tuple(c['span']):c for c in base.get((d['e'],d['a']),{}).get('changes',[])};provenance=[]
 for m in MATH.finditer(d['v']):
  if m[0]not in d['suspicious_math']or(m.start(),m.end())in chosen:continue
  options={};possible=[]
  for src in index[ident,d['a']]:
   if src['html']not in cache:
    nodes=roots(BeautifulSoup(src['html'],'html.parser'));fs=formulas(src['html']);assert len(nodes)==len(fs);pairs=[]
    for node,f in zip(nodes,fs):
     try:
      old=mod.extract_math_from_node(node);replay=md.normalize_math_tex(old[0])if old else None
     except Exception as ex:replay=None
     pairs.append((replay,f))
    cache[src['html']]=pairs
   pairs=cache[src['html']]
   for old,f in pairs:
    if old and isinstance(f,str)and canon(old)==canon(m[0]):options[f]=src['path']
   stored=list(MATH.finditer(d['v']))
   if len(stored)==len(pairs):
    i=next(i for i,other in enumerate(stored)if other.start()==m.start());old,f=pairs[i];possible.append({'source_path':src['path'],'source_tex':f,'legacy_replay':old,'basis':'Same source identity, attribute, formula count and formula position'})
  if len(options)==1:
   f,path=next(iter(options.items()));chosen[m.start(),m.end()]={'span':[m.start(),m.end()],'before':m[0],'after':'$$\n'+f+'\n$$'if m[0].startswith('$$')else'$'+f+'$','proof':'Source-bound legacy serialization replay; comparison normalizes operator spellings, delimiter sizing, whitespace and final punctuation','source_path':path};provenance.append(path)
  else:left.append({'entity':d['e'],'attribute':d['a'],'identity':ident,'span':[m.start(),m.end()],'before':m[0],'matching_options':len(options),'position_candidates':possible})
 if chosen:extra.append({'entity':d['e'],'attribute':d['a'],'identity':ident,'source_path':base.get((d['e'],d['a']),{}).get('source_path')or(provenance[0]if provenance else None),'before':d['v'],'changes':sorted(chosen.values(),key=lambda c:c['span'])})
Path('/tmp/structural-pipe-combined.json').write_text(json.dumps(extra,indent=2)+'\n');Path('/tmp/structural-pipe-unresolved-final.json').write_text(json.dumps(left,indent=2)+'\n');print('combined fields',len(extra),'blocks',sum(len(d['changes'])for d in extra),'remaining blocks',len(left),'remaining fields',len({(d['entity'],d['attribute'])for d in left}))
for d in left[:6]:print(d['entity'],d['identity'],len(d['position_candidates']))
