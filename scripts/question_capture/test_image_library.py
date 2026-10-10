"""Offline image preparation regressions; all files stay in temporary folders."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import hashlib
from io import BytesIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

from PIL import Image
from image_library import (ImageLibrary, ImagePreparationError, capture_html_images,
                           standalone_svg)


def png():
    buffer = BytesIO()
    Image.new('RGB', (3, 2), 'blue').save(buffer, format='PNG')
    return buffer.getvalue()


class ImageLibraryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.library = ImageLibrary(self.root / 'math')
        self.capture = self.root / 'capture'
        self.capture.mkdir()
        self.data = png()
        self.original = self.capture / 'diagram.png'
        self.original.write_bytes(self.data)
        self.digest = hashlib.sha256(self.data).hexdigest()
        self.expected = f'images/{self.digest[:2]}/{self.digest}.png'

    def test_copies_exact_bytes_and_concurrent_publish_has_no_metadata(self):
        with ThreadPoolExecutor(max_workers=8) as executor:
            paths = list(executor.map(lambda _: ImageLibrary(self.root/'math').put_bytes(self.data), range(16)))
        self.assertEqual(set(paths), {self.expected})
        self.assertEqual((self.library.math_root/self.expected).read_bytes(), self.data)
        files = [p for p in self.library.root.rglob('*') if p.is_file()]
        self.assertEqual(files, [self.library.math_root/self.expected])
        self.assertEqual(self.original.read_bytes(), self.data)

    def test_rewrites_all_content_and_image_answers_without_touching_evidence(self):
        image = {'type':'image', 'value':str(self.original)}
        evidence = {'html':'<img src="remote.png">', 'source_url':'https://mathacademy.com/graphic/1',
                    'assets':[{'path':str(self.original), 'sha256':self.digest}]}
        payload = {'questions':[{'problem':f'![]({self.original})',
                                 'worked_solution':f'<img src="{self.original}">',
                                 'answer_fields':[{'type':'radio', 'choices':[image],
                                                   'correct_value':str(self.original)}], **evidence}],
                   'tutorials':[{'content':f'![Diagram]({self.original})'}],
                   'multistep':{'context':f'![]({self.original})'},
                   'canonical_examples':[{'problem':f'![]({self.original})'}]}
        original = deepcopy(payload)
        result = self.library.prepare_content(payload, self.capture)
        self.assertEqual(payload, original)
        question = result['questions'][0]
        self.assertEqual(question['problem'], f'![]({self.expected})')
        self.assertIn(self.expected, question['worked_solution'])
        self.assertEqual(question['answer_fields'][0]['correct_value'], self.expected)
        self.assertEqual(question['answer_fields'][0]['choices'][0]['value'], self.expected)
        for key in evidence:
            self.assertEqual(question[key], original['questions'][0][key])
        self.assertEqual(result['tutorials'][0]['content'], f'![Diagram]({self.expected})')
        self.assertEqual(result['multistep']['context'], f'![]({self.expected})')
        self.assertEqual(result['canonical_examples'][0]['problem'], f'![]({self.expected})')
        self.assertEqual(self.library.prepare_content(result, self.capture), result)

    def test_uses_saved_url_alias_without_network(self):
        assets = self.capture / 'assets'
        assets.mkdir()
        url = 'https://mathacademy.com/graphics/observed.png'
        (assets/'manifest.json').write_text(json.dumps({url:{'path':str(self.original),
            'sha256':self.digest, 'content_type':'image/png'}}))
        self.assertEqual(self.library.prepare_content({'problem':f'![]({url})'}, self.capture),
                         {'problem':f'![]({self.expected})'})

    def test_missing_remote_placeholder_or_malformed_images_are_not_prepared(self):
        for value in ('![](/absent.png)', '![](https://mathacademy.com/graphics/absent.png)',
                      '![](@asset-0@)', '![diagram][unresolved]', '<canvas>', '![](bad file.png)', '![](unfinished'):
            with self.subTest(value=value), self.assertRaises(ImagePreparationError):
                self.library.prepare_content({'problem':value}, self.capture)
        for body, mime in ((b'<!DOCTYPE html><html>Login</html>', 'text/html'),
                           (self.data[:25], 'image/png'), (self.data, 'image/jpeg')):
            with self.subTest(mime=mime), self.assertRaises(ImagePreparationError):
                self.library.put_bytes(body, content_type=mime)
        with self.assertRaises(ImagePreparationError):
            self.library.put_file(self.original, expected_sha256='f'*64)

    def test_detects_corruption_of_existing_destination(self):
        self.library.put_file(self.original)
        (self.library.math_root/self.expected).write_bytes(b'not an image')
        with self.assertRaises(ImagePreparationError):
            self.library.put_file(self.original)
        with self.assertRaises(ImagePreparationError):
            self.library.reference(self.expected)

    def test_inline_svg_includes_shared_defs_and_keeps_geometry(self):
        graphic = '<svg viewBox="0 0 40 50"><use href="#shape" transform="scale(2)"/></svg>'
        definitions = '<svg style="display:none"><defs><g id="shape"><path d="M1 2 L3 4" fill="url(#color)"/></g><linearGradient id="color"><stop offset="0" stop-color="red"/></linearGradient></defs></svg>'
        raw = standalone_svg(graphic, definitions + graphic)
        self.assertIn(b'viewBox="0 0 40 50"', raw)
        self.assertIn(b'id="shape"', raw)
        self.assertIn(b'id="color"', raw)
        self.assertIn(b'M1 2 L3 4', raw)
        self.assertTrue(self.library.put_bytes(raw).endswith('.svg'))
        with self.assertRaises(ImagePreparationError):
            standalone_svg(graphic)

    def test_empty_svg_root_and_wrong_canonical_extension(self):
        self.assertIn(b'xmlns=', standalone_svg('<svg/>'))
        self.library.put_file(self.original)
        wrong = self.expected.replace('.png', '.jpg')
        (self.library.math_root/wrong).write_bytes(self.data)
        with self.assertRaises(ImagePreparationError):
            self.library.reference(wrong)

    def test_svg_missing_defs_and_external_references_are_rejected(self):
        for svg in ('<svg><use href="#missing"/></svg>',
                    '<svg><image href="https://mathacademy.com/graphics/a.png"/></svg>',
                    '<svg><script>alert(1)</script></svg>'):
            with self.subTest(svg=svg), self.assertRaises(ImagePreparationError):
                self.library.put_bytes(svg.encode())

    def test_html_downloads_only_observed_images_and_preserves_evidence(self):
        fetch = Mock(return_value=(self.data, 'image/png'))
        html = '<p>Diagram</p><img src="/graphics/a.png" srcset="/graphics/unused.png 2x">'
        rewritten = capture_html_images(html, page_url='https://mathacademy.com/topics/1',
            fetch_response=fetch, library=self.library, evidence_dir=self.capture)
        fetch.assert_called_once_with('https://mathacademy.com/graphics/a.png')
        self.assertIn(self.expected, rewritten)
        self.assertNotIn('srcset', rewritten)
        self.assertEqual((self.capture/'assets'/Path(self.expected).name).read_bytes(), self.data)
        with self.assertRaises(ImagePreparationError):
            capture_html_images(html, page_url='https://mathacademy.com/topics/1',
                fetch_response=Mock(side_effect=ValueError('401')), library=self.library)

    def test_html_extracts_svg_but_leaves_accessible_math_to_converter(self):
        html = ('<svg style="display:none"><defs><path id="p" d="M0 0 L2 2"/></defs></svg>'
                '<svg viewBox="0 0 3 3"><use href="#p"/></svg>'
                '<mjx-container><svg><title>x^2</title><path d="M1 1"/></svg></mjx-container>')
        fetch = Mock()
        rewritten = capture_html_images(html, page_url='https://mathacademy.com/topics/1',
                                         fetch_response=fetch, library=self.library)
        fetch.assert_not_called()
        self.assertIn('images/', rewritten)
        self.assertIn('<title>x^2</title>', rewritten)
        self.assertNotIn('display:none', rewritten)
        self.assertEqual(len(list(self.library.root.rglob('*.svg'))), 1)


if __name__ == '__main__':
    unittest.main()
