import os
import sqlite3
import base64
import bcrypt
import tkinter
from tkinter import ttk

# Global variables
global open_diary_var  # The path to the current open diary
global db_connection
global cursor
global global_pass  # Auxiliary variable to store the password for the diary
global open_entry_bool  # Boolean that stores if there's an open entry or not
global open_entry_date  # Variable that stores the date of the current open entry
global screen_width_var  # Variable that stores the screen width
global screen_height_var  # Variable that stores the screen height
global update_confirmation_window_answer  # Variable that stores if we have confirmed the entry update


# Setters and getters
def set_open_diary(selected_diary):
    global open_diary_var
    open_diary_var = selected_diary


def get_open_diary():
    return open_diary_var


def get_entries_from_open_diary():
    entry = cursor.execute("SELECT entry_date FROM diary_entries ORDER BY entry_date").fetchall()

    list_aux = []

    for i in range(len(entry)):
        list_aux.append(entry[i][0])

    for j in range(len(list_aux)):
        list_aux[j] = date_format_from_db_to_string(list_aux[j])

    return list_aux


def get_diaries_folder_path():
    return "../diaries"


def get_diaries_extension():
    return ".secretdiary"


def get_non_valid_characters():
    return "<>:\"/\\|?*"


def get_valid_date():
    correct_date = False

    day, month, year = 0, 0, 0

    while not correct_date:
        day = int(input("Introduce the day in number format: "))
        while day <= 0 or day >= 32:
            day = int(input("Wrong day, introduce it again: "))

        month = int(input("Introduce the month in number format: "))
        while month <= 0 or month >= 13:
            month = int(input("Wrong month, introduce it again: "))

        year = int(input("Introduce the year in number format: "))
        while year <= -1 or year >= 10000:
            year = int(input("Wrong year, introduce it again: "))

        # The following bit is from: https://stackoverflow.com/a/51981596
        number_of_days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            number_of_days_per_month[1] = 29

        if day > number_of_days_per_month[month - 1]:
            print("Wrong date, introduce it again!")
        else:
            correct_date = True

    return f"{year:04}{month:02}{day:02}"


def set_active_entry(date):
    global open_entry_bool
    global open_entry_date
    open_entry_bool = True
    open_entry_date = date_format_from_string_to_db(date)


def get_active_entry():
    return open_entry_date


def get_text_from_active_entry():
    global db_connection
    global cursor
    db_connection = sqlite3.connect(open_diary_var)
    cursor = db_connection.cursor()

    entry = cursor.execute("SELECT entry_text FROM diary_entries WHERE entry_date = :date", {"date": open_entry_date}).fetchall()

    return decrypt_text(entry[0][0])


def set_global_pass(password_box, afpw):
    global global_pass
    global_pass = password_box.get()
    afpw.destroy()


def get_diary_name():
    global db_connection
    global cursor
    db_connection = sqlite3.connect(open_diary_var)
    cursor = db_connection.cursor()

    dn = cursor.execute("SELECT diary_name FROM diary_data").fetchall()

    return dn[0][0]


def initialise_global_variables_from_diaries_functions():
    global open_diary_var
    global db_connection
    global cursor
    global global_pass
    global open_entry_bool
    global open_entry_date

    open_entry_bool = ""
    db_connection = ""
    cursor = ""
    global_pass = ""
    open_diary_var = False
    open_entry_date = ""


def set_screen_width_var(value):
    global screen_width_var
    screen_width_var = value


def get_screen_width_var():
    return screen_width_var


def set_screen_height_var(value):
    global screen_height_var
    screen_height_var = value


def get_screen_height_var():
    return screen_height_var


def get_app_main_window_width():
    return 800


def get_app_main_window_height():
    return 600


def set_already_active_entry_window_answer(answer, ucw):
    global update_confirmation_window_answer
    update_confirmation_window_answer = answer
    ucw.destroy()


# Checking functions
def does_diaries_folder_exist():
    if os.path.isdir(get_diaries_folder_path()):
        return True
    else:
        return False


def is_diary_name_valid(string):
    for char in string:
        if char in get_non_valid_characters():
            return False

    return True


# Windows creation functions
def create_message_window(message_text, message_type):
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

    center_x = int(get_screen_width_var() / 2 - diary_window_width / 2)
    center_y = int(get_screen_height_var() / 2 - diary_window_height / 2)

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


