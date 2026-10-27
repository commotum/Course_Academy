"""Preserve independent row/column selection in ordinary matrix practice."""
import re

KP = 17592186059747


def validate_delivery_batch(records, kp_id):
    if int(kp_id) != KP:
        return
    for record in records:
        prompt = record['question'][':question/problem']
        # The partial matrix can supply unassessed entries. The learner must
        # still choose the row and column and form each requested dot product.
        process = r'\b(?:use|multiply|multiplying|match|matching)\b[^.!?]{0,120}\b(?:row|column)\b|\b(?:dot[ -]?product|pairwise|hint)\b'
        if re.search(process, prompt, re.I) or re.search(r'\d\s*\+(?:cdot|times)', prompt):
            raise ValueError('Matrix practice prompt supplies the multiplication process or an entry calculation')
