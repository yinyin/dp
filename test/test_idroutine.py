
# -*- coding: utf-8 -*-

import unittest

import testing_common

import dpcore



class MockIdentifiableObject_1(dpcore.IdentifiableObject):
	def __init__(self, keyval, *args, **kwargs):
		super(MockIdentifiableObject_1, self).__init__(*args, **kwargs)

		self.content = keyval
		self.mockid = None
	# ### def __init__

	def get_object_id(self):
		return self.mockid
	# ### def get_object_id

	def set_object_id(self, new_id):
		self.mockid = new_id
	# ### def get_object_id

	def get_object_signature(self):
		if self.content is None:
			return None
		return str(self.content)
	# ### def get_object_signature
# ### class MockIdentifiableObject_1

class TestIdentityGeneration(unittest.TestCase):
	""" test allocate_object_id() function """

	def test_allocate_w_empty_object(self):
		""" allocate id for empty (object signature is None) object """

		objrepo = {}

		mobj = MockIdentifiableObject_1(None)
		mid = dpcore.allocate_object_id(mobj, "T", objrepo)

		self.assertTrue(mid is None)
		self.assertEqual(len(objrepo), 0)
	# ### def test_allocate_w_empty_object

	def test_dup_gen(self):
		""" allocate id twice """

		objrepo = {}

		mobj = MockIdentifiableObject_1(1)
		mid_a = dpcore.allocate_object_id(mobj, "T", objrepo)
		mid_b = dpcore.allocate_object_id(mobj, "T", objrepo)

		self.assertTrue(mid_a is not None)
		self.assertTrue(mid_b is not None)
		self.assertEqual(mid_a, mid_b)
		self.assertEqual(len(objrepo), 1)
		self.assertEqual(objrepo[mid_a], mobj)
	# ### def test_dup_gen

	def test_allocate_for_diffobj(self):
		""" allocate for different objects """

		objrepo = {}

		mobj_a = MockIdentifiableObject_1(1)
		mobj_b = MockIdentifiableObject_1("a")
		mid_a = dpcore.allocate_object_id(mobj_a, "T", objrepo)
		mid_b = dpcore.allocate_object_id(mobj_b, "T", objrepo)

		self.assertTrue(mid_a is not None)
		self.assertTrue(mid_b is not None)
		self.assertNotEqual(mid_a, mid_b)
		self.assertEqual(len(objrepo), 2)
		self.assertEqual(objrepo[mid_a], mobj_a)
		self.assertEqual(objrepo[mid_b], mobj_b)
	# ### def def test_allocate_for_diffobj
# ### class TestIdentityGeneration



if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 ai nowarp
