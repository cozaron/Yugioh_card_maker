from tkinter import messagebox
import datetime

from tkinter import filedialog

import YDK
import Make_card
import image_operations

import tkinter as tk
from tkinter import ttk


def save_input():
    input_value = input_entry.get()
    # check if input value is an integer and less than 10 characters
    if input_value.isdigit() and len(input_value) <= 10:

        card_temp = Make_card.make_card(input_value)
        image_operations.save_image_png(card_temp, input_value)
        print("Input saved successfully")


    else:
        print("Invalid input")


def execute_code(start_date, end_date):
    print(start_date)
    print(end_date)
    print(Make_card.reformat_date(start_date))
    print(Make_card.reformat_date(end_date))
    start_date = Make_card.reformat_date(start_date)
    end_date = Make_card.reformat_date(end_date)
    Make_card.make_card_date(start_date, end_date)

    pass


def save_dates(get, get1):
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    try:
        start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y')
        end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y')
    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid date format. Please enter dates in the format MM/DD/YYYY")
        return
    execute_code(start_date, end_date)


def save_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        cards = YDK.open_ydk(f'{file_path}')
        for card in cards:
            card_temp = Make_card.make_card(card)
            image_operations.save_image_png(card_temp, "Anime_cards", card)
            print("Input saved successfully")


root = tk.Tk()
root.title("Yu gi oh anime card maker")
root.geometry("400x250")

style = ttk.Style()
style.configure("TButton", background="white", foreground="grey", font=("TkDefaultFont", 12), borderwidth=2,
                relief="solid")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=1)

# First section
section_one = ttk.Frame(notebook)
notebook.add(section_one, text="with ID")

#section_one_label = tk.Label(section_one, text="This is Section 1", font=("TkDefaultFont", 14), foreground="grey")
#section_one_label.pack(pady=10)

# Create a label and an entry widget to take user input
input_label = ttk.Label(section_one, text="Enter an integer (less than 10 characters):")
input_label.pack(pady=(10, 0))

input_entry = ttk.Entry(section_one, width=35)
input_entry.pack(pady=(10, 0))

# Create a button to save the input value
save_button = ttk.Button(section_one, text="Save", command=save_input)
save_button.pack(pady=(20, 0))




# Second section

section_two = ttk.Frame(notebook)
notebook.add(section_two, text="With Date")

#section_two_label = tk.Label(section_two, text="This is Section 2", font=("TkDefaultFont", 14), foreground="grey")
#section_two_label.pack(pady=10)

# Frame to hold the labels, entry fields, and button
section_two_frame = ttk.Frame(section_two)
section_two_frame.pack(padx=10, pady=10)

# Start date label and entry field
start_date_label = ttk.Label(section_two_frame, text="Start Date (MM/DD/YYYY):")
start_date_label.grid(row=0, column=0, padx=10, pady=10)

start_date_entry = ttk.Entry(section_two_frame)
start_date_entry.grid(row=0, column=1, padx=10, pady=10)

# End date label and entry field
end_date_label = ttk.Label(section_two_frame, text="End Date (MM/DD/YYYY):")
end_date_label.grid(row=1, column=0, padx=10, pady=10)

end_date_entry = ttk.Entry(section_two_frame)
end_date_entry.grid(row=1, column=1, padx=10, pady=10)

# Save button
save_button = ttk.Button(section_two_frame, text="Save",command=lambda: save_dates(start_date_entry.get(), end_date_entry.get()))
save_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")




# Third section
section_three = ttk.Frame(notebook)
notebook.add(section_three, text="with YDK")

# Create a new frame for the file browser section
file_browser_frame = ttk.Frame(section_three)
file_browser_frame.pack(pady=10)

# Create labels and button for the file browser section
file_label = tk.Label(file_browser_frame, text="Import your ydk or txt file", font=("TkDefaultFont", 14), foreground="grey")
file_label.pack(side=tk.LEFT, padx=10)

browse_button = ttk.Button(file_browser_frame, text="Browse", command=save_file)
browse_button.pack(side=tk.LEFT)

root.mainloop()



"""# section 01 ---------------------------------------------------------------------------------------------------------
root = tk.Tk()
root.title("Input Box")
root.geometry("400x150")

style = ttk.Style()
style.configure("TButton", background="white", foreground="grey", font=("TkDefaultFont", 12), relief="solid",
                borderwidth=1)
style.configure("TLabel", background="white", foreground="grey", font=("TkDefaultFont", 12))

input_label = ttk.Label(root, text="Enter an integer (less than 10 characters):")
input_label.pack(pady=(10, 0))

input_entry = ttk.Entry(root, width=35)
input_entry.pack(pady=(10, 0))

save_button = ttk.Button(root, text="Save", command=save_input)
save_button.pack(pady=(20, 0))

# section two-----------------------------------------------------------------------------------------------------------
root = tk.Tk()
root.title("Section Two")
root.geometry("400x150")

style = ttk.Style()
style.configure("TButton", background="white", foreground="grey", font=("TkDefaultFont", 12), relief="solid",
                borderwidth=1)
style.configure("TLabel", background="white", foreground="grey", font=("TkDefaultFont", 12))

start_date_label = ttk.Label(root, text="Start Date (YYYY-MM-DD)")
start_date_label.grid(row=0, column=0, padx=10, pady=10)

start_date_entry = ttk.Entry(root)
start_date_entry.grid(row=0, column=1, padx=10, pady=10)

end_date_label = ttk.Label(root, text="End Date (YYYY-MM-DD)")
end_date_label.grid(row=1, column=0, padx=10, pady=10)

end_date_entry = ttk.Entry(root)
end_date_entry.grid(row=1, column=1, padx=10, pady=10)

save_button = ttk.Button(root, text="Save", command=save_dates)
save_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

# section 3 ----------------------------------------------------------------------------------------------------------

def save_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        cards = YDK.open_ydk(f'{file_path}')
        for card in cards:
            card_temp = Make_card.make_card(card)
            image_operations.save_image_png(card_temp, "Anime_cards", card)
            print("Input saved successfully")

root = tk.Tk()
root.title("File Browser")
root.geometry("400x100")

style = ttk.Style()
style.configure("TButton", background="white", foreground="grey", font=("TkDefaultFont", 12), borderwidth=2,
                relief="solid")

text = tk.Label(root, text="Import your ydk or txt file", font=("TkDefaultFont", 14), foreground="grey")
text.pack(pady=10, side=tk.TOP)

browse_button = ttk.Button(root, text="Browse", command=save_file)
browse_button.pack(pady=10, side=tk.BOTTOM)

root.mainloop()
"""