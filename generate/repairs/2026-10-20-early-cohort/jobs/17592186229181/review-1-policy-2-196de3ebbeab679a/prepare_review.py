import json,pathlib,hashlib,shutil,ast
R=pathlib.Path.cwd();J=R.parent;P=J/'workspace';old=J/'review-0-policy-2-93d9391d3687b946'
manifest=json.loads((P/'package.json').read_text())
def hashes():return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
(R/'package-before.json').write_text(json.dumps(hashes(),indent=2))
for name in ['acceptance_regressions.py','review_checks.py','source-math.json','source-original-records.json','minimal-failure.json']:
 shutil.copyfile(old/name,R/('previous-'+name if name=='minimal-failure.json' else name))
(R/'reuse-provenance.json').write_text(json.dumps({'from':str(old),'source_hash':'ad1f38de8941a2ebd50cb9df452cbcbd2a32d2f2b576c7cd45ae8ea5f9715072','copied':['acceptance_regressions.py','review_checks.py','source-math.json','source-original-records.json','previous-minimal-failure.json'],'scope':'Unchanged source math reused; executable helper definitions and strict regressions rerun on current package. Earlier verdict not reused.'},indent=2))
# Retain original executable baseline separately; never modify original snapshot or candidate.
N=R/'negative-fixture';N.mkdir(exist_ok=True)
shutil.copytree(old/'relocated',N,dirs_exist_ok=True)
(N/'package.json').write_text(json.dumps(manifest))
A=R/'author-check';A.mkdir(exist_ok=True)
s=(P/'evidence/checks.py').read_text().replace("ROOT=pathlib.Path(__file__).resolve().parent.parent",'ROOT=pathlib.Path('+repr(str(P))+')').replace("EVIDENCE=ROOT/'evidence'",'EVIDENCE=pathlib.Path('+repr(str(A))+')')
(A/'checks.py').write_text(s);shutil.copyfile(P/'evidence/validate_repair.py',A/'validate_repair.py');shutil.copyfile(R/'previous-minimal-failure.json',A/'before-minimal-failure.json')
print('Saved baseline hashes, scripts with provenance and isolated negative fixture.')
