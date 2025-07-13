from PyPDF2 import PdfReader, PdfWriter
import os

def insert_pdf_page(source_pdf_path, dest_pdf_path, page_to_insert_index, insert_at_index, output_pdf_path):
    """
    Inserts a specific page from a source PDF into a destination PDF.
    This version explicitly manages file handles to prevent 'seek of closed file' errors.

    Args:
        source_pdf_path (str): Path to the PDF file from which to take the page.
        dest_pdf_path (str): Path to the PDF file into which to insert the page.
        page_to_insert_index (int): The 0-based index of the page to insert from the source PDF.
        insert_at_index (int): The 0-based index where the page should be inserted
                                in the destination PDF.
        output_pdf_path (str): Path to save the new PDF with the inserted page.
    """
    source_file = None
    dest_file = None
    output_file = None # Initialize file objects to None for the finally block

    try:
        # 1. Validate file paths
        if not os.path.exists(source_pdf_path):
            print(f"Error: Source PDF file not found at '{source_pdf_path}'.")
            return
        if not os.path.exists(dest_pdf_path):
            print(f"Error: Destination PDF file not found at '{dest_pdf_path}'.")
            return

        # Open all files directly and keep them open until explicitly closed
        source_file = open(source_pdf_path, 'rb')
        dest_file = open(dest_pdf_path, 'rb')
        
        source_reader = PdfReader(source_file)
        dest_reader = PdfReader(dest_file)
        writer = PdfWriter()

        # Check if the page_to_insert_index is valid for the source PDF
        if page_to_insert_index >= len(source_reader.pages) or page_to_insert_index < 0:
            print(f"Error: Page index {page_to_insert_index} is out of bounds for '{source_pdf_path}' (has {len(source_reader.pages)} pages).")
            return

        # Get the page from the source PDF. PyPDF2 will keep a reference to source_file.
        page_to_insert = source_reader.pages[page_to_insert_index]

        # Adjust insert_at_index if it's beyond the number of pages in dest_pdf
        if insert_at_index > len(dest_reader.pages):
            insert_at_index = len(dest_reader.pages)
        elif insert_at_index < 0:
            insert_at_index = 0 # Insert at the beginning if negative index provided

        # Add pages from the destination PDF before the insertion point
        for i in range(insert_at_index):
            writer.add_page(dest_reader.pages[i])

        # Insert the page from the source PDF
        writer.add_page(page_to_insert)

        # Add the remaining pages from the destination PDF
        for i in range(insert_at_index, len(dest_reader.pages)):
            writer.add_page(dest_reader.pages[i])

        # Open the output file and write the new PDF
        output_file = open(output_pdf_path, 'wb')
        writer.write(output_file)
        
        print(f"Page {page_to_insert_index + 1} from '{source_pdf_path}' successfully inserted into '{dest_pdf_path}' at position {insert_at_index + 1} and saved as '{output_pdf_path}'.")

    except FileNotFoundError:
        print("Error: One or more of the PDF files not found. Please check the paths.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure all opened files are closed
        if source_file:
            source_file.close()
        if dest_file:
            dest_file.close()
        if output_file:
            output_file.close()

# --- Usage Example with your provided file names ---
# Make sure you have these files for testing in the same directory as your script:
# 11.pdf: A PDF from which you want to take the page (page 1, index 0).
# odd.pdf: The PDF into which you want to insert the page.
source_pdf = 'Unit9.pdf'
destination_pdf = 'Unit11.pdf'
output_pdf = 'Unit11_with_inserted_page.pdf'

# To insert the first page (index 0) from '11.pdf'
# into 'odd.pdf' at the 6th position (index 5)
print("--- Attempting to insert page from '11.pdf' into 'odd.pdf' ---")
insert_pdf_page(source_pdf, destination_pdf, 19, 0, output_pdf)
print("\n")

# You can uncomment and modify these for other scenarios:

# # To insert the first page (index 0) from '11.pdf'
# # at the very beginning of 'odd.pdf' (index 0)
# print("--- Attempting to insert at beginning ---")
# insert_pdf_page(source_pdf, destination_pdf, 0, 0, 'odd_with_inserted_page_at_beginning.pdf')
# print("\n")

# # To insert the first page (index 0) from '11.pdf'
# # at the very end of 'odd.pdf' (using a large index)
# print("--- Attempting to insert at end ---")
# insert_pdf_page(source_pdf, destination_pdf, 0, 999, 'odd_with_inserted_page_at_end.pdf') # 999 will be adjusted to end
# print("\n")

# # Example: Handle an invalid page index in source (if 11.pdf doesn't have 5 pages)
# print("--- Running Example (Invalid Source Page Index) ---")
# insert_pdf_page(source_pdf, destination_pdf, 4, 0, 'output_invalid_source_page.pdf')
# print("\n")

# # Example: Handle non-existent files
# print("--- Running Example (Non-existent Files) ---")
# insert_pdf_page('non_existent_source.pdf', 'non_existent_dest.pdf', 0, 0, 'output_non_existent.pdf')