import os
import sqlite3
import base64
import bcrypt


def opened_diary_menu():
    print("\nWhat do you want to do?")
    print("1) Read entry")
    print("2) Add entry")
    print("3) Close this diary")

    return int(input("Choose your option: "))


def get_diaries_folder_path():
    return "../diaries"


def get_diaries_extension():
    return ".secretdiary"


def does_diaries_folder_exist():
    if os.path.isdir(get_diaries_folder_path()):
        return True
    else:
        return False


def print_error_missing_diaries_folder():
    print("No diaries folder available")
    print("Restart the program making sure you have writing permissions")


def get_non_valid_characters():
    return "<>:\"/\\|?*"


def is_diary_name_valid(string):
    for char in string:
        if char in get_non_valid_characters():
            return False

    return True


def get_entry_date(cursor):
    print("\nThese are the available entries:")
    date_list = cursor.execute("SELECT entry_date FROM diary_entries").fetchall()

    i = 1
    for elem in date_list:
        aux_string = f"{i}) {elem[0][6:8]}/{elem[0][4:6]}/{elem[0][0:4]}"
        print(aux_string)
        i += 1

    selected_entry = int(input("Which entry you want to read? Select its number: "))

    while selected_entry < 1 or selected_entry > len(date_list):
        selected_entry = int(input("Wrong entry number, pick again: "))

    return date_list[selected_entry-1][0]


def read_entry(cursor):
    entry = cursor.execute("SELECT entry_text FROM diary_entries WHERE entry_date = :date", {"date": get_entry_date(cursor)}).fetchall()

    print(decrypt_text(entry[0][0]))


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


# A very simple form of encryption
def encrypt_text(text):
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


def update_entry():
    # We will need this when we have the GUI and we select a date that already has an entry
    print("To do")


def add_entry(db_connection, cursor):
    print("Please, introduce the date for this entry")

    entry_date = get_valid_date()

    print("What do you want to write in the entry?")
    entry_text = input()

    encrypted_text = encrypt_text(entry_text)

    entry_sql_insert = "INSERT INTO diary_entries(entry_date, entry_text) VALUES (?, ?)"

    cursor.execute(entry_sql_insert, (entry_date, encrypted_text))
    db_connection.commit()


def get_available_diaries():
    if not does_diaries_folder_exist():
        print_error_missing_diaries_folder()
    else:
        present_files = os.listdir(get_diaries_folder_path())

        present_diaries = []

        for file in present_files:
            if file.find(get_diaries_extension()) != -1:
                present_diaries.append(file.replace(get_diaries_extension(), ""))

        return present_diaries


def list_available_diaries():
    diaries = get_available_diaries()

    if len(diaries) == 0:
        print("\nNo diaries available")
    else:
        print("\nThese are the available diaries:")
        for i in range(len(diaries)):
            string = f"{i+1}) {diaries[i]}"
            print(string)


def open_diary():
    list_available_diaries()

    diaries = get_available_diaries()

    if len(diaries) == 0:
        print("Create a diary first!")
    else:
        chosen_option = int(input("Which diary you want to open? Select its number: "))

        while chosen_option not in range(1, len(diaries)+1):
            chosen_option = int(input("Wrong option! Select another diary: "))

        diary_path = f"{get_diaries_folder_path()}/{diaries[chosen_option-1]}{get_diaries_extension()}"

        db_connection = sqlite3.connect(diary_path)
        cursor = db_connection.cursor()

        diary_password = cursor.execute("SELECT diary_password FROM diary_data").fetchall()

        password = input("Please introduce the password of this diary: ")

        while not bcrypt.checkpw(base64.b64encode(password.encode('ascii')), diary_password[0][0]):
            password = input("Wrong password, please introduce the password of this diary again: ")

        chosen_option = 0

        while chosen_option != 3:
            chosen_option = opened_diary_menu()

            if chosen_option == 1:
                read_entry(cursor)
            elif chosen_option == 2:
                add_entry(db_connection, cursor)
            elif chosen_option == 3:
                db_connection.commit()
                db_connection.close()
            else:
                print("Wrong option")


def create_diary():
    diary_name = input("Introduce the diary name: ")
    diary_path = f"{get_diaries_folder_path()}/{diary_name}{get_diaries_extension()}"

    while os.path.isfile(diary_path):
        print("This diary already exists, try again.")
        diary_name = input("Introduce the diary name: ")
        diary_path = f"{get_diaries_folder_path()}/{diary_name}{get_diaries_extension()}"

    while not is_diary_name_valid(diary_name):
        aux_string = f"The following characters are not allowed: {get_non_valid_characters()}, try again."
        print(aux_string)
        diary_name = input("Introduce the diary name: ")

    diary_description = input("Introduce the diary description: ")

    diary_password = input("Introduce the diary password: ")

    encoded_password = base64.b64encode(diary_password.encode('ascii'))

    correct_password = False

    while not correct_password:
        if len(diary_password) == 0:
            print("The password can't be empty")
            diary_password = input("Introduce a new diary password: ")
        elif (len(encoded_password)*3)/4 > 72:
            # Reason: https://stackoverflow.com/a/6793638
            print("The password is too long")
            diary_password = input("Introduce a new diary password: ")
        else:
            correct_password = True

    # We do this to ensure the folder exists, otherwise we can't create the databases for the diaries
    if not does_diaries_folder_exist():
        os.mkdir(get_diaries_folder_path())

    db_connection = sqlite3.connect(diary_path)
    cursor = db_connection.cursor()

    diary_data_table_sql_create = "CREATE TABLE diary_data (diary_name TEXT, diary_description TEXT, diary_password TEXT);"
    diary_data_table_sql_insert = "INSERT INTO diary_data VALUES (?, ?, ?)"
    diary_entries_table_sql_create = "CREATE TABLE diary_entries (entry_id INTEGER PRIMARY KEY, entry_date TEXT, entry_text TEXT);"

    print("Creating diary...")

    salt = bcrypt.gensalt()

    hashed_diary_password = bcrypt.hashpw(base64.b64encode(diary_password.encode('ascii')), salt)

    cursor.execute(diary_data_table_sql_create)
    cursor.execute(diary_data_table_sql_insert, (diary_name, diary_description, hashed_diary_password))
    cursor.execute(diary_entries_table_sql_create)

    db_connection.commit()
    db_connection.close()

    print("Diary created successfully!")
