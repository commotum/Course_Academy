import hashlib,unittest
from run_later_repairs import package_version
class FrozenPackageVersions(unittest.TestCase):
 def test_two_specials_cannot_chain_or_recurse_and_ordinary_resets_base(self):
  base='frozen-base';historic=b'historical-source';quiz=b'quiz7-source'
  actual=[package_version(k,base,historic,quiz) for k in ['14114807','ordinary1','14111253','ordinary2','14118927','ordinary3']]
  self.assertEqual(actual,[hashlib.sha256(base.encode()+historic).hexdigest(),base,hashlib.sha256(base.encode()+historic+quiz).hexdigest(),base,hashlib.sha256(base.encode()+historic).hexdigest(),base])
 def test_package_result_independent_of_previous_order(self):
  base='frozen-base';h=b'h';q=b'q';ids=['14120023','14114807','14111253','ordinary']
  self.assertEqual({i:package_version(i,base,h,q) for i in ids},{i:package_version(i,base,h,q) for i in reversed(ids)})
if __name__=='__main__':unittest.main()
