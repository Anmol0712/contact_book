import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector as mysql

# Establishing the connection from my sql database
conn = mysql.connect(host='localhost', user='root', password='anmol', database='contact_book')
c = conn.cursor()

# Creating 'contacts' table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
    first_name CHAR(100),
    surname CHAR(100),
    phone BIGINT PRIMARY KEY,
    address TEXT,
    email VARCHAR(100)
);
''')

# Creating 'users' table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(100) PRIMARY KEY,
    password VARCHAR(100)
);
''')


# Creating main Tkinter window
root = tk.Tk()
root.title("Contact Book")
root.geometry("1232x700")
root.resizable(width=False, height=False)
ico = Image.open("icon.png")       # Adding an icon in the tkinter window
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)



# Function to disable all buttons in the options frame
def disable_buttons(): 
    create_btn.config(state='disabled')
    view_btn.config(state='disabled')
    edit_btn.config(state='disabled')
    delete_btn.config(state='disabled')
    about_btn.config(state='disabled')

# Function to enable all buttons in the options frame
def enable_buttons(): 
    create_btn.config(state='normal')
    view_btn.config(state='normal')
    edit_btn.config(state='normal')
    delete_btn.config(state='normal')
    about_btn.config(state='normal')


# Function to display Registration page
def register_page():
    remove_pages()
    disable_buttons()
    register_frame = tk.Frame(main_frame)

    lb = tk.Label(register_frame, text="Register", font=("Bold", 30))
    lb.pack(pady=10)

    username_label = tk.Label(register_frame, text="Username", font=("Bold", 15))
    username_label.pack(pady=5)
    username_entry = tk.Entry(register_frame, font=("Bold", 15), width=30)
    username_entry.pack(pady=5)

    password_label = tk.Label(register_frame, text="Password", font=("Bold", 15))
    password_label.pack(pady=5)
    password_entry = tk.Entry(register_frame, font=("Bold", 15), width=30, show='•')
    password_entry.pack(pady=5)

    confirm_password_label = tk.Label(register_frame, text="Confirm Password", font=("Bold", 15))
    confirm_password_label.pack(pady=5)
    confirm_password_entry = tk.Entry(register_frame, font=("Bold", 15), width=30, show='•')
    confirm_password_entry.pack(pady=5)

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter username and password!")
            return

        if password != confirm_password:
            messagebox.showwarning("Input Error", "Passwords do not match!")
            return

        conn = mysql.connect(host='localhost', user='root', password='anmol', database='contact_book')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            login_page()
        except mysql.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            conn.close()

    register_button = tk.Button(register_frame, text="Register", font=("Bold", 15), command=register_user)
    register_button.pack(pady=20)

    register_frame.pack(pady=50)

# Function to display Login page at the starting
def login_page():
    remove_pages()
    disable_buttons()
    login_frame = tk.Frame(main_frame)

    lb = tk.Label(login_frame, text="Login", font=("Bold", 30))
    lb.pack(pady=10)

    username_label = tk.Label(login_frame, text="Username", font=("Bold", 15))
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_frame, font=("Bold", 15), width=30)
    username_entry.pack(pady=5)

    password_label = tk.Label(login_frame, text="Password", font=("Bold", 15))
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_frame, font=("Bold", 15), width=30, show='•')
    password_entry.pack(pady=5)

    def check_login():
        username = username_entry.get()
        password = password_entry.get()
       
        # Fecthing username and password from the database 
        conn = mysql.connect(host='localhost', user='root', password='anmol', database='contact_book')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = c.fetchone()
        conn.close()

        # Replace username and password with actual authentication
        if result: 
            messagebox.showinfo("Login Success", "Welcome!")
            enable_buttons()  # Enable buttons after successful login
            create_page()     # Directly open create contacts page after login
       
        elif (username=="" and password==""):
            messagebox.showerror("Login Failed", "Please enter username and password!")

        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    login_button = tk.Button(login_frame, text="Login", font=("Bold", 15), command=check_login)
    login_button.pack(pady=20)

    register_button = tk.Button(login_frame, text="Register", font=("Bold", 15), command=register_page)
    register_button.pack(pady=5)

    login_frame.pack(pady=50)


