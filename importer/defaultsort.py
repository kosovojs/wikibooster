import re
import os, requests
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot
from pywikibot import xmlreader
from pywikibot import textlib
from bz2 import BZ2File

import urllib.parse as urlparse


class DefaultSortSetup:
	#https://stackoverflow.com/questions/267399/how-do-you-match-only-valid-roman-numerals-with-a-regular-expression
	romans = 'M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'
	badwords = ['no','Lielais','DJ','Jaunākā','pašā','Svētais','Ibn','princese','princis','sultāne','sultāns','karalis','karaliene','vecākais','jaunākais']
	badwords = [f.lower() for f in badwords]

	sparql = '''select ?lv_title where {
		?item wdt:P31 wd:Q5 .
		?lv_title schema:about ?item; schema:isPartOf <https://lv.wikipedia.org/> .
	}'''
	def __init__(self, wiki):
		self.wiki = wiki
		self.findings = []
	

	def pagenamebase(self, title):
		return re.sub('\s*(\([^\(]+)$','',title)

	def validate_title(self, title):
		article = title.replace('_',' ')
		pagenamebase = self.pagenamebase(article)
		words = pagenamebase.split(' ')
		
		if ' ' not in pagenamebase:
			return False
			
		if any([f for f in words if f.lower() in self.badwords]):
			return False
			
		if any([f for f in words if re.search('^{}$'.format(self.romans),f)]):
			return False
		
		return True
	#
	def basic_sparql(self,query):
		payload = {
			'query': query,
			'format': 'json'
		}

		r = requests.get('https://query.wikidata.org/bigdata/namespace/wdq/sparql?', params=payload)
		r.encoding = 'utf-8'
		json_data = eval(r.text)
		
		return json_data['results']['bindings']
		
	def get_quarry(self,page_id,listing='0'):
		null = ''
		url = 'https://quarry.wmflabs.org/query/{}/result/latest/{}/json'.format(page_id,listing)
		res = requests.get(url)
		data = eval(res.text)
		
		return data["rows"]

	def saveResultsToDatabase(self):
		addToDatabaseValues = []

		toAdd = [[f, self.wiki, '1']
			for f in self.findings
		]
		
		return toAdd

	def scanWiki(self):
		pagesWithDefaultsort = self.get_quarry('19335')
		pagesWithDefaultsort = [f[0].replace('_',' ') for f in pagesWithDefaultsort]
		
		peoplefromsparql = self.basic_sparql(self.sparql)
		peoplefromsparql = [urlparse.unquote(f['lv_title']['value'].replace('https://lv.wikipedia.org/wiki/', '').replace('_', ' ')) for f in peoplefromsparql]
		
		fordb = []
		for person in peoplefromsparql:
			if person in pagesWithDefaultsort: continue
			if not self.validate_title(person): continue
			self.findings.append(person)
			
		#
		print('scan ended')
		return self.saveResultsToDatabase()
#
