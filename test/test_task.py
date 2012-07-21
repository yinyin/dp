
# -*- coding: utf-8 -*-

import unittest

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



if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 ai nowarp
