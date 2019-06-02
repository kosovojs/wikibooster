import re
import os
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import sys
sys.path.append(".")
from wiki import WikipediaAPI

class Replacements:
	availableReplacements = ['doubleWords','sekojoss','nakosais']

	replacementDict = {
		'doubleWords': [
			{'from':r'(\s)(([A-Za-zĀČĒĢĪĶĻŅŠŪŽāčēģīķļņšūž]{3,})(\s+\3))(\s)','to':r'\4\5'}
		],
		'sekojoss': [
			{'from':r'Sekojoš(aj)?','to':r'Šād'},
			{'from':r'sekojoš(aj)?','to':r'šād'},
		],
		'nakosais': [
			{'from':r'([Nn])ākoš','to':r'\1ākam'}
		]
	}

	def makeReplacements(self, inputText, replacements):
		#https://stackoverflow.com/a/7088257 - lambda
		for repl in replacements:
			inputText = re.sub(repl['from'],repl['to'],inputText)
		
		return inputText

	
	def getData(self, replacementType, wiki, title):
		if replacementType not in self.availableReplacements:
			return {'status':'error', 'message':'Unknown replacement'}

		pageText = WikipediaAPI.getPageText(wiki, title)

		if not pageText:
			return {'status':'error', 'message':'Could not get page text'}
		#
		repls = self.replacementDict[replacementType]

		newWikitext = self.makeReplacements(pageText, repls)
		
		return {'status':'ok', 'title':title,'origText':pageText,'changedText':newWikitext}

	def testing(self):
		testEntries = [
			{'task':'doubleWords','input':'foo Bar bar baz','expected':'foo Bar baz'},
			{'task':'doubleWords','input':'foo bar bar baz','expected':'foo bar baz'},
		]

		results = []
		for entry in testEntries:
			repls = self.replacementDict[entry['task']]
			newWikitext = self.makeReplacements(entry['input'], repls)

			if newWikitext==entry['expected']:
				results.append('Test {} - input: "{}" - passed'.format(entry['task'], entry['input']))
			else:
				results.append('Test {} - input: "{}" - DID NOT pass - "{}"'.format(entry['task'], entry['input'], newWikitext))
		
		return '<br>'.join(results)