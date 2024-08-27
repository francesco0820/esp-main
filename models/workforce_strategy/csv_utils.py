import pandas as pd
import unicodedata

def read_csv(file_path):
    return pd.read_csv(file_path)

def write_csv(df, file_path):
    df.to_csv(file_path, index=False)

special_char_replacements = {
    'â€™': "'",  # Curly apostrophe
    'â€œ': '"',  # Left double quotation mark
    'â€': '"',   # Right double quotation mark
    'â€”': '-',  # Em Dash
    'â€“': '-',  # En Dash
    'â€¢': '*',  # Bullet
    'Â': ' '
}

def clean_text(text):
    if isinstance(text, str):
        for unicode_char, ascii_char in special_char_replacements.items():
            text = text.replace(unicode_char, ascii_char)
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text