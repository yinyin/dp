
# -*- coding: utf-8 -*-

import unittest
import yaml

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
		dpcore.prepare_story_id()

		self.assertEqual(m["story"], storylist[0].story)
		self.assertEqual(m["note"], storylist[0].note)
		self.assertEqual(m["order"], storylist[0].imp_order)
		self.assertEqual(None, storylist[0].imp_value)
		self.assertEqual(m["demo-method"], storylist[0].demo_method)
		self.assertTrue(storylist[0].story_id is not None)
	# ### def test_load_stories_6
# ### class TestStoriesLoad


class TestStoryYAMLnodeDump(unittest.TestCase):
	""" test yamlnodedump_stories() function """
	
	def test_dump_1(self):
		""" generate node object for 1 story """
		
		m = "This is a story"
		storylist_orig = dpcore.load_stories(m)
		
		nodelist = dpcore.yamlnodedump_stories(storylist_orig[0])
		
		yml = yaml.serialize(nodelist)
		#print yml
		c = yaml.load(yml)
		
		storylist_comp = dpcore.load_stories(c)
		self.assertEqual(storylist_comp[0].story, storylist_orig[0].story)
		self.assertEqual(storylist_comp[0].note, storylist_orig[0].note)
	# ### def test_dump_1
	
	def test_dump_2(self):
		""" generate node object2 for 2 story """
		
		m = ["This is story 1.", {"story": "This is story 2.", "sub-story": "This is a substory.\nwhich have 2 lines.",}]
		storylist_orig = dpcore.load_stories(m)
		
		self.assertEqual(1, len(storylist_orig[1].substory))
		
		nodeobjlist = dpcore.yamlnodedump_stories(storylist_orig)
		nodelist = yaml.SequenceNode(tag=u"tag:yaml.org,2002:seq", value=nodeobjlist, flow_style=False)
		
		yml = yaml.serialize(nodelist)
		#print yml
		c = yaml.load(yml)
		
		storylist_comp = dpcore.load_stories(c)
		for idx in range(2):
			self.assertEqual(storylist_comp[idx].story, storylist_orig[idx].story)
			self.assertEqual(storylist_comp[idx].note, storylist_orig[idx].note)
		self.assertEqual(1, len(storylist_comp[1].substory))
	# ### def test_dump_2
# ### class TestStoryYAMLnodeDump


class MockStoryContainer_1(dpcore.StoryContainer):
	def __init__(self):
		super(MockStoryContainer_1, self).__init__();
	# ### def __init__
# ### class MockStoryContainer_1

class TestStoryContainer(unittest.TestCase):
	def setUp(self):
		self.mockcontainer = MockStoryContainer_1()
	# ### def setUp

	def test_add_story_obj(self):
		storylist1 = dpcore.load_stories("This is a story 1.")
		storylist2 = dpcore.load_stories("This is a story 2.")

		self.mockcontainer.append_substory(storylist1[0])
		self.assertEqual(len(self.mockcontainer.substory), 1)
		self.assertEqual(storylist1[0], self.mockcontainer.substory[0])

		self.mockcontainer.append_substory(storylist2[0])
		self.assertEqual(len(self.mockcontainer.substory), 2)
		self.assertEqual(storylist2[0], self.mockcontainer.substory[1])
	# ### def test_add_story_obj

	def test_add_story_list(self):
		storylist1 = dpcore.load_stories(["This is a story 1a.", "This is a story 1b.",])
		storylist2 = dpcore.load_stories(["This is a story 2a.", "This is a story 2b.",])

		self.mockcontainer.append_substory(storylist1)
		self.assertEqual(len(self.mockcontainer.substory), 2)
		for idx in range(len(storylist1)):
			self.assertEqual(storylist1[idx], self.mockcontainer.substory[0+idx])

		self.mockcontainer.append_substory(storylist2)
		self.assertEqual(len(self.mockcontainer.substory), 4)
		for idx in range(len(storylist2)):
			self.assertEqual(storylist2[idx], self.mockcontainer.substory[2+idx])
	# ### def test_add_story_list
# ### class TestStoryContainer



if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 ai nowarp
