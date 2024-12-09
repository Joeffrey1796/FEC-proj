from fractions import Fraction
import numpy as np

def x():
    pass

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

    return (x, str(x))


def forward_elimination(matrix_a:np.ndarray, matrix_b:np.ndarray) -> tuple[np.ndarray, list[str]] :
    '''Creates and modifies the augmented matrix with the upper triangle'''

    augmented_matrix: np.ndarray = np.concatenate((matrix_a, matrix_b), axis=1).astype(float)
    msg_soln = []
    #? Debugging: show augemented matrix
    msg_soln.append("Augemented Matrix (Initial): ")
    msg_soln.append(f"{augmented_matrix}")
    msg_soln.append(" ")



    #* partial pivot
    for i in range(matrix_b.size):

        max_row = i + np.argmax(abs(augmented_matrix[i:, i]))
        if max_row != i:

            augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]
            msg_soln.append(f"Swapped rows {i} and {max_row}:")
            msg_soln.append(f"{augmented_matrix}")
            msg_soln.append(" ")

    msg_soln.append("Solution: ")


    for i in range(matrix_b.size):

        #! 0 on pivot points (unsolvable)
        if augmented_matrix[i][i] == 0.0:
            print("error: ZeroDivisionError")
            return None


        #? formula R_j = R_j - (scaling factor * R_i)
        for j in range(i+1, matrix_b.size):
            scaling_factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            augmented_matrix[j] -= (scaling_factor * augmented_matrix[i])


            #? Debugging: show augmented matrix
            # print(f"{i}, {j}, {augmented_matrix[j][i]}, {augmented_matrix[i][i]}, {scaling_factor}")
            # print(f"Scaling factor: {scaling_factor}")
            msg_soln.append(f"{augmented_matrix}")
            msg_soln.append(" ")

        #? Debugging: show augmented matrix
        msg_soln.append(f"{augmented_matrix}")
        msg_soln.append(" ")

    return (augmented_matrix, msg_soln)

def gaussian_elimination(matrix_a:np.ndarray, matrix_b:np.ndarray) -> list[str]:
    '''
    Main Function for Gaussian elimination program
    '''

    #! coef matrix is not square
    if not is_square_matrix(matrix_a):
        return

    #! constant matrix is not compatible with coef matrix
    if not is_compatible_matrix(matrix_a,matrix_b):
        return
    msg_soln = []
    aug_matrix, soln1 = forward_elimination(matrix_a,matrix_b)
    # for i in msg_soln:
    #     print(i)
    msg_soln.extend(soln1)
    answers, soln2 = backwards_substitution(aug_matrix,aug_matrix.shape[1] - 1)
    msg_soln.append(soln2)

    ans_frac = [Fraction(x).limit_denominator() for x in answers]

    msg_soln.append(str(ans_frac))

    for i in msg_soln:
        print(i)
    # print(answers)
    # print(ans_frac)

    return msg_soln


def main() -> None:
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

    # a = np.array([[Fraction(3,20),Fraction(-1,8)],
    #               [Fraction(-1,8),Fraction(7,48)]])
    # b = np.array([[Fraction(6,1)],
    #               [Fraction(-1,1)]])
    a = np.array([[0,5,10],
                  [45,0,4],
                  [10,4,0]])
    b = np.array([[130],
                  [106],
                  [0]])
    # a = np.array([[1]])
    # b = np.array([[2]])
    gaussian_elimination(a,b)
    return None

if __name__ == "__main__":
    main()