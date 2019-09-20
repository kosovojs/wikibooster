import re, sys, os
import pymysql, yaml

class DBWiki:
	conn = None
	cursor = None

	# def __init__(self):
		
		#self.connect()
		
	def connect(self, dbname, cluster='web', **kwargs):

		assert cluster in ['tools', 'analytics', 'labsdb', 'web']

		if cluster == 'labsdb':
			domain = 'labsdb'
		else:
			domain = '{}.db.svc.eqiad.wmflabs'.format(cluster)

		if dbname.endswith('_p'):
			dbname = dbname[:-2]

		if dbname == 'meta':
			host = 's7.{}'.format(domain)
		else:
			host = '{}.{}'.format(dbname, domain)
		host = kwargs.pop('host', host)

		self.conn = pymysql.connect(
			database=dbname + '_p',
			host=host,
			read_default_file=os.path.expanduser("~/replica.my.cnf"),
			charset='utf8mb4',
			**kwargs
		)

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