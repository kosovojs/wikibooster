import re
import os, requests
from bs4 import BeautifulSoup

class ReflistSetup:
	url = 'http://tools.wmflabs.org/checkwiki/cgi-bin/checkwiki.cgi?project={}&view=bots&id=3&offset=0'
	taskId = {
		'lvwiki': '6',
		'svwiki': '11'
	}
	
	def __init__(self, wiki):
		self.wiki = wiki
		self.findings = []

	def pagenamebase(self, title):
		return re.sub('\s*(\([^\(]+)$','',title)

	def scanWiki(self):
		page2=requests.get(self.url.format(self.wiki))
		page2.encoding = 'utf-8'
		soup = BeautifulSoup(page2.text, "html.parser")
		list = soup.findAll('pre')
		output = list[0]
		output = str(output)
		output = re.sub('<pre>\n','',output)
		output = re.sub('\n</pre>','',output).splitlines()
		#
		
		dataForDatabase = [[f, self.wiki, self.taskId[self.wiki]]
			for f in output
		]
		return dataForDatabase
#