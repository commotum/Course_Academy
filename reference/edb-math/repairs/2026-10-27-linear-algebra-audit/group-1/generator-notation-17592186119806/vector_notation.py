"""Source vector fonts at the TeX authoring boundary, before content identities."""
import re
from math_format import MATH

def _tex(value, names):
    protected=[]
    for command in re.finditer(r'\\(?:mathbf|mathbb|text|operatorname|mathrm)\s*\{',value):
        i=command.end();depth=1
        while depth and i<len(value):
            if value[i]=='\\' and i+1<len(value) and value[i+1] in '{}':i+=2;continue
            depth+=(value[i]=='{')-(value[i]=='}');i+=1
        if not depth:protected.append((command.start(),i))
    def replace(match):
        if match[0] not in names or any(a<=match.start()<b for a,b in protected):return match[0]
        # x_i denotes a scalar component/coefficient; x denotes the vector.
        if match[0]=='x' and re.match(r'\s*\}?\s*_',value[match.end():]):return match[0]
        return r'\mathbf{'+match[0]+'}'
    return re.sub(r'(?<![A-Za-z\\])([abx])(?![A-Za-z])',replace,value)

def vector_prose(value,names='ab'):
    return MATH.sub(lambda match:_tex(match[0],names),value)

def plain_vector_prose(value):
    # Parsing mathematical parameters must ignore authored font changes.
    return MATH.sub(lambda match:re.sub(r'\\mathbf\{([abx])\}',r'\1',match[0]),value)
