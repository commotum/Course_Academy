"""Read contributor and existing-key provenance at the review basis."""
import json
from audit_capture import OUT, edb, save

def main():
    review=json.loads((OUT/'keyed-resolutions.json').read_text())
    basis=review['basis'];ids=[r['question_eid'] for r in review['questions']]
    provenance=edb.DB.query('[:find ?q ?f ?a ?tx (pull ?s [:db/id :db/ident]) :in $ [?q ...] :where [?q :question/answer-fields ?f] [?f :answer-field/correct ?a ?tx ?s]]',[ids],OUT/'evidence','key-provenance',basis)
    assert {r[0] for r in provenance}==set(ids)
    contributor=edb.DB.query('[:find (pull ?s [:db/id :db/ident :db/doc]) :in $ ?ident :where [?s :db/ident ?ident]]',[edb.kw(':agent/gpt-6.1-sol-high')],OUT/'evidence','future-contributor',basis)
    assert len(contributor)==1
    save('provenance.json',dict(basis=basis,database_writes=0,existing_key_datoms=provenance,existing_contributor_for_future_transactions=contributor))
    print(json.dumps(dict(basis=basis,key_assertions=len(provenance),questions=len(ids),future_contributor_verified=True)))

if __name__=='__main__':main()
