() => {
  const visible = n => !!n?.getClientRects().length && getComputedStyle(n).visibility !== 'hidden';
  const first = selector => [...document.querySelectorAll(selector)].find(visible);
  const hasContent = n => !!n && (!!n.textContent.trim() || !!n.querySelector('img,canvas,svg'));
  // MA inserts the next step before its prompt, answer fields and MathJax are
  // ready. Keep that step's identity while the adapter waits to read it.
  const mathReady = n => [...n.querySelectorAll('mjx-container')]
    .every(m => !!m.querySelector('mjx-assistive-mml math,svg'));
  const tutorialReady = n => {
    const content=n.cloneNode(true);
    content.querySelectorAll('.stepName,button,[id^="continueButton-"]').forEach(x=>x.remove());
    return hasContent(content) && mathReady(n);
  };
  const questionReady = (n, continuation=null) => {
    const grade = n.querySelector('.questionWidget-result,.correctAnswerText,.incorrectAnswerText')?.textContent.trim();
    // A restored grade can replace its editable fields with static content.
    if (grade || visible(continuation)) {
      const solution=n.querySelector('.questionWidget-explanation,.questionExplanation');
      return mathReady(n) && (!solution || hasContent(solution));
    }
    return hasContent(n.querySelector('.questionWidget-text,.questionText')) && mathReady(n) &&
      !!n.querySelector('.questionWidget-choiceLetterCircle,.choiceLetterCircle,.matheditor-wrapper-answer,.selectList,input:not([type="hidden"]),textarea,select,[contenteditable="true"]');
  };
  const identifier = n => {
    if (!n) return null;
    if (n.id) return '#' + CSS.escape(n.id);
    const path = [];
    for (let node=n; node && node.localName !== 'html'; node=node.parentElement) {
      if (node.id) { path.unshift('#'+CSS.escape(node.id)); break; }
      const peers = node.parentElement ? [...node.parentElement.children].filter(p=>p.localName===node.localName) : [node];
      path.unshift(node.localName+':nth-of-type('+(peers.indexOf(node)+1)+')');
    }
    return path.join(' > ');
  };
  const terminal = first('#finalScreen');
  // A failed stylesheet can expose the empty final-screen template while the
  // first question is still unanswered. Its Continue button is not completion.
  const terminalMessages = terminal && [...terminal.querySelectorAll('#finalScreen-completionMessage,#finalScreen-pointsMessage')];
  const terminalReady = terminal && (!terminalMessages.length || terminalMessages.some(hasContent));
  if (terminalReady || /\/diagnostics\/\d+\/analysis(?:[?#]|$)/.test(location.href))
    return {kind:'complete',selector:terminal ? identifier(terminal) : 'body',key:'complete',accepted:true};
  const start = first('#initialScreen-startButton, #startButton');
  if (start) return {kind:'instructions',selector:identifier(start.closest('#initialScreen, #screen')) || 'body',
                    key:'start',action:'start',button:identifier(start)};
  const retry = first('#retryScreen-noButton');
  if (retry) return {kind:'instructions',selector:'#retryScreen',key:'retry',action:'decline_retry',button:identifier(retry)};
  const diagnostic = first('#questionContainer');
  if (diagnostic) {
    const title = diagnostic.querySelector('.questionWidget-title')?.textContent || '';
    const position = Number(title.match(/Question\s+(\d+)/)?.[1]) || null;
    const grade = diagnostic.querySelector('.questionWidget-result')?.textContent.trim();
    const next = first('#nextButton, #doneButton');
    return {kind:'question',selector:'#questionContainer',key:'diagnostic-'+position,
            sequence_position:position,accepted:!!grade,grade,ready:questionReady(diagnostic,next),
            next:identifier(next)};
  }
  const questions = [...document.querySelectorAll('#questions > .question')];
  if (questions.length) return {kind:'assessment',ids:questions.map(n=>n.id),
    question_ready:Object.fromEntries(questions.map(n=>[n.id,questionReady(n)])),
    navigator:[...document.querySelectorAll('#questionNavigator .questionButton')].map(n=>n.id)};
  // Lesson/review has one currently served widget; older steps remain in the DOM.
  let active = [...document.querySelectorAll('.step.questionWidget')].filter(n => visible(n) &&
    visible(n.querySelector('.questionWidget-submitButton')) && !n.querySelector('.questionWidget-result')?.textContent.trim());
  let current = active.length === 1 ? active[0] : null;
  const continuing = [...document.querySelectorAll('[id^="continueButton-"]')].filter(visible);
  if (!current && continuing.length === 1) {
    const token = continuing[0].id.replace('continueButton-','');
    current = document.getElementById('step-'+token);
  }
  // Multistep's sidebar can select its shared setup while the first question
  // is already answerable. Prefer served controls to that scroll selection.
  if (!current) current = [...document.querySelectorAll('#steps > .step')].find(n => visible(n) &&
    (visible(n.querySelector('.submitButton')) || visible(n.querySelector('[id^="continueButton-"]'))));
  if (!current) {
    const button = document.querySelector('.stepButton.current');
    if (button) current = document.getElementById(button.id.replace('stepButton-','step-'));
  }
  if (current) {
    const question = current.matches('.questionWidget') ? current : current.querySelector('.question');
    const token = current.id.replace('step-','');
    const grade = question?.querySelector('.questionWidget-result,.correctAnswerText,.incorrectAnswerText')?.textContent.trim();
    const name = current.querySelector('.stepName,.questionWidget-title')?.textContent.trim();
    const sourceSteps = [...document.querySelectorAll('#steps > .step')];
    const earlier = sourceSteps.slice(0, sourceSteps.indexOf(current));
    const example = earlier.reverse().find(n => /^step-e\d+$/.test(n.id) || n.getAttribute('steptype') === 'example');
    const exampleId = example?.id.match(/^step-e(\d+)$/)?.[1] || example?.getAttribute('contentid');
    let kind = question ? 'question' : current.querySelector('.exampleQuestion') || /^e\d+$/.test(token) ? 'example' : 'tutorial';
    const next = first('#'+CSS.escape('continueButton-'+token));
    const ready = kind === 'question' ? questionReady(question,next) : kind === 'example' ?
      hasContent(current.querySelector('.exampleQuestion')) &&
      hasContent(current.querySelector('.exampleExplanation')) && mathReady(current) : tutorialReady(current);
    return {kind,selector:identifier(question || current),step_id:current.id,ready,
      key:current.id,accepted:!!grade,grade,name,
      source_example_id:exampleId ? 'e-'+exampleId : null,
      knowledge_point:example?.querySelector('.stepName')?.textContent.trim(),
      next:identifier(next),
      source_step:{dom_id:current.id, placement_id:current.getAttribute('stepid'),
       content_id:current.getAttribute('contentid'), type:current.getAttribute('steptype')}};
  }
  const reload = first('#messageBox');
  return {kind:'unknown',selector:'body',key:'unknown',
    reload_required:!!reload && /Reload Required/.test(reload.textContent),
    buttons:[...document.querySelectorAll('button,a,[role="button"],.button')].filter(visible)
      // Navigation links are not activity recovery actions. Keep real buttons
      // and local continuation anchors, including MA's anchor-styled buttons.
      .filter(n => n.localName !== 'a' || !n.getAttribute('href') ||
        n.getAttribute('href') === '#' || /^javascript:/i.test(n.getAttribute('href')))
      .map(n=>({selector:identifier(n),text:n.textContent.trim()})).filter(n=>n.text)};
}
