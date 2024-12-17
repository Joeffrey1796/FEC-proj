import tkinter as tk
import os
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageTk
import gaussian_elimination as ge


def fraction_to_float(fraction_str: str) -> np.float64:
    '''
    Converts a string representing a fraction (e.g., "3/4") into a float64 value.
    '''
    numerator, denominator = fraction_str.split('/')
    return np.float64(int(numerator) / int(denominator))


def is_valid_input(input_str: str) -> bool:
    '''
    Validates whether the input string is a valid number, fraction, or empty.
    '''

    if input_str[0:2] == 'A[':
        return True
    elif input_str[0:2] == 'B[':
        return True
    elif input_str == "":
        return True
    elif input_str == '-':
        return True
    elif '/' in input_str:
        if input_str.count('/') == 1:
            return True
        else:
            return False
    try:
        float(input_str)
        return True
    except ValueError:
        return False


def scrollable(master_root: tk.Tk, width: int, height: int, row: int, column: int,) -> tk.Frame:
    '''
    Creates a scrollable frame within a tkinter window with both vertical and horizontal scrolling.
    '''
    def adjust_frame_size(event: tk.Event) -> None:
        canvas.configure(scrollregion=(0, 0, event.width, event.height))

    def on_mouse_wheel(event: tk.Event) -> None:
        if event.state & 0x0001:
            canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas = tk.Canvas(master_root, width=width, height=height, bg="#1e1e1e",
                       highlightthickness=0)
    v_scroll = tk.Scrollbar(master_root, orient=tk.VERTICAL, command=canvas.yview,
                            bg="#333333", troughcolor="#1e1e1e")
    h_scroll = tk.Scrollbar(master_root, orient=tk.HORIZONTAL, command=canvas.xview,
                            bg="#333333", troughcolor="#1e1e1e")

    canvas.grid(row=row, column=column, sticky="nsew", columnspan=2)
    v_scroll.grid(row=row + 1, column=column + 1, sticky="ns")
    h_scroll.grid(row=row + 1, column=column, sticky="ew")

    v_scroll.grid_remove()
    h_scroll.grid_remove()

    canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    scrollable_frame = tk.Frame(master=canvas, bg="#1e1e1e")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind("<Configure>", adjust_frame_size)
    canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", on_mouse_wheel))
    canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))

    return scrollable_frame



def create_placeholder_entry(parent: tk.Widget, row: int, column: int, placeholder_text: str,
                             color: str = "gray", **kwargs) -> tk.Entry:
    '''
    Creates a tkinter Entry widget with a placeholder text and custom styling.
    '''
    def on_focus_in(event: tk.Event, placeholder_text: str) -> None:
        '''
        Clears the placeholder text when the user clicks into the entry field.
        '''
        entry = event.widget
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg="white")

    def on_focus_out(event: tk.Event, placeholder_text: str) -> None:
        '''
        Restores the placeholder text if the user leaves the entry field without typing anything.
        '''
        entry = event.widget
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg="lightgreen")

    entry = tk.Entry(parent, bg="#2e2e2e", fg=color, font=("Helvetica", 12),
                     insertbackground="white", **kwargs)
    entry.grid(row=row, column=column, padx=5, pady=5)

    entry.insert(0, placeholder_text)  # Insert the placeholder text initially
    entry.config(fg="lightgreen")  # Set the placeholder text color to gray

    # Bind events to clear placeholder text on focus in and restore it on focus out
    entry.bind("<FocusIn>", lambda e: on_focus_in(e, placeholder_text))
    entry.bind("<FocusOut>", lambda e: on_focus_out(e, placeholder_text))

    return entry


def generate_matrix_widgets(matrix_size_entry: tk.Entry, matrix_frame: tk.Frame,
                            constant_frame: tk.Frame,
                            validate_command: callable) -> None:
    '''
    Generates matrix input fields based on the matrix size entered by the user.
    Clears old widgets before adding new ones.
    '''
    for widget in matrix_frame.winfo_children():
        widget.destroy()

    for widget in constant_frame.winfo_children():
        widget.destroy()

    matrix_entries.clear()
    constant_entries.clear()

    try:
        n = int(matrix_size_entry.get())
    except ValueError:
        return None

    if n <= 0:
        return None

    for i in range(n):
        row_entries = []
        for j in range(n):
            placeholder_text = f"A[{i + 1},{j + 1}]"

            entry = create_placeholder_entry(matrix_frame, i, j, placeholder_text=placeholder_text,
                                             width=10,validate="key",
                                             validatecommand=(validate_command,"%P"))
            row_entries.append(entry)
        matrix_entries.append(row_entries)

    for i in range(n):
        placeholder_text = f"B[{i + 1}]"
        entry = create_placeholder_entry(constant_frame, i, 0, placeholder_text=placeholder_text,
                                         width=10,validate="key",validatecommand=(validate_command,"%P"))
        constant_entries.append(entry)


