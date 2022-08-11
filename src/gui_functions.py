from diaries_management_functions import *
import tkinter
from tkinter import ttk, Menu, filedialog
from tkinter.scrolledtext import ScrolledText

# Global variables
root = tkinter.Tk()
list_of_entries = tkinter.StringVar(value="")
entries_list = tkinter.Listbox(root, listvariable=list_of_entries, selectmode="browse")
open_entry_button = ttk.Button(root, text="Open entry", command=lambda: open_entry_function(), state="disabled")
text_label = ttk.Label(root, text="")
text_field = ScrolledText()
save_button = ttk.Button(root, text="Save entry", command=lambda: update_entry(text_field.get("1.0", tkinter.END)), state="disabled")

global already_active_entry_window_answer


def new_diary_window():
    ndw = tkinter.Toplevel()
    ndw.title("Create a new diary")

    diary_window_width = int(get_app_main_window_width()*0.75)
    diary_window_height = int(get_app_main_window_height()/3.9)

    center_x = int(get_screen_width_var() / 2 - diary_window_width / 2)
    center_y = int(get_screen_width_var() / 2 - diary_window_height / 2)

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
    create_diary_button = ttk.Button(ndw, text="Create diary", command=lambda: create_diary(name_box.get(), description_box.get(), password_box.get()))

    name_box.focus()

    ndw.columnconfigure(1, weight=1)

    ndw.rowconfigure(1)
    ndw.rowconfigure(2)
    ndw.rowconfigure(3)
    ndw.rowconfigure(4)
    ndw.rowconfigure(5)
    ndw.rowconfigure(6)
    ndw.rowconfigure(7)

    name_label.grid(column=1, row=1, sticky="W", padx=5)
    name_box.grid(column=1, row=2, sticky="EW", padx=5)
    description_label.grid(column=1, row=3, sticky="W", padx=5)
    description_box.grid(column=1, row=4, sticky="EW", padx=5)
    password_label.grid(column=1, row=5, sticky="W", padx=5)
    password_box.grid(column=1, row=6, sticky="EW", padx=5)
    create_diary_button.grid(column=1, row=7, sticky="S", pady=5)


def open_diary_window():
    set_open_diary(filedialog.askopenfilename(defaultextension=get_diaries_extension(), initialdir=get_diaries_folder_path()))
    open_diary()

    if get_open_diary() == "":
        create_message_window("ERROR: The diary wasn't opened", 0)
    else:
        aux_var = get_entries_from_open_diary()
        list_of_entries.initialize(value=aux_var)
        # list_of_entries = tkinter.StringVar(value=aux_var)

        if len(aux_var) > 0:
            entries_list.configure(listvariable=list_of_entries)
            entries_list.select_set(0)
            open_entry_button.configure(state="!disabled")
            save_button.configure(state="!disabled")
            text_label.configure(text="")
            text_field.delete("1.0", tkinter.END)

        else:
            create_message_window("The diary has been opened but it has no entries", 1)


def set_already_active_entry_window_answer(answer, aaew):
    global already_active_entry_window_answer
    already_active_entry_window_answer = answer
    aaew.destroy()


