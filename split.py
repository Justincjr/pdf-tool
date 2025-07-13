import PyPDF2

# Open the original PDF in read-binary mode
with open("pure_physics_notes.pdf", "rb") as infile:
    reader = PyPDF2.PdfReader(infile)
    writer = PyPDF2.PdfWriter()

    # Add pages 1 to 50 (0-indexed: 0 to 49)
    for page_num in range(222, 247):
        writer.add_page(reader.pages[page_num])

    # Write the output PDF
    with open("summary.pdf", "wb") as outfile:
        writer.write(outfile)
