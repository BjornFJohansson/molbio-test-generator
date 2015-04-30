#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
cw = os.getcwd()
os.chdir("./returned_exams")

import re, sys, string, codecs, zipfile
import stat
import md5
import hashlib
from pyparsing import Word, alphanums, Literal, LineEnd, LineStart, SkipTo, Optional

filesBySize = {}

def walker(arg, dirname, fnames):
    d = os.getcwd()
    os.chdir(dirname)
    try:
        fnames.remove('Thumbs')
    except ValueError:
        pass
    for f in fnames:
        if not os.path.isfile(f):
            continue
        size = os.stat(f)[stat.ST_SIZE]
        if size < 100:
            continue
        if filesBySize.has_key(size):
            a = filesBySize[size]
        else:
            a = []
            filesBySize[size] = a
        a.append(os.path.join(dirname, f))
    os.chdir(d)

os.path.walk(".", walker, filesBySize)

print 'Finding potential dupes...'
potentialDupes = []
potentialCount = 0
trueType = type(True)
sizes = filesBySize.keys()
sizes.sort()
for k in sizes:
    inFiles = filesBySize[k]
    outFiles = []
    hashes = {}
    if len(inFiles) is 1: continue
    print 'Testing %d files of size %d...' % (len(inFiles), k)
    for fileName in inFiles:
        if not os.path.isfile(fileName):
            continue
        aFile = file(fileName, 'r')
        hasher = md5.new(aFile.read(1024))
        hashValue = hasher.digest()
        if hashes.has_key(hashValue):
            x = hashes[hashValue]
            if type(x) is not trueType:
                outFiles.append(hashes[hashValue])
                hashes[hashValue] = True
            outFiles.append(fileName)
        else:
            hashes[hashValue] = fileName
        aFile.close()
    if len(outFiles):
        potentialDupes.append(outFiles)
        potentialCount = potentialCount + len(outFiles)
del filesBySize

print 'Found %d sets of potential duplicate files...' % potentialCount
print 'Scanning for real duplicate files...'

dupes = []
for aSet in potentialDupes:
    outFiles = []
    hashes = {}
    for fileName in aSet:
        print 'Scanning file "%s"...' % fileName
        aFile = file(fileName, 'r')
        hasher = md5.new()
        while True:
            r = aFile.read(4096)
            if not len(r):
                break
            hasher.update(r)
        aFile.close()
        hashValue = hasher.digest()
        if hashes.has_key(hashValue):
            if not len(outFiles):
                outFiles.append(hashes[hashValue])
            outFiles.append(fileName)
        else:
            hashes[hashValue] = fileName
    if len(outFiles):
        dupes.append(outFiles)

i = 0
for d in dupes:
    print 'Original is %s' % d[0]
    for f in d[1:]:
        i = i + 1
        print 'Deleting %s' % f
        os.remove(f)
    print








lst =[]

for filename in sorted(os.listdir(".")):

    f, e = os.path.splitext(filename)
    if e.lower()!=".txt":
        continue

    handle = codecs.open(filename,"rb","latin_1")
    exam = handle.read()
    handle.close()

    md5 = hashlib.md5(exam.encode("latin_1")).hexdigest()

    name      = (Literal(u"Nome") +
                 SkipTo(LineEnd()).setResultsName("name"))

    id        = (Literal("(mec)") +
                 SkipTo(LineEnd()).setResultsName("mec"))

    for data,dataStart,dataEnd in name.scanString(exam):
        parsed_student_name = data["name"].strip()

    for data,dataStart,dataEnd in id.scanString(exam):
        parsed_mec  = data["mec"].strip().lower()

    mec_in_filename = re.search("[\d|A|a|e|E]\d{4,5}",filename)
    if mec_in_filename:
        mec_in_filename = mec_in_filename.group()
        if parsed_mec.upper().startswith("NA"):
            parsed_mec=mec_in_filename.lower()



    new_name = parsed_student_name.replace(" ","_")+"_"+parsed_mec+"_"+md5+".txt"

    #if unicode(filename,"utf-8") != new_name:
    if not re.search("_([a-fA-F\d]{32})\.(txt|TXT)", filename):
        print "rename",filename,
        print "to",     new_name
        lst.append((filename, new_name))


assert len(lst) == len(set([b for a,b in lst]))
if raw_input("rename {} files (y/n)?".format(len(lst)))=="y":
    for filename, newname in lst:
        os.rename(filename, newname)

else:
    print "files not renamed"
    
os.chdir(cw)