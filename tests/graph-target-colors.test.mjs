import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

// Exercise SVG styling and minimap rendering without opening the UI or writing learner data.
const html = await readFile(new URL('../ui/Math-Academy-Graph-Explorer.html', import.meta.url), 'utf8');
const statusPaletteSource = html.slice(html.indexOf('  const STATUS_PALETTES ='), html.indexOf('  let snapshot ='));
const colors = html.slice(html.indexOf('  function competencyFor('), html.indexOf('  function updateCompetencyReadout('));
const minimapSource = html.slice(html.indexOf('  function drawMinimap('), html.indexOf("  minimap.addEventListener('click'"));
const changed = html.slice(html.indexOf('    onChange: learner => {') + '    onChange: learner => {'.length, html.indexOf('\n    },\n  });'));
const queueStart = html.indexOf('    onChange: learner => {', html.indexOf('  const queueControls ='));
const queueChanged = html.slice(queueStart + '    onChange: learner => {'.length, html.indexOf('\n    },\n  });', queueStart));

function fixture() {
  const elements = new Map();
  const nodes = [1, 2, 3].map(id => ({ id, name: `Topic ${id}`, layer: 0 }));
  function createElement() {
    const node = { dataset: {}, attrs: {}, styles: {}, children: [], classList: { toggle() {} },
      setAttribute(key, value) { this.attrs[key] = value; }, appendChild(child) { this.children.push(child); } };
    node.style = { setProperty(key, value) { node.styles[key] = value; } };
    return node;
  }
  for (const id of ['targetColorToggle', 'targetActions', 'statusColorLegend', 'targetMasteryRamp',
    'completedTargetMasteryRamp', 'queueMasteryRamp', 'competencyFillDescription', ...nodes.map(node => 'topic-' + node.id)]) {
    elements.set(id, createElement());
  }
  const fills = [], storage = new Map();
  const ctx = { save() {}, restore() {}, translate() {}, scale() {}, setLineDash() {}, strokeRect() {},
    fillRect(x) { if (x > 0) fills.push(this.fillStyle); },
  };
  const c = vm.createContext({
    $: id => elements.get(id), document: { getElementById: id => elements.get(id), createElement },
    PALETTE: ['#000000', '#303030', '#5A5A5A', '#858585', '#AEAEAE', '#D6D6D6', '#FFFFFF'],
    repetitions: { 1: 5, 2: 2 }, snapshot: { learner: { targets: [1, '3'], selfDirected: false } },
    colorCodeEnabled: false, targetColorKey: 'test-graph-color', light: false,
    isLightTheme: () => c.light, themeColor: color => color, layerLabel: () => 'L01',
    state: { activeIds: new Set([2]), selected: 2, view: { x: 0, y: 0, k: 1 }, width: 100, height: 100,
      layout: { activeNodes: nodes, activeLinks: [], bounds: { x1: 0, y1: 0, x2: 300, y2: 100 },
        pos: new Map(nodes.map(node => [node.id, { x: node.id * 60, y: 10, w: 50, h: 30 }])) } },
    minimapLayout: null, minimap: { width: 440, height: 280 },
    minimapBase: { width: 0, height: 0, getContext: () => ctx },
    mctx: { clearRect() {}, drawImage() {}, strokeRect() {} },
    localStorage: { setItem: (key, value) => storage.set(key, value) },
    targetsView: false, loading: false, targetTopicId: null,
    // This fixture models focused exploration; full root changes are covered
    // by targets-graph.test.mjs.
    refreshTargetScope() { c.refreshTargetColors(); },
    targetControls: { setLearner: learner => c.learnerChanged(learner) },
  });
  vm.runInContext(statusPaletteSource + colors + minimapSource + `\nfunction learnerChanged(learner) { ${changed} }\nfunction queueChanged(learner) { ${queueChanged} }`, c);
  return { c, elements, fills, storage };
}

