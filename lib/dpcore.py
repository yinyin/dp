
# -*- coding: utf-8 -*-

import re
import hashlib
import base64
import datetime



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
	def __init__(self, story_id, story, note, imp_order, imp_value, point, demo_method, sort_order_key=None, *args, **kwargs):
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
	def __init__(self, task_id, task, note, estimated_time, point, status, test_method, *args, **kwargs):
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
	def __init__(self, log_id, log, record_time, author, action=None, *args, **kwargs):

		super(Log, self).__init__(*args, **kwargs)

		self.log_id = log_id
		self.log = log
		self.record_time = record_time
		self.author = author
		self.action = action
	# ### def __init__

	def __repr__(self):
		return "%s.Log(log_id=%r, log=%r, record_time=%r, author=%r, action=%r)" % (self.__module__, self.log_id, self.log, self.record_time, self.author, self.action,)
	# ### def __repr__
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
		if "sub-task" in m:
			sub_tasks = load_tasks(m["sub-task"])
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
			result = (obj,)
	return result
# ### def load_stories

def prepare_story_id():
	""" generate IDs for stories """

	for story in _all_story:
		story.prepare_story_id()
# ### def prepare_story_id


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
			result = (obj,)
	return result
# ### def load_tasks

def prepare_task_id():
	""" generate IDs for tasks """

	for task in _all_task:
		task.prepare_task_id()
# ### def prepare_task_id


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



# vim: ts=4 sw=4 ai nowarp
