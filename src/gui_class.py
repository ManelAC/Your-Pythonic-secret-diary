import tkinter
from tkinter import ttk, Menu, filedialog, font
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import webbrowser


class GUI:

    def __init__(self, diary):
        self.diary = diary
        
        # First we create the basic structure of the main window
        # Tutorial used for the GUI: https://www.pythontutorial.net/tkinter/
        self.root = tkinter.Tk()
        self.root.title("Your Pythonic secret diary")
        self.screen_width = self.root.winfo_screenwidth()  # Variable that stores the screen width
        self.screen_height = self.root.winfo_screenheight()  # Variable that stores the screen height
        self.main_window_width = 800
        self.main_window_height = 600
        
        center_x = int(self.screen_width / 2 - self.main_window_width / 2)
        center_y = int(self.screen_height / 2 - self.main_window_height / 2)

        # root.geometry(f'{get_app_main_window_width()}x{get_app_main_window_height()}+{center_x}+{center_y}')
        self.root.geometry(f'+{center_x}+{center_y}')

        # Solution from here about how to make the GUI appear on top: https://stackoverflow.com/a/45064895
        self.root.attributes('-topmost', True)
        self.root.focus_force()
        self.root.update()
        self.root.attributes('-topmost', False)

        self.root.iconbitmap('../assets/diary.ico')
        
        self.root.columnconfigure(1)
        self.root.columnconfigure(2)
        self.root.columnconfigure(3, weight=1)

        self.root.rowconfigure(1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3)
        self.root.rowconfigure(4)

        # Now we create a menu in the main window
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        diaries_menu = Menu(menubar, tearoff=0)
        diaries_menu.add_command(label='New diary', command=self.new_diary_window)
        diaries_menu.add_command(label='Open diary', command=self.open_diary_window)
        diaries_menu.add_command(label='Close diary', command=self.close_diary_window)
        diaries_menu.add_separator()
        diaries_menu.add_command(label='Exit program', command=self.close_program_window)
        menubar.add_cascade(label="Diaries", menu=diaries_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='Welcome', command=self.welcome_window)
        help_menu.add_command(label='About', command=self.about_window)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # We populate the GUI with the elements we need
        self.entries_text_label = ttk.Label(self.root, text="Available entries")
        self.entries_text_label.grid(column=1, row=1, padx=10, pady=5)

        self.entries_list_content = tkinter.StringVar(value="")
        self.entries_list_box = tkinter.Listbox(self.root, listvariable=self.entries_list_content, selectmode="browse")
        self.entries_list_box_scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.entries_list_box.yview)
        self.entries_list_box['yscrollcommand'] = self.entries_list_box_scrollbar.set
        self.entries_list_box.grid(column=1, row=2, padx=0, pady=0, sticky="NSEW")
        self.entries_list_box_scrollbar.grid(column=2, row=2, sticky="NSEW")

        self.open_entry_button = ttk.Button(self.root, text="Open selected entry", command=lambda: self.open_entry_function(), state="disabled")
        self.open_entry_button.grid(column=1, row=3, padx=10, pady=5)

        self.add_new_entry_button = ttk.Button(self.root, text="Add new entry", command=lambda: self.add_new_entry_window(), state="disabled")
        self.add_new_entry_button.grid(column=1, row=4, padx=0, pady=5)

        self.main_window_text_label = ttk.Label(self.root, text="Open a diary to edit it.")
        self.main_window_text_label.grid(column=3, row=1, padx=10, pady=5, sticky="W")

        self.delete_entry_button = ttk.Button(self.root, text="Delete this entry", command=lambda: self.delete_active_entry_window(), state="disabled")
        self.delete_entry_button.grid(column=3, row=1, padx=10, pady=5, sticky="E")

        self.text_field = ScrolledText()
        self.text_field.grid(column=3, row=2, sticky="NSEW", padx=5, pady=0, rowspan=2)

        self.save_button = ttk.Button(self.root, text="Save entry", command=lambda: self.update_confirmation_window(), state="disabled")
        self.save_button.grid(column=3, row=4, padx=10, pady=5)

    # Setters and getters
    def get_screen_width(self):
        return self.screen_width

    def get_screen_height(self):
        return self.screen_height

    def get_app_main_window_width(self):
        return self.main_window_width

    def get_app_main_window_height(self):
        return self.main_window_height

    def get_gui_root(self):
        return self.root

    # Auxiliary functions
    @staticmethod
    def get_days_list():
        list_aux = []

        for i in range(1, 32):
            list_aux.append(f"{i}")

        return list_aux

    @staticmethod
    def get_months_list():
        list_aux = []

        for i in range(1, 13):
            list_aux.append(f"{i}")

        return list_aux

    @staticmethod
    def get_years_list():
        list_aux = []

        start_year = int(datetime.today().strftime("%Y")) - 5
        end_year = int(datetime.today().strftime("%Y")) + 5

        for i in range(start_year, end_year + 1):
            list_aux.append(f"{i}")

        return list_aux

    def is_date_valid(self, day, month, year):
        # The following bit is from: https://stackoverflow.com/a/51981596
        number_of_days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            number_of_days_per_month[1] = 29

        if day > number_of_days_per_month[month - 1]:
            self.create_message_window("The date is incorrect. Pick a different one.", 0)
            return False
        else:
            aux_var = self.diary.get_entries_from_open_diary()
            aux_string = f"{day:02}/{month:02}/{year:04}"
            if aux_string in aux_var:
                self.create_message_window("An entry for this date already exists. Pick a different one.", 0)
                return False
            else:
                return True

    # Windows creation functions
    def welcome_window(self):
        ww = tkinter.Toplevel()
        ww.title("Welcome")

        welcome_window_width = 600
        welcome_window_height = 100

        center_x = int(self.screen_width / 2 - welcome_window_width / 2)
        center_y = int(self.screen_height / 2 - welcome_window_height / 2)

        ww.geometry(f'+{center_x}+{center_y}')

        ww.attributes('-topmost', True)
        ww.focus_force()
        ww.update()
        ww.attributes('-topmost', False)

        ww.iconbitmap('../assets/diary.ico')

        text1_label = ttk.Label(ww, text="Welcome to Your Pythonic secret diary!", font="bold")
        text2_label = ttk.Label(ww, text="This is a Python-based secret diary management system in which you can keep your secrets in as many diaries as you want.")
        text3_label = ttk.Label(ww, text="To start with the program, just go to the Diaries menu, create your first diary and open it.")
        ok_button = ttk.Button(ww, text="Ok", command=lambda: ww.destroy())

        ww.columnconfigure(1, weight=1)

        ww.rowconfigure(1)
        ww.rowconfigure(2)
        ww.rowconfigure(3)
        ww.rowconfigure(4)

        text1_label.grid(column=1, row=1, pady=5)
        text2_label.grid(column=1, row=2)
        text3_label.grid(column=1, row=3)
        ok_button.grid(column=1, row=4, pady=5)

    @staticmethod
    def open_github_in_browser(url):
        webbrowser.open_new(url)

    def about_window(self):
        aw = tkinter.Toplevel()
        aw.title("About")

        welcome_window_width = 200
        welcome_window_height = 100

        center_x = int(self.screen_width / 2 - welcome_window_width / 2)
        center_y = int(self.screen_height / 2 - welcome_window_height / 2)

        aw.geometry(f'+{center_x}+{center_y}')

        aw.attributes('-topmost', True)
        aw.focus_force()
        aw.update()
        aw.attributes('-topmost', False)

        aw.iconbitmap('../assets/diary.ico')

        text1_label = ttk.Label(aw, text="Your Pythonic secret diary 1.01", font="bold")
        text2_label = ttk.Label(aw, text="My name is Manel and you can find more about me in GitHub at:")

        # How to change the cursor while hovering the text found here: https://stackoverflow.com/questions/45184462/how-do-i-change-my-cursor-to-a-hand-only-when-it-is-hovering-over-a-label
        text3_label = ttk.Label(aw, text="https://github.com/ManelAC", font="bold", foreground="blue", cursor="hand2")

        # How to use underline text in Python 3, extracted from here: https://stackoverflow.com/a/44890599
        my_font = font.Font(text3_label, text3_label.cget("font"))
        my_font.configure(underline=True)
        text3_label.configure(font=my_font)
        text3_label.bind("<Button-1>", lambda e: self.open_github_in_browser("https://github.com/ManelAC"))
        ok_button = ttk.Button(aw, text="Ok", command=lambda: aw.destroy())

        aw.columnconfigure(1, weight=1)

        aw.rowconfigure(1)
        aw.rowconfigure(2)
        aw.rowconfigure(3)
        aw.rowconfigure(4)

        text1_label.grid(column=1, row=1, pady=5)
        text2_label.grid(column=1, row=2, padx=5)
        text3_label.grid(column=1, row=3)
        ok_button.grid(column=1, row=4, pady=5)
    
    def new_diary_window_aux(self, name, description, password, ndw):
        message, result = self.diary.create_diary(name, description, password)

        if not result:
            self.create_message_window(message, 0)
        else:
            ndw.destroy()
            self.create_message_window(message, 1)

    def new_diary_window(self):
        ndw = tkinter.Toplevel()
        ndw.title("Create a new diary")

        new_diary_window_width = int(self.main_window_width * 0.75)
        new_diary_window_height = int(self.main_window_height / 3.9)

        center_x = int(self.screen_width / 2 - new_diary_window_width / 2)
        center_y = int(self.screen_height / 2 - new_diary_window_height / 2)

        ndw.geometry(f'{new_diary_window_width}x{new_diary_window_height}+{center_x}+{center_y}')

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
        create_diary_button = ttk.Button(ndw, text="Create diary", command=lambda: self.new_diary_window_aux(name_box.get(), description_box.get(), password_box.get(), ndw))

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

    def ask_for_password_window_aux(self, password, afpw):
        message, correct_password = self.diary.unlock_diary(password)

        if not correct_password:
            self.create_message_window(message, 0)
        else:
            aux_var = self.diary.get_entries_from_open_diary()
            self.entries_list_content.initialize(value=aux_var)
            # entries_list_content = tkinter.StringVar(value=aux_var)

            self.entries_list_box.configure(listvariable=self.entries_list_content)
            self.entries_list_box.select_set(0)
            self.add_new_entry_button.configure(state="!disabled")
            self.main_window_text_label.configure(text="Open an entry to edit it.")
            self.text_field.delete("1.0", tkinter.END)

            if len(aux_var) == 0:
                self.create_message_window("The diary has been opened but it has no entries.", 1)
            else:
                self.open_entry_button.configure(state="!disabled")

        afpw.destroy()

    def ask_for_password_window(self):
        afpw = tkinter.Toplevel()
        afpw.title("Introduce the password for this diary:")

        diary_window_width = 400
        diary_window_height = 200

        center_x = int(self.screen_width / 2 - diary_window_width / 2)
        center_y = int(self.screen_height / 2 - diary_window_height / 2)

        afpw.geometry(f'+{center_x}+{center_y}')

        afpw.attributes('-topmost', True)
        afpw.focus_force()
        afpw.update()
        afpw.attributes('-topmost', False)

        afpw.iconbitmap('../assets/diary.ico')

        password_label = ttk.Label(afpw, text="Introduce the password for this diary:")

        password = tkinter.StringVar()
        password_box = ttk.Entry(afpw, textvariable=password, show="*")
        open_diary_button = ttk.Button(afpw, text="Open diary", command=lambda: self.ask_for_password_window_aux(password_box.get(), afpw))

        password_box.focus()

        afpw.columnconfigure(1, weight=1)

        afpw.rowconfigure(1)
        afpw.rowconfigure(2)
        afpw.rowconfigure(3)

        password_label.grid(column=1, row=1, sticky="W", padx=5)
        password_box.grid(column=1, row=2, sticky="EW", padx=5)
        open_diary_button.grid(column=1, row=3, sticky="S", pady=5)

    def open_diary_window_aux(self, opw):
        opw.destroy()
        self.diary.close_diary()
        self.open_entry_button.configure(state="disabled")
        self.add_new_entry_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.delete_entry_button.configure(state="disabled")
        self.main_window_text_label.configure(text="Open a diary to edit it.")
        self.text_field.delete("1.0", tkinter.END)
        self.entries_list_content.initialize(value="")
        self.entries_list_box.configure(listvariable=self.entries_list_content)

        self.diary.set_open_diary_path(filedialog.askopenfilename(initialdir=self.diary.get_diaries_folder_path(), filetypes=(("Secret diary", f"{self.diary.get_diaries_extension()}"),)))

        message, open_diary = self.diary.open_diary()

        if not open_diary:
            self.create_message_window(message, 0)
        else:
            self.ask_for_password_window()

    def open_diary_window(self):
        if self.diary.get_open_diary_path() != "":
            opw = tkinter.Toplevel()
            opw.title("Open diary")

            diary_window_width = 400
            diary_window_height = 200

            center_x = int(self.screen_width / 2 - diary_window_width / 2)
            center_y = int(self.screen_height / 2 - diary_window_height / 2)

            # opw.geometry(f'{diary_window_width}x{diary_window_height}+{center_x}+{center_y}')
            opw.geometry(f'+{center_x}+{center_y}')

            opw.attributes('-topmost', True)
            opw.focus_force()
            opw.update()
            opw.attributes('-topmost', False)

            opw.iconbitmap('../assets/diary.ico')

            aux_text1 = f"You want to open a new diary while the diary {self.diary.get_diary_name()} is open."
            aux_text2 = f"You will lose any change you haven't saved in the diary {self.diary.get_diary_name()}."
            aux_text3 = f"Are you sure you want to continue?"

            text_label1 = ttk.Label(opw, text=aux_text1)
            text_label2 = ttk.Label(opw, text=aux_text2)
            text_label3 = ttk.Label(opw, text=aux_text3)

            yes_button = ttk.Button(opw, text="Yes", command=lambda: self.open_diary_window_aux(opw))
            no_button = ttk.Button(opw, text="No", command=lambda: opw.destroy())

            opw.columnconfigure(1)
            opw.columnconfigure(2)

            opw.rowconfigure(1)
            opw.rowconfigure(2)
            opw.rowconfigure(3)
            opw.rowconfigure(4)

            text_label1.grid(column=1, row=1, sticky="N", padx=5, columnspan=2)
            text_label2.grid(column=1, row=2, sticky="N", padx=5, columnspan=2)
            text_label3.grid(column=1, row=3, sticky="N", padx=5, columnspan=2)
            yes_button.grid(column=1, row=4, sticky="N", padx=5, pady=5)
            no_button.grid(column=2, row=4, sticky="N", padx=5, pady=5)
        else:
            opw = tkinter.Toplevel()
            self.open_diary_window_aux(opw)

    def already_active_entry_window_aux(self, new_entry, aaew):
        self.diary.set_active_entry(self.diary.gui_date_to_db_date(new_entry))
        self.text_field.delete("1.0", tkinter.END)
        self.text_field.insert(tkinter.INSERT, self.diary.get_text_from_active_entry())
        text_label_text = f"This is the entry for {self.diary.db_date_to_gui_date(self.diary.get_active_entry())} from diary {self.diary.get_diary_name()}."
        self.main_window_text_label.configure(text=text_label_text)
        self.save_button.configure(state="!disabled")
        self.delete_entry_button.configure(state="!disabled")
        aaew.destroy()

    def already_active_entry_window(self, new_entry, old_entry):
        aaew = tkinter.Toplevel()
        aaew.title("Open entry")

        diary_window_width = 400
        diary_window_height = 200

        center_x = int(self.screen_width / 2 - diary_window_width / 2)
        center_y = int(self.screen_height / 2 - diary_window_height / 2)

        # aaew.geometry(f'{diary_window_width}x{diary_window_height}+{center_x}+{center_y}')
        aaew.geometry(f'+{center_x}+{center_y}')

        aaew.attributes('-topmost', True)
        aaew.focus_force()
        aaew.update()
        aaew.attributes('-topmost', False)

        aaew.iconbitmap('../assets/diary.ico')

        aux_text1 = f"You want to open the {new_entry} entry while the {old_entry} entry is open."
        aux_text2 = f"You will lose any change you haven't saved in the {old_entry} entry."
        aux_text3 = f"Are you sure you want to continue?"

        text_label1 = ttk.Label(aaew, text=aux_text1)
        text_label2 = ttk.Label(aaew, text=aux_text2)
        text_label3 = ttk.Label(aaew, text=aux_text3)

        yes_button = ttk.Button(aaew, text="Yes", command=lambda: self.already_active_entry_window_aux(new_entry, aaew))
        no_button = ttk.Button(aaew, text="No", command=lambda: aaew.destroy())

        aaew.columnconfigure(1)
        aaew.columnconfigure(2)

        aaew.rowconfigure(1)
        aaew.rowconfigure(2)
        aaew.rowconfigure(3)
        aaew.rowconfigure(4)

        text_label1.grid(column=1, row=1, sticky="N", padx=5, columnspan=2)
        text_label2.grid(column=1, row=2, sticky="N", padx=5, columnspan=2)
        text_label3.grid(column=1, row=3, sticky="N", padx=5, columnspan=2)
        yes_button.grid(column=1, row=4, sticky="N", padx=5, pady=5)
        no_button.grid(column=2, row=4, sticky="N", padx=5, pady=5)

    def open_entry_function(self):
        active_selection = self.entries_list_box.selection_get()

        if active_selection == self.diary.db_date_to_gui_date(self.diary.get_active_entry()):
            self.create_message_window("This entry is already open.", 2)

        elif self.diary.get_active_entry() == "":
            self.diary.set_active_entry(self.diary.gui_date_to_db_date(active_selection))
            self.text_field.delete("1.0", tkinter.END)
            self.text_field.insert(tkinter.INSERT, self.diary.get_text_from_active_entry())
            text_label_text = f"This is the entry for {active_selection} from diary {self.diary.get_diary_name()}"
            self.main_window_text_label.configure(text=text_label_text)
            self.save_button.configure(state="!disabled")
            self.delete_entry_button.configure(state="!disabled")

        elif self.diary.get_active_entry() != "":
            self.already_active_entry_window(active_selection, self.diary.db_date_to_gui_date(self.diary.get_active_entry()))

    def add_new_entry_window_aux(self, day, month, year, anew):
        if self.is_date_valid(day, month, year):
            self.diary.add_entry(day, month, year)
            self.entries_list_content = tkinter.StringVar(value=self.diary.get_entries_from_open_diary())
            self.entries_list_box.configure(listvariable=self.entries_list_content)
            self.entries_list_box.select_set(0)
            self.open_entry_button.configure(state="!disabled")
            anew.destroy()

    def add_new_entry_window(self):
        anew = tkinter.Toplevel()
        anew.title("Add a new entry")

        add_new_entry_window_width = int(self.main_window_width * 0.75)
        add_new_entry_window_height = int(self.main_window_height / 3.9)

        center_x = int(self.screen_width / 2 - add_new_entry_window_width / 2)
        center_y = int(self.screen_height / 2 - add_new_entry_window_height / 2)

        # anew.geometry(f'{diary_window_width}x{diary_window_height}+{center_x}+{center_y}')
        anew.geometry(f'+{center_x}+{center_y}')

        anew.attributes('-topmost', True)
        anew.focus_force()
        anew.update()
        anew.attributes('-topmost', False)

        anew.iconbitmap('../assets/diary.ico')

        current_day = int(datetime.today().strftime("%d"))
        current_month = int(datetime.today().strftime("%m"))
        current_year = int(datetime.today().strftime("%Y"))

        days_combobox = ttk.Combobox(anew, values=self.get_days_list(), state="readonly")
        days_combobox.set(current_day)
        # days_combobox.current(current_day-1)
        months_combobox = ttk.Combobox(anew, values=self.get_months_list(), state="readonly")
        months_combobox.set(current_month)
        # months_combobox.current(current_month-1)
        years_combobox = ttk.Combobox(anew, values=self.get_years_list(), state="readonly")
        years_combobox.set(current_year)
        # years_combobox.current(current_year)

        anew_text_label = ttk.Label(anew, text="Pick a date")
        create_diary_button = ttk.Button(anew, text="Add new entry", command=lambda: self.add_new_entry_window_aux(int(days_combobox.get()), int(months_combobox.get()), int(years_combobox.get()), anew))

        anew.columnconfigure(1)
        anew.columnconfigure(2, weight=1)
        anew.columnconfigure(3)

        anew.rowconfigure(1)
        anew.rowconfigure(2)
        anew.rowconfigure(3)

        anew_text_label.grid(column=1, row=1, sticky="N", padx=5, columnspan=3)
        days_combobox.grid(column=1, row=2, sticky="EW", padx=5)
        months_combobox.grid(column=2, row=2, sticky="EW", padx=5)
        years_combobox.grid(column=3, row=2, sticky="EW", padx=5)
        create_diary_button.grid(column=1, row=3, sticky="N", pady=5, columnspan=3)

    def update_confirmation_window_aux(self, ucw):
        self.diary.update_entry(self.text_field.get("1.0", tkinter.END))
        ucw.destroy()

    def update_confirmation_window(self):
        ucw = tkinter.Toplevel()
        ucw.title("Save")

        diary_window_width = 400
        diary_window_height = 200

        center_x = int(self.screen_width / 2 - diary_window_width / 2)
        center_y = int(self.screen_height / 2 - diary_window_height / 2)

        # ucw.geometry(f'{diary_window_width}x{diary_window_height}+{center_x}+{center_y}')
        ucw.geometry(f'+{center_x}+{center_y}')

        ucw.attributes('-topmost', True)
        ucw.focus_force()
        ucw.update()
        ucw.attributes('-topmost', False)

        ucw.iconbitmap('../assets/diary.ico')

        aux_test1 = f"Are you sure you want to save the changes made in this {self.diary.db_date_to_gui_date(self.diary.get_active_entry())} entry?"

        text_label1 = ttk.Label(ucw, text=aux_test1)

        yes_button = ttk.Button(ucw, text="Yes", command=lambda: self.update_confirmation_window_aux(ucw))
        no_button = ttk.Button(ucw, text="No", command=lambda: ucw.destroy())

        ucw.columnconfigure(1)
        ucw.columnconfigure(2)

        ucw.rowconfigure(1)
        ucw.rowconfigure(2)

        text_label1.grid(column=1, row=1, sticky="N", padx=5, columnspan=2)

        yes_button.grid(column=1, row=4, sticky="N", padx=5, pady=5)
        no_button.grid(column=2, row=4, sticky="N", padx=5, pady=5)

    def delete_active_entry_aux(self, deaw):
        self.diary.delete_entry()

        self.entries_list_content.initialize(value=self.diary.get_entries_from_open_diary())
        self.entries_list_box.configure(listvariable=self.entries_list_content)
        self.entries_list_box.select_set(0)
        self.save_button.configure(state="disabled")
        self.delete_entry_button.configure(state="disabled")
        self.main_window_text_label.configure(text="Open an entry to edit it.")
        self.text_field.delete("1.0", tkinter.END)

        if len(self.diary.get_entries_from_open_diary()) == 0:
            self.open_entry_button.configure(state="disabled")

        deaw.destroy()

    def delete_active_entry_window(self):
        deaw = tkinter.Toplevel()
        deaw.title("Close diary")

        diary_window_width = 400
        diary_window_height = 200

        center_x = int(self.screen_width / 2 - diary_window_width / 2)
        center_y = int(self.screen_height / 2 - diary_window_height / 2)

        # cdw.geometry(f'{diary_window_width}x{diary_window_height}+{center_x}+{center_y}')
        deaw.geometry(f'+{center_x}+{center_y}')

        deaw.attributes('-topmost', True)
        deaw.focus_force()
        deaw.update()
        deaw.attributes('-topmost', False)

        deaw.iconbitmap('../assets/diary.ico')

        aux_text1 = f"Are you sure you want to delete the entry for {self.diary.db_date_to_gui_date(self.diary.get_active_entry())}?"
        aux_text2 = f"You will not be able to recover this entry after deleting it."

        text_label1 = ttk.Label(deaw, text=aux_text1)
        text_label2 = ttk.Label(deaw, text=aux_text2)

        yes_button = ttk.Button(deaw, text="Yes", command=lambda: self.delete_active_entry_aux(deaw))
        no_button = ttk.Button(deaw, text="No", command=lambda: deaw.destroy())

        deaw.columnconfigure(1)
        deaw.columnconfigure(2)
        deaw.columnconfigure(3)

        deaw.rowconfigure(1)
        deaw.rowconfigure(2)

        text_label1.grid(column=1, row=1, sticky="N", padx=5, columnspan=2)
        text_label2.grid(column=1, row=2, sticky="N", padx=5, columnspan=2)

        yes_button.grid(column=1, row=3, sticky="N", padx=5, pady=5)
        no_button.grid(column=2, row=3, sticky="N", padx=5, pady=5)

    def close_diary_window_aux(self, cdw):
        self.entries_list_content.initialize(value="")
        self.entries_list_box.configure(listvariable=self.entries_list_content)
        self.open_entry_button.configure(state="disabled")
        self.add_new_entry_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.delete_entry_button.configure(state="disabled")
        self.main_window_text_label.configure(text="Open a diary to edit it.")
        self.text_field.delete("1.0", tkinter.END)

        self.diary.close_diary()
        cdw.destroy()

    def close_diary_window(self):
        if self.diary.get_open_diary_path() == "":
            self.create_message_window("Can't close a diary since no diary is open.", 0)
        else:
            cdw = tkinter.Toplevel()
            cdw.title("Close diary")

            close_diary_window_width = 200
            close_diary_window_height = 100

            center_x = int(self.screen_width / 2 - close_diary_window_width / 2)
            center_y = int(self.screen_height / 2 - close_diary_window_height / 2)

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

            yes_button = ttk.Button(cdw, text="Yes", command=lambda: self.close_diary_window_aux(cdw))
            no_button = ttk.Button(cdw, text="No", command=lambda: cdw.destroy())

            cdw.columnconfigure(1)
            cdw.columnconfigure(2)
            cdw.columnconfigure(3)

            cdw.rowconfigure(1)
            cdw.rowconfigure(2)

            text_label1.grid(column=1, row=1, sticky="N", padx=5, columnspan=2)
            text_label2.grid(column=1, row=2, sticky="N", padx=5, columnspan=2)

            yes_button.grid(column=1, row=3, sticky="N", padx=5, pady=5)
            no_button.grid(column=2, row=3, sticky="N", padx=5, pady=5)

    def close_program_aux(self, cpw):
        self.entries_list_content.initialize(value="")
        self.entries_list_box.configure(listvariable=self.entries_list_content)
        self.open_entry_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.delete_entry_button.configure(state="disabled")
        self.main_window_text_label.configure(text="")
        self.text_field.delete("1.0", tkinter.END)

        self.diary.close_diary()
        cpw.destroy()

        self.root.destroy()

    def close_program_window(self):
        cpw = tkinter.Toplevel()
        cpw.title("Close program")

        close_program_window_width = 400
        close_program_window_height = 200

        center_x = int(self.screen_width / 2 - close_program_window_width / 2)
        center_y = int(self.screen_height / 2 - close_program_window_height / 2)

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

        yes_button = ttk.Button(cpw, text="Yes", command=lambda: self.close_program_aux(cpw))
        no_button = ttk.Button(cpw, text="No", command=lambda: cpw.destroy())

        cpw.columnconfigure(1)
        cpw.columnconfigure(2)
        cpw.columnconfigure(3)

        cpw.rowconfigure(1)
        cpw.rowconfigure(2)

        text_label1.grid(column=1, row=1, sticky="N", padx=5, columnspan=2)
        text_label2.grid(column=1, row=2, sticky="N", padx=5, columnspan=2)

        yes_button.grid(column=1, row=3, sticky="N", padx=5, pady=5)
        no_button.grid(column=2, row=3, sticky="N", padx=5, pady=5)

    def create_message_window(self, message_text, message_type):
        # If message type == 0, it's an error message
        # If message type == 1, it's a success message
        # If message type == 2, it's a caution message

        message_window = tkinter.Toplevel()
        if message_type == 0:
            message_window.title("Error")
        elif message_type == 1:
            message_window.title("Success")
        elif message_type == 2:
            message_window.title("Caution")

        diary_window_width = 0

        if message_type == 0:
            diary_window_width = 400
        elif message_type == 1:
            diary_window_width = 200

        diary_window_height = 100

        center_x = int(self.screen_width / 2 - diary_window_width / 2)
        center_y = int(self.screen_height / 2 - diary_window_height / 2)

        # message_window.geometry(f'{diary_window_width}x{diary_window_height}+{center_x}+{center_y}')
        message_window.geometry(f'+{center_x}+{center_y}')

        message_window.attributes('-topmost', True)
        message_window.focus_force()
        message_window.update()
        message_window.attributes('-topmost', False)

        if message_type == 0:
            message_window.iconbitmap('../assets/cross.ico')
        elif message_type == 1:
            message_window.iconbitmap('../assets/check.ico')
        elif message_type == 2:
            message_window.iconbitmap('../assets/caution.ico')

        text_label = ttk.Label(message_window, text=message_text)
        accept_button = ttk.Button(message_window, text="Accept", command=lambda: message_window.destroy())

        message_window.columnconfigure(1, weight=1)

        message_window.rowconfigure(1)
        message_window.rowconfigure(2)

        text_label.grid(column=1, row=1, padx=10, pady=5)
        accept_button.grid(column=1, row=2, padx=10, pady=5)
