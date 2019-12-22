import scrapy
from common import comunicacion_zooper as cz

class JumboActualizacionSpider(scrapy.Spider):
    name = "jumboactualizacion"

    def start_requests(self):
        print '///////////'*25
        print cz.consultar_productos_a_actualizar()
        print '//////////'*25
        urls = [
            'https://nuevo.jumbo.cl/lentejas-peladas-martini-500-g/p',
            #'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response.css('strong.skuBestPrice::text').extract_first()

        print '121'*45
        #print response.__dict__
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)