def format_currency(amount):
    """Format angka ke format mata uang Indonesia"""
    try:
        return f"Rp {int(amount):,}"
    except:
        return amount

def parse_currency(currency_str):
    """Mengubah string mata uang ke integer"""
    try:
        clean_number = currency_str.replace('Rp', '').replace('.', '').strip()
        return int(clean_number)
    except:
        return 0