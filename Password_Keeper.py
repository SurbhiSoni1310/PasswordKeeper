from tkinter import *
from tkinter import messagebox
import pyperclip
import json
from Password_Generate import generate_good_password

FONT_NAME = "Ariel"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_clicked():
    password = generate_good_password()
    enter_password.insert(0, password)
    option = messagebox.askyesno(title="Confirmation", message="Is the password generated ok ? ")
    if not option:
        enter_password.delete(0, END)
        enter_password.focus()
    else:
        pyperclip.copy(password)


# ---------------------------- SEARCH BUTTON ------------------------------- #


def search():
    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="WARNING", message="File not found")
    else:
        try:
            website_ = website_name.get()
            username_ = data[website_]["email"]
            password_ = data[website_]["password"]
        except KeyError:
            messagebox.showinfo(title="Not found", message="This website's password is not stored")
        else:
            messagebox.showinfo(title="Your Information",
                                message=f"Your Username/Email is : {username_}\nYour Password "
                                        f"is : {password_}")
    finally:
        website_name.delete(0, END)
        website_name.focus()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_clicked():
    username_ = username_entry.get()
    password_ = enter_password.get()
    website_ = website_name.get()

    if len(username_) == 0 or len(website_) == 0 or len(password_) == 0:
        messagebox.showwarning(title="WARNING", message="Please don't leave any field empty")
    else:
        new_data = {
            website_:
                {
                    "email": username_,
                    "password": password_
                }
        }
        option = messagebox.askokcancel(title="Confirmation", message=f"These are the details entered by you : \n"
                                                                      f"Website : {website_}\nUsername : {username_}\n"
                                                                      f"Password : {password_}\nIs it ok to save ?")
        if option:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)  # Dictionary : Read old data
                    data.update(new_data)  # Update Dictionary : Append new data
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)  # Write new data in dictionary
            else:
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)

            finally:
                username_entry.delete(0, END)
                enter_password.delete(0, END)
                website_name.delete(0, END)
                website_name.focus()


# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.minsize(400, 400)
window.config(padx=20, pady=20)
window.title("Password Generator")

# Canvas
canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=0, column=1)

# Website label
website = Label(text="Website : ")
website.grid(row=1, column=0)

# Website entry
website_name = Entry(width=35)
website_name.focus()
website_name.grid(row=1, column=1, columnspan=2, sticky=W)

# User Name label
username = Label(text="Email/Username : ")
username.grid(row=2, column=0)

# Username entry box
username_entry = Entry(width=35)
username_entry.grid(row=2, columnspan=2, column=1, sticky=W)
username_entry.insert(0, "example@gmail.com")

# Entry space for password
enter_password = Entry(width=35)
enter_password.grid(row=3, column=1, columnspan=2, sticky=W)

# Generate Password Button
generate_password = Button(text="Generate Password", width=29, command=generate_clicked)
generate_password.grid(row=4, column=1, columnspan=2, sticky=W, pady=5)

# Password Label
password_label = Label(text="Password : ")
password_label.grid(row=3, column=0)

# Add Button
add_button = Button(text="Add", width=29, command=add_clicked)
add_button.grid(row=5, columnspan=2, column=1, sticky=W, pady=4)

# Search Button
search_button = Button(text="Search", width=29, command=search)
search_button.grid(row=6, columnspan=2, column=1, sticky=W, pady=4)

window.mainloop()
