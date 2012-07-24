
# -*- coding: utf-8 -*-

import os
import sys
import re
import hashlib
import base64
import datetime

import yaml



_rt_config = None	# runtime configuration


class IdentifiableObject(object):
	""" defined an interface for objects which can have an identify"""

	def __init__(self, *args, **kwargs):
		super(IdentifiableObject, self).__init__(*args, **kwargs)
	# ### def __init__

	def get_object_id(self):
		return None
	# ### def get_object_id

	def set_object_id(self, new_id):
		pass
	# ### def get_object_id

	def get_object_signature(self):
		return None
	# ### def get_object_signature
# ### class IdentifiableObject

def __build_object_id(sig, attempt, prefix):
	""" create id for given object signature

	Argument:
		sig - object signature/content
		attempt - number of attempts
		prefix - prefix of identity
	Return:
		candidate identity
	"""

	h = hashlib.md5(sig+str(attempt))
	b64digest = base64.b64encode(h.digest(), "ZY")
	return prefix + b64digest[0:22]
# ### def __build_object_id

def allocate_object_id(idableobj, idprefix, objectrepo):
	""" allocate a unique id for given identifiable object

	Argument:
		idableobj - an IdentifiableObject object
		idprefix - prefix of identity
		objectrepo - object repository (a dict which has identity as key and object as value)
	Return:
		allocated identity
	"""

	idableobj_id = idableobj.get_object_id()
	idableobj_sig = idableobj.get_object_signature()
	if (idableobj_id is not None) or (idableobj_sig is None):
		return idableobj_id

	attempt = 0
	idcandidate = __build_object_id(idableobj_sig, attempt, idprefix)
	while idcandidate in objectrepo:
		attempt = attempt + 1
		idcandidate = __build_object_id(idableobj_sig, attempt, idprefix)

	objectrepo[idcandidate] = idableobj
	idableobj.set_object_id(idcandidate)

	return idcandidate
# ### def _allocate_object_id



def _is_empty_value(v):
	if ( (v is None)
			or ( isinstance(v, (str, unicode,)) and (v.upper() in ("NA", "N/A", "NEW", "-",)) ) ):
		return True
	return False
# ### def _is_empty_value



class StoryContainer(object):
	def __init__(self, *args, **kwargs):
		super(StoryContainer, self).__init__(*args, **kwargs)

		self.substory = []
	# ### def __init__

	def append_substory(self, substory):
		if isinstance(substory, Story):
			self.substory.append(substory)
		elif isinstance(substory, (list, tuple,)) and (len(substory) > 0):
			self.substory.extend(substory)
	# ### def append_substory
# ### class StoryContainer

class TaskContainer(object):
	def __init__(self, *args, **kwargs):
		super(TaskContainer, self).__init__(*args, **kwargs)

		self.subtask = []
	# ### def __init__

	def append_subtask(self, subtask):
		if isinstance(subtask, Task):
			self.subtask.append(subtask)
		elif isinstance(subtask, (list, tuple,)) and (len(subtask) > 0):
			self.subtask.extend(subtask)
	# ### def append_subtask
# ### class TaskContainer

class LogContainer(object):
	def __init__(self, *args, **kwargs):
		super(LogContainer, self).__init__(*args, **kwargs)

		self.logrecord = []
	# ### def __init__

	def append_log(self, logrec):
		if isinstance(logrec, Log):
			self.logrecord.append(logrec)
		elif isinstance(logrec, (list, tuple,)) and (len(logrec) > 0):
			self.logrecord.extend(logrec)
	# ### def append_log
# ### class LogContainer


_every_object = {}

_all_story = []
_all_task = []


