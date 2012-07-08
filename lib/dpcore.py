
# -*- coding: utf-8 -*-


class Story(object):
	def __init__(self, story_id, story, note, imp_order, imp_value, point, demo_method):
		self.story_id = story_id
		self.story = story
		self.note = note
		self.imp_order = imp_order
		self.imp_value = imp_value
		self.point = point
		self.demo_method = demo_method
	# ### def __init__
# ### class Story


def _convert_to_string(v):
	try:
		v = unicode(v).strip()
		if 0 == len(v):
			v = None
	except Exception as e:
		v = None
	
	return v
# ### def _convert_to_string

def load_stories(m):
	""" load stories from m
	"""
	
	result = []
	
	if isinstance(m, (list, tuple,)):
		for mm in m:
			result.extend(load_stories(mm))
	elif isinstance(m, (str, unicode,)):
		pass
		# TODO
	elif isinstance(m, dict):
		story_id = None
		story = None
		note = None
		imp_order = None
		imp_value = None
		point = None
		demo_method = None
		
		if "story-id" in m:
			story_id = str(m["story-id"])
		if "story" in m:
			story = _convert_to_string(m["story"])
		if "note" in m:
			note = _convert_to_string(m["note"])
		# TODO
		
	return result
# ### def load_stories
