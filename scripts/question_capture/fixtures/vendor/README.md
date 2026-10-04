# Offline MathQuill regression dependencies

- `mathquill-ma.v2.1.min.js`: the public distribution loaded by Math Academy,
  downloaded from https://mathacademy.com/js/mathquill.v2.1.min.js on 2026-10-03.
  Its filename is retained; no upstream release version is inferred from it.
  Upstream MathQuill is licensed under MPL-2.0: https://github.com/mathquill/mathquill.
- `mathquill-0.10.1.css`: stylesheet from the `mathquill@0.10.1` npm package,
  under MPL-2.0. Its license notice is preserved in the file.
- `jquery-3.7.1.min.js`: https://code.jquery.com/jquery-3.7.1.min.js, MIT license;
  its license notice is preserved in the file.

These fixtures run in an offline Playwright context. Production entry uses
ordinary typing and visible symbol-menu clicks. Tests use the public API only
to initialize a local editor and implement a fixture symbol button; verification
uses the documented read-only `.latex()` getter.
