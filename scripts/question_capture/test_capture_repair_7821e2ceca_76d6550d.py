import ast
import json
import unittest
from pathlib import Path
from unittest.mock import Mock

import browser
from playwright.sync_api import TimeoutError as PlaywrightTimeout

ROOT = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14004892')

class AssetRetryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        saved = json.loads((ROOT / 'history-q-277261.json').read_text())
        cls.source_url = saved['assets'][0]['source_url']
        cls.saved_errors = saved['errors']
        tree = ast.parse(Path(browser.__file__).read_text())
        read = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'read')
        branch = next(n for n in ast.walk(read) if isinstance(n, ast.Try) and
                      any(isinstance(x, ast.Constant) and x.value == 'Visual asset is not rendered'
                          for x in ast.walk(n)))
        # Execute the actual rendering/retry branch, without asset writes or network access.
        loop = ast.For(target=ast.Name(id='asset', ctx=ast.Store()),
                       iter=ast.Name(id='candidates', ctx=ast.Load()), body=[branch], orelse=[])
        cls.code = compile(ast.fix_missing_locations(ast.Module(body=[loop], type_ignores=[])), '<asset-read-branch>', 'exec')

    def run_branch(self, visible=True, broken=True, succeeds=True):
        asset = Mock()
        asset.is_visible.return_value = visible
        asset.element_handle.return_value = object()
        def evaluate(script):
            if script == "n => n.localName === 'img'":
                return True
            if 'n.complete' in script:
                return broken
            if 'n.src' in script:
                asset.reloaded_url = self.source_url
                return None
            raise AssertionError('Unexpected asset script: ' + script)
        asset.evaluate.side_effect = evaluate
        player = Mock()
        player.page.wait_for_function.side_effect = [PlaywrightTimeout('broken image'), None if succeeds else PlaywrightTimeout('still broken')]
        item = {'errors': []}
        namespace = {'self': player, 'candidates': [asset], 'item': item, 'index': 0,
                     'PlaywrightTimeout': PlaywrightTimeout}
        exec(self.code, namespace)
        return asset, player, item

    def test_saved_broken_image_can_recover(self):
        self.assertIn('Visual asset is not rendered', self.saved_errors)
        asset, player, item = self.run_branch()
        self.assertEqual(item['errors'], [])
        player.pacer.backoff.assert_called_once_with(1)
        self.assertEqual(asset.reloaded_url, self.source_url)
        self.assertEqual(player.page.wait_for_function.call_count, 2)

    def test_persistent_failure_still_rejects_extraction(self):
        asset, player, item = self.run_branch(succeeds=False)
        self.assertIn('Visual asset is not rendered', item['errors'])
        self.assertEqual(player.page.wait_for_function.call_count, 2)

    def test_hidden_asset_is_not_reloaded(self):
        asset, player, item = self.run_branch(visible=False)
        self.assertIn('Visual asset is not rendered', item['errors'])
        player.pacer.backoff.assert_not_called()
        self.assertNotIn('reloaded_url', asset.__dict__)

    def test_pending_image_is_not_reloaded(self):
        asset, player, item = self.run_branch(broken=False)
        self.assertIn('Visual asset is not rendered', item['errors'])
        player.pacer.backoff.assert_not_called()

if __name__ == '__main__':
    unittest.main()
