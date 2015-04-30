#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys
import string
import time
import collections
from pyparsing import *

from ezodf import newdoc, opendoc, Sheet

now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())

print now

rmat = collections.defaultdict(dict)

grade =(Literal("question..........:").suppress() + Word(nums+"."+",").setResultsName("Q#") +
        Literal("points............:").suppress() + Word(nums+"."+",").setResultsName("points") +
        Literal("name..............:").suppress() + restOfLine.setResultsName("name") +
        Literal("mec...............:").suppress() + Word(alphanums).setResultsName("mec") +
        Literal("automatic grade(%):").suppress() + Word(nums+"."+",").setResultsName("autgrade") +
        Literal("manual grade(%)...:").suppress() + Optional(Word(nums+"."+",")).setResultsName("mangrade"))

files = [f for f in sorted(os.listdir(".")) if re.match("^question\d{3}\.txt$",f)]

question_number_list = []
name_list            = []
points               = []

  
names=[]

for file in files:
    weight=[]
    print "processing: ", file
    content = open(file,"r").read()
    for data, dataStart, dataEnd in grade.scanString(content):
        name = unicode(data["name"].strip(), "utf-8")
        mec  = data["mec"]
        if not rmat[mec]:
            rmat[mec] = [name, mec]
            names.append((name, mec))
        question_number_list.append(data["Q#"])
        weight.append(data["points"])
        if "mangrade" in data:
            rmat[mec].append(data["mangrade"].replace('.',','))
        else:
            rmat[mec].append(data["autgrade"].replace('.',','))
    points.extend(list(set(weight)))
    

doc = newdoc(doctype='ods', filename='grades_bioinformatics_{}.ods'.format(now))

doc.sheets.append(Sheet(name="grades", size=(1, 20)))

sheet = doc.sheets['grades']

def write_row(sheet, row):
    for i,v in enumerate(row):
        sheet[(sheet.nrows()-1, i)].set_value(v)
    sheet.append_rows()

headers = (['name','mec']+
           ["Q{}".format(no) for no in sorted(set(question_number_list))]+
           ['grade(0-20)'])

write_row(sheet, headers)
write_row(sheet, ["",""] + points)

from string import ascii_uppercase as letters

formula="!=20*("
for c in range(len(points)):
    formula += "${letter}$2*{letter}3+".format(letter = letters[c+2])
formula = formula.rstrip("+")
formula +=")/{} \n".format(sum([100*int(x) for x in points]))

write_row(sheet, ["Max Maximus", "a99999"] + [100]*len(points) + [formula])

    
for mec in [m for n,m in sorted(names)]:
    write_row(sheet, rmat[mec])

doc.save()
print "finished!"
