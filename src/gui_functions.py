from diaries_management import *
import tkinter
from tkinter import ttk, Menu
from tkinter.scrolledtext import ScrolledText


def get_app_window_width():
    return 800


def get_app_window_height():
    return 600


def draw_gui():
    '''
    Tutorial used for the GUI:
    https://www.pythontutorial.net/tkinter/
    '''

    # We create the basic GUI geometry
    root = tkinter.Tk()
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
    diaries_menu.add_command(label='New diary')
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
    save_button = ttk.Button(text="Save entry")

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
