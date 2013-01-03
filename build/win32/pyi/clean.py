# -*- coding: utf-8 -*-
import os, glob, shutil
exclude = [i.strip() for i in open("build-skip.dat").readlines()]

target = './dist/bin/'
if not os.path.exists(target):
	print "Nothing to clean"
	exit()
 
os.chdir(target)
	
for f in exclude:
    if os.path.isfile(f):
        print "Removing ", f
        os.remove(f)
    if os.path.isdir(f):
        print "Removing ", f
        shutil.rmtree(f)