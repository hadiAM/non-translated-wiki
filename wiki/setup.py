#!/usr/bin/env python3
import os
import db,dep

def run():
	

	folder_path = os.getcwd()+"/sql"

	pages_file = "enwiki-latest-page.sql"
	pages_zfile = pages_file + ".gz"
	langlinks_file = "enwiki-latest-langlinks.sql"
	langlinks_zfile = langlinks_file + ".gz"
	
	pages_path = os.getcwd()+ "/sql/" + pages_file
	pages_zpath = os.getcwd() + "/sql/" + pages_zfile
	langlinks_path = os.getcwd()+ "/sql/" + langlinks_file
	langlinks_zpath = os.getcwd() + "/sql/" + langlinks_zfile
	

	if os.path.exists( folder_path ) == False:
		dep.make_dir()



	if os.path.exists( pages_zpath ) == False and os.path.exists( pages_path ) == False:
		dep.download_file(pages_zfile)
	
	if os.path.exists( langlinks_zpath ) == False and os.path.exists( langlinks_path ) == False:
		dep.download_file(langlinks_zfile)
	
	

	conn = db.DBConnection()
	conn.creat_db()

	if conn.check_dbname("wiki") == True:
		conn.connect()

		if os.path.exists( folder_path ) == True and conn.check_table("page") == False:
			conn.db_import_table("sql/" + pages_file)

		if os.path.exists( folder_path ) == True and conn.check_table("langlinks") == False and conn.check_table("langlinks_ar") == False:
			conn.db_import_table("sql/" + langlinks_file)

		if os.path.exists( folder_path ) == True and conn.check_table("langlinks") == True and conn.check_table("langlinks_ar") == False:
			conn.db_ar_langlinks_table()
			print('successfully setuped')