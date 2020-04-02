from .defaultsort import Defaultsort
from .infobox import Infobox
from .replacements import Replacements
from .reflist import Reflist
from .commons import MoveToCommons
from .move_to_wd import MoveToWikidata
from db import DB

class Tasks:
	def __init__(self, wiki):
		self.db = DB()
		self.wiki = wiki
		self.availableTasks = self.db.getTaskIdsForWiki(wiki)

	def getDataForTask(self, task, article):
		if task not in self.availableTasks:
			return {'status':'error','message':'Unknown task'}
		#
		taskTypeData = self.db.getTaskType(task)
		if taskTypeData == 'defaultsort':
			defaultsort = Defaultsort()
			return defaultsort.getData(self.wiki, article)
		elif taskTypeData == 'repeated':
			replacements = Replacements()
			return replacements.getData('doubleWords',self.wiki, article)
		elif taskTypeData == 'move_to_wd':
			inst = MoveToWikidata()
			return inst.getData(self.wiki, article)
		elif taskTypeData == 'typo':
			taskSubtype = self.db.getTaskSubtype(task)
			replacements = Replacements()
			return replacements.getData(taskSubtype,self.wiki, article)
		#elif task=='5':
		#	infobox = Infobox()
		#	return infobox.getData(self.wiki, article)
		elif taskTypeData == 'reflist':
			wikiLang = self.wiki.replace('wiki','')
			relist = Reflist(wikiLang)
			return relist.handleArticle(wikiLang, article)
		elif taskTypeData == 'commons':
			moveCommons = MoveToCommons()
			return moveCommons.handleFile(self.wiki, article)
		#elif task=='7':
		#	replacements = Replacements()
		#	return replacements.getData('doubleWords',self.wiki, article)
		#if task=='8':
		#	defaultsort = Defaultsort()
		#	return defaultsort.getData(self.wiki, article)
		#elif task=='10':
		#	wikiLang = self.wiki.replace('wiki','')
		#	relist = Reflist(wikiLang)
		#	return relist.handleArticle(wikiLang, article)
		else:
			return {'status':'error','message':'No result'}
		#
	#
	def runTests(self):
		replacements = Replacements()
		return replacements.testing()