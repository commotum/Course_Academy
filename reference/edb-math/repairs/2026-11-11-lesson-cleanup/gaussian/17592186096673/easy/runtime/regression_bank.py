"""Retain the single-z bypass and test the current ordinary visible output."""
import sys
sys.dont_write_bytecode=True
import json
from pathlib import Path
from generator import sample
from math_checks import audit,check_bank

def run():
    checked=0
    for band in ('easy','moderate','hard'):
        for seed in (2991450669,17019):
            for record in sample(band,5,seed):
                audit(record);check_bank(record);checked+=1
    return checked
if __name__=='__main__':print('Passed visible bank and exact math checks for',run(),'current ordinary records')
