from pathlib import Path
H=Path(__file__).resolve().parent
p=H/'generator-17592186129197/17592186129197.py';s=p.read_text();s=s.replace(" if field_specs is not None:\n  question=normalize_question(question);spelling=[normalize_tex(v)for v in spelling]\n content=", " if field_specs is not None:\n  content=",1);p.write_text(s)
p=H/'generator-17592186133927/17592186133927.py';s=p.read_text();s=s.replace("out=HERE/'assets'/('region-'", "out=Path(os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',str(HERE/'assets')))/('region-'");s=s.replace(" if not (out.exists() and out.with_suffix('.json').exists()):", " out.parent.mkdir(parents=True,exist_ok=True)\n if not (out.exists() and out.with_suffix('.json').exists()):");s=s.replace("dir=HERE,suffix='.render-input.json'", "dir=out.parent,suffix='.render-input.json'");p.write_text(s)
p=H/'generator-17592186133927/17592186133927/render.py';s=p.read_text();a=s.index('try:import matplotlib');b=s.index("matplotlib.use('Agg')",a);p.write_text(s[:a]+'import matplotlib\n'+s[b:])
# Defensive addition only if original dump() bypassed recursive asset identity.
p=H/'generator-17592186198374/17592186198374.py';s=p.read_text();s=s.replace('dump(identity)', 'dump(asset_payload(identity))');p.write_text(s)
