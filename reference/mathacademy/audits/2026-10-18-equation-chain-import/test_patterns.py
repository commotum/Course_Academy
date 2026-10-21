"""Controls for the read-only layout detector; no database connection."""
import json,unittest
from .patterns import detect,HERE
class PatternTests(unittest.TestCase):
 def test_complete_equations_and_correct_continuations_are_not_flagged(self):
  for text in (r'$$\begin{aligned}x &= 1 \\ y &= 2\end{aligned}$$',r'$$\begin{aligned}x &= y \\ &= z\end{aligned}$$',r'$\frac{x}{y}=z$',r'Plain prose about aligned objects.'):
   self.assertEqual(detect(text)[0],[])
 def test_valid_legacy_command_is_review_only(self):
  reasons,_=detect(r'$$\eqalign{x &= y \\ &= z}$$')
  self.assertEqual(reasons,['legacy-eqalign'])
 def test_mixed_incomplete_chain_is_separate_from_safe_complete_chain(self):
  reasons,_=detect(r'$$\begin{aligned}a &= \\ b &= \\ &= c\end{aligned}$$')
  self.assertIn('partial-empty-rhs-chain',reasons)
  self.assertNotIn('empty-rhs-equality-chain',reasons)
 def test_legacy_optional_spacing_is_a_single_backslash_row_break(self):
  reasons,_=detect(r'$$\eqalign{a &= \[5pt] b &= \[5pt] c}$$')
  self.assertIn('single-backslash-row-break',reasons)
  self.assertIn('empty-rhs-equality-chain',reasons)
 def test_replayed_archival_formulas_are_detected_and_current_preparation_is_clean(self):
  replay=json.loads((HERE/'reproduction.json').read_text());self.assertTrue(replay['passed'])
  for fixture in replay['fixtures']:
   reasons,_=detect(fixture['raw_capture']);self.assertIn('empty-rhs-equality-chain',reasons)
   self.assertEqual(detect(fixture['current_preparation'])[0],[])
 def test_unsupported_require_is_identified_independently(self):
  self.assertEqual(detect(r'$$\require{cancel}\cancel{x}$$')[0],['unsupported-require'])
if __name__=='__main__':unittest.main()