def solve() -> None:
    '''
    Solves the system of linear equations using Gaussian elimination.
    Displays the result in a new window.
    '''
    try:
        matrix = np.array([
            [fraction_to_float(entry.get()) if '/' in entry.get() else np.float64(entry.get() or 0)
             for entry in row]
            for row in matrix_entries
        ])

        constants = np.array([
            [fraction_to_float(entry.get()) if '/' in entry.get() else np.float64(entry.get() or 0)]
            for entry in constant_entries
        ])
        constants.reshape(-1, 1)
    except Exception:
        pass

    try:
        soln = ge.gaussian_elimination(matrix, constants)
        if "0_division" in soln:
            messagebox.showerror("Error", "Error: ZeroDivisionError due to zero pivot.")
        else:
            solution_window = tk.Toplevel(bg="#1e1e1e")
            solution_window.title("Solution")
            solution_window.minsize(200, 150)
            solution_window.geometry("450x800")
            change_title_bar_color(solution_window, "blue",0.85)

            c_frame = scrollable(solution_window, 600, 800, 0, 0)

            for i in soln:
                soln_label = tk.Label(c_frame, text=i, fg="white", bg="#1e1e1e",
                                      font=("Helvetica", 12))
                soln_label.pack(padx=10, pady=20, anchor="w",side="top")
    except Exception as e:
        msg = f"Error: {e}"
        messagebox.showerror("Error", msg)


matrix_entries: list[list[tk.Entry]] = []
constant_entries: list[tk.Entry] = []

def change_title_bar_color(root, color, opacity):
    """
    Changes the color of the title bar in a tkinter window.

    Args:
    root: The tkinter root window object.
    color: The desired color for the title bar (e.g., 'blue', '#FF0000').
    """
    try:
        root.wm_attributes('-topmost', 1) 
        root.wm_attributes('-transparentcolor', color)
        root.wm_attributes('-alpha', opacity)
    except tk.TclError:
        print(f"Changing title bar color to '{color}' is not supported on this system.")


def main() -> None:
    '''
    Initializes and runs the tkinter main window for the Gaussian elimination application.
    '''
    def go_to_main2():
        '''
        Page 2 of Main Function 
        '''
        proceed_button.grid_forget()
        validate_command = root.register(is_valid_input)

        change_title_bar_color(root, "blue",0.85)
        matrix_size_label = tk.Label(root, text="Enter matrix size (n x n):", fg="white",
                                     bg="#1e1e1e",font=("Helvetica", 12))
        matrix_size_label.grid(row=0, column=0, padx=10, pady=(50, 10), sticky="ew")

        matrix_size_entry = tk.Entry(root, width=10, validate="key",
                                    validatecommand=(validate_command, "%P"),
                                    bg="#2e2e2e", fg="white", font=("Helvetica", 12),
                                    insertbackground="white")
        matrix_size_entry.grid(row=0, column=1, padx=10, pady=(50, 10), sticky="ew")

        update_button = tk.Button(root, text="Generate Matrix",
                                command=lambda: generate_matrix_widgets(matrix_size_entry,
                                                                        matrix_frame,
                                                                        constant_frame,
                                                                        validate_command),
                                fg="white", bg="#333333", font=("Helvetica", 12))
        update_button.grid(row=1, column=0, columnspan=2, pady=10)

        extract_button = tk.Button(root, text="Gaussian Elimination", command=solve, fg="white",
                                    bg="#333333", font=("Helvetica", 12))
        extract_button.grid(row=4, column=0, columnspan=2, pady=30)

        matrix_canvas = scrollable(root, 600, 200, 2, 0)
        matrix_frame = tk.Frame(matrix_canvas, bg="#1e1e1e")
        matrix_frame.grid(row=2, column=0, padx=10, pady=10)

        constant_frame = tk.Frame(matrix_canvas, bg="#1e1e1e")
        constant_frame.grid(row=2, column=1, padx=10, pady=10)

    root = tk.Tk()
    change_title_bar_color(root, "blue",1)
    basedir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(basedir, "Source","Gaussian_Elimination_Logo.ico")
    image_path = os.path.join(basedir, "Source", "Gaussian_Elimination_Logo.png")
    root.iconbitmap(icon_path)
    root.resizable(False, False)
    root.title("Gaussian Elimination")
    root.geometry("600x500")
    root.config(bg="#1e1e1e")

    try:
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        proceed_button = tk.Button(root, image=photo, command=go_to_main2)
        proceed_button.grid(row=0, column=0, sticky="nsew")
    except FileNotFoundError:
        print("Error: Image file not found. Using default button.")
        proceed_button = tk.Button(root, text="Start", command=go_to_main2)
        proceed_button.grid(row=0, column=0, sticky="nsew")

    root.mainloop()

if __name__ == "__main__":
    main()
