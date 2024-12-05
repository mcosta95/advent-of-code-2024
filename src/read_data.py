import pandas as pd

def read_txt_to_df(file_name, col_names):
    return pd.read_csv(file_name, sep='\s+', header=None, names=col_names)

def read_txt_vector_matrix(file_name):
    with open(file_name, 'r') as file:
        data = [list(map(int, line.split())) for line in file]
    return data

def read_txt_vector_matrix_str(file_name):
    with open(file_name, 'r') as file:
        data = [list(line.strip()) for line in file]
    return data

def read_txt_to_str(file_name, with_split=None):
    with open(file_name, "r") as file:
        data = file.read()
    if with_split:
        data = data.split(with_split)
    return data