class Story(IdentifiableObject, StoryContainer, TaskContainer, LogContainer):
	def __init__(self, story_id=None, story=None, note=None, imp_order=None, imp_value=None, point=None, demo_method=None, sort_order_key=None, *args, **kwargs):
		super(Story, self).__init__(*args, **kwargs)

		self.story_id = story_id
		self.story = story
		self.note = note
		self.imp_order = imp_order
		self.imp_value = imp_value
		self.point = point
		self.demo_method = demo_method

		self.sort_order_key = sort_order_key

		if self.story_id is not None:
			_every_object[self.story_id] = self

		_all_story.append(self)
	# ### def __init__

	def prepare_story_id(self):
		""" generate story-id if it is not present
		"""

		if self.story_id is None:
			self.story_id = allocate_object_id(self, "C", _every_object)
	# ### def __prepare_story_id

	def __repr__(self):
		return "%s.Story(story_id=%r, story=%r, note=%r, imp_order=%r, imp_value=%r, point=%r, demo_method=%r, sort_order_key=%r)" % (self.__module__, self.story_id, self.story, self.note, self.imp_order, self.imp_value, self.point, self.demo_method, self.sort_order_key,)
	# ### def __repr__


	def is_empty(self):
		""" check if the story is empty
		"""

		if ( (self.story_id is None)
				and (self.story is None)
				and (self.note is None)
				and _is_empty_value(self.imp_order)
				and _is_empty_value(self.imp_value)
				and _is_empty_value(self.point)
				and (self.demo_method is None)
				and (0 == len(self.substory))
				and (0 == len(self.subtask))
				and (0 == len(self.logrecord)) ):
			return True
		return False
	# ### def is_empty


	def get_object_id(self):
		return self.story_id
	# ### def get_object_id

	def set_object_id(self, new_id):
		self.story_id = new_id
	# ### def get_object_id

	def get_object_signature(self):
		if self.story is None:
			return None
		return str(self)
	# ### def get_object_signature
# ### class Story

class Task(IdentifiableObject, TaskContainer, LogContainer):
	def __init__(self, task_id=None, task=None, note=None, estimated_time=None, point=None, status=None, test_method=None, *args, **kwargs):
		super(Task, self).__init__(*args, **kwargs)

		self.task_id = task_id
		self.task = task
		self.note = note
		self.estimated_time = estimated_time
		self.point = point
		self.status = status
		self.test_method = test_method

		if self.task_id is not None:
			_every_object[self.task_id] = self

		_all_task.append(self)
	# ### def __init__

	def prepare_task_id(self):
		if self.task_id is None:
			self.task_id = allocate_object_id(self, "T", _every_object)
	# ### def __prepare_task_id

	def __repr__(self):
		return "%s.Task(task_id=%r, task=%r, note=%r, estimated_time=%r, point=%r, status=%r, test_method=%r)" % (self.__module__, self.task_id, self.task, self.note, self.estimated_time, self.point, self.status, self.test_method,)
	# ### def __repr__


	def is_empty(self):
		""" check if the story is empty
		"""

		if ( (self.task_id is None)
				and (self.task is None)
				and (self.note is None)
				and _is_empty_value(self.estimated_time)
				and _is_empty_value(self.point)
				and _is_empty_value(self.status)
				and (self.test_method is None)
				and (0 == len(self.subtask))
				and (0 == len(self.logrecord)) ):
			return True
		return False
	# ### def is_empty
	
	def set_status(self, new_status):
		self.status = new_status
	# ### def set_status


	def get_object_id(self):
		return self.task_id
	# ### def get_object_id

	def set_object_id(self, new_id):
		self.task_id = new_id
	# ### def get_object_id

	def get_object_signature(self):
		if self.task is None:
			return None
		return str(self)
	# ### def get_object_signature
# ### class Task

class Log(object):
	def __init__(self, log_id=None, log=None, record_time=None, author=None, action=None, *args, **kwargs):

		super(Log, self).__init__(*args, **kwargs)

		self.log_id = log_id
		self.log = log
		self.record_time = record_time
		self.author = author
		self.action = action
		
		if not self.is_empty():
			if self.record_time is None:
				self.record_time = datetime.datetime.now()
			if self.author is None:
				self.author = _rt_config.username
	# ### def __init__

	def __repr__(self):
		return "%s.Log(log_id=%r, log=%r, record_time=%r, author=%r, action=%r)" % (self.__module__, self.log_id, self.log, self.record_time, self.author, self.action,)
	# ### def __repr__

	def is_empty(self):
		if ( (self.log_id is None)
				and (self.log is None)
				and (self.author is None)
				and (self.action is None) ):
			return True
		return False
	# ### def is_empty
