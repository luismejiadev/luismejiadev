#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal

MILES = ['MIL ', 'MILLONES ', 'BILLONES ', 'TRILLONES ', 'CUATRILLONES ', 'QUINTILLONES ', 'SIXTILLONES ', 'SEPTILLONES ', 'OCTILLONES ']

NUMEROS = [
    ['','CIENTO ', 'DOSCIENTOS ', 'TRESCIENTOS ', 'CUATROCIENTOS ', 'QUINIENTOS ', 'SEISCIENTOS ', 'SETECIENTOS ', 'OCHOCIENTOS ', 'NOVECIENTOS '  ],           
    [ '', 'UN ', 'DOS ', 'TRES ', 'CUATRO ', 'CINCO ', 'SEIS ', 'SIETE ', 'OCHO ', 'NUEVE ', 'DIEZ ', 'ONCE ', 'DOCE ', 'TRECE ', 'CATORCE ', 'QUINCE ', 'DIECISEIS ', 'DIECISIETE ', 'DIECIOCHO ', 'DIECINUEVE ', 'VEINTE '],
    ['','DIEZ ','VENTI', 'TREINTA ', 'CUARENTA ', 'CINCUENTA ', 'SESENTA ', 'SETENTA ', 'OCHENTA ', 'NOVENTA ', 'CIEN '],
]

def number_to_words(value,currency= "CORDOBAS"):    
    """
    Convert Number to Words
    """
    try:
        value = round(value,2)
    except:
        return value
    
    numbers = str(value).split(".")
    
    words = []
    
    decimales = "" if int(numbers[1]) == 0 else "CON " + numbers[1] + "/100 "
    
    if int(numbers[0])==0:
        words.append( "CERO ")
    elif int(numbers[0])==100:
        words.append( "CIEN ")
    else:
        numbers = list(numbers[0])
        n = len(numbers)    
        tens = 0
        for digit in numbers:
            digit = int(digit)
            pos = n%3
            if pos == 0:
                words.append(NUMEROS[pos][digit])
            elif pos == 2:
                tens = digit
                
            elif pos == 1:
                if tens >2:
                    words.append(NUMEROS[2][tens])
                    if digit !=0:
                        words.append("Y ")
                elif tens ==2:
                    if digit ==0:
                        words.append("VEINTE ")
                    else:
                        words.append("VENTI")
                elif tens == 1:
                    
                    words.append(NUMEROS[1][digit + tens*10])
                
                if tens !=1:
                    words.append(NUMEROS[pos][digit])
            
            if n>3 and pos==1:
                words.append(MILES[n//3-1])
            
            n-=1
    words = "".join(words)    
    return  words + decimales + currency +  (" NETOS" if decimales =="" else "")