"""Strict valid-input acceptance witness. Fails archived version 2.0.0 and passes current version 2.0.1.
Run with context Python -B boundary_regression.py. Do not weaken to accept ValueError.
"""
import sys
sys.dont_write_bytecode=True
import review as a
params={'2':1,'3':4}
r=a.g.generate('easy',941713401,profile='q-71722',parameters=params)
a.check_math(r)
assert a.correct_matrix(r)==[[1,-1,4],[1,1,-1]]
assert len(a.bank(r))==5
print('Valid unit-coefficient case returned a correct complete five-choice record.')
