"""Bounded read-only topic/history UI inspection; always resume foundations."""
import json
from pathlib import Path
import subprocess
import threading

from scripts.browser.adapter import MathAcademyBrowser
from scripts.config import Config

ROOT = Path(__file__).resolve().parent
REPO = Path('/home/jake/Developer/Course_Academy')

def main():
    result = {}
    try:
        status = json.loads((REPO / '.local/capture/foundations/status.json').read_text())
        if status.get('status') != 'stopped':
            raise RuntimeError('Foundations has not checkpoint-stopped')
        config = Config(account='foundations', timeout_ms=15000)
        with MathAcademyBrowser(config, threading.Event()) as browser:
            browser.directory = ROOT
            browser._goto('https://mathacademy.com/topics/774')
            try:
                browser.page.locator('div.step[stepid],.questionWidget').first.wait_for(state='attached', timeout=5000)
                browser._settle_content(browser.page.locator('#steps') if browser.page.locator('#steps').count() else browser.page.locator('body'))
            except Exception as error:
                result['topic_readiness_error'] = str(error)
            result['topic'] = browser._evidence(browser.page, ROOT, 'topic-visible')
            result['topic_visible_text'] = browser.page.locator('body').inner_text()
            result['topic_questions'] = browser.page.locator('[id]').evaluate_all("ns => ns.filter(n=>/^question(?:Widget)?-/.test(n.id)).map(n=>({id:n.id,text:n.innerText,html:n.outerHTML}))")
            browser._goto('https://mathacademy.com/learn?taskId=13831129')
            browser.page.locator('#question-122027').wait_for(state='attached')
            browser.page.locator('#question-122027 .helpButton').hover()
            browser.page.wait_for_timeout(1000)
            result['history_help'] = browser._evidence(browser.page, ROOT, 'history-help-visible')
            result['help_menus'] = browser.page.locator('[class*=helpMenu],[class*=help-menu]').evaluate_all('ns=>ns.map(n=>({text:n.innerText,html:n.outerHTML}))')
            result['history_visible_text'] = browser.page.locator('body').inner_text()
            result['visible_links'] = browser.page.locator('a:visible').evaluate_all('ns=>ns.map(n=>({text:n.innerText,url:n.href})).filter(n=>/question|help|preview/i.test(n.text+n.url))')
    except Exception as error:
        result['error'] = str(error)
    finally:
        resumed = subprocess.run([str(REPO/'scripts/ma-workers'), 'start', 'foundations'], cwd=REPO, capture_output=True, text=True)
        result['restart'] = {'returncode': resumed.returncode, 'output':resumed.stdout+resumed.stderr}
        (ROOT/'visible-inspection.json').write_text(json.dumps(result,indent=2))
        print(json.dumps({'error':result.get('error'),'topic_question_count':len(result.get('topic_questions',[])), 'help_menus':result.get('help_menus'), 'restart':result['restart']},indent=2))

if __name__ == '__main__':
    main()
