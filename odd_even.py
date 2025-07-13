from PyPDF2 import PdfReader, PdfWriter

# Paths to your files
even_pdf_path = 'Answer even.pdf'  # pages 4 to 56
odd_pdf_path = 'Answer odd.pdf'  # pages 57 to 5 in reverse

# Load the PDFs
even_reader = PdfReader(even_pdf_path)
odd_reader = PdfReader(odd_pdf_path)

# Output writer
writer = PdfWriter()

# Both should have the same number of pages (26 if pages are from 4-56 and 5-57)
num_pages = len(even_reader.pages)

for i in range(num_pages):
    # print(i)
    # Get odd page from the reverse list
    even_page = even_reader.pages[num_pages - 1 - i]  # reversed
    # odd_page = odd_reader.pages[i]
    odd_page = odd_reader.pages[i]

    writer.add_page(odd_page)
    writer.add_page(even_page)
  

# Save the merged PDF
with open('Answer.pdf', 'wb') as f_out:
    writer.write(f_out)

print("Merging complete. Output saved to 'merged_output.pdf'")
