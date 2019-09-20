import re
import os, requests
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot
from pywikibot import xmlreader
from pywikibot import textlib
from bz2 import BZ2File

from dbWiki import DBWiki

import urllib.parse as urlparse


class DefaultSortSetup:
	#https://stackoverflow.com/questions/267399/how-do-you-match-only-valid-roman-numerals-with-a-regular-expression
	romans = 'M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'
	badwords = {
		'lv': [f.lower() for f in ['no','Lielais','DJ','Jaunākā','pašā','Svētais','Ibn','princese','princis','sultāne','sultāns','karalis','karaliene','vecākais','jaunākais']],
		'et': ['']
	}

	sparql = '''select ?lv_title where {{
		?item wdt:P31 wd:Q5 .
		?lv_title schema:about ?item; schema:isPartOf <https://{}.wikipedia.org/> .
	}}'''
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

	def saveResultsToDatabase(self, wikiLang):
		addToDatabaseValues = []

		taskId = {
			'lv': '1',
			'et': '8'
		}
		toAdd = [[f, self.wiki, taskId[wikiLang]]
			for f in self.findings
		]
		
		return toAdd

	def encode_if_necessary(self, b):
		if type(b) is bytes:
			return b.decode('utf8')
		return b

	def getArticles(self, wiki):
		dbConn = DBWiki()
		dbConn.connect('{}wiki'.format(wiki))
		data = dbConn.run_query("""select p.page_title
from page p
left join page_props pp on p.page_id = pp.pp_page and pp.pp_propname="defaultsort"
where p.page_namespace=0 and pp.pp_value is not null""")

		
		#with open('tsting.txt', 'w', encoding='utf8') as f:
		#	f.write(str(data))

		return data

	def scanWiki(self, wiki):
		quarry = {
			'lv':'19335',
			'et': '38386'
		}
		pagesWithDefaultsort = self.getArticles(wiki)#self.get_quarry(quarry[wiki])
		pagesWithDefaultsort = [self.encode_if_necessary(f[0]).replace('_',' ') for f in pagesWithDefaultsort]
		
		sparqlQuery = self.sparql.format(wiki)
		#print(sparqlQuery)
		peoplefromsparql = self.basic_sparql(sparqlQuery)
		peoplefromsparql = [urlparse.unquote(f['lv_title']['value'].replace('https://{}.wikipedia.org/wiki/'.format(wiki), '').replace('_', ' ')) for f in peoplefromsparql]
		
		fordb = []
		for person in peoplefromsparql:
			if person in pagesWithDefaultsort: continue
			if not self.validate_title(person): continue
			self.findings.append(person)
		#
		print('scan ended')
		return self.saveResultsToDatabase(wiki)
#