def ask_for_password_window():
    afpw = tkinter.Toplevel()
    afpw.title("Introduce the password for this diary")

    diary_window_width = 400
    diary_window_height = 200

    center_x = int(get_screen_width_var() / 2 - diary_window_width / 2)
    center_y = int(get_screen_height_var() / 2 - diary_window_height / 2)

    afpw.geometry(f'+{center_x}+{center_y}')

    afpw.attributes('-topmost', True)
    afpw.focus_force()
    afpw.update()
    afpw.attributes('-topmost', False)

    afpw.iconbitmap('../assets/diary.ico')

    password_label = ttk.Label(afpw, text="Introduce the password for this diary")

    password = tkinter.StringVar()
    password_box = ttk.Entry(afpw, textvariable=password, show="*")
    open_diary_button = ttk.Button(afpw, text="Open diary", command=lambda: set_global_pass(password_box, afpw))

    password_box.focus()

    afpw.columnconfigure(1, weight=1)

    afpw.rowconfigure(1)
    afpw.rowconfigure(2)
    afpw.rowconfigure(3)

    password_label.grid(column=1, row=1, sticky="W", padx=5)
    password_box.grid(column=1, row=2, sticky="EW", padx=5)
    open_diary_button.grid(column=1, row=3, sticky="S", pady=5)

    return afpw


def update_confirmation_window():
    ucw = tkinter.Toplevel()
    ucw.title("Choose an action")

    diary_window_width = 400
    diary_window_height = 200

    center_x = int(get_screen_width_var() / 2 - diary_window_width / 2)
    center_y = int(get_screen_height_var() / 2 - diary_window_height / 2)

    # ucw.geometry(f'{diary_window_width}x{diary_window_height}+{center_x}+{center_y}')
    ucw.geometry(f'+{center_x}+{center_y}')

    ucw.attributes('-topmost', True)
    ucw.focus_force()
    ucw.update()
    ucw.attributes('-topmost', False)

    ucw.iconbitmap('../assets/diary.ico')

    aux_test1 = f"Are you sure you want to save the changes made in this entry?"

    text_label1 = ttk.Label(ucw, text=aux_test1)

    yes_button = ttk.Button(ucw, text="Yes", command=lambda: set_already_active_entry_window_answer(True, ucw))
    no_button = ttk.Button(ucw, text="No", command=lambda: set_already_active_entry_window_answer(False, ucw))

    ucw.columnconfigure(1)
    ucw.columnconfigure(2)

    ucw.rowconfigure(1)
    ucw.rowconfigure(2)

    text_label1.grid(column=1, row=1, sticky="N", padx=5, columnspan=2)

    yes_button.grid(column=1, row=4, sticky="N", padx=5)
    no_button.grid(column=2, row=4, sticky="N", padx=5)

    return ucw


# Other functions
def date_format_from_db_to_string(string_to_convert):
    # Convert a YYYYMMDD string to a DD/MM/YYYY string
    return f"{string_to_convert[6:8]}/{string_to_convert[4:6]}/{string_to_convert[0:4]}"


def date_format_from_string_to_db(string_to_convert):
    # Convert a DD/MM/YYYY string to a YYYYMMDD string
    return f"{string_to_convert[6:10]}{string_to_convert[3:5]}{string_to_convert[0:2]}"


def open_diary_menu():
    print("\nWhat do you want to do?")
    print("1) Read entry")
    print("2) Add entry")
    print("3) Close this diary")

    return int(input("Choose your option: "))


def encrypt_text(text):
    # This is a very simple form of cyphering
    aux_text = list(text) # We do this because strings are immutable in Python: https://bobbyhadz.com/blog/python-typeerror-str-object-does-not-support-item-assignment
    lowercase_string = "abcdefghijklmnopqrstuvwxyz"
    uppercase_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers_string = "0123456789"

    for i in range(len(aux_text)):
        if aux_text[i] in lowercase_string:
            aux_text[i] = lowercase_string[(lowercase_string.find(aux_text[i]) + len(aux_text)) % len(lowercase_string)]
        elif aux_text[i] in uppercase_string:
            aux_text[i] = uppercase_string[(uppercase_string.find(aux_text[i]) + len(aux_text)) % len(uppercase_string)]
        elif aux_text[i] in numbers_string:
            aux_text[i] = numbers_string[(numbers_string.find(aux_text[i]) + len(aux_text)) % len(numbers_string)]

    text = ''.join(aux_text)

    return text


def decrypt_text(text):
    aux_text = list(text)
    lowercase_string = "abcdefghijklmnopqrstuvwxyz"
    uppercase_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers_string = "0123456789"

    for i in range(len(aux_text)):
        if aux_text[i] in lowercase_string:
            aux_text[i] = lowercase_string[(lowercase_string.find(aux_text[i]) - len(aux_text)) % len(lowercase_string)]
        elif aux_text[i] in uppercase_string:
            aux_text[i] = uppercase_string[(uppercase_string.find(aux_text[i]) - len(aux_text)) % len(uppercase_string)]
        elif aux_text[i] in numbers_string:
            aux_text[i] = numbers_string[(numbers_string.find(aux_text[i]) - len(aux_text)) % len(numbers_string)]

    text = ''.join(aux_text)

    return text


