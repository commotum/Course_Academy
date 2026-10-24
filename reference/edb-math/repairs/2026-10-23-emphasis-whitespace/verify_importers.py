"""Run explicit HTML conversion regressions in separate import namespaces."""
import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[4]
CASES=[('<p>before<strong> word </strong>after</p>','before **word** after'),('<p><strong> Step 1</strong>: Do it.</p>','**Step 1**: Do it.'),('<p><em> Hint </em></p>','*Hint*'),('<p>before<b></b>after</p>','beforeafter')]
for setup,expression in [
 ("sys.path.insert(0,'scripts');from bs4 import BeautifulSoup;from import_historical_question_content import Renderer", "Renderer('1159').text(BeautifulSoup(source,'html.parser'))"),
 ("sys.path.insert(0,'capture');from scripts.database.text import markdown",'markdown(source)')]:
 code='import sys;'+setup+'\nfor source,expected in '+repr(CASES)+':\n actual='+expression+'\n assert actual==expected,(source,actual,expected)\nprint("HTML conversion checks passed")\n'
 subprocess.run([sys.executable,'-c',code],cwd=R,check=True)