# Function to create new contacts
def create_page():
    remove_pages()
    create_frame = tk.Frame(main_frame)
    
    lb = tk.Label(create_frame, text="Create Contacts", font=("Bold", 30))
    lb.pack(pady=10)
    
    fname_label = tk.Label(create_frame, text="First Name", font=("Bold", 15))
    fname_label.pack(pady=5)
    fname_entry = tk.Entry(create_frame, font=("Bold", 15), width=30)
    fname_entry.pack(pady=5)
    
    lname_label = tk.Label(create_frame, text="Surname", font=("Bold", 15))
    lname_label.pack(pady=5)
    lname_entry = tk.Entry(create_frame, font=("Bold", 15), width=30)
    lname_entry.pack(pady=5)
    
    phone_label = tk.Label(create_frame, text="Phone", font=("Bold", 15))
    phone_label.pack(pady=5)
    phone_entry = tk.Entry(create_frame, font=("Bold", 15), width=30)
    phone_entry.pack(pady=5)
    
    address_label = tk.Label(create_frame, text="Address", font=("Bold", 15))
    address_label.pack(pady=5)
    address_entry = tk.Text(create_frame, font=("Bold", 15), width=30, height=5)
    address_entry.pack(pady=5)
    
    email_label = tk.Label(create_frame, text="Email", font=("Bold", 15))
    email_label.pack(pady=5)
    email_entry = tk.Entry(create_frame, font=("Bold", 15), width=30)
    email_entry.pack(pady=5)
    
    def save_contact():
        fname = fname_entry.get().strip()
        phone = phone_entry.get().strip()

         # Input Validation
        if not fname or not phone:
            messagebox.showwarning("Input Error", "Please enter at least first name and phone number!")
            return

        if  not fname.isalpha() and not phone.isdigit() :
            messagebox.showwarning("Input Error", "First name should not contain numbers or special characters and phone number should contain only digits!")
            return

        # Inserting data into MySQL database
        conn = mysql.connect(host='localhost', user='root', password='anmol', database='contact_book')
        c = conn.cursor()
        lname = lname_entry.get().strip()
        address = address_entry.get("1.0", "end-1c").strip()
        email = email_entry.get().strip()
        c.execute("INSERT INTO contacts (first_name, surname, phone, address, email) VALUES (%s, %s, %s, %s, %s)", (fname, lname, phone, address, email))
        conn.commit()
        messagebox.showinfo("Success", "Contact added successfully!")

        # Clearing entry fields after saving
        fname_entry.delete(0, tk.END)
        lname_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        address_entry.delete("1.0", tk.END)
        email_entry.delete(0, tk.END)
        conn.close()

    save_button = tk.Button(create_frame, text="Save Contact", font=("Bold", 15), command=save_contact)
    save_button.pack(pady=10)
    
    create_frame.pack(pady=20)


