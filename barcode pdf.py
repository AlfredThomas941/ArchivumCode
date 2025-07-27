import os
import io
from datetime import datetime
from barcode import Code128
from barcode.writer import ImageWriter
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import pdfminer.high_level
import pdfminer.layout

BARCODE_LOG_FILE = "last_barcode.txt"

def generate_barcode(product_id):
    """Generate barcode as PNG bytes with adjusted text spacing"""
    buff = io.BytesIO()
    Code128(product_id, writer=ImageWriter()).write(buff, {
        'module_width': 0.3,
        'module_height': 10,
        'font_size': 10,
        'text_distance': 8,  # Increased space between bars and text
        'quiet_zone': 2.0,
        'background': 'white',
        'foreground': 'black',
        'write_text': True
    })
    buff.seek(0)
    return buff

def detect_text_and_image_regions(pdf_path):
    """Detect both text and image regions per page using pdfminer"""
    laparams = pdfminer.layout.LAParams()
    all_regions = []

    with open(pdf_path, "rb") as fp:
        for page_layout in pdfminer.high_level.extract_pages(fp, laparams=laparams):
            regions = []

            for element in page_layout:
                if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                    regions.append((element.x0, element.y0, element.x1, element.y1))
                elif isinstance(element, pdfminer.layout.LTFigure):
                    for sub_elem in element:
                        if hasattr(sub_elem, "x0") and hasattr(sub_elem, "y0") and hasattr(sub_elem, "x1") and hasattr(sub_elem, "y1"):
                            regions.append((sub_elem.x0, sub_elem.y0, sub_elem.x1, sub_elem.y1))

            all_regions.append(regions)
    return all_regions

def is_region_free(x, y, w, h, text_regions):
    """Check if a region overlaps with any region in text_regions"""
    for tx0, ty0, tx1, ty1 in text_regions:
        if not (x + w < tx0 or x > tx1 or y + h < ty0 or y > ty1):
            return False
    return True

def add_barcodes_per_page(input_path, output_path, base_id, start_number):
    """Add unique barcodes to each page without overlapping text/images"""
    original_pdf = PdfReader(input_path)
    output_pdf = PdfWriter()
    text_regions_per_page = detect_text_and_image_regions(input_path)

    barcode_width = 100
    barcode_height = 50
    margin = 10

    for i, page in enumerate(original_pdf.pages):
        page_number = start_number + i
        barcode_id = f"{base_id}{page_number:03d}"
        barcode_buffer = generate_barcode(barcode_id)
        barcode_image = Image.open(barcode_buffer)
        temp_barcode_path = f"temp_barcode_{i}.png"
        barcode_image.save(temp_barcode_path)

        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        text_regions = text_regions_per_page[i]

        positions = [
            (margin, margin),
            (width - barcode_width - margin, margin),
            (margin, height - barcode_height - margin),
            (width - barcode_width - margin, height - barcode_height - margin),
            ((width - barcode_width) / 2, margin),
            ((width - barcode_width) / 2, height - barcode_height - margin),
        ]

        for x, y in positions:
            if is_region_free(x, y, barcode_width, barcode_height, text_regions):
                break
        else:
            x, y = margin, margin

        overlay = io.BytesIO()
        c = canvas.Canvas(overlay, pagesize=(width, height))
        c.drawImage(
            ImageReader(temp_barcode_path),
            x, y,
            width=barcode_width,
            height=barcode_height,
            mask=[255, 255, 255, 255, 255, 255]
        )
        c.save()
        overlay.seek(0)

        watermark_pdf = PdfReader(overlay)
        page.merge_page(watermark_pdf.pages[0])
        output_pdf.add_page(page)
        os.remove(temp_barcode_path)

    with open(output_path, "wb") as out:
        output_pdf.write(out)

def get_last_barcode_number():
    if os.path.exists(BARCODE_LOG_FILE):
        with open(BARCODE_LOG_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_barcode_number(barcode_id):
    with open(BARCODE_LOG_FILE, "w") as f:
        f.write(barcode_id)

def main():
    print("=== Unique Barcode Adder ===\n")

    last_barcode = get_last_barcode_number()
    if last_barcode:
        print(f"📌 Last used barcode: {last_barcode}")
    else:
        print("📌 No previous barcode used.")

    input_pdf = input("Drag your PDF here or enter path: ").strip('"')
    while not os.path.exists(input_pdf):
        input_pdf = input("❌ File not found. Try again: ").strip('"')

    dir_name, file_name = os.path.split(input_pdf)
    output_pdf = os.path.join(dir_name, f"barcoded_{file_name}")

    today = datetime.now().strftime("%d%m%y")
    category = input("Enter category (1-4): ")
    while category not in ['1', '2', '3', '4']:
        category = input("Invalid. Enter 1-4: ")

    base_id = f"{today[:4]}{today[-1]}{category}"

    last_number = int(last_barcode[-3:]) if last_barcode and last_barcode.startswith(base_id) else 0
    print(f"➡️ Starting from: {last_number + 1:03d}")
    start_input = input(f"Enter starting product number [default: {last_number + 1:03d}]: ")

    try:
        start_number = int(start_input) if start_input else last_number + 1
    except ValueError:
        start_number = last_number + 1

    try:
        add_barcodes_per_page(input_pdf, output_pdf, base_id, start_number)
        final_number = start_number + len(PdfReader(input_pdf).pages) - 1
        new_barcode_id = f"{base_id}{final_number:03d}"
        save_last_barcode_number(new_barcode_id)

        print(f"\n✅ Barcodes added to all pages of: {output_pdf}")
        print(f"🆔 Last barcode used: {new_barcode_id}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("Ensure:")
        print("- PDF isn't password protected")
        print("- You have permission to write")
        print("- Required packages are installed:\n  pip install python-barcode pillow pypdf2 reportlab pdfminer.six")

if __name__ == "__main__":
    main()
