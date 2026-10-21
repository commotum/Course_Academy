"""Regressions for source fidelity of the bulk repair converter."""
import unittest
import convert_source as c
class SourceTests(unittest.TestCase):
 def convert(self,body):return c.convert_source({'id':'control','source_html':'<math>'+body+'</math>'})
 def test_percent_is_escaped_in_math(self):
  r=self.convert('<mn>42</mn><mi mathvariant="normal">%</mi>');self.assertEqual(r['errors'],[]);self.assertIn(r'\%',r['tex'])
 def test_fraction_rule_is_preserved(self):
  self.assertEqual(self.convert('<mfrac><mn>7</mn><mn>2</mn></mfrac>')['tex'],r'\frac{7}{2}')
  self.assertEqual(self.convert('<mfrac linethickness="0"><mn>7</mn><mn>2</mn></mfrac>')['tex'],r'\genfrac{}{}{0pt}{}{7}{2}')
 def test_hidden_zero_width_is_not_visible_p(self):
  self.assertEqual(self.convert('<mpadded width="0"><mphantom><mi>p</mi></mphantom></mpadded>')['tex'],r'\vphantom{p}')
 def test_bbox_collapse_preserves_parent_color(self):
  r=self.convert('<mstyle mathcolor="blue" style="border:1pt solid black"><mpadded width="+4pt" height="+2pt" depth="+2pt" lspace="2pt"><mphantom><mn>0</mn></mphantom></mpadded></mstyle>')
  self.assertEqual(r['errors'],[]);self.assertIn(r'\color{blue}',r['tex']);self.assertIn(r'\phantom{0}',r['tex']);self.assertIn('border:1pt solid black',r['tex'])
 def test_empty_trailing_table_cells_are_only_padding(self):
  r=self.convert('<mtable columnlines="solid"><mtr><mtd><mn>1</mn></mtd><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>3</mn></mtd></mtr></mtable>')
  self.assertEqual(r['errors'],[]);self.assertEqual(r['tex'],r'\begin{array}{c|c}1 & 2 \\ 3 & \end{array}')
 def test_strike_directions_are_distinct(self):
  for source,command in [('updiagonalstrike','cancel'),('downdiagonalstrike','bcancel'),('updiagonalstrike downdiagonalstrike','xcancel')]:
   self.assertEqual(self.convert('<menclose notation="'+source+'"><mn>3</mn></menclose>')['tex'],'\\'+command+'{3}')
 def test_balanced_source_markers_preserve_math_and_prose(self):
  r=self.convert('<mtext>if [math]x[/math] is even</mtext>');self.assertEqual(r['errors'],[]);self.assertEqual(r['tex'],r'\text{if } {x} \text{ is even}')
  self.assertTrue(self.convert('<mtext>if [math]x is even</mtext>')['errors'])
 def test_mixed_math_box_is_math_mode(self):
  r=c.convert_source({'id':'control','source_html':r'<title>\fbox{<mjx-container><math><mphantom><mn>00</mn></mphantom></math></mjx-container>}</title>'})
  self.assertEqual(r['errors'],[]);self.assertIn(r'\boxed',r['tex']);self.assertNotIn('{{',r['tex']);self.assertIn(r'\phantom{00}',r['tex'])
 def test_unsupported_geometry_fails(self):
  self.assertTrue(self.convert('<mpadded width="0"><mi>x</mi></mpadded>')['errors'])
  self.assertTrue(self.convert('<mtable><mtr><mtd columnspan="2"><mn>1</mn></mtd></mtr></mtable>')['errors'])
 def test_hat_without_attribute_is_retained(self):
  self.assertEqual(self.convert('<mover><mi>x</mi><mo>^</mo></mover>')['tex'],r'\hat{x}')
 def test_explicit_displaystyle_inside_array_is_preserved(self):
  r=self.convert('<mtable displaystyle="true"><mtr><mtd><mfrac><mn>1</mn><mn>5</mn></mfrac></mtd></mtr></mtable>')
  self.assertEqual(r['errors'],[]);self.assertIn(r'\displaystyle \frac{1}{5}',r['tex'])
 def test_mixed_text_wrapper_keeps_fragment_in_math_mode(self):
  r=c.convert_source({'id':'control','source_html':r'<title>\textrm{a cycle <mjx-container><math><msub><mi>v</mi><mn>1</mn></msub></math></mjx-container>}</title>'})
  self.assertEqual(r['errors'],[]);self.assertIn(r'\textrm{a cycle }',r['tex']);self.assertIn(r'{v}_{1}',r['tex']);self.assertNotIn(r'\textrm{ {v}',r['tex'])
 def test_wrap_preserves_invisible_right_delimiter(self):
  from prepare import wrap
  after=wrap(r'\left\{\begin{array}{l}x=1\end{array}\right.','$x=1$.',None)
  self.assertIn(r'\right.$',after);self.assertTrue(after.endswith('$.'))
 def test_zero_rule_stack_uses_full_height_paired_source_fences(self):
  r=self.convert('<mstyle displaystyle="true"><mrow><mrow data-mjx-texclass="OPEN"><mo minsize="2.047em" maxsize="2.047em">(</mo></mrow><mfrac linethickness="0"><mn>4</mn><mn>4</mn></mfrac><mrow data-mjx-texclass="CLOSE"><mo minsize="2.047em" maxsize="2.047em">)</mo></mrow></mrow></mstyle>')
  self.assertEqual(r['errors'],[]);self.assertIn(r'\left(',r['tex']);self.assertIn(r'\right)',r['tex']);self.assertIn(r'\genfrac{}{}{0pt}{}{4}{4}',r['tex'])
 def test_explicitly_fixed_source_fences_are_not_stretched(self):
  r=self.convert('<mo stretchy="false">(</mo><mfrac linethickness="0"><mn>4</mn><mn>4</mn></mfrac><mo stretchy="false">)</mo>')
  self.assertEqual(r['errors'],[]);self.assertNotIn(r'\left',r['tex'])
 def test_mathjax_literal_hash_in_text_is_not_a_backslash(self):
  self.assertEqual(self.convert('<mtext># of samples</mtext>')['tex'],r'\text{# of samples}')
if __name__=='__main__':unittest.main()
