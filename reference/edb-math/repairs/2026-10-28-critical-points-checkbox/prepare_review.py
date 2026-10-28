from pathlib import Path
import json,subprocess,sys
from migration import H,ROOT,Publisher,MigrationCommitter,prepare,loads,native_executable
p=Publisher.from_environment(source=':agent/codex')
p.config.preview_bin=native_executable(p.config,p.client.stop_event,(str((H/'native_preview.rs').relative_to(ROOT)),'capture/scripts/database/preview.py','engine/edb/answer_fields.rs','engine/edb/configuration.rs','engine/edb/progress.rs'),'critical-checkbox-preview')
d=H/'review';prepared=prepare(p,d)
subprocess.run([sys.executable,str(ROOT/'skills/radio2checkbox/scripts/lint_presentation.py'),str(d/'proposed-presentation.json'),'--output',str(d/'proposed-lint.json')],check=True)
MigrationCommitter(p.config,p.client,d).preview(loads(prepared['batch_edn']),loads(prepared['snapshot_edn']))
(H/'native-build.json').write_text(json.dumps({'preview_executable':str(p.config.preview_bin)},indent=2)+'\n')
print('Prepared and speculatively previewed nine conversions and one None cleanup at',prepared['basis'])
