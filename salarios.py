import pandas as pd
import numpy as np  
import time 
from datetime import datetime 

def main():
    
    #lendo apenas a coluna desejada do arquivo 
    df = pd.read_csv("/home/tati/ed2/salarios/salaries.csv", usecols=['salary'])
    salaries_data = pd.DataFrame(df)
    pd.set_option("display.max_rows", 3000, "display.max_columns", None)
    print("\n------DESORDENADO------\n")
    print(salaries_data)

    # print(salaries_data.to_string())

    # salary = salaries_data.iloc[:,[4]]

    start_time = time.time()
    # start_time = datetime.now()
    #ordenar crescente quick_sort
    ordem_crescenteQS = salaries_data.sort_values(by='salary', ascending=True, kind="quicksort")
    cresQStime = time.time() - start_time
    print("\n-----CRESCENTE QS------\n")
    print(ordem_crescenteQS)
    

    #ordenar decrescente quick_sort 
    ordem_decrescenteQS = salaries_data.sort_values(by='salary', ascending=False, kind="quicksort")
    decresQStime = time.time() - start_time
    print("\n------ DECRESCENTE QS-------\n")
    print(ordem_decrescenteQS)
    

    #ordem inversa QS
    ordem_inversaQS = ordem_crescenteQS.sort_values(by='salary', ascending=False, kind="quicksort")
    inversaQStime = time.time() - start_time
    print("\n ----ORDEM INVERSA QS------\n")
    print(ordem_inversaQS)

    #ordenar crescente merge_sort
    ordem_crescenteMS = salaries_data.sort_values(by='salary', ascending=True, kind="mergesort")
    print("\n------ CRESCENTE MS-------\n")
    print(ordem_crescenteMS)
    cresMStime = time.time() - start_time

    # ordenar decrescente merge_sort
    ordem_decrescenteMS = salaries_data.sort_values(by='salary', ascending=False, kind="mergesort")
    print("\n------ DECRESCENTE MS-------\n")
    print(ordem_decrescenteMS)
    decresMStime = time.time() - start_time

    # ordem inversa merge sort
    ordem_inversaMS = ordem_crescenteMS.sort_values(by='salary', ascending=False, kind="mergesort")
    inversaMStime = time.time() - start_time 
    print("\n ----ORDEM INVERSA MS------\n")
    print(ordem_inversaMS)

    #ordenar crescente heap_sort
    ordem_crescenteHS = salaries_data.sort_values(by='salary', ascending=True, kind="heapsort")
    print("\n------ CRESCENTE HS-------\n")
    print(ordem_crescenteHS)
    crescHStime = time.time() - start_time

    #ordenar decrescente heap_sort
    ordem_decrescenteHS = salaries_data.sort_values(by='salary', ascending=False, kind="heapsort")
    print("\n------ DECRESCENTE HS-------\n")
    print(ordem_decrescenteHS)
    decresHStime = time.time() - start_time

    # ordem inversa heap_sort
    ordem_inversaHS = ordem_crescenteHS.sort_values(by='salary', ascending=False, kind="heapsort")
    inversaHStime = time.time() - start_time 
    print("\n ----ORDEM INVERSA HS------\n")
    print(ordem_inversaHS)

    print(f"Quick sort tempo para ordem crescente: {cresQStime}")
    print(f"Quick Sort tempo para ordem decrescente: {decresQStime}")
    print(f"Quick Sort tempo para ordem inversa (cresc -> decres): {inversaQStime}")
    print(f"Merge Sort tempo para ordem crescente: {cresMStime}")
    print(f"Merge Sort tempo para ordem decrescente: {decresMStime}")
    print(f"Merge Sort tempo para ordem inversa (cresc -> decres): {inversaMStime}")
    print(f"Heap Sort tempo para ordem crescente: {crescHStime}")
    print(f"Heap Sort tempo para ordem decrescente: {decresHStime}")
    print(f"Heap Sort tempo para ordem inversa (cresc -> decres): {inversaHStime}")

if __name__ == '__main__':
    main()
