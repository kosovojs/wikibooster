import re, sys, os
import pymysql, yaml

null = None
true = True
false = False


def getCurrentTime():
	from time import gmtime, strftime
	currTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())#'2009-01-05 22:14:39'
	return currTime


conn = pymysql.connect(db='s54062__booster_p', read_default_file=os.path.expanduser("~/replica.my.cnf"), host='tools.db.svc.eqiad.wmflabs', port=3306, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()


jsonData = eval(open('typo-data.json','r', encoding='utf-8').read())

currTime = getCurrentTime()

sqlTemplate = "insert into typo (name,search_for,replace_with,`comment`,is_regex,case_sensitive,match_whole_word,active,dont_search_dump,is_minor, wiki, addition_date, user_added) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

for row in jsonData:
	wiki = 'lvwiki'
	name= ''
	search_for = row['find'] or None
	replace_with = row['replace'] or ''
	replace_with = replace_with.replace('$1',r'\1').replace('$2',r'\2').replace('$3',r'\3')
	active = 1 if row['enabled'] else None
	minor = 1 if row['minor'] else None
	comment = row['comment'] or None
	isregex = 1 if row['isregex'] else None
	caseSensitive = 1 if row['regularexpressionoptions'] == 'None' else None

	cursor.execute(sqlTemplate, (name, search_for, replace_with, comment, isregex, caseSensitive, None, active, None, minor, wiki, currTime,'import-user'))
#
conn.commit()