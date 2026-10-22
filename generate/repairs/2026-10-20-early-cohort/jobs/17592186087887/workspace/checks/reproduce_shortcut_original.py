#!/usr/bin/env python3
"""Retained independent review predictor; live regression fails on the legacy package.
Run: python checks/reproduce_shortcut_original.py
The predictor receives only candidate strings/UUIDs, never the ODE or key.
"""
import sys,pathlib,json,argparse,importlib.util,re,collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent

def predict(field):
 bank=field[':answer-field/choices']
 root=[z for z in bank if '\\sqrt[3]' in z[':answer/value']]
 if len(root)==1:return 'unique cube root',root[0][':answer/id']
 log=[z for z in bank if 'x\\ln|x|' in z[':answer/value'] and z[':answer/value'].endswith('+Cx')]
 if len(log)==1:return 'x log and Cx',log[0][':answer/id']
 affine=[]
 for z in bank:
  m=re.fullmatch(r'y=Cx\^2[+-](\d*)x',z[':answer/value'])
  if m:affine.append((int(m.group(1) or 1),z))
 if len(affine)==2 and affine[0][0]!=affine[1][0]:return 'smaller affine coefficient',min(affine,key=lambda z:z[0])[1][':answer/id']
 return 'no recognized cue',None

def main():
 # Keep the review's prompt-blind predictor intact; run current live acceptance checks.
 from check_shortcuts import main as check_current
 check_current()
 return 0
if __name__=='__main__':sys.exit(main())
