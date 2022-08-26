import os
import sqlite3
import base64
import bcrypt


class Diary:

    def __init__(self):
        self.open_diary_path = ""  # The path to the current open diary
        self.db_connection = None
        self.cursor = None
        self.diary_password = ""  # Auxiliary variable to store the password for the diary
        self.active_entry_date = ""  # Variable that stores the date of the active entry
        self.update_confirmation_window_answer = False  # Variable that stores if we have confirmed the entry update

    # Setters and getters
    def initialise_diary_instance_attributes(self):
        self.open_diary_path = ""
        self.db_connection = None
        self.cursor = None
        self.diary_password = ""
        self.active_entry_date = ""
        self.update_confirmation_window_answer = False

    def set_open_diary_path(self, selected_diary):
        self.open_diary_path = selected_diary

    def get_open_diary_path(self):
        return self.open_diary_path

    def set_db_connection(self, db):
        self.db_connection = db

    def get_db_connection(self):
        return self.db_connection

    def set_cursor(self, c):
        self.cursor = c

    def get_cursor(self):
        return self.cursor

    def set_diary_password(self, password):
        self.diary_password = password

    def get_diary_password(self):
        return self.diary_password

    def set_active_entry(self, date):
        self.active_entry_date = date

    def get_active_entry(self):
        return self.active_entry_date

    def get_text_from_active_entry(self):
        self.db_connection = sqlite3.connect(self.open_diary_path)
        self.cursor = self.db_connection.cursor()

        entry = self.cursor.execute("SELECT entry_text FROM diary_entries WHERE entry_date = :date", {"date": self.active_entry_date}).fetchall()

        return self.decrypt_text(entry[0][0])

    def get_diary_name(self):
        self.db_connection = sqlite3.connect(self.open_diary_path)
        self.cursor = self.db_connection.cursor()

        dn = self.cursor.execute("SELECT diary_name FROM diary_data").fetchall()

        return dn[0][0]

    def get_entries_from_open_diary(self):
        entry = self.cursor.execute("SELECT entry_date FROM diary_entries ORDER BY entry_date").fetchall()

        list_aux = []

        for i in range(len(entry)):
            list_aux.append(entry[i][0])

        for j in range(len(list_aux)):
            list_aux[j] = self.db_date_to_gui_date(list_aux[j])

        return list_aux

    @staticmethod
    def get_diaries_folder_path():
        return "../diaries"

    @staticmethod
    def get_diaries_extension():
        return ".secretdiary"

    @staticmethod
    def get_non_valid_characters():
        return "<>:\"/\\|?*"

    # Checking functions
    def does_diaries_folder_exist(self):
        if os.path.isdir(self.get_diaries_folder_path()):
            return True
        else:
            return False

    def is_diary_name_valid(self, string):
        for char in string:
            if char in self.get_non_valid_characters():
                return False

        return True

    # Other functions
    @staticmethod
    def db_date_to_gui_date(string_to_convert):
        # Convert a YYYYMMDD string to a DD/MM/YYYY string
        return f"{string_to_convert[6:8]}/{string_to_convert[4:6]}/{string_to_convert[0:4]}"

    @staticmethod
    def gui_date_to_db_date(string_to_convert):
        # Convert a DD/MM/YYYY string to a YYYYMMDD string
        return f"{string_to_convert[6:10]}{string_to_convert[3:5]}{string_to_convert[0:2]}"

    @staticmethod
    def encrypt_text(text):
        # This is a very simple form of cyphering
        aux_text = list(text)  # We do this because strings are immutable in Python: https://bobbyhadz.com/blog/python-typeerror-str-object-does-not-support-item-assignment
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

    @staticmethod
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

    # Diary management functions
    def create_diary(self, diary_name, diary_description, diary_password):
        diary_path = f"{self.get_diaries_folder_path()}/{diary_name}{self.get_diaries_extension()}"

        if os.path.isfile(diary_path):
            error_text = "ERROR: A diary with this name already exist, pick a new name."
            return error_text, False

        if not self.is_diary_name_valid(diary_name):
            error_text = f"ERROR: The following characters are not allowed: {self.get_non_valid_characters()}, try again."
            return error_text, False

        if len(diary_password) == 0:
            error_text = f"ERROR: The password can't be empty"
            return error_text, False

        encoded_password = base64.b64encode(diary_password.encode('ascii'))

        if (len(encoded_password) * 3) / 4 > 72:
            # Reason: https://stackoverflow.com/a/6793638
            error_text = f"ERROR: The password is too long"
            return error_text, False

        # We do this to ensure the folder exists, otherwise we can't create the databases for the diaries
        if not self.does_diaries_folder_exist():
            os.mkdir(self.get_diaries_folder_path())

        self.db_connection = sqlite3.connect(diary_path)
        self.cursor = self.db_connection.cursor()

        diary_data_table_sql_create = "CREATE TABLE diary_data (diary_name TEXT, diary_description TEXT, diary_password TEXT);"
        diary_data_table_sql_insert = "INSERT INTO diary_data VALUES (?, ?, ?)"
        diary_entries_table_sql_create = "CREATE TABLE diary_entries (entry_id INTEGER PRIMARY KEY, entry_date TEXT, entry_text TEXT);"

        salt = bcrypt.gensalt()

        hashed_diary_password = bcrypt.hashpw(base64.b64encode(diary_password.encode('ascii')), salt)

        self.cursor.execute(diary_data_table_sql_create)
        self.cursor.execute(diary_data_table_sql_insert, (diary_name, diary_description, hashed_diary_password))
        self.cursor.execute(diary_entries_table_sql_create)

        self.db_connection.commit()
        self.db_connection.close()

        return "Diary created successfully!", True

    def unlock_diary(self, password):
        diary_password = self.cursor.execute("SELECT diary_password FROM diary_data").fetchall()

        if not bcrypt.checkpw(base64.b64encode(password.encode('ascii')), diary_password[0][0]):
            self.open_diary_path = ""
            self.cursor.close()
            self.db_connection.close()
            error_text = f"ERROR: Wrong password, open the diary again"
            return error_text, False

        return "", True

    def open_diary(self):
        if self.open_diary_path == "":
            return "ERROR: No diary has been selected", False
        else:
            self.db_connection = sqlite3.connect(self.open_diary_path)
            self.cursor = self.db_connection.cursor()
            return "", True

    def close_diary(self):
        if self.db_connection is not None:
            # self.db_connection.commit()
            self.db_connection.close()

        self.initialise_diary_instance_attributes()  # We reset the variables to their initial state

    def add_entry(self, day, month, year):
        entry_sql_insert = "INSERT INTO diary_entries(entry_date, entry_text) VALUES (?, ?)"

        entry_date = f"{year:04}{month:02}{day:02}"

        self.cursor.execute(entry_sql_insert, (entry_date, ""))
        self.db_connection.commit()

    def update_entry(self, entry_text):
        diary_entries_table_sql_update_entry = "UPDATE diary_entries SET entry_text = ? WHERE entry_date = ?;"

        self.cursor.execute(diary_entries_table_sql_update_entry, (self.encrypt_text(entry_text), self.get_active_entry()))

        self.db_connection.commit()

    def delete_entry(self):
        entry_sql_delete = "DELETE FROM diary_entries WHERE entry_date = ?;"
        self.cursor.execute(entry_sql_delete, (self.get_active_entry(),))
        self.db_connection.commit()

        self.active_entry_date = ""
