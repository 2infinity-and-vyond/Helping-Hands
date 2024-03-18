import tkinter as tk
import sqlite3
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import PhotoImage


# Connect to the SQLite database
conn = sqlite3.connect('directory.db')
cursor = conn.cursor()

# Create contacts table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY,
                    first_initial TEXT,
                    last_name TEXT,
                    subject TEXT,
                    location TEXT,
                    extension TEXT
                )''')
conn.commit()

# Function to insert data into SQLite
def add(firstInitial, lastName, subject, location, extension):
    cursor.execute('''INSERT INTO contacts (first_initial, last_name, subject, location, extension)
                      VALUES (?, ?, ?, ?, ?)''', (firstInitial.capitalize(), lastName.capitalize(), subject.capitalize(), location, extension))
    conn.commit()

# Function to remove data from SQLite
def remove(lastName):
    cursor.execute('''SELECT * FROM contacts WHERE last_name = ?''', (lastName.capitalize(),))
    contacts = cursor.fetchall()
    if len(contacts) == 0:
        return "No contacts found with that last name."
    elif len(contacts) == 1:
        cursor.execute('''DELETE FROM contacts WHERE last_name = ?''', (lastName.capitalize(),))
        conn.commit()
        return "Contact removed successfully."
    else:
        choice = simpledialog.askinteger("Multiple Contacts Found",
                                          f"There are multiple contacts found with the last name '{lastName}'. Please select the number of the contact you want to remove:\n" +
                                          "\n".join([f"{i+1}. {contact[0]}. {contact[1]} {contact[2]}" for i, contact in enumerate(contacts)]))
        if choice is not None and 0 < choice <= len(contacts):
            cursor.execute('''DELETE FROM contacts WHERE id = ?''', (contacts[choice-1][0],))
            conn.commit()
            return "Contact removed successfully."
        else:
            return "Invalid choice or operation cancelled."

# Function to search for contacts in SQLite
def search(user_input):
    cursor.execute('''SELECT * FROM contacts WHERE last_name = ?''', (user_input.capitalize(),))
    contacts = cursor.fetchall()
    return contacts


# Function to retrieve subjects from SQLite
def get_selected_subject():
    selected = selected_subject.get()
    predefined_subjects = ["Math", "Science", "English", "Business", "Sponsor"]
    display_text.delete(1.0, tk.END)

    # Check if the selected subject is one of the predefined subjects
    if selected not in predefined_subjects:
        # Create a string of placeholders for the SQL query
        placeholders = ', '.join(['?'] * len(predefined_subjects))

        # Generate the SQL query dynamically to exclude predefined subjects
        query = f'''SELECT * FROM contacts WHERE subject NOT IN ({placeholders})'''
        cursor.execute(query, predefined_subjects)

        contacts = cursor.fetchall()
        for contact in contacts:
            display_text.insert(tk.END, f"{contact[1]} {contact[2]}, {contact[3]}, {contact[4]}, {contact[5]}\n")
    else:
        cursor.execute('''SELECT * FROM contacts WHERE subject = ?''', (selected,))
        contacts = cursor.fetchall()
        for contact in contacts:
            display_text.insert(tk.END, f"{contact[1]} {contact[2]}, {contact[3]}, {contact[4]}, {contact[5]}\n")


# Function to open new window for input
def open_input_window():
    input_window = tk.Toplevel(root)
    input_window.title("Add Contact")

    tk.Label(input_window, text="First Initial:").grid(row=0, column=0)
    first_initial_entry = tk.Entry(input_window)
    first_initial_entry.grid(row=0, column=1)

    tk.Label(input_window, text="Last Name:").grid(row=1, column=0)
    last_name_entry = tk.Entry(input_window)
    last_name_entry.grid(row=1, column=1)

    tk.Label(input_window, text="Subject:").grid(row=2, column=0)
    subject_entry = tk.Entry(input_window)
    subject_entry.grid(row=2, column=1)

    tk.Label(input_window, text="Location:").grid(row=3, column=0)
    location_entry = tk.Entry(input_window)
    location_entry.grid(row=3, column=1)

    tk.Label(input_window, text="Extension:").grid(row=4, column=0)
    extension_entry = tk.Entry(input_window)
    extension_entry.grid(row=4, column=1)

    submit_button = tk.Button(input_window, text="Submit", command=lambda: submit_contact(first_initial_entry.get(),
                                                                                           last_name_entry.get(),
                                                                                           subject_entry.get(),
                                                                                           location_entry.get(),
                                                                                           extension_entry.get(),
                                                                                           input_window), borderwidth=0, highlightthickness=0)
    submit_button.grid(row=5, columnspan=2)

# Function to handle submission of contact data
def submit_contact(first_initial, last_name, subject, location, extension, input_window):
    add(first_initial, last_name, subject, location, extension)
    input_window.destroy()

# Function to open remove window
def open_remove_window():
    remove_window = tk.Toplevel(root)
    remove_window.title("Remove Contact")

    tk.Label(remove_window, text="ID:").grid(row=0, column=0)
    id_entry = tk.Entry(remove_window)
    id_entry.grid(row=0, column=1)

    remove_button = tk.Button(remove_window, text="Remove", command=lambda: remove_contact(id_entry.get(), remove_window), borderwidth=0, highlightthickness=0)
    remove_button.grid(row=1, columnspan=2)

# Function to handle removal of contact data
def remove_contact(contact_id, window):
    try:
        contact_id = int(contact_id)
        cursor.execute('''DELETE FROM contacts WHERE id = ?''', (contact_id,))
        conn.commit()
        messagebox.showinfo("Remove Contact", "Contact removed successfully.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid contact ID.")
    window.destroy()

# Function to display all contacts
def display_all_contacts():
    display_text.delete(1.0, tk.END)
    cursor.execute('''SELECT * FROM contacts''')
    contacts = cursor.fetchall()
    for contact in contacts:
        display_text.insert(tk.END, f"{contact[0]}. {contact[1]} {contact[2]}, {contact[3]}, {contact[4]}, {contact[5]}\n")

# Create the main Tkinter window
root = tk.Tk()
root.title("Helping Hands")
root.geometry("650x300")
root.configure(bg='#5CE1E6')

#Initialize Logo
logo_image = PhotoImage(file="Logo.png")

#Create a Label to display the image
logo_label = tk.Label(root, image=logo_image, borderwidth=0, highlightthickness=0)
logo_label.grid(row=1, column=1, sticky='w', padx=(0,100), columnspan=3)


# Welcome message
welcome_label = tk.Label(root, text="Welcome to Helping Hands!", font=("Arial", 24), bg= '#5CE1E6')
welcome_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)


# Create a button to retrieve input
search_img = PhotoImage(file="search.png")
search_button = tk.Button(root, image=search_img, command=lambda: get_user_input(), borderwidth=0, highlightthickness=0)
search_button.grid(row=1, column=0, sticky="ne", padx=(0,70), columnspan=2)


# Create an input bar
search_input = tk.Entry(root, width=25)
search_input.grid(row=1, column=0, sticky="ne", padx= (0,55), columnspan = 2,)
search_input.insert(0, 'Enter last name...')


# Create a button to open input window
add_img = PhotoImage(file="add.png")
add_button = tk.Button(root, image=add_img, command=open_input_window, borderwidth=0, highlightthickness=0)
add_button.grid(row=1, column=0, sticky="nw",padx=(100,0), pady=(140,0))

# Create a button to open remove window
remove_img = PhotoImage(file="remove.png")
remove_button = tk.Button(root, image=remove_img, command=open_remove_window, borderwidth=0, highlightthickness=0)
remove_button.grid(row=1, column=0, sticky='n',padx=(80,0),pady=(140,0))

# Create a button to display all contacts
display_all_img = PhotoImage(file="display.png")
display_all_button = tk.Button(root, image=display_all_img, command=display_all_contacts, borderwidth=0, highlightthickness=0)
display_all_button.grid(row=1, column=0, sticky="nw", padx=(0, 0),pady=(140,0) )


# Create options for dropdown menu
subjects = ["Science", "English", "Math", "Business", "Sponsor","Other"]

# Initialize dropdown menu selections
selected_subject = tk.StringVar(root)
selected_subject.set(subjects[0])  # Set the default value

# Create a button to collect info from filter
filter_img = PhotoImage(file="filter.png")
filter_button = tk.Button(root, image=filter_img, command=get_selected_subject, borderwidth=0, highlightthickness=0)
filter_button.grid(row=1, column=0, sticky="ne",  padx= (20,120), columnspan = 2, pady=(110,0))

# Create the dropdown menu
subject_menu = tk.OptionMenu(root, selected_subject, *subjects)
subject_menu.grid(row=1, column=0, sticky="ne", padx= (0,120), columnspan = 2, pady=(100,0))

# Initialize text box
display_text = tk.Text(root, width=40, height=10)
display_text.grid(row=1, column=0, sticky='nw', columnspan=2)

# Display all contacts upon opening
display_all_contacts()

def get_user_input():
    user_input = search_input.get()
    contacts = search(user_input)
    display_text.delete(1.0, tk.END)
    if not contacts:
        display_text.insert(tk.END, "No Partners Found\n")
    else:
        for contact in contacts:
            display_text.insert(tk.END, f"{contact[1]} {contact[2]}, {contact[3]}, {contact[4]}, {contact[5]}\n")
    search_input.delete(0, "end")  # delete all the text in the entry

#Deleting ghost text on click
def on_entry_click(event):
    if search_input.get() == 'Enter last name...':
        search_input.delete(0, "end")
        search_input.insert(0, '')
        search_input.config(fg='black')

#Replacing ghost text
def on_focusout(event):
    if search_input.get() == '':
        search_input.insert(0, 'Enter last name...')
        search_input.config(fg='grey')

search_input.bind('<FocusIn>', on_entry_click)
search_input.bind('<FocusOut>', on_focusout)
search_input.config(fg='grey')

root.mainloop()