import scrapy

from sulekha_scraper.items import YellowPagesItem


class JustDial(scrapy.Spider):
    name = 'yellowpages'
    allowed_domains = ['yellowpages.sulekha.com']
    start_urls = ['http://yellowpages.sulekha.com']

    def parse(self, response):
        for href in response.xpath('//div[@class="subtab-nav"]//li/a/@href'):
            extracted_addr = href.extract()
            if extracted_addr.startswith('/'):
                complete_url = response.urljoin(extracted_addr)
                print "Generating URL............................", complete_url
                yield scrapy.Request(complete_url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        print "<-------------Starting to Yield Items-------------------------->"
        for sel in response.xpath('//div[@id="listingtabcontent"]//ol//li'):
            item = YellowPagesItem()
            item['name'] = sel.xpath('h3/a/@title').extract()[0]
            item['phone_no'] = sel.xpath('.//div[@class="item-info"]/b/text()').extract()[0]
            item['address'] = sel.xpath('.//address//span/text()').extract()[0]
            item['title'] = response.xpath('/html/head/title/text()').extract()[0]
            print item
            yield item
        print "<-----------------Yielding items End----------------------------->"
        next_page = response.xpath('//li[@class="next"]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            print "<---------------Going to Next Page------------------------------>", url
            yield scrapy.Request(url, callback=self.parse_dir_contents)
