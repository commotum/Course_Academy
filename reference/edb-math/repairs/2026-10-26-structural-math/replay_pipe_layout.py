import collections,json,re,sys,types
from pathlib import Path
from bs4 import BeautifulSoup
R=Path.cwd();H=R/'reference/edb-math/repairs/2026-10-26-structural-math';p=H/'recover_formulas.py';ns={'__file__':str(p)};exec(compile(p.read_text().split('index=collections.defaultdict(list)')[0],str(p),'exec'),ns);MATH=ns['MATH'];formulas=ns['formulas'];roots=ns['roots']
mod=types.ModuleType('pipe_legacy_json');mod.__file__='/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py';sys.modules[mod.__name__]=mod;s=Path(mod.__file__).read_text();a=s.index('    if name == "mtable":',s.index('def mathml_to_text'));b=s.index('    if name == "mtr":',a);s=s[:a]+'''    if name == "mtable":
        return clean_math_text("; ".join(mathml_to_text(child) for child in node.children if isinstance(child, Tag)))

'''+s[b:];exec(compile(s,mod.__file__,'exec'),mod.__dict__)
md=types.ModuleType('pipe_legacy_md');md.__file__='/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py';sys.modules[md.__name__]=md;exec(compile(Path('/tmp/structural-md-prevention/legacy-md.py').read_text(),md.__file__,'exec'),md.__dict__)
canon=lambda t:re.sub(r'\s+|\\displaystyle(?![A-Za-z])','',t).strip('$')
index=collections.defaultdict(list)
for d in json.loads(Path('/tmp/structural-pipe-source-index.json').read_text()):index[d['identity'],d['attribute']].append(d)
props=json.loads(Path('/tmp/structural-pipe-proposals.json').read_text());unresolved=json.loads(Path('/tmp/structural-pipe-unresolved.json').read_text());extra=[];left=[];cache={}
for d in unresolved:
 opts=[];notes=[]
 for ident in d['identities']:
  for src in index[ident,d['attribute']]:
   if src['html']not in cache:
    nodes=roots(BeautifulSoup(src['html'],'html.parser'));fs=formulas(src['html']);assert len(nodes)==len(fs);pairs=[]
    for node,f in zip(nodes,fs):
     try:
      old=mod.extract_math_from_node(node);replay=md.normalize_math_tex(old[0])if old else None
     except Exception as ex:replay=None
     pairs.append((replay,f))
    cache[src['html']]=pairs
   pairs=cache[src['html']];changes=[]
   for m in MATH.finditer(d['before']):
    if not (re.search(r'(?<!\\)\|\s*=',m[0])and';'in m[0]and not re.search(r'\\begin\{(?:aligned|array|.*matrix)\}',m[0])):continue
    found={f for old,f in pairs if old and isinstance(f,str)and canon(old)==canon(m[0])}
    if len(found)==1:
     f=next(iter(found));changes.append({'span':[m.start(),m.end()],'before':m[0],'after':'$$\n'+f+'\n$$'if m[0].startswith('$$')else'$'+f+'$','proof':'Exact legacy MathML serialization and Markdown replay'})
   if changes:opts.append({'entity':d['entity'],'attribute':d['attribute'],'identity':ident,'source_path':src['path'],'before':d['before'],'changes':changes})
 unique={json.dumps(o['changes'],sort_keys=True):o for o in opts}
 if len(unique)==1:extra.append(next(iter(unique.values())))
 else:left.append({**d,'matching_options':len(unique)})
Path('/tmp/structural-pipe-replayed.json').write_text(json.dumps(extra,indent=2)+'\n');Path('/tmp/structural-pipe-unresolved-replayed.json').write_text(json.dumps(left,indent=2)+'\n');print('additional exact replay fields',len(extra),'blocks',sum(len(d['changes'])for d in extra),'remaining',len(left))
for d in left[:12]:print(d['entity'],d['identities'],d['matching_options'])
