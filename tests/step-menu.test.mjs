import assert from 'node:assert/strict';
import test from 'node:test';
import { stepEntityId, academyEntityId } from '../ui/step-menu.js';

test('database IDs preserve exact digits and reject UUIDs or rounded numbers', () => {
  assert.equal(academyEntityId('q-123'), 'q-123');
  assert.equal(academyEntityId('e-456'), 'e-456');
  assert.equal(academyEntityId('arbitrary-text'), null);
  assert.equal(stepEntityId(17592186157459), '17592186157459');
  assert.equal(stepEntityId('18446744073709551615'), '18446744073709551615');
  for (const value of [null, undefined, '', 0, -1, 1.5, Number.MAX_SAFE_INTEGER + 1, 'abc', 'step-1', '1e3']) {
    assert.equal(stepEntityId(value), null);
  }
});

// Interaction, nested identity, clipboard, dialog and keyboard coverage lives
// in entity-menu-browser.cjs against the real shared renderer and browser DOM.
