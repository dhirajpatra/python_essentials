from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import inch
import os

def reformat_pdf(input_pdf_path, output_pdf_path, max_chars_per_line, lines_per_page):
    """
    Reads a PDF, reformats the text content with a specified character limit per line
    and lines per page, and saves the output to a new PDF file.

    :param input_pdf_path: Path to the input PDF file
    :param output_pdf_path: Path to save the output PDF file
    :param max_chars_per_line: Maximum number of characters allowed per line
    :param lines_per_page: Number of lines allowed per page
    """
    # Check if the input file exists
    if not os.path.exists(input_pdf_path):
        print(f"Error: File {input_pdf_path} does not exist.")
        return

    # Read the input PDF
    reader = PdfReader(input_pdf_path)
    text_content = ""

    # Extract text from all pages
    for page in reader.pages:
        text_content += page.extract_text() + " "

    # Split the text into words
    words = text_content.split()

    # Create lines while respecting the character limit and avoiding word breaks
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars_per_line:  # +1 accounts for the space
            current_line += (word + " ")
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:  # Add the last line if not empty
        lines.append(current_line.strip())

    # Create a new PDF with the formatted text
    page_width = 3.5 * inch
    page_height = 5.5 * inch
    c = canvas.Canvas(
        output_pdf_path,
        pagesize=(page_width, page_height),
        initialFontSize=10
    )

    # Initialize y-position and line counter
    margin_top = 20  # Top margin in points
    margin_left = 10  # Left margin in points
    line_height = 14  # Line height in points
    y_position = page_height - margin_top
    current_line_count = 0

    for line in lines:
        # If the current line count exceeds the allowed lines per page, start a new page
        if current_line_count >= lines_per_page:
            c.showPage()
            y_position = page_height - margin_top
            current_line_count = 0

        # Write the line on the canvas
        c.drawString(margin_left, y_position, line.strip())
        y_position -= line_height
        current_line_count += 1

    # Save the new PDF
    c.save()
    print(f"Reformatted PDF saved as {output_pdf_path}")

# Example usage
if __name__ == "__main__":
    input_pdf = input("Enter the path to the input PDF file: ").strip()
    output_pdf = input("Enter the path to save the output PDF file: ").strip()
    max_chars_per_line = 42  # Max characters per line
    lines_per_page = 27  # Max lines per page

    reformat_pdf(input_pdf, output_pdf, max_chars_per_line, lines_per_page)
