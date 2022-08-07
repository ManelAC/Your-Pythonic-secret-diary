from diaries_management import *


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

    chosen_option = 0

    while chosen_option != 4:
        chosen_option = main_menu()

        if chosen_option == 1:
            list_available_diaries()
        elif chosen_option == 2:
            open_diary()
        elif chosen_option == 3:
            create_diary()
        elif chosen_option == 4:
            pass
        else:
            print("Wrong option")

        print("\n")

    print("\nThanks for using this program!")


if __name__ == "__main__":
    main()