def update_entry(entry_text):
    aux = update_confirmation_window()
    aux.wait_window()

    if update_confirmation_window_answer:
        diary_entries_table_sql_update_entry = "UPDATE diary_entries SET entry_text = ? WHERE entry_date = ?;"

        cursor.execute(diary_entries_table_sql_update_entry, (encrypt_text(entry_text), get_active_entry()))

        db_connection.commit()


def add_entry(db_connection, cursor):
    print("Please, introduce the date for this entry")

    entry_date = get_valid_date()

    print("What do you want to write in the entry?")
    entry_text = input()

    encrypted_text = encrypt_text(entry_text)

    entry_sql_insert = "INSERT INTO diary_entries(entry_date, entry_text) VALUES (?, ?)"

    cursor.execute(entry_sql_insert, (entry_date, encrypted_text))
    db_connection.commit()


def delete_entry():
    entry_sql_delete = "DELETE FROM diary_entries WHERE entry_date = ?;"
    cursor.execute(entry_sql_delete, (get_active_entry(),))
    db_connection.commit()

    global open_diary_var
    open_diary_var = ""


def open_diary():
    if len(open_diary_var) == 0:
        error_text = "ERROR: No diary has been selected"
        create_message_window(error_text, 0)
    else:
        global db_connection
        global cursor
        db_connection = sqlite3.connect(open_diary_var)
        cursor = db_connection.cursor()

        aux = ask_for_password_window()
        aux.wait_window()

        diary_password = cursor.execute("SELECT diary_password FROM diary_data").fetchall()

        temp_pass = global_pass

        if not bcrypt.checkpw(base64.b64encode(temp_pass.encode('ascii')), diary_password[0][0]):
            error_text = f"ERROR: Wrong password, open the diary again"
            create_message_window(error_text, 0)
            set_open_diary("")
            cursor.close()
            db_connection.close()


def create_diary(diary_name, diary_description, diary_password):
    diary_path = f"{get_diaries_folder_path()}/{diary_name}{get_diaries_extension()}"

    can_create_diary = True
    diary_already_exists = False

    if os.path.isfile(diary_path):
        error_text = "ERROR: A diary with this name already exist, pick a new name."
        create_message_window(error_text, 0)
        can_create_diary = False
        diary_already_exists = True

    if not is_diary_name_valid(diary_name):
        error_text = f"ERROR: The following characters are not allowed: {get_non_valid_characters()}, try again."
        create_message_window(error_text, 0)
        can_create_diary = False

    if len(diary_password) == 0 and not diary_already_exists:
        error_text = f"ERROR: The password can't be empty"
        create_message_window(error_text, 0)
        can_create_diary = False

    encoded_password = base64.b64encode(diary_password.encode('ascii'))

    if (len(encoded_password) * 3) / 4 > 72:
        # Reason: https://stackoverflow.com/a/6793638
        error_text = f"ERROR: The password is too long"
        create_message_window(error_text, 0)
        can_create_diary = False

    if can_create_diary:
        # We do this to ensure the folder exists, otherwise we can't create the databases for the diaries
        if not does_diaries_folder_exist():
            os.mkdir(get_diaries_folder_path())

        db_connection = sqlite3.connect(diary_path)
        cursor = db_connection.cursor()

        diary_data_table_sql_create = "CREATE TABLE diary_data (diary_name TEXT, diary_description TEXT, diary_password TEXT);"
        diary_data_table_sql_insert = "INSERT INTO diary_data VALUES (?, ?, ?)"
        diary_entries_table_sql_create = "CREATE TABLE diary_entries (entry_id INTEGER PRIMARY KEY, entry_date TEXT, entry_text TEXT);"

        salt = bcrypt.gensalt()

        hashed_diary_password = bcrypt.hashpw(base64.b64encode(diary_password.encode('ascii')), salt)

        cursor.execute(diary_data_table_sql_create)
        cursor.execute(diary_data_table_sql_insert, (diary_name, diary_description, hashed_diary_password))
        cursor.execute(diary_entries_table_sql_create)

        db_connection.commit()
        db_connection.close()

        create_message_window("Diary created successfully!", 1)


def close_diary():
    if db_connection != "":
        db_connection.commit()
        db_connection.close()

    initialise_global_variables_from_diaries_functions()  # We reset the variables to their initial state
