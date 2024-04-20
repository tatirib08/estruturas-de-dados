import pandas as pd

data = pd.read_csv('app_web/livros.csv') # Carregamento do arquivo

tamanhoMax = 52

tabela = [['', '']]*tamanhoMax

def converterString(string):
  soma=0
  for pos in range(len(string)):
    soma+=ord(string[pos])
  return soma

def hashPrincipal(value): # Calcular a posição do elemento na tabela
    val = converterString(value)
    return val % tamanhoMax

def deslocamento(value): # Calcular o deslocamento do elemento após colisão
  val = converterString(value)
  return round((val / tamanhoMax) % tamanhoMax)

def verificarPosicao(value1, value2): # Para saber se uma posição é valida para inserção
  if (value1 == value2):
    print(f'O valor {value1} já está inserido na tabela.')
    return False
  elif (value2 == 'none' or value2 == '##'):
    return True
  else:
    return False

def busca(value):
  leituras = 1
  pos = hashPrincipal(value)
  desloc = deslocamento(value)
  novaPos = pos + desloc
  if novaPos >= tamanhoMax:
    novaPos = novaPos - tamanhoMax
  if tabela[pos][0] == value:
    print(f'Valor encontrado após {leituras} leitura(s)')
  else:                     # Caso o elemento não seja encontrado na sua posição padrão, cai no looping
    while novaPos != pos:
      leituras = leituras + 1
      if tabela[novaPos][0] == value:
        print(f'Valor encontrado após {leituras} leitura(s)')
      elif tabela[novaPos][0] == 'none' or tabela[novaPos][0] != value:
        print(f'Valor não encontrado... {leituras} leitura(s)')
        #break
      novaPos = novaPos + desloc
      if novaPos >= tamanhoMax:
        novaPos = novaPos - tamanhoMax

def remover(value):
  pos = hashPrincipal(value)
  desloc = deslocamento(value)
  novaPos = pos + desloc
  if novaPos >= tamanhoMax:
    novaPos = novaPos - tamanhoMax
  if tabela[pos][0] == value:
    tabela[pos] = ['##', 0, '##']
    print(f'Valor {value} removido com sucesso!\n')
    for value in tabela:
      print(value)
  else:                     # Caso o elemento não seja encontrado na sua posição padrão, cai no looping
    while novaPos != pos:
      if tabela[novaPos][0] == value:
        tabela[novaPos] = ['##', 0, '##']
        print(f'\nValor {value} removido com sucesso!\n')
        for value in tabela:
          print(value)
        break
      elif tabela[novaPos][0] == 'none' or tabela[novaPos][0] != value:
        print(f'Valor não encontrado...')
      novaPos = novaPos + desloc
      if novaPos >= tamanhoMax:
        novaPos = novaPos - tamanhoMax

def metodoHashingDuplo():
  leituras = 0
  for i, registro in data.iterrows():
    posicao = hashPrincipal(registro[nome])
    if (tabela[posicao][0] == 'none'): # Se a posição está vazia, adiciona
      tabela[posicao] = [registro[nome], registro['RG'], registro['Signo']]
    else:  #Senão, faz o deslocamento
      print('Ocorreu uma colisão para o valor %s'% registro['nome']) 
      if (registro['nome'] != tabela[posicao][0]): # Se o valor é diferente do valor já inserido, procura uma nova posição
        deslocar = deslocamento(registro['nome'])
        if (deslocar == 0): 
          deslocar = 1 # Atribui o valor 1 caso o calculo do deslocamento dê 0
        novaPosicao = posicao + deslocar # Valor para a nova posição
        while (novaPosicao != posicao):
          leituras = leituras + 1
          if (novaPosicao >= tamanhoMax):
            novaPosicao = novaPosicao - tamanhoMax
          if (verificarPosicao(registro['nome'], tabela[novaPosicao][0])): # Verifica se a nova posição está vazia
            print(f'Inserido após colição na posição {novaPosicao}\nTotal de {leituras} acesso(s)\n')
            tabela[novaPosicao] = [registro['nome'], registro['RG'], registro['Signo']] # Inserido após colisão
            novaPosicao = posicao
          else: # se não está vazia, prossegue a busca
            novaPosicao = novaPosicao + deslocar
            if (novaPosicao == posicao):
              print('Todas as posições possíveis para %s estão preenchidas\n'% registro['nome'])
      else:
        print('O valor %s já está na tabela!'% registro['nome']) 
  print('\n')

metodoHashingDuplo()
for value in tabela:
  print(value)

print('\n')
print('=========='*7)
print(' '*13+'Tabela Hash'+' '*13)
print('=========='*7)
print('\n')
opcao = 0
while opcao != 3:
  opcao = int(input('''
  Escolha uma opção:
  [1] - Pesquisar um valor na tabela
  [2] - Remover um valor da tabela
  [3] - Sair
  
  '''))
  if opcao == 1:
    escolha = str(input('\nInforme um valor para pesquisar na tabela: '))
    busca(escolha)
    print('')
  elif opcao == 2:
    escolha = str(input('\nInforme um valor para remover da tabela: '))
    remover(escolha)
  elif opcao == 3:
    print('Saindo...')
  else:
    print('Opção inválida.')
print('Fim do programa')