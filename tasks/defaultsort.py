import re
import os
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot
from wiki import WikipediaAPI
from db import DB

class Defaultsort:

	#https://stackoverflow.com/questions/267399/how-do-you-match-only-valid-roman-numerals-with-a-regular-expression
	romans = 'M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'
	badwords = ['no','Lielais','DJ','Jaunākā','pašā','Svētais','Ibn','princese','princis','sultāne','sultāns','karalis','karaliene','vecākais','jaunākais']
	badwords = [f.lower() for f in badwords]

	catregex = re.compile('(\[\[(category|kategorija)[^\n]+)', re.I)

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
	def addDefaultsort(self, title, proposedDef):
		site_orig = pywikibot.Site('lv', "wikipedia")
		page = pywikibot.Page(site_orig,title)

		if not page.exists():
			return None, None

		wikitext = page.get(get_redirect=True)

		if page.defaultsort():
			return None, None

		newwikitext = wikitext
		
		categories = re.search(self.catregex,wikitext)
		
		if not categories:
			newwikitext = newwikitext + "\n\n{{DEFAULTSORT:%s}}" % (proposedDef)
			#print('didn\'t find cats, skipping')
			#return
		else:
			categregexres = categories.group(1)
			catanddef = "\n{{DEFAULTSORT:%s}}\n%s" % (proposedDef, categregexres)
			newwikitext = newwikitext.replace(categregexres,catanddef)


		return wikitext, newwikitext
	#
	def getData(self, wiki, title):
		db = DB()
		
		articleID = db.getArticleForTask(1,title)
		if not self.validate_title(title):
			return {'status':'noaction', 'message':'Lapas nosaukums atzīts par nederīgu vai neatbilstošu šādai darbībai','articleID':articleID}
		
		proposedDefaultsort = self.getDefaultsort(title)
		otherWikiDef = self.getDefaultsortFromXWiki(title,'en')

		origWikicode, newWikicode = self.addDefaultsort(title,proposedDefaultsort)

		return {'status':'ok', 'title':title,'defaultsort':proposedDefaultsort,'other':otherWikiDef,'origText':origWikicode,'changedText':newWikicode,'articleID':articleID}