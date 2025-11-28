import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import io
import sys

def remove_red_lines(input_path, output_path, red_threshold=100):
    """
    Remove red lines from a PDF by converting pages to images,
    filtering out red pixels, and reconstructing the PDF.
    
    Args:
        input_path: Path to input PDF
        output_path: Path to save the output PDF
        red_threshold: How aggressively to remove red (higher = more aggressive)
    """
    # Open the PDF
    doc = fitz.open(input_path)
    new_doc = fitz.open()
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Render page to image at high resolution
        mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_array = np.array(img)
        
        # Identify red pixels
        # Red pixels have high R, low G, low B values
        r = img_array[:, :, 0].astype(np.int16)
        g = img_array[:, :, 1].astype(np.int16)
        b = img_array[:, :, 2].astype(np.int16)
        
        # Create mask for red pixels
        # A pixel is "red" if R is high and significantly greater than G and B
        red_mask = (
            (r > 150) &  # R channel is high
            (r - g > red_threshold) &  # R is much greater than G
            (r - b > red_threshold)    # R is much greater than B
        )
        
        # Replace red pixels with white
        img_array[red_mask] = [255, 255, 255]
        
        # Convert back to PIL Image
        cleaned_img = Image.fromarray(img_array)
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        cleaned_img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Create new page with same dimensions
        new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
        
        # Insert the cleaned image
        new_page.insert_image(new_page.rect, stream=img_bytes.read())
        
        print(f"Processed page {page_num + 1}/{len(doc)}")
    
    # Save the new PDF
    new_doc.save(output_path)
    new_doc.close()
    doc.close()
    
    print(f"\nDone! Saved to: {output_path}")


def remove_red_annotations(input_path, output_path):
    """
    Remove red annotations/markup from a PDF without converting to images.
    This preserves text quality but only works for annotation-based red marks.
    """
    doc = fitz.open(input_path)
    
    for page in doc:
        # Get all annotations
        annots = page.annots()
        if annots:
            annots_to_delete = []
            for annot in annots:
                # Check if annotation has red color
                colors = annot.colors
                if colors:
                    stroke = colors.get('stroke', None)
                    fill = colors.get('fill', None)
                    
                    # Check if stroke or fill is red-ish
                    if stroke and len(stroke) >= 3:
                        if stroke[0] > 0.7 and stroke[1] < 0.3 and stroke[2] < 0.3:
                            annots_to_delete.append(annot)
                            continue
                    if fill and len(fill) >= 3:
                        if fill[0] > 0.7 and fill[1] < 0.3 and fill[2] < 0.3:
                            annots_to_delete.append(annot)
                            continue
            
            # Delete red annotations
            for annot in annots_to_delete:
                page.delete_annot(annot)
    
    doc.save(output_path)
    doc.close()
    print(f"Done! Saved to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python remove.py <input.pdf> <output.pdf> [mode]")
        print("  mode: 'image' (default) - converts to images and removes red pixels")
        print("        'annot' - removes red annotations only (preserves text quality)")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'image'
    
    if mode == 'annot':
        remove_red_annotations(input_pdf, output_pdf)
    else:
        remove_red_lines(input_pdf, output_pdf)
