
# -*- coding: utf-8 -*-

import datetime
import unittest
import yaml

import testing_common

import dpcore


class TestLogLoad(unittest.TestCase):
	""" test load_logs() function """

	def test_load_logs_1(self):
		""" load log with string object """

		m = "This is a log"
		loglist = dpcore.load_logs(m)

		self.assertEqual(m, loglist[0].log)
	# ### def test_load_tasks_1

	def test_load_logs_2(self):
		""" load log with dict object (with task definition attached) """

		m = {"l": "This is a log"}
		loglist = dpcore.load_logs(m)

		self.assertEqual(m["l"], loglist[0].log)
	# ### def test_load_logs_2

	def test_load_logs_4(self):
		""" load task with dict object (without any content) """

		m = {}
		loglist = dpcore.load_logs(m)

		self.assertEqual(0, len(loglist))
	# ### def test_load_logs_4

	def test_load_logs_5(self):
		""" load log with list object """

		m = ["this is log 1", "this is log 2",]
		loglist = dpcore.load_logs(m)

		self.assertEqual(2, len(loglist))
		idx = 0
		for mm in m:
			self.assertEqual(mm, loglist[idx].log)
			idx = idx + 1
	# ### def test_load_logs_5

	def test_load_logs_6(self):
		""" load log with dict object (basic information) """

		m = {"l": "a log of development.", "record-time": "2012-07-20 03:12:59",
				"author": "Test User"}
		loglist = dpcore.load_logs(m)

		self.assertEqual(m["l"], loglist[0].log)
		self.assertEqual(datetime.datetime(2012, 7, 20, 3, 12, 59), loglist[0].record_time)
		self.assertEqual(m["author"], loglist[0].author)
	# ### def test_load_logs_6
# ### class TestLogLoad


class TestLogYAMLnodeDump(unittest.TestCase):
	""" test yamlnodedump_logs() function """
	
	def test_dump_1(self):
		""" generate node object for 1 log """
		
		m = "This is a log record"
		loglist_orig = dpcore.load_logs(m)
		
		nodelist = dpcore.yamlnodedump_logs(loglist_orig[0])
		
		yml = yaml.serialize(nodelist)
		#print yml
		c = yaml.load(yml)
		
		loglist_comp = dpcore.load_logs(c)
		self.assertEqual(loglist_comp[0].log, loglist_orig[0].log)
		self.assertEqual(loglist_comp[0].action, loglist_orig[0].action)
	# ### def test_dump_1
	
	def test_dump_2(self):
		""" generate node object2 for 2 task """
		
		m = ["This is log 1.", "this is log message 2."]
		loglist_orig = dpcore.load_logs(m)
		
		nodeobjlist = dpcore.yamlnodedump_logs(loglist_orig)
		nodelist = yaml.SequenceNode(tag=u"tag:yaml.org,2002:seq", value=nodeobjlist, flow_style=False)
		
		yml = yaml.serialize(nodelist)
		#print yml
		c = yaml.load(yml)
		
		loglist_comp = dpcore.load_logs(c)
		for idx in range(2):
			self.assertEqual(loglist_comp[idx].log, loglist_orig[idx].log)
			self.assertEqual(loglist_comp[idx].action, loglist_orig[idx].action)
	# ### def test_dump_2
# ### class TestLogYAMLnodeDump


class MockLogContainer_1(dpcore.LogContainer):
	def __init__(self):
		super(MockLogContainer_1, self).__init__();
	# ### def __init__
# ### class MockLogContainer_1

class TestLogContainer(unittest.TestCase):
	def setUp(self):
		self.mockcontainer = MockLogContainer_1()
	# ### def setUp

	def test_add_log_obj(self):
		loglist1 = dpcore.load_logs("This is log 1.")
		loglist2 = dpcore.load_logs("This is log 2.")

		self.mockcontainer.append_log(loglist1[0])
		self.assertEqual(len(self.mockcontainer.logrecord), 1)
		self.assertEqual(loglist1[0], self.mockcontainer.logrecord[0])

		self.mockcontainer.append_log(loglist2[0])
		self.assertEqual(len(self.mockcontainer.logrecord), 2)
		self.assertEqual(loglist2[0], self.mockcontainer.logrecord[1])
	# ### def test_add_log_obj

	def test_add_log_list(self):
		loglist1 = dpcore.load_logs(["This is log 1a.", "This is log 1b.",])
		loglist2 = dpcore.load_logs(["This is log 2a.", "This is log 2b.",])

		self.mockcontainer.append_log(loglist1)
		self.assertEqual(len(self.mockcontainer.logrecord), 2)
		for idx in range(len(loglist1)):
			self.assertEqual(loglist1[idx], self.mockcontainer.logrecord[0+idx])

		self.mockcontainer.append_log(loglist2)
		self.assertEqual(len(self.mockcontainer.logrecord), 4)
		for idx in range(len(loglist2)):
			self.assertEqual(loglist2[idx], self.mockcontainer.logrecord[2+idx])
	# ### def test_add_log_list
# ### class TestLogContainer



if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 ai nowarp
