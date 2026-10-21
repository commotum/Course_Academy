"""Refresh only the missing fence normalizer in the two affected packages."""
import ast,hashlib,importlib,json,shutil,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from scripts.generator_packages import build_manifest,manifest_digest,publish_package,resolve_registered_script
from capture.scripts.database.edn import dumps,loads,kw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
base=importlib.import_module('reference.mathacademy.repairs.2026-10-19-fraction-fences-corpus.publish')
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False,default=str)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def prepare():
    canonical=(ROOT/'scripts/question_capture/math_format.py').read_text();node=next(n for n in ast.parse(canonical).body if isinstance(n,ast.FunctionDef) and n.name=='scalable_fraction_parentheses');helper='\n'.join(canonical.splitlines()[node.lineno-1:node.end_lineno])+'\n\n\n';updates=[];checks=json.loads((HERE/'generator-checks.json').read_text());topics=json.loads((HERE/'logarithm-lesson-generators.json').read_text());gens={k[':db/id']:k[':knowledge-point/question-generator'] for [t] in topics for k in t[':topic/knowledge-points']}
    for g in checks:
        if g['kp'] not in (17592186110589,17592186110591):continue
        original=Path(g['script']).parent;manifest=json.loads((original/'generator-package.json').read_text());dest=HERE/'generator-repairs'/str(g['kp']);dest.mkdir(parents=True,exist_ok=True)
        for name in manifest['files']:
            path=dest/name;path.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original/name,path)
        path=dest/'math_format.py';text=path.read_text();assert 'def scalable_fraction_parentheses' not in text;text=text.replace('def normalize_tex(value):',helper+'def normalize_tex(value):');old='text = _matrix_layouts(_legacy_commands(text))';assert text.count(old)==1;text=text.replace(old,'text = scalable_fraction_parentheses(_matrix_layouts(_legacy_commands(text)))');path.write_text(text)
        path=dest/'generator.py';text=path.read_text();old_version="VERSION = '1.0.0'" if g['kp']==17592186110589 else "VERSION = '1.2.0'";new_version="VERSION = '1.0.1'" if g['kp']==17592186110589 else "VERSION = '1.2.1'";assert text.count(old_version)==1;path.write_text(text.replace(old_version,new_version))
        updated=build_manifest(dest,manifest['entrypoint'],manifest['files'],dependencies=manifest['dependencies']);digest=manifest_digest(updated);save('generator-repairs/'+str(g['kp'])+'/reviewed-manifest.json',updated);updates.append({'kp':g['kp'],'entity':gens[g['kp']][':db/id'],'old_reference':g['reference'],'new_reference':f'generators/{digest[:2]}/{digest}/{manifest["entrypoint"]}','digest':digest,'directory':str(dest),'manifest':updated})
    save('generator-updates.json',updates);print('Prepared two minimal package revisions.')
def audit():
    checks=json.loads((HERE/'generator-checks.json').read_text());updates={u['kp']:u for u in json.loads((HERE/'generator-updates.json').read_text())};reports=[];examples=[]
    def run(g):
        script=Path(updates[g['kp']]['directory'])/'generator.py' if g['kp'] in updates else Path(g['script']);r=subprocess.run([str(ROOT/'.venv/bin/python'),'-B',str(script),'--count','20','--seed','192110'],capture_output=True,text=True,timeout=60);r.check_returncode();records=json.loads(r.stdout);old=json.loads(Path(g['script']).with_name('sizing-audit-samples.json').read_text());fields=0
        for before,after in zip(old,records):
            oq,q=before['question'],after['question']
            for key in (':question/problem',':question/worked-solution'):
                assert base.PREP.analysis.signature(oq[key])==base.PREP.analysis.signature(q[key]);assert base.PREP.analysis.scale(q[key])==q[key];fields+=1
            for of,f in zip(oq[':question/answer-fields'],q[':question/answer-fields']):
                def bank(field):
                    return sorted(base.PREP.analysis.signature(a[':answer/value']) for a in field[':answer-field/choices'])
                def correct(field):
                    ref=field[':answer-field/correct'];ref=ref[1] if isinstance(ref,list) else ref;return base.PREP.analysis.signature(next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==ref))
                assert bank(of)==bank(f) and correct(of)==correct(f) and of[':answer-field/type']==f[':answer-field/type']
                for a in f[':answer-field/choices']:assert base.PREP.analysis.scale(a[':answer/value'],a[':answer/type']==':answer.type/math')==a[':answer/value'];fields+=1
        return {'kp':g['kp'],'records':len(records),'fields_checked':fields,'passed':True,'patched':g['kp'] in updates},records[0]
    with ThreadPoolExecutor(max_workers=3) as pool:
        for report,example in pool.map(run,checks):reports.append(report);examples.append(example)
    save('generator-verification.json',{'passed':True,'generators':len(reports),'records':sum(r['records'] for r in reports),'sizing_only_semantic_comparison':True,'checks':reports});save('generator-render-input.json',examples);print('All four generators passed 80 seeded records with unchanged mathematical content and correct answers.')
