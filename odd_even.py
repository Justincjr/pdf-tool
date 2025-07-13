import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

def merge_pdfs(even_path, odd_path, output_path):
    try:
        even_reader = PdfReader(even_path)
        odd_reader = PdfReader(odd_path)

        writer = PdfWriter()
        num_pages = len(even_reader.pages)

        for i in range(num_pages):
            even_page = even_reader.pages[num_pages - 1 - i]  # reversed
            odd_page = odd_reader.pages[i]
            writer.add_page(odd_page)
            writer.add_page(even_page)

        with open(output_path, 'wb') as f_out:
            writer.write(f_out)

        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

def select_even_file():
    path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if path:
        even_entry.delete(0, tk.END)
        even_entry.insert(0, path)

def select_odd_file():
    path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if path:
        odd_entry.delete(0, tk.END)
        odd_entry.insert(0, path)

def merge_files():
    even_path = even_entry.get()
    odd_path = odd_entry.get()
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    
    if not even_path or not odd_path or not output_path:
        messagebox.showwarning("Input Missing", "Please select both input files and specify an output filename.")
        return

    success = merge_pdfs(even_path, odd_path, output_path)
    if success:
        messagebox.showinfo("Success", f"Merged PDF saved to:\n{output_path}")

# --- GUI Setup ---
root = tk.Tk()
root.title("PDF Odd-Even Merger")
root.geometry("500x250")

tk.Label(root, text="Even PDF (reversed):").pack(pady=(10, 0))
even_entry = tk.Entry(root, width=50)
even_entry.pack()
tk.Button(root, text="Browse", command=select_even_file).pack()

tk.Label(root, text="Odd PDF:").pack(pady=(10, 0))
odd_entry = tk.Entry(root, width=50)
odd_entry.pack()
tk.Button(root, text="Browse", command=select_odd_file).pack()

tk.Button(root, text="Merge PDFs", command=merge_files, bg="#4CAF50", fg="white", height=2).pack(pady=20)

root.mainloop()
