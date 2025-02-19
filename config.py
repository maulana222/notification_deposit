import locale
from datetime import timedelta

# Set locale untuk format mata uang Indonesia
locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

# Konfigurasi supplier dan batas saldo minimum
SUPPLIER_CONFIGS = {
    'BIJUR': {
        'threshold': 3000000,  # 3 juta
        'found': False,
        'last_notification': None,
        'notification_count': 0,
        'next_check': None
    },
    'KURNIA': {
        'threshold': 3000000,  # 3 juta
        'found': False,
        'last_notification': None,
        'notification_count': 0,
        'next_check': None
    }
}

# Konfigurasi login
LOGIN_CONFIG = {
    'url': 'https://digipro-sb-gkrbvw.digiswitch.id/login',
    'email': 'ergialipfalah@gmail.com',
    'password': 'IntelCorei7'
}

# Konfigurasi waktu
TIME_CONFIG = {
    'page_load_wait': 2,
    'login_wait': 3,
    'otp_wait': 5,
    'refresh_interval': 10
}

def get_notification_interval(notification_count):
    """Menentukan interval notifikasi berdasarkan jumlah notifikasi"""
    if notification_count == 0:
        return timedelta(seconds=0)  # Notifikasi pertama langsung
    elif notification_count == 1:
        return timedelta(minutes=2)  # Notifikasi kedua setelah 2 menit
    else:
        return timedelta(minutes=1)  # Notifikasi selanjutnya setiap 1 menit