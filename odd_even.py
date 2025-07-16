import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

# --- PDF Functions ---

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

def split_pdf(input_path, start_page, end_page, output_path):
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for i in range(start_page - 1, end_page):  # Adjusting to 0-based index
            writer.add_page(reader.pages[i])

        with open(output_path, "wb") as f_out:
            writer.write(f_out)

        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

def insert_pdf_page(source_pdf_path, dest_pdf_path, page_to_insert_index, insert_at_index, output_pdf_path):
    source_file = dest_file = output_file = None
    try:
        # if not os.path.exists(source_pdf_path):
        #     messagebox.showerror("Error", f"Source PDF not found: {source_pdf_path}")
        #     return False
        # if not os.path.exists(dest_pdf_path):
        #     messagebox.showerror("Error", f"Destination PDF not found: {dest_pdf_path}")
        #     return False

        source_file = open(source_pdf_path, 'rb')
        dest_file = open(dest_pdf_path, 'rb')

        source_reader = PdfReader(source_file)
        dest_reader = PdfReader(dest_file)
        writer = PdfWriter()

        if not (0 <= page_to_insert_index < len(source_reader.pages)):
            messagebox.showerror("Error", f"Invalid source page index: {page_to_insert_index + 1}")
            return False

        page_to_insert = source_reader.pages[page_to_insert_index]

        insert_at_index = max(0, min(insert_at_index, len(dest_reader.pages)))

        for i in range(insert_at_index):
            writer.add_page(dest_reader.pages[i])

        writer.add_page(page_to_insert)

        for i in range(insert_at_index, len(dest_reader.pages)):
            writer.add_page(dest_reader.pages[i])

        output_file = open(output_pdf_path, 'wb')
        writer.write(output_file)
        return True

    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")
        return False
    finally:
        if source_file: source_file.close()
        if dest_file: dest_file.close()
        if output_file: output_file.close()


# --- GUI Functions ---
def open_insert_page_window():
    clear_window()

    tk.Label(root, text="Source PDF (page to insert):").pack(pady=(10, 0))
    source_entry = tk.Entry(root, width=50)
    source_entry.pack()
    tk.Button(root, text="Browse", command=lambda: select_file(source_entry)).pack()

    tk.Label(root, text="Destination PDF (to insert into):").pack(pady=(10, 0))
    dest_entry = tk.Entry(root, width=50)
    dest_entry.pack()
    tk.Button(root, text="Browse", command=lambda: select_file(dest_entry)).pack()

    tk.Label(root, text="Page number to take from source:").pack()
    page_from_entry = tk.Entry(root, width=10)
    page_from_entry.pack()

    tk.Label(root, text="Position to insert into destination:").pack()
    insert_at_entry = tk.Entry(root, width=10)
    insert_at_entry.pack()

    def do_insert():
        source_path = source_entry.get()
        dest_path = dest_entry.get()
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])

        try:
            page_from = int(page_from_entry.get()) - 1
            insert_at = int(insert_at_entry.get()) - 1
        except ValueError:
            messagebox.showerror("Invalid Input", "Page numbers must be integers.")
            return

        if not source_path or not dest_path or not output_path:
            messagebox.showwarning("Missing Input", "Please fill in all required fields.")
            return

        success = insert_pdf_page(source_path, dest_path, page_from, insert_at, output_path)
        if success:
            messagebox.showinfo("Success", f"Page inserted successfully and saved to:\n{output_path}")

    tk.Button(root, text="Insert Page", command=do_insert, bg="#FF9800", fg="white", height=2).pack(pady=20)
    tk.Button(root, text="Back to Menu", command=main_menu).pack()

def open_merge_window():
    clear_window()

    tk.Label(root, text="Even PDF (reversed):").pack(pady=(10, 0))
    even_entry = tk.Entry(root, width=50)
    even_entry.pack()
    tk.Button(root, text="Browse", command=lambda: select_file(even_entry)).pack()

    tk.Label(root, text="Odd PDF:").pack(pady=(10, 0))
    odd_entry = tk.Entry(root, width=50)
    odd_entry.pack()
    tk.Button(root, text="Browse", command=lambda: select_file(odd_entry)).pack()

    def do_merge():
        even_path = even_entry.get()
        odd_path = odd_entry.get()
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])

        if not even_path or not odd_path or not output_path:
            messagebox.showwarning("Input Missing", "Please select both input files and specify an output filename.")
            return

        if merge_pdfs(even_path, odd_path, output_path):
            messagebox.showinfo("Success", f"Merged PDF saved to:\n{output_path}")

    tk.Button(root, text="Merge PDFs", command=do_merge, bg="#4CAF50", fg="white", height=2).pack(pady=20)
    tk.Button(root, text="Back to Menu", command=main_menu).pack()

def open_split_window():
    clear_window()

    tk.Label(root, text="Select PDF to split:").pack(pady=(10, 0))
    input_entry = tk.Entry(root, width=50)
    input_entry.pack()
    tk.Button(root, text="Browse", command=lambda: select_file(input_entry)).pack()

    tk.Label(root, text="Start Page:").pack()
    start_entry = tk.Entry(root, width=10)
    start_entry.pack()

    tk.Label(root, text="End Page:").pack()
    end_entry = tk.Entry(root, width=10)
    end_entry.pack()

    def do_split():
        input_path = input_entry.get()
        try:
            start_page = int(start_entry.get())
            end_page = int(end_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Start and end pages must be numbers.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])

        if not input_path or not output_path:
            messagebox.showwarning("Input Missing", "Please select input file and output filename.")
            return

        if split_pdf(input_path, start_page, end_page, output_path):
            messagebox.showinfo("Success", f"Split PDF saved to:\n{output_path}")

    tk.Button(root, text="Split PDF", command=do_split, bg="#2196F3", fg="white", height=2).pack(pady=20)
    tk.Button(root, text="Back to Menu", command=main_menu).pack()

def main_menu():
    clear_window()

    tk.Label(root, text="PDF Tool", font=("Arial", 18)).pack(pady=20)
    tk.Button(root, text="Merge Odd-Even PDFs for Single Sided Scanning", command=open_merge_window, height=2, width=45).pack(pady=10)
    tk.Button(root, text="Split PDF (Page Range)", command=open_split_window, height=2, width=45).pack(pady=10)
    tk.Button(root, text="Insert Page from another PDF", command=open_insert_page_window, height=2, width=45).pack(pady=10)

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def select_file(entry_widget):
    path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, path)

# --- Main Window Setup ---
root = tk.Tk()
root.title("PDF Tool")
root.geometry("500x400")

main_menu()
root.mainloop()
