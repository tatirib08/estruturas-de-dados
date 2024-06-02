import pickle, os

class LempelZivWelch():

    @staticmethod
    def compress(stringfied_file: str, file_name: str = "./output.pkl", print_stats: bool = False, print_variables: bool = False) -> None:
        string: str = stringfied_file
        root_dictionary: list = LempelZivWelch.__take_root_chars(string)
        dictionary: list = root_dictionary.copy()
        
        raw_result: list = []
        final_result: str = ""
        prefix: str = ""

        #realiza a compressão
        for current_char in string:

            prefix_plus_current_char = prefix + current_char

            #checa se a nova palavra está no dicionário
            if not prefix_plus_current_char in dictionary:
                dictionary.append(prefix_plus_current_char)

                max_index_representable_in_unicode = 1114111

                if prefix != "":
                    index = dictionary.index(prefix) #indice 0 nunca deve ser utilizado, para que se tenha um caractere livre não-ambíguo
                    char_to_append = ""
                    #verifica se é possivel representar indice utilizando a tabela unicode
                    if index <= max_index_representable_in_unicode:
                        char_to_append = chr(index)
                    #se não é representavel pela tabela unicode, coloca o índice inteiro como string (o ideal seria dividir em varios caracteres unicode para reduzir o tamanho)
                    else:
                        char_to_append = index 

                    raw_result.append(char_to_append)
                
                prefix = current_char
            else:
                prefix = prefix + current_char

        else:
            index = dictionary.index(prefix)
            if index <= max_index_representable_in_unicode:
                char_to_append = chr(index)
            else:
                char_to_append = index
            raw_result.append(char_to_append)


        #adiciona o dicionario de raizes no inicio do resultado
        final_result += LempelZivWelch.__root_dict_to_str(root_dictionary)

        #adiciona a sequencia codificada
        final_result += LempelZivWelch.__encoded_sequence_to_str(raw_result)

        #serializa a string
        with open(file_name, 'wb') as file:
            pickle.dump(final_result, file)

        #imprime os resultados da compressão
        if print_variables or print_stats:
            print("\n--COMPRESSÃO--")
        if print_variables:
            print(f'dicionario raizes -> {root_dictionary}')
            print(f'dicionario completo -> {dictionary}')
            print(f'sequencia codificada -> {raw_result}')
            print(f'resultado final -> {final_result}')
        if print_stats:
            tamanho_original = len(string)
            tamanho_comprimido = os.stat(file_name).st_size
            print(f'tamanho original -> {tamanho_original} bytes')
            print(f'tamanho comprimido -> {tamanho_comprimido} bytes')
            print(f'taxa de compressão (em relação ao tamanho original) -> {-100 + (100*(tamanho_comprimido/tamanho_original))}%\n')

    @staticmethod
    def uncompress(file_path: str, print_variables: bool = False) -> str:
        with open(file_path, 'rb') as file:
            encoded_string: str = pickle.load(file)

            root_dictionary: list = LempelZivWelch.__take_root_dict_from_str(encoded_string)
            
            dictionary: list = root_dictionary.copy()
            
            encoded_sequence: list = LempelZivWelch.__take_encoded_sequence_from_str(encoded_string)

            if print_variables:
                print("\n--DESCOMPRESSÃO--")
                print(f'dicionario de raizes -> {root_dictionary}')
                print(f'sequencia_codificada ->  {encoded_sequence}')

            result: str = ""

            pW: str = ""

            encoded_sequence_index: int = 0

            cW: str = encoded_sequence[encoded_sequence_index]

            result += dictionary[cW]

            while encoded_sequence_index < len(encoded_sequence):

                pW = cW

                encoded_sequence_index += 1

                if encoded_sequence_index >= len(encoded_sequence):
                    continue

                cW = encoded_sequence[encoded_sequence_index]

                does_exist_in_dictionary: bool = cW < len(dictionary)
                if does_exist_in_dictionary:
                    result += dictionary[cW]
                    P: str = ""
                    if pW > 0 and pW < len(dictionary):
                        P = dictionary[pW]
                    C: str = dictionary[cW][0]
                    dictionary.append(P + C)
                else:
                    P: str = dictionary[pW]
                    C: str = P[0]
                    dictionary.append(P + C)
                    result += (P + C)

            return result

    @staticmethod
    def __take_root_chars(string: str) -> list:
        result: list = [""] #primeiro indice é reservado

        for char in string:
            if not char in result:
                result.append(char)

        return result
    
    @staticmethod
    def __root_dict_to_str(root_list: list) -> str:
        final_result: str = ""

        for char in root_list:
            if char != None:
                final_result += str(char)
        final_result += chr(0) 
        #dicionario de raizes é separado da sequência codificada por caractere de indice 0 na tabela unicode, já que com certeza não vai gerar conflito.
        
        return final_result

    @staticmethod
    def __encoded_sequence_to_str(coded_sequence_list: list) -> str:
        final_result: str = ""

        for char in coded_sequence_list:
            #toda vez que a palavra código possuir mais de um caractere, é colocada entre caracteres de indice 0 da tabela unicode (somente em casos que não foi possível representar com tabela unicode)
            if(len(str(char)) > 1):
                final_result += chr(0)
                final_result += str(char)
                final_result += chr(0)
            else:
                final_result += str(char)
        
        return final_result
    
    @staticmethod
    def __take_root_dict_from_str(encoded_message: str) -> list:
        final_result: list = [""] # primeiro índice é reservado

        for char in encoded_message:
            if char != chr(0):
                final_result.append(char)
            else:
                break
        
        return final_result
    
    @staticmethod
    def __take_encoded_sequence_from_str(encoded_message: str) -> list:

        final_result: list = []
        starting_index = encoded_message.index(chr(0)) + 1
        char_index = starting_index

        #lẽ a mensagem comprimida começando depois do dicionario de raizes (depois do primeiro chr(0))
        while char_index < len(encoded_message):
            char: str = encoded_message[char_index]
            
            #se for um caractere unicode, lê normal
            if char != chr(0):
                final_result.append(ord(char))
            #se não for um caractere unicode, lê o número caractere por caractere -> chr(0) indica o inicio de um numero por extenso em string
            else:
                char_index += 1 #vai pro primeiro caractere do numero por extenso
                number_str: str = ""
                while encoded_message[char_index] != chr(0): #le até o proximo chr(0) indicar que o numero por extenso finalizou
                    number_str += encoded_message[char_index]
                    char_index += 1
                final_result.append(int(number_str))
        
            char_index += 1

        return final_result
        

