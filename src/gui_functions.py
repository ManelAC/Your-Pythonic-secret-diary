from diaries_management_functions import *
import tkinter
from tkinter import ttk, Menu
from tkinter.scrolledtext import ScrolledText

# Global variables
root = tkinter.Tk()


def get_app_window_width():
    return 800


def get_app_window_height():
    return 600


def new_diary_window():
    ndw = tkinter.Toplevel()
    ndw.title("Create a new diary")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    diary_window_width = int(get_app_window_width()*0.75)
    diary_window_height = int(get_app_window_height()/3.9)

    center_x = int(screen_width / 2 - diary_window_width / 2)
    center_y = int(screen_height / 2 - diary_window_height / 2)

    ndw.geometry(f'{diary_window_width}x{diary_window_height}+{center_x}+{center_y}')

    ndw.attributes('-topmost', True)
    ndw.focus_force()
    ndw.update()
    ndw.attributes('-topmost', False)

    ndw.iconbitmap('../assets/diary.ico')

    name_label = ttk.Label(ndw, text="Diary name")
    description_label = ttk.Label(ndw, text="Diary description")
    password_label = ttk.Label(ndw, text="Diary password")

    name = tkinter.StringVar()
    name_box = ttk.Entry(ndw, textvariable=name)
    description = tkinter.StringVar()
    description_box = ttk.Entry(ndw, textvariable=description)
    password = tkinter.StringVar()
    password_box = ttk.Entry(ndw, textvariable=password, show="*")
    create_diary_button = ttk.Button(ndw, text="Create diary", command=lambda: create_diary(root, name_box.get(), description_box.get(), password_box.get()))
    
    name_box.focus()

    ndw.columnconfigure(1, weight=1)

    ndw.rowconfigure(1)
    ndw.rowconfigure(2)
    ndw.rowconfigure(3)
    ndw.rowconfigure(4)
    ndw.rowconfigure(5)
    ndw.rowconfigure(6)
    ndw.rowconfigure(7)

    padx_var = 5

    name_label.grid(column=1, row=1, sticky="W", padx=padx_var)
    name_box.grid(column=1, row=2, sticky="EW", padx=padx_var)
    description_label.grid(column=1, row=3, sticky="W", padx=padx_var)
    description_box.grid(column=1, row=4, sticky="EW", padx=padx_var)
    password_label.grid(column=1, row=5, sticky="W", padx=padx_var)
    password_box.grid(column=1, row=6, sticky="EW", padx=padx_var)
    create_diary_button.grid(column=1, row=7, sticky="S", pady=padx_var)


def main_gui():
    '''
    Tutorial used for the GUI:
    https://www.pythontutorial.net/tkinter/
    '''

    # We create the basic GUI geometry
    # root = tkinter.Tk()
    root.title("Your Pythonic secret diary")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width / 2 - get_app_window_width() / 2)
    center_y = int(screen_height / 2 - get_app_window_height() / 2)

    root.geometry(f'{get_app_window_width()}x{get_app_window_height()}+{center_x}+{center_y}')

    # Solution from here about how to make the GUI appear on top: https://stackoverflow.com/a/45064895
    root.attributes('-topmost', True)
    root.focus_force()
    root.update()
    root.attributes('-topmost', False)

    root.iconbitmap('../assets/diary.ico')

    # Now we create the menu
    menubar = Menu(root)
    root.config(menu=menubar)

    diaries_menu = Menu(menubar, tearoff=0)
    diaries_menu.add_command(label='New diary', command=new_diary_window)
    diaries_menu.add_command(label='Open diary')
    diaries_menu.add_command(label='Close diary')
    diaries_menu.add_separator()
    diaries_menu.add_command(label='Exit program', command=root.destroy)

    menubar.add_cascade(label="Diaries", menu=diaries_menu)
    help_menu = Menu(menubar, tearoff=0)

    help_menu.add_command(label='Welcome')
    help_menu.add_command(label='About...')

    menubar.add_cascade(label="Help", menu=help_menu)

    # We populate the GUI with the elements we need
    text_label = ttk.Label(root, text="You're editing entry DD/MM/YYYY from diary X")
    entries_label = ttk.Label(root, text="Available entries")
    save_button = ttk.Button(root, text="Save entry")

    root.columnconfigure(1)  # The entries panel
    root.columnconfigure(2, weight=1)  # The text panel
    root.columnconfigure(3)  # The scrollbar panel

    root.rowconfigure(1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3)
    root.rowconfigure(4)

    text_label.grid(column=2, row=1, padx=10, pady=5)
    entries_label.grid(column=1, row=1, padx=10, pady=5)
    save_button.grid(column=2, row=4, padx=10, pady=5)

    text_field = ScrolledText()
    text_field.grid(column=2, row=2, sticky="NSEW", padx=0, pady=0)

    root.mainloop()
