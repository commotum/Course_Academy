from pathlib import Path

def patch(p):
    s=p.read_text();s=s.replace("VERSION = '1.1.0'","VERSION = '1.1.1-source-notation'")
    s=s.replace("return r'b\\notin\\operatorname{Span}\\{' + ','.join('a_{'+str(i)+'}'", "return r'\\mathbf{b}\\notin\\operatorname{Span}\\{' + ','.join(r'\\mathbf{a}_{'+str(i)+'}'")
    s=s.replace("names = ','.join('a_{'+str(i)+'}'", "names = ','.join(r'\\mathbf{a}_{'+str(i)+'}'")
    s=s.replace("'x_{'+str(i)+'}a_{'+str(i)+'}'", "'x_{'+str(i)+r'}\\mathbf{a}_{'+str(i)+'}'")
    s=s.replace("displays = ['a_{'+str(j+1)+'}='", "displays = [r'\\mathbf{a}_{'+str(j+1)+'}='")
    s=s.replace("['b='+vector(b)]", "[r'\\mathbf{b}='+vector(b)]")
    s=s.replace('$b',r'$\\mathbf{{b}}').replace('{decomposition}=b.',r'{decomposition}=\\mathbf{{b}}.')
    assert s.count(r'\mathbf{a}')>=4
    p.write_text(s)

if __name__=='__main__':
    patch(Path(__file__).resolve().parent/'staged-generators/17592186119808/generator.py')
