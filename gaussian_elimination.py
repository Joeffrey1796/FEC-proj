import numpy as np


def is_square_matrix(matrix:np.ndarray) -> bool:
    '''Checks if matrix is a square matrix'''
    return matrix.ndim == 2 and matrix.shape[0] == matrix.shape[1]

def is_compatible_matrix(matrix_a:np.ndarray,matrix_b) -> bool:
    '''Checks if constant matrix is compatible to coef matrix'''
    return matrix_b.shape[0] == 1 or matrix_b.shape[0] == matrix_a.shape[0]

def backwards_substitution(matrix:np.ndarray,size) -> np.ndarray:
    '''Performs backwards subsitution on an augmented matrix'''
    x = np.zeros(size)

    #* Grab the last unknown
    x[size - 1] = matrix[size - 1][size] / matrix[size - 1][size - 1]

    for i in range(size-2,-1,-1):
        sum_ = matrix[i][size]
        for j in range(i + 1,size):
            sum_ -= (matrix[i][j] * x[j])

        x[i] = sum_ / matrix[i][i]

    return x


def forward_elimination(matrix_a:np.ndarray, matrix_b:np.ndarray) -> np.ndarray:
    '''Creates and modifies the augmented matrix with the upper triangle'''

    augmented_matrix: np.ndarray = np.concatenate((matrix_a, matrix_b), axis=1).astype(float)

    #? Debugging: show augemented matrix
    print(augmented_matrix)
    print()

    for i in range(matrix_b.size):
        #! 0 on pivot points
        #todo: partial pivot
        if augmented_matrix[i][i] == 0.0:
            raise ZeroDivisionError


        #? formula R_j = R_j - (scaling factor * R_i)
        for j in range(i+1, matrix_b.size):
            scaling_factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            augmented_matrix[j] -= (scaling_factor * augmented_matrix[i])


            #? Debugging: show augmented matrix
            # print(f"{i}, {j}, {augmented_matrix[j][i]}, {augmented_matrix[i][i]}, {scaling_factor}")
            print(augmented_matrix)
            print()

        #? Debugging: show augmented matrix
        print()
        print(augmented_matrix)

    return augmented_matrix

def gaussian_elimination(matrix_a:np.ndarray, matrix_b:np.ndarray) -> None:
    '''
    Main Function for Gaussian elimination program
    '''

    #! coef matrix is not square
    if not is_square_matrix(matrix_a):
        return

    #! constant matrix is not compatible with coef matrix
    if not is_compatible_matrix(matrix_a,matrix_b):
        return

    aug_matrix = forward_elimination(matrix_a,matrix_b)
    answers = backwards_substitution(aug_matrix,aug_matrix.shape[1] - 1)

    print(answers)

    return None


#? TEST CASES
# a = np.array([[1,1,3,1],
#               [0,1,3,4],
#               [-1,3,0,2],
#               [8,1,4,2]])
# b = np.array([[1],
#               [3],
#               [5],
#               [4]])
# c = np.array([[10,11,12],
#               [13,14,15],
#               [16,17,45]])
# d = np.array([[3],
#              [5],
#              [1]])

# gaussian_elimination(c,d)
