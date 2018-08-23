#!/usr/bin/env python3
from os import system
import mysql.connector 

	
class DBConnection(object):

	global cursor

	def __init__(self):
		self.USERNAME = "root" #defualt is "root"
		self.PASSWORD = "" # defualt is empty "" 
		self.DBNAME = "wiki" 
		self.HOST = "localhost" #defualt is localhost
		self.PORT = 0 #defualt is 3306
		self.cursor = 0


		
	def connect(self):
		self.db = mysql.connector.connect( host=self.HOST, user=self.USERNAME, passwd=self.PASSWORD, database=self.DBNAME)
		self.cursor = self.db.cursor(buffered=True)
	
	def creat_db(self):
		self.db = mysql.connector.connect( host=self.HOST, user=self.USERNAME, passwd=self.PASSWORD)
		self.cursor = self.db.cursor(buffered=True)
		self.cursor.execute("CREATE DATABASE IF NOT EXISTS " + self.DBNAME)
	
	def db_import_table(self,FILE):
		command = """mysql -u %s -p%s --host %s --port %s %s < %s""" %(self.USERNAME, self.PASSWORD,  self.HOST, self.PORT, self.DBNAME, FILE)
		system(command)
	
	
	def db_ar_langlinks_table(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS `langlinks_ar` ( `ll_from` int(8) UNSIGNED NOT NULL DEFAULT '0',  `ll_lang` varbinary(20) NOT NULL,  `ll_title` varbinary(255) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
	
		self.cursor.execute("INSERT INTO `langlinks_ar`(`ll_from`, `ll_lang`, `ll_title`) SELECT * FROM langlinks WHERE ll_lang = 'ar'")
	
		self.cursor.execute("DROP TABLE langlinks")
	
	
	
	def check_dbname(self,dbname):
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
		self.cursor.execute("SELECT CAST(page_title as CHAR) FROM page inner join langlinks_ar ON langlinks_ar.ll_from != page.page_id  ")