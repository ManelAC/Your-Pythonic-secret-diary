from diaries_management_functions import *
from gui_functions import *


def main():
    # We do this to ensure the folder exists, otherwise we can't create the databases for the diaries
    if not does_diaries_folder_exist():
        os.mkdir(get_diaries_folder_path())

    main_gui()


if __name__ == "__main__":
    main()
