# Community Service Tracker
# AP Computer Science Principles final project (Create)
# Josh Leffler
# March/April 2020

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import datetime


def is_valid_int(input_to_test):
    try:
        int(input_to_test)
        return True
    except ValueError:
        return False


def is_valid_date(month, day, year):
    try:
        datetime.datetime(year, month, day)
        return True
    except ValueError:
        return False


def add_student():
    def commit_student():
        # Check that the user input is valid
        valid_id = is_valid_int(student_id_entry.get())
        valid_fname = first_name_entry.get() != ""
        valid_lname = last_name_entry.get() != ""
        valid_grade = is_valid_int(grade_entry.get()) and 9 <= int(grade_entry.get()) <= 12

        if valid_id and valid_fname and valid_lname and valid_grade:
            # Check that the user is inputting a unique student ID
            try:
                # Connect to database
                db_connection = sqlite3.connect('csdatabase.db')
                db_cursor = db_connection.cursor()

                # Add new student to database
                db_cursor.execute("INSERT INTO students (student_id, first_name, last_name, grade) VALUES ("
                                  ":student_id, :first_name, :last_name, :grade);",
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

            except sqlite3.IntegrityError:
                messagebox.showerror(title="Invalid Input",
                                     message="Student with this student ID already exists.")

        else:
            messagebox.showerror(title="Invalid Input",
                                 message="Please enter valid information (student ID is digits only, first and last "
                                         "names aren't blank, and grade between 9 and 12).")

    # <editor-fold desc="Create a new window">
    add_student_window = Toplevel()
    add_student_window.title("Add a Student")
    # </editor-fold>

    # <editor-fold desc="Create the add student window's elements">
    add_student_title = Label(add_student_window, text="Add a Student")
    add_student_title.config(font=("Arial", 18))

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
    add_student_title.grid(row=0, column=0, columnspan=2, pady=(10, 0))

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
    # Called once the student has been selected
    def add_hours_to_student(info):
        # Called when the user is ready to add the inputted information to the database
        def commit_hours():
            # Process user input for input into SQL
            month_numbers = {
                "   January": "01",
                "   February": "02",
                "   March": "03",
                "   April": "04",
                "   May": "05",
                "   June": "06",
                "   July": "07",
                "   August": "08",
                "   September": "09",
                "   October": "10",
                "   November": "11",
                "   December": "12",
            }
            month_num = month_numbers[selected_month.get()]

            # Check that user input is valid
            # noinspection PyPep8
            valid_date = is_valid_int(day_entry.get()) and is_valid_int(year_entry.get()) and is_valid_date(int(month_num), int(day_entry.get()), int(year_entry.get()))
            valid_organization = organization_entry.get() != ""
            valid_hours = is_valid_int(hours_entry.get()) and int(hours_entry.get()) > 0

            if valid_date and valid_organization and valid_hours:
                day_num = str(day_entry.get())
                year_num = str(year_entry.get())

                # Convert one-digit day numbers to two digits
                if len(day_num) == 1:
                    day_num = "0" + day_num

                date_string = year_num + "-" + month_num + "-" + day_num

                # Connect to database
                db_connection = sqlite3.connect('csdatabase.db')
                db_cursor = db_connection.cursor()

                # Add new hours to database
                db_cursor.execute("INSERT INTO service (student_id, date, organization, hours) VALUES (:student_id, "
                                  ":date, :organization, :hours);",
                                  {
                                      "student_id": id_num,
                                      "date": date_string,
                                      "organization": organization_entry.get(),
                                      "hours": hours_entry.get()
                                  }
                                  )

                db_connection.commit()
                db_connection.close()

                # Close add student window
                add_hours_window.destroy()

            else:
                messagebox.showerror(title="Invalid Input",
                                     message="Please enter valid information (valid date, organization name isn't "
                                             "blank, and an integer greater than 0 for hours).")

        # Format the student's information
        id_num = int(info[0])
        name = info[1] + " " + info[2]

        # <editor-fold desc="Create a new window">
        add_hours_window = Toplevel()
        add_hours_window.title("Add Hours")
        # </editor-fold>

        # <editor-fold desc="Create the add hours window's elements">
        add_hours_title = Label(add_hours_window, text=("Add Hours for " + name))
        add_hours_title.config(font=("Arial", 18))

        month_label = Label(add_hours_window, text="Month")
        day_label = Label(add_hours_window, text="Day")
        year_label = Label(add_hours_window, text="Year")
        organization_label = Label(add_hours_window, text="Organization")
        hours_label = Label(add_hours_window, text="Hours of Service")

        months = ["   January", "   February", "   March", "   April", "   May", "   June", "   July", "   August",
                  "   September", "   October", "   November", "   December"]
        selected_month = StringVar()
        selected_month.set(months[0])

        month_entry = OptionMenu(add_hours_window, selected_month, *months)
        month_entry.configure(anchor="w")
        day_entry = Entry(add_hours_window, width=20)
        year_entry = Entry(add_hours_window, width=20)
        organization_entry = Entry(add_hours_window, width=20)
        hours_entry = Entry(add_hours_window, width=20)

        add_hours_exit_button = Button(add_hours_window, text="Cancel", command=add_hours_window.destroy, width=15,
                                       pady=10)
        add_hours_submit_button = Button(add_hours_window, text="Add", command=commit_hours, width=20, pady=10)
        # </editor-fold>

        # <editor-fold desc="Place the add hours window's elements">
        add_hours_title.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        month_label.grid(row=1, column=0)
        day_label.grid(row=2, column=0)
        year_label.grid(row=3, column=0)
        organization_label.grid(row=4, column=0)
        hours_label.grid(row=5, column=0)

        month_entry.grid(row=1, column=1, padx=(0, 10), sticky="ew")
        day_entry.grid(row=2, column=1, padx=(0, 10))
        year_entry.grid(row=3, column=1, padx=(0, 10))
        organization_entry.grid(row=4, column=1, padx=(0, 10))
        hours_entry.grid(row=5, column=1, padx=(0, 10))

        add_hours_exit_button.grid(row=6, column=0, pady=10, padx=10)
        add_hours_submit_button.grid(row=6, column=1, pady=10, padx=(0, 10))
        # </editor-fold>

    # Called to select the correct result after the database has been queried
    def select_student(results):
        # Called when the user picked from multiple results
        def return_student(info):
            select_student_window.destroy()
            add_hours_to_student(info)

        # If the search had no results, notify the user
        if len(results) == 0:
            messagebox.showinfo(title="No Results", message="No students matching that query were found.")
            return
        # If the search had one result, select that result and proceed
        elif len(results) == 1:
            add_hours_to_student(results[0])
        # If the search had more than one result, allow the user to select which result they want
        else:
            # Create and configure a window
            select_student_window = Toplevel()
            select_student_window.title("Select Student")

            select_student_title = Label(select_student_window, text="Multiple Results")
            select_student_title.config(font=("Arial", 18))
            select_student_title.grid(row=0, column=0, columnspan=4, pady=(10, 0))

            # For each result, create a row and a button that the user can use to select that result
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

    # Called when the "search by student ID" button is pressed
    def search_by_id():
        # Connect to database
        db_connection = sqlite3.connect('csdatabase.db')
        db_cursor = db_connection.cursor()

        # Search database for any students with the specified student ID
        db_cursor.execute("SELECT * FROM students WHERE student_id == :student_id;",
                          {
                              "student_id": str(student_id_entry.get()),
                          }
                          )

        # Close search student window
        search_student_window.destroy()

        # Access and return any search results
        result = db_cursor.fetchall()
        select_student(result)

        # Close database connection
        db_connection.commit()
        db_connection.close()

    # Called when the "search by last name" button is pressed
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

        # Close search student window
        search_student_window.destroy()

        # Access and return any search results
        result = db_cursor.fetchall()
        select_student(result)

        # Close database connection
        db_connection.commit()
        db_connection.close()

    # <editor-fold desc="Create add hours window">
    search_student_window = Toplevel()
    search_student_window.title("Select a Student")
    # </editor-fold>

    # <editor-fold desc="Create elements for add hours window">
    add_hours_select_student_title = Label(search_student_window, text="Select a Student")
    add_hours_select_student_title.config(font=("Arial", 18))

    student_id_label = Label(search_student_window, text="Student ID")
    last_name_label = Label(search_student_window, text="Last Name")

    student_id_entry = Entry(search_student_window, width=20)
    last_name_entry = Entry(search_student_window, width=20)

    student_id_button = Button(search_student_window, text="Search by student ID", command=search_by_id, width=20,
                               pady=10)
    last_name_button = Button(search_student_window, text="Search by last name", command=search_by_lname, width=20,
                              pady=10)
    search_window_exit_button = Button(search_student_window, text="Cancel", command=search_student_window.destroy,
                                       width=15, pady=10)
    # </editor-fold>

    # <editor-fold desc="Place elements for add hours window">
    add_hours_select_student_title.grid(row=0, column=0, columnspan=2, pady=(10, 0))

    student_id_label.grid(row=1, column=0, padx=(10, 0))
    student_id_entry.grid(row=1, column=1, padx=(0, 10))
    student_id_button.grid(row=2, column=0, columnspan=2, pady=(5, 15))

    last_name_label.grid(row=3, column=0, padx=(10, 0))
    last_name_entry.grid(row=3, column=1, pady=(0, 10))
    last_name_button.grid(row=4, column=0, columnspan=2, pady=(5, 15))

    search_window_exit_button.grid(row=5, column=0, columnspan=2, pady=(0, 10))
    # </editor-fold>


def view_student():
    # Called once the student has been selected
    def display_student(info):
        # <editor-fold desc="Create window, title, and subtitle">

        # Process/format student info
        name = info[1] + " " + info[2]
        grade = "Grade " + str(info[3])
        id_num = "ID " + str(info[0])

        # Create window to display student info
        display_student_window = Toplevel()
        display_student_window.title("View Student Info")

        # Display student's name as a title at the top of the window
        student_title = Label(display_student_window, text=name)
        student_title.config(font=("Arial", 18))
        student_title.grid(row=0, column=0, columnspan=4, pady=(10, 0))

        # Display student's grade level and ID number as a subtitle at the top of the window
        subtitle = Label(display_student_window, text=(grade + " | " + id_num))
        subtitle.config(font=("Arial", 14))
        subtitle.grid(row=1, column=0, columnspan=4, )

        # </editor-fold>

        # Connect to database
        db_connection = sqlite3.connect('csdatabase.db')
        db_cursor = db_connection.cursor()

        # Get the total hours completed by a student
        db_cursor.execute("SELECT SUM(hours) FROM service WHERE student_id == :student_id;",
                          {
                              "student_id": str(info[0]),
                          }
                          )

        result = db_cursor.fetchall()
        total_hours = str(result[0][0])

        # Display a student's total hours at the top of the window
        total_label = Label(display_student_window, text=("Total Hours: " + total_hours))
        total_label.config(font=("Arial", 14))
        total_label.grid(row=2, column=0, columnspan=4, pady=(0, 10), padx=10)

        # Find all service records for student
        db_cursor.execute("SELECT *, strftime('%m/%d/%Y', date) FROM service WHERE student_id == :student_id;",
                          {
                              "student_id": str(info[0]),
                          }
                          )

        results = db_cursor.fetchall()

        # Display each service record
        for i, entry in enumerate(results):
            # select_button = Button(select_student_window, text="Select",
            #                        command=lambda student_temp=student: return_student(student_temp),
            #                        padx=8, pady=8)
            entry_date = Label(display_student_window, text=entry[5])
            entry_organization = Label(display_student_window, text=entry[3])
            hours_string = str(entry[4]) + " hours"
            entry_hours = Label(display_student_window, text=hours_string)

            # select_button.grid(row=i + 1, column=0, padx=5, pady=5)
            entry_date.grid(row=i + 3, column=1, padx=(5, 10))
            entry_organization.grid(row=i + 3, column=2, padx=(0, 10))
            entry_hours.grid(row=i + 3, column=3, padx=(0, 5))

        # Close the connection to the database
        db_connection.commit()
        db_connection.close()

    # Called to select the correct result after the database has been queried
    def select_student(results):
        # Called when the user picked from multiple results
        def return_student(info):
            select_student_window.destroy()
            display_student(info)

        # If the search had no results, notify the user
        if len(results) == 0:
            messagebox.showinfo(title="No Results", message="No students matching that query were found.")
            return
        # If the search had one result, select that result and proceed
        elif len(results) == 1:
            display_student(results[0])
        # If the search had more than one result, allow the user to select which result they want
        else:
            # Create and configure a window
            select_student_window = Toplevel()
            select_student_window.title("Select Student")

            select_title = Label(select_student_window, text="Multiple Results")
            select_title.config(font=("Arial", 18))
            select_title.grid(row=0, column=0, columnspan=4, pady=(10, 0))

            # For each result, create a row and a button that the user can use to select that result
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

    # Called when the "search by student ID" button is pressed
    def search_by_id():
        # Connect to database
        db_connection = sqlite3.connect('csdatabase.db')
        db_cursor = db_connection.cursor()

        # Search database for any students with the specified student ID
        db_cursor.execute("SELECT * FROM students WHERE student_id == :student_id;",
                          {
                              "student_id": str(student_id_entry.get()),
                          }
                          )

        # Close search student window
        search_student_window.destroy()

        # Access and return any search results
        result = db_cursor.fetchall()
        select_student(result)

        # Close database connection
        db_connection.commit()
        db_connection.close()

    # Called when the "search by last name" button is pressed
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

        # Close search student window
        search_student_window.destroy()

        # Access and return any search results
        result = db_cursor.fetchall()
        select_student(result)

        # Close database connection
        db_connection.commit()
        db_connection.close()

    # <editor-fold desc="Create view student info window">
    search_student_window = Toplevel()
    search_student_window.title("View Student Info")
    # </editor-fold>

    # <editor-fold desc="Create elements for view student info window">
    view_student_select_title = Label(search_student_window, text="View Student Info")
    view_student_select_title.config(font=("Arial", 18))

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
    view_student_select_title.grid(row=0, column=0, columnspan=2, pady=(10, 0))

    student_id_label.grid(row=1, column=0, padx=(10, 0))
    student_id_entry.grid(row=1, column=1, padx=(0, 10))
    student_id_button.grid(row=2, column=0, columnspan=2, pady=(5, 15))

    last_name_label.grid(row=3, column=0, padx=(10, 0))
    last_name_entry.grid(row=3, column=1, pady=(0, 10))
    last_name_button.grid(row=4, column=0, columnspan=2, pady=(5, 15))

    search_window_exit_button.grid(row=5, column=0, columnspan=2, pady=(0, 10))
    # </editor-fold>


def generate_report():
    # <editor-fold desc="Get and process all students">
    # Open connection to database
    db_connection = sqlite3.connect('csdatabase.db')
    db_cursor = db_connection.cursor()

    # Get a list of all registered students
    db_cursor.execute("SELECT * FROM students")
    all_students = db_cursor.fetchall()

    # Prepare lists for students who have and have not met the requirement
    passing_students = []
    failing_students = []

    # Get and process all hours completed by a certain student
    for student in all_students:
        db_cursor.execute("SELECT SUM(hours) FROM service WHERE student_id == :student_id;",
                          {
                              "student_id": str(student[0]),
                          }
                          )

        result = db_cursor.fetchall()
        hours = result[0][0]
        if hours is None:
            hours = 0

        # Condense information into a usable format
        info_string = student[1] + " " + student[2] + " (Grade " + str(student[3]) + ", ID " + str(
            student[0]) + "): " + str(hours) + " hours"

        # Sort student into the correct category
        if hours >= 24:
            passing_students.append(info_string)
        else:
            failing_students.append(info_string)

    db_connection.commit()
    db_connection.close()
    # </editor-fold>

    # <editor-fold desc="Create and save report file">
    # Ask user where to save the report
    report_file = filedialog.asksaveasfile(filetypes=[("Text file", "*.txt")], mode='w')

    # Print which students have and have not met the requirement
    if report_file:
        report_file.write("MET REQUIREMENT:")
        report_file.write("\n")

        for student in passing_students:
            report_file.write(student)
            report_file.write("\n")

        report_file.write("\n")
        report_file.write("NOT MET REQUIREMENT:")
        report_file.write("\n")

        for student in failing_students:
            report_file.write(student)
            report_file.write("\n")
    # </editor-fold>


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
    view_report_button = Button(main_screen, text="Generate Service Report", command=generate_report, width=30, pady=30)
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
