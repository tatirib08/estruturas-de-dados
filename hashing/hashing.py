import pickle 


class Tabela:
    def __init__(self):
        self.dicionario= dict()
        # self.file=

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
        print("informe o nome do funcionário que deseja adicionar:")
        nome = input()
        print("informe o cargo do funcionário:")
        cargo = input()
        print("informe o salário do funcionário:")
        salario = int(input())
        print("informe a empresa do funcionário: ")
        empresa = input()
        print("deseja adicionar relacionamento?[s/n]")
        resp = input()
        lista = []
        self.dicionario[nome] = {'cargo':cargo,'salario': salario, 'empresa':empresa, 'lista': lista}
        if(resp=='s'):
            self.addRelacionamento(self, nome)
        # adicionando no dicionario

    def listar(self):
        print(self.dicionario)

    
    def atualizarFuncionario(self):
        print("Informe o nome do funcionario que deseja atualizar")
        nome = input()
        # verificar se o funcionario está na lista
        if (nome in self.dicionario):
            # print(self.dicionario[nome]['lista'])
            self.addRelacionamento(self,nome)
            # self.dicionario[nome]['lista'].append('carol')
            print(self.dicionario)
            # print(self.dicionario[nome]['lista'])
        
        else:
            print("O funcionário não está na lista")
        
        
    def addRelacionamento(self, funcionario):        
        
        print("Digite 0 para finalizar ou 1 para continuar")
        escolha = int(input())
        while(escolha!=0):
            print("informe o relacionamento")
            relacao = input()
            self.dicionario[funcionario]['lista'].append(relacao)
            # lista.append(relacao)
            print("digite 0 para finalizar ou 1 para continuar")
            escolha = int(input())

    def buscaFuncionario(self):
        print("")

    def eliminarFuncionario(self):
        print("informe o nome do funcionário que deseja eliminar.")
        nome = input()
        removido = self.dicionario.pop(nome)
        print("funcionario removido:", removido)
        print("novo dicionario", self.dicionario)

    def eliminarRelacionamento():
        print("")

    def salvarArquivo():
        print("")

def main():
    tabela = Tabela()
    tabela.menu()

if __name__ == '__main__':
    main()