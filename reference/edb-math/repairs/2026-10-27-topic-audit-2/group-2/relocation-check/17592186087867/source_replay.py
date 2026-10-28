#!/usr/bin/env python3
"""Parameterized five-option identification of first-order linear ODEs.

Exact source banks at a=1,h=0; default affine-function variants replace only
independent-variable functions by u=a*x+h, preserving derivative notation.
These categorical objects encode explicit operations (higher derivative,
derivative square, nonlinear y function, y-dependent factor and cancellation),
not numerical distractor fits. All 12 observed profiles are default eligible.
Complete profile chosen first; invalid whole banks rejected. Every solution
uses the observed fixed sentence and stage template. No EDB calls or plots.
Evidence, source provenance, review, and native checks: sibling directory.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
import sympy as sp
KP_ID=17592186087867
KP_UUID="bc50a680-dbf8-5d45-a8c3-72c3c15243f6"
TITLE="Identifying First-Order Linear ODEs"
VERSION="linear-ode-identification-1"
X,Y,D,D2=sp.symbols("x y D D2", real=True)
SOURCE={"database":"math","basis_t":1356,"lineage":"01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}

TEMPLATES = {'q_103560': {'level': 'moderate',
              'source': 'q-103560',
              'problem': 'Which of the following is **NOT** a first order linear ordinary differential '
                         'equation?',
              'solution': 'To determine which of the following differential equations is a first-order '
                          'linear ordinary differential equation, we attempt to write each option in '
                          'the standard form.\n'
                          '\n'
                          'A first-order linear ODE is in standard form if it is written as\n'
                          '\n'
                          '$$\n'
                          '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                          '$$\n'
                          '\n'
                          "Let's attempt to write "
                          '$\\frac{\\text{d}y}{\\text{d}x}-{@@X@@}^{2}=\\frac{1}{1-y}$ in the standard '
                          'form:\n'
                          '\n'
                          '$$\n'
                          '\\begin{aligned}\\frac{\\text{d}y}{\\text{d}x}-{@@X@@}^{2}=\\frac{1}{1-y} '
                          '\\\\ '
                          '\\frac{\\text{d}y}{\\text{d}x}+\\frac{1}{y-1}={@@X@@}^{2}\\end{aligned}\n'
                          '$$\n'
                          '\n'
                          'This differential equation cannot be written in standard form since the '
                          'power of $y$ in the term $\\frac{1}{y-1}$ is not $1.$ Since the equation '
                          'cannot be written in standard form, we conclude that it is not a first-order '
                          'linear ODE.\n'
                          '\n'
                          'All of the other equations can be written in the standard form, and '
                          'therefore they are first-order linear ODEs.',
              'choices': ['\\frac{\\text{d}y}{\\text{d}x}-(\\operatorname{tan}\u2061@@X@@)y=\\operatorname{sec}\u2061@@X@@',
                          '@@X@@\\frac{\\text{d}y}{\\text{d}x}-{@@X@@}^{2}y=@@X@@\\operatorname{sin}\u2061@@X@@',
                          '2\\frac{\\text{d}y}{\\text{d}x}-4@@X@@y=\\sqrt{@@X@@}',
                          '\\frac{\\text{d}y}{\\text{d}x}-{@@X@@}^{2}=\\frac{1}{1-y}',
                          '\\frac{\\text{d}y}{\\text{d}x}-\\frac{{e}^{@@X@@}}{@@X@@}y={@@X@@}^{3}']},
 'q_8349': {'level': 'easy',
            'source': 'q-8349',
            'problem': 'Which of the following is a first-order linear ordinary differential equation?',
            'solution': 'To determine which of the following differential equations is a first-order '
                        'linear ordinary differential equation, we attempt to write each option in the '
                        'standard form.\n'
                        '\n'
                        'A first-order linear ODE is in standard form if it is written as\n'
                        '\n'
                        '$$\n'
                        '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                        '$$\n'
                        '\n'
                        'Note that the option\n'
                        '\n'
                        '$$\n'
                        '\\frac{\\text{d}y}{\\text{d}x}+2@@X@@y=6{@@X@@}^{2}\n'
                        '$$\n'
                        '\n'
                        'is already is written in standard form with  $P(x)=2@@X@@$ and '
                        '$Q(x)=6{@@X@@}^{2}.$ Since the equation is written in standard form, we '
                        'conclude that it is a first-order linear ODE.\n'
                        '\n'
                        'All of the other equations cannot be written in the standard form, and '
                        'therefore they are not first-order linear ODEs.',
            'choices': ['\\frac{{\\text{d}}^{2}y}{\\text{d}{x}^{2}}+2@@X@@y=6@@X@@',
                        'y\\frac{\\text{d}y}{\\text{d}x}+2@@X@@=6@@X@@',
                        '\\frac{\\text{d}y}{\\text{d}x}+2@@X@@y=6{@@X@@}^{2}',
                        '\\frac{\\text{d}y}{\\text{d}x}+2@@X@@{y}^{2}=6@@X@@',
                        '{(\\frac{\\text{d}y}{\\text{d}x})}^{2}+2@@X@@y=6@@X@@']},
 'q_8352': {'level': 'hard',
            'source': 'q-8352',
            'problem': 'Which of the following is **NOT** a first-order linear ordinary differential '
                       'equation?',
            'solution': 'To determine which of the following differential equations is a first-order '
                        'linear ordinary differential equation, we attempt to write each option in the '
                        'standard form.\n'
                        '\n'
                        'A first-order linear ODE is in standard form if it is written as\n'
                        '\n'
                        '$$\n'
                        '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                        '$$\n'
                        '\n'
                        "Let's attempt to write $y\\frac{\\text{d}y}{\\text{d}x}+@@X@@=y$ in the "
                        'standard form:\n'
                        '\n'
                        '$$\n'
                        '\\begin{aligned}y\\frac{\\text{d}y}{\\text{d}x}+@@X@@=y \\\\ '
                        '\\frac{\\text{d}y}{\\text{d}x}+@@X@@{y}^{-1}=1\\end{aligned}\n'
                        '$$\n'
                        '\n'
                        'This differential equation cannot be written in standard form since the power '
                        'of $y$ in the term $@@X@@{y}^{-1}$ is not $1.$ Since the equation cannot be '
                        'written in standard form, we conclude that it is not a first-order linear '
                        'ODE.\n'
                        '\n'
                        'All of the other equations can be written in the standard form, and therefore '
                        'they are first-order linear ODEs.',
            'choices': ['\\frac{\\text{d}y}{\\text{d}x}+y=@@X@@',
                        'y\\frac{\\text{d}y}{\\text{d}x}+@@X@@=y',
                        '\\frac{\\text{d}y}{\\text{d}x}+@@X@@=y',
                        '\\frac{\\text{d}y}{\\text{d}x}+y=@@X@@y',
                        '\\frac{\\text{d}y}{\\text{d}x}+y=\\operatorname{cos}\u2061{e}^{\\operatorname{arctan}\u2061({@@X@@}^{2}+\\operatorname{ln}\u2061@@X@@)}']},
 'q_103551': {'level': 'easy',
              'source': 'q-103551',
              'problem': 'Which of the following is a first-order linear ordinary differential '
                         'equation?',
              'solution': 'To determine which of the following differential equations is a first-order '
                          'linear ordinary differential equation, we attempt to write each option in '
                          'the standard form.\n'
                          '\n'
                          'A first-order linear ODE is in standard form if it is written as\n'
                          '\n'
                          '$$\n'
                          '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                          '$$\n'
                          '\n'
                          'Note that the option\n'
                          '\n'
                          '$$\n'
                          '\\frac{\\text{d}y}{\\text{d}x}-3(\\operatorname{ln}\u2061@@X@@)y=\\frac{1}{@@X@@}\n'
                          '$$\n'
                          '\n'
                          'is already is written in standard form with  '
                          '$P(x)=-3\\operatorname{ln}\u2061@@X@@$ and $Q(x)=\\frac{1}{@@X@@}.$ Since '
                          'the equation is written in standard form, we conclude that it is a '
                          'first-order linear ODE.\n'
                          '\n'
                          'All of the other equations cannot be written in the standard form, and '
                          'therefore they are not first-order linear ODEs.',
              'choices': ['\\frac{\\text{d}y}{\\text{d}x}-3(\\operatorname{ln}\u2061@@X@@)y=\\frac{1}{@@X@@}',
                          '\\frac{1}{y}\\frac{\\text{d}y}{\\text{d}x}-@@X@@y={@@X@@}^{3}',
                          '{(\\frac{\\text{d}y}{\\text{d}x})}^{2}+{@@X@@}^{2}y=\\operatorname{sin}\u2061@@X@@',
                          '\\frac{\\text{d}y}{\\text{d}x}+\\operatorname{sin}\u2061(@@X@@y)=@@X@@-1',
                          '\\frac{\\text{d}y}{\\text{d}x}-{@@X@@}^{3}y=\\frac{@@X@@}{1+y}']},
 'q_103554': {'level': 'easy',
              'source': 'q-103554',
              'problem': 'Which of the following is a first-order linear ordinary differential '
                         'equation?',
              'solution': 'To determine which of the following differential equations is a first-order '
                          'linear ordinary differential equation, we attempt to write each option in '
                          'the standard form.\n'
                          '\n'
                          'A first-order linear ODE is in standard form if it is written as\n'
                          '\n'
                          '$$\n'
                          '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                          '$$\n'
                          '\n'
                          'Note that the option\n'
                          '\n'
                          '$$\n'
                          '\\frac{\\text{d}y}{\\text{d}x}-\\frac{{e}^{@@X@@}}{@@X@@}y={@@X@@}^{2}\\operatorname{sin}\u2061@@X@@\n'
                          '$$\n'
                          '\n'
                          'is already is written in standard form with  '
                          '$P(x)=-\\frac{{e}^{@@X@@}}{@@X@@}$ and '
                          '$Q(x)={@@X@@}^{2}\\operatorname{sin}\u2061@@X@@.$ Since the equation is '
                          'written in standard form, we conclude that it is a first-order linear ODE.\n'
                          '\n'
                          'All of the other equations cannot be written in the standard form, and '
                          'therefore they are not first-order linear ODEs.',
              'choices': ['{(\\frac{\\text{d}y}{\\text{d}x})}^{2}-{@@X@@}^{3}=\\sqrt{1+y}',
                          '\\frac{\\text{d}y}{\\text{d}x}-{e}^{@@X@@y}=@@X@@',
                          '\\frac{\\text{d}y}{\\text{d}x}-\\frac{{e}^{@@X@@}}{@@X@@}y={@@X@@}^{2}\\operatorname{sin}\u2061@@X@@',
                          '\\frac{1}{{y}^{2}}\\frac{\\text{d}y}{\\text{d}x}-{@@X@@}^{2}=\\operatorname{sin}\u2061@@X@@',
                          '\\frac{\\text{d}y}{\\text{d}x}+@@X@@\\operatorname{ln}\u2061(@@X@@y)={@@X@@}^{2}']},
 'q_103557': {'level': 'moderate',
              'source': 'q-103557',
              'problem': 'Which of the following is **NOT** a first-order linear ordinary differential '
                         'equation?',
              'solution': 'To determine which of the following differential equations is a first-order '
                          'linear ordinary differential equation, we attempt to write each option in '
                          'the standard form.\n'
                          '\n'
                          'A first-order linear ODE is in standard form if it is written as\n'
                          '\n'
                          '$$\n'
                          '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                          '$$\n'
                          '\n'
                          'Note that the option\n'
                          '\n'
                          '$$\n'
                          '\\frac{\\text{d}y}{\\text{d}x}-\\sqrt{@@X@@y}={@@X@@}^{2}\n'
                          '$$\n'
                          '\n'
                          'cannot be written in standard form since the power of $y$ in the term '
                          '$\\sqrt{@@X@@y}$ is not $1.$ Since the equation cannot be written in '
                          'standard form, we conclude that it is not a first-order linear ODE.\n'
                          '\n'
                          'All of the other equations can be written in the standard form, and '
                          'therefore they are first-order linear ODEs.',
              'choices': ['\\frac{\\text{d}y}{\\text{d}x}-4y=@@X@@',
                          '\\frac{\\text{d}y}{\\text{d}x}-\\sqrt{@@X@@y}={@@X@@}^{2}',
                          '@@X@@\\frac{\\text{d}y}{\\text{d}x}-({@@X@@}^{3}\\operatorname{cos}\u2061@@X@@)y=\\operatorname{sin}\u2061@@X@@',
                          '{@@X@@}^{2}\\frac{\\text{d}y}{\\text{d}x}-(1+@@X@@)y=1',
                          '\\frac{\\text{d}y}{\\text{d}x}-\\frac{1}{{@@X@@}^{2}}y={e}^{-@@X@@}']},
 'q_103559': {'level': 'moderate',
              'source': 'q-103559',
              'problem': 'Which of the following is **NOT** a first-order linear ordinary differential '
                         'equation?',
              'solution': 'To determine which of the following differential equations is a first-order '
                          'linear ordinary differential equation, we attempt to write each option in '
                          'the standard form.\n'
                          '\n'
                          'A first-order linear ODE is in standard form if it is written as\n'
                          '\n'
                          '$$\n'
                          '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                          '$$\n'
                          '\n'
                          'Note that the option\n'
                          '\n'
                          '$$\n'
                          '\\frac{\\text{d}y}{\\text{d}x}+\\operatorname{ln}\u2061(@@X@@y)={@@X@@}^{2}\n'
                          '$$\n'
                          '\n'
                          'cannot be written in standard form since the power of $y$ in the term '
                          '$\\operatorname{ln}\u2061(@@X@@y)$ is not $1.$ Since the equation cannot be '
                          'written in standard form, we conclude that it is not a first-order linear '
                          'ODE.\n'
                          '\n'
                          'All of the other equations can be written in the standard form, and '
                          'therefore they are first-order linear ODEs.',
              'choices': ['\\frac{1}{@@X@@}\\frac{\\text{d}y}{\\text{d}x}-{@@X@@}^{2}y=\\operatorname{sin}\u2061@@X@@',
                          '\\frac{\\text{d}y}{\\text{d}x}+4y={e}^{@@X@@}',
                          '\\frac{\\text{d}y}{\\text{d}x}-@@X@@y=\\operatorname{sin}\u2061@@X@@',
                          '\\frac{\\text{d}y}{\\text{d}x}+(\\operatorname{ln}\u2061@@X@@)y={@@X@@}^{2}',
                          '\\frac{\\text{d}y}{\\text{d}x}+\\operatorname{ln}\u2061(@@X@@y)={@@X@@}^{2}']},
 'q_79750': {'level': 'moderate',
             'source': 'q-79750',
             'problem': 'Which of the following is **NOT** a first-order linear ordinary differential '
                        'equation?',
             'solution': 'To determine which of the following differential equations is a first-order '
                         'linear ordinary differential equation, we attempt to write each option in the '
                         'standard form.\n'
                         '\n'
                         'A first-order linear ODE is in standard form if it is written as\n'
                         '\n'
                         '$$\n'
                         '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                         '$$\n'
                         '\n'
                         'Note that the option\n'
                         '\n'
                         '$$\n'
                         '\\frac{\\text{d}y}{\\text{d}x}+@@X@@y={y}^{2}\n'
                         '$$\n'
                         '\n'
                         'cannot be written in standard form since the right-hand side depends on $y$ through the nonlinear term $y^2.$ '
                         'Since the equation cannot be written in standard form, we conclude that it is '
                         'not a first-order linear ODE.\n'
                         '\n'
                         'All of the other equations can be written in the standard form, and therefore '
                         'they are first-order linear ODEs.',
             'choices': ['y\\frac{\\text{d}y}{\\text{d}x}+@@X@@{y}^{2}=2y',
                         '\\frac{\\text{d}y}{\\text{d}x}+\\frac{y}{2}=@@X@@',
                         '\\frac{\\text{d}y}{\\text{d}x}+y=1+\\operatorname{sin}\u2061@@X@@',
                         '\\frac{\\text{d}y}{\\text{d}x}+@@X@@y={y}^{2}',
                         '\\frac{\\text{d}y}{\\text{d}x}+{@@X@@}^{2}y=\\operatorname{sec}\u2061@@X@@']},
 'q_79752': {'level': 'moderate',
             'source': 'q-79752',
             'problem': 'Which of the following is **NOT** a first-order linear ordinary differential '
                        'equation?',
             'solution': 'To determine which of the following differential equations is a first-order '
                         'linear ordinary differential equation, we attempt to write each option in the '
                         'standard form.\n'
                         '\n'
                         'A first-order linear ODE is in standard form if it is written as\n'
                         '\n'
                         '$$\n'
                         '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                         '$$\n'
                         '\n'
                         'Note that the option\n'
                         '\n'
                         '$$\n'
                         '\\frac{\\text{d}y}{\\text{d}x}+\\sqrt{y}=@@X@@\\operatorname{cos}\u2061@@X@@\n'
                         '$$\n'
                         '\n'
                         'cannot be written in standard form since the power of $y$ in the term '
                         '$\\sqrt{y}$ is not $1.$ Since the equation cannot be written in standard '
                         'form, we conclude that it is not a first-order linear ODE.\n'
                         '\n'
                         'All of the other equations can be written in the standard form, and therefore '
                         'they are first-order linear ODEs.',
             'choices': ['\\frac{\\text{d}y}{\\text{d}x}+y=0',
                         '\\frac{\\text{d}y}{\\text{d}x}+\\frac{y}{{@@X@@}^{2}}={e}^{2@@X@@}',
                         '\\frac{\\text{d}y}{\\text{d}x}+\\frac{y}{\\sqrt{{@@X@@}^{2}+1}}=0',
                         '\\frac{\\text{d}y}{\\text{d}x}+\\sqrt{y}=@@X@@\\operatorname{cos}\u2061@@X@@',
                         '\\frac{\\text{d}y}{\\text{d}x}+\\frac{y}{\\operatorname{arctan}\u2061@@X@@}=\\frac{1}{{@@X@@}^{2}}']},
 'q_79753': {'level': 'easy',
             'source': 'q-79753',
             'problem': 'Which of the following is a first-order linear ordinary differential equation?',
             'solution': 'To determine which of the following differential equations is a first-order '
                         'linear ordinary differential equation, we attempt to write each option in the '
                         'standard form.\n'
                         '\n'
                         'A first-order linear ODE is in standard form if it is written as\n'
                         '\n'
                         '$$\n'
                         '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                         '$$\n'
                         '\n'
                         'Note that the option\n'
                         '\n'
                         '$$\n'
                         '\\frac{\\text{d}y}{\\text{d}x}+(\\sqrt{@@X@@})y=@@X@@\\operatorname{tan}\u2061@@X@@\n'
                         '$$\n'
                         '\n'
                         'is already is written in standard form with  $P(x)=\\sqrt{@@X@@}$ and '
                         '$Q(x)=@@X@@\\operatorname{tan}\u2061@@X@@.$ Since the equation is written in '
                         'standard form, we conclude that it is a first-order linear ODE.\n'
                         '\n'
                         'All of the other equations cannot be written in the standard form, and '
                         'therefore they are not first-order linear ODEs.',
             'choices': ['\\frac{\\text{d}y}{\\text{d}x}+y=\\operatorname{sin}\u2061y',
                         '\\frac{\\text{d}y}{\\text{d}x}+(\\sqrt{@@X@@})y=@@X@@\\operatorname{tan}\u2061@@X@@',
                         '\\frac{\\text{d}y}{\\text{d}x}-@@X@@y=\\frac{1}{y-1}',
                         '\\frac{\\text{d}y}{\\text{d}x}-y={y}^{2}\\operatorname{cos}\u2061@@X@@',
                         '\\frac{\\text{d}y}{\\text{d}x}+\\sqrt{(@@X@@y)}=@@X@@+1']},
 'q_79754': {'level': 'hard',
             'source': 'q-79754',
             'problem': 'Which of the following is a first-order linear ordinary differential equation?',
             'solution': 'To determine which of the following differential equations is a first-order '
                         'linear ordinary differential equation, we attempt to write each option in the '
                         'standard form.\n'
                         '\n'
                         'A first-order linear ODE is in standard form if it is written as\n'
                         '\n'
                         '$$\n'
                         '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                         '$$\n'
                         '\n'
                         "Let's attempt to write "
                         '$(\\frac{1}{y})\\frac{\\text{d}y}{\\text{d}x}=\\frac{2y+{@@X@@}^{2}}{y}$ in '
                         'the standard form:\n'
                         '\n'
                         '$$\n'
                         '\\begin{aligned}(\\frac{1}{y})\\frac{\\text{d}y}{\\text{d}x} & '
                         '=\\frac{2y+{@@X@@}^{2}}{y} \\\\ \\frac{\\text{d}y}{\\text{d}x} & '
                         '=y(\\frac{2y+{@@X@@}^{2}}{y}) \\\\ \\frac{\\text{d}y}{\\text{d}x} & '
                         '=2y+{@@X@@}^{2} \\\\ \\frac{\\text{d}y}{\\text{d}x}-2y & '
                         '={@@X@@}^{2}.\\end{aligned}\n'
                         '$$\n'
                         '\n'
                         'This differential equation is in standard form with  $P(x)=-2$ and '
                         '$Q(x)={@@X@@}^{2}.$ Since the equation is written in standard form, we '
                         'conclude that it is a first-order linear ODE.\n'
                         '\n'
                         'All of the other equations cannot be written in the standard form, and '
                         'therefore they are not first-order linear ODEs.',
             'choices': ['(\\frac{1}{y})\\frac{\\text{d}y}{\\text{d}x}=\\frac{2y+{@@X@@}^{2}}{y}',
                         '(\\frac{1}{y})\\frac{\\text{d}y}{\\text{d}x}=\\frac{1}{y\\operatorname{cos}\u2061@@X@@}-y',
                         '\\frac{\\text{d}y}{\\text{d}x}=\\frac{{y}^{2}+3@@X@@}{y}',
                         'y\\frac{\\text{d}y}{\\text{d}x}={y}^{2}-2@@X@@',
                         '(\\frac{1}{y})\\frac{\\text{d}y}{\\text{d}x}=\\frac{y-@@X@@}{{y}^{2}}']},
 'q_103567': {'level': 'hard',
              'source': 'q-103567',
              'problem': 'Which of the following is a first-order linear ordinary differential '
                         'equation?',
              'solution': 'To determine which of the following differential equations is a first-order '
                          'linear ordinary differential equation, we attempt to write each option in '
                          'the standard form.\n'
                          '\n'
                          'A first-order linear ODE is in standard form if it is written as\n'
                          '\n'
                          '$$\n'
                          '\\frac{\\text{d}y}{\\text{d}x}+P(x)y=Q(x).\n'
                          '$$\n'
                          '\n'
                          "Let's attempt to write "
                          '$\\frac{1}{y}\\frac{\\text{d}y}{\\text{d}x}-@@X@@{e}^{2@@X@@}=\\frac{\\operatorname{cos}\u2061@@X@@}{y}$ '
                          'in the standard form:\n'
                          '\n'
                          '$$\n'
                          '\\begin{aligned}\\frac{1}{y}\\frac{\\text{d}y}{\\text{d}x}-@@X@@{e}^{2@@X@@} '
                          '& =\\frac{\\operatorname{cos}\u2061@@X@@}{y} \\\\ '
                          '\\frac{\\text{d}y}{\\text{d}x}-@@X@@{e}^{2@@X@@}y & =y\\cdot '
                          '\\frac{\\operatorname{cos}\u2061@@X@@}{y} \\\\ '
                          '\\frac{\\text{d}y}{\\text{d}x}-@@X@@{e}^{2@@X@@}y & '
                          '=\\operatorname{cos}\u2061@@X@@.\\end{aligned}\n'
                          '$$\n'
                          '\n'
                          'This differential equation is in standard form with  '
                          '$P(x)=-@@X@@{e}^{2@@X@@}$ and $Q(x)=\\operatorname{cos}\u2061@@X@@.$ Since '
                          'the equation is written in standard form, we conclude that it is a '
                          'first-order linear ODE.\n'
                          '\n'
                          'All of the other equations cannot be written in the standard form, and '
                          'therefore they are not first-order linear ODEs.',
              'choices': ['\\frac{1}{y}\\frac{\\text{d}y}{\\text{d}x}-@@X@@{e}^{2@@X@@}=\\frac{\\operatorname{cos}\u2061@@X@@}{y}',
                          '\\frac{1}{y}\\frac{\\text{d}y}{\\text{d}x}+@@X@@{e}^{2@@X@@}y=\\frac{\\operatorname{cos}\u2061@@X@@}{y}',
                          '\\frac{\\text{d}y}{\\text{d}x}-@@X@@{e}^{y}={@@X@@}^{3}',
                          'y\\frac{\\text{d}y}{\\text{d}x}-@@X@@{e}^{@@X@@}=\\frac{\\operatorname{sin}\u2061@@X@@}{y}',
                          '\\frac{\\text{d}y}{\\text{d}x}-y{e}^{2@@X@@}=\\frac{\\operatorname{cos}\u2061@@X@@}{y}']}}

class LatexReader:
    """Small exact parser for the observed equation grammar, not a CAS grader.

