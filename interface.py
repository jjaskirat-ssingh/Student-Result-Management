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


def view_command():
    list1.delete(0, END)
    for row in database.view():
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
    

def insert_command():
        database.insert(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
        list1.delete(0, END)
        list1.insert(END, (title_text.get(), author_text.get(), year_text.get(), isbn_text.get()))
   
def delete_command():
        database.delete(selected_tuple[0])

def update_command():
        database.update(selected_tuple[0], title_text.get(), author_text.get(), year_text.get(), isbn_text.get())


window=Tk()
window.wm_title("Student Result")

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

b1=Button(window, text="View all", width = 12, command=view_command)
b1.grid(row=2, column=5)
b2=Button(window, text="Search entry", width = 12, command=search_command)
b2.grid(row=3, column=5)
b3=Button(window, text="Add entry", width = 12, command=insert_command)
b3.grid(row=4, column=5)
b4=Button(window, text="Update selected", width = 12, command=update_command)
b4.grid(row=5, column=5)
b5=Button(window, text="Delete selected", width = 12, command=delete_command)
b5.grid(row=6, column=5)
b6=Button(window, text="Close", width = 12, command=window.destroy)
b6.grid(row=7, column=5)

window.mainloop()