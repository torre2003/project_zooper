# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from common import comunicacion_zooper as cz
from common import utils_bdd as bdd
import re



class ProductosSpider(CrawlSpider):
    name = 'lider_busqueda'
    allowed_domains = ['www.lider.cl']

    urls_encontradas = []
    paginas = []

    def start_requests(self):
        urls = None
        if True:
            r = cz.consultar_articulo_supermercado_custom(supermercado='lider')
            if r['status'] == 'success':
                urls = r['info']
            else:
                print 'error'
                urls = []
        else:
            urls = [
                'https://www.lider.cl/supermercado/product/Drive-Detergente-Líquido-Perfect-Results-Recarga/660114',
                
            ]
        print ' *'*30
        print 'Urls buscadas'
        for url in urls:
            print url
            yield scrapy.Request(url=url, callback=self.parse_detalle)
        print ' *'*30

    def parse_detalle(self, response):
        url = response._url
        codigo = response.selector.xpath('//*[@id="item-number-id"]//text()')[0].extract()
        titulo = ''
        try:
            titulo = response.selector.xpath('//h1/span//text()')[0].extract()
        except Exception, e:
            pass
        subtitulo = ''
        try:
            subtitulo = response.selector.xpath('//h1/span//text()')[1].extract()
        except Exception, e:
            pass
        caracteristica = ''
        try:
            caracteristica = response.selector.xpath('//h1/span//text()')[2].extract()
        except Exception, e:
            pass
        
        precio = ''
        try:
            precio = response.selector.xpath('//*[@id="productPrice"]/p[2]')[0].xpath('@content').extract_first()
        except Exception, e:
            pass
        precio_unidad_medida = ''
        try:
            precio_unidad_medida = response.selector.xpath('//*[@id="productPrice"]/p[3]//text()')[0].extract()
        except Exception, e:
            pass
        precio_unidad_medida = ''
        try:
            precio_unidad_medida = re.sub(r'[^a-zA-Z0-9:$]', '', precio_unidad_medida) # eliminamos los caracteres raros
        except Exception, e:
            pass

        aux_codigo_imagen = url.split('/')
        codigo_imagen = aux_codigo_imagen[len(aux_codigo_imagen)-1]
        url_imagen = 'https://images.lider.cl/wmtcl?source=url[file:/productos/'+codigo_imagen+'a.jpg'

        aux_producto = {
            'url_producto':url,
            'url_imagen':url_imagen,
            'codigo':codigo,
            'marca':titulo,
            'nombre':subtitulo,
            'caracteristica':caracteristica,
            'precio':precio,
            'precio_unidad_medida':precio_unidad_medida,
            'etiquetas_precio':[],
            'etiquetas_oferta':[],
        }

        etiquetas_precio = response.selector.xpath('//div[@id="loadPDPCon"]//div[@id="productPrice"]//p')
        for etiqueta in etiquetas_precio:
            _id = etiqueta.xpath('@id')
            _class = etiqueta.xpath('@class')
            _itemprop = etiqueta.xpath('@itemprop')
            _content = etiqueta.xpath('@content')
            _texto = etiqueta.xpath('text()')
            aux = {'id':'','class':'','itemprop':'','content':'','texto':'',}
            if len(_id) > 0:
                aux['id'] = _id[0].extract()
            if len(_class) > 0:
                aux['class'] = _class[0].extract()
            if len(_itemprop) > 0:
                aux['itemprop'] =_itemprop[0].extract()
            if len(_content) > 0:
                aux['content'] = _content[0].extract()
            if len(_texto) > 0:
                aux['texto'] = _texto[0].extract()
            aux_producto['etiquetas_precio'].append(aux);

        ##########################
        ## Faltan etiquetas oferta
        ##########################
            # print _id,' - ',_class,' - ',_itemprop,' - ',_content,' - ',_texto

        etiquetas_oferta = response.selector.xpath('//div[@id="loadPDPCon"]//div[@class="product-tags"]//span')
        for etiqueta in etiquetas_oferta:
            clases_etiqueta = etiqueta.xpath('@class')
            texto_etiqueta = etiqueta.xpath('text()')
            otros_etiqueta = etiqueta.xpath('*')
            aux = {}
            aux['clase'] = []
            _class = clases_etiqueta.extract_first()
            for __class in _class.split(' '):
                if __class != 'label-icon':
                    aux['clase'].append(__class)
            aux['texto'] = texto_etiqueta.extract_first()
            if len(otros_etiqueta) > 0:
                otros_etiqueta = otros_etiqueta.xpath('text()')
                otros_etiqueta = otros_etiqueta.extract_first()
            else:
                otros_etiqueta = None
            aux['otros'] = otros_etiqueta
            aux_producto['etiquetas_oferta'].append(aux);
            print aux
        print '---------------'
        
        dump = json.dumps(aux_producto, ensure_ascii=False)
        print dump
        codigo_temporal = bdd.ingresar_registro_temporal (aux_producto)
        # ingresar_articulo_supermercado_custom(supermercado, **extra_params)
        cz.ingresar_articulo_supermercado_custom(
            supermercado='lider',
            data={},
            opcion='ingreso_producto',
            cod_supermercado=codigo,
            status_actualizacion='actualizado',
            codigo=codigo_temporal,
            # params,
            # **extra_params
        )
