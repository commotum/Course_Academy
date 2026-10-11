"""Answer-field entry with readback; no mathematical answer selection."""
from __future__ import annotations

import json
import re


def by_id(scope, identifier):
    return scope.locator("[id=" + json.dumps(str(identifier)) + "]")


def normalized_math(value):
    """Normalize editor spelling/group notation, without solving the expression."""
    value = re.sub(r"\s+|\\(?:left|right)|\\[,;!:]", "", str(value)).replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac").replace("−", "-")
    value = re.sub(r"\^([A-Za-z0-9])", r"^{\1}", value)
    def group(start):
        if start >= len(value) or value[start] != "{":
            return None
        depth = 1
        end = start + 1
        while end < len(value) and depth:
            depth += (value[end] == "{") - (value[end] == "}")
            end += 1
        return (value[start + 1:end - 1], end) if depth == 0 else None
    output, index = [], 0
    while index < len(value):
        if value.startswith("\\frac", index):
            numerator = group(index + 5)
            denominator = group(numerator[1]) if numerator else None
            if numerator and denominator:
                output.append("(" + normalized_math(numerator[0]) + ")/(" + normalized_math(denominator[0]) + ")")
                index = denominator[1]
                continue
        output.append(value[index]); index += 1
    result = "".join(output)
    atom = r"(?:-?\d+(?:\.\d+)?|-?[A-Za-z](?:\^\{[0-9]+\})?|-?\\(?:pi|theta|alpha|beta|gamma))"
    quotient = re.fullmatch("(" + atom + ")/(" + atom + ")", result)
    if quotient:
        result = "(" + quotient[1] + ")/(" + quotient[2] + ")"
    return result


def validated_keys(actions):
    allowed = {"ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Home", "End", "Space"}
    if not isinstance(actions, list) or len(actions) > 1000:
        raise ValueError("Invalid math editor actions")
    for action in actions:
        if not isinstance(action, dict) or set(action) - {"text", "key"}:
            raise ValueError("Invalid math editor action")
        text, key = action.get("text"), action.get("key")
        if (text is None) == (key is None) or (text is not None and (not isinstance(text, str) or len(text) > 10000)):
            raise ValueError("Each math editor action must supply text or a key")
        if key is not None and key not in allowed:
            raise ValueError("Math editor actions cannot submit or leave a question")
    return actions


MATH_FIELD = r'''node => {
  const library=window.MathQuill;
  const MQ=library?.getInterface ? library.getInterface(2) : library;
  return MQ?.(node.querySelector('.mq-editable-field'));
}'''


def write_math(control, value, keys):
    keys = validated_keys(keys or [])
    try:
        observed = control.evaluate("(node,value) => { const field=(" + MATH_FIELD + ")(node); if(!field || typeof field.write!=='function') throw Error('MathQuill editor not ready'); field.focus(); field.select(); field.write(value); return field.latex(); }", str(value))
    except Exception:
        if not keys:
            raise
        observed = None
    if normalized_math(observed) != normalized_math(value) and keys:
        observed = control.evaluate(r'''(node,actions) => {
          const field=(''' + MATH_FIELD + r''')(node);
          if(!field) throw Error('MathQuill editor not ready');
          field.focus(); field.select(); field.keystroke('Backspace');
          const names={ArrowLeft:'Left',ArrowRight:'Right',ArrowUp:'Up',ArrowDown:'Down'};
          for(const action of actions) {
            if(action.key) field.keystroke(names[action.key] || action.key);
            else for(const part of action.text.split(/(\\[A-Za-z]+)/)) {
              if(!part) continue;
              if(/^\\[A-Za-z]+$/.test(part)) field.cmd(part);
              else field.typedText(part);
            }
          }
          return field.latex();
        }''', keys)
    if normalized_math(observed) != normalized_math(value):
        raise ValueError("Math editor readback differs: " + repr(observed) + " != " + repr(value))
    return observed


