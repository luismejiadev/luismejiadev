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
    
    decimals = "" if int(numbers[1]) == 0 else "CON " + numbers[1] + "/100 "
    
    if int(numbers[0])==0:
        words.append("CERO ")

    
    else:
        numbers = list(numbers[0])
        n = len(numbers)    
        tens = 0
        hundreds = 0
        for digit in numbers:
            digit = int(digit)
            pos = n%3
            if pos == 0:
                hundreds = digit
                if digit !=1:
                    words.append(NUMEROS[pos][digit])
                
                    
            elif pos == 2:
                tens = digit
                
            elif pos == 1:
                
                if hundreds == 1 :
                    if tens ==0 and digit == 0:
                        words.append("CIEN ")
                    else:
                        words.append(NUMEROS[0][1])
                elif tens >2:
                    words.append(NUMEROS[2][tens])
                    if digit !=0:
                        words.append("Y ")
                elif tens ==2:
                    if digit ==0:
                        words.append(NUMEROS[1][20])
                    else:
                        words.append(NUMEROS[2][2])
                elif tens == 1:
                    
                    words.append(NUMEROS[1][digit + tens*10])
                
                if tens !=1:
                    words.append(NUMEROS[pos][digit])
            
            if n>3 and pos==1:
                words.append(MILES[n//3-1])
            
            n-=1
    words = "".join(words)    
    return  words + decimals + currency +  (" NETOS" if decimals =="" else "")


def moneyfmt( value, places = 4, curr = '', sep = ',', dp = '.', pos = '', neg = '-', trailneg = '' ):
    """
    Convert Decimal to a money formatted string.

    @param places:  required number of places after the decimal point
    @type places: int
    @param curr:    optional currency symbol before the sign (may be blank)
    @type curr: string
    @param  sep:     optional grouping separator (comma, period, space, or blank)
    @type sep: string
    @param dp:      decimal point indicator (comma or period)  only specify as blank when places is zero
    @type dp: string
    @param pos:     optional sign for positive numbers: '+', space or blank
    @type pos: string
    @param neg:     optional sign for negative numbers: '-', '(', space or blank
    @type neg: string
    @param trailneg: optional trailing minus indicator:  '-', ')', space or blank
    @type trailneg: string
    @rtype: string

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.8901'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.0200>'

    """
    q = Decimal( 10 ) ** -places      # 2 places --> '0.01'
    sign, digits, _exp = value.quantize( q ).as_tuple()
    result = []
    digits = map( str, digits )
    build, next = result.append, digits.pop
    if sign:
        build( trailneg )
    for _i in range( places ):
        build( next() if digits else '0' )
    if places > 0 :
	build( dp )
    if not digits:
        build( '0' )
    i = 0
    while digits:
        build( next() )
        i += 1
        if i == 3 and digits:
            i = 0
            build( sep )
    build( curr )
    build( neg if sign else pos )
    return ''.join( reversed( result ) )