# Function to view all contacts
def view_page():
    remove_pages()
    view_frame = tk.Frame(main_frame)
    
    lb = tk.Label(view_frame, text="View Contacts", font=("Bold", 30))
    lb.pack(pady=10)
    
    # Creating treeview to display contacts
    tree_frame = tk.Frame(view_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    tree = ttk.Treeview(tree_frame, columns=('Name', 'Phone', 'Address', 'Email'), show='headings')
    tree.heading('Name', text='Name')
    tree.heading('Phone', text='Phone')
    tree.heading('Address', text='Address')
    tree.heading('Email', text='Email')
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Fetching data from MySQL and populating treeview
    conn = mysql.connect(host='localhost', user='root', password='anmol', database='contact_book')
    c = conn.cursor()
    c.execute("SELECT CONCAT(first_name, ' ', surname) AS name, phone, address, email FROM contacts")
    rows = c.fetchall()
    for row in rows:
        tree.insert('', tk.END, values=row)
    conn.close()
    
    view_frame.pack(pady=20, fill=tk.BOTH, expand=True)


# Function to edit a contact
def edit_page():
    remove_pages()
    edit_frame = tk.Frame(main_frame)
    
    lb = tk.Label(edit_frame, text="Edit Contacts", font=("Bold", 30))
    lb.pack(pady=10)
    
    fname_label = tk.Label(edit_frame, text="New First Name", font=("Bold", 15))
    fname_label.pack(pady=5)
    fname_entry = tk.Entry(edit_frame, font=("Bold", 15), width=30)
    fname_entry.pack(pady=5)
    
    lname_label = tk.Label(edit_frame, text="New Surname", font=("Bold", 15))
    lname_label.pack(pady=5)
    lname_entry = tk.Entry(edit_frame, font=("Bold", 15), width=30)
    lname_entry.pack(pady=5)
    
    phone_label = tk.Label(edit_frame, text="New Phone", font=("Bold", 15))
    phone_label.pack(pady=5)
    phone_entry = tk.Entry(edit_frame, font=("Bold", 15), width=30)
    phone_entry.pack(pady=5)
    
    address_label = tk.Label(edit_frame, text="New Address", font=("Bold", 15))
    address_label.pack(pady=5)
    address_entry = tk.Text(edit_frame, font=("Bold", 15), width=30, height=5)
    address_entry.pack(pady=5)
    
    email_label = tk.Label(edit_frame, text="New Email", font=("Bold", 15))
    email_label.pack(pady=5)
    email_entry = tk.Entry(edit_frame, font=("Bold", 15), width=30)
    email_entry.pack(pady=5)
    
    # Creating select funtion to select contact from treeview
    def select_contact():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            contact_name = item['values'][0]

            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to update this contact?")
            if confirm:
                conn = mysql.connect(host='localhost', user='root', password='anmol', database='contact_book')
                c = conn.cursor()
        
                # Fetching selected contact details and displaying in entry fields
                c.execute("SELECT first_name, surname, phone, address, email FROM contacts WHERE CONCAT(first_name, ' ', surname) = %s", (contact_name,))
                contact_details = c.fetchone()
                conn.close()
                if contact_details:
                    fname_entry.delete(0, tk.END)
                    fname_entry.insert(0, contact_details[0])
                    lname_entry.delete(0, tk.END)
                    lname_entry.insert(0, contact_details[1])
                    phone_entry.delete(0, tk.END)
                    phone_entry.insert(0, contact_details[2])
                    address_entry.delete("1.0", tk.END)
                    address_entry.insert("1.0", contact_details[3])
                    email_entry.delete(0, tk.END)
                    email_entry.insert(0, contact_details[4])
        else:
            messagebox.showwarning("Selection Error", "Please select a contact!")
    
    select_button = tk.Button(edit_frame, text="Select Contact", font=("Bold", 15), command=select_contact)
    select_button.place(x=629, y=460)
    
    # Creating treeview to display contacts
    tree_frame = tk.Frame(edit_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    tree = ttk.Treeview(tree_frame, columns=('Name', 'Phone', 'Address', 'Email'), show='headings')
    tree.heading('Name', text='Name')
    tree.heading('Phone', text='Phone')
    tree.heading('Address', text='Address')
    tree.heading('Email', text='Email')
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
    
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)     # Adding a scrollbar in treeview
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    conn = mysql.connect(host='localhost', user='root', password='anmol', database='contact_book')
    c = conn.cursor()
    c.execute("SELECT CONCAT(first_name, ' ', surname) AS name, phone, address, email FROM contacts")     # Fetching the data from database
    rows = c.fetchall()
    for row in rows:
        tree.insert('', tk.END, values=row)
    conn.close()
    
    # Function to update the contact
    def update_contact():
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            contact_name = item['values'][0]
            new_fname = fname_entry.get()
            new_lname = lname_entry.get()
            new_phone = phone_entry.get()
            new_address = address_entry.get("1.0", "end-1c")
            new_email = email_entry.get()
            conn = mysql.connect(host='localhost', user='root', password='anmol', database='contact_book')
            c = conn.cursor()

            # Query to update data in the database
            c.execute("UPDATE contacts SET first_name = %s, surname = %s, phone = %s, address = %s, email = %s WHERE CONCAT(first_name, ' ', surname) = %s", (new_fname, new_lname, new_phone, new_address, new_email, contact_name))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Contact updated successfully!")

            # Clearing entry fields after updating
            fname_entry.delete(0, tk.END)
            lname_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            address_entry.delete("1.0", tk.END)
            email_entry.delete(0, tk.END)
            
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to update!")
    
    update_button = tk.Button(edit_frame, text="Update Contact", font=("Bold", 15), command=update_contact)
    update_button.place(x=625, y=500)
    
    edit_frame.pack(pady=20)


# Function to delete the contacts 
def delete_page():
    remove_pages()
    delete_frame = tk.Frame(main_frame)
    
    lb = tk.Label(delete_frame, text="Delete Contacts", font=("Bold", 30))
    lb.pack(pady=10)
    
    # Creating treeview to display contacts
    tree_frame = tk.Frame(delete_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    tree = ttk.Treeview(tree_frame, columns=('Name', 'Phone', 'Address', 'Email'), show='headings')
    tree.heading('Name', text='Name')
    tree.heading('Phone', text='Phone')
    tree.heading('Address', text='Address')
    tree.heading('Email', text='Email')
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    conn = mysql.connect(host='localhost', user='root', password='anmol', database='contact_book')
    c = conn.cursor()
    c.execute("SELECT CONCAT(first_name, ' ', surname) AS name, phone, address, email FROM contacts")
    rows = c.fetchall()
    for row in rows:
        tree.insert('', tk.END, values=row)
    conn.close()
    
    delete_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    def delete_contact():
        selected_item = tree.selection()
        
        if selected_item:
            item = tree.item(selected_item)
            contact_name = item['values'][0]
            
            # Confirmation for deleting the desired contacts
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this contact?")
            if confirm:
                conn = mysql.connect(host='localhost', user='root', password='anmol', database='contact_book')
                c = conn.cursor()
                c.execute("DELETE FROM contacts WHERE CONCAT(first_name, ' ', surname) = %s", (contact_name,))
                conn.commit()
                conn.close()
                tree.delete(selected_item)
                messagebox.showinfo("Success", "Contact deleted successfully!")
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete!")
    
    delete_button = tk.Button(delete_frame, text="Delete Contact", font=("Bold", 15), command=delete_contact)
    delete_button.pack(pady=10)
    
    delete_frame.pack(pady=20)


# Function to display About App page
def about_page():
    remove_pages()
    about_frame = tk.Frame(main_frame)
    
    lb = tk.Label(about_frame, text="About App", font=("Bold", 30))
    lb.pack(pady=10)

    description = tk.Label(about_frame, text="This is a Contact Book App developed using Python and Tkinter.", font=("Bold", 15))
    description.pack(pady=10)


    # Adding first photo with roll number
    photo1 = Image.open("anmol.jpg")
    photo1 = photo1.resize((200, 200), Image.LANCZOS)
    photo1 = ImageTk.PhotoImage(photo1)
    photo_label1 = tk.Label(main_frame, image=photo1)
    photo_label1.image = photo1  # Keep a reference to avoid garbage collection
    photo_label1.place(x=250,y=170)

    name1 = tk.Label(main_frame, text="Name: Anmol Kumar", font=("Bold", 15))
    name1.place(x=245,y=390)
    roll_number1 = tk.Label(main_frame, text="Roll No: 2201320100036", font=("Bold", 15))
    roll_number1.place(x=245,y=430)

    # Adding second photo with roll number
    photo2 = Image.open("aryan.jpg")
    photo2 = photo2.resize((200, 200), Image.LANCZOS)
    photo2 = ImageTk.PhotoImage(photo2)
    photo_label2 = tk.Label(main_frame, image=photo2)
    photo_label2.image = photo2  # Keep a reference to avoid garbage collection
    photo_label2.place(x=550,y=170)

    name2 = tk.Label(main_frame, text="Name: Aryan Katiyar", font=("Bold", 15))
    name2.place(x=545,y=390)
    roll_number2 = tk.Label(main_frame, text="Roll No: 2201320100045", font=("Bold", 15))
    roll_number2.place(x=545,y=430)

    
    dept = tk.Label(main_frame, text="Department of Computer Science & Engineering", font=("Bold", 20))
    dept.place(x=210,y=500)

    about_frame.pack(pady=20)


# Function to hide indicators
def hide_indicators():
    create_indicate.config(bg="#C3C3C3")
    view_indicate.config(bg="#C3C3C3")
    edit_indicate.config(bg="#C3C3C3")
    delete_indicate.config(bg="#C3C3C3")
    about_indicate.config(bg="#C3C3C3")

# Function to destroy the previous frame as soon as next option is selected
def remove_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

# Function to indicators to show which opton has been selected
def indicate(lb, page):
    hide_indicators()
    lb.config(bg="#158AFF")
    remove_pages()
    page()

options_frame = tk.Frame(root, bg="#C3C3C3")      # Creating option frame 

create_btn = tk.Button(options_frame, text="Create contacts", font=("Bold", 18), bg="#C3C3C3", bd=0, command=lambda:indicate(create_indicate, create_page))
create_btn.place(x=15, y=250)
create_indicate = tk.Label(options_frame, text="", bg="#C3C3C3")
create_indicate.place(x=3, y=250, width=5, height=45)

view_btn = tk.Button(options_frame, text="View contacts", font=("Bold", 18),  bg="#C3C3C3", bd=0, command=lambda:indicate(view_indicate, view_page))
view_btn.place(x=15, y=300)
view_indicate = tk.Label(options_frame, text="", bg="#C3C3C3")
view_indicate.place(x=3, y=300, width=5, height=45)

edit_btn = tk.Button(options_frame, text="Edit Contacts", font=("Bold", 18),  bg="#C3C3C3", bd=0, command=lambda:indicate(edit_indicate, edit_page))
edit_btn.place(x=15, y=350)
edit_indicate = tk.Label(options_frame, text="", bg="#C3C3C3")
edit_indicate.place(x=3, y=350, width=5, height=45)

delete_btn = tk.Button(options_frame, text="Delete contacts", font=("Bold", 18),  bg="#C3C3C3", bd=0, command=lambda:indicate(delete_indicate, delete_page))
delete_btn.place(x=15, y=400)
delete_indicate = tk.Label(options_frame, text="", bg="#C3C3C3")
delete_indicate.place(x=3, y=400, width=5, height=45)

about_btn = tk.Button(options_frame, text="About App", font=("Bold", 18),  bg="#C3C3C3", bd=0, command=lambda:indicate(about_indicate, about_page))
about_btn.place(x=15, y=450)
about_indicate = tk.Label(options_frame, text="", bg="#C3C3C3")
about_indicate.place(x=3, y=450, width=5, height=45)

img = Image.open("image.jpg")                   # Adding an image 
img = img.resize((250, 215), Image.LANCZOS)
image = img.convert("RGBA")
data = image.getdata()
bg_color = (195, 195, 195, 255)

bgColor = []                                    # Making background color of an image same as option frame
for item in data:
    if item[0] == 255 and item[1] == 255 and item[2] == 255:
       bgColor.append(bg_color)
    else:
       bgColor.append(item)

image.putdata(bgColor)

photoImage = ImageTk.PhotoImage(image)
label = tk.Label(options_frame, image=photoImage, bg="#C3C3C3")
label.place(x=-27, y=20)

options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=215, height=700)

main_frame = tk.Frame(root)                     # Creating main frame
main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(width=1015, height=700)

login_page()
root.mainloop()