def pick_choice(field, response):
    choices = field.get("choices", [])
    value = response.get("value", response.get("correct_value"))
    if value is not None:
        candidates = [c for c in choices if str(c.get("value")) == str(value)]
        if len(candidates) == 1:
            return candidates[0]
        candidates = [c for c in choices if c.get("type") == "math" and normalized_math(c.get("value")) == normalized_math(value)]
        if len(candidates) == 1:
            return candidates[0]
    option = response.get("option")
    candidates = [c for c in choices if str(c.get("option")) == str(option)] if option is not None else []
    if len(candidates) == 1 and (value is None or str(candidates[0].get("value")) == str(value)):
        return candidates[0]
    raise ValueError("Response does not match a current answer choice: " + field["key"])


def choice_content(control):
    """Compare source content regardless of hidden-menu layout or MathJax CSS."""
    return control.evaluate(r'''node => {
      const clean=text=>text.replace(/\s+/g,' ').trim();
      const shape=n=>n.nodeType===Node.TEXT_NODE ? clean(n.textContent) :
        [n.localName, Array.from(n.attributes || []).filter(a=>!['id','class','style'].includes(a.name))
          .map(a=>[a.name,a.value]).sort(), Array.from(n.childNodes).map(shape).filter(v=>v!=='')];
      return {text:clean(node.textContent),
        math:Array.from(node.querySelectorAll('math')).map(shape),
        images:Array.from(node.querySelectorAll('img')).map(n=>n.currentSrc || n.src || n.getAttribute('src'))};
    }''')


def click_dropdown(control, direct=False):
    """Use an exposed source element point; never click through an overlay."""
    control.scroll_into_view_if_needed()
    if direct:
        control.evaluate("n=>n.scrollIntoView({block:'center',inline:'nearest',behavior:'instant'})")
    point = control.evaluate(r'''(n,direct)=>{
      const r=n.getBoundingClientRect();
      if(!n.getClientRects().length || getComputedStyle(n).visibility==='hidden') return null;
      const xs=direct ? [2,r.width-2,4,r.width-4,r.width/2] : [r.width/2,2,r.width-2,4,r.width-4];
      for(const x of xs) for(const y of [2,r.height-2,4,r.height-4,r.height/2]) {
        if(x<=0 || y<=0 || x>=r.width || y>=r.height) continue;
        const hit=document.elementFromPoint(r.left+x,r.top+y);
        if(hit && (hit===n || (!direct && n.contains(hit)))) return {x,y};
      }
      return null;
    }''', direct)
    if point is None:
        raise ValueError("Dropdown has no exposed " + ("frame" if direct else "option") + " click target")
    control.click(position=point)


def verify_entered(scope, question, answers):
    """Read fields again after MA polling and blur, without changing any value."""
    answers = {answer['key']: answer for answer in answers} if isinstance(answers, list) else answers
    verified = []
    for field in question['fields']:
        if field.get('source_result') == 'Correct' or field.get('disabled'):
            continue
        if field['key'] not in answers:
            raise ValueError('Missing entered response for answer field ' + field['key'])
        answer = answers[field['key']]
        value = answer.get('value', answer.get('correct_value', ''))
        if field['type'] in ('radio', 'select'):
            choice = pick_choice(field, answer)
            if field['type'] == 'radio':
                control = by_id(scope, choice['dom_id']) if choice.get('dom_id') else scope.locator(
                    '.questionWidget-choiceLetterCircle,.choiceLetterCircle').nth(field['choices'].index(choice))
                if not control.evaluate("n=>n.classList.contains('selectedChoice') || n.style.backgroundColor==='rgb(64, 64, 64)' || n.getAttribute('aria-checked')==='true'"):
                    raise ValueError('Radio selection changed before submission')
            elif field.get('tag') == 'select':
                if by_id(scope, field['dom_id']).input_value() != str(choice['option']):
                    raise ValueError('Select value changed before submission')
            else:
                control = by_id(scope, field['dom_id']) if field.get('dom_id') else scope.locator('.selectList').nth(field.get('dom_index', 0))
                frame = control.locator('.selectListFrame, .selectListFrameDisabled').first
                expected = answer.get('choice_content')
                if expected is None:
                    option = by_id(control, choice['dom_id']) if choice.get('dom_id') else control.locator(
                        '.selectListOptions > .selectListOption').nth(field['choices'].index(choice))
                    expected = choice_content(option)
                if frame.locator('.selectListSelectedText').count() or choice_content(frame) != expected:
                    raise ValueError('Custom select readback differs before submission')
        elif field.get('tag') == 'mathquill':
            control = scope.locator('.matheditor-wrapper-answer').nth(field.get('dom_index', 0))
            if control.locator('.mq-latex-command-input').count():
                raise ValueError('Unfinished MathQuill command before submission')
            observed = control.evaluate('node=>{const field=(' + MATH_FIELD + ')(node);return field?.latex();}')
            if not isinstance(observed, str) or normalized_math(observed) != normalized_math(value):
                raise ValueError('Math editor value changed before submission: ' + repr(observed) + ' != ' + repr(value))
        else:
            control = by_id(scope, field['dom_id']) if field.get('dom_id') else scope.locator(
                "input:not([type='hidden']),textarea,[contenteditable='true']").nth(field.get('dom_index', 0))
            observed = control.inner_text() if control.get_attribute('contenteditable') == 'true' else control.input_value()
            if observed != str(value):
                raise ValueError('Answer field changed before submission')
        verified.append(answer)
    return verified


