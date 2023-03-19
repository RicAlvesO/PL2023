import sys
import re

on=False
saldo=0

def parseLine(line):
    global on
    global saldo

    line = line.strip()
    if re.match(r'LEVANTAR',line):
        print('Introduza moedas:')
        on=True
    elif on==True:
        if re.match(r'POUSAR',line) or re.match(r'ABORTAR',line):
            print('Troco: ',saldo)
            on=False
        elif re.match(r'MOEDA( [0-9]+[ce][,.])+',line):
            moedas=re.split(r' ',line)[1:]
            for moeda in moedas:
                moeda=moeda.strip()
                moeda=moeda[:-1]
                if moeda in ['10c','20c','50c']:
                    saldo+=float(moeda[:-1])/100
                elif moeda in ['1e','2e']:
                    saldo+=float(moeda[:-1])
                else:
                    print('Moeda inválida - '+moeda)
        elif re.match(r'T=[0-9]+',line):
            number = re.split(r'=',line)[1]
            if re.match(r'6[04]1[0-9]+',number):
                print('Número não permitido - '+number)
            elif number.startswith('00'):
                if saldo>=1.50:
                    saldo-=1.5
                    print('Ligação para '+number)
                else:
                    print('Saldo insuficiente')
            elif number.startswith('2') and len(number)==9:
                if saldo>=0.25:
                    saldo-=0.25
                    print('Ligação para '+number)
                else:
                    print('Saldo insuficiente')
            elif number.startswith('800') and len(number)==9:
                print('Ligação para '+number)
            elif number.startswith('808') and len(number)==9:
                if saldo>=0.1:
                    saldo-=0.1
                    print('Ligação para '+number)
                else:
                    print('Saldo insuficiente')

for line in sys.stdin:
    parseLine(line)