import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_data_from_rows(driver):
    # Ana div'i bul
    main_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/div[3]/div/div"))
    )
    # Sadece class="row" olan ve ng-scope içermeyen div'leri seç
    rows = main_div.find_elements(By.XPATH, ".//div[(@class='row') or (@class='row ' and not(contains(@class, 'row ng-scope')))]")
    
    data = {}
    labels = ['Name','DBA', 'License Type', 'License Expiration', 'City', 'County', 'Zip Code', 'Telephone', 'mail', 'Hours']
    sayac=1
    for i, row in enumerate(rows):
        if i >= len(labels):
            break
        value = row.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/div[3]/div/div/div[{sayac}]").text.strip()
        if "Street Address:" in value:    
            sayac=sayac+1
            value = row.find_element(By.XPATH, f"/html/body/div[3]/div/div[2]/div[3]/div/div/div[{sayac}]").text.strip()
        
        data[labels[i]] = value
        sayac=sayac+1
    return data

def find_view_buttons():
    return WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//table-builder//tbody//tr//td[7]/a"))
    )

def find_next_button(page):
    if page == 1:
        xpath = "/html/body/div[3]/div/div[2]/div/div[2]/ul/li[1]/button"
    else:
        xpath = "/html/body/div[3]/div/div[2]/div/div[2]/ul/li[3]/button"
    return WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )

def navigate_to_page(driver, target_page):
    current_page = 1
    while current_page < target_page:
        next_button = find_next_button(current_page)
        next_button.click()
        time.sleep(3)  # Sayfanın yüklenmesi için bekle
        current_page += 1
    print(f"Sayfa {target_page}'e gidildi.")

def process_page(driver, page_number):
    data = []
    print(f"Sayfa {page_number} işleniyor...")
    
    view_buttons = find_view_buttons()
    total_buttons = len(view_buttons)

    for i in range(total_buttons):
        try:
            view_buttons = find_view_buttons()
            view_buttons[i].click()
            print(f"Sayfa {page_number}, {i+1}. View butonuna tıklandı")
            
            time.sleep(3)
            
            # Verileri çek
            row_data = get_data_from_rows(driver)
            data.append(row_data)

            # Geri butonuna tıkla
            geri = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div/div[1]/a"))
            )
            geri.click()
            print("Geri butonuna tıklandı")
            
            time.sleep(3)
            
            # Sayfayı yeniden yükle ve gerekli sayfaya git
            driver.refresh()
            time.sleep(3)
            navigate_to_page(driver, page_number)

        except Exception as e:
            print(f"Sayfa {page_number}, {i+1}. butonda hata oluştu: {e}")
            driver.refresh()
            time.sleep(3)
            navigate_to_page(driver, page_number)

    return data

# Ana döngü
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://omma.us.thentiacloud.net/webs/omma/register/#/business/search/all/Dispensary")
time.sleep(3)

all_data = []
current_page = 1
total_records = 1937
records_per_page = 20

while len(all_data) < total_records:
    page_data = process_page(driver, current_page)
    all_data.extend(page_data)
    
    # Excel'e kaydet
    df = pd.DataFrame(all_data)
    df.to_excel('omma_data.xlsx', index=False)
    print(f"Toplam {len(all_data)} veri Excel'e kaydedildi.")
    
    if len(all_data) < total_records:
        try:
            next_button = find_next_button(current_page)
            next_button.click()
            print(f"Sayfa {current_page} tamamlandı. Sonraki sayfaya geçiliyor...")
            current_page += 1
            time.sleep(5)  # Yeni sayfanın yüklenmesi için bekle
        except Exception as e:
            print(f"Sonraki sayfaya geçerken hata oluştu: {e}")
            break
    else:
        print("Tüm veriler toplandı.")
        break

print(f"Toplam {len(all_data)} veri toplandı ve Excel'e kaydedildi.")


# Kullanıcı girişi bekle
input("Tarayıcıyı kapatmak için Enter tuşuna basın...")

# Tarayıcıyı kapat
driver.quit()

