import re
import os
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot
from wiki import WikipediaAPI
from db import DB

class Defaultsort:

	#https://stackoverflow.com/questions/267399/how-do-you-match-only-valid-roman-numerals-with-a-regular-expression
	romans = 'M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'
	badwords = {
		'lvwiki': [f.lower() for f in ['no','Lielais','DJ','Jaunākā','pašā','Svētais','Ibn','princese','princis','sultāne','sultāns','karalis','karaliene','vecākais','jaunākais']],
		'etwiki': [''],
		'svwiki': ['']
	}
	
	categoriesForWiki = {
		'lvwiki': 'category|kategorija',
		'etwiki': 'category|kategooria',
		'svwiki': 'category|kategori'
	}

	defaultsortText = {
		'lvwiki': 'DEFAULTSORT',
		'etwiki': 'JÄRJESTA',
		'svwiki': 'STANDARDSORTERING'
	}

	def setData(self, wiki):
		self.wiki = wiki

		categoriesForWiki = self.categoriesForWiki[self.wiki]

		self.catregex = re.compile('(\[\[('+categoriesForWiki+')\s*:[^\n]+)', re.I)
		
	def pagenamebase(self, title):
		return re.sub('\s*(\([^\(]+)$','',title)

	def validate_title(self, title):
		article = title.replace('_',' ')
		pagenamebase = self.pagenamebase(article)
		words = pagenamebase.split(' ')
		
		if ' ' not in pagenamebase:
			return False
			
		if any([f for f in words if f.lower() in self.badwords[self.wiki]]):
			return False
			
		if any([f for f in words if re.search('^{}$'.format(self.romans),f)]):
			return False
		
		return True
	#
	def getDefaultsortFromXWiki(self, title, wiki):
		#site_orig = pywikibot.Site('lv', "wikipedia")
		#lv_page = pywikibot.Page(site_orig,title)

		en_title = WikipediaAPI.getOtherWikiArticle('lv', title)
		if not en_title:
			return None
		
		site_other = pywikibot.Site(wiki, "wikipedia")
		en_page = pywikibot.Page(site_other,en_title)
		
		#wikitext = page.get(get_redirect=True)
		#defaultsort
		enwikidef = en_page.defaultsort()#re.search('\{\{DEFAULTSORT:([^\}]+)\}\}',wikitext)
		#if enwikidef:
		#	return enwikidef.group(1)
		
		return enwikidef
		#
	def getDefaultsort(self, title):
		pagenamebase = self.pagenamebase(title)
		last = re.sub('.*\s','',pagenamebase)
		first = re.sub('\s+[^\s]+$','',pagenamebase)
		DEFAULTSORT = "{}, {}".format(last, first)
		return DEFAULTSORT
	#
	def removeDefaultsortTextFromCatsort(self, wikitext, proposedDef):
		regexForSearch = r'(\[\[('+self.categoriesForWiki[self.wiki]+')\s*:([^\|]+))\|('+proposedDef+')\]\]'
		
		return re.sub(regexForSearch,r'\1]]',wikitext, flags=re.IGNORECASE)

	def makeChanges(self, wikitext, newwikitext, proposedDef):
		categories = re.search(self.catregex,wikitext)
		
		defaultsortTextInWiki = self.defaultsortText[self.wiki]

		if not categories:
			newwikitext = newwikitext + "\n\n{{%s:%s}}" % (defaultsortTextInWiki, proposedDef)
			#print('didn\'t find cats, skipping')
			#return
		else:
			categregexres = categories.group(1)
			catanddef = "\n{{%s:%s}}\n%s" % (defaultsortTextInWiki, proposedDef, categregexres)
			newwikitext = newwikitext.replace(categregexres,catanddef)
			newwikitext = self.removeDefaultsortTextFromCatsort(newwikitext, proposedDef)


		return wikitext, newwikitext


	def addDefaultsort(self, title, wiki, proposedDef):
		site_orig = pywikibot.Site(wiki.replace('wiki',''), "wikipedia")
		page = pywikibot.Page(site_orig,title)

		if not page.exists():
			return None, None

		wikitext = page.get(get_redirect=True)

		if page.defaultsort():
			return None, None

		newwikitext = wikitext

		wikitext, newwikitext = self.makeChanges(wikitext, newwikitext, proposedDef)

		return wikitext, newwikitext
		
	#
	def getData(self, wiki, title):
		db = DB()
		self.setData(wiki)
		
		if not self.validate_title(title):
			return {'status':'noaction', 'message':'Lapas nosaukums atzīts par nederīgu vai neatbilstošu šādai darbībai'}
		
		proposedDefaultsort = self.getDefaultsort(title)
		#otherWikiDef = self.getDefaultsortFromXWiki(title,'en')

		origWikicode, newWikicode = self.addDefaultsort(title,self.wiki,proposedDefaultsort)

		return {'status':'ok', 'title':title,'defaultsort':proposedDefaultsort,'origText':origWikicode,'changedText':newWikicode}