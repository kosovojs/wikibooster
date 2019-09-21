#https://hackaday.com/2018/08/15/stop-using-python-2-what-you-need-to-know-about-python-3/
import re
import os, mwparserfromhell
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot
from wiki import WikipediaAPI

'''
* pielikt attēlam {{fop-latvija}}/ {{don't move to commons}} veidni
'''

class MoveToCommons:
	wikiLang = None#lv
	wiki = None#lvwiki
	fileData = {}

	sections = None
	templates = None

	fileNsForWiki = {
		'lvwiki': 'file|attēls|image'
	}

	tplNsForWiki = {
		'lvwiki': 'template|veidne'
	}

	catNsForWiki = {
		'lvwiki': 'kategorija|category'
	}

	badtemplates = {
		'lvwiki': ['filmas[_ ]plakāts']
	}

	licenceChanges = {
		'lvwiki': [
			{'from':'filmas[_ ]plakāts', 'to': '{{copyr}}', 'flags': None}
		]
	}

	licenceSections = {
		'lvwiki': ['licence','license']
	}

	descSections = {
		'lvwiki': ['kopsavilkums','apraksts']
	}

	infTemplate = {
		'lvwiki': ['information']
	}

	def parseSections(self):
		wikitext = self.fileData['desc']
		wikicode = mwparserfromhell.parse(wikitext)
		sections = wikicode.get_sections(include_lead=False,include_headings=True)

		dataForSections = {}
		
		for section in sections:
			header = section.get(0)
			title = str.strip(str(header.title)).lower()
			section.remove(header)
			dataForSections.update({title:str(section)})
		
		self.sections = dataForSections

	def getInfoTemplate(self):
		wikitext = self.fileData['desc']
		wikicode = mwparserfromhell.parse(wikitext)
		templates = wikicode.filter_templates()

		dataForTpls = {}

		for tpl in templates:
			if tpl.name.lower().strip() in self.infTemplate[self.wiki]:
				
				return tpl
		
		return None

	def getTplValueByParam(self, tpl, params):
		for par in params:
			if par in tpl:
				return tpl[par]
		
		return None

	def getSectionByHeader(self, header):
		if self.sections is None:
			self.parseSections()
		
		for candidate in header:
			if candidate.lower() in self.sections:
				return self.sections[candidate]
		
		return None
	
	def setData(self, wiki):
		self.wiki = wiki
		self.wikiLang = wiki.replace('wiki','')

		self.tplregex = re.compile('(\[\[('+self.tplNsForWiki[self.wiki]+')\s*:[^\n]+)', re.I)
		
	def makeTemplateRegex(self, parts, full = False):
		if full:
			#print('({{\s*(('+self.tplNsForWiki[self.wiki]+')\s*:\s*)?('+'|'.join(parts)+')}})')
			return re.compile('({{\s*(('+self.tplNsForWiki[self.wiki]+')\s*:\s*)?('+'|'.join(parts)+')\s*}})', re.I)

		return re.compile('({{\s*(('+self.tplNsForWiki[self.wiki]+')\s*:\s*)?('+'|'.join(parts)+'))', re.I)

	def findLicence(self):
		doesHaveLicenceSection = self.getSectionByHeader(self.licenceSections[self.wiki])
		print(doesHaveLicenceSection)
		if not doesHaveLicenceSection:
			return None
		
		return doesHaveLicenceSection

	def parseTimestamp(self, inputStr):
		return inputStr
	
	def parseDimensions(self, size, width, height):
		if width == 0:
			return '{} bytes'.format(size)
		
		return "{} × {} ({} bytes)".format(width, height,size)
	
	def parseUser(self, userhidden, user):

		if userhidden != None or user == None:
			return "<span class=\"history-deleted\">{{int:rev-deleted-user}}</span>"
			
		return "{{uv|" + user + "|"+self.wikiLang+":}}";
	
	def parseComment(self, commenthidden, comment):
		if commenthidden != None or comment == None:
			return "<span class=\"history-deleted\">{{int:rev-deleted-comment}}</span>"
		
		return "<nowiki>" + comment + "</nowiki>"
	
	def buildHistory(self):
		header = "== {{Original upload log}} =="
		domain = "{}.wikipedia".format(self.wikiLang)
		urlSafeName = self.fileData['title']
		transferredFrom = "{{transferred from|" + domain + "||}} {{original description page|" + domain + "|" + urlSafeName + "}}"
		tableHeader = "{| class=\"wikitable\"\n! {{int:filehist-datetime}} !! {{int:filehist-dimensions}} !! {{int:filehist-user}} !! {{int:filehist-comment}}"
		
		tableRows = []

		for row in self.fileData['hist']:
			timest = self.parseTimestamp(row['timestamp'])
			dimensions = self.parseDimensions(row['size'], row['width'], row['height'])
			user = self.parseUser(row['userhidden'] if 'userhidden' in row else None, row['user'])
			comment = self.parseComment(row['commenthidden'] if 'commenthidden' in row else None, row['comment'])

			tableRows.append("|-\n| {} || {} || {} || {}".format(timest, dimensions, user, comment))

		return "{}\n{}\n\n{}\n{}\n|}}".format(header, transferredFrom, tableHeader, '\n'.join(tableRows))

	def parseMetadata(self, data):
		final = {}
		for one in data:
			final.update({one['name']:one['value']})
		
		return final
	
	def setFileInfo_MOCK(self, file):
		self.fileData = {
			'title': 'File:Batman v Superman poster.jpg',
			'desc': '== Kopsavilkums ==\nFilmas plakāts ņemts no [http://www.acmefilm.com/uploads/thumbs/17336/batmanvsupermanlv-302-450.jpg acmefilm.lv] mājaslapas.\n\n== Licence ==\n{{Filmas plakāts}}',
			'hist': [
				{'timestamp': '2017-08-25T16:12:42Z', 'user': 'OskarsC', 'size': 39935, 'width': 302, 'height': 450, 'comment': '', 'url': 'https://upload.wikimedia.org/wikipedia/lv/2/20/Batman_v_Superman_poster.jpg', 'descriptionurl': 'https://lv.wikipedia.org/wiki/Att%C4%93ls:Batman_v_Superman_poster.jpg', 'descriptionshorturl': 'https://lv.wikipedia.org/w/index.php?curid=343130'},
				{'timestamp': '2017-02-02T21:30:13Z', 'user': 'Baisulis', 'size': 127227, 'width': 257, 'height': 380, 'comment': '== Kopsavilkums ==\n[[:en:File:Batman v Superman poster.jpg|File:Batman v Superman poster.jpg]]\n\n== Licence ==\n{{Filmas plakāts}}', 'url': 'https://upload.wikimedia.org/wikipedia/lv/archive/2/20/20170825161241%21Batman_v_Superman_poster.jpg', 'descriptionurl': 'https://lv.wikipedia.org/wiki/Att%C4%93ls:Batman_v_Superman_poster.jpg', 'descriptionshorturl': 'https://lv.wikipedia.org/w/index.php?curid=343130'}
			],
			'metadata': self.parseMetadata([
				{
					"name": "Make",
					"value": "Canon"
				},
				{
					"name": "Model",
					"value": "Canon PowerShot SX600 HS"
				},
				{
					"name": "Orientation",
					"value": 1
				},
				{
					"name": "XResolution",
					"value": "180/1"
				},
				{
					"name": "YResolution",
					"value": "180/1"
				},
				{
					"name": "ResolutionUnit",
					"value": 2
				},
				{
					"name": "DateTime",
					"value": "2015:06:06 17:36:00"
				},
				{
					"name": "YCbCrPositioning",
					"value": 2
				},
				{
					"name": "ExposureTime",
					"value": "1/400"
				},
				{
					"name": "FNumber",
					"value": "110/10"
				},
				{
					"name": "ISOSpeedRatings",
					"value": 200
				},
				{
					"name": "ExifVersion",
					"value": "0230"
				},
				{
					"name": "DateTimeOriginal",
					"value": "2015:06:06 17:36:00"
				},
				{
					"name": "DateTimeDigitized",
					"value": "2015:06:06 17:36:00"
				},
				{
					"name": "ComponentsConfiguration",
					"value": "\n#1\n#2\n#3\n#0"
				},
				{
					"name": "CompressedBitsPerPixel",
					"value": "3/1"
				},
				{
					"name": "ShutterSpeedValue",
					"value": "277/32"
				},
				{
					"name": "ApertureValue",
					"value": "221/32"
				},
				{
					"name": "ExposureBiasValue",
					"value": "0/3"
				},
				{
					"name": "MaxApertureValue",
					"value": "123/32"
				},
				{
					"name": "MeteringMode",
					"value": 5
				},
				{
					"name": "Flash",
					"value": 16
				},
				{
					"name": "FocalLength",
					"value": "4500/1000"
				},
				{
					"name": "FlashPixVersion",
					"value": "0100"
				},
				{
					"name": "ColorSpace",
					"value": 1
				},
				{
					"name": "FocalPlaneXResolution",
					"value": "4608000/243"
				},
				{
					"name": "FocalPlaneYResolution",
					"value": "3456000/182"
				},
				{
					"name": "FocalPlaneResolutionUnit",
					"value": 2
				},
				{
					"name": "SensingMethod",
					"value": 2
				},
				{
					"name": "FileSource",
					"value": 3
				},
				{
					"name": "CustomRendered",
					"value": 0
				},
				{
					"name": "ExposureMode",
					"value": 0
				},
				{
					"name": "WhiteBalance",
					"value": 0
				},
				{
					"name": "DigitalZoomRatio",
					"value": "4608/4608"
				},
				{
					"name": "SceneCaptureType",
					"value": 0
				},
				{
					"name": "GPSVersionID",
					"value": "0.0.3.2"
				},
				{
					"name": "Rating",
					"value": "0"
				},
				{
					"name": "MEDIAWIKI_EXIF_VERSION",
					"value": 1
				}
            ])
		}
		#self.fileData['hist'][-1]['user']
	
	def setFileInfo(self, file):
		data = WikipediaAPI.getFileInfo(self.wiki,file)

		print(data)

		self.fileData = {
			'title': file,
			'desc': data['revisions'][0]['slots']['main']['*'],
			'hist': data['imageinfo'],
			'metadata': self.parseMetadata(data['imageinfo'][0]['metadata'])
		}

		#with open('dfsfdfsdfsf.txt', 'w', encoding='utf8') as f:
		#	f.write(str(self.fileData))

		#print(self.fileData)

	#
	def validateIfOK(self):
		badTplRegex = self.makeTemplateRegex(self.badtemplates[self.wiki])
		#print(badTplRegex)

		if re.search(badTplRegex, self.fileData['desc']):
			return False
		
		return True


	def licenceReplacements(self, licenceText):
		for edit in self.licenceChanges[self.wiki]:
			if edit['flags']:
				licenceText = re.sub(self.makeTemplateRegex([edit['from']],True), edit['to'], licenceText, flags= edit['flags'])
			else:
				licenceText = re.sub(self.makeTemplateRegex([edit['from']],True), edit['to'], licenceText)

		return licenceText

	def buildLicenceSection(self):
		hasLicence = self.findLicence()

		finalLicenceText = "<!-- NO LICENCE!!! -->"

		if hasLicence:
			finalLicenceText = hasLicence
		
		finalLicenceText = self.licenceReplacements(finalLicenceText)

		return "== {{{{int:license}}}} =={}".format(finalLicenceText)

	def formatHistDate(self, date):
		# 2017-08-25T16:12:42Z
		#if re.match('^(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d)',date) and not date.startswith('0000'):
		#	return date[0:10].replace(':','-')
		
		return date
		
	def formatExitDate(self, date):
		if re.match('^\d\d\d\d:\d\d:\d\d',date) and not date.startswith('0000'):
			return date[0:10].replace(':','-')
		
		return None
		
	def buildDescSection(self):
		doesHaveDescSection = self.getSectionByHeader(self.descSections[self.wiki])

		#if not doesHaveDescSection:
		#	doesHaveDescSection = ''
		
		descTemplate = self.getInfoTemplate()

		origUploadDate = self.formatHistDate(self.fileData['hist'][-1]['timestamp']) # + noformēt

		exifDate = self.formatExitDate(self.fileData['metadata']['DateTime'])

		if descTemplate:
			descr = self.getTplValueByParam(descTemplate, ['Description'])
			date = self.getTplValueByParam(descTemplate, ['Date'])
			source = self.getTplValueByParam(descTemplate, ['Source'])
			author = self.getTplValueByParam(descTemplate, ['Author'])
			perm = self.getTplValueByParam(descTemplate, ['Permission'])
			othervers = self.getTplValueByParam(descTemplate, ['Other_versions'])
		else:
			descr = "{{{{{} |1= {} }}}}".format(self.wikiLang, doesHaveDescSection or '').replace('\n','')
			date = "{{according to EXIF data|" + exifDate + "}}" if exifDate else "{{original upload date|" + origUploadDate + "}}"
			source = "{{own work by original uploader}} <!-- change this if not own work -->"
			author = "[[:w:" + self.wikiLang + ":User:" + self.originalUploader + "|]]"
			perm = ''
			othervers = ''
			
		infoTpl = """{{{{Information
|Description    = {desc}
|Date           = {date}
|Source         = {source}
|Author         = {author}
|Permission     = {perm}
|Other_versions = {othervers}
}}}}
""".format(
			desc = descr,
			date = date,
			source = source,
			author = author,
			perm = perm,
			othervers = othervers
		)

		return "== {{int:filedesc}} ==\n"+infoTpl

	def handleFile(self, wiki, fileTitle):
		self.setData(wiki)
		self.setFileInfo(fileTitle)

		self.originalUploader = self.fileData['hist'][-1]['user']

		if not self.validateIfOK():
			return {'status':'noaction','message': 'contains bad template'}
		
		history = self.buildHistory()
		lic = self.buildLicenceSection()
		desc = self.buildDescSection()

		newDesc = "{}\n\n{}\n\n{}".format(desc, lic, history)
		
		return {'status':'ok', 'title':fileTitle,'changedText':newDesc}