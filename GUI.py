import tkinter as tk
import numpy as np
import gaussian_elimination as ge


#todo: PEP-8
#todo: solution window
#todo: debug

def test(x)-> None:
    #? Test function for validate_command param
    pass

def generate_matrix_widgets(matrix_size_entry, matrix_frame, constant_frame, validate_command):


    for widget in matrix_frame.winfo_children():
        widget.destroy()
    
    for widget in constant_frame.winfo_children():
        widget.destroy()

    matrix_entries.clear()
    constant_entries.clear()

    try:
        n = int(matrix_size_entry.get())
    except ValueError:
        return
    
    if n <= 0:
        return

    for i in range(n):
        row_entries = []
        for j in range(n):
            entry = tk.Entry(matrix_frame, width=10, validate="key",
                             validatecommand=(validate_command, "%P")
                            )
            entry.grid(row=i, column=j, padx=5, pady=5)
            row_entries.append(entry)
        matrix_entries.append(row_entries)

    for i in range(n):
        entry = tk.Entry(constant_frame, width=10, validate="key",
                         validatecommand=(validate_command, "%P")
        )
        entry.grid(row=i, column=0, padx=5, pady=5)
        constant_entries.append(entry)

def is_valid_input(input_str):
    """Validate that the input is a digit or empty."""
    if input_str == "":
        return True
    if input_str == '-':
        return True
    try:
        float(input_str)
        return True
    except ValueError:
        return False

def solve():
    """
    Extract the matrix and constants into numpy arrays.
    """

    try:
        matrix = np.array([
            [float(entry.get() or 0) for entry in row]
            for row in matrix_entries
        ])
        constants = np.array([
            [float(entry.get() or 0)] for entry in constant_entries
        ])
        constants.reshape(-1,1)
        print("Matrix:\n", matrix)
        print("Constants:\n", constants)
    except ValueError:
        print("Invalid input detected! Ensure all fields are filled with numbers.")

    solution_window = tk.Toplevel()
    # solution_window.geometry("200x150") 
    solution_window.title("Solution")
    solution_window.resizable(True, True)
    solution_window.minsize(200, 150)

    # close_btn = tk.Button(solution_window, text="Close window", command=solution_window.destroy)
    # close_btn.pack()

    try:
        soln = ge.gaussian_elimination(matrix, constants)
        msg = "\n".join(soln)
    except Exception as e:
        msg = f"Error: {e}"
        print(f"error: {e}")

    soln = tk.Label(solution_window, text=msg)
    soln.pack(padx=10,pady=10)

#todo
matrix_entries = []
constant_entries = []
matrix = []
constants = []

def main() -> None:
    root = tk.Tk()
    root.title("Gaussian Elimination")

    validate_command = root.register(is_valid_input)

    matrix_size_label = tk.Label(root, text="Enter matrix size (n x n):")
    matrix_size_label.grid(row=0, column=0, padx=10, pady=10)

    matrix_size_entry = tk.Entry(root, width=10, validate="key",
                                validatecommand=(validate_command, "%P")
                                )
    matrix_size_entry.grid(row=0, column=1, padx=10, pady=10)


    update_button = tk.Button(root, text="Generate Matrix", command=lambda: generate_matrix_widgets(matrix_size_entry, matrix_frame, constant_frame, validate_command))
    update_button.grid(row=1, column=0, columnspan=2, pady=10)

    extract_button = tk.Button(
        root, text="Solve Matrix",
        command=solve
    )
    extract_button.grid(row=3, column=0, columnspan=2, pady=10)


    matrix_frame = tk.Frame(root)
    matrix_frame.grid(row=2, column=0, padx=10, pady=10)

    constant_frame = tk.Frame(root)
    constant_frame.grid(row=2, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()