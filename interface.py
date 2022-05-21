from tkinter import *
import database

# database = Database("books.db")

def get_selected_row(event):
    global selected_tuple
    try:
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)

        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3])
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])
        e5.delete(0, END)
        e5.insert(END, selected_tuple[4])
        e6.delete(0, END)
        e6.insert(END, selected_tuple[4])
    except IndexError:
        pass


# def view_command():
#     list1.delete(0, END)
#     for row in database.view():
#         list1.insert(END, row)

def filter_by_subject_command():
        list1.delete(0, END)
        if (e4.get() and e4.get().strip()) :
                for row in database.filter_by_subject(subject.get()):
                        list1.insert(END, row)    

def search_command():
        list1.delete(0, END)
        print(e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get())
        if (e1.get() and e1.get().strip()) :
                for row in database.search_student_rollno(roll_no.get()):
                        list1.insert(END, row)
        elif (e3.get() and e3.get().strip()) :
                for row in database.search_student_batch(batch_no.get()):
                        list1.insert(END, row)
        elif (e4.get() and e4.get().strip()) :
                for row in database.search_subject(subject.get()):
                        list1.insert(END, row)

def add_student_command():
        list1.delete(0, END)
        print(e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get())
        if (e1.get() and e1.get().strip() and e2.get() and e2.get().strip() and e3.get() and e3.get().strip()) :
                database.add_student(roll_no.get(), name.get(), batch_no.get())
                        # list1.insert(END, row)    

def add_subject_command():
        list1.delete(0, END)
        print(e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get())
        if (e4.get() and e4.get().strip()) :
                database.add_subject(subject.get())#:
                        # list1.insert(END, row)
        # database.insert(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
        # list1.delete(0, END)
        # list1.insert(END, (title_text.get(), author_text.get(), year_text.get(), isbn_text.get()))
   
def delete_command():
        # database.delete(selected_tuple[0])
        list1.delete(0, END)
        try :
                print(e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get())
                if (e2.get() and e2.get().strip):
                        for row in database.delete_student_name(name.get()):
                                list1.insert(END, row)

                list1.delete(0, END)
                if (e1.get() and e1.get().strip):
                        for row in database.delete_student_roll(roll_no.get()):
                                list1.insert(END, row)

                list1.delete(0, END)
                if (e4.get() and e4.get().strip):
                        for row in database.delete_subject(subject.get()):
                                list1.insert(END, row)
        except :
                list1.insert(END,"no value entered")
        # list1.delete(0, END)
        # if (e1.get() and e1.get().strip and e4.get() and e4.get().strip and e6.get() and e6.get().strip):
        #         for row in database.update_status(status.get(), roll_no.get(), subject.get()):
        #                 list1.insert(END, row)

def add_score_subject_command():
        list1.delete(0, END)
        if (e1.get() and e1.get().strip and e4.get() and e4.get().strip and e5.get() and e5.get().strip and e6.get() and e6.get().strip):
                database.add_score_subject(roll_no.get(),subject.get(),marks.get(),status.get())
                # for row in database.add_score_subject(roll_no.get(), subject.get(), marks.get(), status.get()):
                #         list1.insert(END, row)

def show_students_command():
        list1.delete(0, END)
        for row in database.get_students():
                        list1.insert(END, row)

def show_subjects_command():
        list1.delete(0, END)
        for row in database.get_subjects():
                        list1.insert(END, row)

def update_command():
        list1.delete(0, END)
        print(e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get())
        if (e1.get() and e1.get().strip and e2.get() and e2.get().strip):
                for row in database.update_student_name(name.get(), roll_no.get()):
                        list1.insert(END, row)

        list1.delete(0, END)
        if (e1.get() and e1.get().strip and e3.get() and e3.get().strip):
                for row in database.update_student_batch(batch_no.get(), roll_no.get()):
                        list1.insert(END, row)

        list1.delete(0, END)
        if (e1.get() and e1.get().strip and e4.get() and e4.get().strip and e5.get() and e5.get().strip):
                for row in database.update_score(marks.get(), roll_no.get(), subject.get()):
                        list1.insert(END, row)

        list1.delete(0, END)
        if (e1.get() and e1.get().strip and e4.get() and e4.get().strip and e6.get() and e6.get().strip):
                for row in database.update_status(status.get(), roll_no.get(), subject.get()):
                        list1.insert(END, row)
def filter_by_subject() :
        list1.delete(0, END)
        if (e4.get() and e4.get().split()):
                for row in database.filter_by_subject(subject.get()) :
                        list1.insert(END, row)
window=Tk()
# database.drop_tables()
window.wm_title("Student Result")
database.create_tables()

l1 = Label(window, text="Roll No.")
l1.grid(row=0, column=0)
l2 = Label(window, text="Name")
l2.grid(row=0, column=2)
l3 = Label(window, text="Batch")
l3.grid(row=0, column=4)
l4 = Label(window, text="Subject")
l4.grid(row=1, column=0)
l5 = Label(window, text="Marks")
l5.grid(row=1, column=2)
l6 = Label(window, text="Status")
l6.grid(row=1, column=4)

roll_no = StringVar() 
e1=Entry(window, textvariable=roll_no)
e1.grid(row=0, column=1)
name = StringVar()
e2=Entry(window, textvariable=name)
e2.grid(row=0, column=3)
batch_no = StringVar() 
e3=Entry(window, textvariable=batch_no)
e3.grid(row=0, column=5)
subject = StringVar() 
e4=Entry(window, textvariable=subject)
e4.grid(row=1, column=1)
marks = StringVar() 
e5=Entry(window, textvariable=marks)
e5.grid(row=1, column=3)
status = StringVar()
e6=Entry(window, textvariable=status)
e6.grid(row=1, column=5)
# year_text = StringVar() 

list1 = Listbox(window, height = 8, width = 50)
list1.grid(row=2, column=0, rowspan=6, columnspan= 4)
sb1=Scrollbar(window)
sb1.grid(row=2, column=4, rowspan=6)

list1.configure(yscrollcommand = sb1.set)
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row) 

b1=Button(window, text="View all students", width = 15, command=show_students_command)
b1.grid(row=2, column=5)
b2=Button(window, text="Search entry", width = 15, command=search_command)
b2.grid(row=3, column=5)
b3=Button(window, text="Add student", width = 15, command=add_student_command)
b3.grid(row=4, column=5)
b4=Button(window, text="Add subject", width = 15, command=add_subject_command)
b4.grid(row=5, column=5)
b5=Button(window, text="Add score", width = 15, command=add_score_subject_command)
b5.grid(row=6, column=5)
b6=Button(window, text="Update selected", width = 15, command=update_command)
b6.grid(row=7, column=5)
b7=Button(window, text="Delete selected", width = 15, command=delete_command)
b7.grid(row=8, column=5)
b8=Button(window, text="Show subjects", width = 15, command=show_subjects_command)
b8.grid(row=9, column=5)
b9=Button(window, text="Filter by subject ID", width = 15, command=filter_by_subject_command)
b9.grid(row=10, column=5)
b10=Button(window, text="Close", width = 15, command=window.destroy)
b10.grid(row=11, column=5)

window.mainloop()