test('returning from a completed lesson refreshes mastery without moving the graph', async () => {
  const { c, elements } = fixture();
  c.snapshot.learner.id = 'test';
  c.snapshot.learner.queue = [1, 2];
  c.snapshot.learned = { 1: false, 2: false };
  c.setColorCode(true);
  const layout = c.state.layout, view = c.state.view;
  const progressSource = html.slice(html.indexOf('  let progressRefresh=null;'), html.indexOf("  window.addEventListener('focus',refreshLearningProgress);"));
  let reads = 0, readouts = 0;
  c.readRequest = async () => {
    reads++;
    return { ok: true, json: async () => ({ learner: { id: 'test' }, repetitions: { 1: 4, 2: 3 }, learned: { 1: true, 2: true } }) };
  };
  c.updateCompetencyReadout = () => { readouts++; };
  vm.runInContext(progressSource, c);
  c.queueChanged({ queue: [] });
  await Promise.all([c.refreshLearningProgress(), c.refreshLearningProgress()]);
  assert.equal(reads, 1);
  assert.equal(readouts, 1);
  assert.equal(c.nodeAppearance(1).status, 'completed-target');
  assert.equal(c.nodeAppearance(2).status, null);
  assert.equal(elements.get('topic-2').styles['--node'], c.competencyFor(2).fill);
  assert.equal(c.state.layout, layout);
  assert.equal(c.state.view, view);
  c.document.hidden = true;
  await c.refreshLearningProgress();
  assert.equal(reads, 1);
});

test('Color Code toggles red, green, and blue together in both graph views and themes', () => {
  assert.match(html, />Color Code<\/label>/);
  const { c, elements, fills, storage } = fixture();
  c.snapshot.learner.queue = [2];
  const layout = c.state.layout, view = c.state.view;
  const membership = JSON.stringify(c.snapshot.learner), node = elements.get('topic-1');
  for (const targetsView of [false, true]) for (const light of [false, true]) {
    c.targetsView = targetsView; c.light = light; c.setColorCode(true);
    const expected = light ? ['#13713d', '#8fb3f2', '#f8dadd'] : ['#2a8851', '#183c82', '#4b1118'];
    for (const [i, id] of [1, 2, 3].entries()) {
      assert.equal(elements.get('topic-' + id).styles['--node'], expected[i]);
      assert.equal(elements.get('topic-' + id).styles['--node-border'], c.nodeAppearance(id).border);
    }
    assert.deepEqual(fills.slice(-3), expected);
    assert.equal(elements.get('targetColorToggle').attrs['aria-checked'], 'true');
    c.setColorCode(false);
    for (const id of [1, 2, 3]) assert.equal(elements.get('topic-' + id).styles['--node'], c.competencyFor(id).fill);
    assert.equal(elements.get('targetColorToggle').attrs['aria-checked'], 'false');
  }
  assert.equal(storage.get('test-graph-color'), 'false');
  assert.equal(c.state.layout, layout); assert.equal(c.state.view, view); assert.equal(elements.get('topic-1'), node);
  assert.equal(JSON.stringify(c.snapshot.learner), membership);
});

test('green requires completion AND target membership; completed prerequisites keep default coloring', () => {
  const { c, elements } = fixture(); c.snapshot.learned = { 2: true };
  for (const targetsView of [false, true]) {
    c.targetsView = targetsView; c.setColorCode(true);
    assert.equal(c.nodeAppearance(1).status, 'completed-target');
    assert.equal(c.nodeAppearance(1).fill, '#2a8851');
    assert.equal(c.nodeAppearance(2).target, false);
    assert.equal(c.nodeAppearance(2).fill, c.competencyFor(2).fill);
    assert.doesNotMatch(elements.get('topic-2').attrs['aria-label'], /Completed target/);
  }
  c.snapshot.learner.targets.push(2); c.refreshTargetColors();
  assert.equal(c.nodeAppearance(2).fill, '#0d5734');
  assert.match(elements.get('topic-2').attrs['aria-label'], /Completed target/);
  c.snapshot.learner.targets = [3]; c.refreshTargetColors();
  for (const id of [1, 2]) assert.equal(c.nodeAppearance(id).fill, c.competencyFor(id).fill);
});

test('explicit completion flags take precedence; historical repetition evidence is used only when the flag is absent', () => {
  const { c } = fixture(); c.snapshot.learner.targets = [2]; c.setColorCode(true);
  for (const repetitions of [undefined, 0, .5, -1, NaN]) {
    c.repetitions[2] = repetitions;
    assert.equal(c.nodeAppearance(2).status, 'target');
  }
  c.repetitions[2] = 1; assert.equal(c.nodeAppearance(2).status, 'completed-target');
  c.snapshot.learned = { 2: false }; c.repetitions[2] = 10;
  assert.equal(c.nodeAppearance(2).status, 'target');
  assert.equal(c.nodeAppearance(2).fill, '#cf626b');
  c.snapshot.learned[2] = true; c.repetitions[2] = .9938596149152737;
  assert.equal(c.nodeAppearance(2).status, 'completed-target');
  assert.equal(c.nodeAppearance(2).fill, '#093c22');
  assert.equal(c.nodeAppearance(2).repetitions, .9938596149152737);
  delete c.repetitions[2];
  assert.equal(c.nodeAppearance(2).fill, '#093c22');
  assert.equal(c.nodeAppearance(2).dash, '4 3');
});

