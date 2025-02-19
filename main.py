from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

from config import LOGIN_CONFIG, TIME_CONFIG, SUPPLIER_CONFIGS
from utils import format_currency
from notification_handler import show_notification, should_notify
from supplier_handler import get_supplier_balances

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        # Login process
        driver.get(LOGIN_CONFIG['url'])
        time.sleep(TIME_CONFIG['page_load_wait'])

        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(LOGIN_CONFIG['email'])

        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(LOGIN_CONFIG['password'])
        password_input.send_keys(Keys.RETURN)
        time.sleep(TIME_CONFIG['login_wait'])

        otp_code = input("Masukkan kode OTP Google Authenticator: ")
        otp_input = driver.find_element(By.ID, "otp")
        otp_input.send_keys(otp_code)
        otp_input.send_keys(Keys.RETURN)
        time.sleep(TIME_CONFIG['otp_wait'])

        print("✅ Login berhasil!")

        supplier_menu = driver.find_element(By.XPATH, "//a[@href='/admin/supplier']")
        supplier_menu.click()
        time.sleep(TIME_CONFIG['page_load_wait'])
        
        while True:
            print("\n🔄 Memperbarui data saldo...")
            supplier_balances = get_supplier_balances(driver)
            current_time = datetime.now().strftime('%H:%M:%S')
            
            print(f"📊 Monitoring {len(supplier_balances)} supplier target (Waktu: {current_time}):")
            for supplier in supplier_balances:
                print(f"💰 {supplier['name']}: {supplier['balance_text']} (Batas: {format_currency(supplier['threshold'])})")
                
                if supplier['balance'] < supplier['threshold']:
                    if should_notify(supplier['name'], supplier['balance']):
                        notification_title = f"⚠️ Saldo Rendah - {supplier['name']}"
                        notification_message = (
                            f"Saldo saat ini: {supplier['balance_text']}\n"
                            f"Di bawah batas minimum: {format_currency(supplier['threshold'])}"
                        )
                        show_notification(
                            notification_title,
                            notification_message,
                            supplier['name'],
                            supplier['balance']
                        )
                else:
                    # Reset notification count jika saldo sudah di atas threshold
                    SUPPLIER_CONFIGS[supplier['name']]['notification_count'] = 0
                    SUPPLIER_CONFIGS[supplier['name']]['last_notification'] = None
                    SUPPLIER_CONFIGS[supplier['name']]['next_check'] = None
            
            # Tunggu sebelum refresh
            print("\n⏳ Menunggu 10 detik sebelum pembaruan berikutnya...")
            time.sleep(TIME_CONFIG['refresh_interval'])
            driver.refresh()
            time.sleep(TIME_CONFIG['page_load_wait'])

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {str(e)}")
        show_notification("❌ Error", f"Terjadi kesalahan: {str(e)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()