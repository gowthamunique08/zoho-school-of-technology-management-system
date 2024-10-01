from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

class Create_Student:
    def __init__(self, main):
        self.main_window = main

        # Create table before any operation
        self.create_table_if_not_exists()

        self.C_Frame = Frame(self.main_window, height=600, width=400, relief=GROOVE, border=2, bg="grey")
        self.C_Frame.pack(side=LEFT)
        Label(self.C_Frame, text="Student Details:", font="arial 12 bold", bg="grey").place(x=10, y=10)
        self.C_Frame.pack_propagate(0)

        self.S_ID = Label(self.C_Frame, text="ID:", font="arial 12 bold",bg="grey")
        self.S_ID.place(x=40, y=60)
        self.S_ID_Field = Entry(self.C_Frame, width=40)
        self.S_ID_Field.place(x=150, y=60)

        self.S_Name = Label(self.C_Frame, text="Name:", font="arial 12 bold", bg="grey")
        self.S_Name.place(x=40, y=90)
        self.S_Name_Field = Entry(self.C_Frame, width=40)
        self.S_Name_Field.place(x=150, y=90)

        self.S_Age = Label(self.C_Frame, text="DOB:", font="arial 12 bold", bg="grey")
        self.S_Age.place(x=40, y=120)
        self.S_Age_Field = Entry(self.C_Frame, width=40)
        self.S_Age_Field.place(x=150, y=120)

        self.S_DOB = Label(self.C_Frame, text="Age:", font="arial 12 bold", bg="grey")
        self.S_DOB.place(x=40, y=150)
        self.S_DOB_Field = Entry(self.C_Frame, width=40)
        self.S_DOB_Field.place(x=150, y=150)

        self.S_Gender = Label(self.C_Frame, text="Gender:", font="arial 12 bold", bg="grey")
        self.S_Gender.place(x=40, y=180)
        self.S_Gender_Field = Entry(self.C_Frame, width=40)
        self.S_Gender_Field.place(x=150, y=180)

        self.S_City = Label(self.C_Frame, text="City:", font="arial 12 bold", bg="grey")
        self.S_City.place(x=40, y=210)
        self.S_City_Field = Entry(self.C_Frame, width=40)
        self.S_City_Field.place(x=150, y=210)

        self.Button_Frame = Frame(self.C_Frame, height=250, width=250, relief=GROOVE, bd=2, bg="grey")
        self.Button_Frame.place(x=40, y=250)

        self.Add_Button = Button(self.Button_Frame, text="Add", font="arial 15 bold", bg="red",width=25, command=self.Add)
        self.Add_Button.pack()

        self.Delete_Button = Button(self.Button_Frame, text="Delete", font="arial 15 bold",bg="green",width=25, command=self.Delete)
        self.Delete_Button.pack()

        self.Update_Button = Button(self.Button_Frame, text="Update", font="arial 15 bold",bg="blue", width=25, command=self.Update)
        self.Update_Button.pack()

        self.Clear_Button = Button(self.Button_Frame, text="Clear", font="arial 15 bold", bg="yellow",width=25, command=self.Clear)
        self.Clear_Button.pack()

        self.S_S_Details = Frame(main, height=600, width=800, relief=GROOVE, bd=2, bg="white")
        self.S_S_Details.pack(side=LEFT)

        self.tree = ttk.Treeview(self.S_S_Details, columns=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=25)

        self.tree.column("#1", anchor=CENTER, width=40)
        self.tree.heading("#1", text="ID")
        self.tree.column("#2", anchor=CENTER)
        self.tree.heading("#2", text="Name")
        self.tree.column("#3", anchor=CENTER, width=115)
        self.tree.heading("#3", text="DOB")
        self.tree.column("#4", anchor=CENTER, width=110)
        self.tree.heading("#4", text="Age")
        self.tree.column("#5", anchor=CENTER, width=110)
        self.tree.heading("#5", text="Gender")
        self.tree.column("#6", anchor=CENTER)
        self.tree.heading("#6", text="City")

        c = sqlite3.connect("data.db")
        cursor = c.cursor()
        cursor.execute("SELECT * FROM data")
        a = cursor.fetchall()
        for i in a:
            self.tree.insert("", index=END, values=i)
        c.commit()
        c.close()

        self.tree.place(x=0, y=0)

    def create_table_if_not_exists(self):
        c = sqlite3.connect("data.db")
        cursor = c.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data (
                ID INTEGER PRIMARY KEY,
                NAME VARCHAR(20),
                AGE VARCHAR(20),
                DOB VARCHAR(20),
                GENDER VARCHAR(20),
                CITY VARCHAR(20)
            )
        """)
        c.commit()
        c.close()

    def Add(self):
        id = self.S_ID_Field.get()
        name = self.S_Name_Field.get()
        age = self.S_Age_Field.get()
        dob = self.S_DOB_Field.get()
        gender = self.S_Gender_Field.get()
        city = self.S_City_Field.get()

        c = sqlite3.connect("data.db")
        cursor = c.cursor()
        cursor.execute('INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)', (id, name, age, dob, gender, city))
        c.commit()
        c.close()

        self.tree.insert("", index=0, values=(id, name, age, dob, gender, city))
        print("Row inserted")

    def Delete(self):
        item = self.tree.selection()[0]
        selected_item = self.tree.item(item)['values'][0]

        c = sqlite3.connect("data.db")
        cursor = c.cursor()
        cursor.execute(f"DELETE FROM data WHERE ID={selected_item}")
        c.commit()
        c.close()

        self.tree.delete(item)
        print("Row deleted")

    def Update(self):
        item = self.tree.selection()[0]
        selected_item = self.tree.item(item)['values'][0]

        id = self.S_ID_Field.get()
        name = self.S_Name_Field.get()
        age = self.S_Age_Field.get()
        dob = self.S_DOB_Field.get()
        gender = self.S_Gender_Field.get()
        city = self.S_City_Field.get()

        c = sqlite3.connect("data.db")
        cursor = c.cursor()
        cursor.execute(f"UPDATE data SET ID=?, NAME=?, AGE=?, DOB=?, GENDER=?, CITY=? WHERE ID=?",
                       (id, name, age, dob, gender, city, selected_item))
        c.commit()
        c.close()

        self.tree.item(item, values=(id, name, age, dob, gender, city))
        print("Row updated")

    def Clear(self):
        self.S_ID_Field.delete(0, END)
        self.S_Name_Field.delete(0, END)
        self.S_Age_Field.delete(0, END)
        self.S_DOB_Field.delete(0, END)
        self.S_Gender_Field.delete(0, END)
        self.S_City_Field.delete(0, END)


main_window = Tk()
main_window.iconbitmap(r'C:\Users\USER\Downloads\ZS.ico')

image = Image.open(r'C:\Users\USER\OneDrive\Desktop\zoho\zst.png')
image = image.resize((300, 50), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

label_photo = Label(main_window, image=photo, bg='white')
label_photo.pack()
main_window.title("Student Management System")
main_window.resizable(False, False)
main_window.geometry("1200x600")

Title = Frame(main_window, height=50, width=1200, relief=GROOVE, border=2, bg="black")
Title.pack()
T_Text = Label(Title, text="Student Management System", width=1200, font="arial 24 bold", bg="grey")
T_Text.pack()

Datas = Create_Student(main_window)

main_window.mainloop()
