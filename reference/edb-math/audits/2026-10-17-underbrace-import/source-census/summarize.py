import sys
sys.dont_write_bytecode=True
import collections, csv, html, json, pathlib, re
from bs4 import BeautifulSoup

P=pathlib.Path('/tmp/underbrace-source-census-agent')
rows=json.loads((P/'normalized.json').read_text());orig=json.loads((P/'original-html.json').read_text())
bad=[r for r in rows if r['literal_accents']]
items={}
for r in bad:
    key=(r['topic_id'],r['path'][2])
    if key not in items:
        items[key]={k:r[k] for k in ['file','topic_id','title','item_type','step_type','step_id','content_id','question_id']}
        items[key]['item_index']=r['path'][2]
        items[key]['source_identity']=(('q-'+str(r['question_id'])) if r['item_type']=='question' else ('e-'+str(r['content_id'])) if r['step_type']=='example' else ('tutorial-'+str(r['content_id'])))
        items[key]['leaf_paths']=[];items[key]['counts']=collections.Counter()
    items[key]['leaf_paths'].append(r['path']);items[key]['counts'].update(r['literal_accents'])

source_by_dom=collections.Counter()
for r in orig:
    source_by_dom[(r['topic_id'],r['dom_ancestors'][0],r['kind'])]+=1
normalized_by_dom=collections.Counter()
outside_math=[];bad_not_subsup=[]
for r in bad:
    dom=('question-'+r['question_id']) if r['item_type']=='question' else ('step-'+r['step_id'])
    for k,v in r['literal_accents'].items(): normalized_by_dom[(r['topic_id'],dom,k)]+=v
    soup=BeautifulSoup(r['text'],'html.parser')
    for span in soup.find_all('span',class_='math'):span.decompose()
    if any(c in str(soup) for c in '⏟⏞'):outside_math.append(r['path'])
    leftovers=re.sub(r'\_\(⏟\)|\^\(⏞\)','',r['text'])
    if any(c in leftovers for c in '⏟⏞'):bad_not_subsup.append(r['path'])

assert source_by_dom==normalized_by_dom, list((source_by_dom-normalized_by_dom).items())[:10]
assert not outside_math
assert not bad_not_subsup
assert all(r['parent_tag']==('munder' if r['kind']=='underbrace' else 'mover') for r in orig)
assert all(r['math_source'] for r in orig)

alternates={c:[] for c in '⎵⎴⏝⏜︷︸'}
for p in pathlib.Path('/home/jake/Developer/MA/DATA/Lessons').glob('*/Source/*'):
    if p.suffix not in ('.json','.html') or p.stem!=p.parent.parent.name:continue
    s=p.read_text()
    if p.suffix=='.json':s=json.dumps(json.loads(s),ensure_ascii=False)
    s=html.unescape(s)
    for c in alternates:
        if c in s:alternates[c].append(str(p))

item_rows=list(items.values())
for r in item_rows:r['counts']=dict(r['counts'])
(P/'affected-source-items.json').write_text(json.dumps(item_rows,ensure_ascii=False,indent=2)+'\n')
with (P/'affected-source-items.tsv').open('w') as f:
    w=csv.writer(f,delimiter='\t');w.writerow(['topic_id','title','source_identity','item_type','step_type','step_id','content_id','question_id','underbrace_count','overbrace_count','normalized_leaf_count','json_path','leaf_paths'])
    for r in item_rows:w.writerow([r['topic_id'],r['title'],r['source_identity'],r['item_type'],r['step_type'],r['step_id'],r['content_id'],r['question_id'],r['counts'].get('underbrace',0),r['counts'].get('overbrace',0),len(r['leaf_paths']),r['file'],json.dumps(r['leaf_paths'])])

verification={'all620_bad_occurrences_match_original_mathml_by_topic_item_and_accent':True,'all_bad_glyphs_within_normalized_math_spans':True,'all_bad_glyphs_have_ascii_sub_or_super_script_form':True,'all_original_glyphs_are_mathml_munder_or_mover_accents':True,'alternate_glyph_search_files':5928,'alternate_glyph_hits':alternates,'affected_items':len(item_rows),'affected_item_type_counts':dict(collections.Counter(('practice_question' if r['item_type']=='question' else r['step_type']) for r in item_rows)),'items_multiple_affected_leaves':sum(len(r['leaf_paths'])>1 for r in item_rows),'additional_affected_leaves_beyond_one_per_item':sum(len(r['leaf_paths'])-1 for r in item_rows),'proper_command_rows':sum(bool(r['proper_commands']) for r in rows),'proper_command_topics':len({r['topic_id'] for r in rows if r['proper_commands']}),'mixed_literal_and_proper_leaf_rows':[{'topic_id':r['topic_id'],'path':r['path']} for r in rows if r['literal_accents'] and r['proper_commands']]}
(P/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(verification,ensure_ascii=False,indent=2))
