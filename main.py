import tkinter
import customtkinter
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import hashlib

# Custom Tkinter setup
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

# Define functions for database operations
class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT,
                                email TEXT,
                                password TEXT
                            )''')
        self.connection.commit()

    def insert_user(self, username, email, password):
        try:
            # Hash the password before inserting it into the database
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute('''INSERT INTO users (username, email, password)
                                    VALUES (?, ?, ?)''', (username, email, hashed_password))
            self.connection.commit()
            return True  # Registration successful
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error occurred: {e}")
            return False  # Registration failed

    def get_user(self, username, password):
        # Hash the password before querying the database
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('''SELECT * FROM users
                                WHERE username=? AND password=?''', (username, hashed_password))
        return self.cursor.fetchone()

    def update_password(self, username, email, password):
        # Hash the new password before updating it in the database
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute('''UPDATE users
                                    SET password=?
                                    WHERE username=? AND email=?''', (hashed_password, username, email))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            return False


# Login window
class LoginWindow(tkinter.Tk):
    def __init__(self, db):
        self.db = db
        super().__init__()

        # Center the window on the screen
        self.center_window()

        self.geometry("600x400")
        self.title("Login")
        self.iconbitmap("Assets/icon.ico")
        self.configure(bg="#333333")

        img1 = Image.open("Assets/background.jpg")
        self.bg_image = ImageTk.PhotoImage(img1)
        l1 = customtkinter.CTkLabel(master=self, image=self.bg_image)
        l1.pack()

        frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        l2 = customtkinter.CTkLabel(master=frame, text="Log into your Account", font=("Arial", 20))
        l2.place(x=60, y=45)

        self.username_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Username")
        self.username_entry.place(x=50, y=110)

        self.password_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Password", show="*")
        self.password_entry.place(x=50, y=160)

        forgotPassword_link = customtkinter.CTkLabel(master=frame, text="Forgot Password?", width=22, cursor="hand2")
        forgotPassword_link.place(x=165, y=190)
        forgotPassword_link.bind("<Button-1>", lambda e: self.on_forgot_password_click())

        login_button = customtkinter.CTkButton(master=frame, text="Login", width=220, cursor="hand2", command=self.authenticate_user)
        login_button.place(x=50, y=230)

        register_button = customtkinter.CTkButton(master=frame, text="Register", width=220, cursor="hand2", command=self.on_register_click)
        register_button.place(x=50, y=280)

    def center_window(self):
        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position x and y coordinates to center the window
        x = (screen_width / 2) - (600 / 2)
        y = (screen_height / 2) - (400 / 2)

        # Set the window's position
        self.geometry(f"600x400+{int(x)}+{int(y)}")

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.db.get_user(username, password)
        if user:
            # User authenticated, proceed with login
            messagebox.showinfo("Success", "Login successful")
        else:
            # Authentication failed, show error message
            messagebox.showerror("Error", "Invalid username or password")  

    def on_register_click(self):
        self.withdraw()  # Hide the login window
        register_window = RegisterWindow(self, self.db)
        register_window.mainloop()
    
    def on_forgot_password_click(self):
        self.withdraw()  # Hide the login window
        forgot_window = ForgotWindow(self, self.db)
        forgot_window.mainloop()

# Register window
class RegisterWindow(tkinter.Toplevel):
    def __init__(self, parent, db):
        self.db = db
        super().__init__(parent)

        #Center the window on the screen
        self.center_window()

        self.geometry("600x400")
        self.title("Register")
        self.iconbitmap("Assets/icon.ico")
        self.configure(bg="#333333")

        img1 = Image.open("Assets/background.jpg")
        self.bg_image = ImageTk.PhotoImage(img1)
        l1 = customtkinter.CTkLabel(master=self, image=self.bg_image)
        l1.pack()

        frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        l2 = customtkinter.CTkLabel(master=frame, text="Create an Account", font=("Arial", 20))
        l2.place(x=80, y=45)

        self.username_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Username")
        self.username_entry.place(x=50, y=110)

        self.email_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Email")
        self.email_entry.place(x=50, y=160)

        self.password_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Password", show="*")
        self.password_entry.place(x=50, y=210)

        register_button = customtkinter.CTkButton(master=frame, text="Register", width=220, cursor="hand2", command=self.register_user)
        register_button.place(x=50, y=260)

        login_button = customtkinter.CTkButton(master=frame, text="Login", width=220, cursor="hand2", command=self.on_login_click)
        login_button.place(x=50, y=310)

    def center_window(self):
        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position x and y coordinates to center the window
        x = (screen_width / 2) - (600 / 2)
        y = (screen_height / 2) - (400 / 2)

        # Set the window's position
        self.geometry(f"600x400+{int(x)}+{int(y)}")

    def register_user(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Check if any of the fields are empty
        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        # Insert user data into the database
        if self.db.insert_user(username, email, password):
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Registration failed!")

    def on_login_click(self):
        self.destroy()  # Close the register window
        self.master.deiconify()  # Re-show the login window

# Forgot password window
class ForgotWindow(tkinter.Toplevel):
    def __init__(self, parent, db):
        self.db = db
        super().__init__(parent)

        #Center the window on the screen
        self.center_window()

        self.geometry("600x400")
        self.title("Forgot Password")
        self.iconbitmap("Assets/icon.ico")
        self.configure(bg="#333333")

        img1 = Image.open("Assets/background.jpg")
        self.bg_image = ImageTk.PhotoImage(img1)
        l1 = customtkinter.CTkLabel(master=self, image=self.bg_image)
        l1.pack()

        frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        l2 = customtkinter.CTkLabel(master=frame, text="Forgot Password", font=("Arial", 20))
        l2.place(x=80, y=45)

        self.username_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Username")
        self.username_entry.place(x=50, y=110)

        self.email_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Email")
        self.email_entry.place(x=50, y=160)

        self.password_entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Password", show="*")
        self.password_entry.place(x=50, y=210)

        reset_button = customtkinter.CTkButton(master=frame, text="Reset", width=220, cursor="hand2", command=self.reset_password)
        reset_button.place(x=50, y=260)

        login_button = customtkinter.CTkButton(master=frame, text="Login", width=220, cursor="hand2", command=self.on_login_click)
        login_button.place(x=50, y=310)

    def center_window(self):
        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position x and y coordinates to center the window
        x = (screen_width / 2) - (600 / 2)
        y = (screen_height / 2) - (400 / 2)

        # Set the window's position
        self.geometry(f"600x400+{int(x)}+{int(y)}")

    # Update the password in the database
    def reset_password(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Check if any of the fields are empty
        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Attempt to update the password in the database
        if self.db.update_password(username, email, password):
            # Check if any rows were affected, indicating a successful update
            if self.db.cursor.rowcount > 0:
                messagebox.showinfo("Success", "Password reset successful!")
            else:
                messagebox.showerror("Error", "User not found or incorrect credentials!")
        else:
            messagebox.showerror("Error", "Password reset unsuccessful!")


    def on_login_click(self):
        self.destroy()  # Close the register window
        self.master.deiconify()  # Re-show the login window

if __name__ == "__main__":
    db = Database("login.db")  # Connect to the database
    app = LoginWindow(db)
    app.mainloop()
