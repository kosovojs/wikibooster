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
				{'regex':r'(\s)(([A-Za-zĀČĒĢĪĶĻŅŠŪŽāčēģīķļņšūž]{3,})(\s+\3))(\s)','flag':''}
			],
			'sekojoss': [
				{'regex':r'[Ss]ekojoš','flag':re.IGNORECASE,'taskId':'3'}
			],
			'nakosais': [
				{'regex':r'(?<!(ie|iz|pa))(?<!pie)(nākoš)(?!(ā|ā misija|ā turneja|ais_p|)\s*=)','flag':re.IGNORECASE}
			]
		},
		'etwiki': {
			'doubleWords': [
				{'regex':r'(\s)(([A-Za-zŠšŽžÜüÖöÄäÕõ]{3,})(\s+\3))(\s)','flag':''}#
			]
		}
	}

	def __init__(self, wiki):
		self.wiki = wiki
		self.findings = {}
	
	def saveResultsToDatabase(self):
		addToDatabaseValues = {}
		#print(self.findings)
		for task in self.findings:
			taskData = self.findings[task]
			#toAdd = [[f, self.wiki, task]
			#	for f in taskData
			#]
			addToDatabaseValues.update({task:taskData})
		#
		return addToDatabaseValues

	def parse_findings(self,pagetext,regex,flag):
		if flag == '':
			positiveMatches = re.search(regex, pagetext)
		else:
			positiveMatches = re.search(regex, pagetext, flag)

		if positiveMatches:
			return True

	def scanWiki(self, fileToParse):
		counter = 0
		whatToSearch = self.search[self.wiki]
		with BZ2File(fileToParse) as xml_file:
			for page in xmlreader.XmlDump(fileToParse).parse():
				if page.ns == "0" and not page.isredirect:
					pagetext = textlib.unescape(page.text)
					pagetitle = page.title

					counter+=1
					#if counter == 500: break

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
		print('scan ended')
		return self.saveResultsToDatabase()
#
