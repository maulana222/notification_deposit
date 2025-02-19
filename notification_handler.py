from datetime import datetime
from plyer import notification
from config import SUPPLIER_CONFIGS, get_notification_interval

def should_notify(supplier_name, current_balance):
    """Menentukan apakah perlu mengirim notifikasi"""
    supplier = SUPPLIER_CONFIGS[supplier_name]
    current_time = datetime.now()
    
    # Jika belum pernah ada notifikasi atau belum ada jadwal pengecekan berikutnya
    if supplier['last_notification'] is None or supplier['next_check'] is None:
        return True
        
    # Jika sudah waktunya pengecekan berikutnya
    if current_time >= supplier['next_check']:
        return True
        
    return False

def show_notification(title, message, supplier_name=None, current_balance=None):
    """Menampilkan notifikasi desktop dan update status notifikasi"""
    notification.notify(
        title=title,
        message=message,
        app_icon=None,
        timeout=10,
    )
    
    if supplier_name and supplier_name in SUPPLIER_CONFIGS:
        # Update status notifikasi
        current_time = datetime.now()
        supplier = SUPPLIER_CONFIGS[supplier_name]
        supplier['last_notification'] = current_time
        supplier['notification_count'] += 1
        
        # Hitung waktu pengecekan berikutnya
        interval = get_notification_interval(supplier['notification_count'])
        supplier['next_check'] = current_time + interval
        
        # Log informasi notifikasi
        next_check_str = supplier['next_check'].strftime('%H:%M:%S')
        print(f"📢 Notifikasi ke-{supplier['notification_count']} untuk {supplier_name}")
        print(f"⏰ Pengecekan berikutnya: {next_check_str}")