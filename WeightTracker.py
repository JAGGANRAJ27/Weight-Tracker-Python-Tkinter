import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

# --- Database functions ---
def adduser(name, username, password):
    conn = sqlite3.connect("weightapp.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, username TEXT UNIQUE, password TEXT)")
    try:
        c.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", (name, username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    conn.close()

def checkuser(username, password):
    conn = sqlite3.connect("weightapp.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def getusername(username, password):
    global profilename
    conn = sqlite3.connect("weightapp.db")
    c = conn.cursor()
    c.execute("SELECT name FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()
    if data:
        profilename = data[0]
    conn.close()

# --- Graph function ---
def graph_data():
    conn = sqlite3.connect("weightapp.db")
    c = conn.cursor()
    c.execute("SELECT date, weight FROM weightmeasure")
    data = c.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("No Data", "No weight data to plot.")
        return

    dates = [d[0] for d in data]
    weights = [float(d[1]) for d in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights, marker='o', linestyle='-', color='blue')
    plt.title(f"Weight Progress for {profilename}")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# --- Main Application ---
profilename = ""

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

def login_register_ui():
    root = ctk.CTk()
    root.geometry("900x600")
    root.title("Weight Tracker - Login / Register")

    # --- Left Frame (Login) ---
    frame_login = ctk.CTkFrame(root, corner_radius=15)
    frame_login.place(relx=0.05, rely=0.1, relwidth=0.4, relheight=0.8)

    ctk.CTkLabel(frame_login, text="Login", font=ctk.CTkFont(size=25, weight="bold")).pack(pady=20)

    ctk.CTkLabel(frame_login, text="Username").pack(pady=(10, 5))
    login_username = ctk.StringVar()
    entry_login_user = ctk.CTkEntry(frame_login, textvariable=login_username, placeholder_text="Enter username")
    entry_login_user.pack(pady=5, padx=20)

    ctk.CTkLabel(frame_login, text="Password").pack(pady=(10, 5))
    login_password = ctk.StringVar()
    entry_login_pass = ctk.CTkEntry(frame_login, textvariable=login_password, placeholder_text="Enter password", show="*")
    entry_login_pass.pack(pady=5, padx=20)

    def login():
        a = login_username.get()
        b = login_password.get()
        if checkuser(a, b):
            getusername(a, b)
            # Delay destroy to avoid pending animation callbacks
            root.after(100, lambda: (root.destroy(), appwindow()))
        else:
            messagebox.showinfo('Login Failed', 'Invalid Username or Password')
            entry_login_user.delete(0, 'end')
            entry_login_pass.delete(0, 'end')

    btn_login = ctk.CTkButton(frame_login, text="Login", command=login)
    btn_login.pack(pady=20)

    # --- Right Frame (Register) ---
    frame_register = ctk.CTkFrame(root, corner_radius=15)
    frame_register.place(relx=0.55, rely=0.1, relwidth=0.4, relheight=0.8)

    ctk.CTkLabel(frame_register, text="Register", font=ctk.CTkFont(size=25, weight="bold")).pack(pady=20)

    ctk.CTkLabel(frame_register, text="Name").pack(pady=(10, 5))
    register_name = ctk.StringVar()
    entry_reg_name = ctk.CTkEntry(frame_register, textvariable=register_name, placeholder_text="Enter full name")
    entry_reg_name.pack(pady=5, padx=20)

    ctk.CTkLabel(frame_register, text="Username").pack(pady=(10, 5))
    register_username = ctk.StringVar()
    entry_reg_user = ctk.CTkEntry(frame_register, textvariable=register_username, placeholder_text="Choose username")
    entry_reg_user.pack(pady=5, padx=20)

    ctk.CTkLabel(frame_register, text="Password").pack(pady=(10, 5))
    register_password = ctk.StringVar()
    entry_reg_pass = ctk.CTkEntry(frame_register, textvariable=register_password, placeholder_text="Enter password", show="*")
    entry_reg_pass.pack(pady=5, padx=20)

    ctk.CTkLabel(frame_register, text="Confirm Password").pack(pady=(10, 5))
    register_repassword = ctk.StringVar()
    entry_reg_repass = ctk.CTkEntry(frame_register, textvariable=register_repassword, placeholder_text="Confirm password", show="*")
    entry_reg_repass.pack(pady=5, padx=20)

    def register():
        a = register_name.get().strip()
        b = register_username.get().strip()
        c = register_password.get()
        d = register_repassword.get()
        if a == "" or b == "" or c == "" or d == "":
            messagebox.showinfo('Error', 'Some Fields are Empty')
        elif c != d:
            messagebox.showinfo('Error', 'Passwords do not match')
        elif len(c) < 6:
            messagebox.showinfo('Error', 'Password must be at least 6 characters')
        else:
            adduser(a, b, c)
            messagebox.showinfo('Success', 'Registration Successful')
            entry_reg_name.delete(0, 'end')
            entry_reg_user.delete(0, 'end')
            entry_reg_pass.delete(0, 'end')
            entry_reg_repass.delete(0, 'end')

    btn_register = ctk.CTkButton(frame_register, text="Register", command=register)
    btn_register.pack(pady=20)

    root.mainloop()

def appwindow():
    app = ctk.CTk()
    app.title("Weight Tracker")
    app.geometry("900x700")
    app.resizable(False, False)

    def connect1():
        conn = sqlite3.connect("weightapp.db")
        j = conn.cursor()
        j.execute("CREATE TABLE IF NOT EXISTS weightmeasure(id INTEGER PRIMARY KEY, weight TEXT, date TEXT, sample TEXT)")
        conn.commit()
        conn.close()
    connect1()

    def insert(weight, date, sample):
        conn = sqlite3.connect("weightapp.db")
        j = conn.cursor()
        j.execute("INSERT INTO weightmeasure VALUES(NULL,?,?,?)", (weight, date, sample))
        conn.commit()
        conn.close()

    def view():
        conn = sqlite3.connect("weightapp.db")
        j = conn.cursor()
        j.execute("SELECT * FROM weightmeasure")
        rows = j.fetchall()
        conn.close()
        return rows

    def deletealldata():
        if messagebox.askyesno("Delete All", "Are you sure you want to delete all data?"):
            conn = sqlite3.connect("weightapp.db")
            j = conn.cursor()
            j.execute("DELETE FROM weightmeasure")
            conn.commit()
            conn.close()
            listbox.delete("0.0", 'end')
            messagebox.showinfo('Successful', 'All data deleted')

    def insertitems():
        a = weight_var.get().strip()
        b = date_var.get().strip()
        c = reference_var.get().strip()
        if a == "" or b == "":
            messagebox.showinfo("Error", "Weight and Date fields cannot be empty")
        elif len(b) != 10 or b.count('-') != 2:
            messagebox.showinfo("Error", "DATE should be in format dd-mm-yyyy")
        else:
            try:
                float(a)
                insert(a, b, c)
                weight_var.set("")
                date_var.set("")
                refresh_list()
            except ValueError:
                messagebox.showinfo("Error", "Weight must be a number")

    def refresh_list():
        listbox.delete("0.0", 'end')
        listbox.insert('end', f"{'SI.No':<10}{'Weight':<15}{'Date':<15}\n")
        listbox.insert('end', "-" * 40 + "\n")
        for row in view():
            f = f"{row[0]:<10}{row[1]:<15}{row[2]:<15}\n"
            listbox.insert('end', f)

    # UI
    title_label = ctk.CTkLabel(app, text="Weight Tracker", font=ctk.CTkFont(size=35, weight="bold"), fg_color="yellow", corner_radius=10)
    title_label.pack(padx=20, pady=10, fill='x')

    welcome_label = ctk.CTkLabel(app, text=f"Welcome, '{profilename}'", font=ctk.CTkFont(size=25), fg_color="salmon", corner_radius=10)
    welcome_label.pack(padx=20, pady=10, fill='x')

    frame_inputs = ctk.CTkFrame(app, corner_radius=15)
    frame_inputs.pack(pady=20, padx=20, fill='x')

    ctk.CTkLabel(frame_inputs, text="Enter Your Weight (kg)").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    weight_var = ctk.StringVar()
    entry_weight = ctk.CTkEntry(frame_inputs, textvariable=weight_var)
    entry_weight.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(frame_inputs, text="Date (dd-mm-yyyy)").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    date_var = ctk.StringVar()
    entry_date = ctk.CTkEntry(frame_inputs, textvariable=date_var)
    entry_date.grid(row=1, column=1, padx=10, pady=10)

    reference_var = ctk.StringVar()

    frame_list = ctk.CTkFrame(app, corner_radius=15)
    frame_list.pack(padx=20, pady=10, fill='both', expand=True)

    listbox = ctk.CTkTextbox(frame_list, width=600, height=200, font=ctk.CTkFont(size=15), corner_radius=10)
    listbox.pack(side='left', fill='both', expand=True, padx=10, pady=10)

    scrollbar = ctk.CTkScrollbar(frame_list, command=listbox.yview)
    scrollbar.pack(side='right', fill='y')
    listbox.configure(yscrollcommand=scrollbar.set)

    frame_buttons = ctk.CTkFrame(app)
    frame_buttons.pack(pady=10)

    btn_add = ctk.CTkButton(frame_buttons, text="Add Weight", command=insertitems)
    btn_add.grid(row=0, column=0, padx=10, pady=10)

    btn_delete = ctk.CTkButton(frame_buttons, text="Delete All Data", command=deletealldata)
    btn_delete.grid(row=0, column=1, padx=10, pady=10)

    btn_graph = ctk.CTkButton(frame_buttons, text="Show Graph", command=graph_data)
    btn_graph.grid(row=0, column=2, padx=10, pady=10)

    refresh_list()
    app.mainloop()

if __name__ == "__main__":
    login_register_ui()