Reads complete displayed relations, including nested fractions/functions,
implicit products, roots and derivatives. Unsupported tokens fail closed.
"""
    def __init__(self,text):
        text=text.replace(r'\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}','Dtwo')
        text=text.replace(r'\frac{\text{d}y}{\text{d}x}','Done')
        text=re.sub(r'\\operatorname\{(\w+)\}',r'\\\1 ',text)
        text=text.replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace('−','-')
        text=text.replace('.','').strip()
        self.tokens=re.findall(r'Dtwo|Done|\\[A-Za-z]+|\d+|[^\s]',text);self.i=0
    def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else None
    def pop(self):
        t=self.peek()
        if t is None:raise ValueError('Unexpected end of LaTeX')
        self.i+=1;return t
    def expr(self):
        out=self.product()
        while self.peek() in ('+','-'):
            op=self.pop();v=self.product();out=out+v if op=='+' else out-v
        return out
    def product(self):
        out=self.power()
        while self.peek() is not None and self.peek() not in ('+','-',')','}','=',r'\\','&'):
            if self.peek()=='*':self.pop()
            out*=self.power()
        return out
    def power(self):
        # Unary minus binds below exponentiation: -x^2 means -(x^2).
        if self.peek() in ('+','-'):
            sign=self.pop()
            return self.power() * (1 if sign=='+' else -1)
        out=self.atom()
        if self.peek()=='^':self.pop();out=out**self.atom()
        return out
    def atom(self):
        t=self.pop()
        if t in ('+','-'):return self.atom()*(1 if t=='+' else -1)
        if t in ('{','('):
            out=self.expr();end='}' if t=='{' else ')'
            if self.pop()!=end:raise ValueError('Unbalanced math group')
            return out
        if t==r'\frac':return self.atom()/self.atom()
        if t==r'\sqrt':return sp.sqrt(self.atom())
        if t in (r'\sin',r'\cos',r'\tan',r'\sec',r'\ln',r'\arctan'):
            f={r'\sin':sp.sin,r'\cos':sp.cos,r'\tan':sp.tan,r'\sec':sp.sec,r'\ln':sp.log,r'\arctan':sp.atan}[t]
            return f(self.power(), evaluate=False)
        if t=='Done':return D
        if t=='Dtwo':return D2
        if t=='x':return X
        if t=='y':return Y
        if t=='e':return sp.E
        if t.isdigit():return sp.Integer(t)
        raise ValueError('Unsupported displayed token '+repr(t))
    def equation(self):
        lhs=self.expr()
        if self.pop()!='=':raise ValueError('Equation required')
        rhs=self.expr()
        if self.peek() is not None:raise ValueError('Trailing tokens '+repr(self.tokens[self.i:]))
        return lhs-rhs


def read_equation(value):return LatexReader(value).equation()


def linear_flow(residual):
    """Normalize the coefficient of y' on the source's local nonzero domains."""
    if residual.has(D2):return None
    coefficient=sp.diff(residual,D)
    if coefficient==0 or coefficient.has(D):return None
    flow=sp.cancel(-(residual-coefficient*D)/coefficient)
    if flow.has(D) or sp.simplify(sp.diff(flow,Y,2))!=0:return None
    return flow


def affine_tex(p):
    a,h=p['a'],p['h']
    if (a,h)==(1,0):return 'x'
    core=('x' if a==1 else '-x' if a==-1 else str(a)+'x')
    if h:core+=('+' if h>0 else '')+str(h)
    return '('+core+')'


def render(t,p):return t.replace('@@X@@',affine_tex(p))


def parameter_check(p):
    if set(p)!={'a','h'} or any(type(v) is not int for v in p.values()):raise ValueError('Parameters must be integers a,h')
    if p['a']==0:raise ValueError('Affine independent-variable scale must be nonzero')
    if abs(p['a'])>6 or abs(p['h'])>8:raise ValueError('Parameters outside documented bounds')


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio fields supported')
    rng=random.Random(seed)
    if profile:
        if template is not None and template!=profile:raise ValueError('Profile/template mismatch')
        template=profile
    eligible=[n for n,s in TEMPLATES.items() if s['level']==level]
    name=template or rng.choice(eligible)
    if name not in eligible:raise ValueError('Template incompatible with difficulty')
    spec=TEMPLATES[name]  # Select the complete bank before instantiating any option.
    p=dict(parameters) if parameters is not None else {'a':rng.choice((-3,-2,-1,1,2,3)),'h':rng.randint(-4,4)}
    parameter_check(p)
    values=[render(v,p) for v in spec['choices']]
    residuals=[read_equation(v) for v in values]
    flows=[linear_flow(r) for r in residuals]
    target_linear='**NOT**' not in spec['problem']
    selected=[i for i,f in enumerate(flows) if (f is not None)==target_linear]
    if len(selected)!=1:raise ValueError('Whole bank rejected: classification is ambiguous')
    for i,r in enumerate(residuals):
        for s in residuals[:i]:
            ratio=sp.cancel(r/s)
            if not ratio.has(D,D2):raise ValueError('Whole bank rejected: equivalent equations')
    if len(set(values))!=5:raise ValueError('Whole bank rejected: rendered collision')
    solution=render(spec['solution'],p)
    param_key=hashlib.sha256(json.dumps({'template':name,'parameters':p,'domain':'common-local-real'},sort_keys=True).encode()).hexdigest()
    key=hashlib.sha256(json.dumps({'problem':spec['problem'],'solution':solution,'bank':sorted(values)},sort_keys=True).encode()).hexdigest()
    qid=uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy/generated/{KP_UUID}/{VERSION}/{key}')
    fid=uuid.uuid5(qid,'selection')
    answers=[{':answer/id':str(uuid.uuid5(fid,'math:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=answers[selected[0]][':answer/id'];rng.shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':spec['problem'],':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':name,'parameters':p,'parameter_fingerprint':param_key,'content_fingerprint':key,'bank_profile':name,'bank_origin':'observed-structural','authored_extension':p!={'a':1,'h':0},'extension_kind':'affine independent-variable functions','domain':'Local real intervals where all displayed expressions are defined; affine a*x+h>0 may be used. Require y!=0 wherever canceled, y>0 for logarithms/roots, and all denominators nonzero.','source_analysis':{**SOURCE,'question_ids':[spec['source']]},'plot_rating':'none','answer_shape':'complete equation','normalization':{v:None if f is None else str(f) for v,f in zip(values,flows)}}}


# EASY: one equation already in standard form, four nonlinear/order distractors.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: identify the sole nonlinear equation among rearrangeable linear ones.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: y-dependent derivative factors; decide whether cancellation restores linearity.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)


def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    lines=[q[':question/problem'],'']
    lines += [f'- ${a[":answer/value"]}$' for a in f[':answer-field/choices']]
    lines+=['','Worked solution',q[':question/worked-solution']]
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template');parser.add_argument('--profile')
    args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