# ### class Log



def _convert_to_string(v):
	""" convert given object to string

	If input object is None or empty string None then will be return

	Argument:
		v - the object to be convert
	Return:
		resulted unicode string or None if given object is empty
	"""

	try:
		if v is not None:
			v = unicode(v).strip()
			if 0 == len(v):
				v = None
	except Exception as e:
		v = None

	return v
# ### def _convert_to_string

def _convert_to_integer(v):
	""" convert given object to integer

	If input object is None, empty string or non-numerical string then None will be return

	Argument:
		v - the object to be convert
	Return:
		resulted integer or None if given object is empty
	"""

	try:
		if v is not None:
			v = unicode(v).strip()
			if 0 == len(v):
				v = None
			else:
				v = int(v)
	except Exception as e:
		v = None

	return v
# ### def _convert_to_integer

__regex_date = re.compile('(([0-9]{2,4})(-|/))?([0-9]+)(-|/)([0-9]+)(.*)$')
__regex_time_1 = re.compile('([0-9]{1,2})(\:|,|.)([0-9]{1,2})((\:|,|.)([0-9]{1,2}))?')
__regex_time_2 = re.compile('([0-9]{2})(([0-9]{2})([0-9]{2})?)?')
def _convert_to_datetime(v):
	""" convert given object to datetime

	If input object is None, empty string or non-numerical string then None will be return

	Argument:
		v - the object to be convert
	Return:
		resulted integer or None if given object is empty
	"""

	if v is None:
		return None

	try:
		v = str(v)
		n = datetime.datetime.now()

		year = n.year
		month = n.month
		day = n.day
		hour = 0
		minute = 0
		second = 0

		matched = False

		# {{{ matching date part
		m = __regex_date.search(v)
		if m is not None:
			m_year = _convert_to_integer(m.group(2))
			if m_year is not None:
				if m_year < 70:
					year = m_year + 2000
				elif m_year < 1000:
					year = m_year + 1900
				else:
					year = m_year
			month = int(m.group(4))
			day = int(m.group(6))

			v = m.group(7)

			matched = True
		# }}} matching date part

		# {{{ matching time part
		m = __regex_time_1.search(v)
		if m is not None:
			hour = int(m.group(1))
			minute = int(m.group(3))
			m_second = _convert_to_integer(m.group(6))
			if m_second is not None:
				second = m_second

			matched = True
		else:
			m = __regex_time_2.search(v)
			if m is not None:
				hour = int(m.group(1))
				m_minute = _convert_to_integer(m.group(3))
				if m_minute is not None:
					minute = m_minute
				m_second = _convert_to_integer(m.group(4))
				if m_second is not None:
					second = m_second

				matched = True
		# }}} matching time part

		if matched:
			return datetime.datetime(year, month, day, hour, minute, second)
	except Exception as e:
		print e
		pass
	return None
# ### def _convert_to_datetime


def _select_scalar_style(v):
	if isinstance(v, (str, unicode,)):
		if "\n" in v:
			return "|"
	return None
# ### def _select_scalar_style

def _attach_mapping_value(mapping, mkey, mvalue, alwaysattach=False, styleselection=False):
	if mvalue is None:
		if False == alwaysattach:
			return False
		mo = yaml.ScalarNode(tag=u"tag:yaml.org,2002:null", value=u"")
	else:
		nodestyle = None
		if styleselection:
			nodestyle = _select_scalar_style(mvalue)
		if isinstance(mvalue, float):
			mo = yaml.ScalarNode(tag=u"tag:yaml.org,2002:float", value=unicode(mvalue), style=nodestyle)
		elif isinstance(mvalue, int):
			mo = yaml.ScalarNode(tag=u"tag:yaml.org,2002:int", value=unicode(mvalue), style=nodestyle)
		elif isinstance(mvalue, datetime.datetime):
			mo = yaml.ScalarNode(tag=u"tag:yaml.org,2002:timestamp", value=unicode(mvalue), style=nodestyle)
		else:
			mo = yaml.ScalarNode(tag=u"tag:yaml.org,2002:str", value=unicode(mvalue), style=nodestyle)
	
	mapping.append( (yaml.ScalarNode(tag=u"tag:yaml.org,2002:str", value=mkey), mo,) )
	
	return True
