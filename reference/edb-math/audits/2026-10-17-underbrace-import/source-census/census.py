import sys
sys.dont_write_bytecode=True
import collections, html, json, pathlib, re, time
from bs4 import BeautifulSoup

ROOT=pathlib.Path('/home/jake/Developer/MA/DATA/Lessons')
OUT=pathlib.Path('/tmp/underbrace-source-census-agent')
CHARS={'⏟':'underbrace','⏞':'overbrace','⎵':'underbracket','⎴':'overbracket','⏝':'underparen','⏜':'overparen'}
PAT=re.compile('|'.join(map(re.escape,CHARS)))
COUNTERS=collections.Counter()
normalized=[]; originals=[]; errors=[]; totals=collections.Counter()

def leaves(x,path=()):
    if isinstance(x,dict):
        for k,v in x.items(): yield from leaves(v,path+(k,))
    elif isinstance(x,list):
        for i,v in enumerate(x): yield from leaves(v,path+(i,))
    elif isinstance(x,str): yield path,x

for p in sorted(ROOT.glob('*/Source/*.json')):
    if p.stem!=p.parent.parent.name: continue
    totals['json_files']+=1
    try: d=json.loads(p.read_text())
    except Exception as e: errors.append({'path':str(p),'error':str(e)});continue
    title=d.get('topic_title');topic=d.get('topic_id')
    for path,s in leaves(d):
        if not path or path[-1]!='normalized_html': continue
        literal={CHARS[c]:s.count(c) for c in CHARS if c in s}
        explicit={name:len(re.findall(r'\\'+name+r'\b',s)) for name in CHARS.values() if re.search(r'\\'+name+r'\b',s)}
        if not literal and not explicit:continue
        item={}
        if len(path)>2 and path[0:2]==('lesson','items'):item=d['lesson']['items'][path[2]]
        row={'file':str(p),'topic_id':topic,'title':title,'path':list(path),'item_type':item.get('item_type'),'step_type':item.get('step_type'),'step_id':item.get('step_id'),'content_id':item.get('content_id'),'question_id':item.get('question_id'),'literal_accents':literal,'proper_commands':explicit,'text':s}
        normalized.append(row)
    hp=p.with_suffix('.html')
    if not hp.exists(): totals['missing_html']+=1;continue
    totals['html_files']+=1
    hs=hp.read_text()
    if not PAT.search(html.unescape(hs)):continue
    soup=BeautifulSoup(hs,'html.parser')
    for mo in soup.find_all('mo'):
        ch=mo.get_text().strip()
        if ch not in CHARS:continue
        par=mo.parent
        math=mo.find_parent('math')
        dom=[]
        for anc in mo.parents:
            if anc.get('id') and re.match(r'(?:step|question|kp)-',anc.get('id')):dom.append(anc['id'])
        outer=par
        if par.name in ('munder','mover','munderover'):
            while outer.parent and outer.parent.name in ('mrow','mstyle','munder','mover','munderover'):
                outer=outer.parent
        originals.append({'file':str(hp),'topic_id':topic,'title':title,'kind':CHARS[ch],'glyph':ch,'parent_tag':par.name,'parent_attrs':par.attrs,'dom_ancestors':dom,'mathml':str(outer),'math_source':str(math) if math else None})

summary={'totals':dict(totals),'errors':errors,'normalized_attribute_rows':len(normalized),'normalized_topics':len(set(x['topic_id'] for x in normalized)), 'normalized_literal_rows':sum(bool(x['literal_accents']) for x in normalized),'normalized_literal_topics':len(set(x['topic_id'] for x in normalized if x['literal_accents'])),'normalized_literal_occurrences':dict(sum((collections.Counter(x['literal_accents']) for x in normalized),collections.Counter())),'normalized_proper_command_occurrences':dict(sum((collections.Counter(x['proper_commands']) for x in normalized),collections.Counter())),'original_html_occurrences':len(originals),'original_html_topics':len(set(x['topic_id'] for x in originals)),'original_html_kinds':dict(collections.Counter(x['kind'] for x in originals)),'original_parent_tags':dict(collections.Counter(x['parent_tag'] for x in originals))}
for name,obj in [('normalized.json',normalized),('original-html.json',originals),('summary.json',summary)]:
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,indent=2))
