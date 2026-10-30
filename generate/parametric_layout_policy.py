"""Keep generated parametric tables and coordinate formulas visible."""
import re
TABLE_KP=17592186087717
TRIG_KP=17592186087736

def validate_delivery_batch(records,kp_id):
    if int(kp_id) not in (TABLE_KP,TRIG_KP):return
    for r in records:
        q=r['question']
        if int(kp_id)==TABLE_KP:
            for text in (q[':question/problem'],q[':question/worked-solution']):
                for line in text.splitlines():
                    if line.startswith('|') and len(line.strip().strip('|').split('|'))>4:
                        raise ValueError('Parametric value tables must use small panels with repeated headings')
        else:
            for block in re.findall(r'\$\$(.*?)\$\$',q[':question/problem'],re.S):
                if re.search(r'\bx\s*=',block) and re.search(r'\by\s*=',block):
                    raise ValueError('Trigonometric coordinate formulas must be independently visible')
