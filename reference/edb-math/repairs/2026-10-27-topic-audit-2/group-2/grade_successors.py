import json,copy,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;source=(H/'validate_generators.py').read_text();body=source[source.index('checks=[];fields=[]'):];body=body.replace("'generator-grading-input.json'","'successor-grading-input.json'").replace("'generator-grading.json'","'successor-grading.json'").replace("'generator-render-input.json'","'successor-render-input.json'");samples=json.loads((H/'successor-samples.json').read_text());fresh=samples;exec(body)
