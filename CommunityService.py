from tkinter import *
from tkinter import messagebox
import sqlite3

global add_student_window
global search_student_window


def query_database(query):
    db_connection = sqlite3.connect('csdatabase.db')
    db_cursor = db_connection.cursor()

    db_cursor.execute(query)
    result = db_cursor.fetchall()

    db_connection.commit()
    db_connection.close()

    return result


def commit_student(student_id_entry, first_name_entry, last_name_entry, grade_entry):
    # TODO verify user responses (not blank, integers are integers, student ID is unique)

    # Connect to database
    db_connection = sqlite3.connect('csdatabase.db')
    db_cursor = db_connection.cursor()

    # Add new student to database
    db_cursor.execute("INSERT INTO students (student_id, first_name, last_name, grade) VALUES (:student_id, "
                      ":first_name, :last_name, :grade);",
                      {
                          "student_id": student_id_entry.get(),
                          "first_name": first_name_entry.get(),
                          "last_name": last_name_entry.get(),
                          "grade": grade_entry.get()
                      }
                      )

    db_connection.commit()
    db_connection.close()

    # Close add student window
    add_student_window.destroy()


def add_student():
    # <editor-fold desc="Create a new window">
    global add_student_window
    add_student_window = Toplevel()
    add_student_window.title("Add a Student")
    # </editor-fold>

    # <editor-fold desc="Create the add student window's elements">
    title = Label(add_student_window, text="Add a Student")
    title.config(font=("Arial", 18))

    student_id_label = Label(add_student_window, text="Student ID")
    first_name_label = Label(add_student_window, text="First Name")
    last_name_label = Label(add_student_window, text="Last Name")
    grade_label = Label(add_student_window, text="Grade")

    student_id_entry = Entry(add_student_window, width=20)
    first_name_entry = Entry(add_student_window, width=20)
    last_name_entry = Entry(add_student_window, width=20)
    grade_entry = Entry(add_student_window, width=20)

    add_student_exit_button = Button(add_student_window, text="Cancel", command=add_student_window.destroy, width=15,
                                     pady=10)
    add_student_submit_button = Button(add_student_window, text="Add",
                                       command=lambda: commit_student(student_id_entry, first_name_entry,
                                                                      last_name_entry, grade_entry), width=20, pady=10)
    # </editor-fold>

    # <editor-fold desc="Place the add student window's elements">
    title.grid(row=0, column=0, columnspan=2, pady=(10, 0))

    student_id_label.grid(row=1, column=0)
    first_name_label.grid(row=2, column=0)
    last_name_label.grid(row=3, column=0)
    grade_label.grid(row=4, column=0)

    student_id_entry.grid(row=1, column=1, padx=(0, 10))
    first_name_entry.grid(row=2, column=1, padx=(0, 10))
    last_name_entry.grid(row=3, column=1, padx=(0, 10))
    grade_entry.grid(row=4, column=1, padx=(0, 10))

    add_student_exit_button.grid(row=5, column=0, pady=10, padx=10)
    add_student_submit_button.grid(row=5, column=1, pady=10, padx=(0,10))
    # </editor-fold>


def add_hours():
    return


def view_student_by_id(student_id_entry):
    # TODO check that ID was entered, is integer, check that ID exists

    # Connect to database
    db_connection = sqlite3.connect('csdatabase.db')
    db_cursor = db_connection.cursor()

    # Add new student to database
    # TODO
    # db_cursor.execute("INSERT INTO students (student_id, first_name, last_name, grade) VALUES (:student_id, "
    #                   ":first_name, :last_name, :grade);",
    #                   {
    #                       "student_id": student_id_entry.get(),
    #                       "first_name": first_name_entry.get(),
    #                       "last_name": last_name_entry.get(),
    #                       "grade": grade_entry.get()
    #                   }
    #                   )

    db_connection.commit()
    db_connection.close()

    # Close search student window
    search_student_window.destroy()


def view_student_by_lname():
    return


def view_student():
    # <editor-fold desc="Create view student info window">
    global search_student_window
    search_student_window = Toplevel()
    search_student_window.title("View Student Info")
    # </editor-fold>

    # <editor-fold desc="Create elements for view student info window">
    title = Label(search_student_window, text="View Student Info")
    title.config(font=("Arial", 18))

    student_id_label = Label(search_student_window, text="Student ID")
    last_name_label = Label(search_student_window, text="Last Name")

    student_id_entry = Entry(search_student_window, width=20)
    last_name_entry = Entry(search_student_window, width=20)

    student_id_button = Button(search_student_window, text="Search by student ID",
                               command=lambda: view_student_by_id(student_id_entry), width=20, pady=10)
    last_name_button = Button(search_student_window, text="Search by last name", command=view_student_by_lname(),
                              width=20, pady=10, state=DISABLED)
    search_window_exit_button = Button(search_student_window, text="Cancel", command=search_student_window.destroy,
                                       width=15, pady=10)
    # </editor-fold>

    # <editor-fold desc="Place elements for student info window">
    title.grid(row=0, column=0, columnspan=2, pady=(10, 0))

    student_id_label.grid(row=1, column=0, padx=(10, 0))
    student_id_entry.grid(row=1, column=1, padx=(0, 10))
    student_id_button.grid(row=2, column=0, columnspan=2, pady=(5, 15))

    last_name_label.grid(row=3, column=0, padx=(10, 0))
    last_name_entry.grid(row=3, column=1, pady=(0, 10))
    last_name_button.grid(row=4, column=0, columnspan=2, pady=(5, 15))

    search_window_exit_button.grid(row=5, column=0, columnspan=2, pady=(0, 10))
    # </editor-fold>


def view_report():
    return


if __name__ == "__main__":
    # <editor-fold desc="Create the main screen">
    main_screen = Tk()
    main_screen.title("Community Service Tracker")
    # main_screen.geometry("500x200")
    # </editor-fold>

    # <editor-fold desc="Create the main menu elements">
    # Main menu title
    title = Label(main_screen, text="Welcome to the Community Service Tracker!")
    title.config(font=("Arial", 24))

    # Main menu buttons
    add_student_button = Button(main_screen, text="Add a Student", command=add_student, width=30, pady=30)
    add_hours_button = Button(main_screen, text="Add Service Hours", command=add_hours, width=30, pady=30)
    view_student_button = Button(main_screen, text="View Student Info", command=view_student, width=30, pady=30)
    view_report_button = Button(main_screen, text="View Service Report", command=view_report, width=30, pady=30)
    exit_button = Button(main_screen, text="Exit", command=main_screen.quit, width=30, pady=30)
    # </editor-fold>

    # <editor-fold desc="Place main menu elements on screen">
    title.grid(row=0, column=0, pady=(10, 0), padx=10)
    add_student_button.grid(row=1, column=0, pady=(10, 0))
    add_hours_button.grid(row=2, column=0, pady=(10, 0))
    view_student_button.grid(row=3, column=0, pady=(10, 0))
    view_report_button.grid(row=4, column=0, pady=(10, 0))
    exit_button.grid(row=5, column=0, pady=10)
    # </editor-fold>

    main_screen.mainloop()
