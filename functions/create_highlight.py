import os
import fitz  # PyMuPDF
from PIL import Image, ImageDraw

# Function to highlight text in PDF with a red box
def highlight_pdf(file_path, highlight_coords):
    doc = fitz.open(file_path)
    for coord in highlight_coords:
        page = doc.load_page(coord['pageNumber'] - 1)
        rect = fitz.Rect(coord['polygon'][0] * 72, coord['polygon'][1] * 72, coord['polygon'][4] * 72, coord['polygon'][5] * 72)
        annot = page.add_rect_annot(rect)
        annot.set_colors(stroke=(1, 0, 0))  # Red color
        annot.set_border(width=4)  # Border width
        annot.update()

    highlighted_file_path = os.path.join(os.getcwd(), "documents", "temp.pdf")

    # highlighted_file_path = "documents/temp.pdf"
    try:
        doc.save(highlighted_file_path)
    except Exception as e:
        print(f"Error saving PDF: {e}")
    return highlighted_file_path

# Function to highlight text in IMG with a red box
def highlight_img(file_path, highlight_coords):
    # Open the PNG image
    image = Image.open(file_path)
    
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Iterate over the highlight coordinates
    for highlight in highlight_coords:
        polygon = highlight['polygon']
        
        # Convert polygon to rectangle
        x0, y0, x1, y1 = polygon[0], polygon[1], polygon[4], polygon[5]
        
        # Draw a rectangle with a semi-transparent fill
        draw.rectangle([x0, y0, x1, y1], outline="red", width=4)
    
    # get file type from the file path
    file_type = file_path.split(".")[-1]

    output_png_path = os.path.join(os.getcwd(), "documents", f"temp.{file_type}")
    image.save(output_png_path)
    return output_png_path