# ### def _attach_mapping_value

def _attach_mapping_sequence(mapping, mkey, mseq, alwaysattach=False, flowstyle=None):
	if 0 == len(mseq):
		if False == alwaysattach:
			return False
		mo = yaml.ScalarNode(tag=u"tag:yaml.org,2002:null", value=u"")
	else:
		mo = yaml.SequenceNode(tag=u"tag:yaml.org,2002:seq", value=mseq, flow_style=flowstyle)
	
	mapping.append( (yaml.ScalarNode(tag=u'tag:yaml.org,2002:str', value=mkey), mo,) )
	
	return True
# ### def _attach_mapping_sequence



def load_stories(m):
	""" load stories from m
	"""

	result = []

	if isinstance(m, (list, tuple,)):
		for mm in m:
			result.extend(load_stories(mm))
	elif isinstance(m, (str, unicode,)):
		m = m.strip()
		if len(m) > 0:
			return load_stories({"story": m})
	elif isinstance(m, dict):
		story_id = None
		story = None
		note = None
		imp_order = None
		imp_value = None
		point = None
		demo_method = None

		sort_order_key = None

		sub_stories = None
		sub_tasks = None
		logrecords = None

		is_accepted_any_attribute = False

		if "story-id" in m:
			story_id = str(m["story-id"])
			is_accepted_any_attribute = True
		if "story" in m:
			story = _convert_to_string(m["story"])
			is_accepted_any_attribute = True
		if "note" in m:
			note = _convert_to_string(m["note"])
			is_accepted_any_attribute = True
		if "order" in m:
			imp_order = _convert_to_string(m["order"])
			if imp_order is not None:
				v = imp_order.upper()
				if "HIGH" == v:
					sort_order_key = 9
				elif "NORMAL" == v:
					sort_order_key = 5
				elif "LOG" == v:
					sort_order_key = 1
			is_accepted_any_attribute = True
		if "value" in m:
			imp_value = _convert_to_string(m["value"])
			is_accepted_any_attribute = True
		if "point" in m:
			point = _convert_to_integer(m["point"])
			is_accepted_any_attribute = True
		if "demo-method" in m:
			demo_method = _convert_to_string(m["demo-method"])
			is_accepted_any_attribute = True
		if "sub-story" in m:
			sub_stories = load_stories(m["sub-story"])
			is_accepted_any_attribute = True
		if "task" in m:
			sub_tasks = load_tasks(m["task"])
			is_accepted_any_attribute = True
		if "log" in m:
			logrecords = load_logs(m["log"])
			is_accepted_any_attribute = True

		if is_accepted_any_attribute:
			obj = Story(story_id, story, note, imp_order, imp_value, point, demo_method, sort_order_key)
			if sub_stories is not None:
				obj.append_substory(sub_stories)
			if sub_tasks is not None:
				obj.append_subtask(sub_tasks)
			if logrecords is not None:
				obj.append_log(logrecords)
			
			if False == obj.is_empty():
				result = (obj,)
	return result
# ### def load_stories

def prepare_story_id():
	""" generate IDs for stories """

	for story in _all_story:
		story.prepare_story_id()
# ### def prepare_story_id

