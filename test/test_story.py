
# -*- coding: utf-8 -*-

import unittest

import testing_common

import dpcore


class TestStoriesLoad(unittest.TestCase):
	""" test load_stories() function """
	
	def test_load_stories_1(self):
		""" load story with string object """
		
		m = "This is a story"
		storylist = dpcore.load_stories(m)
		
		self.assertEqual(m, storylist[0].story)
	# ### def test_load_stories_1
	
	def test_load_stories_2(self):
		""" load story with dict object (with story attached) """
		
		m = {"story": "This is a story"}
		storylist = dpcore.load_stories(m)
		
		self.assertEqual(m["story"], storylist[0].story)
	# ### def test_load_stories_2
	
	def test_load_stories_3(self):
		""" load story with dict object (without story attached, but attached valid key-value pair) """
		
		m = {"point": 6}
		storylist = dpcore.load_stories(m)
		
		self.assertEqual(None, storylist[0].story)
	# ### def test_load_stories_3
	
	def test_load_stories_4(self):
		""" load story with dict object (without any valid key-value pair) """
		
		m = {}
		storylist = dpcore.load_stories(m)
		
		self.assertEqual(0, len(storylist))
	# ### def test_load_stories_4

	def test_load_stories_5(self):
		""" load story with list object """
		
		m = ["this is story 1", "this is story 2",]
		storylist = dpcore.load_stories(m)
		
		self.assertEqual(2, len(storylist))
		idx = 0
		for mm in m:
			self.assertEqual(mm, storylist[idx].story)
			idx = idx + 1
	# ### def test_load_stories_5
	
	def test_load_stories_6(self):
		""" load story with dict object (basic information) """
		
		m = {"story": "a story of development.", "note": "* multiple line\n* notes and notes",
				"order": "normal", "value": "", "point": 7, "demo-method": "use demo system to demo."}
		storylist = dpcore.load_stories(m)
		
		self.assertEqual(m["story"], storylist[0].story)
		self.assertEqual(m["note"], storylist[0].note)
		self.assertEqual(m["order"], storylist[0].imp_order)
		self.assertEqual(None, storylist[0].imp_value)
		self.assertEqual(m["demo-method"], storylist[0].demo_method)
		self.assertTrue(storylist[0].story_id is not None)
	# ### def test_load_stories_6
# ### class TestStoriesLoad



if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 ai nowarp
