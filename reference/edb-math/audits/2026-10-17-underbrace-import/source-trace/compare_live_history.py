import json,re,hashlib
from pathlib import Path
O=Path('/tmp/underbrace-import-trace-agent');E=Path('/home/jake/Developer/Course_Academy/reference/edb-math/audits/2026-10-17-underbrace-import/evidence')
h=json.loads((E/'target-history.json').read_text());meta=json.loads((E/'target-history-metadata.json').read_text());target=json.loads((E/'target.json').read_text())[0][0]
r=json.loads((O/'reproduction.json').read_text());old=r['original']['markdown_output'];newer=r['newer']['import_content'];texts={v[2]:v[1] for v in h if v[0]==1064 and v[-1]};times={row[0][':db/id']:row[0].get(':db/txInstant') for row in meta};out={'current_entity':target[':db/id'],'transaction_partition_offset':13194139533312,'versions':[]}
for tx,text in sorted(texts.items()):
 out['versions'].append({'tx':tx,'basis':tx-13194139533312,'txInstant':times[tx],'source_eid':next(row[3] for row in h if row[2]==tx and row[-1]),'source':':org/Math-Academy','sha256':hashlib.sha256(text.encode()).hexdigest(),'exact_original_json_render':text==old,'exact_newer_import_occurrence':text==newer,'equals_newer_import_after_U2061_removal':text.replace('\u2061','')==newer,'equals_current_pull':text==target[':tutorial/content'],'underbrace_glyph_count':text.count('⏟'),'proper_underbrace_command_count':text.count(r'\underbrace'),'invisible_U2061_count':text.count('\u2061')})
assert out['versions'][0]['exact_original_json_render'];assert out['versions'][1]['exact_newer_import_occurrence'];assert out['versions'][2]['equals_current_pull'];assert out['versions'][2]['equals_newer_import_after_U2061_removal']
for group in ['current_converters','historical_converters']:
 for name,entry in r[group].items():entry['exact_formula_in_current_pull']=entry['problem'].strip('$\n') in target[':tutorial/content']
out['current_formula_matches']={name:entry['exact_formula_in_current_pull'] for name,entry in r['current_converters'].items()}
out['later_change']='T3083 reinserted 15 actual U+2061 FUNCTION APPLICATION characters immediately after \\operatorname{cos|sin}; removing them exactly restores T126. No other character changed. Both _{⏟} brace constructs are preserved.'
(O/'reproduction.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');(O/'current-lineage-history-comparison.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
