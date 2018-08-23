#!/usr/bin/python

import os
import sys
import tqdm
import math
import requests
import mysql.connector

def download_file(filename):
	'''Downloads a wikipedia MySQL database'''
	try:
		os.mkdir(os.getcwd()+'/sql')
	except:
		pass
	URL = 'https://dumps.wikimedia.org/enwiki/latest/'
	r = requests.get(URL+filename, stream=True)
	total_size = int(r.headers.get('content-length', 0));
	block_size = 1024
	wrote = 0
	zfile_path = 'sql/'+filename
	with open(zfile_path, 'wb') as f:
		for data in tqdm.tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size), unit='KB', unit_scale=True):
			wrote = wrote+len(data)
			f.write(data)
	if total_size != 0 and wrote != total_size:
		print('[-] ERROR in download')
	os.system('gunzip '+zfile_path)

class DBConnection(object):
	'''Parses the downloaded MySQL databases'''
	global cursor
	def __init__(self):
		self.USERNAME = 'alroot'	# Defualt is root
		self.PASSWORD = ''		# Defualt is empty
		self.DBNAME = 'wiki'		# Enter any database name
		self.HOST = 'localhost'		# Defualt is localhost
		self.PORT = 3306		# Defualt is 3306
		self.cursor = 0
	def connect(self):
		self.db = mysql.connector.connect(host=self.HOST, user=self.USERNAME, passwd=self.PASSWORD, database=self.DBNAME)
		self.cursor = self.db.cursor(buffered=True)
	def creat_db(self):
		self.db = mysql.connector.connect(host=self.HOST, user=self.USERNAME, passwd=self.PASSWORD)
		self.cursor = self.db.cursor(buffered=True)
		self.cursor.execute("CREATE DATABASE IF NOT EXISTS " + self.DBNAME)
	def db_import_table(self, FILE):
		command = """mysql -u %s -p%s --host %s --port %s %s < %s""" %(self.USERNAME, self.PASSWORD,  self.HOST, self.PORT, self.DBNAME, FILE)
		os.system(command)
	def db_ar_langlinks_table(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `langlinks_ar` ( `ll_from` int(8) UNSIGNED NOT NULL DEFAULT '0',  `ll_lang` varbinary(20) NOT NULL,  `ll_title` varbinary(255) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
		self.cursor.execute("INSERT INTO `langlinks_ar`(`ll_from`, `ll_lang`, `ll_title`) SELECT * FROM langlinks WHERE ll_lang = 'ar'")
		self.cursor.execute("DROP TABLE langlink")
	def check_dbname(self, dbname):
		self.cursor.execute("SHOW DATABASES LIKE '%s'" %dbname)
		for i in self.cursor.fetchall():
			if dbname in i:
				return dbname in i
		return False
	def check_table(self,table):
		self.cursor.execute("SHOW TABLES LIKE '%s'" %table)
		for i in self.cursor.fetchall():
			if table in i:
				return table in i
		return False
	def select_titles(self):
		self.cursor.execute("SELECT CAST(page_title as CHAR) FROM page inner join langlinks_ar ON langlinks_ar.ll_from != page.page_id ")

def main():
	path = os.getcwd()+'/sql'
	p_file = 'enwiki-latest-page.sql'
	p_zfile = p_file+'.gz'
	ll_file = 'enwiki-latest-langlinks.sql'
	ll_zfile = ll_file+'.gz'
	p_path = os.getcwd()+'/sql/'+p_file
	p_zpath = os.getcwd()+'/sql/'+p_zfile
	ll_path = os.getcwd()+'/sql/'+ll_file
	ll_zpath = os.getcwd()+'/sql/'+ll_zfile
	pages = os.path.exists(p_path)
	langs = os.path.exists(ll_path)
	# Download the Wikipedia databases
	if sys.argv[1] == 'download':
		if pages == False and langs == False:
			download_file(ll_zfile)
			download_file(p_zfile)
		else:
			print('[+] Database found')
	# Parse databases
	elif sys.argv[1] == 'parse':
		conn = DBConnection()
		conn.creat_db()
		if conn.check_dbname('wiki') == True:		
			conn.connect()				# Problem seems to be here
			conn.db_import_table('sql/'+p_file)	# |
			conn.db_import_table('sql/'+ll_file)	# |
			conn.db_ar_langlinks_table()		# |
			print('[+] Setup successful')
		else:
			print('[-] Error: wiki database not created')
	# Run analysis
	elif sys.argv[1] == 'run':				# Not yet tested/optamised
		conn = DBConnection()				# |
		conn.connect()					# |
		conn.select_titles()				# |
		for x in conn.cursor:				# |
			print(x[0])				# |
	else:
		print('[-] Error in command argument')

if __name__ == '__main__':
	main()