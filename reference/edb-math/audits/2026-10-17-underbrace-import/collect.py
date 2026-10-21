"""Read-only brace-accent census at a pinned EDB basis."""
import collections, concurrent.futures, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from capture.scripts.database.edn import loads,dumps
HERE=Path(__file__).resolve().parent
E=HERE/'evidence'
B=json.loads((E/'status.json').read_text())['basis']
C=Publisher.from_environment(source=':agent/codex').client
ATTRS=loads((E/'string-attributes.edn').read_text())
# U+23DE/U+23DF horizontal braces; compatibility forms and correct commands
# make repaired occurrences distinguishable from malformed ones.
NEEDLES=['⏟','⏞','︷','︸',r'\underbrace',r'\overbrace']

def query(q, inputs, name, history=False):
    p=E/name;p.parent.mkdir(parents=True,exist_ok=True)
    qp=p.with_name(p.name+'-query.edn');ip=p.with_name(p.name+'-inputs.edn')
    qp.write_text(q);ip.write_text(dumps(inputs))
    options=['--file',qp,'--inputs',ip,'--as-of',B,'--timeout-ms','120000','--max-value-bytes','536870912','--max-join-bytes','268435456','--max-results','1000000']
    if history:options+=['--history']
    data=C.command('query',*options,timeout=150)
    p.with_suffix('.edn').write_text(data)
    return loads(data)

def scan(attr):
    aid,ident=attr;stem=str(ident)[1:].replace('/','-')
    if aid==1080:
        # The query engine exceeded intermediate/EDN collection limits for
        # this attribute. A complete native AEVT stream supplies the census.
        stats=json.loads((E/'answer-native/stats.json').read_text())
        assert stats['as_of_basis']==B and stats['completed_to_end']
        rows=loads((E/'answer-native/matches.edn').read_text())
        assert len(rows)==stats['matching_rows']
        return {'attribute':str(ident),'total_fields':stats['current_datoms'],'rows':rows,'method':'native-aevt-stream'}
    saved=E/'current'/f'{stem}.edn'
    if saved.exists():
        rows=loads(saved.read_text())
    else:
        # Separate predicates avoid multiplying large string bindings in OR.
        found=set()
        for i,needle in enumerate(NEEDLES):
            fragment=E/'current'/f'{stem}-{i}.edn'
            if fragment.exists(): part=loads(fragment.read_text())
            else:
                q='[:find ?e ?v ?tx ?source :where [?e '+str(ident)+' ?v ?tx ?source] [(includes? ?v '+dumps(needle)+')]]'
                part=query(q,[],'current/'+stem+'-'+str(i))
            found.update(tuple(r) for r in part)
        rows=sorted(found)
        saved.write_text(dumps(rows))
    cp=E/'counts'/f'{stem}.edn'
    count=loads(cp.read_text()) if cp.exists() else query('[:find (count ?e) :where [?e '+str(ident)+' ?v]]',[],'counts/'+stem)
    print(ident,'fields',count,'matching',len(rows),flush=True)
    return {'attribute':str(ident),'total_fields':count[0][0] if count else 0,'rows':rows}

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as p:results=list(p.map(scan,ATTRS))
    (E/'current-results.json').write_text(json.dumps(jsonable(results),ensure_ascii=False,indent=2)+'\n')
    hp=E/'target-history.edn'
    history=loads(hp.read_text()) if hp.exists() else query('[:find ?a ?v ?tx ?s ?added :in $ ?e :where [?e ?a ?v ?tx ?s ?added]]',[17592186060895],'target-history',True)
    (E/'target-history.json').write_text(json.dumps(jsonable(history),ensure_ascii=False,indent=2)+'\n')
    print('TOTAL',sum(len(x['rows']) for x in results),flush=True)
