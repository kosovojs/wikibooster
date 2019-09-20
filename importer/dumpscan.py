import re
import os
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot
from pywikibot import xmlreader
from pywikibot import textlib
from bz2 import BZ2File

class WikipediaDumpScanner:
	search = {
		'lvwiki': {
			'doubleWords': [
				{'regex':r'(\s)(([A-Za-zĀČĒĢĪĶĻŅŠŪŽāčēģīķļņšūž]{3,})(\s+\3))(\s)','flag':False}
			],
			'sekojoss': [
				{'regex':r'[Ss]ekojoš','flag':re.IGNORECASE}
			],
			'nakosais': [
				{'regex':r'(?<!(ie|iz|pa))(?<!pie)(nākoš)(?!(ā|ā misija|ā turneja|ais_p|)\s*=)','flag':re.IGNORECASE}
			]
		},
		'etwiki': {
			'doubleWords': [
				{'regex':r'(\s)(([A-Za-zŠšŽžÜüÖöÄäÕõ]{3,})(\s+\3))(\s)','flag':False}#
			]
		}
	}

	reflist = {
		'etwiki': {
			'templates': ['reflist','viited'],
			'tplns': ['template','mall'],
			'tags': ['<references']
		}
	}

	def __init__(self, wiki):
		self.wiki = wiki
		self.findings = {}
	
	def saveResultsToDatabase(self):
		addToDatabaseValues = {}
		#with open('tsting.txt', 'w', encoding='utf8') as f:
		#	f.write(str(self.findings))
		#print(self.findings)
		for task in self.findings:
			taskData = self.findings[task]
			#toAdd = [[f, self.wiki, task]
			#	for f in taskData
			#]
			addToDatabaseValues.update({task:taskData})
		#
		return addToDatabaseValues

	def parse_reflist_search(self, pagetext):


		if re.search('<ref',pagetext):

			searches = self.reflist[self.wiki]
			tpls = '|'.join(searches['templates'])
			tpls_ns = '|'.join(searches['tplns'])

			fullPattern = r'{{{{\s*(({})\s*:\s*)?({})'.format(tpls_ns,tpls)

			if not re.search(fullPattern, pagetext) and not re.search('<references', pagetext):
				return True


	def parse_findings(self,pagetext,regex,flag):
		if flag:
			positiveMatches = re.search(regex, pagetext, flag)
		else:
			positiveMatches = re.search(regex, pagetext)

		if positiveMatches:
			return True

	def scanWiki(self, fileToParse, plugins):
		counter = 0
		whatToSearch = self.search[self.wiki]
		
		reflistTaskName = 'reflist'

		with BZ2File(fileToParse) as xml_file:
			for page in xmlreader.XmlDump(fileToParse).parse():
				if page.ns == "0" and not page.isredirect:
					pagetext = textlib.unescape(page.text)
					pagetitle = page.title

					counter+=1
					#if counter == 5000: break

					if counter % 10000 ==0:
						print(counter)

					for task in whatToSearch:
						for entry in whatToSearch[task]:
							doesHaveMatch = self.parse_findings(pagetext, entry['regex'], entry['flag'])
							if doesHaveMatch:
								if task in self.findings:
									self.findings[task].append(pagetitle)
								else:
									self.findings[task] = [pagetitle]
					#
					if 'reflist' in plugins:
						doesHaveMatch = self.parse_reflist_search(pagetext)
						
						if doesHaveMatch:
							if reflistTaskName in self.findings:
								self.findings[reflistTaskName].append(pagetitle)
							else:
								self.findings[reflistTaskName] = [pagetitle]

		#
		print('scan ended')
		return self.saveResultsToDatabase()
#