def yamlnodedump_stories(e):
	""" dump Story object to YAML Node object
	"""
	
	if isinstance(e, Story):
		empty_node = e.is_empty()
		
		mapping = []
		
		_attach_mapping_value(mapping, u"story-id", e.story_id)
		_attach_mapping_value(mapping, u"story", e.story, empty_node, True)
		_attach_mapping_value(mapping, u"note", e.note, empty_node, True)
		_attach_mapping_value(mapping, u"order", e.imp_order, empty_node, False)
		_attach_mapping_value(mapping, u"value", e.imp_value, empty_node, False)
		_attach_mapping_value(mapping, u"point", e.point, empty_node, False)
		_attach_mapping_sequence(mapping, u"sub-story", yamlnodedump_stories(e.substory), empty_node, False)
		_attach_mapping_value(mapping, u"demo-method", e.demo_method, empty_node, True)
		_attach_mapping_sequence(mapping, u"task", yamlnodedump_tasks(e.subtask), empty_node, False)
		_attach_mapping_sequence(mapping, u"log", yamlnodedump_logs(e.logrecord), empty_node, False)
		
		return yaml.MappingNode(tag=u"tag:yaml.org,2002:map", value=mapping, flow_style=False)
	elif isinstance(e, (list, tuple,)):
		result = []
		for elem in e:
			result.append(yamlnodedump_stories(elem))
		return result
# ### def yamlnodedump_stories


def load_tasks(m):
	""" load tasks from m
	"""

	result = []

	if isinstance(m, (list, tuple,)):
		for mm in m:
			result.extend(load_tasks(mm))
	elif isinstance(m, (str, unicode,)):
		m = m.strip()
		if len(m) > 0:
			return load_tasks({"t": m})
	elif isinstance(m, dict):
		task_id = None
		task = None
		note = None
		estimated_time = None
		point = None
		status = None
		test_method = None

		sub_tasks = None
		logrecords = None

		is_accepted_any_attribute = False

		if "t-id" in m:
			task_id = str(m["t-id"])
			is_accepted_any_attribute = True
		if "t" in m:
			task = _convert_to_string(m["t"])
			is_accepted_any_attribute = True
		if "note" in m:
			note = _convert_to_string(m["note"])
			is_accepted_any_attribute = True
		if "estimated-time" in m:
			estimated_time = _convert_to_integer(m["estimated-time"])
			is_accepted_any_attribute = True
		if "point" in m:
			point = _convert_to_integer(m["point"])
			is_accepted_any_attribute = True
		if "status" in m:
			status = _convert_to_string(m["status"])
			if 'new' == status:
				status = None
			is_accepted_any_attribute = True
		if "test-method" in m:
			test_method = _convert_to_string(m["test-method"])
			is_accepted_any_attribute = True
		if "sub-task" in m:
			sub_tasks = load_tasks(m["sub-task"])
			is_accepted_any_attribute = True
		if "log" in m:
			logrecords = load_logs(m["log"])
			is_accepted_any_attribute = True

		if is_accepted_any_attribute:
			obj = Task(task_id, task, note, estimated_time, point, status, test_method)
			if sub_tasks is not None:
				obj.append_subtask(sub_tasks)
			if logrecords is not None:
				obj.append_log(logrecords)

			if False == obj.is_empty():
				result = (obj,)
	return result
# ### def load_tasks

def prepare_task_id():
	""" generate IDs for tasks """

	for task in _all_task:
		task.prepare_task_id()
# ### def prepare_task_id

def yamlnodedump_tasks(e):
	""" dump Task object to YAML Node object
	"""
	
	if isinstance(e, Task):
		empty_node = e.is_empty()
		
		mapping = []
		
		_attach_mapping_value(mapping, u"t-id", e.task_id)
		_attach_mapping_value(mapping, u"t", e.task, empty_node, True)
		_attach_mapping_value(mapping, u"note", e.note, empty_node, True)
		_attach_mapping_value(mapping, u"estimated-time", e.estimated_time, empty_node, False)
		_attach_mapping_value(mapping, u"point", e.point, empty_node, False)
		_attach_mapping_value(mapping, u"status", e.status, empty_node, False)
		_attach_mapping_sequence(mapping, u"sub-task", yamlnodedump_tasks(e.subtask), empty_node, False)
		_attach_mapping_value(mapping, u"test-method", e.test_method, empty_node, True)
		_attach_mapping_sequence(mapping, u"log", yamlnodedump_logs(e.logrecord), empty_node, False)

		return yaml.MappingNode(tag=u"tag:yaml.org,2002:map", value=mapping, flow_style=False)
	elif isinstance(e, (list, tuple,)):
		result = []
		for elem in e:
			result.append(yamlnodedump_tasks(elem))
		return result
