import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
from flask import render_template

import mwoauth
import requests_oauthlib
import os
import yaml
import mwapi

from tasks.main import Tasks
from save import Save
from db import DB

from typo.fix import TypoFix

app = Flask(__name__, static_folder="./frontend/build/static", template_folder="./frontend/build")
#app = Flask(__name__)
CORS(app)

user_agent = 'WikiBooster'

__dir__ = os.path.dirname(__file__)

configFile = open(os.path.join(__dir__, 'config.yaml'))
app.config.update(yaml.safe_load(configFile))

def authenticated_session(domain = 'meta.wikimedia.org'):
	if 'oauth_access_token' in flask.session:
		access_token = mwoauth.AccessToken(**flask.session['oauth_access_token'])
		auth = requests_oauthlib.OAuth1(client_key=app.config['CONSUMER_KEY'], client_secret=app.config['CONSUMER_SECRET'],
										resource_owner_key=access_token.key, resource_owner_secret=access_token.secret)
		return mwapi.Session(host='https://'+domain, auth=auth, user_agent=user_agent)
	else:
		return None

def getUserInfo(domain = 'meta.wikimedia.org'):
	session = authenticated_session(domain)

	if not session:
		return None, None, {'status':'error','message':'not logged in'}

	try:
		userinfo = session.get(action='query',
								meta='userinfo',
								uiprop=['groups', 'centralids'])['query']['userinfo']
		
		return True, session, {'status':'ok','username':userinfo['name']}
	except mwapi.errors.APIError as e:
		if e.code == 'mwoauth-invalid-authorization-invalid-user':
			# user is viewing a batch for a wiki where they do not have a local user account
			# treat as anonymous on the local wiki, but query Meta to find out if they’re a steward
			
			return None, None, {'status':'error','message':'server error'}

		else:
			raise e
			
	return None, None, {'status':'error','message':'server error'}

@app.route('/', methods=['GET'])
def index_page():
	return render_template('index.html')

#http://127.0.0.1:5000/task/lvwiki/1/Helēna Mārnija
@app.route('/task/<wiki>/<name>/<page>', methods=['GET'])
def getTaskResult(wiki,name,page):
	tasks = Tasks(wiki)

	articleInfo = tasks.getDataForTask(name,page)

	return jsonify(articleInfo)

@app.route('/testing', methods=['GET'])
def runTests():
	tasks = Tasks('lvwiki')

	articleInfo = tasks.runTests()

	return articleInfo

@app.route('/wikis', methods=['GET'])
def listWikis():
	db = DB()
	wikis = db.getAvailableWikis()
	return jsonify(wikis)

@app.route('/tasks/<wiki>', methods=['GET'])
def listJobs(wiki):
	db = DB()
	articles = db.getTasksForWiki(wiki)
	return jsonify(articles)

@app.route('/task/<wiki>/<task_id>/articles', methods=['GET'])
def listArticles(wiki,task_id):
	db = DB()
	articles = db.get_articles_for_task(wiki,task_id)
	return jsonify(articles)
#

@app.route('/typo/<wiki>', methods=['GET'])
def listTypos(wiki):
	db = DB()
	typos = db.getTyposForWiki(wiki)
	return jsonify(typos)


@app.route('/typo/articles', methods=['GET'])
def typo_list_for_wiki():
	db = DB()
	wiki = 'lvwiki'
	typos = db.get_typo_articles(wiki)
	return jsonify(typos)

@app.route('/typo/fix/<article>', methods=['GET'])
def fix_typos(article):
	db = DB()
	typoFixer = TypoFix()

	res = typoFixer.getData('lvwiki', article, db)

	return jsonify(res)

@app.route('/rules/<wiki>', methods=['GET'])
def listRules(wiki):
	db = DB()
	rules = db.getRulesForWiki(wiki)
	return jsonify(rules)

@app.route('/save', methods=['POST'])
def doSave():
	req = request.get_json()
	wiki = req['wiki']
	domain = "{}.wikipedia.org".format(wiki)
	userStatus, session, respFromGettingUserInfo = getUserInfo(domain)

	if not userStatus:
		return jsonify(respFromGettingUserInfo)
	#
	userName = respFromGettingUserInfo['username'] if 'username' in respFromGettingUserInfo else respFromGettingUserInfo['message']
	
	job = req['job']
	article = req['article']
	result = req['result']
	wikitext = req['wikitext']
	status = req['status']

	handlingSave = Save(session)
	respFromSave = handlingSave.saveArticle(job,article,result,wikitext,status,userName)

	return jsonify(respFromSave)

@app.route('/save_typo', methods=['POST'])
def doSaveTypo():
	req = request.get_json()
	wiki = req['wiki']
	domain = "{}.wikipedia.org".format(wiki.replace('wiki',''))
	userStatus, session, respFromGettingUserInfo = getUserInfo(domain)

	if not userStatus:
		return jsonify(respFromGettingUserInfo)
	
	userName = respFromGettingUserInfo['username'] if 'username' in respFromGettingUserInfo else respFromGettingUserInfo['message']
	
	active = req['active']
	case = req['case']
	comment = req['comment']
	dumpsearch = req['dumpsearch']
	minor = req['minor']
	name = req['name']
	regex = req['regex']
	replace_with = req['replace_with']
	search_for = req['search_for']
	test_cases = req['test_cases']
	whole = req['whole']
	id = req['id']
	
	db = DB()
	typoData = db.saveTypo(active,case,comment,dumpsearch,minor,name,regex,replace_with,search_for,test_cases,whole,wiki,userName,id)

	return jsonify({'status':'ok', 'info':typoData})

@app.route('/save_rule', methods=['POST'])
def saveRule():
	req = request.get_json()
	wiki = req['wiki']
	domain = "{}.wikipedia.org".format(wiki.replace('wiki',''))
	userStatus, session, respFromGettingUserInfo = getUserInfo(domain)

	if not userStatus:
		return jsonify(respFromGettingUserInfo)
	
	userName = respFromGettingUserInfo['username'] if 'username' in respFromGettingUserInfo else respFromGettingUserInfo['message']
	
	wiki = req['wiki']
	rule_name = req['rule_name']
	rule_object = req['rule_object']
	rule = req['rule']
	result = req['result']
	id = req['id']
	
	db = DB()
	db.saveRule(id, wiki, rule_name, rule_object, rule, result)

	return jsonify({'status':'ok'})

@app.route('/info', methods=['GET'])
def user_info():
	userStatus, _,respFromGettingUserInfo = getUserInfo()
	
	return jsonify(respFromGettingUserInfo)

@app.route('/login')
def login():
	consumer_token = mwoauth.ConsumerToken(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
	redirect, request_token = mwoauth.initiate('https://meta.wikimedia.org/w/index.php', consumer_token, user_agent=user_agent)
	flask.session['oauth_request_token'] = dict(zip(request_token._fields, request_token))
	return flask.redirect(redirect)

@app.route('/oauth-callback')
def oauth_callback():
	consumer_token = mwoauth.ConsumerToken(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
	request_token = mwoauth.RequestToken(**flask.session.pop('oauth_request_token'))
	access_token = mwoauth.complete('https://meta.wikimedia.org/w/index.php', consumer_token, request_token, flask.request.query_string, user_agent=user_agent)
	flask.session['oauth_access_token'] = dict(zip(access_token._fields, access_token))
	return flask.redirect(flask.url_for('index_page'))

@app.route('/logout')
def logout():
	"""Log the user out by clearing their session."""
	flask.session.clear()
	return flask.redirect(flask.url_for('index_page'))

if __name__ == '__main__':
	app.run(debug=True)