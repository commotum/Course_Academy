"""Check the exact integrated plan and prepare actual application-renderer cases."""
import collections,hashlib,json,pathlib,re,sys
import html as html_lib
HERE=pathlib.Path(__file__).resolve().parent;BULK=HERE.parent
def sha(x):return hashlib.sha256(x if isinstance(x,bytes) else x.encode()).hexdigest()
def tokens(x):return re.findall(r'\{\{[^{}]+\}\}',x)
def images(x):return re.findall(r'!\[[^\]]*\]\([^)]*\)',x)
def ident(x):return x.get(':db/ident','').split('/')[-1]
def answer(a,updates):return {'id':str(a[':db/id']),'type':ident(a.get(':answer/type',{})),'value':updates.get((a[':db/id'],':answer/value'),a.get(':answer/value',''))}
def fields(q,updates):return [{'id':str(f[':db/id']),'key':f.get(':answer-field/key',''),'type':ident(f.get(':answer-field/type',{})),
    'choices':[answer(a,updates) for a in f.get(':answer-field/choices',[])]} for f in q.get(':question/answer-fields',[])]
def main():
    source=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else BULK/'integrated-changes.json'
    data=json.loads(source.read_text());changes=data['changes'] if isinstance(data,dict) else data
    snap=BULK/'snapshot-3482';entities={r[':db/id']:r for r in json.loads((snap/'entities.json').read_text())}
    qs={r[':db/id']:r for r in json.loads((snap/'questions.json').read_text())}
    updates={(r['entity'],r['attribute']):r['after'] for r in changes}
    failures=[];formula_cases=[];seen=set();filehash={};source_checks=[]
    for r in changes:
        key=(r['entity'],r['attribute']);before=r['before'];after=r['after']
        if entities.get(r['entity'],{}).get(r['attribute'])!=before:failures.append([key,'fresh-before-mismatch'])
        if tokens(before)!=tokens(after):failures.append([key,'control-token-change'])
        if images(before)!=images(after):failures.append([key,'image-reference-change'])
        rebuilt=before;repls=sorted(r['replacements'],key=lambda x:x['start'])
        if any(a['end']>b['start'] for a,b in zip(repls,repls[1:])):failures.append([key,'overlap'])
        for p in reversed(repls):
            old=p.get('before',p.get('old_markdown'));new=p.get('after',p.get('new_markdown'))
            if before[p['start']:p['end']]!=old:failures.append([key,'span-mismatch'])
            rebuilt=rebuilt[:p['start']]+new+rebuilt[p['end']:]
            path=p['source_file']
            if path not in filehash:filehash[path]=pathlib.Path(path).read_text()
            raw=filehash[path]
            html=p['source_html'];offset=p.get('source_offset')
            if html not in raw or sha(html)!=p['source_sha256']:failures.append([key,'source-mismatch'])
            if offset is not None and raw[offset:offset+len(html)]!=html:failures.append([key,'source-offset-mismatch'])
            rid=p.get('source_occurrence_id',p.get('occurrence_id'));source_checks.append(rid)
            if (rid,new) not in seen:
                seen.add((rid,new));problem=new
                if r['attribute']==':answer/value' and ident(entities[r['entity']].get(':answer/type',{}))=='math':problem='$'+new+'$'
                formula_cases.append({'id':rid,'problem':problem,'source_html':html,'change':list(key)})
        if rebuilt!=after:failures.append([key,'not-exact-localized-edit'])
    cases=[];qids=set()
    changed_answers={e for e,a in updates if a==':answer/value'}
    for qid,q in qs.items():
        if (qid,':question/problem') in updates or (qid,':question/worked-solution') in updates or any(a[':db/id'] in changed_answers for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])):qids.add(qid)
    for qid in sorted(qids):
        q=qs[qid]
        for state,up in [('before',{}),('after',updates)]:
            cases.append({'id':f'{qid}-{state}','problem':up.get((qid,':question/problem'),q.get(':question/problem','')),
                'solution':up.get((qid,':question/worked-solution'),q.get(':question/worked-solution','')),'fields':fields(q,up)})
    for r in changes:
        if r['attribute']==':tutorial/content':
            for state in ('before','after'):cases.append({'id':f'{r["entity"]}-{state}','problem':r[state]})
        elif r['attribute']==':answer/value' and not any(any(a[':db/id']==r['entity'] for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])) for q in qs.values()):
            atype=ident(entities[r['entity']].get(':answer/type',{}))
            for state in ('before','after'):cases.append({'id':f'{r["entity"]}-{state}','problem':'','fields':[{'id':'unowned-answer-preview','key':'selection','type':'radio','choices':[{'id':str(r['entity']),'type':atype,'value':r[state]}]}]})
    for case in cases:case['omitTrees']=True
    source_tex=set()
    for case in formula_cases:
        for literal in re.findall(r'<mtext\b[^>]*>([\s\S]*?)</mtext>',case['source_html']):
            source_tex.update(html_lib.unescape(body) for body in re.findall(r'\[math\]([\s\S]*?)\[/math\]',literal))
    source_tex_cases=[{'id':sha(body)[:12],'problem':'$$\n'+body+'\n$$'} for body in sorted(source_tex)]
    summary={'input':str(source),'input_sha256':sha(source.read_bytes()),'fields':len(changes),'source_replacements':len(source_checks),'unique_source_formula_cases':len(formula_cases),'full_before_after_cases':len(cases),'questions':len(qids),'failures':failures,'passed':not failures}
    for name,value in [('static-verification.json',summary),('formula-cases.json',formula_cases),('full-cases.json',cases),('source-tex-cases.json',source_tex_cases)]: (HERE/name).write_text(json.dumps(value,ensure_ascii=False)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
