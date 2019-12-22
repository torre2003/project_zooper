# -*- coding: utf-8 -*-
import scrapy
import json
import os.path
from scrapy.spiders import CrawlSpider, Rule, BaseSpider
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from datetime import datetime, timedelta



class LoginSpider(BaseSpider):
    name = 'cotmedia.cl'
    start_urls = ['https://www.cotmedia.cl/cotmedia2/index.php']
    url_base = 'http://www.cotmedia.cl/cotmedia2/admin/pauta.php?dia='
    flag = False

    def parse(self, response):
        print '***********************************************'
        print 'PARSE'
        return [
                FormRequest.from_response(
                    response,
                    formdata={
                        # 'kt_login_user': 'rguerrero',
                        # 'kt_login_password': 'ricardo123' ,
                        'kt_login_user': 'mtello',
                        'kt_login_password': 'hadas' ,
                        'kt_login1': 'Ingresar'
                    },
                    callback=self.parse_paginalogin
                )
            ]

    def parse_paginalogin(self, response):
        print '***********************************************'
        print 'AFTER'
        if "authentication failed" in response.body:
            print 'LOGIN FAILED'
            self.log("Login failed", level=log.ERROR)
            return
        else:
            # return Request(url="http://www.cotmedia.cl/cotmedia2/admin/pauta.php?dia=2018-1-22",callback=self.parse_paginapauta)
            # yield scrapy.Request(url="http://www.cotmedia.cl/cotmedia2/admin/pauta.php?dia=2019-12-31",callback=self.parse_paginapauta)
            # yield scrapy.Request(url="http://www.cotmedia.cl/cotmedia2/admin/pauta.php?dia=2018-1-21",callback=self.parse_paginapauta)
            print '***********************************************'
            print '***********************************************'
            print '***********************************************'
            print '***********************************************'
            fecha_inicio = datetime.date(datetime(year=2018, month=12, day=31))
            fecha_final = datetime.date(datetime(year=2015, month=1, day=1))
            # fecha_final = datetime.date(datetime(year=2018, month=12, day=31))
            fecha_actual = fecha_inicio

            while fecha_actual >= fecha_final:
                # print unicode(fecha_actual),
                fecha_url = unicode(fecha_actual.year)+'-'+unicode(fecha_actual.month)+'-'+unicode(fecha_actual.day)
                archivo_registro = 'cotmedia_files/cotmedia_ovallino__'+fecha_url+'.txt'
                # print archivo_registro
                # print unicode(os.path.exists(archivo_registro))
                # print fecha_url ,
                if not os.path.exists(archivo_registro):
                    # print 'existe'
                    yield scrapy.Request(url="http://www.cotmedia.cl/cotmedia2/admin/pauta.php?diario=El%20Ovallino&dia="+fecha_url,callback=self.parse_paginapauta)
                # else:
                    # print '------'
                fecha_actual = datetime.date(datetime(year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day) - timedelta(days=1))

            # fecha_inicio = datetime.date(datetime.today() - timedelta(days=6))
            print '***********************************************'
            print '***********************************************'
            print '***********************************************'
            print '***********************************************'

        print 'LOGIN START'



    def parse_paginapauta(self, response):
        print '|'*25
        print '|'*25
        print response
        print response.url
        print response.url.split('=')[1]
        nombre_archivo = 'cotmedia_ovallino__'+response.url.split('=')[2]+'.txt'
        print '|'*25
        print '|'*25
        print 'V'*25
        response.xpath('//table[2]')
        if len(response.xpath('//table[2]')) == 0:
            return
        filas_tabla = response.xpath('//table[2]//tr')
        i = 1
        keys_diccionario = ['op', 'cliente', 'ubicacion', 'color', 'disposicion', 'tamano', 'pagina', 'total',
        # 'arte', 'vb_com', 
        'estado', 'vendedor', 'fecha_publicacion']
        
        f = open("cotmedia_files/"+nombre_archivo,"w+")
        for k in keys_diccionario:
            f.write(k+"\t")
            print k
        f.write("\r\n")

        filas = []
        while i < len(filas_tabla) - 1:
            aux_fila = {}
            fila_tabla = filas_tabla[i]
            # aux_fila[''] = fila_tabla.xpath('td[0]//text()').extract_first()
            aux_fila['op'] = fila_tabla.xpath('td[1]//text()').extract_first()
            aux_fila['cliente'] = fila_tabla.xpath('td[2]//a//text()').extract_first()
            aux_fila['ubicacion'] = fila_tabla.xpath('td[3]//text()').extract_first()
            aux_fila['color'] = fila_tabla.xpath('td[4]//text()').extract_first()
            aux_fila['disposicion'] = fila_tabla.xpath('td[5]//text()').extract_first()
            aux_fila['tamano'] = fila_tabla.xpath('td[6]//text()').extract_first()
            aux_fila['total'] = fila_tabla.xpath('td[7]//text()').extract_first()
            aux_fila['pagina'] = fila_tabla.xpath('td[8]//text()').extract_first()
            aux_fila['arte'] = fila_tabla.xpath('td[9]//text()').extract_first()
            aux_fila['vb_com'] = fila_tabla.xpath('td[10]//text()').extract_first()
            aux_fila['estado'] = fila_tabla.xpath('td[11]//text()').extract_first()
            aux_fila['vendedor'] = fila_tabla.xpath('td[12]//text()').extract_first()
            aux_fila['llamado'] = fila_tabla.xpath('td[13]//text()').extract_first()
            aux_fila['fecha_publicacion'] = response.url.split('=')[2]+' 00:00:00'
            filas.append(aux_fila)
            i=i+1

        for fila in filas:
            print 'fila'
            print fila
            for k in keys_diccionario:
                print (fila[k])
                try:
                    if fila[k] is not None:
                        f.write(unicode(fila[k])+"\t")
                    else:
                        f.write("\t")
                except Exception,e:
                    f.write("\t")
            f.write("\r\n")
        f.close() 