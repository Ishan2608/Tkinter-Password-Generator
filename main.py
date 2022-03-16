import tkinter as tk
from tkinter import messagebox
import json

import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
import random


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    p_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    p_symbols = [random.choice(symbols) for _ in range(random.randint(2, 5))]
    p_numbers = [random.choice(numbers) for _ in range(random.randint(2, 5))]

    password_list = p_letters + p_symbols + p_numbers

    random.shuffle(password_list)

    # password = ""
    # for char in password_list:
    #     password += char

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)
    copy_msg.config(text="Password Copied to Clipboard")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_password():
    password_ = password_entry.get()
    website = website_entry.get()
    user_name = user_name_entry.get()

    try:
        with open('passwords.json') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        pass
    else:
        if website in data:
            messagebox.showinfo(message="Password for this Website already saved")
            password_entry.delete(0, tk.END)
            return

    new_dictinary = {
        website: {
            'email': user_name,
            'password': password_
        }
    }

    if len(password_) == 0 or len(website) == 0 or len(user_name) == 0:
        messagebox.showinfo(title='Error', message="You have left some entries empty")
        return
    else:
        ok = messagebox.askyesno(title=website, message=
        f"These are the details entered\nemail: {user_name}\npassword: {password_}\nIs it OK to save?")
        messagebox.showinfo(title="Success", message="Your Password was Saved")

        if not ok:
            password_entry.delete(0, tk.END)
            return

        try:
            with open('passwords.json', mode='r') as data_file:
                # read old data
                data = json.load(data_file)

        except FileNotFoundError:
            with open('passwords.json', 'w') as data_file:
                json.dump(new_dictinary, data_file, indent=4)

        else:
            # update it
            data.update(new_dictinary)
            with open('passwords.json', 'w') as file:
                # write the updated one.
                json.dump(data, file, indent=4)

        finally:
            # clear out the entries after the file writing is done
            password_entry.delete(0, tk.END)
            website_entry.delete(0, tk.END)
            copy_msg.config(text="")


# ----------------------------- SEARCH -------------------------------- #

def search():
    website = website_entry.get()
    try:
        with open('passwords.json') as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title='Error', message="No Websites saved Yet")

    else:
        if website not in data:
           messagebox.showinfo(message="Password for this website not saved yet")
           password_entry.delete(0, tk.END)

        else:
            web_dict = data[website]
            email = web_dict['email']
            password = web_dict['password']
            messagebox.showinfo(message=f"Email: {email}\nPassword: {password}")


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Password Generator")
window.config(padx=50, pady=50)

canvas = tk.Canvas(width=200, height=200)
lock_image = tk.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=0, column=1)

website_label = tk.Label(text='Website:')
password_label = tk.Label(text='Password:')
user_name_label = tk.Label(text='Email/Username:')
copy_msg = tk.Label(text="")
website_label.grid(row=1, column=0)
user_name_label.grid(row=2, column=0)
password_label.grid(row=3, column=0)
copy_msg.grid(row=5, column=1)

website_entry = tk.Entry(width=32)
user_name_entry = tk.Entry(width=42)
password_entry = tk.Entry(width=33)
website_entry.focus()
user_name_entry.insert(0, "dummyemail@gmail.com")

search = tk.Button(text="Search", width=6, border=1, bg='light gray', command=search)
search.grid(row=1, column=2)

website_entry.grid(row=1, column=1)
user_name_entry.grid(row=2, column=1, columnspan=2)
password_entry.grid(row=3, column=1)

generate_button = tk.Button(text='Generate', width=7, border=1, bg='light gray', command=generate_password)
add_button = tk.Button(text='Add', width=36, border=1, bg='light gray', command=add_password)
generate_button.grid(row=3, column=2)
add_button.grid(row=4, column=1, columnspan=2)

# keeping the screen up
window.mainloop()
