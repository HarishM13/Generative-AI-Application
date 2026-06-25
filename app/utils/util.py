import re
def clean_text(text: str) -> str:
    """
    Data Cleaning Pipeline: Removes junk text artifacts, fixes whitespaces, 
    and handles broken character formatting.
    """
    if not text:
        return ""
    # 1. Remove non-printable/control characters (junk byte strings)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
    # 2. Standardize multiple repeating line breaks or tab gaps down to a single space/line
    text = re.sub(r' +', ' ', text)  # Collapse multiple spaces
    text = re.sub(r'\n\s*\n+', '\n', text)  # Collapse multiple empty lines
    # 3. Clean up common structural junk text artifacts (e.g., repeating dashes, underscores, or HTML tags)
    text = re.sub(r'[-_=]{3,}', '', text) 
    text = re.sub(r'<[^>]*>', '', text)  # Strip occasional HTML residue
    return text.strip()