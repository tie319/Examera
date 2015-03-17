# coding: utf8
from datetime import datetime
import re
import unittest


db.define_table('classes',
    Field('c_id', 'integer'),
    Field('name'),
    Field('info'),
    Field('start_date', 'date'),
    Field('end_date', 'date'),
    Field('teachers', 'list:string'),
    Field('students', 'list:string'),
    Field('test_ids', 'list:integer'),
    Field('test_names', 'list:string'),
    Field('class_avg', 'double'),
    Field('grades', 'blob')
    )

db.define_table('tests',
                Field('creator', 'string'),
                Field('name', 'string'),
                Field('test_data', 'blob')
                )

db.define_table('test_submissions',
                Field('test_taker', 'string'),
                Field('class_id', 'string'),
                Field('test_id', 'string'),
                Field('answers', 'list:string'),
                Field('grade', 'float'),
)
