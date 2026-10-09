import copy
import json
import unittest
from pathlib import Path
from unittest.mock import Mock

from bs4 import BeautifulSoup
from browser import CaptureBrowser

EVIDENCE = Path(__file__).parent / 'fixtures/reload-required-14061012'


class ReloadRequiredRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        html = BeautifulSoup((EVIDENCE / 'page.html').read_text(), 'html.parser')
        cls.title = html.select_one('#messageBox-title').get_text(strip=True)
        cls.message = html.select_one('#messageBox-message').get_text(strip=True)
        assert cls.title == 'Reload Required'
        assert cls.message == 'Something has changed that requires the page to reload.'
        assert 'visibility: visible' in html.select_one('#messageBox')['style']
        # This is the diagnostic's original checkpoint, before live recovery
        # changed the activity state to graded/completed.
        cls.state = json.loads((EVIDENCE / 'state.json').read_text())
        assert cls.state['task_id'] == 14061012
        assert cls.state['questions']['q-318979']['status'] == 'submitting'
        cls.url = cls.state['activity_url']

    def reader(self, visible=True, title=None, message=None):
        reader = object.__new__(CaptureBrowser)
        reader.state = copy.deepcopy(self.state)
        reader.page = Mock()
        reader.page.url = self.url
        nodes = {name: Mock() for name in ('#messageBox', '#messageBox-title', '#messageBox-message')}
        nodes['#messageBox'].is_visible.return_value = visible
        nodes['#messageBox-title'].inner_text.return_value = self.title if title is None else title
        nodes['#messageBox-message'].inner_text.return_value = self.message if message is None else message
        reader.page.locator.side_effect = lambda name: nodes[name]
        reader.check, reader.navigate, reader.pacer = Mock(), Mock(), Mock()
        return reader

    def recover(self, reader):
        method = getattr(reader, 'recover_reload_required', None)
        self.assertTrue(callable(method), 'Original reader lacks reload-dialog recovery')
        return method()

    def test_saved_dialog_recovers_without_changing_checkpoint(self):
        reader = self.reader()
        state = copy.deepcopy(reader.state)
        self.assertTrue(self.recover(reader))
        reader.pacer.backoff.assert_called_once_with(1)
        reader.navigate.assert_called_once_with(self.url, force=True)
        self.assertEqual(reader.state, state)
        self.assertFalse(any('click' in str(call) for call in reader.page.mock_calls))

    def test_hidden_or_unrelated_dialog_does_not_trigger_navigation(self):
        for kwargs in ({'visible': False}, {'title': 'Authentication Required'}, {'message': 'Different message'}):
            with self.subTest(kwargs=kwargs):
                reader = self.reader(**kwargs)
                self.assertFalse(self.recover(reader))
                reader.navigate.assert_not_called()
                reader.pacer.backoff.assert_not_called()

    def test_stop_preserves_checkpoint(self):
        reader = self.reader()
        reader.check.side_effect = KeyboardInterrupt('Stopped')
        with self.assertRaises(KeyboardInterrupt):
            self.recover(reader)
        reader.navigate.assert_not_called()
        reader.pacer.backoff.assert_not_called()
        self.assertEqual(reader.state, self.state)
        self.assertFalse(any('click' in str(call) for call in reader.page.mock_calls))


if __name__ == '__main__':
    unittest.main()
