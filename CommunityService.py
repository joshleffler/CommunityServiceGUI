from tkinter import *
from tkinter import messagebox
import sqlite3


def query_database(query):
    db_connection = sqlite3.connect('csdatabase.db')
    db_cursor = db_connection.cursor()

    db_cursor.execute(query)
    result = db_cursor.fetchall()

    db_connection.commit()
    db_connection.close()

    return result


def add_student():
    def commit_student():
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

    # <editor-fold desc="Create a new window">
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
    add_student_submit_button = Button(add_student_window, text="Add", command=commit_student, width=20, pady=10)
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
    add_student_submit_button.grid(row=5, column=1, pady=10, padx=(0, 10))
    # </editor-fold>


def add_hours():
    return


def display_student(info):
    # <editor-fold desc="Create window, title, and subtitle">

    # Process/format student info
    name = info[1] + " " + info[2]
    grade = "Grade " + str(info[3])
    id_num = "ID " + str(info[0])

    # Create window to display student info
    display_student_window = Toplevel()
    display_student_window.title(name)

    # Display student's name as a title at the top of the window
    title = Label(display_student_window, text=name)
    title.config(font=("Arial", 18))
    title.grid(row=0, column=0, columnspan=3, pady=(10, 0))

    # Display student's grade level and ID number as a subtitle at the top of the window
    subtitle = Label(display_student_window, text=(grade + " | " + id_num))
    subtitle.config(font=("Arial", 14))
    subtitle.grid(row=1, column=0, columnspan=3, pady=10, padx=10)

    # </editor-fold>

    # Connect to database
    db_connection = sqlite3.connect('csdatabase.db')
    db_cursor = db_connection.cursor()

    # Find all service records for student
    db_cursor.execute("SELECT * FROM service WHERE student_id == :student_id;",
                      {
                          "student_id": str(info[0]),
                      }
                      )

    result = db_cursor.fetchall()
    print(result)

    db_connection.commit()
    db_connection.close()


def select_student(results):
    def return_student(info):
        select_student_window.destroy()
        display_student(info)

    if len(results) == 0:
        messagebox.showinfo(title="No Results", message="No students matching that query were found.")
        return
    elif len(results) == 1:
        display_student(results[0])
    else:
        select_student_window = Toplevel()
        select_student_window.title("Select Student")

        title = Label(select_student_window, text="Multiple Results")
        title.config(font=("Arial", 18))
        title.grid(row=0, column=0, columnspan=4, pady=(10, 0))

        for i, student in enumerate(results):
            name = student[1] + " " + student[2]
            grade = "Grade " + str(student[3])
            id_num = "ID " + str(student[0])

            select_button = Button(select_student_window, text="Select",
                                   command=lambda student_temp=student: return_student(student_temp),
                                   padx=8, pady=8)
            student_name = Label(select_student_window, text=name)
            student_grade = Label(select_student_window, text=grade)
            student_id = Label(select_student_window, text=id_num)

            select_button.grid(row=i + 1, column=0, padx=5, pady=5)
            student_name.grid(row=i + 1, column=1)
            student_grade.grid(row=i + 1, column=2)
            student_id.grid(row=i + 1, column=3, padx=(0, 5))


def view_student():
    def search_by_id():
        # Connect to database
        db_connection = sqlite3.connect('csdatabase.db')
        db_cursor = db_connection.cursor()

        # Add new student to database
        db_cursor.execute("SELECT * FROM students WHERE student_id == :student_id;",
                          {
                              "student_id": str(student_id_entry.get()),
                          }
                          )

        result = db_cursor.fetchall()
        select_student(result)

        db_connection.commit()
        db_connection.close()

        # Close search student window
        search_student_window.destroy()

    def search_by_lname():
        # Connect to database
        db_connection = sqlite3.connect('csdatabase.db')
        db_cursor = db_connection.cursor()

        # Search database for any students with the specified last name
        db_cursor.execute("SELECT * FROM students WHERE UPPER(last_name) == UPPER(:last_name);",
                          {
                              "last_name": last_name_entry.get(),
                          }
                          )

        # Access and return any search results
        result = db_cursor.fetchall()
        select_student(result)

        # Close database connection
        db_connection.commit()
        db_connection.close()

        # Close search student window
        search_student_window.destroy()

    # <editor-fold desc="Create view student info window">
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
                               command=search_by_id, width=20, pady=10)
    last_name_button = Button(search_student_window, text="Search by last name", command=search_by_lname,
                              width=20, pady=10)
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
