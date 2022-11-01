import random
import typing


# Constant values to modify the settings of the randomly generated matrix (set number of columns and rows, set min and max value limits)
MATRIX_COLUMNS: int = 5 
MATRIX_ROWS: int = 7 
MAX_NUMBER_VALUE: int = 9 
MIN_NUMBER_VALUE: int = -9

# This constant value is 'deactivated' when set to None.
# If the value is changed, the new value will be used as the matrix for the program
SPECIFIC_MATRIX: typing.Optional[list[list[int]]] = None 


def process_matrix(matrix: list[list[int]]) -> list[list[int]]:
    '''
    Processes a matrix, creating a new one. Every element in the new matrix is the result 
    of the average between it and the values on its 4 sides.
    '''
    new_matrix = []
    for i, column in enumerate(matrix):
        new_column = []
        for j in range((len(column))): 
            new_column.append(process_element(i, j, matrix))
        new_matrix.append(new_column)

    return new_matrix

    """
    # Alternatives

    # 1: List comprehensions
    return [[process_element(i, j, matrix) for j in range((len(column)))] for i, column in enumerate(matrix)]

    # 2: Map
    return map(lambda i: map(lambda j: process_element(i, j, matrix), range(len(matrix[i]))), range(len(matrix)))
    """


def process_element(i: int, j: int , matrix: list[list[int]]) -> float:
    '''
    Processes an element and calculates the average between the element and its 4 side values.
    '''
    neighbours = get_neighbours(i, j, matrix)
    neighbours.append(matrix[i][j]) 
    average = sum(neighbours) / len(neighbours)

    return average


def get_neighbours(i: int, j: int , matrix: list[list[int]]) -> list[int]:
    '''
    Gets all side values from an element within a matrix and returns them inside a list.
    '''
    neighbours = []

    if i > 0: 
        neighbours.append(matrix[i - 1][j]) 

    if i < len(matrix) - 1: 
        neighbours.append(matrix[i + 1][j]) 

    if j > 0:  
        neighbours.append(matrix[i][j - 1]) 

    if j < len(matrix[0]) - 1:  
        neighbours.append(matrix[i][j + 1]) 

    return neighbours


def generate_matrix(columns: int, rows: int, min_value: int, max_value: int) -> list[list[int]]:
    '''
    Returns a randomly generated matrix
    '''
    if columns <= 0:
        columns = 1
    if rows < 0:
        rows = 0

    new_matrix = []
    for column in range(columns):
        new_column = []
        for element in range(rows):
            new_column.append(random.randint(min_value, max_value))
        new_matrix.append(new_column)

    return new_matrix

    """
    # Alternatives

    # 1: List comprehensions
    return [[random.randint(min_value, max_value) for element in range(rows)] for i in range(columns)]

    # 2: Map
    return map(lambda _: map(lambda _: random.randint(min_value, max_value), range(rows)), range(columns))
    """


def generate_operations_matrix(matrix: list[list[int]]) -> list[list[int]]:
    '''
    Generates a new matrix with the math operations that take place between side elements.
    Formulates the operation as a string.
    '''

    new_matrix = []
    for i, column in enumerate(matrix):
        new_list = []
        for j in range(len(column)):
            neighbours = get_neighbours(i, j, matrix)
            neighbours.append(matrix[i][j])
          
            summation = ""
            for number in neighbours:
                summation += f"{str(number)} + "

            operation = f"({summation[:-3]}) / {len(neighbours)}"
            operation = f"{operation:30}" 

            new_list.append(operation)
        new_matrix.append(new_list)

    return new_matrix


def display_matrix(matrix: list[list]) -> None:
    '''
    Displays a matrix on the console
    '''
    matrix_text = ""
    for row in range(len(matrix) - (len(matrix) - len(matrix[0]))): 
        new_line = ""
        for element in range(len(matrix[0]) - (len(matrix[0]) - len(matrix))):
            value = matrix[element][row]

            if type(value) == float:
                value = round(value, 2)

            new_line += f"{str(value):>10}"    
        matrix_text = f"\n{new_line}\n{matrix_text}" 

    print(matrix_text)


import pandas as pd
def display_matrix_pandas(matrix: list[list[int]]) -> None:
    '''
    Displays a matrix as a pandas dataframe.
    '''

    new_matrix = []

    for row in range(len(matrix) - (len(matrix) - len(matrix[0]))):
        new_line = []
        for element in range(len(matrix[0]) - (len(matrix[0]) - len(matrix))):

            value = matrix[element][row]
            if type(value) == float:
                value = round(value, 2)

            new_line.append(value) 
        new_matrix.insert(0, new_line)
    matrix_df = pd.DataFrame(new_matrix)
    
    print(f"\n{matrix_df.to_markdown()}") 


def is_valid_matrix(matrix: list[list[int]]) -> bool:
    valid = True

    if len(matrix) == 0:
        valid = False
    
    column_length = len(matrix[0]) 

    for column in matrix:
        if len(column) != column_length:
            valid = False
            break

        for element in column:
            if type(element) != int and type(element) != float:
                valid = False
                break

    return valid


def complete_execution(display_function, specific_matrix: typing.Optional[list[list[int]]] = None) -> None:
    '''
    Generates a random matrix, displays it; generates an operations matrix and displays it, too; and processes matrix and displays it.
    '''
    if specific_matrix != None:
        matrix = specific_matrix

        if not is_valid_matrix(matrix):
            raise ValueError(
            "\n\tThe introduced matrix is invalid." +
            "\n\tPlease check that the specific_matrix arguments is a valid matrix (at least one column, columns have the same height, and the values inside are only ints or floats)." +
            "\n\tIf you don't want to input a specific matrix, please leave that argument as None")
    else:
        matrix = generate_matrix(MATRIX_COLUMNS, MATRIX_ROWS, MIN_NUMBER_VALUE, MAX_NUMBER_VALUE)
    
    display_function(matrix)
    display_function(generate_operations_matrix(matrix))
    display_function(process_matrix(matrix))
    

if __name__ == "__main__":

    print("\nIn order to change the matrix size or the range of random numbers, change the constant variables at the top of this file.")

    if SPECIFIC_MATRIX != None:
        complete_execution(display_matrix, SPECIFIC_MATRIX)
    else:
        while True:
            response = input("\nDo you want to generate and process a random matrix? (Y/P/N)\n\tY: Yes\n\tP: Yes, but using pandas and tabulate to display it\n\tN: No, stop the execution\n").strip().upper()

            if response == "Y":
                complete_execution(display_matrix, SPECIFIC_MATRIX)
            elif response == "P":
                complete_execution(display_matrix_pandas, SPECIFIC_MATRIX)
            else:
                print("\nThanks for using my program")
                break
