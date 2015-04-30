#!/usr/bin/env python
# -*- coding: utf-8 -*-

student_list_file               = "alunos.txt"
shelf_file                      = "shelf.shelf"
included_files_location         = u"/home/bjorn/Dropbox/python_packages/bio_info_questions/bio_info_questions/files_to_be_included"
password_to_open_exam           = u"zyxpep93"
password_to_see_correct_exam    = u"LWQsGHefywehfLSFKG6Q3W"
exam_folder                     = "./empty_exams"
start_separator                 = u"\n=========== start of exame =====================================================\n"
question_separator              = u"\n*********** Question {} ***********\n"
endseparator                    = u"\n========== end of exame ========================================================"

header = u'''================================================================================
Genética Molecular e Bioinformática 2704N9 | Licenciatura em Bioquímica
Nome                       {name}
Número mecanográfico (mec) {mec}
Exam date                  2014-06-25|Wednesday June 25|Week 25
Unix time stamp            {timestamp}
================================================================================

Instruções para o exame:

Este exame tem {number_of_questions} questões.
Deve responder às questões dentro neste documento.
Preencha a sua resposta, substituindo os simbolos "?".

Por favor NÂO MODIFIQUE MAIS NADA no exame, será corrigido automaticamente.
em particular, não modifique ou remova o QuestionID, que serve para identificar
as respostas certas.

Instructions for completing the exam:
This exam has {number_of_questions} questions.
You shuld respond to these questions within this document.
Fill in your answers where you find the "?" symbol(s) in each question.

Please do not edit anything else, as this exam will be automatically corrected.
In particular, do NOT modify the QuestionID as this is used for identifying the
correct answer.
'''
