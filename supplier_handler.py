from selenium.webdriver.common.by import By
from config import SUPPLIER_CONFIGS
from utils import parse_currency
import time

def get_supplier_balances(driver):
    """Mengambil data saldo supplier yang ditargetkan dari semua halaman"""
    balances = []
    found_suppliers = set()
    
    try:
        # Reset status found untuk setiap supplier
        for supplier in SUPPLIER_CONFIGS:
            SUPPLIER_CONFIGS[supplier]['found'] = False
            
        while len(found_suppliers) < len(SUPPLIER_CONFIGS):
            rows = driver.find_elements(By.CSS_SELECTOR, "tr.el-table__row")
            
            for row in rows:
                try:
                    name = row.find_element(By.CSS_SELECTOR, "td.el-table_1_column_1 .cell").text.upper()
                    
                    if name in SUPPLIER_CONFIGS and not SUPPLIER_CONFIGS[name]['found']:
                        switch = row.find_element(By.CSS_SELECTOR, "td.el-table_1_column_4 .el-switch")
                        is_active = "is-checked" in switch.get_attribute("class")
                        
                        if is_active:
                            balance_element = row.find_element(By.CSS_SELECTOR, "td.el-table_1_column_2 .cell span")
                            balance_text = balance_element.text.strip()
                            balance = parse_currency(balance_text)
                            
                            balances.append({
                                "name": name,
                                "balance": balance,
                                "balance_text": balance_text,
                                "threshold": SUPPLIER_CONFIGS[name]['threshold']
                            })
                            found_suppliers.add(name)
                            SUPPLIER_CONFIGS[name]['found'] = True
                            
                except Exception as e:
                    print(f"❌ Error saat memproses supplier: {str(e)}")
            
            if len(found_suppliers) < len(SUPPLIER_CONFIGS):
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "button.btn-next")
                    if "disabled" not in next_button.get_attribute("class"):
                        next_button.click()
                        time.sleep(2)
                    else:
                        break
                except:
                    break
                    
    except Exception as e:
        print(f"❌ Error saat mengambil data supplier: {str(e)}")
        
    missing_suppliers = set(SUPPLIER_CONFIGS.keys()) - found_suppliers
    if missing_suppliers:
        print(f"⚠️ Supplier tidak ditemukan: {', '.join(missing_suppliers)}")
        
    return balances