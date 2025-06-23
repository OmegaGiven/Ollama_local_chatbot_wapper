"""
This module provides functionality to read PDF files using different libraries.
"""

config = "pymupdf"

def pdfplumber_read(uploaded_file):
    try:
        import pdfplumber
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    except ImportError:
        raise ImportError("pdfplumber is not installed. Please install it using 'pip install pdfplumber'.")


def pymupdf_read(uploaded_file):
    try:
        import pymupdf
        doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    except ImportError:
        raise ImportError("pymupdf is not installed. Please install it using 'pip install pymupdf'.")


pdf_read_switch = {
    "pdfplumber": pdfplumber_read,
    "pymupdf": pymupdf_read
}

def read_pdf(uploaded_file):
    """
    Reads a PDF file using the configured method.
    
    Args:
        uploaded_file: The PDF file to read.
    
    Returns:
        The text extracted from the PDF.
    """
    return pdf_read_switch[config](uploaded_file)