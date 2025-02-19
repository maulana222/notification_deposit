from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from config import SUPPLIER_CONFIGS
from utils import parse_currency, should_notify, show_notification

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def login(driver, email, password, otp_code):
    driver.get("https://example.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password, Keys.RETURN)
    time.sleep(3)
    driver.find_element(By.ID, "otp").send_keys(otp_code, Keys.RETURN)
    time.sleep(5)
    print("✅ Login berhasil!")

def get_supplier_balances(driver):
    balances = []
    for supplier in SUPPLIER_CONFIGS:
        SUPPLIER_CONFIGS[supplier]['found'] = False
    
    rows = driver.find_elements(By.CSS_SELECTOR, "tr.el-table__row")
    for row in rows:
        try:
            name = row.find_element(By.CSS_SELECTOR, "td.el-table_1_column_1 .cell").text.upper()
            if name in SUPPLIER_CONFIGS and not SUPPLIER_CONFIGS[name]['found']:
                balance_text = row.find_element(By.CSS_SELECTOR, "td.el-table_1_column_2 .cell span").text.strip()
                balance = parse_currency(balance_text)
                balances.append({"name": name, "balance": balance, "balance_text": balance_text})
                SUPPLIER_CONFIGS[name]['found'] = True
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    return balances