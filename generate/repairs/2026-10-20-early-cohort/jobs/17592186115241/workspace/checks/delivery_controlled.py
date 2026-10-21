"""Compare controlled banks/keys after the real delivery filter."""
import json,sys
sys.dont_write_bytecode=True
from validate_repair import E,dump,field,correct,vec
raw=json.load(open(E/'controlled-records.json'))
post=json.load(open(E/'delivery-controlled/accepted.json'))
assert len(raw)==len(post)==35
def signature(r):
    bank=sorted(str(vec(c[':answer/value'])) for c in field(r)[':answer-field/choices'])
    key=str(vec(next(c[':answer/value'] for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r))))
    return bank,key
assert [signature(r) for r in raw]==[signature(r) for r in post]
dump('controlled-delivery-results.json',{'input':35,'accepted':35,'banks_and_keyed_lines_preserved':True,'all_five_roles_with_same_bank_survive_in_each_case':True})
dump('controlled-grader-input.json',[{'label':str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct(r) else 'rejected','purpose':'controlled changes after shared delivery filtering'} for c in field(r)[':answer-field/choices']]} for i,r in enumerate(post)])