function luminance(hex) {
  const rgb = hex.match(/[0-9a-f]{2}/gi).map(channel => parseInt(channel, 16) / 255);
  const linear = rgb.map(channel => channel <= .04045 ? channel / 12.92 : ((channel + .055) / 1.055) ** 2.4);
  return linear.reduce((sum, channel, i) => sum + channel * [.2126, .7152, .0722][i], 0);
}

test('band six uses the former band four fill, with the former band five outline in each theme', () => {
  const { c } = fixture();
  const endpoints = {
    target: { dark: ['#4b1118', '#cf626b', '#e5a0a6'], light: ['#f8dadd', '#8c202b', '#681821'] },
    'completed-target': { dark: ['#093c22', '#56a978', '#9edbb4'], light: ['#def4e5', '#10633b', '#0c5130'] },
    queue: { dark: ['#102653', '#628fec', '#a6c5f5'], light: ['#e1ecfc', '#1b459c', '#173775'] },
  };
  for (const [status, themes] of Object.entries(endpoints)) for (const light of [false, true]) {
    c.light = light;
    const [zero, six, border] = themes[light ? 'light' : 'dark'];
    assert.equal(c.statusMasteryAppearance(status, { known: true, level: 0 }).fill, zero);
    assert.equal(c.statusMasteryAppearance(status, { known: true, level: 6 }).fill, six);
    for (let level = 0; level <= 6; level++) {
      assert.equal(c.statusMasteryAppearance(status, { known: true, level }).border, border);
    }
    assert.equal(c.statusMasteryAppearance(status, { known: false, level: null }).border, border);
  }
});

test('each status has distinct mastery bands, reverses shade progression with theme, and keeps readable text and data outlines', () => {
  const { c } = fixture(); c.snapshot.learner.targets = [1]; c.snapshot.learned = { 1: false }; c.setColorCode(true);
  for (const status of ['target', 'completed-target', 'queue']) for (const light of [false, true]) {
    c.light = light; c.snapshot.learned[1] = status === 'completed-target';
    c.snapshot.learner.queue = status === 'queue' ? [1] : [];
    const appearances = [];
    for (let level = 0; level <= 6; level++) {
      c.repetitions[1] = level;
      const appearance = c.nodeAppearance(1); appearances.push(appearance);
      assert.equal(appearance.status, status); assert.equal(appearance.level, level);
      assert.equal(appearance.dash, 'none'); assert.equal(appearance.repetitions, level);
      const a = luminance(appearance.fill), b = luminance(appearance.text);
      assert.ok((Math.max(a, b) + .05) / (Math.min(a, b) + .05) >= 4.5, status + ': unreadable text at ' + level);
    }
    assert.equal(new Set(appearances.map(appearance => appearance.fill)).size, 7);
    for (let i = 1; i < appearances.length; i++) {
      assert.ok(light ? luminance(appearances[i].fill) < luminance(appearances[i - 1].fill)
        : luminance(appearances[i].fill) > luminance(appearances[i - 1].fill));
    }
    c.repetitions[1] = 60; assert.equal(c.nodeAppearance(1).fill, appearances[6].fill);
    delete c.repetitions[1];
    const unknown = c.nodeAppearance(1);
    assert.equal(unknown.known, false); assert.equal(unknown.level, null);
    assert.equal(unknown.dash, '4 3'); assert.equal(unknown.fill, appearances[0].fill);
  }
});

