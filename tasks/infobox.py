import re
import os
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot, requests
from pywikibot import textlib, pagegenerators
import sys
sys.path.append(".")
from wiki import WikipediaAPI
#from db import DB

class Infobox:
	fileregex = "\[\[\s*(?:file|attēls|image)\s*:([^]|]*)"
	order = [
			{'name':'name'},
			{'name':'native_name'},
			{'name':'settlement_type'},
			{'name':'image_skyline'},
			{'name':'image_caption'},
			{'name':'image_flag'},
			{'name':'image_seal'},
			{'name':'image_shield'},
			{'name':'pushpin_map','default':''},
			{'name':'coordinates'},
			{'name':'subdivision_type','default':'Valsts'},
			{'name':'subdivision_name','default':''},
			
			{'name':'area_footnotes'},
			{'name':'area_total_km2'},
			{'name':'population_total'},
			{'name':'population_as_of'},
			{'name':'population_footnotes'},
			{'name':'population_density_km2','default':'auto'},
			{'name':'website'},
	]

	def get_infobox_params(self, tplnames,pagetext):
		infobox = {}
		#pywikibot.output(tplnames)
		counter = 0
		for template, fielddict in textlib.extract_templates_and_params(pagetext, remove_disabled_parts=False, strip=True):
			#pywikibot.output(template)
			tplname = template.lower().strip().replace('_',' ')
			#pywikibot.output(tplname)
			counter += 1
			if counter == 50:
				break
			if tplname in tplnames:
				pywikibot.output(tplname)
				infobox = {f[0]:f[1].strip() for f in fielddict.items() if f[1].strip()!=''}
				#fileobj.write(str(thisrow))
				#if len(parsed) % 25 == 0:
				#	print(len(parsed))
				#pywikibot.output(infobox)
				break
		
		return infobox
		
	def get_value(self, mas,keys,formatter = None):
		#pywikibot.output(mas)
		#pywikibot.output(key)
		

		if type(keys) is not list:
			keys = [keys]
		
		for key in keys:
			value = mas[key] if key in mas else None
			
			if value and key in ['locator_map','flag_image','arms_image']:
				if '[' in value:#tas ir kā links, tātad jāizgūst pats attēls
					filename = re.search(self.fileregex,value,flags=re.I)
					if filename:
						value = filename.group(1)
			
			if value and formatter:
				value = formatter
			
			if value:
				return value
		
		return ''
	
	def getTextFromXWiki(self, title, wiki):
		#site_orig = pywikibot.Site('lv', "wikipedia")
		#lv_page = pywikibot.Page(site_orig,title)

		en_title = WikipediaAPI.getOtherWikiArticle('lv', title)
		if not en_title:
			return None, None
		
		site_other = pywikibot.Site(wiki, "wikipedia")
		en_page = pywikibot.Page(site_other,en_title)
		
		wikitext = en_page.get(get_redirect=True)
		
		return wikitext, en_title
	
	def formatEnWiki(self, parsedInfobox):
		infoboxParts = []

		for key in parsedInfobox:
			infoboxParts.append([key, parsedInfobox[key]])
		
		longestparamname = max([len(f[0]) for f in infoboxParts])
		
		#print(longestparamname)
		
		formattedparams = [" | {}{} = {}".format(' '*(longestparamname-len(f[0])),f[0],f[1]) for f in infoboxParts]
		
		new_infobox = "{{Infobox settlement\n"+'\n'.join(formattedparams)+'\n}}'
		
		#pywikibot.output(new_infobox)
		
		return new_infobox
	
	
	def make_infobox(self,newdata):
		beigas = []
		
		for item in self.order:
			paramname = item['name']
			defaultval = item['default'] if 'default' in item else None
			
			if paramname in newdata and newdata[paramname]:
				beigas.append([paramname,newdata[paramname]])
			elif defaultval or defaultval=='':
				beigas.append([paramname,defaultval])

		longestparamname = max([len(f[0]) for f in beigas])
		
		#print(longestparamname)
		
		formattedparams = [" | {}{} = {}".format(' '*(longestparamname-len(f[0])),f[0],f[1]) for f in beigas]
		
		new_infobox = "{{Apdzīvotas vietas infokaste\n"+'\n'.join(formattedparams)+'\n}}'
		
		#pywikibot.output(new_infobox)
		
		return new_infobox
	
	#http://petscan.wmflabs.org/?psid=9467800
	def makeInfobox(self, lvtitle):
		site_orig = pywikibot.Site('lv', "wikipedia")
		page = pywikibot.Page(site_orig,lvtitle)

		if not page.exists():
			return None, None

		enwikitext, entitle = self.getTextFromXWiki(lvtitle,'en')

		lvwikitext = page.get(get_redirect=True)

		
		parsed_en = self.get_infobox_params(['infobox settlement'],enwikitext)

		enFormatted = self.formatEnWiki(parsed_en)

		entitle= self.get_value(parsed_en,'name')

		enformatted = self.get_value(parsed_en,'name')#,lambda x: "''{}''".format(x)
		if enformatted:
			enformatted = "''{}''".format(enformatted)

		area = self.get_value(parsed_en,'area_total_km2')
		population = self.get_value(parsed_en,['population_est','population_total'])

		if area!='':
			area = area.replace(',','.')
		if population!='':
			population = population.replace(',','')
		#koords vajag
		newdata = {
			'name':lvtitle,
			'native_name' : enformatted,
			'area_total_km2' : area,
			'coordinates' : self.get_value(parsed_en,'coordinates'),
			'website' : self.get_value(parsed_en,'website'),
			'population_total' : population,
			'pop_est_as_of' : self.get_value(parsed_en,'pop_est_as_of'),
			'image_flag' : self.get_value(parsed_en,'image_flag'),
			'motto' : self.get_value(parsed_en,'motto'),
			'image_shield' : self.get_value(parsed_en,'image_shield'),
			'image_skyline' : self.get_value(parsed_en,'image_skyline'),
			'pushpin_map' : self.get_value(parsed_en,'pushpin_map'),
			'subdivision_name' : self.get_value(parsed_en,'subdivision_name'),
		}

		proposedChanges = self.make_infobox(newdata)
		
		return lvwikitext, proposedChanges, enFormatted
	#
	def getData(self, title):
		origWikicode, newWikicode, enFormatted = self.makeInfobox(title)
		#return (newWikicode, enFormatted)
		#status, origText, changedText, articleID
		return {'status':'ok', 'title':title,'origText':origWikicode,'changedText':newWikicode,'enFormatted':enFormatted}
#
#obj = Infokaste()
#res, enw = obj.getData('Medana')
#print(res)