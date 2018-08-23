#!/usr/bin/env python3
import os
import requests
import math
from tqdm import tqdm

d = os.getcwd()+"/sql"


def make_dir():
	
	try:  
	    os.mkdir(d)
	except OSError:  
	    print ("Creation of the directory %s failed" % d)
	else:  
	    print ("Successfully created the directory %s " % d)


def download_file(file):

	
	print(file)
	# Streaming, so we can iterate over the response.
	r = requests.get("https://dumps.wikimedia.org/enwiki/latest/"+file, stream=True)
	
	# Total size in bytes.
	total_size = int(r.headers.get('content-length', 0)); 
	block_size = 1024
	wrote = 0 
	zfile_path = 'sql/'+file
	with open(zfile_path , 'wb') as f:
	    for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
	        wrote = wrote  + len(data)
	        f.write(data)
	if total_size != 0 and wrote != total_size:
	    print("ERROR, something went wrong")

	os.system("gunzip " + zfile_path)