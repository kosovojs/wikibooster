import re, sys, os
import pymysql, yaml

class DB:
	conn = None
	cursor = None

	def __init__(self):
		#https://stackoverflow.com/questions/36104412/result-returned-nonetype-object-has-no-attribute-execute-during-i-make-conne
		self.port = ''
		self.host = ''
		self.user = ''
		self.password = ''
		self.database = ''
		self.isDev = False
		self.defaultFile = ''

		self.loadConfig()
		self.connectTools()

	def loadConfig(self):
		__dir__ = os.path.dirname(__file__)

		configFile = open(os.path.join(__dir__, 'db.yaml'))
		configuration = yaml.safe_load(configFile)
		#print(configuration)

		self.isDev = configuration['IS_DEV'] if 'IS_DEV' in configuration else False
		self.port = configuration['PORT'] if 'PORT' in configuration else 3306
		self.host = configuration['HOST'] if 'HOST' in configuration else 'tools.db.svc.eqiad.wmflabs'
		self.user = configuration['USER'] if 'USER' in configuration else ''
		self.password = configuration['PASSWORD'] if 'PASSWORD' in configuration else ''
		self.database = configuration['DATABASE'] if 'DATABASE' in configuration else 's53957__dev_p'
		self.defaultFile = configuration['DEFAULT_FILE'] if 'DEFAULT_FILE' in configuration else os.path.expanduser("~/replica.my.cnf")

	def connectTools(self):
		if self.isDev:
			self.conn = pymysql.connect(db=self.database, user=self.user, passwd=self.password, host=self.host, port=self.port, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
		else:
			self.conn = pymysql.connect(db=self.database, read_default_file=os.path.expanduser("~/replica.my.cnf"), host=self.host, port=self.port, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
		#
		self.cursor = self.conn.cursor()

	def getCurrentTime(self):
		from time import gmtime, strftime
		currTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())#'2009-01-05 22:14:39'
		return currTime

	def run_query(self, sql, params = ()):

		try:
			if len(params) == 0:
				self.cursor.execute(sql)
				rows = self.cursor.fetchall()
			else:
				self.cursor.execute(sql, params)
				rows = self.cursor.fetchall()
		except KeyboardInterrupt:
			#sys.exit()
			rows = []

		return rows
	#
	def get_typo_articles(self, wiki):
		sql = "SELECT distinct article from typos_2021_booster where completion_date IS NULL"
		results = self.run_query(sql)

		return [f['article'] for f in results]

	def get_typo_replacements(self):
		sql = "SELECT search_for as `from`, replace_with as `to`, match_whole_word from typo where is_active_2021=1"
		results = self.run_query(sql)

		return results

	def getWikiRules(self, wiki):
		sql = "SELECT rule_object, rule, result from rules where wiki=%s"
		results = self.run_query(sql, str(wiki))

		return results
	#
	def get_articles_for_task(self, wiki, task):
		sql = "SELECT article_name FROM article_list WHERE task=%s AND completion_date IS NULL"
		results = self.run_query(sql, str(task))
		results = [f['article_name'] for f in results]

		return results
	#
	def getCurrentArticlesForImport(self, task):
		sql = "SELECT article_name FROM article_list WHERE (completion_date IS NULL OR result='error') AND task=%s"#todo: fixme - ja rezultats nav pieejams
		# OR result<>''
		results = self.run_query(sql, str(task))
		results = [f['article_name'] for f in results]

		return results

	def getTaskID(self, wiki, taskName, subtaskName = None):
		if subtaskName:

			sql = "SELECT id FROM tasks WHERE  wiki=%s and task_type=%s and task_subtype=%s"
			results = self.run_query(sql, (wiki, taskName, subtaskName))
		else:
			sql = "SELECT id FROM tasks WHERE  wiki=%s and task_type=%s"
			results = self.run_query(sql, (wiki, taskName))

		return results[0]['id']
	#
	#šeit jāatgriež arī lapas ID
	def getNextArticleForTask(self,task_id,mode,lastID):
		sql = "SELECT article_name FROM article_list WHERE task=%s AND completion_date IS NULL and id>%d "
		#if mode == "random":
		#	sql += " ORDER BY RAND()"
		results = self.run_query(sql, (task_id,lastID))
		results = [f['article_name'] for f in results]

		return results

	def getTaskIdsForWiki(self,wiki):
		sql = "SELECT CAST(url_id as CHAR) as url_id FROM tasks where wiki=%s and active=1"
		results = self.run_query(sql, (wiki))
		if len(results)>0:
			results = [f['url_id'] for f in results]
		else:
			return []

		return results

	def getTasksForWiki(self,wiki):
		sql = "SELECT url_id, nav_title, task, description, (SELECT 1 FROM article_list WHERE task=tasks.id AND completion_date IS NULL LIMIT 1) AS hasArticles FROM tasks where wiki=%s and active=1"
		results = self.run_query(sql, (wiki))

		return results

	def getTyposForWiki(self,wiki,idFilter=False):
		if idFilter:
			sql = "SELECT id, name, search_for,replace_with, `comment`, is_regex as regex, case_sensitive AS `case`, match_whole_word as whole, is_active_2021 as active, dont_search_dump dumpsearch, is_minor as minor, test_cases FROM typo where wiki=%s and id=%s"
			results = self.run_query(sql, (wiki,idFilter))[0]
		else:
			sql = "SELECT id, name, search_for,replace_with, `comment`, is_regex as regex, case_sensitive AS `case`, match_whole_word as whole, is_active_2021 as active, dont_search_dump dumpsearch, is_minor as minor, test_cases FROM typo where wiki=%s"
			results = self.run_query(sql, (wiki))

		return results

	def getRulesForWiki(self, wiki):
		sql = "SELECT id, wiki, rule_name, rule_object, rule, result FROM rules where wiki=%s"
		results = self.run_query(sql, (wiki))

		return results

	def saveRule(self,id, wiki, rule_name, rule_object, rule, result):
		#
		if id==0:
			#currTime = self.getCurrentTime()

			sqlTemplate = "insert into rules (wiki, rule_name, rule_object, rule, result) values (%s, %s, %s, %s, %s)"
			self.cursor.execute(sqlTemplate, (wiki, rule_name, rule_object, rule, result))
			self.conn.commit()

		else:
			sqlTemplate = "update rules set wiki=%s, rule_name=%s,rule_object=%s, `rule`=%s, result=%s where id=%s"

			self.cursor.execute(sqlTemplate, (wiki, rule_name, rule_object, rule, result, id))
			self.conn.commit()

	def saveTypo(self,active,case,comment,dumpsearch,minor,name,regex,replace_with,search_for,test_cases,whole,wiki,user, id):
		#
		if id==0:
			currTime = self.getCurrentTime()

			sqlTemplate = "insert into typo (name,search_for,replace_with,`comment`,is_regex,case_sensitive,match_whole_word,is_active_2021,dont_search_dump,is_minor, wiki, addition_date, user_added) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			self.cursor.execute(sqlTemplate, (name, search_for, replace_with, comment, regex, case, whole, active, dumpsearch, minor, wiki, currTime,user))
			self.conn.commit()

			id = self.run_query('SELECT LAST_INSERT_ID() as id')[0]['id']

		else:
			sqlTemplate = "update typo set name=%s, search_for=%s,replace_with=%s, `comment`=%s, is_regex=%s, case_sensitive=%s, match_whole_word=%s, is_active_2021=%s, dont_search_dump=%s, is_minor=%s where id=%s"

			self.cursor.execute(sqlTemplate, (name, search_for, replace_with, comment, regex, case, whole, active, dumpsearch, minor, id))
			self.conn.commit()

		newTypoInfo = self.getTyposForWiki(wiki, id)
		return newTypoInfo

	def saveArticlesInDatabase(self,values):
		currTime = self.getCurrentTime()
		sqlTemplate = "insert into article_list (article_name, wiki, task, addition_date) values (%s, %s, %s, %s)"

		for entry in values:
			self.cursor.execute(sqlTemplate, (entry[0],entry[1],entry[2],currTime))
		self.conn.commit()

	def getArticleForTask(self,task_id,title):
		sql = "SELECT id FROM article_list WHERE task=%s AND article_name=%s"
		results = self.run_query(sql, (task_id,title))
		if len(results)>0:
			results = [f['id'] for f in results][0]
		else:
			return 0

		return results

	def saveStatus(self,task_id,pageTitle, result, user):
		currTime = self.getCurrentTime()

		sql = "update article_list set completion_date=%s, result=%s, user=%s where article_name=%s and task=%s and completion_date IS NULL"

		affected_rows = self.cursor.execute(sql, (currTime, result, user, pageTitle, task_id))
		self.conn.commit()

		return affected_rows

	def getAvailableWikis(self):
		sql = "SELECT distinct wiki FROM tasks where active=1 ORDER BY wiki"
		results = self.run_query(sql, ())

		return [f['wiki'] for f in results]

	def getTaskEditSummary(self, task):
		sql = "SELECT edit_summary FROM tasks WHERE id=%s"
		results = self.run_query(sql, str(task))

		return results[0]['edit_summary']

	def getTaskType(self, task):
		sql = "SELECT task_type FROM tasks WHERE id=%s"
		results = self.run_query(sql, str(task))

		return results[0]['task_type']

	def getTaskSubtype(self, task):
		sql = "SELECT task_subtype FROM tasks WHERE id=%s"
		results = self.run_query(sql, str(task))

		return results[0]['task_subtype']
