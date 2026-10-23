"""Strict retained decision-case regression, including explicit candidate record input."""
import argparse,json,pathlib,re,collections
p=argparse.ArgumentParser();p.add_argument('--candidate-records',required=True);p.add_argument('--output',required=True);a=p.parse_args();groups=collections.defaultdict(list)
for r in json.load(open(a.candidate_records)):
 q=r.get('question',r);f=q[':question/answer-fields'][0];t=f[':answer-field/type'];t=t.get(':db/ident') if isinstance(t,dict) else t
 if not t.endswith('/radio'):continue
 s=q[':question/problem'];m=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',s,re.S);n=len(m[1].split('\\\\'));i,j=map(int,re.search(r'_\{(\d)(\d)\}',s).groups());groups[(n,'display' if '$$' in s else 'inline')].append({'id':q[':question/id'],'missing':i>n or j>n})
checks=[{'group':list(g),'cases':rs,'passed':{r['missing'] for r in rs}=={True,False}} for g,rs in groups.items()];passed=bool(checks) and all(c['passed'] for c in checks)
pathlib.Path(a.output).write_text(json.dumps({'candidate_file':a.candidate_records,'checks':checks,'passed':passed},indent=2));print(json.dumps({'passed':passed,'groups':len(checks)}));raise SystemExit(0 if passed else 1)
