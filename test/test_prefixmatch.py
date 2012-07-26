
# -*- coding: utf-8 -*-

import unittest

import testing_common

import dpcore


class TestCheckPrefix(unittest.TestCase):
	""" check if _check_prefix function """

	def test_check_uppercase(self):
		subj = "DONE (abcdefg)"

		r = dpcore._check_string_prefix(subj, "DONE")
		self.assertEqual(r, True)

		r = dpcore._check_string_prefix(subj, "FINISH")
		self.assertEqual(r, False)
	# ### def test_check_uppercase

	def test_check_lowercase(self):
		subj = "done (abcdefg)"

		r = dpcore._check_string_prefix(subj, "DONE")
		self.assertEqual(r, True)

		r = dpcore._check_string_prefix(subj, "FINISH")
		self.assertEqual(r, False)
	# ### def test_check_lowercase
# ### class TestCheckPrefix



if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 ai nowarp

