# -*- coding: utf-8 -*-
import scrapy
import json
import re

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class DiarioDoCentroDoMundoSpider(scrapy.Spider):
    name = 'diario_do_centro_do_mundo'
    allowed_domains = ['diariodocentrodomundo.com.br']
    start_urls = []

    def __init__(self, *a, **kw):
        super(DiarioDoCentroDoMundoSpider, self).__init__(*a, **kw)
        with open('seeds/diario_do_centro_do_mundo.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        section = response.url.split("/")[-2]
        
        for href in response.css("h3.entry-title.td-module-title a::attr(href)").getall():
            
            #request url must be string
            request = scrapy.Request(href, callback = self.parse_href)
            request.meta['section'] = section
            yield request

        #for href in response.css("h3.entry-title.td-module-title a::attr(href)"):
        #    yield response.follow(href, callback = self.parse_href)
        
    def parse_href(self, response):
        for element in response.css('article'):
            yield {
                'title' : element.css("div.td-post-header.td-pb-padding-side header h1::text").get(),
                'subtitle' : "",
                'author' : element.css("div.td-post-header.td-pb-padding-side header div.td-post-author-name a::text").get(),
                'date' : self.format_date(element.css("time::attr(datetime)").get()),
                'section' : response.meta['section'],
                'text' : " ".join(element.css("div.td-post-content.td-pb-padding-side p::text").getall()[:-1]),
                'url' : response.url,
            }

    def format_date(self, string):
        splitted_date = re.split("[-T:+]+", string)
        splitted_date[0], splitted_date[2] = splitted_date[2], splitted_date[0]
        string_date = " ".join(splitted_date[:3]).replace(" ", "/") + " " + " ".join(splitted_date[3:6]).replace(" ", ":")
        
        return string_date
