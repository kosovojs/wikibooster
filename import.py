import sys
#sys.path.append(".")
from db import DB
from importer.dumpscan import WikipediaDumpScanner
from importer.defaultsort import DefaultSortSetup
from importer.reflist import ReflistSetup

class Import:

	def __init__(self, wiki, date):
		self.db = DB()
		self.wiki = wiki
		self.date = date
		#self.availableTasks = db.getTaskIdsForWiki(wiki)
	def getDumpScanLink(self):
		return '/public/dumps/public/{wiki}/{date}/{wiki}-{date}-pages-articles.xml.bz2'.format(wiki = self.wiki, date = self.date)

	def handleArticleRemoval(self, newArticles, task, subtask = None, shouldConvertFormat = False):
		taskID = self.db.getTaskID(self.wiki, task, subtask)
		currArticles = self.db.getCurrentArticlesForImport(taskID)
		if shouldConvertFormat:
			newArticles = [[f, self.wiki, taskID] for f in newArticles]
		candidateArticles = [f for f in newArticles if f[0] not in currArticles]

		return candidateArticles

	def handleDefaultsortImport(self):
		dumpscanner = DefaultSortSetup(self.wiki)
		langCode = self.wiki.replace('wiki','')
		dumpresults = dumpscanner.scanWiki(langCode)

		#for taskType in dumpresults:
		self.db.saveArticlesInDatabase(self.handleArticleRemoval(dumpresults, 'defaultsort'))
		#print(dumpresults)

	def handleReflistImport(self):
		dumpscanner = ReflistSetup(self.wiki)
		dumpresults = dumpscanner.scanWiki()
		#print(dumpresults)
		self.db.saveArticlesInDatabase(self.handleArticleRemoval(dumpresults, 'reflist'))

	def handleDumpScan(self, plugins = ['fnr']):
		dumpscanner = WikipediaDumpScanner(self.wiki)
		dumpresults = dumpscanner.scanWiki(self.getDumpScanLink(), plugins)

		taskTypeGeneral = {
			'doubleWords': {'main':'repeated','sub':None},
			'sekojoss': {'main':'typo','sub':'sekojoss'},
			'nakosais': {'main':'typo','sub':'nakosais'},
			'kimija': {'main':'typo','sub':'kimija'}
		}

		for taskType in dumpresults:
			if taskType == 'reflist':

				filtered = self.handleArticleRemoval(dumpresults[taskType], 'reflist', None, True)
				self.db.saveArticlesInDatabase(filtered)
			else:
				finalType = taskTypeGeneral[taskType]
				dataForDB = self.handleArticleRemoval(dumpresults[taskType], finalType['main'], finalType['sub'], True)
				self.db.saveArticlesInDatabase(dataForDB)

		#print(dumpresults)
		#self.db.saveArticlesInDatabase(dumpresults)

	def main_lv(self):
		self.handleDefaultsortImport()
		self.handleReflistImport()
		self.handleDumpScan(['fnr'])

	def main_et(self):
		self.handleDefaultsortImport()
		#self.handleReflistImport()
		self.handleDumpScan(['fnr','reflist'])

	def main_sv(self):
		#self.handleDefaultsortImport()
		#self.handleReflistImport()
		self.handleDumpScan(['fnr'])
#
#importObj = Import('lvwiki')
#importObj.main()

importObj = Import('lvwiki','20210420')
importObj.main_lv()

importObj = Import('etwiki','20210420')
importObj.main_et()

#importObj = Import('svwiki','20191001')
#importObj.main_sv()
