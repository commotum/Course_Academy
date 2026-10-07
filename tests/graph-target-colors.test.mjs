import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

// Exercise SVG styling and minimap rendering without opening the UI or writing learner data.
const html = await readFile(new URL('../ui/Math-Academy-Graph-Explorer.html', import.meta.url), 'utf8');
const colors = html.slice(html.indexOf('  function competencyFor('), html.indexOf('  function updateCompetencyReadout('));
const minimapSource = html.slice(html.indexOf('  function drawMinimap('), html.indexOf("  minimap.addEventListener('click'"));
const changed = html.slice(html.indexOf('    onChange: learner => {') + '    onChange: learner => {'.length, html.indexOf('\n    },\n  });'));

function fixture() {
  const elements = new Map();
  const nodes = [1, 2, 3].map(id => ({ id, name: `Topic ${id}`, layer: 0 }));
  for (const id of ['targetColorToggle', 'targetActions', ...nodes.map(node => 'topic-' + node.id)]) {
    elements.set(id, { dataset: {}, attrs: {}, styles: {}, classList: { toggle() {} },
      setAttribute(key, value) { this.attrs[key] = value; },
      style: { setProperty(key, value) { elements.get(id).styles[key] = value; } },
    });
  }
  const fills = [], storage = new Map();
  const ctx = { save() {}, restore() {}, translate() {}, scale() {}, setLineDash() {}, strokeRect() {},
    fillRect(x) { if (x > 0) fills.push(this.fillStyle); },
  };
  const c = vm.createContext({
    $: id => elements.get(id), document: { getElementById: id => elements.get(id) },
    PALETTE: ['#000000', '#303030', '#5A5A5A', '#858585', '#AEAEAE', '#D6D6D6', '#FFFFFF'],
    repetitions: { 1: 5, 2: 2 }, snapshot: { learner: { targets: [1, '3'], selfDirected: false } },
    targetsInRed: false, targetColorKey: 'test-graph-color', light: false,
    isLightTheme: () => c.light, themeColor: color => color, layerLabel: () => 'L01',
    state: { activeIds: new Set([2]), selected: 2, view: { x: 0, y: 0, k: 1 }, width: 100, height: 100,
      layout: { activeNodes: nodes, activeLinks: [], bounds: { x1: 0, y1: 0, x2: 300, y2: 100 },
        pos: new Map(nodes.map(node => [node.id, { x: node.id * 60, y: 10, w: 50, h: 30 }])) } },
    minimapLayout: null, minimap: { width: 440, height: 280 },
    minimapBase: { width: 0, height: 0, getContext: () => ctx },
    mctx: { clearRect() {}, drawImage() {}, strokeRect() {} },
    localStorage: { setItem: (key, value) => storage.set(key, value) },
    targetsView: false, loading: false, targetTopicId: null,
  });
  vm.runInContext(colors + minimapSource + `\nfunction learnerChanged(learner) { ${changed} }`, c);
  return { c, elements, fills, storage };
}

test('saved targets turn red in both themes without changing mastery, selection, layout, or node elements', () => {
  const { c, elements, fills, storage } = fixture();
  const layout = c.state.layout, view = c.state.view, target = elements.get('topic-1');
  const original = c.competencyFor(1);
  c.setTargetColors(true);
  assert.equal(elements.get('targetColorToggle').attrs['aria-checked'], 'true');
  assert.equal(storage.get('test-graph-color'), 'true');
  assert.equal(target.styles['--node'], '#b52b34');
  assert.equal(target.styles['--node-text'], '#FFFFFF');
  assert.equal(elements.get('topic-2').styles['--node'], c.competencyFor(2).fill);
  assert.equal(elements.get('topic-3').styles['--node'], '#b52b34');
  assert.equal(elements.get('topic-3').styles['--competency-dash'], '4 3');
  assert.match(target.attrs['aria-label'], /Study target/);
  assert.deepEqual(fills.slice(-3), ['#b52b34', '#5A5A5A', '#b52b34']);
  assert.deepEqual(c.competencyFor(1), original);
  c.light = true; c.refreshTargetColors();
  assert.equal(target.styles['--node'], '#b52b34');
  assert.equal(target.styles['--node-text'], '#FFFFFF');
  c.setTargetColors(false);
  assert.equal(target.styles['--node'], c.competencyFor(1).fill);
  assert.equal(elements.get('targetColorToggle').attrs['aria-checked'], 'false');
  assert.equal(c.state.layout, layout); assert.equal(c.state.view, view);
  assert.equal(elements.get('topic-1'), target);
  assert.deepEqual([...c.state.activeIds], [2]);
});

