import collections,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/currency-escaping-2026-10-26'
TOKEN=re.compile(r'(?<!\\)\\\[[\s\S]*?\\\]|(?<!\\)\\\([\s\S]*?\\\)|(?P<bad>(?<!\\)\$\$(?:\\,\s*)*\d[^$\n]*?(?<!\\)\$(?!\$))|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$')
fields={f['entity']:f for f in json.loads((H/'fields.json').read_text())};pending=[];seen=set();facts=0;strings=0
for line in(W/'after.jsonl').open():
 d=json.loads(line);facts+=1;v=d['v']
 if not isinstance(v,str):continue
 strings+=1
 if d['a']=='answer/value'and d['e']in fields:assert v==fields[d['e']]['after'];seen.add(d['e'])
 if any(m['bad']is not None for m in TOKEN.finditer(v))or re.search(r'\\\[/?math\]',v):pending.append(d)
 elif d['a']=='answer/value'and(re.fullmatch(r'\$-\s*\$\d+(?:\.\d+)?\$',v)or re.fullmatch(r'\$\$\(-?[\d, \\]+\)\$',v)or'$V(4) = $'in v):pending.append(d)
assert len(seen)==1066 and not pending
report={'basis_t':json.loads((W/'after.manifest.json').read_text())['basis_t'],'facts_scanned':facts,'string_values_scanned':strings,'repaired_answer_values_verified':len(seen),'remaining_confirmed_currency_patterns':len(pending),'scope':'Nested currency delimiters, negative currency, parenthesized currency and reviewed V(4) monetary equations'};(H/'postscan.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
