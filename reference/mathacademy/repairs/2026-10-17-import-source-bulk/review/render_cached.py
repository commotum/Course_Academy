"""Reuse only byte-identical cases rendered with the exact current UI sources."""
import argparse,collections,hashlib,json,pathlib,subprocess
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[4]
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha(p):return sha_bytes(p.read_bytes())
def case_hash(c):return sha_bytes(json.dumps(c,ensure_ascii=False,separators=(',',':')).encode())
def ui_hashes():return {p:sha(ROOT/p) for p in ['ui/learning.js','ui/learning.css','ui/question-fields.js','ui/mathjax-config.js','ui/prose-lists.js']}
def main():
    p=argparse.ArgumentParser();p.add_argument('cases',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);p.add_argument('widths');p.add_argument('old_cases',type=pathlib.Path);p.add_argument('old_report',type=pathlib.Path);a=p.parse_args()
    cases=json.loads(a.cases.read_text());old_cases=json.loads(a.old_cases.read_text());old=json.loads(a.old_report.read_text());widths=list(map(int,a.widths.split(',')))
    assert old['input_sha256']==sha(a.old_cases),'baseline report not bound to exact old cases'
    current_ui=ui_hashes();assert old['ui_unchanged'] and old['ui_sha256']==current_ui,'cannot reuse another UI version'
    old_report_sha=sha(a.old_report);positions=collections.Counter();cache={}
    for batch in old['measurements']:
        w=batch['width']
        for item in batch['items']:
            c=old_cases[positions[w]];positions[w]+=1;assert c['id']==item['id'],'baseline order mismatch'
            h=case_hash(c);cache[(w,h)]={**item,'case_sha256':h,'evidence_report_sha256':old_report_sha}
    assert all(n==len(old_cases) for n in positions.values())
    pending=[c for c in cases if any((w,case_hash(c)) not in cache for w in widths)]
    pending_file=a.output.with_suffix('.pending-cases.json');fresh_file=a.output.with_suffix('.fresh.json');pending_file.write_text(json.dumps(pending,ensure_ascii=False)+'\n')
    fresh=None;fresh_sha=None
    if pending:
        subprocess.run(['node',str(HERE/'render-review.cjs'),str(pending_file),str(fresh_file),a.widths],check=True)
        fresh=json.loads(fresh_file.read_text());fresh_sha=sha(fresh_file)
        assert fresh['input_sha256']==sha(pending_file) and fresh['ui_unchanged'] and fresh['ui_sha256']==current_ui
        positions=collections.Counter()
        for batch in fresh['measurements']:
            w=batch['width']
            for item in batch['items']:
                c=pending[positions[w]];positions[w]+=1;assert c['id']==item['id']
                h=case_hash(c);cache[(w,h)]={**item,'case_sha256':h,'evidence_report_sha256':fresh_sha}
    assert ui_hashes()==current_ui,'UI changed during cache merge'
    result={'input':str(a.cases),'input_sha256':sha(a.cases),'ui_sha256':current_ui,'ui_unchanged':True,
        'errors':old['errors']+(fresh['errors'] if fresh else []),'measurements':[{'width':w,'items':[cache[(w,case_hash(c))] for c in cases]} for w in widths],
        'reuse_proof':{'baseline_cases':str(a.old_cases),'baseline_cases_sha256':sha(a.old_cases),'baseline_report':str(a.old_report),'baseline_report_sha256':old_report_sha,
          'fresh_cases':str(pending_file),'fresh_cases_sha256':sha(pending_file),'fresh_report':str(fresh_file) if fresh else None,'fresh_report_sha256':fresh_sha,
          'reused_cases':len(cases)-len(pending),'fresh_cases_count':len(pending),'rule':'Every reused case is exact canonical JSON byte equality, including source HTML and fields, and has matching current UI source hashes.'}}
    a.output.write_text(json.dumps(result,ensure_ascii=False)+'\n');print(json.dumps(result['reuse_proof'],indent=2))
if __name__=='__main__':main()