test('color legend mirrors the node shades and hides when coloring is off', () => {
  const { c, elements } = fixture();
  for (const light of [false, true]) {
    c.light = light; c.setColorCode(true);
    assert.equal(elements.get('statusColorLegend').hidden, false);
    for (const [status, id] of [['target', 'targetMasteryRamp'], ['completed-target', 'completedTargetMasteryRamp'], ['queue', 'queueMasteryRamp']]) {
      const cells = elements.get(id).children; assert.equal(cells.length, 7);
      for (let level = 0; level <= 6; level++) {
        const expected = c.statusMasteryAppearance(status, { known: true, level });
        assert.equal(cells[level].styles['--swatch-fill'], expected.fill);
        assert.equal(cells[level].styles['--swatch-text'], expected.text);
        assert.equal(cells[level].styles['--swatch-border'], expected.border);
      }
    }
    assert.match(elements.get('competencyFillDescription').textContent, /green marks completed targets/);
  }
  c.setColorCode(false); assert.equal(elements.get('statusColorLegend').hidden, true);
  assert.match(elements.get('competencyFillDescription').textContent, /Every topic uses grayscale/);
});

test('queue updates repaint focused exploration; removal restores target status or default prerequisite coloring', () => {
  const { c, elements, fills } = fixture(); c.targetsView = true; c.setColorCode(true);
  const layout = c.state.layout, view = c.state.view;
  c.queueChanged({ queue: [1, 2, '3', 99] });
  assert.deepEqual(fills.slice(-3), ['#3464df', '#183c82', '#102653']);
  for (const id of [1, 2, 3]) assert.match(elements.get('topic-' + id).attrs['aria-label'], /In queue/);
  c.queueChanged({ queue: [] });
  assert.deepEqual(fills.slice(-3), ['#2a8851', '#5A5A5A', '#4b1118']);
  assert.equal(c.state.layout, layout); assert.equal(c.state.view, view);
  c.queueChanged({ queue: [3] });
  c.learnerChanged({ ...c.snapshot.learner, queue: [] });
  assert.equal(elements.get('topic-3').styles['--node'], '#102653');
  c.queueChanged({ queue: [] }); assert.equal(elements.get('topic-3').styles['--node'], '#4b1118');
});

test('membership changes repaint a newly completed target and do not require browser storage', () => {
  const { c, elements, fills } = fixture(); c.setColorCode(true);
  c.learnerChanged({ targets: [2], selfDirected: false });
  assert.equal(elements.get('topic-1').styles['--node'], c.competencyFor(1).fill);
  assert.deepEqual(fills.slice(-3), ['#D6D6D6', '#0d5734', '#000000']);
  c.localStorage.setItem = () => { throw Error('Unavailable'); };
  c.setColorCode(false); assert.equal(elements.get('targetColorToggle').attrs['aria-checked'], 'false');
});

test('Color Code preserves the former switch preference and prioritizes the new setting', () => {
  const preferenceSource = html.slice(html.indexOf('  const targetColorKey ='), html.indexOf('  let targetTopicId ='));
  for (const [values, expected] of [
    [{}, false], [{ 'course-academy.graph-targets-red': 'true' }, true],
    [{ 'course-academy.graph-targets-red': 'false' }, false],
    [{ 'course-academy.graph-targets-red': 'true', 'course-academy.graph-color-code': 'false' }, false],
    [{ 'course-academy.graph-color-code': 'true' }, true],
  ]) {
    const c = vm.createContext({ localStorage: { getItem: key => values[key] ?? null } });
    vm.runInContext(preferenceSource, c); assert.equal(vm.runInContext('colorCodeEnabled', c), expected);
  }
  const c = vm.createContext({ localStorage: { getItem() { throw Error('Unavailable'); } } });
  vm.runInContext(preferenceSource, c); assert.equal(vm.runInContext('colorCodeEnabled', c), false);
});


test('minimap starts a new subpath at each distant stub instead of drawing a phantom long connection', () => {
  const { c }=fixture();const commands=[];
  c.minimapBase.getContext=()=>({
    save(){},restore(){},translate(){},scale(){},fillRect(){},strokeRect(){},setLineDash(){},stroke(){},
    beginPath(){commands.push('begin');},moveTo(...point){commands.push(['move',...point]);},
    bezierCurveTo(...points){commands.push(['curve',...points]);},
  });
  c.state.layout.activeLinks=[{segments:[
    {p0:[80,20],c1:[98,20],c2:[116,20],p1:[134,20]},
    {p0:[806,100],c1:[824,100],c2:[842,100],p1:[860,100]},
  ]}];
  c.drawMinimap();
  assert.deepEqual(commands.filter(command=>Array.isArray(command)&&command[0]==='move'),[['move',80,20],['move',806,100]]);
  assert.equal(commands.filter(command=>Array.isArray(command)&&command[0]==='curve').length,2);
});