test('target membership updates repaint the current graph and invalidate the minimap cache', () => {
  const { c, elements, fills } = fixture();
  c.setTargetColors(true);
  c.learnerChanged({ targets: [2], selfDirected: false });
  assert.equal(elements.get('topic-1').styles['--node'], c.competencyFor(1).fill);
  assert.equal(elements.get('topic-2').styles['--node'], '#b52b34');
  assert.deepEqual(fills.slice(-3), ['#D6D6D6', '#b52b34', '#000000']);
  c.localStorage.setItem = () => { throw new Error('Unavailable'); };
  c.setTargetColors(false);
  assert.equal(elements.get('targetColorToggle').attrs['aria-checked'], 'false');
});


test('Targets renders all studied topics green in both themes, ahead of red target coloring', () => {
  const { c, elements, fills } = fixture(); c.targetsView = true;
  for (const light of [false, true]) {
    c.light = light;
    for (const red of [false, true]) {
      c.setTargetColors(red);
      // One target and one visible prerequisite that is not a target.
      for (const id of [1, 2]) {
        const node = elements.get('topic-' + id);
        assert.equal(node.styles['--node'], '#14783e');
        assert.equal(node.styles['--node-text'], '#FFFFFF');
        assert.match(node.attrs['aria-label'], /Already studied/);
      }
      assert.equal(elements.get('topic-3').styles['--node'], red ? '#b52b34' : '#000000');
      assert.deepEqual(fills.slice(-3), ['#14783e', '#14783e', red ? '#b52b34' : '#000000']);
    }
  }
  c.targetsView = false; c.setTargetColors(false);
  assert.equal(elements.get('topic-1').styles['--node'], c.competencyFor(1).fill);
  assert.doesNotMatch(elements.get('topic-1').attrs['aria-label'], /Already studied/);
});

test('green status uses at least one repetition, leaving zero, fractional and missing records unchanged', () => {
  const { c } = fixture(); c.targetsView = true;
  for (const value of [undefined, 0, .5, -1, NaN]) {
    c.repetitions[2] = value;
    assert.equal(c.nodeAppearance(2).fill, c.competencyFor(2).fill);
  }
  c.repetitions[2] = 1;
  assert.equal(c.nodeAppearance(2).fill, '#14783e');
  assert.equal(c.competencyFor(2).repetitions, 1);
});


test('explicit learned status colors a completed local lesson green with a fractional repetition score', () => {
  const { c, elements } = fixture(); c.targetsView = true;
  c.repetitions[1] = 0.9938596149152737;
  c.snapshot.learned = { 1: true, 2: false };
  for (const light of [false, true]) {
    c.light = light; c.setTargetColors(true);
    assert.equal(elements.get('topic-1').styles['--node'], '#14783e');
    assert.match(elements.get('topic-1').attrs['aria-label'], /Already studied/);
    assert.equal(c.competencyFor(1).repetitions, 0.9938596149152737);
  }
  // Imported topics without a learned flag still use their repetition evidence.
  c.repetitions[2] = 1;
  assert.equal(c.nodeAppearance(2).fill, '#14783e');
  c.repetitions[2] = .9;
  assert.equal(c.nodeAppearance(2).fill, c.competencyFor(2).fill);
  c.snapshot.learned[2] = true; delete c.repetitions[2];
  assert.equal(c.nodeAppearance(2).fill, '#14783e');
});
