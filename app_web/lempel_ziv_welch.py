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

        max_index_representable_in_unicode = 1114111

        #realiza a compressão
        for current_char in string:

            prefix_plus_current_char = prefix + current_char

            #checa se a nova palavra está no dicionário
            if not prefix_plus_current_char in dictionary:
                dictionary.append(prefix_plus_current_char)

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
    def decompress(file_path: str, print_variables: bool = False) -> str:
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

    print(f'Resultado descompressão -> {LempelZivWelch.decompress("./temp/catalogo.pkl")}')


if __name__ == "__main__":
    main()