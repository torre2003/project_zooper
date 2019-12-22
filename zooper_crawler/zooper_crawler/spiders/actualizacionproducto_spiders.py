import scrapy
from common import comunicacion_zooper as cz

class ActualizacionProductoSpider(scrapy.Spider):
    name = "actualizacionproducto"
    data_urls = None
    def start_requests(self):
        print '///////////'*25
        self.data_urls = cz.consultar_productos_a_actualizar()
        for item in self.data_urls:
            if item['supermercado'] == 'jumbo':
                yield scrapy.Request(url=item['url'], callback=self.parseJumbo)
            elif item['supermercado'] == 'lider':
                yield scrapy.Request(url=item['url'], callback=self.parseLider)
            elif item['supermercado'] == 'telemercado':
                yield scrapy.Request(url=item['url'], callback=self.parseTelemercado)
            elif item['supermercado'] == 'tottus':
                yield scrapy.Request(url=item['url'], callback=self.parseTottus)
            else:
                print 'No se reconoce el supermercado'
        print '//////////'*25

    def parseJumbo(self, response):
        print ''; print '';
        print 'parseJumbo'
        print response.url
        estado_producto='PENDIENTE_ACTUALIZACION'
        precio = response.css('strong.skuBestPrice::text').extract_first()
        if precio is None:
            estado_producto = 'SIN_PRECIO'
            precio=''
        else:
            print precio , 
            aux_precio = precio
            aux_precio = aux_precio.replace('$','')
            aux_precio = aux_precio.replace('.','')
            aux_precio = aux_precio.replace(',','.')
            aux_precio = aux_precio.replace(' ','')
            aux_precio = unicode(int(float(aux_precio)))
            precio=aux_precio
            try:
                int_precio = int(precio)
                estado_producto = 'ACTUALIZADA'
            except Exception, e:
                estado_producto = 'ERROR_PRECIO'

        data_url = self.recuperarDataURL(response.url)
        cz.enviar_actualizacion_producto(
            cod_supermercado = data_url['productosupermercado_id'], 
            supermercado = data_url['supermercado'], 
            precio = precio, 
            status_actualizacion = estado_producto, 
            )
        print precio ,' --- ',estado_producto

    def parseLider(self, response):
        print ''; print '';
        print 'parseLider'
        print response.url
        estado_producto='PENDIENTE_ACTUALIZACION'
        precio = response.css('div[id=productPrice]').css('p.price::text').extract_first()
        if precio is None:
            estado_producto = 'SIN_PRECIO'
            precio=''
        else:
            print precio , 
            aux_precio = precio
            aux_precio = aux_precio.replace('$','')
            aux_precio = aux_precio.replace('.','')
            aux_precio = aux_precio.replace(',','.')
            aux_precio = aux_precio.replace(' ','')
            aux_precio = unicode(int(float(aux_precio)))
            precio=aux_precio
            try:
                int_precio = int(precio)
                estado_producto = 'ACTUALIZADA'
            except Exception, e:
                estado_producto = 'ERROR_PRECIO'
        data_url = self.recuperarDataURL(response.url)
        cz.enviar_actualizacion_producto(
            cod_supermercado = data_url['productosupermercado_id'], 
            supermercado = data_url['supermercado'], 
            precio = precio, 
            status_actualizacion = estado_producto, 
            )
        print precio ,' --- ',estado_producto


    def parseTelemercado(self, response):
        print ''; print '';
        print 'parseTelemercado'
        print response.url
        estado_producto='PENDIENTE_ACTUALIZACION'
        precio = response.css('span.precio').css('a::text').extract_first()
        if precio is None:
            estado_producto = 'SIN_PRECIO'
            precio=''
        else:
            print precio , 
            aux_precio = precio
            aux_precio = aux_precio.replace('$','')
            aux_precio = aux_precio.replace('.','')
            aux_precio = aux_precio.replace(',','.')
            aux_precio = aux_precio.replace(' ','')
            aux_precio = unicode(int(float(aux_precio)))
            precio=aux_precio
            try:
                int_precio = int(precio)
                estado_producto = 'ACTUALIZADA'
            except Exception, e:
                estado_producto = 'ERROR_PRECIO'
        data_url = self.recuperarDataURL(response.url)
        cz.enviar_actualizacion_producto(
            cod_supermercado = data_url['productosupermercado_id'], 
            supermercado = data_url['supermercado'], 
            precio = precio, 
            status_actualizacion = estado_producto, 
            )
        print precio ,' --- ',estado_producto


    def parseTottus(self, response):
        print ''; print '';
        print 'parseTottus'
        print response.url
        estado_producto='PENDIENTE_ACTUALIZACION'
        precio = response.css('div.prices').css('span.active-price').css('span::text').extract()[1]
        if precio is None:
            estado_producto = 'SIN_PRECIO'
            precio=''
        else:
            print precio , 
            aux_precio = precio
            aux_precio = aux_precio.replace('$','')
            aux_precio = aux_precio.replace('.','')
            aux_precio = aux_precio.replace(',','.')
            aux_precio = aux_precio.replace(' ','')
            aux_precio = unicode(int(float(aux_precio)))
            precio=aux_precio
            try:
                int_precio = int(precio)
                estado_producto = 'ACTUALIZADA'
            except Exception, e:
                estado_producto = 'ERROR_PRECIO'
        data_url = self.recuperarDataURL(response.url)
        cz.enviar_actualizacion_producto(
            cod_supermercado = data_url['productosupermercado_id'], 
            supermercado = data_url['supermercado'], 
            precio = precio, 
            status_actualizacion = estado_producto, 
            )
        print precio ,' --- ',estado_producto



    def parse(self, response):
        response.css('strong.skuBestPrice::text').extract_first()

        print '121'*45
        #print response.__dict__
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def recuperarDataURL(self, url):
        for item in self.data_urls:
            if item['url'] == url:
                return item
        return None