from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letter_list = [choice(letters) for i in range(randint(4, 6))]
    number_list = [choice(numbers) for j in range(randint(2, 3))]
    symbol_list = [choice(symbols) for k in range(randint(2, 3))]

    password_list = letter_list + number_list + symbol_list
    shuffle(password_list)

    password_entry.delete(0, END)

    password = "".join(password_list)
    pyperclip.copy(password)
    return password


def save(website, email, password):
    if len(website_entry.get()) == 0 or len(email_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showwarning("Warning", "Please fill all the blanks.")
    else:
        new_record = {
            website: {
                "email": email,
                "password": password
            }
        }

        try:
            with open("data.json", "r") as database:
                data = json.load(database)
        except FileNotFoundError:
            with open("data.json", "w") as database:
                json.dump(new_record, database, indent=4)
        else:
            data.update(new_record)
            with open("data.json", "w") as database:
                json.dump(data, database, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


def find_password(website):
    try:
        with open("data.json", "r") as database:
            data = json.load(database)
    except FileNotFoundError:
        messagebox.showerror("Error", "No records saved.")
    else:
        try:
            email_record = data[website]["email"]
            password_record = data[website]["password"]

            messagebox.showinfo(website, f"email: {email_record}\n"
                                         f"password: {password_record}")
        except KeyError:
            messagebox.showerror("Error", "No records matching.")


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=100, height=100)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(50, 50, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

website_entry = Entry(width=16)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "deardursungokoglan@gmail.com")

password_entry = Entry(width=16)
password_entry.grid(column=1, row=3)

generate_password_button = Button(text="Generate Password", command=lambda: password_entry.insert(0, generate_password()))
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=30, command=lambda: save(website_entry.get(), email_entry.get(), password_entry.get()))
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=15, command=lambda: find_password(website_entry.get()))
search_button.grid(column=2, row=1)

window.mainloop()
