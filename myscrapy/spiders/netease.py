# -*- coding: utf-8 -*-
import scrapy
from myscrapy.items import SingerItem

cats = {
        '1001': '华语男歌手', '1002': '华语女歌手', '1003': '华语组合/乐队',
        '2001': '欧美男歌手', '2002': '欧美女歌手', '2003': '欧美组合/乐队',
        '6001': '日本男歌手', '6002': '日本女歌手', '6003': '日本组合/乐队',
        '7001': '韩国男歌手', '7002': '韩国女歌手', '7003': '韩国组合/乐队',
        '4001': '其他男歌手', '4002': '其他女歌手', '4003': '其他组合/乐队'
    }
initials = [i for i in range(65, 91)]
initials.append(0)
url_patten = "http://music.163.com/discover/artist/cat?id={}&initial={}"

class NeteaseSpider(scrapy.Spider):
    name = 'netease'
    allowed_domains = ['music.163.com']
    start_urls = [url_patten.format(cat, initial) for cat in cats.keys() for initial in initials]

    def parse(self, response):
        cat_id = response.url.split('=')[1].split('&')[0]
        lis = response.xpath('//ul[@id="m-artist-box"]/li')
        for li in lis:
            singer = SingerItem()
            singer['cat'] = cats[cat_id]
            hrefs = li.xpath('p/a|a')
            if len(hrefs) == 2: 
                uid = hrefs[1].xpath('@href').extract_first().split('=')[1]
                singer['uid'] = int(uid)
            aid = hrefs[0].xpath('@href').extract_first().split('=')[1]
            name = hrefs[0].xpath('text()').extract_first()   
            singer['_id'] = int(aid)
            singer['name'] = name
            yield singer
            
