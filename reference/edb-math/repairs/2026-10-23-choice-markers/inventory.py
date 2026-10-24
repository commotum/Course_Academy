import json,re,collections
from pathlib import Path
H=Path('reference/edb-math/repairs/2026-10-23-choice-markers');snapshot=Path('.local/edb/choice-marker-repair-current.jsonl');problems={};qfields=collections.defaultdict(list);fields=collections.defaultdict(dict);idents={};gpaths=collections.defaultdict(list);kpgen={};titles={};gens={};qmeta={}
for r in map(json.loads,snapshot.open()):
 e,a,v=r['e'],r['a'],r['v']
 if a=='question/problem':problems[e]=r
 if a=='question/answer-fields':qfields[e].append(v)
 if a in ('answer-field/key','answer-field/type','answer-field/choices','answer-field/correct'):
  if a=='answer-field/choices':fields[e].setdefault(a,[]).append(v)
  else:fields[e][a]=v
 if a=='db/ident':idents[e]=v
 if a=='knowledge-point/question-generator':kpgen[e]=v
 if a=='knowledge-point/title':titles[e]=v
 if a=='question-generator/script':gpaths[e].append(v)
 if a=='question-generator/id':gens[e]=v
 if a=='question/math-academy-id':qmeta[e]=v
pat=re.compile(r'\{\{(?:answer-field:)?([^{}]+)\}\}');candidates=[];kinds=collections.Counter()
for e,r in problems.items():
 if '{{' not in r['v']:continue
 fs=[{'entity':f,**fields[f],'type':idents.get(fields[f].get('answer-field/type'),fields[f].get('answer-field/type'))} for f in qfields[e]];bykey={f.get('answer-field/key'):f for f in fs};bad=[]
 for m in pat.finditer(r['v']):
  f=bykey.get(m[1]);typ=str(f.get('type','')).split('/')[-1] if f else 'unbound'
  kinds[typ]+=1
  if f and typ in ('radio','checkbox','free'):bad.append({'start':m.start(),'end':m.end(),'marker':m[0],'key':m[1],'type':typ,'field':f['entity']})
 if bad:candidates.append({**r,'fields':fs,'markers':bad,'ma_id':qmeta.get(e)})
active=[{'kp':kp,'title':titles.get(kp),'generator':g,'generator_id':gens.get(g),'scripts':gpaths[g]} for kp,g in kpgen.items()];allgens=[{'generator':g,'id':gens.get(g),'scripts':p,'active':g in kpgen.values()} for g,p in gpaths.items()]
for name,data in [('candidates.json',candidates),('active-generators.json',active),('all-generators.json',allgens)]: (H/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('basis',json.loads(snapshot.with_suffix('.manifest.json').read_text())['basis_t']);print('marker kinds',kinds);print('affected',len(candidates),collections.Counter(m['type'] for q in candidates for m in q['markers']));print('active generators',len(active),'all',len(allgens));print('paths sample',[a['scripts'] for a in active[:12]]);print('path prefixes',collections.Counter('/'.join(str(p).split('/')[:3]) for a in active for p in a['scripts']))
