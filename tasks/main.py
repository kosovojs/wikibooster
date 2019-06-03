from .defaultsort import Defaultsort
from .infobox import Infobox
from .replacements import Replacements
from db import DB

class Tasks:
	def __init__(self, wiki):
		db = DB()
		self.wiki = wiki
		self.availableTasks = db.getTaskIdsForWiki(wiki)

	def getDataForTask(self, task, article):
		if task not in self.availableTasks:
			return {'status':'error','message':'Unknown task'}
		#
		if task=='1':
			defaultsort = Defaultsort()
			return defaultsort.getData(self.wiki, article)
		elif task=='2':
			replacements = Replacements()
			return replacements.getData('doubleWords',self.wiki, article)
		elif task=='3':
			replacements = Replacements()
			return replacements.getData('sekojoss',self.wiki, article)
		elif task=='4':
			replacements = Replacements()
			return replacements.getData('nakosais',self.wiki, article)
		elif task=='5':
			infobox = Infobox()
			return infobox.getData(self.wiki, article)
		else:
			return {'status':'error','message':'No result'}
		#
	#
	def runTests(self):
		replacements = Replacements()
		return replacements.testing()