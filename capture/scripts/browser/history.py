"""Recover MC choices omitted by the completed-task history renderer.

Only the owned task's answers endpoint is used. Render in a separate offline
page, bind by both source ID and prompt, and never synthesize learner attempts.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from ..storage import atomic_text


class HistoryChoices:
    def __init__(self, context, repo_root):
        self.page = context.new_page()
        vendor = Path(repo_root)/'ui/vendor/mathjax'
        local = {f'https://capture.invalid/mathjax/input/tex/extensions/{name}.js':
                 vendor/f'input/tex/extensions/{name}.js' for name in ('bbox','cancel','color','enclose')}
        self.page.route('**/*', lambda route: route.fulfill(path=str(local[route.request.url]),
            content_type='application/javascript') if route.request.url in local else route.abort())
        self.page.set_content('<body></body>')
        self.page.evaluate("window.MathJax={loader:{paths:{mathjax:'https://capture.invalid/mathjax'}},startup:{typeset:false}}")
        self.page.add_script_tag(path=str(vendor/'tex-svg.js'))
        self.page.evaluate('MathJax.startup.promise')

    def close(self):
        self.page.close()

    def recover(self, record, answer, source_file, directory):
        from ..activity.capture import ActivityCapture
        question = answer.get('question', {})
        identity = 'q-' + str(question.get('id'))
        if record.get('math_academy_id') != identity:
            raise ValueError('Task answer question ID does not match history')
        if record.get('fields') or record.get('answer_fields'):
            return deepcopy(record)
        if question.get('format') != 'MC':
            return deepcopy(record)  # Other formats require their own source renderer.
        choices = [question.get('choice'+str(i)) for i in range(1,6)]
        if not question.get('text') or not all(isinstance(c,str) and c.strip() for c in choices):
            raise ValueError('Task answer has incomplete MC source')
        # Build inert DOM from the original HTML, retaining the separate raw JSON.
        # MathJax only converts TeX to MathML; no website state is executed.
        self.page.evaluate(r'''async q => {
          document.body.replaceChildren();
          const root=document.createElement('div');root.id='source-question';
          const prompt=document.createElement('div');prompt.className='questionText';prompt.innerHTML=q.text;root.append(prompt);
          const table=document.createElement('table');table.className='questionWidget-choicesTable';root.append(table);
          for(let i=1;i<=5;i++) {
            const row=table.insertRow(),letter=row.insertCell(),content=row.insertCell();
            const circle=document.createElement('span');circle.className='choiceLetterCircle';circle.id='source-choice-'+i;
            circle.textContent=String.fromCharCode(96+i);letter.append(circle);content.className='choiceText';content.innerHTML=q['choice'+i];
          }
          root.querySelectorAll('script,iframe,object,embed').forEach(n=>n.remove());
          const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),nodes=[];while(walker.nextNode()) nodes.push(walker.currentNode);
          const pattern=/(?<!\\)\$\$([\s\S]*?)(?<!\\)\$\$|\\\[([\s\S]*?)\\\]|(?<!\\)\$([^$]*?)(?<!\\)\$|\\\(([\s\S]*?)\\\)/g;
          for(const node of nodes) {
            const fragment=document.createDocumentFragment();let start=0,found=false;
            for(const match of node.textContent.matchAll(pattern)) {
              found=true;fragment.append(node.textContent.slice(start,match.index));
              const display=match[1]!==undefined || match[2]!==undefined;
              const math=new DOMParser().parseFromString(await MathJax.tex2mmlPromise(match[1]??match[2]??match[3]??match[4]),'text/xml').documentElement;
              // tex2mml pretty prints container indentation. It is not authored
              // spacing inside a token such as mtext.
              const spaces=document.createTreeWalker(math,NodeFilter.SHOW_TEXT),empty=[];
              while(spaces.nextNode()) if(!spaces.currentNode.textContent.trim() &&
                !['mi','mo','mn','mtext','ms'].includes(spaces.currentNode.parentNode.localName)) empty.push(spaces.currentNode);
              empty.forEach(n=>n.remove());
              math.setAttribute('display',String(display));fragment.append(document.importNode(math,true));start=match.index+match[0].length;
            }
            if(found) {fragment.append(node.textContent.slice(start));node.replaceWith(fragment);}
          }
          document.body.append(root);
        }''', question)
        from .adapter import EXTRACT
        parsed = self.page.locator('#source-question').evaluate(EXTRACT)
        if parsed.get('errors') or parsed.get('assets'):
            raise ValueError('Task answer MC rendering requires unsupported math or assets')
        # Compare the actual history prompt without its separately captured graphic.
        self.page.evaluate("html=>{document.body.innerHTML=html}", record.get('html', ''))
        from .entry import by_id
        root = by_id(self.page,'question-'+str(question['id']))
        if root.count() != 1:
            raise ValueError('History DOM question identity differs from task answer')
        prompt = root.locator('.questionText,.questionWidget-text')
        if prompt.count() != 1:
            raise ValueError('History has no unique source prompt')
        observed = prompt.evaluate('(node,extract)=>{const root=document.createElement("div");root.append(node.cloneNode(true));document.body.append(root);try{return eval("("+extract+")")(root).problem}finally{root.remove()}}', EXTRACT)
        if not ActivityCapture._source_binding_matches({'problem':observed}, {'problem':parsed['problem']}):
            raise ValueError('Task answer prompt differs from completed history')
        digest = hashlib.sha256(json.dumps(question,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        rendered = Path(directory)/'source'/('task-answer-'+identity+'-'+digest[:16]+'.html')
        atomic_text(rendered,parsed['html'])
        result = deepcopy(record)
        result['fields'] = parsed['fields']
        result['answer_fields_complete'] = True
        result['extraction_parts'] = list(dict.fromkeys(record.get('extraction_parts',[]) + ['fields']))
        result['field_recovery'] = {'kind':'owned_task_answers','source_file':str(Path(source_file).resolve()),
            'question_id':identity,'question_sha256':digest,'rendered_file':str(rendered.resolve()),
            'order':'canonical source order; not the live shuffled order',
            'learner_answer':deepcopy({k:v for k,v in answer.items() if k!='question'})}
        return result


def task_answers(payload, task_id):
    task = payload.get('task', {})
    if payload.get('error') or str(task.get('id')) != str(task_id):
        raise ValueError('Task answers response does not identify the owned completed task')
    answers = task.get('answers')
    if not isinstance(answers,list):
        raise ValueError('Task answers response has no answers list')
    by_id = {}
    for answer in answers:
        identity = 'q-' + str(answer.get('question',{}).get('id'))
        if identity in by_id:
            raise ValueError('Ambiguous repeated question in task answers')
        by_id[identity] = answer
    return by_id
