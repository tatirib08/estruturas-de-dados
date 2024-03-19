import pandas as pd
import numpy as np 
import datetime 
# print(pd.__version__) 


def main():
    
    salaries_data = pd.read_csv("salarios/salaries.csv")
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    # print(salaries_data.to_string())
    
    work_year = salaries_data.iloc[:,[0]]
    experience_level = salaries_data.iloc[:,[1]]
    employment_type = salaries_data.iloc[:,[2]]
    job_title = salaries_data.iloc[:,[3]]
    salary = salaries_data.iloc[:,[4]]
    salary_currency = salaries_data.iloc[:,[5]]
    salary_in_usd = salaries_data.iloc[:,[6]]
    employee_residence = salaries_data.iloc[:,[7]]
    remote_ratio = salaries_data.iloc[:,[8]]
    company_location = salaries_data.iloc[:,[9]]
    company_size = salaries_data.iloc[:,[10]]
    
    # print(salaries_data.iloc[:,[2]])

    #ordenar crescente 
    ordem_crescente = salaries_data.sort_values(by=4, axis=1, ascending=True)
    print(ordem_crescente)


if __name__ == '__main__':
    main()
