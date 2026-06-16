import logging
from pathlib import Path
import pypdf

logger = logging.getLogger(__name__)

class PDFExtractor:
    """Class responsible for extracting and cleaning text from PDF files."""

    @staticmethod
    def extract_text(pdf_path: Path, max_chars: int = 120000) -> str:
        """
        Extracts and cleans text from a PDF file.
        Truncates the output to `max_chars` for API efficiency.
        """
        if not pdf_path.exists():
            logger.warning(f"PDF file not found: {pdf_path}")
            return ""

        try:
            reader = pypdf.PdfReader(pdf_path)
            extracted_pages = []
            char_count = 0

            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                # Simple normalization of whitespace
                normalized_text = " ".join(text.split())
                extracted_pages.append(normalized_text)
                char_count += len(normalized_text)
                
                # Check character count threshold
                if char_count >= max_chars:
                    logger.info(f"Reached max character limit ({max_chars}) at page {i+1} of {pdf_path.name}")
                    break

            full_text = "\n\n".join(extracted_pages)
            return full_text[:max_chars]

        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}", exc_info=True)
            return ""
