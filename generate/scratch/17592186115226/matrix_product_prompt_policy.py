"""Preserve independent row/column selection in ordinary matrix practice."""
import re

KP = 17592186059747
SUPPLIED_ENTRIES_KP = 17592186115226


def validate_delivery_batch(records, kp_id):
    if int(kp_id) == SUPPLIED_ENTRIES_KP:
        for record in records:
            prompt = record['question'][':question/problem']
            marker = r'<td>\s*\$?\s*(?:\\+ast\b|\\+star\b|\*)\s*\$?\s*</td>'
            if re.search(marker, prompt, re.I) or re.search(r'\basterisk\b', prompt, re.I):
                raise ValueError('Distributive-law partial matrices must supply the actual unrequested entries')
        return
    if int(kp_id) != KP:
        return
    for record in records:
        prompt = record['question'][':question/problem']
        # The partial matrix can supply unassessed entries. The learner must
        # still choose the row and column and form each requested dot product.
        process = r'\b(?:use|multiply|multiplying|match|matching)\b[^.!?]{0,120}\b(?:row|column)\b|\b(?:dot[ -]?product|pairwise|hint)\b'
        numeric_product = r'\d\s*' + re.escape(chr(92)) + r'+(?:cdot|times)'
        if re.search(process, prompt, re.I) or re.search(numeric_product, prompt):
            raise ValueError('Matrix practice prompt supplies the multiplication process or an entry calculation')
