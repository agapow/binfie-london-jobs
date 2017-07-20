# -*- coding: utf-8 -*-
"""
Crawls the RSS feed for New Scientist Jobs.

Details are
"""

### IMPORTS

import re

import scrapy
from w3lib.html import remove_tags

from . import utils


### CONSTANTS & DEFINES

TRACKING_RE = re.compile (r'/\?TrackID=\d+$')


### CODE ###

def convert_nsj_date (dt_str):
   """
   Convert New Scientist jobs date to our format.
   """
   return utils.convert_date_fmt_ymd (dt_str, '%d %b %Y')


class NewscijobsSpider (scrapy.Spider):
   name = "newscijobs"

   start_urls = [
      'http://jobs.newscientist.com/en-gb/jobsrss/?LocationId=325&keywords=bioinformatics&radiallocation=30&countrycode=GB'
   ]

   def start_requests (self):
      """
      Must return a iterable of requests where crawling will start.
      """
      for url in self.start_urls:
         yield scrapy.Request (url=url, callback=self.parse)

   def parse (self, response):
      def clean_match (m):
         if len (m) == 0:
            return ''
         if len (m) == 1:
            return m[0].strip()
         raise ValueError ('unexpected multiple matches %s' % m)

      res_list = response.css ('item')
      for r in res_list:
         title = r.css ('title::text').extract_first()
         desc_sal = r.css ('description::text').extract_first()
         salary, description = desc_sal.split (':', 1)
         canonical_url = r.css ('link::text').extract_first()
         canonical_url = TRACKING_RE.sub ('', canonical_url)
         pubdate = r.css ('pubDate::text').extract_first()
         date_str = pubdate.split(', ')[1]
         placed = convert_nsj_date (date_str[:-15])

         yield {
            'canonical_url': canonical_url,
            'title': title.strip(),
            'description': description.strip(),
            'institution': '',
            'salary': salary.strip(),
            'placed': placed,
            'expires': '',

         }


### END ###
