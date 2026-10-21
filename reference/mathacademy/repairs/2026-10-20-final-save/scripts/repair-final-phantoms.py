from pathlib import Path
from playwright.sync_api import sync_playwright
from scripts.config import Config
from scripts.recovery import repair_saved_capture
from scripts.storage import atomic_json
root=Path('reference/mathacademy/repairs/2026-10-20-final-save')
with sync_playwright()as p:
 b=p.chromium.launch();page=b.new_page()
 page.route('**/*',lambda route:route.abort())
 r=repair_saved_capture(Config(),Path('reference/mathacademy/capture/foundations/14352410'),page,apply=True)
 atomic_json(root/'phantom-repair.json',r);print(r)
 b.close()
