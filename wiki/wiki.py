#!/usr/bin/env python3
import os
import setup
import db
import time


#do_setup = input("Do you want to do setup?")
#if do_setup == 'yes' or do_setup == 'YES' or do_setup == 'y' or do_setup == 'Y':
setup.run()







conn = db.DBConnection()
conn.connect()
conn.print_titles()
#db.cursor.execute("SELECT CAST(page_title as CHAR) FROM page inner join arlanglist ON arlanglist.ll_from != page.page_id  ")
i = 0

for x in conn.cursor:
  print(x[0])
  i = i + 1
  if i == 3:
  	break
  #time.sleep(0.2)

print(db)

#10373382
#10373382