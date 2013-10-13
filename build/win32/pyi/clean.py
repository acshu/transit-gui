# -*- coding: utf-8 -*-
import os, shutil

exclude = [i.strip() for i in open("build-skip.dat").readlines()]

target = './dist/bin/'
if not os.path.exists(target):
    print "Nothing to clean"
    exit()

#for filename in os.listdir(target):
#    if filename.endswith('27.dll'):
#        os.rename(os.path.join(target, filename), os.path.join(target, filename.replace('27.dll', '.dll', 1)))
#
#exit()

os.chdir(target)

for f in exclude:
    if os.path.isfile(f):
        print "Removing ", f
        os.remove(f)
    if os.path.isdir(f):
        print "Removing ", f
        shutil.rmtree(f)
