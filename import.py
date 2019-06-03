import sys
#sys.path.append(".")
from db import DB
from importer.dumpscan import WikipediaDumpScanner
from importer.defaultsort import DefaultSortSetup
from importer.reflist import ReflistSetup

class Import:
	
	def __init__(self, wiki):
		self.db = DB()
		self.wiki = wiki
		#self.availableTasks = db.getTaskIdsForWiki(wiki)

	def handleDefaultsortImport(self):
		dumpscanner = DefaultSortSetup(self.wiki)
		dumpresults = dumpscanner.scanWiki()
		#print(dumpresults)
		self.db.saveArticlesInDatabase(dumpresults)

	def handleReflistImport(self):
		dumpscanner = ReflistSetup(self.wiki)
		dumpresults = dumpscanner.scanWiki()
		#print(dumpresults)
		self.db.saveArticlesInDatabase(dumpresults)

	def handleDumpScan(self):
		dumpscanner = WikipediaDumpScanner(self.wiki)
		dumpresults = dumpscanner.scanWiki('lvwiki-20190520-pages-articles.xml.bz2')
		#print(dumpresults)
		self.db.saveArticlesInDatabase(dumpresults)

	def main(self):
		#self.handleDumpScan()
		#self.handleDefaultsortImport()
		self.handleReflistImport()
#
importObj = Import('lvwiki')
importObj.main()
