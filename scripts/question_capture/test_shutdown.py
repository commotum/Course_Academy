"""Real SIGTERM while Playwright waits must leave checkpoints and release the lock."""
import os
import signal
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from core import Pacer

class ShutdownTests(unittest.TestCase):
    def test_stop_interrupts_pacing_before_another_action(self):
        args=SimpleNamespace(stop_event=threading.Event(),event_min=60,event_max=60)
        args.stop_event.set()
        with self.assertRaises(KeyboardInterrupt):Pacer(args).wait('event','fixture')

    def test_sigterm_during_playwright_wait_closes_browser_and_releases_lock(self):
        script='''
import sys
from unittest.mock import patch
from capture import main
from browser import CaptureBrowser
from playwright.sync_api import sync_playwright
from types import SimpleNamespace

def fixture(args):
 with sync_playwright() as p:
  context=p.chromium.launch(headless=True)
  try:
   page=context.new_page();page.set_content('<body>Question</body>')
   reader=CaptureBrowser(page,args,None,None)
   print('READY',flush=True)
   page.wait_for_timeout(1500)
   reader.check()
  finally:context.close()
with patch('capture.run',fixture):
 raise SystemExit(main(['run','--state-dir',sys.argv[1]]))
'''
        for stop_signal in (signal.SIGTERM, signal.SIGINT):
            with self.subTest(signal=stop_signal):
                with tempfile.TemporaryDirectory() as work:
                    process=subprocess.Popen([sys.executable,'-u','-c',script,work],
                        cwd=Path(__file__).parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                    try:
                        self.assertEqual(process.stdout.readline().strip(),'READY')
                        process.send_signal(stop_signal)
                        output,error=process.communicate(timeout=12)
                        self.assertEqual(process.returncode,1,error)
                        self.assertIn('saved checkpoints are retained',error)
                        import fcntl
                        with (Path(work)/'capture.lock').open('a') as lock:
                            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                    finally:
                        if process.poll() is None:process.kill();process.wait()

if __name__=='__main__':unittest.main()