def main():
    test = "{'0': {'nome': 'É assim que acaba', 'autor': 'Colleen Hoover', 'quantidade': 43, 'img': 'https://m.media-amazon.com/images/I/9112cWOV-OL._SY385_.jpg'}, '1': {'nome': 'É assim que começa', 'autor': 'Colleen Hoover', 'quantidade': 17, 'img': 'https://m.media-amazon.com/images/I/813TDwBsihL._SY385_.jpg'}, '2': {'nome': 'A Hipótese do Amor', 'autor': 'Ali Hazelwood', 'quantidade': 48, 'img': 'https://m.media-amazon.com/images/I/41knBs4ouOL._SY445_SX342_.jpg'}, '3': {'nome': 'Uma Breve História do Tempo', 'autor': 'Stephen Hawking', 'quantidade': 42, 'img': 'https://m.media-amazon.com/images/I/51aG2+outOL._SY445_SX342_.jpg'}, '4': {'nome': 'O Universo Numa Casca de Noz', 'autor': 'Stephen Hawking', 'quantidade': 33, 'img': 'https://m.media-amazon.com/images/I/51wYh204mfL._SY445_SX342_.jpg'}, '5': {'nome': 'O Universo Elegante', 'autor': 'Brian Greene', 'quantidade': 10, 'img': 'https://m.media-amazon.com/images/I/61r1T8rcXAL._SY385_.jpg'}, '6': {'nome': 'Breves Respostas para Grandes Questões', 'autor': 'Stephen Hawking', 'quantidade': 39, 'img': 'https://m.media-amazon.com/images/I/51uywlQG4UL._SY445_SX342_.jpg'}, '7': {'nome': 'O Homem de Giz', 'autor': 'C. J. Tudor', 'quantidade': 16, 'img': 'https://m.media-amazon.com/images/I/41LuOehnKtL._SY445_SX342_.jpg'}, '8': {'nome': 'Manual de Assassinato para Boas Garotas', 'autor': 'Holly Jackson', 'quantidade': 34, 'img': 'https://m.media-amazon.com/images/I/71fE-JgveUL._SY385_.jpg'}, '9': {'nome': 'Anatomia do Mal', 'autor': 'Harold Schechter', 'quantidade': 50, 'img': 'https://m.media-amazon.com/images/I/71SV55vWSEL._SY385_.jpg'}, '10': {'nome': 'Os Sertões', 'autor': 'Euclides da Cunha', 'quantidade': 37, 'img': 'https://m.media-amazon.com/images/I/61wNPOSBNsL._SY385_.jpg'}, '11': {'nome': 'O Gato Malhado e a Andorinha Sinhá', 'autor': 'Jorge Amado', 'quantidade': 14, 'img': 'https://m.media-amazon.com/images/I/51TFb7yExqS._SY445_SX342_.jpg'}, '12': {'nome': 'O Jardim das Borboletas', 'autor': 'Dot Hutchison', 'quantidade': 47, 'img': 'https://m.media-amazon.com/images/I/A142ngVX2rL._SY385_.jpg'}, '13': {'nome': 'Capitães da Areia', 'autor': 'Jorge Amado', 'quantidade': 6, 'img': 'https://m.media-amazon.com/images/I/41egZIo3eYL._SY445_SX342_.jpg'}, '14': {'nome': 'O Príncipe Cruel', 'autor': 'Holly Black', 'quantidade': 3, 'img': 'https://m.media-amazon.com/images/I/81FH6q0EqYS._SY385_.jpg'}, '15': {'nome': 'O Senhor dos Anéis- A Sociedade do Anel', 'autor': 'J.R.R. Tolkien', 'quantidade': 14, 'img': 'https://m.media-amazon.com/images/I/81MZ8OjmQrL._SY425_.jpg'}, '16': {'nome': 'Drácula', 'autor': 'Bram Stoker', 'quantidade': 32, 'img': 'https://m.media-amazon.com/images/I/71eyN+ZYvCL._SY385_.jpg'}, '17': {'nome': 'O Pequeno Príncipe', 'autor': 'Antoine de Saint-Exupéry', 'quantidade': 2, 'img': 'https://m.media-amazon.com/images/I/71FpfkjJUSL._SY385_.jpg'}, '18': {'nome': 'O Menino do Pijama Listrado', 'autor': 'John Boyne', 'quantidade': 27, 'img': 'https://m.media-amazon.com/images/I/41lCCL6N4nL._SY445_SX342_.jpg'}, '19': {'nome': 'Memórias Póstumas de Brás Cubas', 'autor': 'Machado de Assis', 'quantidade': 39, 'img': 'https://m.media-amazon.com/images/I/61Us+SweQDL._SY385_.jpg'}, '20': {'nome': 'Ai Meus Deuses', 'autor': 'Tera Lynn Childs', 'quantidade': 46, 'img': 'https://m.media-amazon.com/images/I/81hG2dbNMwL._SY385_.jpg'}, '21': {'nome': '50 Ideias de Física Quântica que Você Precisa Conhecer', 'autor': 'Joanne Baker', 'quantidade': 48, 'img': 'https://m.media-amazon.com/images/I/31k6fPZOtyL._SY445_SX342_.jpg'}, '22': {'nome': '50 Tons de Cinza', 'autor': 'E. L. James', 'quantidade': 11, 'img': 'https://m.media-amazon.com/images/I/51XHQHnyciL._SY445_SX342_.jpg'}, '23': {'nome': 'Moby Dick', 'autor': 'Herman Melville', 'quantidade': 10, 'img': 'https://m.media-amazon.com/images/I/51cQOAZhjgL._SY445_SX342_.jpg'}, '24': {'nome': 'Não Conte a Ninguém', 'autor': 'Harlan Coben', 'quantidade': 15, 'img': 'https://m.media-amazon.com/images/I/51KmwUlCluL._SY445_SX342_.jpg'}, '25': {'nome': 'Harry Potter e a Pedra Filosofal', 'autor': 'J.K. Rowling', 'quantidade': 46, 'img': 'https://m.media-amazon.com/images/I/41897yAI4LL._SY445_SX342_.jpg'}, '26': {'nome': 'As Crônicas de Nárnia', 'autor': 'C.S. Lewis', 'quantidade': 40, 'img': 'https://m.media-amazon.com/images/I/51+2QAB7I+L._SY445_SX342_.jpg'}, '27': {'nome': 'Percy Jackson e Os Olimpianos- ladrão de raios', 'autor': 'Rick Riordan', 'quantidade': 9, 'img': 'https://m.media-amazon.com/images/I/61lPJcX3j1L._SY385_.jpg'}, '28': {'nome': 'Morro dos Ventos Uivantes', 'autor': 'Emily Brontë', 'quantidade': 36, 'img': 'https://m.media-amazon.com/images/I/71lqmkoeosL._SY385_.jpg'}, '29': {'nome': 'Orgulho e Preconceito', 'autor': 'Jane Austen', 'quantidade': 29, 'img': 'https://m.media-amazon.com/images/I/717jpDhXioL._SY385_.jpg'}, '30': {'nome': 'Razão e Sensibilidade', 'autor': 'Jane Austen', 'quantidade': 24, 'img': 'https://m.media-amazon.com/images/I/81eN74IRg4L._SY385_.jpg'}, '31': {'nome': '1984', 'autor': 'George Orwell', 'quantidade': 3, 'img': 'https://m.media-amazon.com/images/I/51feD87yuEL._SY445_SX342_.jpg'}, '32': {'nome': 'Macunaíma', 'autor': 'Mário de Andrade', 'quantidade': 14, 'img': 'https://cdn.maioresemelhores.com/imagens/01-maiores-e-melhores-macunaima-cke.jpg'}, '33': {'nome': 'Grande Sertão Veredas', 'autor': 'João Guimarães Rosa', 'quantidade': 4, 'img': 'https://cdn.maioresemelhores.com/imagens/02-maiores-e-melhores-grande-sertao-cke.jpg'}, '34': {'nome': 'Dom Casmurro', 'autor': 'Machado de Assis', 'quantidade': 5, 'img': 'https://cdn.maioresemelhores.com/imagens/06-maiores-e-melhores-dom-casmurro-cke.jpg'}, '35': {'nome': 'O Cortiço', 'autor': 'Aluísio Azevedo', 'quantidade': 12, 'img': 'https://cdn.maioresemelhores.com/imagens/07-maiores-e-melhores-o-cortico-cke.jpg'}, '36': {'nome': 'Gabriela Cravo e Canela', 'autor': 'Jorge Amado', 'quantidade': 29, 'img': 'https://cdn.maioresemelhores.com/imagens/09-maiores-e-melhores-gabriela-cravo-e-canela-cke.jpg'}, '37': {'nome': 'Vidas Secas', 'autor': 'Graciliano Ramos', 'quantidade': 18, 'img': 'https://cdn.maioresemelhores.com/imagens/11-maiores-e-melhores-vidas-secas-cke.jpg'}, '38': {'nome': 'A Moreninha', 'autor': 'Joaquim Manuel de Macedo', 'quantidade': 44, 'img': 'https://cdn.maioresemelhores.com/imagens/13-maiores-e-melhores-a-moreninha-cke.jpg'}, '39': {'nome': 'Iracema', 'autor': 'José de Alencar', 'quantidade': 43, 'img': 'https://cdn.maioresemelhores.com/imagens/14-maiores-e-melhores-iracema-cke.jpg'}, '40': {'nome': 'O Ateneu', 'autor': 'Raul Pompeia', 'quantidade': 19, 'img': 'https://cdn.maioresemelhores.com/imagens/16-maiores-e-melhores-o-ateneu-cke.jpg'}, '41': {'nome': 'A Escrava Isaura', 'autor': 'Bernardo Guimarães', 'quantidade': 43, 'img': 'https://www.martinclaret.com.br/wp-content/uploads/2017/04/91xeKg8nI4L.jpg'}, '42': {'nome': 'O Guarani', 'autor': 'José de Alencar', 'quantidade': 11, 'img': 'https://cdn.maioresemelhores.com/imagens/20-maiores-e-melhores-o-guarani-cke.jpg'}, '43': {'nome': 'A divina Comédia', 'autor': 'Dante Alighieri', 'quantidade': 18, 'img': 'https://m.media-amazon.com/images/I/51SLwaM1-XL._SY445_SX342_.jpg'}, '44': {'nome': 'Dom Quixote', 'autor': 'Miguel de Cervantes', 'quantidade': 32, 'img': 'https://m.media-amazon.com/images/I/81k74t+lqyL._SY385_.jpg'}, '45': {'nome': 'Frankenstein', 'autor': 'Mary Shelley', 'quantidade': 16, 'img': 'https://m.media-amazon.com/images/I/810eLEben8L._SY385_.jpg'}, '46': {'nome': 'Os Três Mosqueteiros', 'autor': 'Alexandre Dumas', 'quantidade': 39, 'img': 'https://m.media-amazon.com/images/I/817bVkQAWhL._SY385_.jpg'}, '47': {'nome': 'Os Miseráveis', 'autor': 'Victor Hugo', 'quantidade': 33, 'img': 'https://m.media-amazon.com/images/I/51UvQ7XBImL._SY445_SX342_.jpg'}, '48': {'nome': 'O Corvo', 'autor': 'Edgar Allan Poe', 'quantidade': 6, 'img': 'https://m.media-amazon.com/images/I/515xkV5l3XL._SY445_SX342_.jpg'}, '49': {'nome': 'Madame Bovary', 'autor': 'Gustave Flaubert', 'quantidade': 17, 'img': 'https://m.media-amazon.com/images/I/41uoHb7H5vL._SY445_SX342_.jpg'}, '50': {'nome': 'Xeque-mate', 'autor': 'Ali Hazelwood', 'quantidade': 16, 'img': 'https://m.media-amazon.com/images/I/81O6eWVPaiL._SL1500_.jpg'}}"
    # test = "Teste"
    LempelZivWelch.compress(test, file_name="./compressao.pkl", print_stats=True)
    print(f'Resultado descompressão -> {LempelZivWelch.uncompress("./compressao.pkl")}')


if __name__ == "__main__":
    main()