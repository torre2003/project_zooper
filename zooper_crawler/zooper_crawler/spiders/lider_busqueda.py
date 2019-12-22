# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
import re
from common import utils_bdd as bdd
from common import comunicacion_zooper as cz


class BusquedaProductosSpider(CrawlSpider):
    name = 'lider_busqueda'
    allowed_domains = ['www.lider.cl']
    url_origen = 'https://www.lider.cl/supermercado/category/Congelados/?No=80&isNavRequest=Yes&Nrpp=40&page=-1'
    # start_urls = [origen]
    urls_encontradas = []
    paginas = []

    def start_requests(self):
        urls = [
            self.url_origen,
        ]
        self.urls_encontradas.append(self.url_origen)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_busqueda)


    def parse_busqueda(self, response):
        #########################
        #   Analisis de productos
        #########################

        item_links = response.css('.product-link::attr(href)').extract()
        print(len(item_links))
        for item_link in item_links:
            link = 'https://www.lider.cl'+item_link
            if not link in self.urls_encontradas:
                self.urls_encontradas.append(link)
                print link
                codigo_temporal = bdd.ingresar_registro_temporal ({'url':link})
                # ingresar_articulo_supermercado_custom(supermercado, **extra_params)
                cz.ingresar_articulo_supermercado_custom(
                    supermercado='lider',
                    data={},
                    opcion='ingreso_busqueda',
                    codigo=codigo_temporal,
                    # params,
                    # **extra_params
                )
                yield scrapy.Request(link, callback=self.parse_busqueda)

        ######################
        #   Agregación de links de paginación
        ######################
        
        links_paginado = response.selector.xpath('//*[@id="paginationBox"]/nav/ul[@class="pagination pull-right"]/li/a//@href').extract()
        for link_pagina in links_paginado:
            link = 'https://www.lider.cl'+link_pagina
            if not link in self.urls_encontradas:
                try:
                    pagina_actual = link.split('page=')[1]
                    if not pagina_actual in self.paginas:
                        self.paginas.append(pagina_actual)
                        self.urls_encontradas.append(link)
                        yield scrapy.Request(link, callback=self.parse_busqueda)
                except Exception, e:
                    pass
