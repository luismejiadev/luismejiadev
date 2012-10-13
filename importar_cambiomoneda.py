# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from core.models import TipoCambio, Moneda
import datetime
from django.db import transaction
from contabilidad.models import MESES
from suds.client import Client
from decimal import Decimal

class Command(BaseCommand):
    help = 'Importar tipos de cambios del banco central para el mes actual'
    
    @transaction.commit_manually
    def handle(self, *args, **options):
        
        try:            
            year = int(args[0] if len(args) > 0 else datetime.date.today().year)
            month = int(args[1] if len(args) > 1 else datetime.date.today().month)
            moneda = Moneda.objects.get(pk=2)
            source = args[2] if len(args) > 2 else "WS"
            
            if source == "WS":
                print "conectando a webservice .... "
                client = Client('https://servicios.bcn.gob.ni/Tc_Servicio/ServicioTC.asmx?WSDL')
                print "conexion realizada"
                
                print "obteniendo data .... para %s %s"%(year,month)
                data = client.service.RecuperaTC_Mes(year,month)[0][0]
                print "data obtenida"
                for record in data:
                    fecha = record['Fecha']
                    base = record['Valor']
                    tipo  = TipoCambio.objects.create(moneda=moneda,fecha=fecha, base = base)
                    print "*************************"
                    print base
                    print fecha
                    print "*************************"
                    tipo.save()   
            else:
                print "Abriendo archivo  .... "
                with open(source, 'r') as file_handle:
                    lines = file_handle.readlines()            
                print "archivo abierto"

                print "obteniendo data .... para %s %s"%(year,month)
                soup = get_soup(" ".join(lines))
                
                for line in soup.findAll("tr"):
                    cols = line.findAll("td")
                    if len(cols) ==2:
                        fecha = datetime.datetime.strptime(cols[0].text,"%d-%m-%Y") 
                        base = Decimal(cols[1].text)
                        print fecha, base
                        tipo  = TipoCambio.objects.create(moneda=moneda,fecha=fecha, base = base)                        
                    
                             
            
    
        except Exception as inst:
            print u"No se pudieron importar los Tipos de Cambios para el mes de  %s-%d" % (  MESES[month][1], year)            
            transaction.rollback()
            print unicode(inst)
        else:
            transaction.commit()
            print u"Tipos de Cambios Importados exitosamente para el mes de  %s-%d" % (  MESES[month][1], year)
                    
        

        

def get_soup(value):
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from beautifulsoup import BeautifulSoup
    return BeautifulSoup(value)