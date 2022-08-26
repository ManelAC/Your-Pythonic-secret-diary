from diary_class import Diary
from gui_class import GUI


if __name__ == "__main__":
    my_diary = Diary()
    GUI = GUI(my_diary)

    GUI.get_gui_root().mainloop()
