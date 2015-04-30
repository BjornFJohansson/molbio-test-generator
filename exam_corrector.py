#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import string
import collections
import codecs
import shelve
import textwrap

shelf_file       = "shelf.shelf"
exam_folder      = "./returned_exams"
uuidpat          = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

from exam_settings import endseparator

from bio_info_questions import reverse_complement
from bio_info_questions import change_origin
from bio_info_questions import find_feature_rc
from bio_info_questions import find_region_of_similarity
from bio_info_questions import find_repeated_sequences
from bio_info_questions import blunt_cloning
from bio_info_questions import pcr_primer_design

files  = sorted([f for f in sorted(os.listdir(exam_folder)) if re.search("_([a-fA-F\d]{32})\.(txt|TXT)",f)]) # all files ending with md5.txt

files = [f for f in files if not f.endswith("~")]

print "{} files out of {} in {} identified as exams".format(len(files), len(os.listdir(exam_folder)), exam_folder)

shelf  = shelve.open(shelf_file)
matrix = collections.defaultdict(list)
point_matrix = collections.defaultdict(list)

#files = [f for f in sorted(os.listdir(exam_folder)) if "60730" in f]

names=[]

for f in files:
    print f
    test = codecs.open(os.path.join(exam_folder,f),"r","latin_1").read()
    header, rest = re.split(uuidpat,test, maxsplit=1)
    rest = rest.split(endseparator)[0]
    name_from_header = re.search(u"(Name|Nome)(.*?)$",header,re.M).group(2).strip()
    mec_from_header  = re.search(u"^(Número mecanográfico \(mec\))(.*?)$",header,re.M).group(2).strip()   
    exame = list((f.group(1),f.group(2)) for f in re.finditer("({uuidpat})(.*?)(?=({uuidpat}|$))".format(uuidpat=uuidpat),test,re.DOTALL))

    names.append((name_from_header, mec_from_header,))

    for question_no, (id, answer) in enumerate(exame):
        
        if sys.argv[1:] and not str(question_no+1) in sys.argv[1:]:
            print "\tquestion {} skipped".format(question_no+1)
            continue        
        
        questionobj = shelf[str(id)]
        print "\t{} points {}".format(questionobj.__class__.__module__, questionobj.points)
        grade, comment = questionobj.correct(answer)
        point_matrix[question_no].append(questionobj.points)
        matrix[mec_from_header].append(textwrap.dedent(u'''
                {sep1}
                {correct_answer}
                {sep2}
                {students_answer}
                {sep3}
                
                automatic comments:
                {comment}
                manual comment:

                question..........: {question_no:03d}
                points............: {points}
                name..............: {name}
                mec...............: {mec}
                automatic grade(%): {grade}
                manual grade(%)...:
                {sep4}
                ''').format( question_no     = question_no+1,
                             points          = questionobj.points,
                             mec             = mec_from_header,
                             name            = name_from_header,
                             correct_answer  = questionobj.correct_answer,
                             students_answer = answer,
                             grade           = grade,
                             comment         = comment,
                             sep1            = "^"*(79-15)+" CORRECT ANSWER",
                             sep2            = "="*(79-16)+" students answer",
                             sep3            = "_"*(79-11)+" correction",
                             sep4            = "~"*79,
                             ))

lengths=[]

for key in sorted(matrix.keys()):
    lengths.append(len(matrix[key]))
lengths = list(set(lengths))

if len(lengths) != 1: # The same number of questions found in all exams!
    print lengths
    raw_input()

length = lengths.pop()

points=[]
for key in point_matrix:
    point = list(set(point_matrix[key]))
    assert len(point) == 1

for q in range(length):
    
    text = "".join([matrix[key][q] for key in [m for n,m in sorted(names)]])
    text = string.replace(text, '\r\n', '\n')
    text = string.replace(text, '\n',   '\r\n')

    codecs.open("question{0:03d}.txt".format(q+1),"w","utf-8").write(text)

shelf.close()
