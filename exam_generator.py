#!/usr/bin/env python
# -*- coding: utf-8 -*-

make_only_first_exam = False 
encrypt_exam         = True

import time
import string
import re
#import py7zlib
import subprocess
import os
import shelve
import shutil

from bio_info_questions import *

from exam_settings import *

import ParseStudentList

mecs, names = ParseStudentList.parse_student_file(student_list_file)

if not encrypt_exam:
    print "No encryption!"
    password_to_open_exam=""
    password_to_see_correct_exam=""
else:
    print u"password_to_open_exam = {}".format(password_to_open_exam)
    print u"password_to_see_correct_exam = {}".format(password_to_see_correct_exam)
    password_to_open_exam= u"-p{}".format(password_to_open_exam)
    password_to_see_correct_exam= u"-p{}".format(password_to_see_correct_exam)

studentlist = zip(mecs,names)

if make_only_first_exam:
    studentlist = studentlist[:1]

shelf = shelve.open(shelf_file)

if not os.path.isdir(exam_folder):
    os.makedirs(exam_folder)

for student in studentlist:
    timestamp = int(time.time())
    mec, name = student
    print "Start prep exam for",mec,name
    q=[]
    q.append( reverse_complement.question(1,50)     )
    q.append( change_origin.question(2)             )
    q.append( find_feature_rc.question(1)           )
    q.append( find_region_of_similarity.question(4) )
    q.append( find_repeated_sequences.question(4)   )
    q.append( pcr_cloning.question(8)               )
             


    empty_exam = header.format(name=name,
                               mec=mec,
                               timestamp=timestamp,
                               question_separator=question_separator,
                               number_of_questions=len(q) )
    correct_exam = empty_exam

    for index, question in enumerate(q):
        empty_exam += question_separator.format(index+1)
        correct_exam += question_separator.format(index+1)
        empty_exam += question.empty_question
        correct_exam += question.correct_answer
        shelf[question.id] = question

    empty_exam   += endseparator
    correct_exam += endseparator

    empty_exam   = re.sub("\r?\n", "\r\n", empty_exam)
    correct_exam = re.sub("\r?\n", "\r\n", correct_exam)
    
    if os.path.exists(u"/tmp/exam"):
        shutil.rmtree(u"/tmp/exam")
    
    os.makedirs(u"/tmp/exam")
    os.makedirs(u"/tmp/exam/files")
    
    #os.chdir(u"/tmp/exam")
    
    with open(u"/tmp/exam/correct_exam.txt".format(mec=mec), "w") as f:
        f.write(correct_exam.encode("latin-1"))
    
    cmd = u'7z a -tzip /tmp/exam/correct_exam_encrypted.zip /tmp/exam/correct_exam.txt {pw} '.format(pw=password_to_see_correct_exam)
    
    slask=subprocess.call(cmd, shell=True)
    
    os.remove(u"/tmp/exam/correct_exam.txt")

    for file in os.listdir(included_files_location):
        if "~" not in file and not file.startswith("."):
            shutil.copy(os.path.join(included_files_location, file),u"/tmp/exam/files/"+file)
    
    filename = u"{}_{}".format(name.replace(" ","_"),mec)

    with open(u"/tmp/exam/{filename}.txt".format(filename=filename).format(mec=mec), "w") as f:
        f.write( empty_exam.encode("latin-1"))
     
    cmd = u'7za a -tzip "{exam_folder}/{filename}.zip" /tmp/exam/ {pw} '.format(pw = password_to_open_exam,
                                                                                exam_folder = exam_folder,
                                                                                filename    = filename) 
    slask=subprocess.call(cmd, shell=True)

shelf.close()
print "Finished"
