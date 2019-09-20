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
			'nakosais': {'main':'typo','sub':'nakosais'}
		}

		for taskType in dumpresults:
			if taskType == 'reflist':
				self.db.saveArticlesInDatabase(self.handleArticleRemoval(dumpresults[taskType], 'reflist'))
			else:
				finalType = taskTypeGeneral[taskType]
				dataForDB = self.handleArticleRemoval(dumpresults[taskType], finalType['main'], finalType['sub'], True)
				self.db.saveArticlesInDatabase(dataForDB)
			
		#print(dumpresults)
		#self.db.saveArticlesInDatabase(dumpresults)

	def main(self):
		#self.handleDefaultsortImport()
		#self.handleReflistImport()
		self.handleDumpScan(['fnr','reflist'])
#
#importObj = Import('lvwiki')
#importObj.main()
importObj = Import('etwiki','20190801')
importObj.main()