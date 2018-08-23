#!/usr/bin/env python3
import os
import setup
import db
import time


setup.run()


conn = db.DBConnection()
conn.connect()
conn.print_titles()

for x in conn.cursor:
  print(x[0])
  #time.sleep(0.2)