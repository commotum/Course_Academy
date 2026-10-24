"""The bundled guard preserves valid sampling and refuses excluded source families."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]


class RuntimeGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name)
        for target,source in [('ca_source_policy.py','generator_source_policy.py'),('ca_source_runtime.py','generator_source_runtime.py')]:
            shutil.copyfile(ROOT/'scripts'/source,self.folder/target)
        self.policy={'excluded':[{':db/id':7,':question/math-academy-id':'q-7'}]}
        self.path=self.folder/'policy.json';self.path.write_text(json.dumps(self.policy))
        sys.path.insert(0,str(self.folder));self.addCleanup(sys.path.remove,str(self.folder))
        spec=importlib.util.spec_from_file_location('runtime_under_test',self.folder/'ca_source_runtime.py')
        self.runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.runtime)

    def test_api_prunes_dispatch_and_rejects_positional_or_metadata_bypass(self):
        namespace={'PROFILES':{'bad':{'source_id':'q-7'},'good':{'source_id':'q-8'}},
                   'LEVELS':{'easy':['bad'],'moderate':['good']},
                   'SOURCES':{'q-7':{'archive':'retain evidence'}}}
        def generate(template):return {'question':{},'generation':{'source_id':{'bad':'q-7','good':'q-8'}[template]}}
        namespace['generate']=generate;self.runtime.install(namespace,self.path)
        self.assertEqual(set(namespace['PROFILES']),{'good'})
        self.assertEqual(namespace['LEVELS']['easy'],[])
        self.assertEqual(namespace['SOURCES'],{})
        self.assertEqual(namespace['generate']('good')['generation']['source_id'],'q-8')
        with self.assertRaises(self.runtime.ExcludedSource):namespace['generate']('bad')
        with self.assertRaises(self.runtime.ExcludedSource):namespace['generate'](template='bad')

    def write_cli(self):
        script=self.folder/'generator.py'
        script.write_text('''import argparse,json,os,sys
from pathlib import Path
from ca_source_runtime import cli,install
if __name__=='__main__' and not os.environ.get('_CA_SOURCE_POLICY_CHILD'):
    cli(__file__,Path(__file__).with_name('policy.json'));raise SystemExit
def generate(seed):
    return {'question':{':question/problem':str(seed)},'generation':{'source_id':'q-7' if seed%2 else 'q-8','parameter_fingerprint':str(seed)}}
install(globals(),Path(__file__).with_name('policy.json'))
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ['difficulty','format','template','output']:p.add_argument('--'+k)
    p.add_argument('--seed',type=int);p.add_argument('--count',type=int)
    a=p.parse_args()
    n=a.count*3 if a.difficulty=='all' else a.count
    print(json.dumps([generate(a.seed+2*i) for i in range(n)]))
''')
        return script

    def run_cli(self,*args):
        return subprocess.run([sys.executable,str(self.write_cli()),'--format','json','--count','2',*args],capture_output=True,text=True)

    def test_valid_batch_and_all_band_count_are_preserved(self):
        p=self.run_cli('--seed','2','--difficulty','all');self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual([r['question'][':question/problem'] for r in json.loads(p.stdout)],['2','4','6','8','10','12'])

    def test_retries_invalid_batch_without_duplicates_and_honors_output_file(self):
        out=self.folder/'output.json'
        p=self.run_cli('--seed','1','--difficulty','moderate','--output',str(out));self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(p.stdout,'')
        self.assertEqual([r['question'][':question/problem'] for r in json.loads(out.read_text())],['2','4'])

    def test_explicit_or_all_band_invalid_request_fails_without_partial_output(self):
        for args in [('--template','bad'),('--difficulty','all')]:
            p=self.run_cli('--seed','1',*args)
            self.assertNotEqual(p.returncode,0);self.assertIn('Source-eligibility policy rejects',p.stderr)
            self.assertEqual(p.stdout,'')


if __name__=='__main__':unittest.main()