# ### def yamlnodedump_tasks


def load_logs(m):
	""" load logs from m
	"""

	result = []

	if isinstance(m, (list, tuple,)):
		for mm in m:
			result.extend(load_logs(mm))
	elif isinstance(m, (str, unicode,)):
		m = m.strip()
		if len(m) > 0:
			return load_logs({"l": m})
	elif isinstance(m, dict):
		log_id = None
		log = None
		record_time = None
		author = None
		action = None

		is_accepted_any_attribute = False

		if "l-id" in m:
			log_id = str(m["l-id"])
			is_accepted_any_attribute = True
		if "l" in m:
			log = _convert_to_string(m["l"])
			is_accepted_any_attribute = True
		if "record-time" in m:
			record_time = _convert_to_datetime(m["record-time"])
			is_accepted_any_attribute = True
		if "author" in m:
			author = _convert_to_string(m["author"])
			is_accepted_any_attribute = True
		if "action" in m:
			action = _convert_to_string(m["action"])
			is_accepted_any_attribute = True

		if is_accepted_any_attribute:
			obj = Log(log_id, log, record_time, author, action)
			result = (obj,)
	return result
# ### def load_logs

def yamlnodedump_logs(e):
	""" dump Log object to YAML Node object
	"""
	
	if isinstance(e, Log):
		empty_node = e.is_empty()
		
		mapping = []
		
		_attach_mapping_value(mapping, u"l-id", e.log_id)
		_attach_mapping_value(mapping, u"l", e.log, empty_node, True)
		_attach_mapping_value(mapping, u"record-time", e.record_time, empty_node, False)
		_attach_mapping_value(mapping, u"author", e.author, empty_node, False)
		_attach_mapping_value(mapping, u"action", e.action, empty_node, False)

		return yaml.MappingNode(tag=u"tag:yaml.org,2002:map", value=mapping, flow_style=False)
	elif isinstance(e, (list, tuple,)):
		result = []
		for elem in e:
			result.append(yamlnodedump_logs(elem))
		return result
# ### def yamlnodedump_logs



class DevelopmentProject(StoryContainer):
	def __init__(self, product_backlog, tracked_issue):
		
		super(DevelopmentProject, self).__init__()
		
		self.product_backlog = product_backlog
		self.tracked_issue = tracked_issue
		
		self.substory = self.product_backlog
	# ### def __init__
# ### class DevelopmentProject

def load_project(c):
	""" load dp document
	"""

	product_backlog = None
	tracked_issue = None
	
	if "product-backlog" in c:
		product_backlog = load_stories(c["product-backlog"])
		
		# TODO: load issues
	else:
		product_backlog = load_stories(c)
	
	dpobj = DevelopmentProject(product_backlog, tracked_issue)
	
	prepare_story_id()
	prepare_task_id()
	
	return dpobj
# ### def load_project

def yamlnodedump_project(e):

	mapping = []
	
	if e.product_backlog is not None:
		sobj = yamlnodedump_stories(e.product_backlog)
		_attach_mapping_sequence(mapping, "product-backlog", sobj, False, False)
	if e.tracked_issue is not None:
		pass	# TODO
	
	return yaml.MappingNode(tag=u"tag:yaml.org,2002:map", value=mapping, flow_style=False)
# ### def yamlnodedump_project

def read_project(filename):
	fp = open(filename, "r")
	c = yaml.load(fp)
	return load_project(c)
# ### def read_project

def write_project(filename, proj):
	fp = open(filename, "w")
	yml = yaml.serialize(yamlnodedump_project(proj), stream=fp, encoding='utf-8', allow_unicode=True)
	print repr(yml)
	#fp.write(yml)
	fp.close()
# ### def write_project


