# -*- coding: utf-8 -*-
import string
import sys
from fractions import Fraction
from decimal import Decimal
import matplotlib.pyplot as plt
from sympy import Symbol, limit
from math import log
#from mpmath import

'''
*** Para identificar, se a série converge mas a dos valores absolutos diverge, então é possível obter um L.
'''


print '''
Curso:      Análise Matemática para Aplicações
Professor:  Antônio Carlos Saraiva Branco 
Aluno:      Pablo Cerdeira
Exercício:
Fazer um progama que tenha como entradas um número real L e um epsilon > 0 (tolerância).

Rearranjar os termos da série harmônica alternada de modo que ela convirja para L;
Critério de parada: | Sn - L | < epsilon, para qualquer n > N

Saídas:
    np1, np2, np3, ... , npk (número de parcelas positivas entre as "viradas")
    nn1, nn2, nn3, ... , nnk (número de parcelas negativas entre as "viradas")
-----------

Instruções:
- Termo geral da série alternada a utilizar. Ex:
    Harmônica alternada: (-1)**(x+1)/x
    etc
    OBS: Se o campo for deixado em branco, a série harmônica alternada é utilizada por padrão.

- Número real L: número a ser alcançado no limite da converência. Ex:
    0.0
    2.0
   -2.5
    etc
    OBS: Se o campo for deixado em branco, 0.0 será utilizado.
    
- Épsilon: tolerância de convergência. Ex:
    0.01
    0.001
    etc
    OBS: Se o campo for deixado em branco, 0.01 será utilizado.
    
'''

# variáveis globais
termoGeral = ''
L, E = float('Inf'), float('Inf')
inf = float('Inf')
i = 1.
somatorio = 0.
bufferPositivos = []
bufferNegativos = []
somatorioHist = []
elementosHist = []
x = Symbol('x')


def parametros():
    global termoGeral, L, E
    termoGeral = raw_input('Termo Geral (default: harmônica alternada): ')
    if len(termoGeral) < 1:
        termoGeral = '((-1)**(x+1))/x'                   
        #termoGeral = '(-1)**(x+1)/2**x'                
        #termoGeral = '(-1)**(x+1)/x**2'                
        #termoGeral = '((-1)**(x+1))*3*x/((4*x)-1)'
    L = raw_input('Número real L (default: 0.0): ')
    if len(L) < 1:
        # L = log(2)
        L = 0.
    else:
        if '.' not in L: L+'.'
        L = float(L)
    E = raw_input('Épsilon (default: 0.01): ')
    if len(E) < 1:
        E = 0.01
    else:
        if '.' not in E: E+'.'
        E = float(E)
    

# função para calcular o elemento n da série
# divido o termo geral em denominador e numerador e os calculo separadamente
# isso para evitar que a função retorne floats irracionais, como no caso de
# 1/6, que retornaria 0,1666667, desviando o resultado.

def serieElemento(termoGeral,retFloat=False):                                                  
    global i
    
    termoGeral = termoGeral.replace('x',str(i))                                 # Substitui a variável x pelo valor de n
    if retFloat == False:
        termoGeral = termoGeral.split('/')                                      # Divide o termo geral para calcular denominador numerador independentemente
        termoGeral1 = Decimal(eval(termoGeral[0]))                              # Calcula numerador
        termoGeral2 = Decimal(eval(termoGeral[1]))                              # Calcula denominador
        termoGeral = str(termoGeral1)+'/'+str(termoGeral2)                      # Remonta o resultado na forma de fração e não de float
        return Fraction(termoGeral)
    else:
        return float(eval(termoGeral))

# função para somar o próximo elemento ao somatório