def already_active_entry_window(new_entry, old_entry):
    aaew = tkinter.Toplevel()
    aaew.title("Choose an action")

    diary_window_width = 400
    diary_window_height = 200

    center_x = int(get_screen_width_var() / 2 - diary_window_width / 2)
    center_y = int(get_screen_height_var() / 2 - diary_window_height / 2)

    # aaew.geometry(f'{diary_window_width}x{diary_window_height}+{center_x}+{center_y}')
    aaew.geometry(f'+{center_x}+{center_y}')

    aaew.attributes('-topmost', True)
    aaew.focus_force()
    aaew.update()
    aaew.attributes('-topmost', False)

    aaew.iconbitmap('../assets/diary.ico')

    aux_text1 = f"You want to open the {new_entry} entry while the {old_entry} entry is open."
    aux_text2 = f"You will lose any change you haven't saved."
    aux_text3 = f"Are you sure you want to continue?"

    text_label1 = ttk.Label(aaew, text=aux_text1)
    text_label2 = ttk.Label(aaew, text=aux_text2)
    text_label3 = ttk.Label(aaew, text=aux_text3)

    yes_button = ttk.Button(aaew, text="Yes", command=lambda: set_already_active_entry_window_answer(True, aaew))
    no_button = ttk.Button(aaew, text="No", command=lambda: set_already_active_entry_window_answer(False, aaew))

    aaew.columnconfigure(1)
    aaew.columnconfigure(2)

    aaew.rowconfigure(1)
    aaew.rowconfigure(2)
    aaew.rowconfigure(3)
    aaew.rowconfigure(4)

    text_label1.grid(column=1, row=1, sticky="N", padx=5, columnspan=2)
    text_label2.grid(column=1, row=2, sticky="N", padx=5, columnspan=2)
    text_label3.grid(column=1, row=3, sticky="N", padx=5, columnspan=2)
    yes_button.grid(column=1, row=4, sticky="N", padx=5)
    no_button.grid(column=2, row=4, sticky="N", padx=5)

    return aaew


def close_diary_aux(cdw):
    list_of_entries.initialize(value="")
    entries_list.configure(listvariable=list_of_entries)
    open_entry_button.configure(state="disabled")
    save_button.configure(state="disabled")
    text_label.configure(text="")
    text_field.delete("1.0", tkinter.END)

    close_diary()
    cdw.destroy()


def close_diary_window():
    cdw = tkinter.Toplevel()
    cdw.title("Close diary")

    diary_window_width = 400
    diary_window_height = 200

    center_x = int(get_screen_width_var() / 2 - diary_window_width / 2)
    center_y = int(get_screen_height_var() / 2 - diary_window_height / 2)

    # cdw.geometry(f'{diary_window_width}x{diary_window_height}+{center_x}+{center_y}')
    cdw.geometry(f'+{center_x}+{center_y}')

    cdw.attributes('-topmost', True)
    cdw.focus_force()
    cdw.update()
    cdw.attributes('-topmost', False)

    cdw.iconbitmap('../assets/diary.ico')

    aux_text1 = f"Are you sure you want to close this diary?"
    aux_text2 = f"You will lose any change you haven't saved."

    text_label1 = ttk.Label(cdw, text=aux_text1)
    text_label2 = ttk.Label(cdw, text=aux_text2)

    yes_button = ttk.Button(cdw, text="Yes", command=lambda: close_diary_aux(cdw))
    no_button = ttk.Button(cdw, text="No", command=lambda: cdw.destroy())

    cdw.columnconfigure(1)
    cdw.columnconfigure(2)
    cdw.columnconfigure(3)

    cdw.rowconfigure(1)
    cdw.rowconfigure(2)

    text_label1.grid(column=1, row=1, sticky="N", padx=5, columnspan=2)
    text_label2.grid(column=1, row=2, sticky="N", padx=5, columnspan=2)

    yes_button.grid(column=1, row=3, sticky="N", padx=5)
    no_button.grid(column=2, row=3, sticky="N", padx=5)


def close_program_aux(cpw):
    list_of_entries.initialize(value="")
    entries_list.configure(listvariable=list_of_entries)
    open_entry_button.configure(state="disabled")
    save_button.configure(state="disabled")
    text_label.configure(text="")
    text_field.delete("1.0", tkinter.END)

    close_diary()
    cpw.destroy()

    root.destroy()


