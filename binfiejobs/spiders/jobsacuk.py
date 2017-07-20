# -*- coding: utf-8 -*-
"""
Various shared utilities for spiders
"""

### IMPORTS

import scrapy
from w3lib.html import remove_tags

from . import utils


### CONSTANTS & DEFINES

### CODE ###

def convert_jac_date (dt_str):
   """
   Convert jobsacuk date to our format.
   """
   return utils.convert_date_fmt_ymd (dt_str, '%d-%m-%Y')


class JobsacukSpider (scrapy.Spider):
   name = "jobsacuk"
   allowed_domains = ["http://www.jobs.ac.uk/search/?keywords=bioinformatics"]
   start_urls = [
      'http://www.jobs.ac.uk/search/?keywords=bioinformatics&sort=re&show=300&s=1'
      'http://www.jobs.ac.uk/search/?keywords=genomics&sort=re&show=300&s=1'
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

      res_list = response.css ('div.result')
      for r in res_list:
         res_text = r.css ('div.text')
         if not utils.mentions_london (res_text.extract_first()):
            continue

         link_title = res_text.css ('a')
         url = "http://www.jobs.ac.uk" + clean_match ( link_title.xpath('@href').extract())
         title = clean_match (link_title.css('::text').extract())

         dept = clean_match (res_text.css
            ('div.department::text').extract())
         employer = clean_match (res_text.css
            ('div.employer::text').extract())
         placed = clean_match (res_text.re (r'placed\s+(\S+)<br'))
         expires = clean_match (res_text.re (r'exp\s+(\S+)<br'))

         info = res_text.css ('div.info')
         salary = info.re (r'Salary:\s*</strong>\s*([^<]+)<')
         if salary:
            salary = salary[0].strip()
            if salary[-1] == '.':
               salary = salary[:-1]

         yield {
            'canonical_url': url,
            'title': title,
            'institution': "%s (%s)" % (employer, dept) if dept else employer,
            'salary': salary,
            'placed': convert_jac_date (placed) if placed else '',
            'expires': convert_jac_date (expires) if expires else '',
            'description': '',

         }


### END ###
