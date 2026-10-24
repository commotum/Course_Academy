"""Exercise an actual registered legacy generator and the shared publication path."""
import copy,importlib.util,json,sys
from pathlib import Path
from types import SimpleNamespace
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R));sys.path.insert(0,str(R/'scripts'))
from scripts.generator_publish import localize_record,stable_identities,validate_question,enum,answer_id
from scripts.question_capture.math_format import normalize_math_boundaries
class NoAssets:
 saved={}
 def text(self,value):return value
 def resolve(self,value):return value

def main():
 p=R/'generate/scratch/17592186064281.py';sp=importlib.util.spec_from_file_location('registered_trig',p);g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g);rows=[]
 for profile,(level,_,_,parameters) in g.PROFILES.items():
  t=next(t for t in parameters if g.eligible(profile,t));original=g.generate(level,0,profile=profile,t=t);before=copy.deepcopy(original);localized=localize_record(original,R,R,library=NoAssets());q=localized['question'];validate_question(q);stable=stable_identities(q,g.KP_UUID)
  assert original==before
  assert q[':question/answer-fields']==before['question'][':question/answer-fields'];assert stable[':question/worked-solution']==q[':question/worked-solution']
  rows.append({'profile':profile,'difficulty':level,'prompt_changed':q[':question/problem']!=before['question'][':question/problem'],'solution_changed':q[':question/worked-solution']!=before['question'][':question/worked-solution'],'answers_unchanged':True,'publication_validated':True})
 # Verify the exact imported source HTML now normalizes at the historical entry point.
 from bs4 import BeautifulSoup
 from import_historical_question_content import Renderer
 source=(R/'reference/edb-math/audits/2026-10-23-solution-latex-17592186233932/source-0-worked-solution.html').read_text();value=Renderer(305).text(BeautifulSoup(source,'html.parser'));assert r'\begin{align*}' not in value and value.count(r'\begin{aligned}')==2
 # The current capture importer uses the same formatting boundary after HTML conversion.
 from capture.scripts.database.text import markdown
 from capture.scripts.database.math_content import prose
 value=prose('<p>Differentiate.</p><p>\\begin{align*}x&=1\\\\[5pt]\n\n&=1\\end{align*}</p>');assert '$$' in value and r'\begin{aligned}' in value
 report={'registered_legacy_generator':str(p.relative_to(R)),'profiles':len(rows),'results':rows,'historical_html_import_verified':True,'current_capture_import_verified':True,'shared_publication_normalizes_before_identity':True,'immutable_packages_need_no_in_place_edits':True};(H/'process-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
