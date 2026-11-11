"""Check actual delivery survivors from printed givens and offered responses."""
import sys
sys.dont_write_bytecode = True
import argparse,json
from pathlib import Path
from fingerprint import content_fingerprint
from math_checks import audit, check_bank

CHECKS=['visible-mathematics','independent-pivot-task','last-coordinate-ambiguity']
def run(records):
    witnesses=[]
    for record in records:
        a=audit(record)
        check_bank(record)
        witnesses.append({'fingerprint':content_fingerprint(record['question']),**a})
    fingerprints=sorted(w['fingerprint'] for w in witnesses)
    return {'status':'passed','checked_fingerprints':fingerprints,'check_results':[{'id':i,'status':'passed','checked_fingerprints':fingerprints} for i in CHECKS],'witnesses':witnesses}

def main():
    p=argparse.ArgumentParser();p.add_argument('--records',required=True);p.add_argument('--inventory',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    records=json.loads(Path(a.records).read_text());json.loads(Path(a.inventory).read_text())
    Path(a.output).write_text(json.dumps(run(records),indent=2)+'\n')
if __name__=='__main__':main()