def somar(termoGeral,somatorio,sentido):
    global i
    while len(bufferPositivos) < 1 or len(bufferNegativos) < 1:                   # Verifica se as listas de negativos e positivos tem pelo menos um elemento
        elemento = serieElemento(termoGeral)                                    # Em caso negativo, calcula os próximos elementos até que ambas
        i += 1                                                                  # tenham pelo menos um elemento
        if elemento > 0: bufferPositivos.append(elemento)                       # Se o elemento é positivo, adiciona ao bufferPositivos
        else: bufferNegativos.append(elemento)                                  # Se é negativo, ao bufferNegativo
    if sentido == 'positivo':                                                   # Verifica o sentido da soma
        elemento = bufferPositivos.pop(0)                                       # Retira o elementoa esquerda do bufferPositivos
        print '+++ Somar positivo - Valor anterior: %s - Elemento: %s - Valor atual: %s' % (str(somatorio),str(elemento),str(somatorio + elemento))
        somatorio = somatorio + elemento                                        # Soma o elemento retirado ao somatório                                      
        elementosHist.append(str(elemento))                                     # Adiciona o elemento somado ao histórico de elementos
        somatorioHist.append(somatorio)                                         # Adiciona o resultado parcial do somatório ao histórico de resultados
    else:
        elemento = bufferNegativos.pop(0)                                       # Mesmo passos do acima, no caso de somar elemento negativo
        print '--- Somar negativo - Valor anterior: %s - Elemento: %s - Valor atual: %s' % (str(somatorio),str(elemento),str(somatorio + elemento))
        somatorio = somatorio + elemento
        elementosHist.append(str(elemento))
        somatorioHist.append(somatorio)
    return somatorio


# função para verificar se a série é alternada ou não

def verificaAlternancia():
    global termoGeral, x, i
    
    ''' 
    Atenção:
    Este teste é superficial.
    Apenas garante que a série dada parece ser alternada.
    Pode haver casos em que a alternância não seja detectada.
    '''
    elementos = []
    print 'Testando alternância da série.'
    for i in range(1,5):
        elementos.append(serieElemento(termoGeral))
        i += 1
    if (elementos[0] >= 0 and elementos[1] <= 0 and elementos[2] >= 0 and elementos[3] <= 0) or \
        (elementos[0] >= 0 and elementos[1] <= 0 and elementos[2] >= 0 and elementos[3] <= 0):
        print 'A série parece ser alternada. Continuando...'
    else:
        print 'A série %s não parece ser alternada. Parando.' % str(termoGeral)
        sys.exit()
    i = 1.



def main():
    global termoGeral, L, E, elemento, somatorio, i, x
    parametros()                                                                # Pega parâmetros
    verificaAlternancia()                                                       # Verifica a alternância da série
    out()

    
def out():
    global termoGeral, L, E, elemento, somatorio, i, x, bufferPositivos, bufferNegativos
    inversoes = 0                                                               # conta as inversoes menores que Epsilon
    sentido = ''
    nextSomatorio = 0.
    tmpD = 0.
                                                                                                                                                            # Preparando primeiro elemento      
    elemento = serieElemento(termoGeral)                                        # Calcula o elemento atual
    somatorio += elemento                                                       # Calcula o somatório
    elementosHist.append(str(Fraction(elemento)))                               # Adiciona o elemento atual ao histórico de elementos
    somatorioHist.append(somatorio)                                             # Adiciona o resultado parcial do somatório ao histórico de resultados
    D = abs(L - somatorio)                                                      # Distância entre limite pretendido (L) e somatório atual
    i += 1
    
    while D >= E or inversoes < 2:                                             # Loop para somar elementos positivos e negativos ao somatório
        if somatorio > L:                                                       # Se o somatório atual for maior do que o limite L
            somatorio = somar(termoGeral,somatorio,'negativo')                  # Então somar negativos
            sentido = 'cima'
        else:                                                                   # Se o somatório atual for menor do que o limite L
            somatorio = somar(termoGeral,somatorio,'positivo')                  # Então somar positivos
            sentido = 'baixo'
        D = abs(L - somatorio)                                                  # Recalcula a distância entre o limite L e somatório 
        if D < E:
            if sentido == 'cima':
                elemento = bufferPositivos[0]
                nextSomatorio = somatorio + elemento 
                tmpD = abs(L - nextSomatorio)
            else:
                elemento = bufferNegativos[0]
                nextSomatorio = somatorio + elemento 
                tmpD = abs(L - nextSomatorio)
            if tmpD < E:
                inversoes += 1

    print '---'
    print 'Concluído'
    print '---'
    print 'Limite = %s' % str(L)
    print 'Epsilon = %s' % str(E)
    print 'Somatório = %s' % str(somatorio)
    print 'Distância = %s' % str(D)
    print 'Histórico do somatório (em float):'
    print str(somatorioHist)
    print 'Histórico dos elementos (em decimais):'
    print str(elementosHist)
    plt.plot(somatorioHist)                                                     # Plota gráfico com os resultados
    plt.axhline(y=L,color='r')                                                  # Adiciona linha horizontal vermelha no limite L
    plt.show()                                                                  # Exibe o gráfico

if __name__ == "__main__":
    main()