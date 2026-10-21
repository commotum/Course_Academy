"""Fail when supported original source cases are unavailable for replay."""
import sys,argparse,json
sys.dont_write_bytecode=True
p=argparse.ArgumentParser();p.add_argument('--workspace',default='../workspace');a=p.parse_args();sys.path.insert(0,a.workspace)
import generator
failures=[]
for profile in ['q-20598','q-20589','e-4709']:
 try:generator.generate(difficulty='easy',seed=731,template=profile,replay=True)
 except Exception as e:failures.append({'profile':profile,'error':repr(e)})
print(json.dumps({'expected':'all supplied source cases replay, with documented corrections or inferred missing source keys','failures':failures},indent=2))
sys.exit(1 if failures else 0)
