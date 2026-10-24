"""Publish the reviewed formatting-only successor; retain original package bytes."""
import hashlib,json,sys,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT));from scripts.generator_packages import build_manifest,manifest_digest,publish_package,verify_package

def main():
 c=next(c for c in json.loads((HERE/'source-changes.json').read_text()) if c['kind']=='package-successor');source=ROOT/c['source'];old=Path('/media/jake/SSD/EDB/math')/c['path'];m=c['manifest'];manifest=build_manifest(source,m['entrypoint'],m['files'],dependencies=m['dependencies']);digest=manifest_digest(manifest)
 checked=json.loads((HERE/'generator-verification.json').read_text());assert checked['only_expected_presentation_changes'];assert any(r['reference']==c['path'] for r in checked['results'])
 # The user explicitly authorized these source changes and their publication.
 package=publish_package(source,Path('/media/jake/SSD/EDB/math'),m['entrypoint'],m['files'],dependencies=m['dependencies'],expected_digest=digest)
 prior=verify_package(old.parent)
 assert all(manifest['files'][n]==m['files'][n] for n in m['files'] if n!=m['entrypoint'])
 new_id=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:question-generator:'+digest))
 active=[g for g in json.loads((HERE/'active-generators.json').read_text()) if c['path'] in g['scripts']];assert len(active)==1
 evidence={'old_reference':c['path'],'old_digest':prior.digest,'new_reference':package.reference,'new_digest':digest,'new_generator_id':new_id,'registration':active[0],'new_manifest':manifest,'authorization':'User explicitly requested repair of all affected generators and publication without waiting.','validation':'Only the two redundant radio markers change; original package bytes and dependency closure preserved.'}
 (HERE/'package-publication.json').write_text(json.dumps(evidence,indent=2)+'\n');print(json.dumps({k:v for k,v in evidence.items() if k not in ('registration','new_manifest')}))
if __name__=='__main__':main()
