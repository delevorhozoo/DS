import time
import subprocess
import itertools # Untuk membuat counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# --- PENGATURAN UTAMA ---
# !!! PERINGATAN: Jangan menurunkan nilai ini terlalu rendah !!!
# Risiko pemblokiran akan meningkat drastis jika jeda terlalu singkat.
# 300 detik = 5 menit. Ini adalah nilai yang relatif lebih aman.
DELAY_BETWEEN_REPORTS = 300 

# --- FUNGSI UNTUK MENDAPATKAN PATH CHROMIUM DAN DRIVER ---
def get_chromedriver_path():
    """Mencari path chromedriver yang terinstal di Termux."""
    try:
        path = subprocess.check_output(['which', 'chromedriver']).decode('utf-8').strip()
        return path
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: chromedriver tidak ditemukan. Pastikan Anda sudah menjalankan 'apt install chromium -y '.")
        return None

# --- KONFIGURASI WEBDRIVER ---
def setup_driver():
    """Mengatur dan menjalankan WebDriver Chromium dalam mode headless."""
    chromedriver_path = get_chromedriver_path()
    if not chromedriver_path:
        return None

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# --- PROSES UTAMA PELAPORAN ---
def laporkan_username(username, alasan, driver):
    """Fungsi untuk mengunjungi profil dan mengirimkan SATU laporan."""
    # --- KAMUS ALUR PELAPORAN ---
    report_flows = {
        "scam": {
            "description": "Penipuan atau Scam",
            "steps": [
                "//div[contains(text(), 'Report account')]",
                "//div[contains(text(), 'Scam and fraud')]",
                "//div[contains(text(), 'Financial scam')]"
            ]
        },
        "porn": {
            "description": "Pornografi atau Konten Seksual",
            "steps": [
                "//div[contains(text(), 'Report account')]",
                "//div[contains(text(), 'Nudity and sexual activities')]"
            ]
        },
        "hate": {
            "description": "Ujaran Kebencian",
            "steps": [
                "//div[contains(text(), 'Report account')]",
                "//div[contains(text(), 'Hate speech or symbols')]"
            ]
        },
        "bullying": {
            "description": "Bully atau Pelecehan",
            "steps": [
                "//div[contains(text(), 'Report account')]",
                "//div[contains(text(), 'Harassment or bullying')]"
            ]
        },
        "minor": {
            "description": "Akun di bawah umur",
            "steps": [
                "//div[contains(text(), 'Report account')]",
                "//div[contains(text(), 'Minor safety')]"
            ]
        }
    }

    try:
        url = f"https://www.tiktok.com/@{username}"
        print(f"Membuka halaman profil: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 20)

        more_button_selector = "[data-e2e='profile-more-options']"
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, more_button_selector))).click()

        report_option_selector = "//div[contains(text(), 'Report')]"
        wait.until(EC.element_to_be_clickable((By.XPATH, report_option_selector))).click()

        if alasan.lower() not in report_flows:
            print(f"ERROR: Alasan '{alasan}' tidak valid.")
            return False # Gagal

        flow = report_flows[alasan.lower()]
        print(f"Mengikuti alur untuk: {flow['description']}")

        for selector in flow['steps']:
            wait.until(EC.element_to_be_clickable((By.XPATH, selector))).click()
            # Tidak ada delay di sini agar proses satu laporan secepat mungkin

        submit_button_selector = "//button[@type='submit']"
        wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_selector))).click()
        
        print("✅ Laporan berhasil dikirim!")
        return True # Berhasil

    except (TimeoutException, WebDriverException) as e:
        print(f"\n!!! GAGAL mengirim laporan. Error: {e}")
        print("Kemungkinan halaman berubah, jaringan lambat, atau IP sudah diblokir.")
        return False # Gagal

# --- EKSEKUSI SKRIP ---
if __name__ == "__main__":
    print("--- TikTok Report Tool (Loop Mode - VERY HIGH RISK) ---")
    username_to_report = input("Masukkan username yang ingin dilaporkan (tanpa '@'): ")
    
    print("\nPilih alasan pelaporan:")
    print("  scam  - Penipuan atau Scam")
    print("  porn  - Pornografi atau Konten Seksual")
    print("  hate  - Ujaran Kebencian")
    print("  bully - Bully atau Pelecehan")
    print("  minor - Akun di bawah umur")
    
    reason_to_report = input("Masukkan kode alasan (misal: scam): ")

    if not username_to_report or not reason_to_report:
        print("Username atau alasan tidak boleh kosong.")
    else:
        # Setup driver SATU KALI di luar loop
        driver = setup_driver()
        if not driver:
            print("Gagal menginisialisasi browser. Keluar.")
        else:
            print(f"\n--- MEMULAI LOOP PELAPORAN ---")
            print(f"Setiap laporan akan memiliki jeda {DELAY_BETWEEN_REPORTS} detik ({DELAY_BETWEEN_REPORTS/60} menit).")
            print("Tekan CTRL+C untuk menghentikan script.")
            time.sleep(3) # Jeda sebelum mulai loop

            try:
                # Loop tak terbatas
                for i in itertools.count(start=1):
                    print(f"\n========== Laporan ke-{i} ==========")
                    success = laporkan_username(username_to_report, reason_to_report, driver)
                    
                    if not success:
                        print("Laporan gagal. Mencoba lagi dalam 1 menit...")
                        time.sleep(60) # Jeda lebih singkat jika gagal, mungkin hanya masalah sesaat

                    print(f"\nMenunggu {DELAY_BETWEEN_REPORTS} detik sebelum laporan berikutnya...")
                    time.sleep(DELAY_BETWEEN_REPORTS)

            except KeyboardInterrupt:
                print("\n\n--- Script dihentikan oleh pengguna. ---")
            finally:
                print("Menutup browser.")
                driver.quit()
