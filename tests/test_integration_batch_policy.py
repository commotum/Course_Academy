import copy
import importlib.util
import sys
import unittest
from pathlib import Path

from scripts.integration_batch_policy import validate_delivery_batch
from scripts.generator_publish import prepare_records,content_fingerprint

ROOT=Path(__file__).resolve().parents[1]
PACKAGE=ROOT/'reference/mathacademy/repairs/2026-10-20-integration-lesson-quality/17592186184154/package'
sys.path.insert(0,str(PACKAGE))
spec=importlib.util.spec_from_file_location('integration_forward_test',PACKAGE/'forward.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
KP=17592186184154

class IntegrationBatchPolicyTests(unittest.TestCase):
 def test_source_bounded_batch_passes(self):
  for kp,bands in ((17592186184153,('moderate','hard')),(KP,('easy','moderate')),(17592186184155,('moderate','hard'))):
   for band in bands:validate_delivery_batch(g.sample(kp,5,41,band),kp)
 def test_same_power_pattern_required_in_every_option(self):
  rows=g.sample(KP,5,41,'moderate');r=next(r for r in rows if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio'))
  r['generation']['bank_terms'][0][0][1]='19'
  with self.assertRaisesRegex(ValueError,'same power'):validate_delivery_batch(rows,KP)
 def test_sign_matching_cannot_give_away_the_answer(self):
  rows=g.sample(KP,5,41,'easy');row=rows[0]['generation']['bank_terms'][0];row[0][0]=str(-g.F(row[0][0]))
  with self.assertRaisesRegex(ValueError,'sign pattern'):validate_delivery_batch(rows,KP)
 def test_copying_the_constant_cannot_identify_an_option(self):
  kp=17592186184155;rows=g.sample(kp,5,41,'moderate');r=next(r for r in rows if r['generation']['family']=='polynomial-three');j=next(j for j,(c,p)in enumerate(r['generation']['input_terms'])if g.F(p)==0);c=g.F(r['generation']['bank_terms'][0][j][0]);r['generation']['bank_terms'][0][j][0]=str(2*c)
  with self.assertRaisesRegex(ValueError,'Copied constants'):validate_delivery_batch(rows,kp)
 def test_sign_flip_does_not_count_as_a_different_structure(self):
  rows=g.sample(KP,5,41,'moderate');clone=copy.deepcopy(rows[0]);clone['generation']['input_terms'][0][0]=str(-g.F(clone['generation']['input_terms'][0][0]));rows[1]=clone
  with self.assertRaisesRegex(ValueError,'sign-only clone'):validate_delivery_batch(rows,KP)
 def test_after_deduplication_losing_other_families_rejects_publication(self):
  candidates=g.sample(KP,20,71,'moderate');radicals=[r for r in candidates if r['generation']['family']=='radical-product'][:2];others=[next(r for r in candidates if r['generation']['family']==family)for family in ('power-quotient','direct-quotient-blank')]
  with self.assertRaisesRegex(ValueError,'family coverage'):
   prepare_records(radicals+others,KP,g.IDS[KP],{content_fingerprint(r['question'])for r in others},ROOT,ROOT,localizer=lambda r,*args:copy.deepcopy(r))
 def test_scope_crossing_rejected(self):
  rows=g.sample(KP,5,41,'easy');rows[0]['generation']['input_terms'][0][1]='-1'
  with self.assertRaisesRegex(ValueError,'elementary power'):validate_delivery_batch(rows,KP)
 def test_legacy_unreviewed_contract_is_not_silently_published(self):
  rows=g.sample(KP,5,41,'moderate');rows[0]['generation'].pop('batch_contract')
  with self.assertRaisesRegex(ValueError,'batch contract'):validate_delivery_batch(rows,KP)

if __name__=='__main__':unittest.main()
