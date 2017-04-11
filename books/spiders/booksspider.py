# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from books.items import BooksItem

class book(CrawlSpider):
    name = "book"
    start_urls = ['http://www.oreilly.com.cn/index.php?func=completelist']
    url = 'http://www.oreilly.com.cn/index.php?func=completelist'

    def parse(self,response):

        #item = BooksItem()
        selector = Selector(response)
        books = selector.xpath('//a[@class="tip"]')

        for book in books:
            title = book.xpath('./text()').extract()

            id = book.xpath('./@href').extract()
            id = id[0]
            whichbook = "http://www.oreilly.com.cn/{}".format(str(id))


            yield  scrapy.Request(url=whichbook,callback=self.detail_parse,
                                     meta={"title":title})

    def detail_parse(self,response):
            item = BooksItem()
            content = []
            selector = Selector(response)
            reads = selector.xpath('//div[@id="tab1"]/div/ol/li').extract()
            for read in reads:
                 read = read.replace("<li>", "").replace("</li>", "").replace("\r", " ")
                 content.append(read)

            #content = reads.xpath('./text()').extract()

            #content = reads
            #content = reads.pop().replace("<li>", "")

            str_convert = ''.join(content)
            # print  123
            # print str_convert
            item['title'] = response.meta["title"]
            item['content'] = str_convert
            yield item







            nextLink = selector.xpath('//div[@class="plain_page"]/div/span/span/a/@href').extract()
            #第10页是最后一页，没有下一页的链接
            if nextLink:
                nextLink = nextLink[0]
                print nextLink
                yield Request(self.url + nextLink,callback=self.parse)




