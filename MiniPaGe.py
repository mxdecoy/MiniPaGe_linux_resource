# This code is licensed under the MIT License.
# Copyright (c) 2025 mxz
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter.messagebox
import secrets
import os
import sys
import string


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

safe_punctuation = string.punctuation.replace('"', '').replace("'", '').replace('\\', '') # some password policies are crap so...
chars = string.ascii_letters + string.digits + safe_punctuation

def create_pw(digit):
    '''(int) -> str
    Return a new password with the length of digit
    '''
    try:
        digit = int(digit)
        if digit < 12 or digit > 256:
            return 'size matters'
        return ''.join(secrets.choice(chars) for _ in range(digit))
    except ValueError:
        return 'enter a number'


def main():
    root = ThemedTk(theme='black')
    version = '1.1.0'
    root.title(f'MiniPaGe v{version}')
    root.geometry('370x110')
    root.resizable(False, False)
    
    # linux icon
    icon_path = resource_path("icon.png")
    root.iconphoto(True, tk.PhotoImage(file=icon_path))

    
    root.configure(background="#000000")  # Hauptfenster-Hintergrund

    style = ttk.Style()
    style.theme_use('black')
    style.configure('TFrame', background='#000000')
    style.configure('TLabel', background='#000000', foreground='#00FF88')
    style.configure('TEntry', fieldbackground='#222222', foreground='#00FF88')
    style.configure('TButton', background='#000000', foreground='#00FF88')

    frame = ttk.Frame(root, padding=10, style='TFrame')
    frame.grid()

    ttk.Label(frame, text='password length (12–256):', style='TLabel').grid(column=0, row=0, sticky='w')

    digit_var = tk.StringVar()
    digit_entry = ttk.Entry(frame, textvariable=digit_var, width=10, style='TEntry')
    digit_entry.grid(column=1, row=0)

    password_var = tk.StringVar()
    password_entry = ttk.Entry(frame, textvariable=password_var, state='readonly', style='TEntry')
    password_entry.grid(column=0, row=1, columnspan=3, pady=10, sticky='we')


    # pw strength
    def pw_strength(password):
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in safe_punctuation for c in password)

        score = sum([has_upper, has_lower, has_digit, has_symbol])

        if length < 12 or score < 2:
            return 'weak'
        elif length < 16 or score < 3:
            return 'ok'
        else:
            return 'strong'

    # generate pw
    def on_generate():
        password = create_pw(digit_var.get())
        password_var.set(password)

        strength = pw_strength(password)

        if strength == 'weak':
            ampel_var.set('nah, try again')
            ampel_label.config(foreground='red')
        elif strength == 'ok':  
            ampel_var.set('it\'s ok')
            ampel_label.config(foreground='yellow')
        elif strength == 'strong':
            ampel_var.set('nice one!')
            ampel_label.config(foreground='green')

    # show/hide password logic
    show_password = tk.BooleanVar(value=True)
    def toggle_password():
        if show_password.get():
            password_entry.config(show='☻')
            show_button.config(text='show')
            show_password.set(False)
        else:
            password_entry.config(show='')
            show_button.config(text='hide')
            show_password.set(True)

    # copy password to clipboard
    def copy_password():
        password = password_var.get()
        if password:
            root.clipboard_clear()
            root.clipboard_append(password)
            root.update()
            tkinter.messagebox.showinfo("copied", "password copied to clipboard!")



    generate_button = ttk.Button(frame, text='generate', command=on_generate, style='TButton')
    generate_button.grid(column=2, row=0)

    # hide and show button
    show_button = ttk.Button(frame, text='hide', command=toggle_password, style='TButton')
    show_button.grid(column=1, row=2, sticky='w')

    # copy button
    copy_button = ttk.Button(frame, text='copy', command=copy_password, style='TButton')
    copy_button.grid(column=2, row=2, sticky='e')

    # ampel links neben copy button
    ampel_var = tk.StringVar()
    ampel_label = ttk.Label(frame, textvariable=ampel_var, font=('Consolas', 9))
    ampel_label.grid(column=0, row=2, sticky='w')  


    root.mainloop()

if __name__ == "__main__":
    main()