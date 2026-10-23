"""Equivalent TeX spellings supported by the installed player packages."""
import re

def normalize(tex):
 # The player has color's CSS syntax, without a separately defined HTML model.
 tex=re.sub(r'\\color\[HTML\]\{([0-9a-fA-F]{6})\}',lambda m:r'\color{#'+m[1]+'}',tex)
 # This player's package list omits boldsymbol. Preserve the exact source
 # mathematical alphabet using Unicode, which its TeX input supports.
 mapping={'f':'𝒇',r'\beta':'𝜷','1':'𝟏'}
 def bold(m):
  payload=m[1] or m[2]
  if payload not in mapping:raise ValueError('Unreviewed boldsymbol '+payload)
  return mapping[payload]
 tex=re.sub(r'\\boldsymbol\s*(?:\{([^{}]*)\}|([A-Za-z0-9]|\\[A-Za-z]+))',bold,tex)
 return tex

def normalize_asset(path,tex,svg):
 tex=normalize(tex)
 markers=list(re.finditer(r'\\\[/?math\]',tex))
 if markers:
  # These titles were rewritten by the source's dollar-marker serialization.
  # The intact SVG drawing, independently, must contain that many dollar glyphs.
  drawing=svg.split('</defs>',1)[-1]
  dollars=len(re.findall(r'<use\b[^>]*href=[\'"]#[^\'"]*-24[\'"]',drawing))
  assert dollars==len(markers)+tex.count(r'\$'),(path,dollars,len(markers))
  tex=re.sub(r'\\\[/?math\]',lambda m:r'\$',tex)
 tex=re.sub(r'(?<!\\)\$',lambda m:r'\$',tex)
 tex=re.sub(r'\\(sech|csch)\b',lambda m:r'\operatorname{'+m[1]+'}',tex)
 return tex
