from diaries_management import *
from gui_functions import *


def main_menu():
    print("What do you want to do?")
    print("1) List available diaries")
    print("2) Open a diary")
    print("3) Create a diary")
    print("4) Close the program")

    return int(input("Choose your option: "))


def main():
    # We do this to ensure the folder exists, otherwise we can't create the databases for the diaries
    if not does_diaries_folder_exist():
        os.mkdir(get_diaries_folder_path())

    draw_gui()


if __name__ == "__main__":
    main()
