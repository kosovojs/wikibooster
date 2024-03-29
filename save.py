import re
import os
os.environ.setdefault('PYWIKIBOT2_NO_USER_CONFIG', '1')
import pywikibot
import mwapi
from db import DB

class Save:
	def __init__(self, session):
		self.session = session
		if session:
			self.csrf_token = session.get(action='query',
										meta='tokens')['query']['tokens']['csrftoken']
		else:
			self.csrf_token = ''

	def makeSummary(self,taskID, summaryDB):
		if summaryDB:
			return summaryDB + ' ([[toollabs:booster|booster]])'

		return 'edit made with [[toollabs:booster|booster]] tool'

	def doSaveAction(self, article, wikitext, task, editSummary):
		summary = self.makeSummary(task, editSummary)
		params = {'action': 'edit',
					'title':article,
					'text': wikitext,
					'summary': summary,
					#'bot': True,
					'contentmodel': 'wikitext',
					'token': self.csrf_token,
					'assert': 'user',
					'maxlag': 5,
					'formatversion': 2
		}

		try:
			params = params
			response = self.session.post(**params)
		except mwapi.errors.APIError as e:
			return {'status':'error','message':'nevarēja saglabāt'}

	def saveArticle(self, job, article, result, wikitext, savingStatus, user):
		db = DB()

		#vispirms laikam jācenšas saglabāt; ja tur ir error, tad nesaglabāt DB?
		if result == 'error':
			affectedRows = db.saveStatus(job,article,'error',user)
		elif result == 'success':
			editSummary = db.getTaskEditSummary(job)
			affectedRows = db.saveStatus(job,article,'ok',user)
			if savingStatus== 'noaction':
				print('no need to save')
			else:
				print('need to save')
				self.doSaveAction(article, wikitext, job, editSummary)
			#simply save to DB result
		#	return {'status':'ok'}
		#task_id,pageID, result, user
		if affectedRows == 1:
			return {'status':'ok','message':'saved'}

		return {'status':'info','message':'no data to save'}