def close_program_window():
    cpw = tkinter.Toplevel()
    cpw.title("Close program")

    diary_window_width = 400
    diary_window_height = 200

    center_x = int(get_screen_width_var() / 2 - diary_window_width / 2)
    center_y = int(get_screen_height_var() / 2 - diary_window_height / 2)

    # cdw.geometry(f'{diary_window_width}x{diary_window_height}+{center_x}+{center_y}')
    cpw.geometry(f'+{center_x}+{center_y}')

    cpw.attributes('-topmost', True)
    cpw.focus_force()
    cpw.update()
    cpw.attributes('-topmost', False)

    cpw.iconbitmap('../assets/diary.ico')

    aux_text1 = f"Are you sure you want to close the program?"
    aux_text2 = f"You will lose any change you haven't saved."

    text_label1 = ttk.Label(cpw, text=aux_text1)
    text_label2 = ttk.Label(cpw, text=aux_text2)

    yes_button = ttk.Button(cpw, text="Yes", command=lambda: close_program_aux(cpw))
    no_button = ttk.Button(cpw, text="No", command=lambda: cpw.destroy())

    cpw.columnconfigure(1)
    cpw.columnconfigure(2)
    cpw.columnconfigure(3)

    cpw.rowconfigure(1)
    cpw.rowconfigure(2)

    text_label1.grid(column=1, row=1, sticky="N", padx=5, columnspan=2)
    text_label2.grid(column=1, row=2, sticky="N", padx=5, columnspan=2)

    yes_button.grid(column=1, row=3, sticky="N", padx=5)
    no_button.grid(column=2, row=3, sticky="N", padx=5)
    

def open_entry_function():
    active_selection = entries_list.selection_get()

    if active_selection == date_format_from_db_to_string(get_active_entry()):
        create_message_window("This entry is already open", 2)
    elif get_active_entry() == "":
        set_active_entry(active_selection)
        text_field.delete("1.0", tkinter.END)
        text_field.insert(tkinter.INSERT, get_text_from_active_entry())
        text_label_text = f"This is the entry for {active_selection} from diary {get_diary_name()}"
        text_label.configure(text=text_label_text)
    elif get_active_entry() != "":
        aux = already_active_entry_window(active_selection, date_format_from_db_to_string(get_active_entry()))
        aux.wait_window()

        if already_active_entry_window_answer:
            set_active_entry(active_selection)
            text_field.delete("1.0", tkinter.END)
            text_field.insert(tkinter.INSERT, get_text_from_active_entry())
            text_label_text = f"This is the entry for {active_selection} from diary {get_diary_name()}"
            text_label.configure(text=text_label_text)


def main_gui():
    # Tutorial used for the GUI: https://www.pythontutorial.net/tkinter/

    # We create the basic GUI geometry
    # root = tkinter.Tk()
    root.title("Your Pythonic secret diary")
    
    set_screen_width_var(root.winfo_screenwidth())
    set_screen_height_var(root.winfo_screenheight())

    center_x = int(get_screen_width_var() / 2 - get_app_main_window_width() / 2)
    center_y = int(get_screen_height_var() / 2 - get_app_main_window_height() / 2)

    root.geometry(f'{get_app_main_window_width()}x{get_app_main_window_height()}+{center_x}+{center_y}')

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
    diaries_menu.add_command(label='Open diary', command=open_diary_window)
    diaries_menu.add_command(label='Close diary', command=close_diary_window)
    diaries_menu.add_separator()
    diaries_menu.add_command(label='Exit program', command=close_program_window)

    menubar.add_cascade(label="Diaries", menu=diaries_menu)
    help_menu = Menu(menubar, tearoff=0)

    help_menu.add_command(label='Welcome')
    help_menu.add_command(label='About...')

    menubar.add_cascade(label="Help", menu=help_menu)

    # We populate the GUI with the elements we need
    entries_label = ttk.Label(root, text="Available entries")
    scrollbar = ttk.Scrollbar(root, orient='vertical', command=entries_list.yview)
    entries_list['yscrollcommand'] = scrollbar.set

    root.columnconfigure(1)
    root.columnconfigure(2)
    root.columnconfigure(3, weight=1)

    root.rowconfigure(1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3)

    entries_label.grid(column=1, row=1, padx=10, pady=5)
    entries_list.grid(column=1, row=2, padx=0, pady=0, sticky="NSEW")
    open_entry_button.grid(column=1, row=3, padx=10, pady=5)
    scrollbar.grid(column=2, row=2, sticky="NSEW")
    text_label.grid(column=3, row=1, padx=10, pady=5)
    text_field.grid(column=3, row=2, sticky="NSEW", padx=5, pady=0)
    save_button.grid(column=3, row=3, padx=10, pady=5)

    initialise_global_variables_from_diaries_functions()

    root.mainloop()
