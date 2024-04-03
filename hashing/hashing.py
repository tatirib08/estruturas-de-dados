import json
import os

class Tabela:
    def __init__(self):
        self.dicionario= dict()

    def menu(self):
        op = -1
        while(op!=0):
            print("1. Listar os funcionários;") #nomes em ordem alfabética
            print("2. Inserir dados de um funcionário;")
            print("3. Inserir relacionamentos;")
            print("4. Buscar um funcionário;")
            print("5. Eliminar um fucionário;")
            print("6. Eliminar um relacionamento;")
            print("7. Salvar o dicionário em um arquivo;")
            print("Aperte 0 para finalizar.")
            op = int(input())
            
            match op:

                case 1:
                    self.listar()
                case 2:
                    self.addFuncionario()
                case 3:
                    self.atualizarFuncionario()
                case 4:
                    self.buscaFuncionario()
                case 5:
                    self.eliminarFuncionario()
                case 6:
                    self.eliminarRelacionamento()
                case 7:
                    self.salvarArquivo()
                case 0:
                    break
        exit()
    
    def addFuncionario(self):
        print("\nInforme o nome do funcionário que deseja adicionar:")
        nome = input()
        print("\nInforme o cargo do funcionário:")
        cargo = input()
        print("\nInforme o salário do funcionário:")
        salario = int(input())
        print("\nInforme a empresa do funcionário: ")
        empresa = input()
        print("\nDeseja adicionar relacionamento?[s/n]")
        resp = input()
        while(resp!='s' and resp!='n'):
            print("\nInforme uma opção válida.")
            resp = input()
    
        lista = []
        self.dicionario[nome] = {'cargo':cargo,'salario': salario, 'empresa':empresa, 'lista': lista}
        if(resp=='s'):
            self.addRelacionamento(nome)
        self.salvarArquivo()
        

    def listar(self):
        # carregar do arquivo
        
        if os.path.exists("dict.json"):
            file = open("dict.json", "r")
            self.dicionario = json.load(file)
            # print(self.dicionario)
            ordenado = dict(sorted(self.dicionario.items()))
            print(ordenado)
        else:
            print("\nO dicionário está vazio.")

    
    def atualizarFuncionario(self):
        print("\nInforme o nome do funcionario que deseja atualizar")
        nome = input()
        # verificar se o funcionario está na lista
        if (nome in self.dicionario):
            
            self.addRelacionamento(nome)
            
            # print(self.dicionario)
            
        else:
            print("\nO funcionário não está no dicionário.")
        
        self.salvarArquivo()
        
    def addRelacionamento(self, funcionario):        
        
        print("\nDigite 0 para finalizar ou 1 para continuar\n")
        escolha = int(input())
        while(escolha!=0):
            if(escolha == 1):
                print("\nInforme o relacionamento que deseja adicionar.\n")
                relacao = input()
                if (relacao in self.dicionario):
                    # adiciona o relacionamento em ambos os funcionários
                    self.dicionario[funcionario]['lista'].append(relacao)
                    self.dicionario[relacao]['lista'].append(funcionario)
                else:
                    print(relacao, " não está cadastrado.\n")
                    print("\nSó é possível adicionar relacionamentos com funcionários cadastrados.\n")
                    self.addFuncionario()
                print("\nDigite 0 para finalizar ou 1 para continuar.\n")
            else:
                print("\nInforme uma opção válida.\n")
            escolha = int(input())
        self.salvarArquivo()

    def buscaFuncionario(self):
        print("\nInforme o funcionário que deseja buscar.\n")
        nome = input()
        if (nome in self.dicionario):
            print(self.dicionario[nome])
        else:
            print("\nO funcionário não está no dicionário.\n")

    def eliminarFuncionario(self):
        print("\nInforme o nome do funcionário que deseja eliminar.")
        nome = input()
        if (nome in self.dicionario):
            removido = self.dicionario.pop(nome)
            print("\nFuncionario removido:", removido)
            print("\nNovo dicionario", self.dicionario)
            # remover relacionamentos do funcionario removido
            self.removeRel(nome)
        else:
            print("\nO funcionario não está na lista\n")
        self.salvarArquivo()

    def eliminarRelacionamento(self):
        print("\nInforme de qual funcionário deseja eliminar o relacionamento.\n")
        nome = input()
        if (nome in self.dicionario):
            print("Relacionamentos de ", nome,":", self.dicionario[nome]['lista'])
            print("\nInforme o relacionamento que deseja remover.\n")
            rel = input()
            
            # checar se o relacionamento está na lista
            if (rel in self.dicionario[nome]['lista']):
                # remove o relacionamento do funcionario informado
                self.removeRel(rel)
                # remove o funcionario do relacionamento que foi removido
                self.dicionario[rel]['lista'].remove(nome)
            else:
                print("\nO relacionamento não existe.\n")

        else:
            print("\nO funcionário não está no dicionário.")
        self.salvarArquivo()

    def salvarArquivo(self):
        
        print("\nGravando arquivo.\n")

        file = open("dict.json", "w")
        json.dump(self.dicionario, file)
        file.close()
    
    def removeRel(self, rel):
        
        for nome in self.dicionario:

            if (rel in self.dicionario[nome]['lista']):
                
                self.dicionario[nome]['lista'].remove(rel)
                
                # print(self.dicionario[nome]['lista'])

def main():
    tabela = Tabela()
    tabela.menu()

if __name__ == '__main__':
    main()