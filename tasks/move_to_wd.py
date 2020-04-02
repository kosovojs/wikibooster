import re
import os
import json
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot
from wiki import WikipediaAPI
from db import DB

class MoveToWikidata:
	def pagenamebase(self, title):
		return re.sub('\s*(\([^\(]+)$','',title)

	def handleRules(self, wiki, title, validationObjects):
		db = DB()
		rules = db.getWikiRules(wiki)
		
		propertiesForReturn = []

		for rule in rules:
			rule_object = rule['rule_object']
			rule_action = json.loads(rule['rule'])
			result = json.loads(rule['result'])

			for action in rule_action:
				if rule_object == 'category':
					for category in validationObjects['categories']:
						if action['value'] in category:
							propertiesForReturn.extend(result)
							break
				if rule_object == 'template':
					for template in validationObjects['templates']:
						if action['value'] in template:
							propertiesForReturn.extend(result)
							break
				if rule_object == 'pagename':
					if action['value'] in validationObjects['title']:
						propertiesForReturn.extend(result)
						break
				if rule_object == 'pagenamebase':
					if action['value'] in validationObjects['pagenamebase']:
						propertiesForReturn.extend(result)
						break
		
		return propertiesForReturn
		
	#
	def getData(self, wiki, title):
		title = title.replace('_',' ')
		wikiLang = wiki.replace('wiki','')
		pagenamebase = self.pagenamebase(title)

		otherInfo =  WikipediaAPI.getArticleInfo(wikiLang, title)

		redirects = [f['title'] for f in otherInfo['redirects']] if 'redirects' in otherInfo else []

		coords = [otherInfo['coordinates'][0]['lat'], otherInfo['coordinates'][0]['lon']] if 'coordinates' in otherInfo else None

		categories = [f['title'] for f in otherInfo['categories']] if 'categories' in otherInfo else []

		tpls = [f['title'] for f in otherInfo['templates']] if 'templates' in otherInfo else []

		proposition = self.handleRules(wikiLang, title, {'title': title, 'pagenamebase': pagenamebase, 'categories': categories,'templates': tpls})

		return {
			'status':'ok',
			'title':title,
			'pagenamebase': pagenamebase,
			'properties': proposition,
			'info': {
				'reds': redirects,
				'coords': coords,
				'categories': categories,
				'tpls': tpls
			}
		}