def enter(scope, field, response):
    """A replay may refill an unsubmitted response; never repeat a graded one."""
    if field.get("source_result") == "Correct" or field.get("disabled"):
        return {"key": field["key"], "already_accepted": True}
    value = response.get("value", response.get("correct_value", ""))
    if field["type"] in ("radio", "select"):
        choice = pick_choice(field, response)
        if field["type"] == "radio":
            if choice.get("dom_id"):
                control = by_id(scope, choice["dom_id"])
            else:
                control = scope.locator(".questionWidget-choiceLetterCircle,.choiceLetterCircle").nth(field["choices"].index(choice))
            control.click()
            selected = control.evaluate("n => n.classList.contains('selectedChoice') || n.style.backgroundColor === 'rgb(64, 64, 64)' || n.getAttribute('aria-checked') === 'true'")
            if not selected:
                raise ValueError("Radio selection was not acknowledged")
        elif field.get("tag") == "select":
            control = by_id(scope, field["dom_id"])
            control.select_option(str(choice["option"]))
            if control.input_value() != str(choice["option"]):
                raise ValueError("Select readback differs from response")
        else:
            control = by_id(scope, field["dom_id"]) if field.get("dom_id") else scope.locator(".selectList").nth(field.get("dom_index", 0))
            frame = control.locator(".selectListFrame, .selectListFrameDisabled").first
            option = by_id(control, choice["dom_id"]) if choice.get("dom_id") else control.locator(".selectListOptions > .selectListOption").nth(field["choices"].index(choice))
            # MA reparents the menu to body as it opens; retain this exact source
            # option node before the field-scoped selector ceases to match it.
            handle = option.element_handle()
            if handle is None:
                raise ValueError("Captured dropdown option is not present")
            expected = choice_content(handle)
            # The window mousedown handler hides menus clicked through a
            # formula child; use the frame itself after bringing it on screen.
            click_dropdown(frame, direct=True)
            click_dropdown(handle)
            if control.locator(".selectListFrame .selectListSelectedText").count():
                raise ValueError("Custom select still shows an unselected placeholder")
            if choice_content(frame) != expected:
                raise ValueError("Custom select readback differs from selected source option")
        entered = {"key": field["key"], "option": choice["option"], "value": choice["value"], "value_type": choice["type"]}
        if field['type'] == 'select' and field.get('tag') != 'select':
            entered['choice_content'] = expected
        return entered
    if field.get("tag") == "mathquill":
        control = scope.locator(".matheditor-wrapper-answer").nth(field.get("dom_index", 0))
        # Use the editor's public write API so fractions, roots and matrices keep
        # their mathematical structure. It invokes MathQuill's normal edit event.
        write_math(control, value, response.get("keys", response.get("correct_keys", [])))
    else:
        control = by_id(scope, field["dom_id"]) if field.get("dom_id") else scope.locator("input:not([type='hidden']),textarea,[contenteditable='true']").nth(field.get("dom_index", 0))
        control.fill(str(value))
        observed = control.inner_text() if control.get_attribute("contenteditable") == "true" else control.input_value()
        if observed != str(value):
            raise ValueError("Answer field readback differs from response")
    return {"key": field["key"], "value": str(value), "value_type": response.get("value_type", "math" if field.get("tag") == "mathquill" else "text")}
