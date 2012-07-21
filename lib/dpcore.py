
# -*- coding: utf-8 -*-

import hashlib
import base64



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



_every_object = {}


class Story(IdentifiableObject):
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


class Task(IdentifiableObject):
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

		if is_accepted_any_attribute:
			obj = Story(story_id, story, note, imp_order, imp_value, point, demo_method, sort_order_key)
			result = (obj,)
	return result
# ### def load_stories


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

		if is_accepted_any_attribute:
			obj = Task(task_id, task, note, estimated_time, point, status, test_method)
			result = (obj,)
	return result
# ### def load_tasks


