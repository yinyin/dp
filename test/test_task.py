
# -*- coding: utf-8 -*-

import unittest
import yaml

import testing_common

import dpcore


class TestTaskLoad(unittest.TestCase):
	""" test load_tasks() function """

	def test_load_tasks_1(self):
		""" load task with string object """

		m = "This is a task"
		tasklist = dpcore.load_tasks(m)

		self.assertEqual(m, tasklist[0].task)
	# ### def test_load_tasks_1

	def test_load_tasks_2(self):
		""" load task with dict object (with task definition attached) """

		m = {"t": "This is a task"}
		tasklist = dpcore.load_tasks(m)

		self.assertEqual(m["t"], tasklist[0].task)
	# ### def test_load_tasks_2

	def test_load_tasks_3(self):
		""" load task with dict object (without task definition attached, but attached valid key-value pair) """

		m = {"point": 6}
		tasklist = dpcore.load_tasks(m)

		self.assertEqual(None, tasklist[0].task)
	# ### def test_load_tasks_3

	def test_load_tasks_4(self):
		""" load task with dict object (without any valid key-value pair) """

		m = {}
		tasklist = dpcore.load_tasks(m)

		self.assertEqual(0, len(tasklist))
	# ### def test_load_tasks_4

	def test_load_tasks_5(self):
		""" load task with list object """

		m = ["this is task 1", "this is task 2",]
		tasklist = dpcore.load_tasks(m)

		self.assertEqual(2, len(tasklist))
		idx = 0
		for mm in m:
			self.assertEqual(mm, tasklist[idx].task)
			idx = idx + 1
	# ### def test_load_tasks_5

	def test_load_tasks_6(self):
		""" load story with dict object (basic information) """

		m = {"t": "a task of development.", "note": "* multiple line\n* notes and notes",
				"point": 7, "estimated-time": 3, "status": "new", "test-method": "use demo system to demo."}
		tasklist = dpcore.load_tasks(m)
		dpcore.prepare_task_id()

		self.assertEqual(m["t"], tasklist[0].task)
		self.assertEqual(m["note"], tasklist[0].note)
		self.assertEqual(7, tasklist[0].point)
		self.assertEqual(m["estimated-time"], tasklist[0].estimated_time)
		self.assertEqual(None, tasklist[0].status)
		self.assertEqual(m["test-method"], tasklist[0].test_method)
		self.assertTrue(tasklist[0].task_id is not None)
	# ### def test_load_tasks_6
# ### class TestTaskLoad


class TestTaskYAMLnodeDump(unittest.TestCase):
	""" test yamlnodedump_tasks() function """
	
	def test_dump_1(self):
		""" generate node object for 1 task """
		
		m = "This is a task"
		tasklist_orig = dpcore.load_tasks(m)
		
		nodelist = dpcore.yamlnodedump_tasks(tasklist_orig[0])
		
		yml = yaml.serialize(nodelist)
		#print yml
		c = yaml.load(yml)
		
		tasklist_comp = dpcore.load_tasks(c)
		self.assertEqual(tasklist_comp[0].task, tasklist_orig[0].task)
		self.assertEqual(tasklist_comp[0].note, tasklist_orig[0].note)
	# ### def test_dump_1
	
	def test_dump_2(self):
		""" generate node object2 for 2 task """
		
		m = ["This is task 1.", {"t": "This is task 2.", "sub-task": "This is a subtask.\nwhich have 2 lines.",}]
		tasklist_orig = dpcore.load_tasks(m)
		
		self.assertEqual(1, len(tasklist_orig[1].subtask))
		
		nodeobjlist = dpcore.yamlnodedump_tasks(tasklist_orig)
		nodelist = yaml.SequenceNode(tag=u"tag:yaml.org,2002:seq", value=nodeobjlist, flow_style=False)
		
		yml = yaml.serialize(nodelist)
		#print yml
		c = yaml.load(yml)
		
		tasklist_comp = dpcore.load_tasks(c)
		for idx in range(2):
			self.assertEqual(tasklist_comp[idx].task, tasklist_orig[idx].task)
			self.assertEqual(tasklist_comp[idx].note, tasklist_orig[idx].note)
		self.assertEqual(1, len(tasklist_comp[1].subtask))
	# ### def test_dump_2
# ### class TestStoryYAMLnodeDump


class MockTaskContainer_1(dpcore.TaskContainer):
	def __init__(self):
		super(MockTaskContainer_1, self).__init__();
	# ### def __init__
# ### class MockTaskContainer_1

class TestTaskContainer(unittest.TestCase):
	def setUp(self):
		self.mockcontainer = MockTaskContainer_1()
	# ### def setUp

	def test_add_task_obj(self):
		tasklist1 = dpcore.load_tasks("This is a task 1.")
		tasklist2 = dpcore.load_tasks("This is a task 2.")

		self.mockcontainer.append_subtask(tasklist1[0])
		self.assertEqual(len(self.mockcontainer.subtask), 1)
		self.assertEqual(tasklist1[0], self.mockcontainer.subtask[0])

		self.mockcontainer.append_subtask(tasklist2[0])
		self.assertEqual(len(self.mockcontainer.subtask), 2)
		self.assertEqual(tasklist2[0], self.mockcontainer.subtask[1])
	# ### def test_add_task_obj

	def test_add_task_list(self):
		tasklist1 = dpcore.load_tasks(["This is a task 1a.", "This is a task 1b.",])
		tasklist2 = dpcore.load_tasks(["This is a task 2a.", "This is a task 2b.",])

		self.mockcontainer.append_subtask(tasklist1)
		self.assertEqual(len(self.mockcontainer.subtask), 2)
		for idx in range(len(tasklist1)):
			self.assertEqual(tasklist1[idx], self.mockcontainer.subtask[0+idx])

		self.mockcontainer.append_subtask(tasklist2)
		self.assertEqual(len(self.mockcontainer.subtask), 4)
		for idx in range(len(tasklist2)):
			self.assertEqual(tasklist2[idx], self.mockcontainer.subtask[2+idx])
	# ### def test_add_task_list
# ### class TestTaskContainer



if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 ai nowarp
