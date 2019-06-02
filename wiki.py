import requests
import os
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot

#https://stackoverflow.com/questions/30556857/creating-a-static-class-with-no-instances
#pārbaudīt, vai šis normāli strādā, ja izsauc vairākas reizes un dažādas metodes
class WikipediaAPI(object):
	@staticmethod
	def getPageText(wiki, page):
		wiki = wiki.replace('wiki','')#lvwiki -> lv
		site_orig = pywikibot.Site(wiki, "wikipedia")
		page = pywikibot.Page(site_orig,page)

		if not page.exists():
			return None

		lvwikitext = page.get(get_redirect=True)

		return lvwikitext

		'''
		request = requests.get("https://{}.wikipedia.org/w/api.php".format(wiki), params={
			"action": "query",
			"format": "json",
			"prop": "revisions",
			"titles": page,
			"redirects": 1,
			"rvprop": "content",
			"rvslots": "*"
		})
		'''
	@staticmethod
	def getOtherWikiArticle(wiki, page):
		request = requests.get("https://{}.wikipedia.org/w/api.php".format(wiki), params={
			"action": "query",
			"format": "json",
			"prop": "langlinks",
			"titles": page,
			"redirects": 1,
			"lllang": "en"
		})
		resp = request.json()
		itemlist = resp['query']['pages'].keys()
		for key in itemlist:
			res = resp['query']['pages'][key]['langlinks'][0]['*'] if 'langlinks' in resp['query']['pages'][key] else None
			return res
		
		return None
#action='query', prop='langlinks',lllang='en', titles=article