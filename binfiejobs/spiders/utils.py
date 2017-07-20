"""
Various shared utilities for spiders
"""

### IMPORTS

from datetime import datetime


### CONSTANTS & DEFINES

### CODE ###

def convert_date_fmt (dt_str, in_fmt, out_fmt):
   """
   Convert date string from one format to another.
   """
   dt = datetime.strptime (dt_str, in_fmt)
   return datetime.strftime (dt, out_fmt)


def convert_date_fmt_ymd (in_date, in_fmt):
   """
   Convert date string to Y-M-D format.
   """
   return convert_date_fmt (in_date, in_fmt, '%Y-%m-%d')

ALLOWED_LOCNS = [
   'London',
   'Sanger Institute',
   'WTSI',
   'University of Surrey',
   'Guilford',
   'Croydon',
]

def mentions_london (txt):
   """
   Does the text show that this is about London?
   """
   for locn in ALLOWED_LOCNS:
      if locn in txt:
         return True
   return False


### END ###
