from PyPDF2 import PdfMerger  # In older versions, use PdfFileMerger

merger = PdfMerger()

pdfs = ["4-139.pdf", "140-.pdf"]  # Replace with your actual PDF paths

for pdf in pdfs:
    merger.append(pdf)

merger.write("merged_output.pdf")
merger.close()