class RuntimeConfiguration(object):
	def __init__(self, username, active_projfile, archive_projfile):
		self.username = username
		self.active_projfile = active_projfile
		self.archive_projfile = archive_projfile
	# ### def __init__
# ### class RuntimeConfiguration

def read_runtimeconfig(filename):
	fp = open(filename, "r")
	c = yaml.load(fp)
	
	username = None
	if "DP_USERNAME" in os.environ:
		username = os.environ["DP_USERNAME"]
	elif "username" in c:
		username = c["username"]
		
	active_projfile = c["dp-active"]
	archive_projfile = None
	if "dp-archive" in c:
		archive_projfile = c["dp-archive"]
	
	return RuntimeConfiguration(username, active_projfile, archive_projfile)
# ### def read_runtimeconfig



def command_noop(proj, args):
	""" respond to "rebuild", "r.b.", "rb", "r" command
	"""
	return True
# ### def command_noop

def command_add_story(proj, args):
	""" respond to "add-story", "addstory", "a.s.", "as" command
	"""
	
	add_after = None
	
	if len(args) >= 1:
		add_after = args[0]
	
	nobj = Story()
	if add_after is None:
		proj.append_substory(nobj)
	elif add_after in _every_object:
		_every_object[add_after].append_substory(nobj)
	else:
		print "ERR: parent object not found: [%r]" % (add_after,)
		return False
	
	return True
# ### def command_add_story

def command_add_task(proj, args):
	""" respond to "add-task", "addtask", "a.t.", "at" command
	"""
	
	add_after = None
	
	if len(args) >= 1:
		add_after = args[0]
	
	nobj = Task()
	if add_after is None:
		proj.append_subtask(nobj)
	elif add_after in _every_object:
		_every_object[add_after].append_subtask(nobj)
	else:
		print "ERR: parent object not found: [%r]" % (add_after,)
		return False
	
	return True
# ### def command_add_task

def command_mark_complete(proj, args):
	""" respond to "done", "complete" command
	"""
	
	add_after = None
	
	if len(args) >= 1:
		add_after = args[0]
	else:
		print "ERR: need object ID to mark done"
		return False
	
	if add_after in _every_object:
		t = _every_object[add_after]
		t.set_status("DONE")
		t.append_log(Log(log="mark task as done."))
	else:
		print "ERR: object for done is not found: [%r]" % (add_after,)
		return False
	
	return True
# ### def command_mark_complete

def do_backup_project(filename, maxbackup=9):
	for idx in range(maxbackup, 1, -1):
		tgt_filename = ".".join( (filename, str(idx)) )
		prv_filename = ".".join( (filename, str(idx-1)) )
		try:
			os.unlink(tgt_filename)
		except:
			pass
		if os.access(prv_filename, os.F_OK):
			os.rename(prv_filename, tgt_filename)
	
	tgt_filename = ".".join( (filename, "1") )
	os.rename(filename, tgt_filename)
# ### def do_backup_project


def main():
	global _rt_config
	_rt_config = read_runtimeconfig(".dprc")
	
	cmdfunc = None
	cmdargs = []
	
	for opt in sys.argv:
		if cmdfunc is not None:
			cmdargs.append(opt)
		elif opt in ("add-story", "addstory", "a.s.", "as",):
			cmdfunc = command_add_story
		elif opt in ("add-task", "addtask", "a.t.", "at",):
			cmdfunc = command_add_task
		elif opt in ("done", "complete",):
			cmdfunc = command_mark_complete
		elif opt in ("rebuild", "r.b.", "rb", "r",):
			cmdfunc = command_noop
	
	if cmdfunc is None:
		print "ERR: no command"
		sys.exit(1)

	proj = read_project(_rt_config.active_projfile)
	
	if not cmdfunc(proj, cmdargs):
		sys.exit(3)
	
	do_backup_project(_rt_config.active_projfile)
	write_project(_rt_config.active_projfile, proj)
	
	sys.exit(0)
# ### def main



if __name__ == '__main__':
	main()

# vim: ts=4 sw=4 ai nowarp
