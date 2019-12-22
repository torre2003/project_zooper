import scrapy
from common import comunicacion_zooper as cz

class TelemercadoURLSpider(scrapy.Spider):
    name = "telemercadourl"
    data_urls = None
    def start_requests(self):
        self.data_urls = cz.consultar_productos_custom(supermercado='telemercado', opcion='urls_update')
        print self.data_urls
        for item in self.data_urls:
            yield scrapy.Request(url=item['url'], callback=self.parseTelemercado)


    def parseTelemercado(self, response):
        print ''; print '';
        print 'parseTelemercado'
        print response.url
        url = response.css('span.precio').css('a::attr(href)').extract_first()
        if url is None:
            estado_producto = 'ERROR_PRECIO'
            url=''
        else:
            estado_producto = 'ACTUALIZADA'
        data_url = self.recuperarDataURL(response.url)
        if data_url is not None:
            cz.enviar_actualizacion_producto_custom(
                cod_supermercado = data_url['productosupermercado_id'], 
                supermercado = data_url['supermercado'], 
                status_actualizacion = estado_producto,
                params = 'url',
                url=url
            )


    def recuperarDataURL(self, url):
        for item in self.data_urls:
            if item['url'] == url:
                return item
        return None