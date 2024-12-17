from fractions import Fraction
import numpy as np

def is_square_matrix(matrix: np.ndarray) -> bool:
    '''
    Checks if matrix is a square matrix
    '''
    return matrix.ndim == 2 and matrix.shape[0] == matrix.shape[1]

def is_compatible_matrix(matrix_a: np.ndarray, matrix_b: np.ndarray) -> bool:
    '''
    Checks if constant matrix is compatible with coef matrix
    '''
    return matrix_b.shape[0] == 1 or matrix_b.shape[0] == matrix_a.shape[0]

def backwards_substitution(matrix: np.ndarray, size: int) -> list[str]:
    '''
    Performs backward substitution on an augmented matrix
    '''
    x = np.zeros(size)
    x[size - 1] = matrix[size - 1][size] / matrix[size - 1][size - 1]

    for i in range(size - 2, -1, -1):
        sum_ = matrix[i][size]
        for j in range(i + 1, size):
            sum_ -= (matrix[i][j] * x[j])

        x[i] = sum_ / matrix[i][i]
    msg_soln = []
    msg_soln.append("\nDecimal Form")
    for i, ans in enumerate(x):
        msg_soln.append(f"x_{i+1}: {ans}")

    ans_frac = [Fraction(i).limit_denominator() for i in x]
    msg_soln.append("\nFraction Form")

    for i, ans in enumerate(ans_frac):
        msg_soln.append(f"x_{i+1}: {ans}")

    return msg_soln

def forward_elimination(matrix_a: np.ndarray, matrix_b: np.ndarray) -> tuple[np.ndarray, list[str]]:
    '''
    Creates and modifies the augmented matrix with the upper triangle
    '''
    augmented_matrix: np.ndarray = np.concatenate((matrix_a, matrix_b), axis=1).astype(object)
    augmented_matrix = np.vectorize(Fraction)(augmented_matrix)
    msg_soln = []

    msg_soln.append("Augmented Matrix (Initial): ")
    formatted_matrix = "\n".join(["\t".join([str(entry) for entry in row]) for row in augmented_matrix])
    msg_soln.append(formatted_matrix)
    msg_soln.append(" ")

    #? Partial pivoting
    for i in range(matrix_a.shape[0]):
        max_row = i + np.argmax(abs(augmented_matrix[i:, i]))
        if max_row != i:
            augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]
            msg_soln.append(f"Swapped rows {i} and {max_row}:")
            formatted_matrix = "\n".join(["\t".join([str(entry) for entry in row]) for row in augmented_matrix])
            msg_soln.append(formatted_matrix)
            msg_soln.append(" ")

    msg_soln.append("Solution: ")

    #? Forward elimination
    for i in range(matrix_a.shape[0]):
        if augmented_matrix[i][i] == 0.0:
            msg = "0_division"
            return (None, [msg])

        for j in range(i + 1, matrix_a.shape[0]):  # Use matrix_a's row size
            scaling_factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            augmented_matrix[j] -= scaling_factor * augmented_matrix[i]

            msg_soln.append(f"Row {j+1} updated by subtracting {scaling_factor} * Row {i+1}:")
            formatted_matrix = "\n".join(["\t".join([str(entry) for entry in row]) for row in augmented_matrix])
            msg_soln.append(formatted_matrix)
            msg_soln.append(" ")

    return (augmented_matrix, msg_soln)

def gaussian_elimination(matrix_a: np.ndarray, matrix_b: np.ndarray) -> list[str]:
    '''
    Main Function for Gaussian elimination program
    '''

    #! Error: Coefficient matrix is not square.
    if not is_square_matrix(matrix_a):
        return None

    #! Error: Constant matrix is not compatible with coefficient matrix.
    if not is_compatible_matrix(matrix_a, matrix_b):
        return None

    msg_soln = []
    aug_matrix, soln1 = forward_elimination(matrix_a, matrix_b)
    msg_soln.extend(soln1)

    if aug_matrix is None:
        return msg_soln

    answers = backwards_substitution(aug_matrix, aug_matrix.shape[1] - 1)
    msg_soln.extend(answers)


    return msg_soln