def commit():
    audit=json.loads((HERE/'generator-verification.json').read_text());assert audit['passed'];assert json.loads((HERE/'generator-ui/rendering.json').read_text())['passed'];updates=json.loads((HERE/'generator-updates.json').read_text());forms=[]
    for u in updates:
        manifest=u['manifest'];pkg=publish_package(Path(u['directory']),manifest['entrypoint'],manifest['files'],base.DB.config.math_root,dependencies=manifest['dependencies'],expected_digest=u['digest']);assert pkg.reference==u['new_reference'];forms.append([kw('db/cas'),u['entity'],kw('question-generator/script'),u['old_reference'],u['new_reference']])
    tx=HERE/'generator-transaction.edn';text=dumps(forms)+'\n'
    if tx.exists():assert tx.read_text()==text
    else:tx.write_text(text)
    intent=HERE/'generator-request.json'
    def check(report,committed):
        assert report[':edb/committed'] is committed;observed={(e,base.IDENTS[a],v,added) for e,a,v,t,s,added in report[':edb/tx-data'] if base.IDENTS[a]!=':db/txInstant'};wanted={(u['entity'],':question-generator/script',u[side],added) for u in updates for side,added in [('old_reference',False),('new_reference',True)]};assert observed==wanted and all(s==base.SOURCE_ID for e,a,v,t,s,added in report[':edb/tx-data'])
    if not intent.exists():
        raw=base.DB.command('with','--file',tx,'--source',base.SOURCE);(HERE/'generator-preview.edn').write_text(raw);report=loads(raw);check(report,False);save('generator-request.json',{'source':base.SOURCE,'endpoint':base.DB.config.endpoint,'database':'math','transaction_file':str(tx),'transaction_sha256':sha(tx),'request_key':'fraction-fence-generators-'+sha(tx),'audit_sha256':sha(HERE/'generator-verification.json'),'ui_sha256':sha(HERE/'generator-ui/rendering.json')})
    request=json.loads(intent.read_text());assert sha(tx)==request['transaction_sha256'] and sha(HERE/'generator-verification.json')==request['audit_sha256'] and sha(HERE/'generator-ui/rendering.json')==request['ui_sha256'];receipt=HERE/'generator-receipt.edn'
    if not receipt.exists():
        r=subprocess.run([str(base.SUBMIT),'transact','--database','math','--file',str(tx),'--endpoint',request['endpoint'],'--request-key',request['request_key'],'--source',base.SOURCE,'--timeout-ms','180000'],env=base.DB.environment,capture_output=True,text=True,timeout=210)
        if r.returncode:save('generator-submission-error.json',{'returncode':r.returncode,'stderr':r.stderr,'stdout':r.stdout});r.check_returncode()
        receipt.write_text(r.stdout)
    report=loads(receipt.read_text());check(report,True);basis=report[':edb/db-after-t'];rows=base.DB.query('[:find (pull ?g [*]) :in $ [?g ...] :where [?g :question-generator/id _]]',[[u['entity'] for u in updates]],HERE/'generator-committed','generators',basis);current={g[':db/id']:g for [g] in rows}
    for u in updates:assert current[u['entity']][':question-generator/script']==u['new_reference'];resolve_registered_script(u['new_reference'],ROOT,base.DB.config.math_root)
    save('generator-commit-verification.json',{'committed':True,'basis_after':basis,'generators_updated':2,'generator_records_tested':80,'only_generator_package_references_changed':True,'exact_committed_readback':True});print('Two generator package references committed and verified at basis',basis)
if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
