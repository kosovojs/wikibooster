import re
import os
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot
from pywikibot import xmlreader
from pywikibot import textlib
from bz2 import BZ2File

class WikipediaDumpScanner:
	search = {
		'doubleWords': [
			{'regex':r'(\s)(([A-Za-zĀČĒĢĪĶĻŅŠŪŽāčēģīķļņšūž]{3,})(\s+\3))(\s)','flag':'','taskId':'2'}
		],
		'sekojoss': [
			{'regex':r'[Ss]ekojoš','flag':re.IGNORECASE,'taskId':'3'}
		],
		'nakosais': [
			{'regex':r'(?<!(ie|iz|pa))(?<!pie)(nākoš)(?!(ā|ā misija|ā turneja|ais_p|)\s*=)','flag':re.IGNORECASE,'taskId':'4'}
		]
	}
	def __init__(self, wiki):
		self.wiki = wiki
		self.findings = {}
	
	def saveResultsToDatabase(self):
		addToDatabaseValues = []
		#print(self.findings)
		for task in self.findings:
			taskData = self.findings[task]
			toAdd = [[f, self.wiki, task]
				for f in taskData
			]
			addToDatabaseValues.extend(toAdd)
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
		with BZ2File(fileToParse) as xml_file:
			for page in xmlreader.XmlDump(fileToParse).parse():
				if page.ns == "0" and not page.isredirect:
					pagetext = textlib.unescape(page.text)
					pagetitle = page.title

					counter+=1
					#if counter == 500: break

					if counter % 10000 ==0:
						print(counter)

					for task in self.search:
						if task=='doubleWords' and 'biotakso' in pagetext.lower():
							continue

						for entry in self.search[task]:
							doesHaveMatch = self.parse_findings(pagetext, entry['regex'], entry['flag'])
							if doesHaveMatch:
								if entry['taskId'] in self.findings:
									self.findings[entry['taskId']].append(pagetitle)
								else:
									self.findings[entry['taskId']] = [pagetitle]
		#
		print('scan ended')
		return self.saveResultsToDatabase()
#
