import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

def run_register():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Please enter a name.")
        return

    status_label.config(text="📸 Capturing images...")

    def process():
        subprocess.run(["python", "register.py", name])
        status_label.config(text="✅ Captured images. Encoding...")

        subprocess.run(["python", "encode.py"])
        status_label.config(text="✅ Encoded. Starting recognition...")

        subprocess.run(["python", "recognize.py"])
        status_label.config(text="✅ Recognition session completed.")

    threading.Thread(target=process).start()

# GUI
window = tk.Tk()
window.title("Face Recognition Attendance")
window.geometry("400x250")
window.configure(bg="#f0f0f0")

tk.Label(window, text="Enter Your Name:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
name_entry = tk.Entry(window, font=("Arial", 12), width=30)
name_entry.pack()

tk.Button(window, text="Start Registration", font=("Arial", 12), command=run_register, bg="#4caf50", fg="white").pack(pady=20)

status_label = tk.Label(window, text="", font=("Arial", 12), bg="#f0f0f0", fg="blue")
status_label.pack(pady=10)

window.mainloop()
